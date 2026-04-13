---
name: watch-session
description: "交互式监听 Claude Code 会话事件流（通过 /esp -w 调用）。当用户说'查看会话'、'监听会话'、'交互式监听' 时触发。"
version: 0.4.4
allowed-tools:
  - Bash
---

# 交互式会话监听

## 执行步骤

### 第一步：获取插件路径

```bash
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
if [ -z "$PLUGIN_ROOT" ]; then
  PLUGIN_ROOT="$HOME/.claude/plugins/marketplaces/alfie-qe/plugins/za-qe-tools"
fi
BIN_PATH="$PLUGIN_ROOT/bin/claude-esp.exe"
```

### 第二步：进入交互模式

```bash
"$BIN_PATH"
```

### 常用命令参考

| 功能 | 命令 |
|------|------|
| 列出活跃会话 | `$BIN_PATH -a` |
| 列出最近会话 | `$BIN_PATH -l` |
| 监听指定会话 | `$BIN_PATH -s <session-id>` |
| 跳过历史只看新事件 | `$BIN_PATH -n -s <session-id>` |
