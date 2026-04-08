# /// script
# dependencies = ["winotify"]
# ///
import json, sys, os
from winotify import Notification

DANGEROUS_PATTERNS = [
    'rm -rf', 'rm -fr', 'rmdir /s',
    'git push --force', 'git push -f',
    'git reset --hard',
    'drop table', 'drop database',
    'format ', 'mkfs',
    'dd if=',
    '> /dev/sd',
]

try:
    data = json.load(sys.stdin)
    tool = data.get('tool_name', '')
    tool_input = data.get('tool_input', {})
    command = tool_input.get('command', '') if isinstance(tool_input, dict) else ''
    cwd = data.get('cwd', '')
    project = os.path.basename(cwd) if cwd else ''

    is_dangerous = any(p in command.lower() for p in DANGEROUS_PATTERNS)
    if not is_dangerous:
        sys.exit(0)

    short_cmd = command[:80] + '...' if len(command) > 80 else command
    msg = f"📁 {project}\n{short_cmd}" if project else short_cmd

    toast = Notification(
        app_id="Claude Code",
        title="⚠️ 危险命令",
        msg=msg,
        duration="long",
    )
    toast.show()
except Exception:
    pass
