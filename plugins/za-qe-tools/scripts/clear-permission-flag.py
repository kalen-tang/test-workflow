# /// script
# ///
import sys, json, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

try:
    data = json.loads(sys.stdin.read())
    session_id = data.get('session_id', 'default')
except Exception:
    session_id = 'default'

FLAG_FILE = Path(tempfile.gettempdir()) / f'claude-permission-pending-{session_id}'
FLAG_FILE.unlink(missing_ok=True)
