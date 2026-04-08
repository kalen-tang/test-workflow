# /// script
# dependencies = ["winotify"]
# ///
import json, sys, os, glob
from datetime import datetime
from winotify import Notification

sys.stdout.reconfigure(encoding='utf-8')

project = ''
model = ''
cost = 0
duration_ms = 0

try:
    raw = sys.stdin.read().strip()
    if raw:
        data = json.loads(raw)
        cwd = data.get('cwd', '')
        project = os.path.basename(cwd) if cwd else ''
        model = data.get('model', {}).get('display_name', '') if isinstance(data.get('model'), dict) else ''
        cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
        duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0
        # 尝试从 transcript_path 旁边找会话数据
        transcript = data.get('transcript_path', '')
        if not project and transcript:
            project = os.path.basename(os.path.dirname(transcript))
except Exception:
    pass

# 从当前工作目录猜项目名（兜底）
if not project:
    try:
        project = os.path.basename(os.getcwd())
    except Exception:
        pass

mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

parts = []
if model:
    parts.append(f"[{model}]")
if cost:
    parts.append(f"${cost:.2f}")
if duration_ms:
    parts.append(f"⏱️ {mins}m {secs}s")
msg = "  ".join(parts)

toast = Notification(
    app_id="Claude Code",
    title=f"✅ 已完成  {project}  {datetime.now().strftime('%H:%M:%S')}" if project else f"✅ 已完成  {datetime.now().strftime('%H:%M:%S')}",
    msg=msg,
    duration="short",
)
toast.show()

