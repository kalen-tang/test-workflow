# /// script
# dependencies = ["winotify"]
# ///
import json, sys, os
from winotify import Notification

try:
    data = json.load(sys.stdin)
    cwd = data.get('cwd', '')
    project = os.path.basename(cwd) if cwd else ''
    pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
    msg = f"📁 {project}  上下文已用 {pct}%，即将压缩" if project else f"上下文已用 {pct}%，即将压缩"
except Exception:
    msg = "上下文即将压缩"

toast = Notification(
    app_id="Claude Code",
    title="📦 上下文压缩",
    msg=msg,
    duration="short",
)
toast.show()
