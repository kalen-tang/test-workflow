# QA Toolkit - 银行测试自动化工具集

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/wf-bank-test)
[![Category](https://img.shields.io/badge/category-testing-green.svg)](https://github.com/your-org/wf-bank-test)

## 📋 概述

QA Toolkit 是一个完整的测试左移解决方案，提供从需求分析到用例生成的全流程自动化能力。通过三个核心 Skills 的协同工作，帮助测试团队在开发早期介入，提升测试效率和质量。

## 🎯 核心能力

### 🔧 辅助命令（Commands）

快速查询和配置工具集状态的便捷命令。

#### `/qa-status` - 查看工具状态

显示 qa-toolkit 工具集的当前状态和可用功能。

**功能**:
- 📋 列出所有可用 Skills
- ⚡ 显示当前工作模式（快速/完整）
- 📂 查看最近生成的输出文件
- 🔍 检查 Python 环境和依赖包

**使用方式**:
```bash
/qa-status
```

**输出示例**:
```
🔧 qa-toolkit 工具集状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 可用 Skills (3个):
  • /shift-left-analyzer - 测试左移分析器
  • /requirement-validator - 需求验证器
  • /api-case-generator - API用例生成器

⚡ 工作模式:
  • 快速模式: 2步到位（接口测试）
  • 完整模式: 4阶段流程（全面质量保证）

📂 最近输出 (./result/):
  • test-analysis.md (2026-03-13 17:30)
  • api-test-cases/ (2026-03-13 16:45)
  • quality-report.docx (2026-03-13 15:20)
```

---

#### `/qa-config` - 配置工具参数

管理 qa-toolkit 工具集的配置项，包括输出目录、工作模式、代码风格等。

**功能**:
- 📂 设置输出目录
- ⚡ 切换工作模式（quick/full）
- 📝 配置代码生成风格
- 🌍 管理测试环境列表
- 📊 调整日志级别

**使用方式**:
```bash
# 查看当前配置
/qa-config

# 设置输出目录
/qa-config output_dir ./test-output

# 切换到快速模式
/qa-config mode quick

# 设置测试环境
/qa-config environments sit,auto_qe,uat

# 配置代码风格
/qa-config code_style pep8

# 设置最大行长度
/qa-config max_line_length 180

# 设置日志级别
/qa-config log_level info
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
- 项目级: `.claude/qa-toolkit.local.md` (YAML frontmatter)
- 全局级: `~/.claude/qa-toolkit.config.yaml`

项目级配置优先级高于全局配置。

---

#### `/qa-help` - 显示帮助信息

显示 qa-toolkit 工具集的完整帮助信息和使用指南。

**功能**:
- 📚 显示所有 Skills 的详细说明
- 🔄 展示完整工作流程
- 💡 提供使用示例和最佳实践
- 📖 链接到详细文档

**使用方式**:
```bash
# 显示完整帮助
/qa-help

# 查看 Skills 详细说明
/qa-help skills

# 查看工作流程
/qa-help workflow

# 查看使用示例
/qa-help examples
```

**输出示例**:
```
🔧 qa-toolkit 测试自动化工具集
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 核心 Skills:
  1️⃣ /shift-left-analyzer <文档路径>
     分析 KM 开发方案，生成测试左移分析报告

  2️⃣ /requirement-validator
     验证需求实现完整性，生成质量评分报告

  3️⃣ /api-case-generator <报告路径>
     生成 API 测试用例代码和数据

🚀 推荐工作流:
  ⚡ 快速模式（接口测试）:
     /qa-quick ./docs/plan.md  ← 一键执行

  📊 完整模式（全面质量保证）:
     /qa-full ./project-root   ← 开发中

⚙️ 辅助命令:
  • /qa-status  - 查看工具状态
  • /qa-config  - 配置工具参数
  • /qa-help    - 显示帮助信息
```

---

#### `/qa-quick` - 快速模式工作流 ⭐ 推荐

**一键执行**快速模式测试左移流程，从 KM 开发方案直接生成 API 自动化测试用例。

**功能**:
- 🎯 自动串联两个核心 Skills
- 📊 自动检测中间输出文件
- ⚡ 无需手动复制路径
- 🚀 适合接口测试场景

**使用方式**:
```bash
# 从本地文档生成
/qa-quick ./docs/za-zone-development.md

# 从网页URL生成（需要Playwright MCP）
/qa-quick https://km.company.com/doc/12345

# 等价于手动执行：
# /shift-left-analyzer ./docs/za-zone-development.md
# /api-case-generator ./result/za_zone_测试左移分析报告.md
```

**执行流程**:
```
📄 KM 开发方案
    ↓
📊 shift-left-analyzer（步骤1）
    ↓ 自动检测输出路径
📋 测试左移分析报告
    ↓
🧪 api-case-generator（步骤2）
    ↓
🎯 API 自动化测试用例集
```

**优势对比**:

| 维度 | 手动执行 | /qa-quick |
|------|---------|-----------|
| 命令数 | 2条 | 1条 ✅ |
| 需要复制路径 | 是 | 否 ✅ |
| 容易出错 | 中 | 低 ✅ |
| 学习成本 | 中 | 低 ✅ |

---

#### `/qa-full` - 完整模式工作流 🚧

**一键执行**完整模式测试左移流程（四阶段），提供从需求规范化到自动化用例生成的全流程质量保证。

**当前状态**: 🚧 开发中（预计 2026-04-20 完成）

**功能**（开发完成后）:
- 📦 第一阶段：原始产出物规范化
- ✅ 第二阶段：需求实现检查
- 📝 第三阶段：手工案例生成
- 🧪 第四阶段：自动化案例生成

**预期使用方式**:
```bash
# 一键执行完整模式
/qa-full ./project-root

# 分阶段执行（推荐）
/qa-full --stage normalize    # 规范化
/qa-full --stage validate     # 需求检查
/qa-full --stage manual-cases # 手工案例
/qa-full --stage automation   # 自动化
```

**当前替代方案**:
```bash
# 手动执行第二阶段（需求检查）
/requirement-validator

# 或使用快速模式
/qa-quick ./docs/plan.md
```

**开发进度**:
- ✅ 第二阶段：requirement-validator（已完成）
- ✅ 第四阶段：api-case-generator（已完成）
- 🚧 第一阶段：规范化工具（开发中）
- 🚧 第三阶段：手工案例生成（开发中）

详见：[完整模式文档](./commands/full-workflow.md)

---

### 🔬 核心 Skills

#### 1. shift-left-analyzer（测试左移分析器）

**用途**: 分析开发方案(KM)文档，生成测试左移方案

**功能**:
- 📄 解析 KM 开发方案文档结构
- 🔍 提取关键接口信息和依赖关系
- 📊 生成单接口测试用例建议
- 🔗 自动识别业务流程场景用例
- ⚠️ 标注测试重点和风险点

**使用方式**:
```bash
/shift-left-analyzer ./docs/development-plan.md
```

**输出**: 测试左移分析报告（Markdown 格式）

---

#### 2. requirement-validator（需求验证器）

**用途**: 验证需求实现一致性，生成检查报告

**功能**:
- 📋 对比需求文档、设计文档、代码差异
- ✅ 验证需求实现完整性
- 📊 生成文档质量评分（A/B/C/D）
- 🎯 提供针对性测试建议
- ⚠️ 识别测试风险点和解决措施

**使用方式**:
```bash
/requirement-validator
```

**配置**: 在技能内配置文档目录
- 需求文档目录: `./requirement_word`
- 设计文档目录: `./design_word`
- 代码差异目录: （根据需要配置）

**输出**: 需求实现检查报告（Word 格式）

---

#### 3. api-case-generator（API用例生成器）

**用途**: 基于测试方案生成 API 测试用例

**功能**:
- 🎯 从测试左移方案提取接口测试点
- 🧪 自动生成接口测试用例代码
- 📝 生成测试数据和断言规则
- 🔧 支持多种测试框架
- 📊 生成测试覆盖率报告

**使用方式**:
```bash
/api-case-generator ./reports/shift-left-analysis.md
```

**输出**: API 测试用例集和执行脚本

## 🔄 完整工作流

```
                    QA Toolkit 测试左移工作流

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1️⃣  开发方案文档 (KM)                                   │
│      ↓                                                  │
│  📊 shift-left-analyzer                                 │
│      ↓                                                  │
│  📄 测试左移分析报告                                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  2️⃣  需求文档 + 设计文档 + 代码差异                        │
│      ↓                                                  │
│  ✅ requirement-validator                               │
│      ↓                                                  │
│  📋 需求实现检查报告                                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  3️⃣  测试左移分析报告                                     │
│      ↓                                                  │
│  🧪 api-case-generator                                  │
│      ↓                                                  │
│  🎯 API 测试用例集                                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📦 安装

### 前提条件

- Claude Code CLI 已安装
- Python 3.14+ (用于某些脚本)
- 可选: Playwright MCP (用于网页内容提取)

### 安装步骤

```bash
# 1. 克隆或复制 qa-toolkit 到你的项目
cp -r path/to/qa-toolkit ./plugins/

# 2. 在 .claude-plugin/marketplace.json 中添加配置
{
  "plugins": [
    {
      "name": "qa-toolkit",
      "source": "./plugins/qa-toolkit",
      "category": "testing"
    }
  ]
}

# 3. 重新加载 Claude Code
claude-code reload
```

## 🚀 快速开始

### ⚡ 最快上手方式（推荐）

```bash
# 一条命令完成快速模式测试左移
/qa-quick ./docs/your-plan.md
```

就是这么简单！`/qa-quick` 会自动：
1. 分析 KM 开发方案
2. 生成测试左移分析报告
3. 生成 API 自动化测试用例
4. 显示生成结果和下一步操作

---

### 首次使用推荐流程

```bash
# 步骤 1: 查看帮助信息
/qa-help

# 步骤 2: 查看工具状态
/qa-status

# 步骤 3: 一键执行快速模式
/qa-quick ./docs/your-plan.md

# 步骤 4: 查看生成结果
/qa-status
```

---

### 示例 1: 快速模式（推荐）✅

**一条命令搞定**：

```bash
# 方式1: 从本地文档
/qa-quick ./docs/za-zone-development.md

# 方式2: 从网页URL
/qa-quick https://km.company.com/doc/12345
```

**等价于手动执行**：

```bash
# 步骤 1: 分析开发方案
/shift-left-analyzer ./docs/za-zone-development.md

# 步骤 2: 生成 API 测试用例
/api-case-generator ./result/za_zone_测试左移分析报告.md
```

---

### 示例 2: 仅需求验证

### 示例 2: 仅需求验证

```bash
# 准备文档目录
mkdir -p ./requirement_word ./design_word

# 将文档放入对应目录
cp 需求文档*.docx ./requirement_word/
cp 设计文档*.docx ./design_word/

# 执行需求验证
/requirement-validator
```

---

### 示例 3: 完整模式（开发中）🚧

```bash
# 一键执行完整模式（预计 2026-04-20 可用）
/qa-full ./project-root

# 当前替代方案：手动组合
/requirement-validator              # 需求检查
/qa-quick ./docs/plan.md            # 快速生成接口测试
```

## 📊 输出示例

### 测试左移分析报告

```markdown
# 测试左移分析报告

## 一、接口测试用例

### 1.1 单接口测试用例
- 接口名称: createUser
- 测试场景: 正常创建、参数校验、权限检查
- 优先级: P0
...

## 二、场景测试用例

### 2.1 用户注册流程
1. 验证手机号 → 2. 发送验证码 → 3. 创建账户
...
```

### 需求实现检查报告

```
# 需求实现检查报告

## 文档质量评分
- 需求文档: A (95分)
- 设计文档: B (82分)
- 代码差异: B (85分)

## 需求对齐度分析
- 已实现: 28/30 (93.3%)
- 部分实现: 2/30 (6.7%)
- 未实现: 0/30 (0%)
...
```

## 🎯 适用场景

### 适合使用 QA Toolkit 的场景

✅ 新功能开发，需要测试左移
✅ 需求变更，需要验证实现一致性
✅ API 接口开发，需要快速生成测试用例
✅ 测试团队早期介入开发过程
✅ 需要自动化生成测试文档

### 不适合的场景

❌ 纯前端 UI 测试（建议使用其他工具）
❌ 性能测试（需要专门的性能测试工具）
❌ 安全渗透测试（需要安全测试工具）

## 🔧 高级配置

### 使用 /qa-config 命令配置

推荐使用 `/qa-config` 命令进行配置管理，无需手动编辑文件：

```bash
# 配置输出目录
/qa-config output_dir ./custom-output

# 切换工作模式
/qa-config mode full

# 配置测试环境
/qa-config environments sit,uat,prod

# 设置代码风格
/qa-config code_style google

# 调整日志级别
/qa-config log_level debug
```

查看所有配置项详情：
```bash
/qa-help
```

### Playwright MCP（可选）

shift-left-analyzer 支持从网页提取内容，需要安装 Playwright MCP：

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

### 文档目录配置

requirement-validator 需要配置文档目录，可以在 SKILL.md 中修改默认配置：

```yaml
文档目录配置:
- 需求文档目录: `./requirement_word`
- 设计文档目录: `./design_word`
```

## 📚 详细文档

### 命令文档

**辅助命令**：
- [/qa-status 命令文档](./commands/status.md) - 查看工具状态
- [/qa-config 命令文档](./commands/config.md) - 配置工具参数
- [/qa-help 命令文档](./commands/help.md) - 显示帮助信息

**工作流命令**：
- [/qa-quick 命令文档](./commands/quick-workflow.md) - 快速模式工作流 ⭐ 推荐
- [/qa-full 命令文档](./commands/full-workflow.md) - 完整模式工作流 🚧 开发中

### Skills 文档

每个 Skill 都有详细的配置文档：

- [shift-left-analyzer/SKILL.md](./skills/shift-left-analyzer/SKILL.md)
  - [references/](./skills/shift-left-analyzer/references/) - 详细参考文档（4个文件）
  - [examples/](./skills/shift-left-analyzer/examples/) - 使用示例
- [requirement-validator/SKILL.md](./skills/requirement-validator/SKILL.md)
- [api-case-generator/SKILL.md](./skills/api-case-generator/SKILL.md)
  - [references/](./skills/api-case-generator/references/) - 详细参考文档（6个文件）
  - [examples/](./skills/api-case-generator/examples/) - 使用示例

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 作者

WF Bank Test Team

---

**快速链接**:
- [⚡ 最快上手](#最快上手方式推荐) - `/qa-quick` 一键执行
- [🔧 辅助命令](#辅助命令commands) - `/qa-status`, `/qa-config`, `/qa-help`
- [🔬 核心 Skills](#核心-skills) - 测试左移分析、需求验证、用例生成
- [🚀 快速开始](#快速开始) - 使用示例和推荐流程
- [📦 安装指南](#安装)
- [🔄 完整工作流](#完整工作流)
- [⚙️ 高级配置](#高级配置) - 使用 `/qa-config` 命令
- [📚 详细文档](#详细文档) - Commands 和 Skills 文档
