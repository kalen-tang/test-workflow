---
name: launch
description: "启动 claude-esp 新终端模式。"
version: 0.4.4
allowed-tools:
  - Bash
arguments:
  - name: mode
    description: "可选参数：-w 表示交互式监听，缺省为新终端启动"
    required: false
---

# /esp — 新终端启动模式

## 执行逻辑

### 第一步：检测参数

检查是否传入 `-w` 参数，若有则走交互式监听路径。

### 第二步：定位二进制

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/alfie-qe/plugins/za-qe-tools"
fi
BIN_PATH="$PLUGIN_ROOT/bin/claude-esp.exe"
```

### 第三步：验证并启动

验证文件存在后，在新终端中启动：

```bash
WIN_BIN_DIR=$(cygpath -w "$(dirname "$BIN_PATH")" 2>/dev/null || echo "$PLUGIN_ROOT/bin")
powershell.exe -Command "Start-Process wt -ArgumentList 'new-tab', '--title', '\"claude-esp\"', '--', 'cmd', '/k', 'cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe'" 2>/dev/null

if [ $? -ne 0 ]; then
  cmd.exe /c "start \"claude-esp\" cmd /k \"cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe\""
fi
```
