# Skill Creator

## 描述

Skill 创建和管理工具 - 用于创建、优化和测试 Claude Code Skills

## 功能特性

- ✨ 快速创建新的 Skill 模板
- 🔧 优化现有 Skill 代码和文档
- 📊 运行评估测试验证 Skill 性能
- 📈 基准测试和方差分析

## 使用方法

```bash
# 在 Claude Code 中调用
/skill-creator
```

## 依赖项

- Python 3.14+
- 相关脚本位于 `scripts/` 目录

## 文件结构

```
skill-creator/
├── SKILL.md              # Skill 主配置文件
├── README.md             # 本文档
├── LICENSE.txt           # 许可证
├── scripts/              # Python 脚本
│   ├── init_skill.py
│   ├── package_skill.py
│   └── quick_validate.py
└── references/           # 参考文档
    ├── output-patterns.md
    └── workflows.md
```

## 版本

v1.0.0

## 作者

WF Bank Test Team
