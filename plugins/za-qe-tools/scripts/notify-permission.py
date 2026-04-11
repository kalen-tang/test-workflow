# /// script
# dependencies = ["winotify", "chardet"]
# ///
import json, sys, time, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
import chardet
from winotify import Notification


def fix_encoding(text: str) -> str:
    """检测并修复可能的编码问题，确保文本可在 Windows Toast 中正确显示。"""
    try:
        raw_bytes = text.encode('utf-8')
        detected = chardet.detect(raw_bytes)
        enc = detected.get('encoding', 'utf-8') or 'utf-8'
        # 如果检测结果不是 utf-8 兼容编码，尝试用检测到的编码重新解码
        if enc.lower().replace('-', '') not in ('utf8', 'ascii'):
            return raw_bytes.decode(enc, errors='replace')
        # 尝试 latin1 回退：UTF-8 字节被误读为 latin1 的情况
        try:
            repaired = raw_bytes.decode('utf-8').encode('latin1').decode('utf-8')
            if repaired != text:
                return repaired
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
        # 尝试 GBK 回退：Windows 中文环境常见
        try:
            repaired = raw_bytes.decode('utf-8').encode('latin1').decode('gbk')
            if repaired != text:
                return repaired
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
        return text
    except Exception:
        return text


try:
    raw = sys.stdin.buffer.read()
    # 优先 UTF-8 解码，失败则用 chardet 检测
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        detected = chardet.detect(raw)
        enc = detected.get('encoding', 'utf-8') or 'utf-8'
        text = raw.decode(enc, errors='replace')

    data = json.loads(text)
    tool = data.get('tool_name', '')
    cwd = data.get('cwd', '')
    project = Path(cwd).name if cwd else ''
    tool_input = data.get('tool_input', {})

    # 工具名中文映射
    tool_names = {
        'Bash': '执行',
        'Read': '读取',
        'Write': '写入',
        'Edit': '编辑',
        'Glob': '搜索文件',
        'Grep': '搜索内容',
        'Agent': '代理',
        'WebFetch': '抓取',
        'WebSearch': '搜索',
        'NotebookEdit': '编辑笔记本',
    }
    tool_label = tool_names.get(tool, tool)

    if tool == 'Bash':
        detail = tool_input.get('description', '') or tool_input.get('command', '')
        detail = fix_encoding(detail)
        detail = detail[:60] + '...' if len(detail) > 60 else detail
    elif tool in ('Read', 'Write', 'Edit'):
        detail = tool_input.get('file_path', '')
        detail = fix_encoding(Path(detail).name) if detail else ''
    else:
        detail = fix_encoding(str(tool_input)[:60]) if tool_input else ''

    parts = []
    parts.append(f"🔧 {tool_label}")
    if detail:
        parts.append(detail)
    msg = "\n".join(parts) if parts else "等待确认"
    session_id = data.get('session_id', 'default')
except Exception:
    msg = "等待确认"
    session_id = 'default'

FLAG_FILE = Path(tempfile.gettempdir()) / f'claude-permission-pending-{session_id}'
FLAG_FILE.write_text('pending')

# 每秒轮询标记文件，最多等 15 秒；用户确认后 PostToolUse 会删除标记文件
for _ in range(15):
    time.sleep(1)
    if not FLAG_FILE.exists():
        sys.exit(0)

# 超时仍未确认，弹出提醒通知
if FLAG_FILE.exists():
    FLAG_FILE.unlink(missing_ok=True)
    title = f"⏳ 等待确认 · {project}" if project else "⏳ 等待确认"
    toast = Notification(
        app_id="Claude Code",
        title=title,
        msg=msg,
        duration="long",
    )
    toast.show()
