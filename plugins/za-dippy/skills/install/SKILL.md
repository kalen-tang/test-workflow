---
name: install
description: "安装 Dippy：将 PreToolUse hook 和 enabledPlugins 写入 ~/.claude/settings.json，并部署默认配置到 ~/.dippy/config。当用户执行 /dippy:install 或明确说'安装dippy'、'配置dippy'、'install dippy'、'dippy不生效'时触发。不应被通用的 setup/install 请求触发。"
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Dippy 安装配置

将 Dippy 的 PreToolUse hook 写入用户全局 `~/.claude/settings.json`，并启用插件，使 Bash 命令智能审批生效。

## 背景

Claude Code 插件的 `hooks.json` 在 `statusLine` 场景下无法自动注入到用户全局配置。
Dippy 的 hook 需要**绝对路径**写入 `~/.claude/settings.json` 的 `PreToolUse` 才能生效。
此 Skill 自动完成路径检测、hook 注入、插件启用、默认配置部署全流程。

## 执行步骤

### 第一步：检测插件安装路径

运行以下命令获取 dippy 插件绝对路径：

```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

如果变量为空，则读取插件缓存索引：

```bash
cat ~/.claude/plugins/installed_plugins.json
```

从中找到 `dippy@alfie-qe` 的 `installPath`，即为插件根目录。

### 第二步：读取当前 settings.json

读取 `~/.claude/settings.json`（Windows 路径：`C:/Users/<用户名>/.claude/settings.json`）。

### 第三步：检查是否已安装

检查以下两个条件是否都已满足：

1. `enabledPlugins` 中存在 `"dippy@alfie-qe": true`
2. `hooks.PreToolUse` 中存在指向该插件 `bin/dippy-hook` 的 command

如果都已满足，告知用户 Dippy 已安装完成，无需操作。

### 第四步：写入 PreToolUse hook

在 `settings.json` 的 `hooks.PreToolUse` 数组**首位**插入以下配置（将 `<插件根目录>` 替换为第一步检测到的实际绝对路径，路径统一使用正斜杠）：

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "python <插件根目录>/bin/dippy-hook"
    }
  ]
}
```

**注意**：如果 `PreToolUse` 中已存在其他指向旧路径或重复的 dippy hook，先删除再插入，避免重复。

### 第五步：启用插件

在 `settings.json` 的 `enabledPlugins` 中添加：

```json
"dippy@alfie-qe": true
```

### 第六步：部署默认配置

检查 `~/.dippy/config` 是否已存在：

- **已存在** → 跳过，提示用户配置已保留
- **不存在** → 将插件目录下的 `config/default.dippy` 复制到 `~/.dippy/config`

```bash
# 检查
ls ~/.dippy/config 2>/dev/null && echo "exists" || echo "missing"
```

如果需要复制，使用 Write 工具将 `<插件根目录>/config/default.dippy` 的内容写入 `~/.dippy/config`。

### 第七步：确认完成

告知用户安装结果，例如：

```
Dippy 安装完成 ✓
• Hook 已写入 ~/.claude/settings.json
• 默认配置已部署到 ~/.dippy/config
• 重启 Claude Code 后生效

如需自定义规则，在项目根目录创建 .dippy 文件即可。
```

## 注意事项

- `${CLAUDE_PLUGIN_ROOT}` 在 hook 执行时可用，但写入 `settings.json` 的路径必须是**绝对路径**
- 路径统一使用正斜杠（`/`），兼容跨平台
- **仅修改** `hooks.PreToolUse`、`enabledPlugins` 这两个字段，不要覆盖 `settings.json` 中的其他配置
- 如果用户的 `settings.json` 不存在，先创建 `{ }` 再写入
