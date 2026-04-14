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
wt_branch = worktree.get('branch', '')

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

# 模型名简化：去掉 " context" 后缀，如 "Opus 4.6 (1M context)" → "Opus 4.6 (1M)"
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
    autocompact_pct_env = int(os.environ.get('CLAUDE_AUTOCOMPACT_PCT_OVERRIDE') or 100)
    autocompact_limit = int(ctx_window_size * autocompact_pct_env / 100)
    pct = int(used_tokens * 100 / autocompact_limit) if autocompact_limit else 0
    pct = min(pct, 100)

tokens_used_k = f"{used_tokens / 1000:.1f}"
tokens_limit_k = f"{ctx_window_size / 1000:.0f}"

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

git_dirty = ""
if branch:
    if int(staged) > 0:
        git_dirty += f" +{staged}"
    if int(modified) > 0:
        git_dirty += f" ~{modified}"
    if int(untracked) > 0:
        git_dirty += f" ?{untracked}"
    if lines_added > 0 or lines_removed > 0:
        git_dirty += f" +{lines_added}/-{lines_removed}"

# 虚拟环境
venv = os.environ.get('VIRTUAL_ENV') or os.environ.get('CONDA_DEFAULT_ENV') or ''
venv_name = os.path.basename(venv) if venv else ''

# Powerline 风格
RESET = '\033[0m'
SEP = '\ue0b0'  # Powerline 箭头

# --- Nord Truecolor 配色 ---
# fg/bg 辅助函数
def fg_rgb(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'

def bg_rgb(r, g, b):
    return f'\033[48;2;{r};{g};{b}m'

# Nord 色板
C_FROST     = (136, 192, 208)  # #88C0D0 霜蓝
C_GREEN     = (163, 190, 140)  # #A3BE8C 绿
C_YELLOW    = (235, 203, 139)  # #EBCB8B 黄
C_RED       = (191, 97, 106)   # #BF616A 红
C_GRAY      = (76, 86, 106)    # #4C566A 灰
C_PURPLE    = (180, 142, 173)  # #B48EAD 紫
C_OCEAN     = (94, 129, 172)   # #5E81AC 深蓝
C_POLAR0    = (46, 52, 64)     # #2E3440 极夜深色
C_POLAR1    = (59, 66, 82)     # #3B4252 极夜中色
C_SNOW0     = (216, 222, 233)  # #D8DEE9 雪白
C_SNOW1     = (236, 239, 244)  # #ECEFF4 亮白
C_CHARCOAL  = (52, 58, 72)     # #343A48 深炭色（进度条空余）

FG_DARK  = fg_rgb(*C_POLAR0)   # 深色前景
FG_LIGHT = fg_rgb(*C_SNOW1)    # 亮色前景

# 上下文进度条颜色
if pct >= 90:
    ctx_color = C_RED
elif pct >= 70:
    ctx_color = C_YELLOW
else:
    ctx_color = C_FROST

# 费用颜色
if cost > 25:
    cost_color = C_RED
elif cost > 10:
    cost_color = C_PURPLE
else:
    cost_color = C_GREEN

# 分支颜色
branch_color = C_GREEN if branch in ('master', 'main') else C_YELLOW

# --- segment 渲染（truecolor） ---
def segment_tc(text, bg_c, fg_c=C_SNOW1, next_bg_c=None):
    bg_code = bg_rgb(*bg_c)
    fg_code = fg_rgb(*fg_c)
    if next_bg_c is not None:
        sep = f'{RESET}{fg_rgb(*bg_c)}{bg_rgb(*next_bg_c)}{SEP}'
    else:
        sep = f'{RESET}{fg_rgb(*bg_c)}{SEP}{RESET}'
    return f"{bg_code}{fg_code} {text} {sep}"

def render_line(segments):
    output = ""
    for i, (text, bg_c, fg_c) in enumerate(segments):
        next_bg_c = segments[i + 1][1] if i + 1 < len(segments) else None
        output += segment_tc(text, bg_c, fg_c, next_bg_c)
    output += RESET
    return output

# --- 第一行：模型 → 目录 → 分支 → 虚拟环境 ---
# --- 第二行：进度条 → 费用 → 时长 → 速度 ---
# 色块分配原则：上下同位置不同色
#   位置1: 第一行 C_FROST 霜蓝  / 第二行 进度条(动态色→CHARCOAL)
#   位置2: 第一行 C_GRAY 灰     / 第二行 费用(动态色)
#   位置3: 第一行 branch(动态)   / 第二行 C_OCEAN 深蓝
#   位置4: 第一行 C_PURPLE 紫   / 第二行 C_POLAR1 极夜中色
model_label = model_display
if thinking_effort:
    model_label += f" [{thinking_effort}]"
line1_segs = []
line1_segs.append((model_label, C_FROST, C_POLAR0))
line1_segs.append((f"\ue5ff {directory}", C_GRAY, C_SNOW1))
if branch:
    line1_segs.append((f"\ue0a0 {branch}{git_dirty}", branch_color, C_POLAR0))
if wt_name:
    line1_segs.append((f"\ue728 {wt_name}", C_OCEAN, C_SNOW1))
elif venv_name:
    line1_segs.append((f"\ue73c {venv_name}", C_PURPLE, C_SNOW1))

# --- 第二行：进度条(文字跨三色) → 费用 → 时长 → 速度 ---
BAR_WIDTH = 20
empty_color = C_CHARCOAL
C_CACHE = (129, 161, 193)  # #81A1C1 Nord9 冰蓝（cache 区域，比 ctx_color 浅/深一档）

# 构建进度条文字
tokens_str = f'{tokens_used_k}/{tokens_limit_k}k'
if pct >= 90:
    left_label = f' [建议压缩] {pct}% '
else:
    left_label = f' {pct}% '

right_label = f'{tokens_str} '
pad = max(0, BAR_WIDTH - len(left_label) - len(right_label))
full_text = left_label + ' ' * pad + right_label
if len(full_text) < BAR_WIDTH:
    full_text += ' ' * (BAR_WIDTH - len(full_text))
total_len = len(full_text)

# 三段分割：non-cached | cached | empty
# cached 占 used_tokens 中的比例
cache_pct = int(cached_tokens * 100 / ctx_window_size) if ctx_window_size and cached_tokens else 0
non_cache_pct = max(0, pct - cache_pct)

split_nc = max(1, int(total_len * non_cache_pct / 100)) if non_cache_pct > 0 else 0
split_ca = max(split_nc, int(total_len * pct / 100))
# 确保 cached 段至少有位置（如果有 cache）
if cache_pct > 0 and split_ca <= split_nc:
    split_ca = min(split_nc + 1, total_len)

part_nc = full_text[:split_nc]
part_ca = full_text[split_nc:split_ca]
part_empty = full_text[split_ca:]

# 手动渲染三段：non-cached(ctx_color) | cached(C_CACHE) | empty(CHARCOAL)
bar_parts = f'{bg_rgb(*ctx_color)}{FG_LIGHT}{part_nc}'
if part_ca:
    bar_parts += f'{bg_rgb(*C_CACHE)}{part_ca}'
bar_parts += (
    f'{RESET}{fg_rgb(*C_CACHE if part_ca else ctx_color)}{bg_rgb(*empty_color)}{SEP}'
    f'{FG_LIGHT}{part_empty}'
)
bar_entry = (bar_parts, empty_color, C_SNOW1)

# 速度格式化
if tok_per_sec and tok_per_sec >= 1000:
    tok_per_sec_str = f"\uf0e7 {tok_per_sec / 1000:.1f}k t/s"
elif tok_per_sec:
    tok_per_sec_str = f"\uf0e7 {tok_per_sec:.1f} t/s"
else:
    tok_per_sec_str = ""

line2_segs = []
line2_segs.append(bar_entry)
line2_segs.append((f"\uf155{cost:.2f}", cost_color, C_POLAR0))
line2_segs.append((f"\uf017 {duration_str} \uf362 {api_str}", C_OCEAN, C_SNOW1))
if tok_per_sec_str:
    line2_segs.append((tok_per_sec_str, C_POLAR1, C_SNOW1))

# 第二行特殊渲染（第一段已手动渲染颜色）
def render_line2(segments):
    output = ""
    for i, (text, bg_c, fg_c) in enumerate(segments):
        next_bg_c = segments[i + 1][1] if i + 1 < len(segments) else None
        if i == 0:
            if next_bg_c is not None:
                sep = f'{RESET}{fg_rgb(*bg_c)}{bg_rgb(*next_bg_c)}{SEP}'
            else:
                sep = f'{RESET}{fg_rgb(*bg_c)}{SEP}{RESET}'
            output += text + sep
        else:
            output += segment_tc(text, bg_c, fg_c, next_bg_c)
    output += RESET
    return output

# 用 non-breaking space 替换普通空格，防止终端/VSCode trim 导致色块散落
# 行首加 \x1b[0m 覆盖 Claude Code 自带的 dim 样式
def fix_output(line):
    return '\x1b[0m' + line.rstrip().replace(' ', '\u00a0')

print(fix_output(render_line(line1_segs)))
print(fix_output(render_line2(line2_segs)))
