---
name: esp
description: 启动 Claude Code 会话事件流查看工具
triggers:
  - /za-qe-tools:esp
  - /za-qe-tools:esp -w
execution:
  type: skill
  skill: launch
arguments:
  - name: mode
    description: "可选：'-w' 表示交互式监听模式，缺省为新终端模式"
    required: false
---

# /za-qe-tools:esp — Claude Code 会话事件流查看工具

启动 claude-esp 工具查看 Claude Code 会话事件。

## 使用方法

### 新终端模式（默认）
`/za-qe-tools:esp`

### 交互式监听模式
`/za-qe-tools:esp -w`

## 前置条件

ESP 模块需要通过 `/za-qe-tools:config` 开启后才可使用。
