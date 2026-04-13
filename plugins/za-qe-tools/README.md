# za-qe-tools — QE 通用工具集

QE 通用工具集插件，提供 4 个可独立启停的功能模块。

## 功能模块

| 模块 | 功能 | 默认 | 说明 |
|------|------|------|------|
| **statusline** | 状态栏 | 开启 | Powerline/标准 双模式，实时显示模型、费用、进度 |
| **notify** | 系统通知 | 关闭 | 会话结束通知 + 权限等待超时提醒 |
| **dippy** | 命令审批 | 关闭 | Bash 命令 AST 分析，自动放行安全命令，拦截危险操作 |
| **esp** | 事件流查看 | 关闭 | 实时追踪和回放 Claude Code 会话事件 |

## 快速开始

### 查看/修改模块配置
```
/za-qe-tools:config
```

### 切换状态栏模式
```
/za-qe-tools:statusline-config powerline
/za-qe-tools:statusline-config standard
/za-qe-tools:statusline-config off
```

### 启动事件流查看（需先开启 ESP 模块）
```
/za-qe-tools:esp       # 新终端模式
/za-qe-tools:esp -w    # 交互式监听
```

## 配置文件

模块开关存储在 `~/.claude/za-qe-tools.json`：

```json
{
  "statusline": { "enabled": true, "mode": "powerline" },
  "notify": { "enabled": false },
  "dippy": { "enabled": false },
  "esp": { "enabled": false }
}
```

首次启动时自动创建，默认仅开启 statusline。

## 架构

所有 Hook 通过统一入口 `scripts/hook-router.py` 分发：
- 模块开启 → 执行对应逻辑
- 模块关闭 → 静默放行/跳过

```
SessionStart → auto-setup.js → 初始化配置 + statusline + dippy config
PreToolUse   → hook-router.py → dippy 命令审批（开关控制）
Stop         → hook-router.py → 会话结束通知（开关控制）
Permission   → hook-router.py → 权限等待通知（开关控制）
PostToolUse  → hook-router.py → 清除权限标记（开关控制）
```

## Dippy 命令审批

基于 AST 分析的 Bash 命令审批系统，支持 100+ 工具的安全判断。

- 默认规则：`~/.dippy/config`（首次开启时自动部署）
- 项目级规则：项目根目录 `.dippy` 文件
- 日志：`~/.claude/hook-approvals.log`

## ESP 事件流查看

预编译的 Claude Code 会话事件流工具，支持新终端和交互式两种模式。

## 版本

- v3.0.0 — 合并 za-dippy (v0.2.7) 和 za-claude-esp (v0.4.4)，统一模块配置
- v2.2.0 — Powerline 状态栏 + Windows 通知系统
