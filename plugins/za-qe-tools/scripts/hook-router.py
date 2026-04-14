# /// script
# dependencies = [
#   "winotify; sys_platform == 'win32'",
#   "chardet",
# ]
# ///
"""
za-qe-tools 统一 Hook 路由入口。

所有 Hook 事件通过此脚本分发，内部检查模块开关状态：
- 模块开启 → 执行对应逻辑
- 模块关闭 → 静默放行/跳过

用法: uv run hook-router.py --event <EventName>

配置文件: ~/.claude/za-qe-tools.json
"""
from __future__ import annotations

import json
import os
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

CONFIG_PATH = Path.home() / ".claude" / "za-qe-tools.json"

DEFAULT_CONFIG = {
    "statusline": {"enabled": True, "mode": "powerline"},
    "notify": {"enabled": False},
    "dippy": {"enabled": False},
    "esp": {"enabled": False},
}

PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", str(Path(__file__).resolve().parent.parent)))


def load_config() -> dict:
    """加载模块配置，不存在则返回默认值。"""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
            # 合并默认值（新增模块自动获得默认配置）
            merged = {}
            for key, default in DEFAULT_CONFIG.items():
                if key in saved:
                    merged[key] = {**default, **saved[key]}
                else:
                    merged[key] = default.copy()
            return merged
        except (json.JSONDecodeError, OSError):
            pass
    return {k: v.copy() for k, v in DEFAULT_CONFIG.items()}


def is_enabled(config: dict, module: str) -> bool:
    """检查模块是否启用。"""
    return config.get(module, {}).get("enabled", False)


def handle_stop(config: dict) -> None:
    """Stop 事件：会话结束通知。"""
    if not is_enabled(config, "notify"):
        return
    script = PLUGIN_ROOT / "scripts" / "notify.py"
    subprocess.run(
        ["uv", "run", str(script)],
        input=sys.stdin.buffer.read(),
        capture_output=True,
    )


def handle_permission_request(config: dict) -> None:
    """PermissionRequest 事件：权限请求通知。"""
    if not is_enabled(config, "notify"):
        return
    script = PLUGIN_ROOT / "scripts" / "notify-permission.py"
    subprocess.run(
        ["uv", "run", str(script)],
        input=sys.stdin.buffer.read(),
        capture_output=True,
    )


def handle_post_tool_use(config: dict) -> None:
    """PostToolUse / PostToolUseFailure 事件：清除权限标记。"""
    if not is_enabled(config, "notify"):
        return
    script = PLUGIN_ROOT / "scripts" / "clear-permission-flag.py"
    subprocess.run(
        ["uv", "run", str(script)],
        input=sys.stdin.buffer.read(),
        capture_output=True,
    )


def main() -> None:
    args = sys.argv[1:]
    event = ""
    for i, arg in enumerate(args):
        if arg == "--event" and i + 1 < len(args):
            event = args[i + 1]
            break

    config = load_config()

    handlers = {
        "Stop": handle_stop,
        "PermissionRequest": handle_permission_request,
        "PostToolUse": handle_post_tool_use,
        "PostToolUseFailure": handle_post_tool_use,
    }

    handler = handlers.get(event)
    if handler:
        handler(config)
    else:
        # 未知事件，静默通过
        print(json.dumps({"suppressOutput": True}))


if __name__ == "__main__":
    main()
