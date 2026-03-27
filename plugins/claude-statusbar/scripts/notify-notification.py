# /// script
# dependencies = ["winotify"]
# ///
import json, sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
from winotify import Notification

try:
    data = json.load(sys.stdin)
    raw_msg = data.get('message', '')
    # 常见英文系统消息翻译
    translations = {
        r'context window is (\d+)% full': lambda m: f"上下文已用 {m.group(1)}%",
        r'running low on context': lambda m: "上下文即将耗尽",
        r'new version available': lambda m: "有新版本可用",
        r'MCP.*error': lambda m: "MCP 服务器错误",
        r'MCP.*disconnect': lambda m: "MCP 服务器断开",
    }
    # 权限请求由 PermissionRequest hook 处理，这里跳过
    if re.search(r'needs your permission|permission to use', raw_msg, re.IGNORECASE):
        sys.exit(0)
    msg = raw_msg
    for pattern, replacement in translations.items():
        m = re.search(pattern, raw_msg, re.IGNORECASE)
        if m:
            msg = replacement(m)
            break
    cwd = data.get('cwd', '')
    project = os.path.basename(cwd) if cwd else ''
    title = f"📁 {project}" if project else "系统通知"
except Exception:
    msg = ""
    title = "Claude Code"

if msg:
    toast = Notification(
        app_id="Claude Code",
        title=title,
        msg=msg,
        duration="short",
    )
    toast.show()
