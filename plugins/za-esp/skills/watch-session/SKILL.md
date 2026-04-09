---
name: watch-session
description: Use this skill when the user asks to watch a Claude Code session, view session history, monitor an active session, or replay session events. Triggers on phrases like "watch session", "list sessions", "active session", "monitor Claude session", "view session", "esp", "展示实时思考流程", "查看会话", "监听会话", "实时思考", "查看思考过程", "显示思考流程", "回放会话", "活跃会话", "会话事件".
version: 0.4.4
allowed-tools:
  - Bash
---

# claude-esp — Claude Code 会话事件流查看工具

## 使用说明

`claude-esp` 已随插件打包，**无需额外安装**，可直接通过以下方式调用：

```bash
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe <参数>
```

## 常用命令

| 目标 | 命令 |
|------|------|
| 列出活跃会话（5 分钟内有更新） | `claude-esp.exe -a` |
| 列出最近所有会话 | `claude-esp.exe -l` |
| 监听指定会话的事件流 | `claude-esp.exe -s <session-id>` |
| 仅显示实时新事件（跳过历史） | `claude-esp.exe -n -s <session-id>` |
| 调整轮询间隔（单位 ms，最小 100） | `claude-esp.exe -p 200` |
| 查看版本 | `claude-esp.exe -v` |

> 无参数运行时进入交互模式，自动选择最近的会话。

## 执行步骤

当用户需要查看会话时，按以下步骤操作：

### 第一步：获取插件路径

```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

若变量不可用，从插件缓存中查找：

```bash
cat ~/.claude/plugins/installed_plugins.json
```

找到 `claude-esp@alfie-qe` 的 `installPath`，即为插件根目录。

### 第二步：运行命令

将 `<plugin-root>` 替换为第一步获取的路径：

```bash
# 列出活跃会话
<plugin-root>/bin/claude-esp.exe -a

# 列出最近会话
<plugin-root>/bin/claude-esp.exe -l

# 监听指定会话（替换 <id>）
<plugin-root>/bin/claude-esp.exe -s <id>
```

### 第三步：根据用户需求继续

- 若用户要监听某个会话，使用 `-s <session-id>`
- 若只关心实时新事件，追加 `-n` 参数
- 若需要更快的刷新率，追加 `-p 200`（200ms）
