#!/usr/bin/env python3
import json, sys, subprocess, os, time, tempfile
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

ctx_window_size = ctx.get('context_window_size') or 200000
autocompact_pct = int(os.environ.get('CLAUDE_AUTOCOMPACT_PCT_OVERRIDE') or 100)
autocompact_limit = int(ctx_window_size * autocompact_pct / 100)
pct = int(input_tokens * 100 / autocompact_limit) if autocompact_limit else 0
pct = min(pct, 100)

tokens_used_k = f"{input_tokens / 1000:.1f}"
tokens_limit_k = f"{autocompact_limit / 1000:.0f}"

def fmt_duration(ms):
    total_secs = ms // 1000
    mins = total_secs // 60
    secs = total_secs % 60
    if mins >= 60:
        h = mins // 60
        m = mins % 60
        return f"{h}h{m}m"
    return f"{mins}m{secs}s"

duration_str = fmt_duration(duration_ms)
api_str = fmt_duration(api_duration_ms)

# Token 速度：基于增量计算，缓存上次值
TOK_CACHE_FILE = os.path.join(tempfile.gettempdir(), "statusline-tok-cache")
tok_per_sec = None

try:
    with open(TOK_CACHE_FILE, encoding='utf-8') as f:
        cached = json.load(f)
    if cached.get('session_id') != session_id:
        # 新会话（含 -c 续接），重置缓存
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

git_dirty = ""
if branch:
    if int(staged) > 0:
        git_dirty += f" +{staged}"
    if int(modified) > 0:
        git_dirty += f" ~{modified}"

# 虚拟环境
venv = os.environ.get('VIRTUAL_ENV') or os.environ.get('CONDA_DEFAULT_ENV') or ''
venv_name = os.path.basename(venv) if venv else ''

# Powerline 风格
RESET = '\033[0m'
SEP = '\ue0b0'  # Powerline 箭头

# --- 颜色定义（Nord 配色） ---
# 上下文颜色（第二行位置1，对应第一行模型67 → 用97紫错开）
if pct >= 90:
    ctx_bg = 131  # Nord11 红
elif pct >= 70:
    ctx_bg = 173  # Nord12 橙
else:
    ctx_bg = 24   # Nord9 钢蓝（与剩余17深蓝相近）

# 费用颜色（第二行位置2，对应第一行目录24 → 用非24色）
if cost > 25:
    cost_bg = 131  # Nord11 红
elif cost > 10:
    cost_bg = 173  # Nord12 橙
else:
    cost_bg = 71   # Nord14 绿（错开第一行目录24）

# 分支颜色（第一行位置3）
branch_bg = 71 if branch in ('master', 'main') else 173  # Nord14 绿 / Nord12 橙

# --- segment 渲染 ---
def segment(text, bg, fg=255, next_bg=None):
    bg_code = f'\033[48;5;{bg}m'
    fg_code = f'\033[38;5;{fg}m'
    if next_bg is not None:
        sep = f'\033[0m\033[38;5;{bg}m\033[48;5;{next_bg}m{SEP}\033[38;5;{fg}m'
    else:
        sep = f'\033[0m\033[38;5;{bg}m{SEP}{RESET}'
    return f"{bg_code}{fg_code} {text} {sep}"

def render_line(segments):
    output = ""
    for i, (text, bg, fg) in enumerate(segments):
        next_bg = segments[i + 1][1] if i + 1 < len(segments) else None
        output += segment(text, bg, fg, next_bg)
    output += RESET
    return output

# --- 第一行：模型 → 目录 → 分支 → 虚拟环境 ---
line1_segs = []
line1_segs.append((model, 67, 255))
line1_segs.append((f"📁 {directory}", 24, 255))
if branch:
    line1_segs.append((f"🌿 {branch}{git_dirty}", branch_bg, 255))
if venv_name:
    line1_segs.append((f"🐍 {venv_name}", 97, 255))

# --- 第二行：进度条(文字跨双色) → 费用 → 时长 ---

# 进度条区域：文字拆成不可分割 token，按百分比分配到左右区域
BAR_WIDTH = 20  # 进度条总字符宽度
empty_bg = 238  # 剩余部分背景色（深炭色）

# 构建进度条文字（固定 BAR_WIDTH 字符宽）
# tokens_str 右对齐，百分比左对齐，字符级精确分割
tokens_str = f'{tokens_used_k}/{tokens_limit_k}k'
if pct >= 90:
    left_label = f' [建议压缩] {pct}% '
else:
    left_label = f' {pct}% '

# 右对齐：右侧固定放 tokens_str + 空格，中间填充
right_label = f'{tokens_str} '
pad = max(0, BAR_WIDTH - len(left_label) - len(right_label))
full_text = left_label + ' ' * pad + right_label
# 确保总宽度 = BAR_WIDTH
if len(full_text) < BAR_WIDTH:
    full_text += ' ' * (BAR_WIDTH - len(full_text))
total_len = len(full_text)

# 字符级精确分割
split_pos = max(1, int(total_len * pct / 100))
left_part = full_text[:split_pos]
right_part = full_text[split_pos:]

# 手动渲染：左半(ctx_bg) + 箭头 + 右半(empty_bg)
bar_segment = (
    f'\033[48;5;{ctx_bg}m\033[38;5;255m{left_part}'
    f'\033[0m\033[38;5;{ctx_bg}m\033[48;5;{empty_bg}m{SEP}'
    f'\033[38;5;255m{right_part}'
)
# bar_segment 的最终 bg 是 empty_bg，用于下一个箭头衔接
bar_entry = (bar_segment, empty_bg, 255)

line2_segs = []
line2_segs.append(bar_entry)
line2_segs.append((f"💰 ${cost:.2f}", cost_bg, 255))
line2_segs.append((f"⏱ {duration_str} [api {api_str}]", 24, 255))
if tok_per_sec:
    line2_segs.append((f"⚡ {tok_per_sec:.0f}t/s", 67, 255))

# 第二行需要特殊渲染（第一段已经手动渲染了颜色）
def render_line2(segments):
    output = ""
    for i, (text, bg, fg) in enumerate(segments):
        next_bg = segments[i + 1][1] if i + 1 < len(segments) else None
        if i == 0:
            # 第一段已经包含完整 ANSI，只需加箭头
            if next_bg is not None:
                sep = f'\033[0m\033[38;5;{bg}m\033[48;5;{next_bg}m{SEP}'
            else:
                sep = f'\033[0m\033[38;5;{bg}m{SEP}{RESET}'
            output += text + sep
        else:
            output += segment(text, bg, fg, next_bg)
    output += RESET
    return output

print(render_line(line1_segs))
print(render_line2(line2_segs))
