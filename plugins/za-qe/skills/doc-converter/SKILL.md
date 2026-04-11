---
name: doc-converter
description: 将 docx/doc 文档批量转换为 UTF-8 Markdown。当用户说"转换文档"、"docx 转 md"、"doc 转 markdown"、"转换需求文档格式"、"文档格式转换"，或 workflow 需要将 Word 文档转为 md 时应触发。
status: active
allowed-tools: Read, Write, Grep, Glob, Bash(uv run:*), Bash, TodoWrite, AskUserQuestion,  Skill, Task
---

# 文档转换器

## 技能目标

将目录中的 `.docx`/`.doc` 文件批量转换为 UTF-8 编码的 Markdown 文件，并自动修复编码问题。作为 workflow 阶段 2 的执行者，也可独立使用。

## 输入

- **输入目录**：包含 `.docx`/`.doc` 文件的目录路径（绝对路径）
- **输出目录**：Markdown 文件输出目录路径（绝对路径，不存在时自动创建）
- **文件名前缀**（可选）：输出文件名前缀（如 `design_`，用于区分设计文档）

## 输出

- 每个 docx/doc 文件对应一个 `.md` 文件，文件名保持一致（仅扩展名改为 `.md`）
- 所有输出文件确保为 UTF-8 编码

## 执行流程

### 步骤 1：调用转换脚本

使用绝对路径调用 `convert_docx.py` 脚本，一次性完成转换和编码修复：

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/convert_docx.py" '<输入目录绝对路径>' '<输出目录绝对路径>'
```

如果需要添加文件名前缀（如设计文档）：

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/convert_docx.py" '<输入目录绝对路径>' '<输出目录绝对路径>' --prefix design_
```

### 步骤 2：解读脚本输出

脚本输出格式：
- `OK: <path>` — 转换成功，已是 UTF-8
- `FIXED: <path> from <enc>` — 转换成功，编码已从 enc 修复为 UTF-8
- `WARN: <path>` — 转换成功，但编码无法自动识别，需人工检查
- `ERROR: <path> <msg>` — 转换失败

### 步骤 3：汇报结果

输出转换汇总：
```
文档转换完成：
  成功：N 个
  编码修复：M 个
  失败：K 个
```

如果有失败文件，列出失败原因。

## 脚本工具

- **`scripts/convert_docx.py`** — 批量 docx/doc → Markdown 转换 + 编码修复（一体化）
  - 依赖：`markitdown[docx]>=0.1.0`（uv 自动管理）
  - 编码检测优先级：utf-8 → utf-8-sig → gb18030 → big5 → utf-16
  - 转换完每个文件后自动检查并修复编码

## 注意事项

- 始终使用**绝对路径**，禁止 `cd` 切换目录
- 禁止使用 `;` 连接命令
- 使用 `${CLAUDE_SKILL_DIR}` 引用脚本路径，确保跨安装环境可用
