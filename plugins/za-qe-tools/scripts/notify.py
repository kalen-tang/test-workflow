# /// script
# dependencies = [
#   "winotify; sys_platform == 'win32'",
#   "chardet",
# ]
# ///
import json, sys, os, subprocess
from datetime import datetime
import chardet

sys.stdout.reconfigure(encoding='utf-8')


def notify(title: str, msg: str, duration: str = "short") -> None:
    """跨平台弹出系统通知。"""
    if sys.platform == "win32":
        from winotify import Notification
        Notification(app_id="Claude Code", title=title, msg=msg, duration=duration).show()
    elif sys.platform == "darwin":
        t = title.replace('"', '\\"')
        m = msg.replace('"', '\\"')
        subprocess.run(["osascript", "-e", f'display notification "{m}" with title "{t}"'], capture_output=True, timeout=5)


project = ''
model = ''
cost = 0
duration_ms = 0

try:
    raw_bytes = sys.stdin.buffer.read().strip()
    try:
        raw = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        detected = chardet.detect(raw_bytes)
        enc = detected.get('encoding', 'utf-8') or 'utf-8'
        raw = raw_bytes.decode(enc, errors='replace')
    if raw:
        data = json.loads(raw)
        cwd = data.get('cwd', '')
        project = os.path.basename(cwd) if cwd else ''
        model = data.get('model', {}).get('display_name', '') if isinstance(data.get('model'), dict) else ''
        cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
        duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0
        transcript = data.get('transcript_path', '')
        if not project and transcript:
            project = os.path.basename(os.path.dirname(transcript))
except Exception:
    pass

if not project:
    try:
        project = os.path.basename(os.getcwd())
    except Exception:
        pass

mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

parts = []
if model:
    parts.append(f"模型: {model}")
if cost:
    parts.append(f"费用: ${cost:.2f}")
if duration_ms:
    parts.append(f"耗时: {mins}分{secs}秒")
msg = "  ".join(parts)

now = datetime.now().strftime('%H:%M:%S')
title = f"✅ 会话结束 · {project}  {now}" if project else f"✅ 会话结束  {now}"

notify(title, msg)
