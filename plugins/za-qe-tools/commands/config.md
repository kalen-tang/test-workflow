---
description: "管理 za-qe-tools 各功能模块的配置。当用户说'配置工具'、'工具配置'、'开启dippy'、'关闭通知'、'模块管理'、'tools config'、'切换状态栏'、'关闭状态栏'、'状态栏配置' 时触发。"
argument-hint: "[模块名 on/off | statusline powerline/powerline-nf/standard/off]"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - AskUserQuestion
arguments:
  - name: module_action
    description: "可选：'<模块名> on/off' 或 'statusline powerline/powerline-nf/standard/off'。无参数进入交互式配置。"
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
/za-qe-tools:config statusline powerline-nf
/za-qe-tools:config statusline standard
/za-qe-tools:config statusline off
```

## 配置存储

- **dippy/notify/esp** 开关：`~/.claude/za-qe-tools.json`
- **statusline**：`~/.claude/settings.json` 的 `statusLine` 字段（由 auto-setup.py 管理）

## 可配置模块

| 模块 | 功能 | 默认 | 选项 |
|------|------|------|------|
| `statusline` | 状态栏 | 开启 (powerline) | powerline / powerline-nf / standard / off |
| `notify` | 会话结束 + 权限等待通知 | 关闭 | on / off |
| `dippy` | Bash 命令智能审批 | 关闭 | on / off |
| `esp` | 会话事件流查看 | 关闭 | on / off |

## 执行步骤

### 第一步：解析参数

检查用户是否直接指定了模块和状态：
- `/za-qe-tools:config dippy on` → 直接开启 dippy，跳到第三步
- `/za-qe-tools:config statusline standard` → 直接切换状态栏模式，跳到第三步
- 无参数 → 进入第二步交互式配置

### 第二步：交互式配置（无参数时）

直接使用 AskUserQuestion 展示选项，用户选择后拿着结果进入第三步：

```
questions:
  - header: "statusline"
    question: "状态栏模式："
    multiSelect: false
    options:
      - label: "powerline"
        description: "Powerline 箭头风格，兼容 Unicode 图标（无需特殊字体）"
      - label: "powerline-nf"
        description: "Powerline + Nerd Font 图标（需安装 NF 字体）"
      - label: "standard"
        description: "标准 ASCII，无需特殊字体"
      - label: "off"
        description: "关闭状态栏"
  - header: "notify"
    question: "系统通知："
    multiSelect: false
    options:
      - label: "on"
        description: "启用会话结束 + 权限等待通知"
      - label: "off"
        description: "禁用"
  - header: "dippy"
    question: "命令审批："
    multiSelect: false
    options:
      - label: "on"
        description: "启用 Bash 命令智能审批"
      - label: "off"
        description: "禁用"
  - header: "esp"
    question: "事件流查看："
    multiSelect: false
    options:
      - label: "on"
        description: "启用事件流查看"
      - label: "off"
        description: "禁用"
```

### 第三步：读取当前配置并写入

读取现有配置文件：

```bash
cat ~/.claude/za-qe-tools.json 2>/dev/null || echo '{}'
```

```bash
cat ~/.claude/settings.json 2>/dev/null | grep -o '"statusLine[^}]*}'
```

将用户的选择与现有配置合并，写入 `~/.claude/za-qe-tools.json`（dippy/notify/esp）。

### 第四步：处理 statusline

如果 statusline 模式发生变化（非第一步直接指定的情况，则基于用户选择）：

- `off` → `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/auto-setup.py off`
- `powerline` → `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/auto-setup.py powerline`
- `powerline-nf` → `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/auto-setup.py powerline-nf`
- `standard` → `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/auto-setup.py standard`

### 第五步：确认结果

告知用户配置已更新，列出当前各模块状态。

提示：**需要重启 Claude Code 生效**。

## 注意事项

- dippy/notify/esp 开关存储在 `~/.claude/za-qe-tools.json`，由 hook-router.py 统一读取
- statusline 通过 auto-setup.py 直接修改 `~/.claude/settings.json`
- dippy 已独立为 `claude-dippy` 包，通过 `uvx --from claude-dippy dippy` 调用，启停由 hook-router 控制
- esp 无 Hook，命令内部检查开关
