---
name: watch-session
description: "交互式监听 Claude Code 会话事件流。当用户说'查看会话'、'监听会话'、'esp -w'、'/esp -w'、'watch'、'交互式监听' 时触发。"
version: 0.4.4
allowed-tools:
  - Bash
---

# /esp -w — 交互式监听会话

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
