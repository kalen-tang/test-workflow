# /// script
# dependencies = ["winotify"]
# ///
import json, sys, time, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
from winotify import Notification

try:
    raw = sys.stdin.read()
    data = json.loads(raw)
    tool = data.get('tool_name', '')
    cwd = data.get('cwd', '')
    project = Path(cwd).name if cwd else ''
    tool_input = data.get('tool_input', {})

    if tool == 'Bash':
        detail = tool_input.get('command', '')
        detail = detail[:60] + '...' if len(detail) > 60 else detail
    elif tool in ('Read', 'Write', 'Edit'):
        detail = tool_input.get('file_path', '')
        detail = Path(detail).name if detail else ''
    else:
        detail = str(tool_input)[:60] if tool_input else ''

    parts = []
    parts.append(f"🔧 {tool}")
    if detail:
        parts.append(detail)
    msg = "\n".join(parts) if parts else "等待你的确认"
    session_id = data.get('session_id', 'default')
except Exception:
    msg = "等待你的确认"
    session_id = 'default'

FLAG_FILE = Path(tempfile.gettempdir()) / f'claude-permission-pending-{session_id}'
FLAG_FILE.write_text('pending')

# 等30秒
time.sleep(30)

# 检查标记文件是否还在（PostToolUse 会删除它）
if FLAG_FILE.exists():
    FLAG_FILE.unlink(missing_ok=True)
    toast = Notification(
        app_id="Claude Code",
        title=f"⚠️ 请求权限  {project}" if project else "⚠️ 请求权限",
        msg=msg,
        duration="long",
    )
    toast.show()
