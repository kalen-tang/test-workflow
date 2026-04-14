# /// script
# dependencies = []
# ///
"""
StatusLine 配置脚本。

用法:
  SessionStart 自动调用（无参数）：首次写入 powerline，已有则修正路径
  config 命令调用（带参数）：切换模式
    uv run auto-setup.py powerline
    uv run auto-setup.py standard
    uv run auto-setup.py off
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"
PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT", "")

SCRIPT_MAP = {
    "powerline": "statusline-powerline.py",
    "standard": "statusline.py",
}


def read_json(file_path: Path) -> dict | None:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def write_json(file_path: Path, data: dict) -> None:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError:
        pass


def make_statusline_config(mode: str) -> dict:
    script_name = SCRIPT_MAP[mode]
    script_path = PLUGIN_ROOT.replace("\\", "/") + "/scripts/" + script_name
    return {
        "type": "command",
        "command": f"uv run {script_path}",
        "padding": 2,
    }


def main() -> None:
    if not PLUGIN_ROOT:
        print(json.dumps({"suppressOutput": True}))
        return

    settings = read_json(SETTINGS_PATH) or {}
    original = json.dumps(settings)

    args = sys.argv[1:]
    mode = args[0] if args else None

    if mode == "off":
        # 删除 statusLine
        settings.pop("statusLine", None)
    elif mode in SCRIPT_MAP:
        # 指定模式 → 写入
        settings["statusLine"] = make_statusline_config(mode)
    else:
        # 无参数（SessionStart 自动调用）
        if "statusLine" not in settings:
            # 首次：默认 powerline
            settings["statusLine"] = make_statusline_config("powerline")
        else:
            # 已有：检查路径是否指向当前 PLUGIN_ROOT，过期则修正
            current_cmd = settings.get("statusLine", {}).get("command", "")
            if PLUGIN_ROOT.replace("\\", "/") not in current_cmd and "statusline" in current_cmd.lower():
                # 路径过期，检测当前模式并修正
                if "statusline-powerline" in current_cmd:
                    settings["statusLine"] = make_statusline_config("powerline")
                elif "statusline.py" in current_cmd:
                    settings["statusLine"] = make_statusline_config("standard")

    if json.dumps(settings) != original:
        write_json(SETTINGS_PATH, settings)

    print(json.dumps({"suppressOutput": True}))


if __name__ == "__main__":
    main()
