---
name: tools-config
description: "管理 za-qe-tools 各功能模块的启停配置。当用户说'配置工具'、'工具配置'、'开启dippy'、'关闭通知'、'模块管理'、'tools config'、'/za-qe-tools:config' 时触发。"
argument-hint: "[模块名 on/off]"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - AskUserQuestion
---

# za-qe-tools 模块配置

管理 za-qe-tools 各功能模块的启用/禁用状态。

## 配置文件

配置存储在 `~/.claude/za-qe-tools.json`，格式：

```json
{
  "statusline": { "enabled": true, "mode": "powerline" },
  "notify": { "enabled": false },
  "dippy": { "enabled": false },
  "esp": { "enabled": false }
}
```

## 模块说明

| 模块 | 功能 | 默认 |
|------|------|------|
| `statusline` | Powerline/标准 状态栏 | 开启 (powerline) |
| `notify` | 会话结束通知 + 权限等待通知 | 关闭 |
| `dippy` | Bash 命令智能审批（AST 分析） | 关闭 |
| `esp` | 会话事件流查看工具 | 关闭 |

## 执行步骤

### 第一步：读取当前配置

```bash
cat ~/.claude/za-qe-tools.json 2>/dev/null || echo "not found"
```

如果配置文件不存在，使用默认值创建。

### 第二步：解析参数

检查用户是否直接指定了模块和状态：
- `/za-qe-tools:config dippy on` → 直接开启 dippy
- `/za-qe-tools:config notify off` → 直接关闭 notify
- 无参数 → 进入交互式配置

### 第三步：交互式配置（无参数时）

使用 AskUserQuestion 展示当前状态，让用户选择要切换的模块。

用 multiSelect 问题展示所有模块及其当前状态，让用户选择要**切换**（toggle）的模块。

示例问题格式：
```
选择要切换状态的模块（当前已开启的模块取消选中即关闭）：
  ✅ statusline (powerline) — 状态栏
  ❌ notify — 会话结束/权限等待通知
  ❌ dippy — Bash 命令智能审批
  ❌ esp — 会话事件流查看
```

### 第四步：更新配置文件

将用户选择写入 `~/.claude/za-qe-tools.json`。

### 第五步：处理 statusline 特殊逻辑

如果 statusline 状态发生变化：
- **关闭** → 读取 `~/.claude/settings.json`，删除 `statusLine` 字段
- **开启** → 读取 `~/.claude/settings.json`，写入 statusLine 配置（需要检测插件路径）

statusline 路径检测：
```bash
echo "${CLAUDE_PLUGIN_ROOT}"
```

如果变量不可用，查询：
```bash
cat ~/.claude/plugins/installed_plugins.json
```

从中找到 `za-qe-tools@alfie-qe` 的 `installPath`。

### 第六步：处理 dippy 首次开启

如果 dippy 从关闭切换为开启：
- 检查 `~/.dippy/config` 是否存在
- 不存在则从插件目录 `config/default.dippy` 复制

### 第七步：确认结果

告知用户配置已更新，列出当前各模块状态。

提示：**需要重启 Claude Code 才能使 Hook 相关变更（dippy/notify）完全生效**。
statusline 的变更则需要重启生效。
esp 的开启/关闭不涉及 Hook，Skill 内部会检查开关状态。

## 注意事项

- 仅修改 `~/.claude/za-qe-tools.json`，不修改 `plugin.json`
- statusline 变更需要同步修改 `~/.claude/settings.json`
- dippy 的 Hook 始终注册在 plugin.json 中，通过 hook-router.py 内部检查开关
- esp 无 Hook，仅 Skill 内部检查开关
