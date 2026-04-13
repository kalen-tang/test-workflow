---
name: config
description: 管理 za-qe-tools 各功能模块的启停配置
triggers:
  - /za-qe-tools:config
execution:
  type: skill
  skill: tools-config
arguments:
  - name: module_action
    description: "可选：'<模块名> on/off'，如 'dippy on'。无参数进入交互式配置。"
    required: false
---

# /za-qe-tools:config — 模块配置管理

管理 za-qe-tools 通用工具集中各功能模块的启用/禁用。

## 使用方法

### 交互式配置（推荐）
```
/za-qe-tools:config
```

### 直接指定
```
/za-qe-tools:config dippy on
/za-qe-tools:config notify off
/za-qe-tools:config statusline standard
```

## 可配置模块

| 模块 | 说明 | 默认 |
|------|------|------|
| statusline | 状态栏（powerline/standard/off） | 开启 (powerline) |
| notify | 系统通知（会话结束+权限等待） | 关闭 |
| dippy | Bash 命令智能审批 | 关闭 |
| esp | 会话事件流查看 | 关闭 |
