# API Generator

## 描述

接口用例生成器 - 基于测试左移方案自动生成 API 测试用例

## 功能特性

- 🎯 从测试左移方案提取接口测试点
- 🧪 自动生成接口测试用例
- 📝 支持多种测试框架格式
- 🔧 可配置的用例模板

## 使用方法

```bash
# 在 Claude Code 中调用
/api-generator <shift-left-analysis-report>
```

## 输入

- 测试左移分析报告

## 输出

- API 测试用例集
- 测试数据模板
- 断言规则

## 文件结构

```
api-generator/
├── SKILL.md              # Skill 主配置文件
├── README.md             # 本文档
└── README_SKILL.md       # Skill 详细说明
```

## 版本

v1.0.0

## 作者

WF Bank Test Team
