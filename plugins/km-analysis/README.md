# KM Analysis

## 描述

开发方案分析工具 - 分析 KM 文档并生成测试左移方案，识别潜在风险和测试点

## 功能特性

- 📄 解析 KM（Knowledge Management）文档
- 🔍 自动识别测试场景和风险点
- 📊 生成测试左移分析报告
- ⚠️ 风险评估和优先级排序

## 使用方法

```bash
# 在 Claude Code 中调用
/km-analysis <km-document-path>
```

## 输入

- KM 开发方案文档（Markdown 或其他格式）

## 输出

- 测试左移分析报告
- 风险矩阵
- 测试建议

## 文件结构

```
km-analysis/
├── SKILL.md              # Skill 主配置文件
└── README.md             # 本文档
```

## 版本

v1.0.0

## 作者

WF Bank Test Team
