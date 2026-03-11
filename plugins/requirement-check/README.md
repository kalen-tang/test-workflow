# Requirement Check

## 描述

需求实现检查工具 - 对比需求文档、设计文档和代码差异，生成需求实现检查报告

## 功能特性

- 📋 解析需求文档和设计文档
- 🔄 对比代码变更和需求说明
- ✅ 验证需求实现完整性
- 📊 生成详细的检查报告

## 使用方法

```bash
# 在 Claude Code 中调用
/requirement-check <requirement-doc> <design-doc> <code-diff>
```

## 输入

- 需求文档
- 设计文档
- 代码差异分析文档

## 输出

- 需求实现检查报告
- 覆盖率分析
- 遗漏需求列表

## 文件结构

```
requirement-check/
├── SKILL.md              # Skill 主配置文件
└── README.md             # 本文档
```

## 版本

v1.0.0

## 作者

WF Bank Test Team
