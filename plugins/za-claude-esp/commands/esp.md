---
name: esp
description: 启动 Claude Code 会话事件流查看工具（新终端）
skills:
  - launch
  - watch-session
arguments:
  - name: mode
    description: "可选：'-w' 表示交互式监听模式，缺省为新终端模式"
    required: false
---

# /esp — Claude Code 会话事件流查看工具

启动 claude-esp 工具查看 Claude Code 会话事件。

## 用法

### /esp
在新终端窗口中启动 claude-esp（自动进入交互模式）。

```bash
/esp
```

### /esp -w
进入交互式监听模式（在当前会话中交互式选择并监听会话事件流）。

```bash
/esp -w
```

## 功能说明

- **新终端模式** (`/esp`)：在新窗口中启动 esp，自动连接到最近的活跃会话
- **交互监听模式** (`/esp -w`)：在当前终端中交互式选择会话并实时监听事件流

## 查看的事件类型

| 事件类型 | 说明 |
|---------|------|
| **Message** | Claude 的消息或用户输入 |
| **Tool Call** | Claude 调用的工具（如 Bash、Read、Edit） |
| **Tool Result** | 工具执行结果 |
| **Thinking** | Claude 的思考过程（Extended Thinking） |
| **Status** | 会话状态变化 |

## 相关信息

- 完整文档：`./plugins/za-claude-esp/README.md`
- 项目主页：`./README.md`
