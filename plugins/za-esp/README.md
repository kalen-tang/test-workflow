# claude-esp Plugin

**claude-esp** 是 Claude Code 的**会话事件流播放器**（Event Stream Player），用于实时追踪、列举和回放 Claude Code 会话事件。

> **二进制已内置，无需安装 Go，开箱即用。**

## 功能

- 列出最近 / 活跃的 Claude Code 会话
- 实时监听指定会话的事件流
- 支持跳过历史、仅查看实时新事件
- 可调节轮询间隔

## 快速上手

安装插件后，直接使用：

```bash
# 查看活跃会话
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe -a

# 列出最近会话
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe -l

# 监听指定会话
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe -s <session-id>

# 交互模式（自动选择最近会话）
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe
```

## Skills

| Skill | 触发场景 |
|-------|---------|
| `watch-session` | 查看、监听、回放 Claude Code 会话事件流 |

## 版本

v0.4.4 — 上游：[github.com/phiat/claude-esp](https://github.com/phiat/claude-esp)
