---
name: esp
description: "启动 Claude Code 会话事件流查看工具。当用户说'打开esp'、'启动esp'、'开启esp'、'esp'、'/esp'、'launch esp'、'监听会话'、'查看会话'、'交互式监听' 时触发。支持 -w 参数。"
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

## 执行流程

### 第一步：检测参数

```bash
MODE="terminal"
if [[ "$1" == "-w" ]] || [[ "$@" == *"-w"* ]]; then
  MODE="watch"
fi
```

### 第二步：根据模式执行

#### 模式 A：新终端启动 (MODE=terminal)

定位 claude-esp 二进制文件：

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

在新终端中启动：

```bash
WIN_BIN_DIR=$(cygpath -w "$(dirname "$BIN_PATH")" 2>/dev/null || echo "$PLUGIN_ROOT/bin")

# 优先尝试 Windows Terminal
powershell.exe -Command "Start-Process wt -ArgumentList 'new-tab', '--title', '\"🧠 claude-esp\"', '--', 'cmd', '/k', 'cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe'" 2>/dev/null

if [ $? -ne 0 ]; then
  # 回退到普通 cmd
  cmd.exe /c "start \"claude-esp\" cmd /k \"cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe\""
fi

echo "✅ 已在新终端窗口中启动 claude-esp"
```

#### 模式 B：交互式监听 (MODE=watch)

直接运行 claude-esp 无参数，进入交互模式：

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/alfie-qe/plugins/za-claude-esp"
fi
BIN_PATH="$PLUGIN_ROOT/bin/claude-esp.exe"

if [ ! -f "$BIN_PATH" ]; then
  echo "❌ claude-esp 二进制文件未找到"
  exit 1
fi

echo "📋 交互式监听模式 - 选择要监听的会话："
echo ""
"$BIN_PATH"
```

## 事件类型说明

| 事件类型 | 说明 |
|---------|------|
| **Message** | Claude 的消息或用户输入 |
| **Tool Call** | Claude 调用的工具（Bash、Read、Edit 等） |
| **Tool Result** | 工具执行结果 |
| **Thinking** | Claude 的思考过程（Extended Thinking） |
| **Status** | 会话状态变化 |

## 使用示例

```bash
# 在新终端启动 esp
/esp

# 交互式监听会话
/esp -w
```

## 常用 claude-esp 命令参考

若需要手动运行：

```bash
# 列出活跃会话
claude-esp.exe -a

# 列出最近会话
claude-esp.exe -l

# 监听指定会话
claude-esp.exe -s <session-id>

# 跳过历史只看新事件
claude-esp.exe -n -s <session-id>
```
