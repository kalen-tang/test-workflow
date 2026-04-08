# ZA Bank Test Team - 银行测试自动化工具集 用户手册

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://gitlab.in.za/dingzhong.hu/qe-toolkit)
[![Category](https://img.shields.io/badge/category-testing-green.svg)](https://gitlab.in.za/dingzhong.hu/qe-toolkit)

## 📋 概述

QA Toolkit 是一个完整的测试左移解决方案，提供从需求分析到用例生成的全流程自动化能力。通过**六个核心 Skills** 和**六个工作流命令**的协同工作，帮助测试团队在开发早期介入，提升测试效率和质量。

> 项目架构、实施计划、团队信息见 [项目主文档](../../README.md)

---

## 🚀 快速开始

### 最快上手

```bash
/qe-quick ./docs/your-plan.md
```

自动完成：分析 KM 开发方案 → 生成测试左移分析报告 → 生成 API 自动化测试用例

### 首次使用推荐流程

```bash
# 1. 查看帮助信息
/qe-help

# 2. 查看工具状态
/qe-status

# 3. 一键执行快速模式
/qe-quick ./docs/your-plan.md

# 4. 查看生成结果
/qe-status
```

---

## ⚡ 工作流命令

### `/qe-quick` - 快速模式工作流 ⭐ 推荐

**一键执行**快速模式测试左移流程，从 KM 开发方案直接生成 API 自动化测试用例。

```bash
# 从本地文档生成
/qe-quick ./docs/za-zone-development.md

# 从网页URL生成（需要Playwright MCP）
/qe-quick https://km.company.com/doc/12345
```

**执行流程**：
```
📄 KM 开发方案
    ↓
📊 devplan-analyzer（步骤1）
    ↓ 自动检测输出路径
📋 测试左移分析报告
    ↓
🧪 api-generator（步骤2）
    ↓
🎯 API 自动化测试用例集
```

**优势对比**：

| 维度 | 手动执行 | /qe-quick |
|------|---------|-----------|
| 命令数 | 2条 | 1条 |
| 需要复制路径 | 是 | 否 |
| 容易出错 | 中 | 低 |

---

### `/qe-manual` - 手工测试案例生成

从需求文档生成可视化的手工测试设计（PlantUML流程图 + MindMap）。

```bash
# 从单个文档生成
/qe-manual ./docs/requirement.md

# 从多个文档生成（自动合并）
/qe-manual ./docs/req1.md ./docs/req2.docx ./docs/req3.txt

# 指定输出目录
/qe-manual ./docs/requirement.md --output ./review
```

**输出**：手工测试案例文档（Markdown格式，包含PlantUML代码）

---

### `/qe-full` - 完整模式工作流 🚧

**一键执行**完整模式测试左移流程（四阶段），提供从需求规范化到自动化用例生成的全流程质量保证。

**当前状态**: 🚧 开发中（预计 2026-04-20 完成）

```bash
# 一键执行完整模式
/qe-full ./project-root

# 分阶段执行
/qe-full --stage normalize    # 规范化
/qe-full --stage validate     # 需求检查
/qe-full --stage manual-cases # 手工案例
/qe-full --stage automation   # 自动化
```

**当前替代方案**：
```bash
/doc-reviewer              # 需求检查
/qe-manual ./docs/requirement.md    # 手工案例
/qe-quick ./docs/plan.md            # API 自动化
```

> 完整模式四阶段设计详见 [项目主文档](../../README.md#-完整模式四阶段设计)

---

### `/qe-status` - 查看工具状态

显示 qe-toolkit 工具集的当前状态和可用功能。

```bash
/qe-status
```

**输出示例**:
```
🔧 qe-toolkit 工具集状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 可用 Skills (6个):
  • /devplan-analyzer - 测试左移分析器
  • /doc-reviewer - 需求验证器
  • /qe-manual - 手工测试案例生成器
  • /api-generator - API用例生成器
  • /req-parser - 需求文档规范化器
  • /design-parser - 设计文档规范化器 🚧

⚡ 工作模式:
  • 快速模式: 2步到位（接口测试）
  • 完整模式: 4阶段流程（全面质量保证）

📂 最近输出 (./result/):
  • test-analysis.md
  • api-test-cases/
```

---

### `/qe-config` - 配置工具参数

管理 qe-toolkit 工具集的配置项。

```bash
# 查看当前配置
/qe-config

# 设置输出目录
/qe-config output_dir ./test-output

# 切换工作模式
/qe-config mode quick

# 设置测试环境
/qe-config environments sit,auto_qe,uat

# 配置代码风格
/qe-config code_style pep8

# 设置最大行长度
/qe-config max_line_length 180

# 设置日志级别
/qe-config log_level info
```

**可配置项**:

| 配置项 | 说明 | 默认值 | 示例值 |
|--------|------|--------|--------|
| `output_dir` | 输出目录 | `./result/` | `./test-output` |
| `mode` | 工作模式 | `quick` | `quick`/`full` |
| `code_style` | 代码风格 | `pep8` | `pep8`/`google`/`numpy` |
| `max_line_length` | 最大行长度 | `180` | `80`/`120`/`180` |
| `environments` | 测试环境列表 | `sit,auto_qe,uat` | 逗号分隔 |
| `log_level` | 日志级别 | `info` | `debug`/`info`/`warning`/`error` |

**配置存储**:
- 项目级: `.claude/qe-toolkit.local.md`（YAML frontmatter）
- 全局级: `~/.claude/qe-toolkit.config.yaml`
- 项目级配置优先级高于全局配置

---

### `/qe-help` - 显示帮助信息

显示 qe-toolkit 工具集的完整帮助信息。

```bash
# 显示完整帮助
/qe-help

# 查看 Skills 详细说明
/qe-help skills

# 查看工作流程
/qe-help workflow

# 查看使用示例
/qe-help examples
```

---

## 🔬 核心 Skills

### 1. devplan-analyzer（测试左移分析器）

分析开发方案(KM)文档，生成测试左移分析报告。

- 解析 KM 开发方案文档结构
- 提取关键接口信息和依赖关系
- 生成单接口测试用例建议
- 自动识别业务流程场景用例
- 标注测试重点和风险点

```bash
/devplan-analyzer ./docs/development-plan.md
```

**输出**: 测试左移分析报告（Markdown 格式），保存到 `./result/`

---

### 2. doc-reviewer（需求验证器）

验证需求实现一致性，生成检查报告。

- 对比需求文档、设计文档、代码差异
- 验证需求实现完整性
- 生成文档质量评分（A/B/C/D）
- 提供针对性测试建议
- 识别测试风险点和解决措施

```bash
/doc-reviewer
```

**配置**：在技能内配置文档目录
- 需求文档目录: `./requirement_word`
- 设计文档目录: `./design_word`

**输出**: 需求实现检查报告（Word 格式）

---

### 3. case-designer（手工案例生成器）

从需求文档生成可视化的手工测试设计。

- 解析需求文档（支持 Markdown、Word、PDF、纯文本）
- 生成业务流程图（PlantUML Activity Diagram）
- 生成测试功能点（PlantUML MindMap，三层）
- 生成详细测试案例（PlantUML MindMap，四层）
- 应用命名规范（去掉"测试"后缀、动作与结果分离）

```bash
/qe-manual ./docs/requirement.md
```

**输出**: 手工测试案例文档（Markdown格式，包含PlantUML代码）

---

### 4. api-generator（API用例生成器）

基于测试方案生成 API 测试用例。

- 从测试左移方案提取接口测试点
- 自动生成 Python pytest 测试代码
- 生成多环境测试数据（YAML，支持 sit/auto_qe/uat）
- 生成执行脚本

```bash
/api-generator ./result/xxx_测试左移分析报告.md
```

**输出**: API 测试用例集（Python 代码 + YAML 数据），保存到 `./result/` 子目录

---

### 5. req-parser（需求文档规范化器）✅

将原始需求文档转为标准化 YAML 格式，是完整模式第一阶段的核心组件。

- 解析原始需求文档（Word/Markdown/PDF）
- 提取业务场景、功能需求、验收标准
- 生成标准化 YAML 输出（遵循 [normalized-requirement v2.0](./references/artifact-schemas/01-normalized-requirement-v2.md) 格式）
- 支持 ZA Bank PRD 模板

```bash
/req-parser ./docs/requirement.docx
```

**输出**: 标准化需求文档（YAML 格式）

---

### 6. design-parser（设计文档规范化器）🚧

将原始设计文档转为标准化 YAML 格式，是完整模式第一阶段的核心组件。

- 解析原始设计文档
- 提取接口设计、数据库设计、系统交互
- 生成标准化 YAML 输出（遵循 [normalized-design v1.0](./references/artifact-schemas/02-normalized-design.md) 格式）

**当前状态**: 🚧 开发中

```bash
/design-parser ./docs/design.docx
```

---

## 📦 Artifact Schemas

完整模式各 Skill 之间通过标准化 YAML 格式通信。每个 Skill 的输入输出格式都有严格定义，确保组件间无缝协作。

> 详细规范见 [Artifact Schemas 总览](./references/artifact-schemas/00-overview.md)

### Skill 输入输出映射

| Skill | 输入格式 | 输出格式 |
|-------|---------|---------|
| req-parser | 原始需求文档 | 01-normalized-requirement |
| design-parser | 原始设计文档 | 02-normalized-design |
| doc-reviewer | 01 + 02 + 04 | 05-validation-report |
| case-designer | 01 + 02 + 03 + 04 | 06-manual-test-cases |
| api-generator | 06 + 01~04 | 07-api-test-cases |

---

## 🎯 适用场景

### 适合

- 新功能开发，需要测试左移
- 需求变更，需要验证实现一致性
- API 接口开发，需要快速生成测试用例
- 测试团队早期介入开发过程
- 需要自动化生成测试文档

### 不适合

- 纯前端 UI 测试（建议使用其他工具）
- 性能测试（需要专门的性能测试工具）
- 安全渗透测试（需要安全测试工具）

---

## 🔧 高级配置

### Playwright MCP（可选）

devplan-analyzer 支持从网页提取内容，需要安装 Playwright MCP：

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

### 文档目录配置

doc-reviewer 需要配置文档目录，可以在 SKILL.md 中修改默认配置：

```yaml
文档目录配置:
- 需求文档目录: `./requirement_word`
- 设计文档目录: `./design_word`
```

---

## 📚 详细文档

### 命令文档

| 命令 | 文档 | 说明 |
|------|------|------|
| `/qe-quick` ⭐ | [quick-workflow.md](./commands/quick-workflow.md) | 快速模式工作流 |
| `/qe-manual` | [manual-case.md](./commands/manual-case.md) | 手工测试案例生成 |
| `/qe-full` 🚧 | [full-workflow.md](./commands/full-workflow.md) | 完整模式工作流 |
| `/qe-status` | [status.md](./commands/status.md) | 查看工具状态 |
| `/qe-config` | [config.md](./commands/config.md) | 配置工具参数 |
| `/qe-help` | [help.md](./commands/help.md) | 显示帮助信息 |

### Skills 文档

| Skill | 文档 | 参考文档 |
|-------|------|---------|
| devplan-analyzer | [SKILL.md](./skills/devplan-analyzer/SKILL.md) | [references/](./skills/devplan-analyzer/references/) (4个), [examples/](./skills/devplan-analyzer/examples/) |
| doc-reviewer | [SKILL.md](./skills/doc-reviewer/SKILL.md) | - |
| case-designer | [SKILL.md](./skills/case-designer/SKILL.md) | [references/](./skills/case-designer/references/) (4个), [examples/](./skills/case-designer/examples/) (5个) |
| api-generator | [SKILL.md](./skills/api-generator/SKILL.md) | [references/](./skills/api-generator/references/) (6个), [examples/](./skills/api-generator/examples/) |
| req-parser | [SKILL.md](./skills/req-parser/SKILL.md) | [references/](./skills/req-parser/references/), [examples/](./skills/req-parser/examples/) |
| design-parser | [SKILL.md](./skills/design-parser/SKILL.md) | [references/](./skills/design-parser/references/) |

### Artifact Schemas 文档

| 编号 | 文档 |
|------|------|
| 00 | [总览](./references/artifact-schemas/00-overview.md) |
| 01 | [normalized-requirement v2.0](./references/artifact-schemas/01-normalized-requirement-v2.md) |
| 02 | [normalized-design](./references/artifact-schemas/02-normalized-design.md) |
| 03 | [normalized-cases](./references/artifact-schemas/03-normalized-cases.md) |
| 04 | [code-diff-report](./references/artifact-schemas/04-code-diff-report.md) |
| 05 | [validation-report](./references/artifact-schemas/05-validation-report.md) |
| 06 | [manual-test-cases](./references/artifact-schemas/06-manual-test-cases.md) |
| 07 | [api-test-cases](./references/artifact-schemas/07-api-test-cases.md) |

---

**版本**: v1.2.0 | [项目主文档](../../README.md) | ZA Bank Test Team
