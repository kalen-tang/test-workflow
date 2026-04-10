# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概述

基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案。核心是 `za-qe` 插件（`plugins/za-qe/`），包含六个核心 Skills 和六个工作流命令。

- **Marketplace**：`alfie-qe`（owner: Alfie）
- **仓库地址**：`https://gitlab.in.za/claude/alfie/qe`
- **完整文档**：`README.md`（安装说明、架构图）
- **插件规范**：`docs/alfie-plugin-spec.md`（当前适用规范 + 扩展时参考）

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
<<<<<<< HEAD
2. **插件级**：`plugins/za-qe/.claude-plugin/plugin.json` — 插件元数据（当前 v1.4.0），声明 `commands`/`skills` 路径

### 核心与可选插件

| 插件 | 类型 | 用途 |
|------|------|------|
| `za-qe` | core | 测试左移工具集：需求分析、场景案例、API用例生成 |
| `za-qe-tools` | optional | 状态栏 + Windows 通知系统 |
| `za-ui` | optional | UI自动化测试：Playwright转换、修复、增量更新 |
| `za-dippy` | optional | Bash命令智能审批：自动放行安全命令，拦截危险操作 |
| `za-claude-esp` | optional | 会话事件流查看工具：实时追踪、回放 Claude Code 会话 |

所有 Skill 位于 `plugins/za-qe/skills/` 下：

| Skill | 状态 | 用途 |
|-------|------|------|
| `interface-extractor` | ✅ | 从设计文档提取接口数据，生成接口数据报告 |
| `doc-reviewer` | ✅ | 验证需求实现一致性 |
| `case-designer` | ✅ | 生成 PlantUML 流程图、测试用例 MindMap 和场景案例表 |
| `api-generator` | ✅ | 生成 Python pytest 测试代码和 YAML 数据 |
| `req-parser` | ✅ | 将原始需求文档转为标准化 Markdown |
| `design-parser` | ✅ | 检查开发方案文档是否符合规范 |

### 工作流模式

**全流程模式**（`/za-qe:qe-workflow`，✅ 推荐）：
- 阶段 1：环境探测 + 交互式目录配置（需求文档/设计文档/输出/自动化项目）
- 阶段 2：`uvx markitdown` docx/doc → md + UTF-8 编码修复
- 阶段 3：`req-parser` → `design-parser` → `interface-extractor` → `case-designer` → `api-generator`
- 输出：规范化文档 + 测试左移分析报告 + API 自动化测试用例

### Artifact Schemas（完整模式核心协议）

完整模式各 Skill 之间通过标准化 YAML 格式通信，定义在 `plugins/za-qe/references/artifact-schemas/`：

| 编号 | 格式 | 产出工具 | 状态 |
|------|------|---------|------|
| 01 | normalized-requirement | req-parser | ✅ v2.0 |
| 02 | normalized-design | design-parser | ✅ v1.0 |
| 03 | normalized-cases | case-normalizer | 📋 计划中 |
| 04 | code-diff-report | code-diff-mcp | 📋 计划中 |
| 05 | validation-report | doc-reviewer | ✅ v1.0 |
| 06 | manual-test-cases | case-designer | ✅ v1.0 |
| 07 | api-test-cases | api-generator | ✅ v1.0 |

**总览文档**：`plugins/za-qe/references/artifact-schemas/00-overview.md`

## 📝 开发规范

### 命名规范

- **插件名**：`za-qe`（`za-{域}` 格式）
- **命令前缀**：`/za-qe:xxx`
- **Skill 命名**：`{功能域}-{类型后缀}`，通用名加 `qe-` 前缀避免冲突
- **SKILL.md frontmatter**：`status` 使用纯文本（`active`），不用 emoji

### 新增或更新 Skill 时需同步更新的文件

1. `skills/<skill-name>/SKILL.md`（含 YAML frontmatter：name、description、status）
2. `skills/<skill-name>/references/` 参考文档（编号前缀：`01-xxx.md`）
3. `skills/<skill-name>/examples/` 示例文件
4. `commands/<command-name>.md`（如需工作流命令，使用 `/za-qe:` 前缀）
5. `.claude-plugin/marketplace.json` 和 `plugins/za-qe/.claude-plugin/plugin.json`（版本号 + 描述）
6. `plugins/za-qe/README.md`、`commands/help.md`、`commands/status.md`
7. 项目根 `README.md` 和本 `CLAUDE.md`

**参考示例**：`case-designer` Skill（v1.3.0 完整实现）

### 关键规范

- Skill 引用 references 文档使用**无 `./` 前缀的相对路径**：`references/01-xxx.md`（不写 `./references/01-xxx.md`）
- **Skill 不得跨目录引用 `../../references/artifact-schemas/`**：Claude Code 对插件缓存的跨目录读取有额外安全确认，会中断工作流。需要 artifact-schema 的 Skill 应将对应文件**复制到自己的 `references/` 下**，两边保持同步更新
- 版本号遵循 SemVer：新增 Skill/Command → 次版本升级（`1.3.0 → 1.4.0`）
- 所有文档中 Skills 数量和版本号必须保持一致
- `plugin.json` 必须放在 `.claude-plugin/` 子目录下

### References 两级结构

- **插件级**：`plugins/za-qe/references/` — 公共参考文档（如 `artifact-schemas/`），为规范源头
- **Skill 级**：`plugins/za-qe/skills/<name>/references/` — Skill 专属参考文档（编号前缀 `01-xxx.md`）
- **同步规则**：在 `artifact-schemas/` 新建或更新规范文件后，必须同步复制到引用该规范的所有 Skill 的 `references/` 目录下

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
| artifact-schemas 总览 | `plugins/za-qe/references/artifact-schemas/00-overview.md` |
| req-parser Skill | `plugins/za-qe/skills/req-parser/SKILL.md` |
| api-generator 参考 | `plugins/za-qe/skills/api-generator/references/` |
| interface-extractor 参考 | `plugins/za-qe/skills/interface-extractor/references/` |
