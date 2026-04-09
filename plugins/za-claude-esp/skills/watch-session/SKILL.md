---
name: watch-session
description: "交互式监听 Claude Code 会话事件流（通过 /esp -w 调用）。当用户说'查看会话'、'监听会话'、'交互式监听' 时触发。"
version: 0.4.4
allowed-tools:
  - Bash
---

# 交互式会话监听

在当前会话中交互式选择并实时监听 Claude Code 会话事件流。

**推荐使用**: `/esp -w` 命令调用此功能。

## 执行步骤

### 第一步：获取插件路径

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/alfie-qe/plugins/za-claude-esp"
fi
BIN_PATH="$PLUGIN_ROOT/bin/claude-esp.exe"
```

验证二进制存在：

```bash
if [ ! -f "$BIN_PATH" ]; then
  echo "❌ claude-esp 二进制文件未找到"
  exit 1
fi
```

### 第二步：进入交互模式

直接运行 claude-esp 无参数，进入交互模式：

```bash
"$BIN_PATH"
```

claude-esp 会：
1. 列出最近的活跃会话
2. 提示用户选择会话 ID
3. 实时流式展示选中会话的所有事件

### 常用命令参考

| 功能 | 命令 |
|------|------|
| 列出活跃会话 | `$BIN_PATH -a` |
| 列出最近所有会话 | `$BIN_PATH -l` |
| 监听指定会话 | `$BIN_PATH -s <session-id>` |
| 跳过历史只看新事件 | `$BIN_PATH -n -s <session-id>` |

## 事件类型说明

通过交互模式可查看的事件包括：

| 事件类型 | 说明 |
|---------|------|
| **Message** | Claude 的消息或用户输入 |
| **Tool Call** | Claude 调用的工具（Bash、Read、Edit 等） |
| **Tool Result** | 工具执行结果 |
| **Thinking** | Claude 的思考过程（Extended Thinking） |
| **Status** | 会话状态变化 |

## 使用示例

```bash
# 交互式监听（推荐）
/esp -w

# 或直接运行
claude-esp.exe
```
