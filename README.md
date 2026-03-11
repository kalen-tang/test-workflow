# WF Bank Test - 银行测试自动化工具集

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-org/wf-bank-test)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)

## 📋 概述

基于 Claude Code 插件系统构建的完整测试自动化工具集，提供从需求分析到用例生成的全流程测试左移解决方案。

## 🎯 qa-toolkit 测试工具集

### shift-left-analyzer（测试左移分析器）
- 📄 分析 KM 开发方案文档
- 🔍 提取接口信息和依赖关系
- 📊 生成测试左移方案和用例建议
- **使用**: `/shift-left-analyzer ./docs/plan.md`

### requirement-validator（需求验证器）
- 📋 对比需求、设计、代码差异文档
- ✅ 验证需求实现完整性
- 📊 生成质量评分报告（A/B/C/D）
- **使用**: `/requirement-validator`

### api-case-generator（API用例生成器）
- 🎯 基于测试方案生成 API 测试用例
- 🧪 自动生成测试代码和数据
- 📝 支持多种测试框架
- **使用**: `/api-case-generator ./reports/analysis.md`

## 🚀 快速开始

```bash
# 1. 分析开发方案
/shift-left-analyzer ./docs/development-plan.md

# 2. 验证需求实现
/requirement-validator

# 3. 生成 API 测试用例
/api-case-generator ./result/test-analysis.md
```

## 📁 项目结构

```
wf_bank_test/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场配置
│
├── plugins/                      # 插件目录
│   └── qa-toolkit/               # 测试自动化工具集
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── shift-left-analyzer/
│       │   ├── requirement-validator/
│       │   └── api-case-generator/
│       └── README.md
│
├── result/                       # 输出结果
└── README.md                     # 本文档
```

## 🔄 完整工作流

```
┌─────────────────────────────────────────┐
│     QA Toolkit 测试左移工作流            │
└─────────────────────────────────────────┘

📄 KM 开发方案文档
        ↓
📊 shift-left-analyzer
        ↓
📋 测试左移分析报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 需求 + 设计 + 代码差异
        ↓
✅ requirement-validator
        ↓
📊 需求实现检查报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 测试左移分析报告
        ↓
🧪 api-case-generator
        ↓
🎯 API 测试用例集
```

## 🔧 插件配置

### 两级配置结构

#### 1. 项目级配置
`.claude-plugin/marketplace.json` - 定义所有可用插件

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "wf-bank-test",
  "plugins": [
    {
      "name": "qa-toolkit",
      "source": "./plugins/qa-toolkit",
      "category": "testing"
    }
  ]
}
```

#### 2. 插件级配置
`plugins/qa-toolkit/.claude-plugin/plugin.json` - 插件元数据

```json
{
  "name": "qa-toolkit",
  "description": "银行测试自动化工具集...",
  "version": "1.0.0",
  "author": {...}
}
```


## 🔌 推荐官方插件

如需扩展更多能力，推荐以下官方插件：

### 插件开发
- **plugin-dev** - 最全面的开发套件，包含 `agent-creator`、`skill-reviewer` 等工具
- **skill-creator** - Skill 专用创建和优化工具

### 代码质量
- **pr-review-toolkit** - PR 全面审查（6个专业 Agents）
- **code-simplifier** - 代码简化和重构

### 工作流
- **commit-commands** - 简化 Git 提交流程
- **feature-dev** - 功能开发全流程助手

**官方仓库**: [claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 📚 相关文档

- [qa-toolkit 使用指南](./plugins/qa-toolkit/README.md)
- [Claude Code 文档](https://claude.ai/code)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 团队

WF Bank Test Team

---

**版本**: v1.0.0 | **更新**: 2026-03-11 | **维护**: WF Bank Test Team
