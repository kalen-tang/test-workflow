# /// script
# dependencies = []
# ///
"""
SessionStart hook: za-qe-tools 自动初始化。

逻辑：
1. 确保 ~/.claude/za-qe-tools.json 配置文件存在
2. 根据 statusline 配置自动写入 settings.json
"""
from __future__ import annotations

import json
import os
from pathlib import Path

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"
CONFIG_PATH = Path.home() / ".claude" / "za-qe-tools.json"

PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT", "")

DEFAULT_CONFIG = {
    "statusline": {"enabled": True, "mode": "powerline"},
    "notify": {"enabled": False},
    "dippy": {"enabled": False},
    "esp": {"enabled": False},
}


def read_json(file_path: Path) -> dict | None:
    """读取 JSON 文件，失败返回 None。"""
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def ensure_module_config() -> dict:
    """确保模块配置文件存在，不存在则创建默认配置。"""
    if CONFIG_PATH.exists():
        config = read_json(CONFIG_PATH)
        if config is not None:
            return config

    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
    except OSError:
        pass

    return DEFAULT_CONFIG


def setup_statusline(config: dict, settings: dict) -> dict:
    """根据 statusline 配置自动写入 settings.json。"""
    if not PLUGIN_ROOT:
        return settings

    sl_config = config.get("statusline", {})
    if not sl_config.get("enabled"):
        return settings

    if "statusLine" in settings:
        return settings

    script_name = "statusline.py" if sl_config.get("mode") == "standard" else "statusline-powerline.py"
    script_path = PLUGIN_ROOT.replace("\\", "/") + "/scripts/" + script_name

    settings["statusLine"] = {
        "type": "command",
        "command": f"uv run {script_path}",
        "padding": 2,
    }

    return settings


def main() -> None:
    config = ensure_module_config()

    settings = read_json(SETTINGS_PATH) or {}

    original = json.dumps(settings)
    settings = setup_statusline(config, settings)

    if json.dumps(settings) != original:
        try:
            SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
            SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")
        except OSError:
            pass

    print(json.dumps({"suppressOutput": True}))


if __name__ == "__main__":
    main()
