#!/usr/bin/env python3
import json, sys, subprocess, os, time, tempfile
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(sys.stdin)
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
    return f"{mins}m {secs}s"

duration_str = fmt_duration(duration_ms)
api_str = fmt_duration(api_duration_ms)

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

# --- 颜色定义 ---
# 上下文颜色
if pct >= 90:
    ctx_bg = 196  # 红
elif pct >= 70:
    ctx_bg = 208  # 橙
else:
    ctx_bg = 71   # 绿

# 费用颜色
if cost > 25:
    cost_bg = 196
elif cost > 10:
    cost_bg = 208
else:
    cost_bg = 71

# 分支颜色
branch_bg = 71 if branch in ('master', 'main') else 208

# --- segment 渲染 ---
def segment(text, bg, fg=255, next_bg=None):
    bg_code = f'\033[48;5;{bg}m'
    fg_code = f'\033[38;5;{fg}m'
    if next_bg is not None:
        sep = f'\033[0m\033[38;5;{bg}m\033[48;5;{next_bg}m{SEP}'
    else:
        sep = RESET
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
line1_segs.append((model, 31, 255))
line1_segs.append((f"📁 {directory}", 240, 255))
if branch:
    line1_segs.append((f"🌿 {branch}{git_dirty}", branch_bg, 255))
if venv_name:
    line1_segs.append((f"🐍 {venv_name}", 25, 255))

# --- 第二行：进度条(文字跨双色) → 费用 → 时长 ---

# 进度条区域：文字拆成不可分割 token，按百分比分配到左右区域
BAR_WIDTH = 20  # 进度条总字符宽度
empty_bg = 240  # 剩余部分背景色

# 构建 token 列表（每个 token 不可跨区分割）
tokens_str = f'{tokens_used_k}/{tokens_limit_k}k'
if pct >= 90:
    tokens = [' ', '[建议压缩]', ' ', f'{pct}%', ' ', tokens_str, ' ']
else:
    tokens = [' ', f'{pct}%', ' ', tokens_str, ' ']

# 总字符宽度，不够则末尾补空格 token
total_len = sum(len(t) for t in tokens)
if total_len < BAR_WIDTH:
    tokens.append(' ' * (BAR_WIDTH - total_len))
    total_len = BAR_WIDTH

# 按百分比找分割点：累积宽度超过 split_target 时切
split_target = max(1, int(total_len * pct / 100))
acc = 0
split_idx = len(tokens)  # 默认全部在左边
for i, t in enumerate(tokens):
    acc += len(t)
    if acc >= split_target:
        split_idx = i + 1
        break

left_part = ''.join(tokens[:split_idx])
right_part = ''.join(tokens[split_idx:])

# 手动渲染：左半(ctx_bg) + 箭头 + 右半(empty_bg)
bar_segment = (
    f'\033[48;5;{ctx_bg}m\033[38;5;255m{left_part}'
    f'\033[0m\033[38;5;{ctx_bg}m\033[48;5;{empty_bg}m{SEP}'
    f'\033[38;5;255m{right_part}'
)
# bar_segment 的最终 bg 是 empty_bg，用于下一个箭头衔接
bar_entry = (bar_segment, empty_bg, 255)  # bg 记录为 empty_bg 给箭头用

line2_segs = []
line2_segs.append(bar_entry)
line2_segs.append((f"💰 ${cost:.2f}", cost_bg, 255))
line2_segs.append((f"⏱️  {duration_str} (api {api_str})", 240, 255))

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
                sep = RESET
            output += text + sep
        else:
            output += segment(text, bg, fg, next_bg)
    output += RESET
    return output

print(render_line(line1_segs))
print(render_line2(line2_segs))
