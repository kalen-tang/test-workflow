---
name: esp
description: 启动 Claude Code 会话事件流查看工具
triggers:
  - /esp
  - /esp -w
execution:
  type: skill
  skill: launch
arguments:
  - name: mode
    description: "可选：'-w' 表示交互式监听模式，缺省为新终端模式"
    required: false
---

# /esp — Claude Code 会话事件流查看工具

启动 claude-esp 工具查看 Claude Code 会话事件。

## 使用方法

### 新终端模式（默认）
```bash
/esp
```
在新终端窗口中启动 claude-esp，自动连接到最近的活跃会话。

### 交互式监听模式
```bash
/esp -w
```
在当前会话中交互式选择并实时监听会话事件流。

## 可查看的事件类型

| 事件类型 | 说明 |
|---------|------|
| **Message** | Claude 的消息或用户输入 |
| **Tool Call** | Claude 调用的工具（Bash、Read、Edit 等） |
| **Tool Result** | 工具执行结果 |
| **Thinking** | Claude 的思考过程（Extended Thinking） |
| **Status** | 会话状态变化 |

## 执行步骤

根据参数选择执行模式：

- 若无 `-w` 参数 → 调用 launch Skill（新终端启动）
- 若有 `-w` 参数 → 调用 watch-session Skill（交互式监听）

## 相关文档

- 完整说明：`./plugins/za-claude-esp/README.md`
- Skill 实现：`./plugins/za-claude-esp/skills/`
