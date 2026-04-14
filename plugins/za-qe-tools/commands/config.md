---
name: config
description: "管理 za-qe-tools 各功能模块的配置。当用户说'配置工具'、'工具配置'、'开启dippy'、'关闭通知'、'模块管理'、'tools config'、'切换状态栏'、'关闭状态栏'、'状态栏配置' 时触发。"
argument-hint: "[模块名 on/off | statusline powerline/standard/off]"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - AskUserQuestion
arguments:
  - name: module_action
    description: "可选：'<模块名> on/off' 或 'statusline powerline/standard/off'。无参数进入交互式配置。"
    required: false
---

# /za-qe-tools:config — 模块配置管理

统一管理 za-qe-tools 所有功能模块的配置。

## 使用方法

### 交互式配置（推荐）
```
/za-qe-tools:config
```

### 直接指定
```
/za-qe-tools:config dippy on
/za-qe-tools:config notify off
/za-qe-tools:config esp on
/za-qe-tools:config statusline powerline
/za-qe-tools:config statusline standard
/za-qe-tools:config statusline off
```

## 配置文件

配置存储在 `~/.claude/za-qe-tools.json`：

```json
{
  "statusline": { "enabled": true, "mode": "powerline" },
  "notify": { "enabled": false },
  "dippy": { "enabled": false },
  "esp": { "enabled": false }
}
```

## 可配置模块

| 模块 | 功能 | 默认 | 选项 |
|------|------|------|------|
| `statusline` | 状态栏 | 开启 (powerline) | powerline / standard / off |
| `notify` | 会话结束 + 权限等待通知 | 关闭 | on / off |
| `dippy` | Bash 命令智能审批 | 关闭 | on / off |
| `esp` | 会话事件流查看 | 关闭 | on / off |

## 执行步骤

### 第一步：读取当前配置

```bash
cat ~/.claude/za-qe-tools.json 2>/dev/null || echo "not found"
```

如果配置文件不存在，使用默认值创建。

### 第二步：解析参数

检查用户是否直接指定了模块和状态：
- `/za-qe-tools:config dippy on` → 直接开启 dippy，跳到第四步
- `/za-qe-tools:config statusline standard` → 直接切换状态栏模式，跳到第四步
- 无参数 → 进入第三步交互式配置

### 第三步：交互式配置（无参数时）

使用 AskUserQuestion 展示两个问题：

**问题 1：选择要配置的模块**（单选）

```
header: "模块"
question: "选择要配置的模块："
options:
  - label: "statusline"
    description: "状态栏 — 当前：powerline"
  - label: "dippy"
    description: "Bash 命令审批 — 当前：关闭"
  - label: "notify"
    description: "系统通知 — 当前：关闭"
  - label: "esp"
    description: "事件流查看 — 当前：关闭"
```

**问题 2：根据选中模块展示对应选项**

如果选了 `statusline`：
```
header: "模式"
question: "选择状态栏模式："
options:
  - label: "powerline"
    description: "Powerline 箭头风格（需 Nerd 字体）"
  - label: "standard"
    description: "标准 ASCII，无需特殊字体"
  - label: "off"
    description: "关闭状态栏"
```

如果选了 `dippy`/`notify`/`esp`：
```
header: "状态"
question: "设置 <模块名> 状态："
options:
  - label: "on"
    description: "启用"
  - label: "off"
    description: "禁用"
```

### 第四步：更新配置文件

将用户选择写入 `~/.claude/za-qe-tools.json`。

### 第五步：处理 statusline 特殊逻辑

如果 statusline 配置发生变化，需要同步修改 `~/.claude/settings.json`：

先检测插件路径：
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

如果变量不可用，查询：
```bash
cat ~/.claude/plugins/installed_plugins.json
```
从中找到 `za-qe-tools@alfie-qe` 的 `installPath`。

根据目标模式修改 `settings.json` 的 `statusLine` 字段：

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

将 `<插件绝对路径>` 替换为检测到的实际路径，路径统一使用正斜杠。

同步更新 `za-qe-tools.json` 中的 `statusline` 字段：
- powerline → `{ "enabled": true, "mode": "powerline" }`
- standard → `{ "enabled": true, "mode": "standard" }`
- off → `{ "enabled": false, "mode": "powerline" }`

### 第六步：确认结果

告知用户配置已更新，列出当前各模块状态。

提示：**需要重启 Claude Code 生效**。

## 注意事项

- 仅修改 `~/.claude/za-qe-tools.json`（和 statusline 的 `settings.json`），不修改 `plugin.json`
- `${CLAUDE_PLUGIN_ROOT}` 在 hooks 中可用，但 `statusLine.command` 运行时不可用，路径必须是绝对路径
- 路径统一使用正斜杠，兼容跨平台
- dippy 已独立为 `claude-dippy` 包，通过 `uvx claude-dippy` 调用，启停由本配置控制
- esp 无 Hook，命令内部检查开关
