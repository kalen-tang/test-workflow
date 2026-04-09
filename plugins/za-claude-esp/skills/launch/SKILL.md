---
name: launch
description: "启动 claude-esp。当用户说'打开esp'、'启动esp'、'开启esp'、'esp'、'/esp'、'launch esp' 时触发。支持 -w 参数进入交互式监听模式。"
version: 0.4.4
allowed-tools:
  - Bash
arguments:
  - name: mode
    description: "可选参数：-w 表示交互式监听，缺省为新终端启动"
    required: false
---

# /esp — Claude Code 会话事件流查看工具

启动 claude-esp 工具查看 Claude Code 会话事件。

## 参数说明

- **无参数** (`/esp`)：在新终端窗口中启动 claude-esp
- **-w 参数** (`/esp -w`)：在当前会话中交互式监听会话事件流

## 执行逻辑

### 第一步：检测参数

检查是否传入 `-w` 参数：

```bash
# 从 $1 或命令参数中检取
if [[ "$1" == "-w" ]] || [[ "$@" == *"-w"* ]]; then
  # 走交互式监听路径
  MODE="watch"
else
  # 走新终端启动路径
  MODE="terminal"
fi
```

### 第二步：路由到对应实现

**模式 A：新终端启动** (MODE=terminal)

定位 claude-esp 二进制文件，优先使用环境变量：

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/alfie-qe/plugins/za-claude-esp"
fi
BIN_PATH="$PLUGIN_ROOT/bin/claude-esp.exe"
```

验证文件存在：

```bash
if [ ! -f "$BIN_PATH" ]; then
  echo "❌ claude-esp 二进制文件未找到"
  echo "预期路径: $BIN_PATH"
  exit 1
fi
```

在新终端中启动（优先 Windows Terminal，回退 cmd）：

```bash
# 将路径转换为 Windows 绝对路径（若需要）
WIN_BIN_DIR=$(cd "$(dirname "$BIN_PATH")" && pwd -W 2>/dev/null || echo "$BIN_PATH" | sed 's|/|\\|g')

# 优先尝试 Windows Terminal
powershell.exe -Command "Start-Process wt -ArgumentList 'new-tab', '--title', '\"🧠 claude-esp\"', '--', 'cmd', '/k', 'cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe'" 2>/dev/null

if [ $? -ne 0 ]; then
  # 回退到普通 cmd
  cmd.exe /c "start \"claude-esp\" cmd /k \"cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe\""
fi
```

**模式 B：交互式监听** (MODE=watch)

直接运行 watch-session Skill 的逻辑，在当前会话中交互式选择并监听会话事件流。

### 第三步：确认成功

根据模式输出对应消息：
- 终端模式：提示已启动新窗口
- 监听模式：显示会话列表和监听界面

## 使用示例

```bash
# 在新终端启动 esp
/esp

# 交互式监听会话
/esp -w
```

## 注意事项

- 交互式模式 (`-w`) 会在当前终端中运行，保持互动性
- 新终端模式 (`/esp`) 会在独立窗口中运行，便于并行调试
