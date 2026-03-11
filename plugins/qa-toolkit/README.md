# QA Toolkit - 银行测试自动化工具集

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/wf-bank-test)
[![Category](https://img.shields.io/badge/category-testing-green.svg)](https://github.com/your-org/wf-bank-test)

## 📋 概述

QA Toolkit 是一个完整的测试左移解决方案，提供从需求分析到用例生成的全流程自动化能力。通过三个核心 Skills 的协同工作，帮助测试团队在开发早期介入，提升测试效率和质量。

## 🎯 核心能力

### 1. shift-left-analyzer（测试左移分析器）

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

### 2. requirement-validator（需求验证器）

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

### 3. api-case-generator（API用例生成器）

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

### 示例 1: 完整测试左移流程

```bash
# 步骤 1: 分析开发方案
/shift-left-analyzer ./docs/za-zone-development.md

# 步骤 2: 验证需求实现（配置好文档目录后）
/requirement-validator

# 步骤 3: 生成 API 测试用例
/api-case-generator ./result/za_zone_测试左移分析报告.md
```

### 示例 2: 仅需求验证

```bash
# 直接调用需求验证器
/requirement-validator

# 按提示配置文档路径和检查重点
```

### 示例 3: 从网页提取并分析

```bash
# shift-left-analyzer 支持从网页提取内容
/shift-left-analyzer https://your-km-system.com/doc/12345
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

## 🔧 配置

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

每个 Skill 都有详细的配置文档：

- [shift-left-analyzer/SKILL.md](./skills/shift-left-analyzer/SKILL.md)
- [requirement-validator/SKILL.md](./skills/requirement-validator/SKILL.md)
- [api-case-generator/SKILL.md](./skills/api-case-generator/SKILL.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 作者

WF Bank Test Team

---

**快速链接**:
- [安装指南](#安装)
- [快速开始](#快速开始)
- [完整工作流](#完整工作流)
- [配置说明](#配置)
