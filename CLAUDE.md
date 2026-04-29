# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概述

基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案。核心是 `za-qe` 插件（`plugins/za-qe/`），包含八个核心 Skills 和六个工作流命令。

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
2. **插件级**：`plugins/za-qe/.claude-plugin/plugin.json` — 插件元数据（当前 v2.5.7），声明 `commands`/`skills` 路径

### 核心与可选插件

| 插件 | 类型 | 用途 |
|------|------|------|
| `za-qe` | core | 测试左移工具集：需求分析、场景案例、API用例生成 |
| `za-qe-tools` | optional | 通用工具集：状态栏 + 系统通知 + 命令审批(Dippy) + 事件流查看(ESP) |
| `za-ui` | optional | UI自动化测试：Playwright转换、修复、增量更新 |

所有 Skill 位于 `plugins/za-qe/skills/` 下：

| Skill | 状态 | 用途 |
|-------|------|------|
| `req-parser` | ✅ | 将原始需求文档转为标准化 Markdown |
| `design-parser` | ✅ | 检查开发方案文档是否符合规范 |
| `doc-converter` | ✅ | 将 docx/doc 文档批量转换为 UTF-8 Markdown |
| `interface-extractor` | ✅ | 从设计文档提取接口数据，生成接口数据报告 |
| `case-designer` | ✅ | 生成 PlantUML 流程图、测试用例 MindMap 和场景案例表 |
| `api-generator` | ✅ | 生成 Python pytest 测试代码和 YAML 数据 |
| `doc-reviewer` | ✅ | 验证需求实现一致性 |
| `code-diff-analysis` | ✅ | 分析需求代码变更，识别质量风险，输出测试策略 |

### 工作流模式

**全流程模式**（`/za-qe:qe-workflow`，✅ 推荐）：
- 阶段 1：环境探测 + 交互式目录配置（需求文档/设计文档/输出/自动化项目）
- 阶段 2：`uvx markitdown` docx/doc → md + UTF-8 编码修复
- 阶段 3：`req-parser` → `design-parser` → `interface-extractor` → `case-designer` → `api-generator`
- 输出：规范化文档 + 测试左移分析报告 + API 自动化测试用例

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

- Skill 引用 references 文档使用**无 `./` 前缀的相对路径**：`references/xxx.md`（不写 `./references/xxx.md`）
- 版本号遵循 SemVer：新增 Skill/Command → 次版本升级（`1.3.0 → 1.4.0`）
- 所有文档中 Skills 数量和版本号必须保持一致
- `plugin.json` 必须放在 `.claude-plugin/` 子目录下

### References 结构

- 参考文档统一放在 `plugins/za-qe/skills/<name>/references/` 下（Skill 专属）
- 无插件级 references 目录（已移除 `plugins/za-qe/references/`）
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
| req-parser Skill | `plugins/za-qe/skills/req-parser/SKILL.md` |
| PRD 模板 | `plugins/za-qe/skills/req-parser/references/prd-template.md` |
| api-generator 参考 | `plugins/za-qe/skills/api-generator/references/` |
| interface-extractor 参考 | `plugins/za-qe/skills/interface-extractor/references/` |
