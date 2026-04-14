---
description: "启动 Claude Code 会话事件流查看工具。当用户说'打开esp'、'启动esp'、'开启esp'、'esp'、'/esp'、'launch esp'、'监听会话'、'查看会话'、'交互式监听' 时触发。支持 -w 参数。"
allowed-tools:
  - Bash
arguments:
  - name: mode
    description: "可选参数：-w 表示交互式监听，缺省为新终端启动"
    required: false
---

# /za-qe-tools:esp — Claude Code 会话事件流查看工具

启动 claude-esp 工具查看 Claude Code 会话事件。

## 使用方法

### 新终端模式（默认）
`/za-qe-tools:esp`

### 交互式监听模式
`/za-qe-tools:esp -w`

## 前置检查

在执行前，先读取 `~/.claude/za-qe-tools.json` 检查 esp 模块是否开启：

```bash
cat ~/.claude/za-qe-tools.json 2>/dev/null || echo '{}'
```

如果 `esp.enabled` 为 `false` 或配置文件不存在，提示用户：
> ESP 模块当前未启用。请先运行 `/za-qe-tools:config` 开启 ESP 模块。

## 参数说明

- **无参数** (`/esp`)：在新终端窗口中启动 claude-esp
- **-w 参数** (`/esp -w`)：在当前会话中交互式监听会话事件流

## 执行流程

### 第一步：定位二进制

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/alfie-qe/plugins/za-qe-tools"
fi
BIN_PATH="$PLUGIN_ROOT/bin/claude-esp.exe"
```

验证 `$BIN_PATH` 文件存在，不存在则报错退出。

### 第二步：检测参数并执行

从用户输入中检查是否含 `-w` 参数。

#### 模式 A：新终端启动（无 -w）

在新终端中启动（优先 Windows Terminal，回退 cmd）：

```bash
WIN_BIN_DIR=$(cygpath -w "$(dirname "$BIN_PATH")" 2>/dev/null || echo "$PLUGIN_ROOT/bin")
powershell.exe -Command "Start-Process wt -ArgumentList 'new-tab', '--title', '\"claude-esp\"', '--', 'cmd', '/k', 'cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe'" 2>/dev/null

if [ $? -ne 0 ]; then
  cmd.exe /c "start \"claude-esp\" cmd /k \"cd /d \"$WIN_BIN_DIR\" && .\\claude-esp.exe\""
fi
```

#### 模式 B：交互式监听（-w）

直接运行 `claude-esp.exe` 无参数，进入交互模式：

```bash
"$BIN_PATH"
```

## 事件类型说明

| 事件类型 | 说明 |
|---------|------|
| **Message** | Claude 的消息或用户输入 |
| **Tool Call** | Claude 调用的工具 |
| **Tool Result** | 工具执行结果 |
| **Thinking** | Claude 的思考过程 |
| **Status** | 会话状态变化 |

## 常用 claude-esp 命令参考

| 功能 | 命令 |
|------|------|
| 列出活跃会话 | `claude-esp.exe -a` |
| 列出最近会话 | `claude-esp.exe -l` |
| 监听指定会话 | `claude-esp.exe -s <session-id>` |
| 跳过历史只看新事件 | `claude-esp.exe -n -s <session-id>` |
