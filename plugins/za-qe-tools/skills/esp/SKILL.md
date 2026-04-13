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

### 第一步：检测参数

从用户输入中检查是否含 `-w` 参数。

### 第二步：根据模式执行

#### 模式 A：新终端启动

定位 claude-esp 二进制文件：

PLUGIN_ROOT 优先使用 `${CLAUDE_PLUGIN_ROOT}`，回退到 `~/.claude/plugins/marketplaces/alfie-qe/plugins/za-qe-tools`。

二进制路径：`$PLUGIN_ROOT/bin/claude-esp.exe`

验证文件存在后，在新终端中启动（优先 Windows Terminal，回退 cmd）。

#### 模式 B：交互式监听

直接运行 `claude-esp.exe` 无参数，进入交互模式。

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
