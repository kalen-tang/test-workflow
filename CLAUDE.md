# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概述

基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案。核心是 `za-qe` 插件（`plugins/za-qe/`），包含六个核心 Skills 和六个工作流命令。

**完整文档**：`README.md`（架构、实施计划、团队信息）

## 🚀 常用命令

```bash
# 一键执行快速模式（最常用）
/za-qe:qe-quick ./docs/your-plan.md

# 手工案例生成（PlantUML流程图+MindMap）
/za-qe:manual-case ./docs/requirement.md

# 需求文档标准化（完整模式第一步）
/za-qe:req-parser ./docs/requirement.docx

# 查看工具状态
/za-qe:qe-status

# 查看帮助
/za-qe:qe-help
```

## 🏗️ 项目架构

### 插件系统两级配置

1. **项目级**：`.claude-plugin/marketplace.json` - 定义可用插件
2. **插件级**：`plugins/za-qe/.claude-plugin/plugin.json` - 插件元数据（当前 v1.3.0）

### 六个核心 Skills

所有 Skill 位于 `plugins/za-qe/skills/` 下：

| Skill | 状态 | 用途 |
|-------|------|------|
| `devplan-analyzer` | ✅ | 分析 KM 文档，生成测试左移分析报告（快速模式） |
| `doc-reviewer` | ✅ | 验证需求实现一致性 |
| `case-designer` | ✅ | 生成 PlantUML 流程图和测试用例 MindMap |
| `api-generator` | ✅ | 生成 Python pytest 测试代码和 YAML 数据 |
| `req-parser` | ✅ | 将原始需求文档转为标准化 YAML（完整模式第一阶段） |
| `design-parser` | ✅ | 检查开发方案文档是否符合规范，识别必须章节缺失和接口信息不完整（完整模式第一阶段） |

### 工作流模式

**快速模式**（`/za-qe:qe-quick ./docs/plan.md`）：
- `devplan-analyzer` → `api-generator`
- 输出：`./result/xxx_测试左移分析报告.md` + `./result/xxx/` 测试用例目录

**完整模式**（`/za-qe:full-workflow`，🚧 开发中）：四阶段流程
1. **规范化**：`req-parser` + `design-parser` + CML MCP + Code Diff MCP
2. **需求检查**：`doc-reviewer`
3. **手工案例**：`case-designer`
4. **自动化案例**：`api-generator`

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

### 新增或更新 Skill 时需同步更新的文件

1. `skills/<skill-name>/SKILL.md`（含 YAML frontmatter：name、description、status）
2. `skills/<skill-name>/references/` 参考文档（编号前缀：`01-xxx.md`）
3. `skills/<skill-name>/examples/` 示例文件
4. `commands/<command-name>.md`（如需工作流命令，使用 `/za-qe:` 前缀）
5. `.claude-plugin/marketplace.json` 和 `plugins/za-qe/.claude-plugin/plugin.json`（版本号 + 描述）
6. `plugins/za-qe/README.md`、`commands/help.md`、`commands/status.md`
7. 项目根 `README.md`（9个部分）和本 `CLAUDE.md`

**参考示例**：`case-designer` Skill（v1.3.0 完整实现）

### 关键规范

- Skill 引用 references 文档使用**无 `./` 前缀的相对路径**：`references/01-xxx.md`（不写 `./references/01-xxx.md`）
- 版本号遵循 SemVer：新增 Skill/Command → 次版本升级（`1.3.0 → 1.4.0`）
- 所有文档中 Skills 数量和版本号必须保持一致

### References 两级结构

- **插件级**：`plugins/za-qe/references/` — 公共参考文档（如 `artifact-schemas/`）
- **Skill 级**：`plugins/za-qe/skills/<name>/references/` — Skill 专属参考文档（编号前缀 `01-xxx.md`）

## 🔧 关键技术点

### 接口路径校验

- 微服务接口格式：`微服务域名/接口路径`，如 `zabank_imc_activity_service/activity/list`
- 路径包含 `dmb` → 判定为**网关接口**，必须提示用户替换为微服务接口
- 详细规则：`plugins/za-qe/skills/devplan-analyzer/references/01-interface-validation.md`

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
| 系统架构图 | `architecture.puml` |
| artifact-schemas 总览 | `plugins/za-qe/references/artifact-schemas/00-overview.md` |
| req-parser Skill | `plugins/za-qe/skills/req-parser/SKILL.md` |
| api-generator 参考 | `plugins/za-qe/skills/api-generator/references/` |
| devplan-analyzer 参考 | `plugins/za-qe/skills/devplan-analyzer/references/` |
