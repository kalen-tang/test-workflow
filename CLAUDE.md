# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概述

基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案。

- **Marketplace**：`alfie-qe`（owner: Alfie）
- **仓库地址**：`https://gitlab.in.za/claude/alfie/qe`
- **完整文档**：`README.md`（安装说明）、`docs/alfie-plugin-spec.md`（插件规范）

## 🚀 常用命令

```bash
# 全流程测试左移（推荐，交互式引导）
/za-qe:qe-workflow

# 指定目录直接执行
/za-qe:qe-workflow --req_dir ./docs/req --design_dir ./docs/design --output_dir ./result

# 场景案例生成（PlantUML流程图+MindMap）
/za-qe:qe-gencase ./docs/requirement.md

# 需求文档标准化
/za-qe:req-parser ./docs/requirement.docx

# 查看帮助
/za-qe:qe-help
```

## 🏗️ 项目架构

### 插件系统两级配置

1. **项目级**：`.claude-plugin/marketplace.json` — 定义可用插件（`core`/`optional`）
2. **插件级**：`plugins/<name>/.claude-plugin/plugin.json` — 插件元数据，声明 `commands`/`skills` 路径

### 插件清单

| 插件 | 版本 | 类型 | 用途 |
|------|------|------|------|
| `za-qe` | v2.5.9 | core | 测试左移工具集：需求分析、场景案例、API用例生成（8 个 Skills） |
| `za-qe-tools` | v3.3.1 | optional | 通用工具集：状态栏 + 系统通知 + 命令审批(Dippy) + 事件流查看(ESP) |
| `za-qe-ui` | v1.0.0 | optional | UI自动化测试：Playwright转换、修复、增量更新 |
| `za-qe-perf` | v1.0.0 | 独立 | INVEST 微服务框架性能测试与规范检查（未注册到 marketplace） |

### za-qe 核心 Skills（`plugins/za-qe/skills/`）

| Skill | 用途 |
|-------|------|
| `req-parser` | 将原始需求文档转为标准化 Markdown（7 章 PRD 模板） |
| `design-parser` | 检查开发方案文档是否符合规范 |
| `doc-converter` | 将 docx/doc 文档批量转换为 UTF-8 Markdown |
| `interface-extractor` | 从设计文档提取接口数据，生成接口数据报告 |
| `case-designer` | 生成 PlantUML 流程图、测试用例 MindMap 和场景案例表 |
| `api-generator` | 生成 Python pytest 测试代码和 YAML 数据 |
| `doc-reviewer` | 验证需求实现一致性 |
| `code-diff-analysis` | 分析需求代码变更，识别质量风险，输出测试策略 |

### 数据流管道

全流程工作流（`/za-qe:qe-workflow`）按阶段串行调用 Skills：

```
输入: 需求文档 + 设计文档 (docx/doc)
  ↓ [阶段0] 断点续传检测（读取已有 workflow.md 判断是否恢复）
  ↓ [阶段1] 环境探测 + 交互式配置（需求/设计/输出/自动化项目目录）
  ↓ [阶段2] doc-converter: uvx markitdown → UTF-8 Markdown
  ↓ [阶段3] Skill 链式调用:
      req-parser → BANK-XXXX_PRD.md
      design-parser → BANK-XXXX_DESIGN.md
      interface-extractor → temp/BANK-XXXX_接口数据报告.md
      case-designer → BANK-XXXX_CASE.md + .xmind + temp/CASE_TABLE.md
      api-generator → pytest test_*.py + YAML 数据文件
```

命令通过 `Skill()` 工具调用 Skills，每个 Skill 通过 `TaskCreate`/`TaskUpdate` 追踪进度。

### 权限模型

- **插件级权限**：`plugins/za-qe/settings.json` — 声明 workflow 命令可用的工具和可调用的 Skills
- **Skill 级权限**：每个 `SKILL.md` frontmatter 中的 `allowed-tools` 字段 — 约束单个 Skill 可用的工具
- Bash 命令只允许 `uv run *` 和 `uvx *`，不允许任意 shell 命令

### za-qe-tools Hooks 系统

`za-qe-tools` 通过 `plugin.json` 注册生命周期 hooks，由 `scripts/hook-router.py` 统一路由：

- `SessionStart` → 自动配置（auto-setup.py）
- `PreToolUse` (Bash) → 命令审批
- `PostToolUse` / `PostToolUseFailure` / `Stop` / `PermissionRequest` → 事件流记录

## 🔧 工具链与依赖

- **uv**：Python 包管理 + 脚本运行（`uv run`、`uvx`）
- **markitdown**：docx/doc → markdown 转换（通过 `uvx markitdown` 调用）
- **PlantUML**：活动图 + MindMap 渲染（通过 HTTP API `plantuml.in.za` 校验）
- **Python 脚本**：使用 PEP 723 内联依赖声明，无需 pyproject.toml

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx>=0.27.0"]
# ///
```

## 📝 开发规范

### 命名规范

- **插件名**：`za-{域}` 格式（如 `za-qe`、`za-qe-tools`）
- **命令前缀**：`/za-qe:xxx`
- **Skill 命名**：`{功能域}-{类型后缀}`，通用名加 `qe-` 前缀避免冲突
- **SKILL.md frontmatter**：`status` 使用纯文本（`active`），不用 emoji

### 新增或更新 Skill 时需同步更新的文件

1. `skills/<skill-name>/SKILL.md`（含 YAML frontmatter：name、description、version、status、allowed-tools）
2. `skills/<skill-name>/references/` 参考文档（编号前缀：`01-xxx.md`）
3. `skills/<skill-name>/examples/` 示例文件
4. `commands/<command-name>.md`（如需工作流命令，使用 `/za-qe:` 前缀）
5. `.claude-plugin/marketplace.json` 和 `plugins/za-qe/.claude-plugin/plugin.json`（版本号 + 描述）
6. `plugins/za-qe/README.md`、`commands/help.md`、`commands/status.md`
7. 项目根 `README.md` 和本 `CLAUDE.md`

**参考示例**：`case-designer` Skill（完整实现，含 scripts/references/examples）

### 关键规范

- Skill 引用 references 文档使用**无 `./` 前缀的相对路径**：`references/xxx.md`（不写 `./references/xxx.md`）
- 版本号遵循 SemVer：新增 Skill/Command → 次版本升级（`1.3.0 → 1.4.0`）
- 所有文档中 Skills 数量和版本号必须保持一致
- `plugin.json` 必须放在 `.claude-plugin/` 子目录下
- 参考文档统一放在 `plugins/za-qe/skills/<name>/references/` 下（Skill 专属，无插件级 references）
- 多个 Skill 共享的文档各自维护一份副本

### 扩展插件时

添加 hooks、MCP、拆分多插件、skills.json 索引等，参考 `docs/alfie-plugin-spec.md`。

## 🔧 关键技术点

### 接口路径校验

- 微服务接口格式：`微服务域名/接口路径`，如 `zabank_imc_activity_service/activity/list`
- 路径包含 `dmb` → 判定为**网关接口**，必须提示用户替换为微服务接口
- 详细规则：`plugins/za-qe/skills/interface-extractor/references/01-interface-validation.md`

### API 测试代码生成规范

- 框架：pytest，风格：PEP 8，行长：180 字符
- YAML 测试数据支持三环境：`sit`、`auto_qe`、`uat`
- 参考文档：`skills/api-generator/references/00-yaml-format.md`、`01-test-code-template.md`

### Playwright MCP（可选）

```bash
claude mcp add playwright npx @playwright/mcp@latest
```
用于从网页（如 UDoc 接口文档，域名 `udoc.in.za`）提取内容。

## 📚 重要文档路径

| 文档 | 路径 |
|------|------|
| 插件规范（扩展参考） | `docs/alfie-plugin-spec.md` |
| 系统架构图 | `architecture.puml` |
| 工作流权限配置 | `plugins/za-qe/settings.json` |
| req-parser Skill | `plugins/za-qe/skills/req-parser/SKILL.md` |
| PRD 模板 | `plugins/za-qe/skills/req-parser/references/prd-template.md` |
| api-generator 参考 | `plugins/za-qe/skills/api-generator/references/` |
| interface-extractor 参考 | `plugins/za-qe/skills/interface-extractor/references/` |
