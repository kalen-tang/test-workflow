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

ctx = data.get('context_window', {})
current_usage = ctx.get('current_usage') or {}
input_tokens = (
    (current_usage.get('input_tokens') or 0)
    + (current_usage.get('cache_creation_input_tokens') or 0)
    + (current_usage.get('cache_read_input_tokens') or 0)
)
output_tokens = current_usage.get('output_tokens') or 0
total_tokens = input_tokens + output_tokens

# autocompact 阈值 = context_window_size × CLAUDE_AUTOCOMPACT_PCT_OVERRIDE%
ctx_window_size = ctx.get('context_window_size') or 200000
autocompact_pct = int(os.environ.get('CLAUDE_AUTOCOMPACT_PCT_OVERRIDE') or 100)
autocompact_limit = int(ctx_window_size * autocompact_pct / 100)

# 百分比按 autocompact 阈值计算
pct = int(input_tokens * 100 / autocompact_limit) if autocompact_limit else 0
pct = min(pct, 100)

tokens_used_k = f"{input_tokens / 1000:.1f}"
tokens_limit_k = f"{autocompact_limit / 1000:.0f}"
tokens_str = f"{tokens_used_k}/{tokens_limit_k}k"

CYAN, GREEN, YELLOW, RED, RESET = '\033[36m', '\033[32m', '\033[33m', '\033[31m', '\033[0m'

bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
if pct >= 90:
    bar = '[建议压缩]'
    c1_bot_plain = '[建议压缩] {pct}%'
else:
    filled = pct // 10
    bar = '█' * filled + '░' * (10 - filled)
    c1_bot_plain = f"{bar} {pct}%"

def fmt_duration(ms):
    total_secs = ms // 1000
    mins = total_secs // 60
    secs = total_secs % 60
    if mins >= 60:
        h = mins // 60
        m = mins % 60
        return f"{h}h{m}m"
    return f"{mins}m {secs}s"

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
        staged_out = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True, stderr=subprocess.DEVNULL).strip()
        modified_out = subprocess.check_output(['git', 'diff', '--numstat'], text=True, stderr=subprocess.DEVNULL).strip()
        staged = len(staged_out.split('\n')) if staged_out else 0
        modified = len(modified_out.split('\n')) if modified_out else 0
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            f.write(f"{branch}|{staged}|{modified}")
    except Exception:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            f.write("||")

try:
    with open(CACHE_FILE, encoding='utf-8') as f:
        parts = f.read().strip().split('|')
    branch, staged, modified = parts[0], parts[1], parts[2]
except Exception:
    branch, staged, modified = "", "0", "0"

git_changes = ""
if branch:
    if int(staged) > 0:
        git_changes += f" {GREEN}+{staged}{RESET}"
    if int(modified) > 0:
        git_changes += f" {YELLOW}~{modified}{RESET}"

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
c1_top_plain = f"[{model}]"

c2_top_plain = f"📁 {directory}"
c2_bot_plain = f"📊 {tokens_str}"

c3_top_plain = f"🌿 {branch}{' +'+staged if int(staged)>0 else ''}{' ~'+modified if int(modified)>0 else ''}" if branch else ""
c3_bot_plain = f"💰 ${cost:.2f}"

# 虚拟环境
venv = os.environ.get('VIRTUAL_ENV') or os.environ.get('CONDA_DEFAULT_ENV') or ''
venv_name = os.path.basename(venv) if venv else ''
c4_top_plain = f"({venv_name})" if venv_name else ""
c4_bot_plain = f"⏱️  {duration_str} (api {api_str})"

# 每列宽度 = max(top, bot) 内容宽度，设最小宽度
col_widths = [
    max(vlen(c1_top_plain), vlen(c1_bot_plain), 13),
    max(vlen(c2_top_plain), vlen(c2_bot_plain), 14),
    max(vlen(c3_top_plain), vlen(c3_bot_plain), 10),
]

# 带颜色的内容
c1_top = f"{CYAN}[{model}]{RESET}"
c1_bot = f"{bar_color}{bar}{RESET} {pct}%"

c2_top = f"📁 {directory}"
c2_bot = f"📊 {bar_color}{tokens_str}{RESET}"

branch_color = GREEN if branch in ('master', 'main') else YELLOW
c3_top = f"🌿 {branch_color}{branch}{RESET}{git_changes}" if branch else ""
cost_color = RED if cost > 25 else YELLOW if cost > 10 else GREEN
c3_bot = f"{cost_color}💰 ${cost:.2f}{RESET}"

c4_top = f"{CYAN}({venv_name}){RESET}" if venv_name else ""
tok_per_sec_str = f"⚡ {tok_per_sec:.0f}t/s" if tok_per_sec else ""
c4_bot = f"⏱️  {duration_str} (api {api_str}){('  ' + tok_per_sec_str) if tok_per_sec_str else ''}"

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

print(line1.rstrip())
print(line2.rstrip())
