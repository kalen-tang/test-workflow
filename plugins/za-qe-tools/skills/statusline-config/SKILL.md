---
name: statusline-config
description: "配置状态栏显示模式。当用户说'切换状态栏'、'关闭状态栏'、'取消statusline'、'换成普通状态栏'、'statusline config'、'状态栏配置' 时触发。"
argument-hint: "<powerline|standard|off>"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - AskUserQuestion
---

# 状态栏配置

修改 `~/.claude/settings.json` 中的 `statusLine` 配置。

## 支持的模式

| 模式 | 说明 |
|------|------|
| `powerline` | Powerline 箭头风格（需终端安装 Powerline/Nerd 字体） |
| `standard` | 标准 ASCII 字符，无需特殊字体 |
| `off` | 关闭状态栏显示 |

## 执行步骤

### 1. 解析参数

从用户输入中识别目标模式：
- 包含 `powerline` → powerline 模式
- 包含 `standard`/`普通`/`标准` → standard 模式
- 包含 `off`/`关闭`/`取消`/`disable` → off 模式
- 无参数或不明确 → 用 AskUserQuestion 询问用户选择

### 2. 检测插件路径

```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

如果变量不可用，查询插件缓存：

```bash
cat ~/.claude/plugins/installed_plugins.json
```

从中找到 `za-qe-tools@alfie-qe` 的 `installPath`。

### 3. 读取当前配置

读取 `~/.claude/settings.json`。

### 4. 修改配置

根据目标模式修改 `statusLine` 字段：

**powerline 模式：**
```json
"statusLine": {
  "type": "command",
  "command": "uv run <插件绝对路径>/scripts/statusline-powerline.py",
  "padding": 2
}
```

**standard 模式：**
```json
"statusLine": {
  "type": "command",
  "command": "uv run <插件绝对路径>/scripts/statusline.py",
  "padding": 2
}
```

**off 模式：**
删除 `settings.json` 中的 `statusLine` 字段。

将 `<插件绝对路径>` 替换为第 2 步检测到的实际路径，路径统一使用正斜杠。

### 5. 写入并确认

使用 Edit 工具修改 `settings.json`（仅修改 `statusLine` 字段，不影响其他配置）。

告知用户配置完成，需要重启 Claude Code 生效。

## 注意事项

- `${CLAUDE_PLUGIN_ROOT}` 在 hooks 中可用，但在 `statusLine.command` 运行时不可用，路径必须是绝对路径
- 路径统一使用正斜杠（`/`），兼容跨平台
- **仅操作 `statusLine` 字段**，不覆盖其他配置
