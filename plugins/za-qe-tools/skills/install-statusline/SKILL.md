---
name: install-statusline
description: "安装状态栏：将 statusLine 写入用户的 ~/.claude/settings.json。当用户执行 /za-qe-tools:install-statusline 或明确说'安装状态栏'、'配置状态栏'、'install statusline'、'statusline 不显示' 时触发。不应被通用的 setup/install 请求触发。"
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# 状态栏安装配置

将 statusLine 配置写入用户全局 `~/.claude/settings.json`，使状态栏正常显示。

## 背景

Claude Code 只从用户全局 `settings.json` 读取 `statusLine`，不会自动合并插件的 `settings.json`。此 Skill 用于弥补这一差距，支持两个版本：

- **Powerline 版**（`statusline-powerline.py`）：Powerline 箭头风格，需要终端安装 Powerline 字体
- **普通版**（`statusline.py`）：使用标准 ASCII 字符，无需特殊字体

## 执行步骤

### 第一步：询问用户终端是否已安装 Powerline 字体

向用户提问：

> 你的终端是否已安装 Powerline 字体（如 MesloLGS NF、Nerd Fonts 等）？
> - 是 → 使用 Powerline 版（箭头风格，更美观）
> - 否 / 不确定 → 使用普通版（标准字符，兼容性更好）

等待用户回答后再继续。

### 第二步：检测插件安装路径

运行以下命令获取插件绝对路径：

```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

如果变量不可用，则查询插件缓存目录：

```bash
cat ~/.claude/plugins/installed_plugins.json
```

从中找到 `za-qe-tools@alfie-qe` 的 `installPath`，即为插件根目录。

### 第三步：读取当前配置

读取 `~/.claude/settings.json`（Windows 路径：`C:/Users/<用户名>/.claude/settings.json`）。

### 第四步：检查是否已配置

如果 `statusLine` 已存在且指向本插件的脚本，告知用户已配置完成，无需操作。

### 第五步：写入 statusLine 配置

根据用户选择，在 `settings.json` 中添加或更新 `statusLine` 字段：

**Powerline 版：**
```json
"statusLine": {
  "type": "command",
  "command": "uv run <插件根目录>/scripts/statusline-powerline.py",
  "padding": 2
}
```

**普通版：**
```json
"statusLine": {
  "type": "command",
  "command": "uv run <插件根目录>/scripts/statusline.py",
  "padding": 2
}
```

将 `<插件根目录>` 替换为第二步检测到的实际绝对路径，路径统一使用正斜杠。

### 第六步：确认完成

告知用户配置完成，需要重启 Claude Code 使状态栏生效。

## 注意事项

- `${CLAUDE_PLUGIN_ROOT}` 在 hooks 中可用，但在 `statusLine.command` 运行时**不可用**，写入 `settings.json` 的路径必须是**绝对路径**。
- 路径统一使用正斜杠（`/`），兼容跨平台。
- **仅操作 `statusLine` 字段**，不要覆盖 `settings.json` 中的其他配置。
