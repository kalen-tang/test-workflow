# za-claude-esp 插件 — Claude Code 会话事件流播放器

## 📌 概述

**za-claude-esp** 是 Claude Code 的**会话事件流播放器**（Event Stream Player），用于实时追踪、列举和回放 Claude Code 会话事件。

> **二进制已内置，无需额外安装，开箱即用。**

---

## ✨ 核心功能

- 📋 **列出会话** — 显示最近或活跃的 Claude Code 会话列表
- 👁️ **实时监听** — 实时追踪指定会话的事件流（消息、工具调用、思考过程）
- ⏭️ **灵活过滤** — 支持跳过历史事件，仅查看实时新事件
- ⏱️ **可调轮询** — 自定义事件流轮询间隔

---

## 🚀 快速开始

### 前置条件
- Claude Code 已安装
- za-claude-esp 插件已启用

### 基础命令

#### 查看活跃会话
```bash
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe -a
```
列出当前所有活跃的 Claude Code 会话。

#### 列出最近会话
```bash
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe -l
```
显示最近 10 个会话记录。

#### 监听指定会话
```bash
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe -s <session-id>
```
实时显示指定会话 ID 的事件流。

#### 交互模式（推荐）
```bash
${CLAUDE_PLUGIN_ROOT}/bin/claude-esp.exe
```
进入交互模式，程序会自动选择最近活跃的会话，并以实时流形式显示所有事件。

---

## 📊 事件流信息

通过 za-claude-esp 可以查看的事件包括：

| 事件类型 | 说明 |
|---------|------|
| **Message** | Claude 的消息或用户输入 |
| **Tool Call** | Claude 调用的工具（如 Bash、Read、Edit） |
| **Tool Result** | 工具执行结果 |
| **Thinking** | Claude 的思考过程（O1 模式） |
| **Status** | 会话状态变化 |

---

## 🛠️ Skills 说明

| Skill 名称 | 触发场景 | 功能 |
|-----------|---------|------|
| `esp` | 用户说"打开esp"、"启动esp"、"监听会话"等 | 主入口，支持 -w 参数 |
| `esp_terminal` | 内部调用 | 启动新终端 |
| `esp_watch` | 内部调用 | 交互式监听 |

---

## 💡 使用场景

### 场景 1：启动新终端调试
```bash
/esp
```
在新终端窗口中启动 esp，自动连接最近的活跃会话。

### 场景 2：交互式监听会话
```bash
/esp -w
```
在当前会话中交互式选择并监听会话事件流。

### 场景 3：性能分析
通过观察事件流时间戳，分析 Claude 各步骤耗时。

---

## ⚙️ 版本信息

| 项目 | 值 |
|-----|-----|
| **版本** | v0.4.4 |
| **上游** | [github.com/phiat/claude-esp](https://github.com/phiat/claude-esp) |
| **作者** | phiat |
| **平台** | Windows（.exe）、macOS、Linux 通过源代码 |

---

## 🔗 相关命令

- `/esp` — 启动 esp（新终端）
- `/esp -w` — 交互式监听会话

---

## ❓ 常见问题

**Q: 事件流中看不到思考过程？**  
A: 确保使用支持 Extended Thinking 的 Claude 模型（如 Claude 4.x），并在 Claude Code 中启用思考模式。

**Q: 如何获取 session-id？**  
A: 运行 `claude-esp.exe -l` 列出最近会话，每个会话前会显示 ID。

**Q: 监听事件时实时性如何？**  
A: 默认轮询间隔为 500ms，可通过命令行参数调整。

---

## 📝 配置文件路径

- **插件根目录** — `~/.claude/plugins/marketplaces/alfie-qe/plugins/za-claude-esp/`
- **二进制文件** — `bin/claude-esp.exe`
- **Skills 定义** — `skills/` 目录

---

## 🔧 故障排除

### 新窗口未弹出
- 检查是否安装了 Windows Terminal（推荐）
- 手动运行：`cd <bin目录> && .\claude-esp.exe`

### 无法连接到会话
- 确保 Claude Code 正在运行
- 确认会话 ID 正确（运行 `claude-esp.exe -l` 查看）

### 权限不足
- 确保有权限访问 Claude 会话数据目录

---

## 📚 扩展阅读

- [Claude Code 官方文档](https://claude.ai/code)
- [Dippy 命令审批工具](./za-dippy/README_zh.md)

