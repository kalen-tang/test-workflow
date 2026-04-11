#!/usr/bin/env python3
import json, sys, subprocess, os, time, tempfile, re
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(sys.stdin)
session_id = data.get('session_id', '')
model = data['model']['display_name']
directory = os.path.basename(data['workspace']['current_dir'])
cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0
api_duration_ms = data.get('cost', {}).get('total_api_duration_ms', 0) or 0
lines_added = data.get('cost', {}).get('total_lines_added', 0) or 0
lines_removed = data.get('cost', {}).get('total_lines_removed', 0) or 0

ctx = data.get('context_window') or {}
current_usage = ctx.get('current_usage')

if isinstance(current_usage, (int, float)):
    used_tokens = max(0, current_usage)
    input_tokens = used_tokens
    output_tokens = 0
elif isinstance(current_usage, dict):
    input_tokens = max(0, current_usage.get('input_tokens') or 0)
    output_tokens = max(0, current_usage.get('output_tokens') or 0)
    cache_creation = max(0, current_usage.get('cache_creation_input_tokens') or 0)
    cache_read = max(0, current_usage.get('cache_read_input_tokens') or 0)
    used_tokens = input_tokens + output_tokens + cache_creation + cache_read
    input_tokens = input_tokens + cache_creation + cache_read
    cached_tokens = cache_creation + cache_read
else:
    used_tokens = 0
    input_tokens = 0
    output_tokens = 0
    cached_tokens = 0

total_tokens = used_tokens

# Worktree 信息
worktree = data.get('worktree') or {}
wt_name = worktree.get('name', '')

# Thinking Effort（从 settings 读取）
thinking_effort = ''
try:
    settings_path = os.path.join(os.path.expanduser('~'), '.claude', 'settings.json')
    with open(settings_path, encoding='utf-8') as f:
        settings = json.load(f)
    if settings.get('alwaysThinkingEnabled'):
        thinking_effort = 'T'
except Exception:
    pass

# 模型名简化：去掉 " context" 后缀
model_display = re.sub(r'\s*context\s*', '', model)

# context window size：优先使用 JSON 字段，否则从模型名解析（如 "1M context"）
ctx_window_size = ctx.get('context_window_size')
if not (isinstance(ctx_window_size, (int, float)) and ctx_window_size > 0):
    ctx_window_size = None
    m = re.search(r'(?:[\(\[])\s*([\d,_.]+)\s*([kKmM])\s*(?:[\)\]])', model)
    if m:
        val = float(m.group(1).replace(',', '').replace('_', ''))
        unit = m.group(2).lower()
        ctx_window_size = int(val * (1_000_000 if unit == 'm' else 1_000))
    if not ctx_window_size:
        ctx_window_size = 200_000

# 百分比：优先使用 JSON 提供的 used_percentage
raw_used_pct = ctx.get('used_percentage')
if isinstance(raw_used_pct, (int, float)) and 0 <= raw_used_pct <= 100:
    pct = int(raw_used_pct)
else:
    # autocompact 阈值 = context_window_size × CLAUDE_AUTOCOMPACT_PCT_OVERRIDE%
    autocompact_pct_env = int(os.environ.get('CLAUDE_AUTOCOMPACT_PCT_OVERRIDE') or 100)
    autocompact_limit = int(ctx_window_size * autocompact_pct_env / 100)
    pct = int(used_tokens * 100 / autocompact_limit) if autocompact_limit else 0
    pct = min(pct, 100)

tokens_used_k = f"{used_tokens / 1000:.1f}"
tokens_limit_k = f"{ctx_window_size / 1000:.0f}"
tokens_str = f"{tokens_used_k}/{tokens_limit_k}k"

# Nord Truecolor 配色（标准 Nord 色板）
NORD_FROST  = '\033[38;2;136;192;208m'  # #88C0D0 霜蓝（模型）
NORD_GREEN  = '\033[38;2;163;190;140m'  # #A3BE8C 绿（正常）
NORD_YELLOW = '\033[38;2;235;203;139m'  # #EBCB8B 黄（警告）
NORD_RED    = '\033[38;2;191;97;106m'   # #BF616A 红（危险）
NORD_GRAY   = '\033[38;2;76;86;106m'    # #4C566A 灰（进度条空余）
NORD_PURPLE = '\033[38;2;180;142;173m'  # #B48EAD 紫（费用中等）
NORD_CACHE  = '\033[38;2;129;161;193m'  # #81A1C1 冰蓝（cache 色块）
RESET = '\033[0m'

bar_color   = NORD_RED if pct >= 90 else NORD_YELLOW if pct >= 70 else NORD_GREEN
CYAN, GREEN, YELLOW, RED, TEAL = NORD_FROST, NORD_GREEN, NORD_YELLOW, NORD_RED, NORD_GRAY
if pct >= 90:
    bar = '[建议压缩]'
    c1_bot_plain = '[建议压缩] {pct}%'
else:
    filled = pct // 10
    # cache 色块：从 filled 中分出 cache 占比
    cache_filled = min(filled, int(cached_tokens * 10 / ctx_window_size)) if ctx_window_size and cached_tokens else 0
    non_cache_filled = filled - cache_filled
    bar = '█' * non_cache_filled + f'{NORD_CACHE}' + '█' * cache_filled + f'{TEAL}' + '░' * (10 - filled) + f'{RESET}'
    c1_bot_plain = f"{'█' * filled}{'░' * (10 - filled)} {pct}%"

def fmt_duration(ms):
    total_secs = int(ms / 1000)
    h = total_secs // 3600
    m = (total_secs % 3600) // 60
    s = total_secs % 60
    return f"{h}:{m:02d}:{s:02d}"

duration_str = fmt_duration(duration_ms)
api_str = fmt_duration(api_duration_ms)

# Token 速度：基于增量计算，缓存上次值
TOK_CACHE_FILE = os.path.join(tempfile.gettempdir(), "statusline-tok-cache")
tok_per_sec = None

try:
    with open(TOK_CACHE_FILE, encoding='utf-8') as f:
        cached = json.load(f)
    if cached.get('session_id') != session_id:
        cached = None
except Exception:
    cached = None

if cached:
    delta_api_ms = api_duration_ms - cached['api_duration_ms']
    delta_output = output_tokens - cached['output_tokens']
    if delta_api_ms > 0 and delta_output > 0:
        tok_per_sec = delta_output / (delta_api_ms / 1000)
    else:
        tok_per_sec = cached.get('last_tok_per_sec')

try:
    with open(TOK_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'session_id': session_id,
            'api_duration_ms': api_duration_ms,
            'output_tokens': output_tokens,
            'last_tok_per_sec': tok_per_sec if tok_per_sec else None,
        }, f)
except Exception:
    pass

# Git info with 5-second cache
CACHE_FILE = os.path.join(tempfile.gettempdir(), "statusline-git-cache")
CACHE_MAX_AGE = 5

def cache_is_stale():
    if not os.path.exists(CACHE_FILE):
        return True
    return time.time() - os.path.getmtime(CACHE_FILE) > CACHE_MAX_AGE

if cache_is_stale():
    try:
        subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
        branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True, stderr=subprocess.DEVNULL).strip()
        status_out = subprocess.check_output(
            ['git', '--no-optional-locks', 'status', '--porcelain', '-z'],
            text=True, stderr=subprocess.DEVNULL
        )
        staged = 0
        modified = 0
        untracked = 0
        if status_out:
            entries = status_out.split('\0')
            i = 0
            while i < len(entries):
                e = entries[i]
                if len(e) >= 2:
                    idx_status, wt_status = e[0], e[1]
                    if idx_status in 'MADRCTU':
                        staged += 1
                    if wt_status in 'MADRCTU':
                        modified += 1
                    if e[:2] == '??':
                        untracked += 1
                    # rename/copy 有额外路径条目，跳过
                    if idx_status in ('R', 'C'):
                        i += 1
                i += 1
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            f.write(f"{branch}|{staged}|{modified}|{untracked}")
    except Exception:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            f.write("||0|0")

try:
    with open(CACHE_FILE, encoding='utf-8') as f:
        parts = f.read().strip().split('|')
    branch = parts[0]
    staged = parts[1] if len(parts) > 1 else "0"
    modified = parts[2] if len(parts) > 2 else "0"
    untracked = parts[3] if len(parts) > 3 else "0"
except Exception:
    branch, staged, modified, untracked = "", "0", "0", "0"

git_changes = ""
if branch:
    if int(staged) > 0:
        git_changes += f" {GREEN}+{staged}{RESET}"
    if int(modified) > 0:
        git_changes += f" {YELLOW}~{modified}{RESET}"
    if int(untracked) > 0:
        git_changes += f" {YELLOW}?{untracked}{RESET}"
    if lines_added > 0 or lines_removed > 0:
        git_changes += f" {GREEN}+{lines_added}{RESET}/{RED}-{lines_removed}{RESET}"

ansi_escape = re.compile(r'\033\[[0-9;]*m')

def vlen(s):
    s = ansi_escape.sub('', s)
    w = 0
    for c in s:
        w += 2 if ord(c) > 0x2E7F else 1
    return w

def rpad(s, width):
    return s + ' ' * max(0, width - vlen(s))

# 四列结构，两行竖线对齐
# 列1: 模型 / 进度条+百分比
# 列2: 📁 目录 / token
# 列3: 🌿 branch / 💰 费用
# 列4: (空) / ⏱️ 时长

# 计算各列内容（纯文本，用于宽度计算）
model_label = model_display
if thinking_effort:
    model_label += f" [{thinking_effort}]"
c1_top_plain = f"[{model_label}]"

c2_top_plain = f"📁 {directory}"
c2_bot_plain = f"📊 {tokens_str}"

lines_info = f' +{lines_added}/-{lines_removed}' if (lines_added > 0 or lines_removed > 0) else ''
c3_top_plain = f"🌿 {branch}{' +'+staged if int(staged)>0 else ''}{' ~'+modified if int(modified)>0 else ''}{' ?'+untracked if int(untracked)>0 else ''}{lines_info}" if branch else ""
c3_bot_plain = f"💰 ${cost:.2f}"

# 虚拟环境 / Worktree
venv = os.environ.get('VIRTUAL_ENV') or os.environ.get('CONDA_DEFAULT_ENV') or ''
venv_name = os.path.basename(venv) if venv else ''
if wt_name:
    c4_top_plain = f"🌲 {wt_name}"
elif venv_name:
    c4_top_plain = f"({venv_name})"
else:
    c4_top_plain = ""
c4_bot_plain = f"⏱️ {duration_str} [api {api_str}]"

# 每列宽度 = max(top, bot) 内容宽度，设最小宽度
col_widths = [
    max(vlen(c1_top_plain), vlen(c1_bot_plain), 13),
    max(vlen(c2_top_plain), vlen(c2_bot_plain), 14),
    max(vlen(c3_top_plain), vlen(c3_bot_plain), 10),
]

# 带颜色的内容
c1_top = f"{CYAN}[{model_label}]{RESET}"
c1_bot = f"{bar_color}{bar}{RESET} {pct}%"

c2_top = f"📁 {directory}"
c2_bot = f"📊 {bar_color}{tokens_str}{RESET}"

branch_color = GREEN if branch in ('master', 'main') else YELLOW
c3_top = f"🌿 {branch_color}{branch}{RESET}{git_changes}" if branch else ""
cost_color = RED if cost > 25 else NORD_PURPLE if cost > 10 else GREEN
c3_bot = f"{cost_color}💰 ${cost:.2f}{RESET}"

if wt_name:
    c4_top = f"{CYAN}🌲 {wt_name}{RESET}"
elif venv_name:
    c4_top = f"{CYAN}({venv_name}){RESET}"
else:
    c4_top = ""
if tok_per_sec and tok_per_sec >= 1000:
    tok_per_sec_str = f"⚡ {tok_per_sec / 1000:.1f}k t/s"
elif tok_per_sec:
    tok_per_sec_str = f"⚡ {tok_per_sec:.1f} t/s"
else:
    tok_per_sec_str = ""
c4_bot = f"⏱️ {duration_str} [api {api_str}]{('  ' + tok_per_sec_str) if tok_per_sec_str else ''}"

line1 = (
    f"{rpad(c1_top, col_widths[0])} | "
    f"{rpad(c2_top, col_widths[1])} | "
    f"{rpad(c3_top, col_widths[2])} | "
    f"{c4_top}"
)
line2 = (
    f"{rpad(c1_bot, col_widths[0])} | "
    f"{rpad(c2_bot, col_widths[1])} | "
    f"{rpad(c3_bot, col_widths[2])} | "
    f"{c4_bot}"
)

# 用 non-breaking space 替换普通空格，防止终端/VSCode trim 导致列宽错乱（色块散落）
# 行首加 \x1b[0m 覆盖 Claude Code 自带的 dim 样式
def fix_output(line):
    return '\x1b[0m' + line.rstrip().replace(' ', '\u00a0')

print(fix_output(line1))
print(fix_output(line2))
