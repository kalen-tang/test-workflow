# MCP Builder

## 描述

MCP 服务器构建工具 - 快速搭建和部署 Model Context Protocol 服务器

## 功能特性

- 🚀 快速初始化 MCP 服务器项目
- 🐍 支持 Python 和 Node.js
- 📚 内置最佳实践和示例
- ✅ 自动化评估和测试

## 使用方法

```bash
# 在 Claude Code 中调用
/mcp-builder
```

## 依赖项

- Python 3.14+ 或 Node.js 18+
- 相关依赖见 `scripts/requirements.txt`

## 文件结构

```
mcp-builder/
├── SKILL.md              # Skill 主配置文件
├── README.md             # 本文档
├── LICENSE.txt           # 许可证
├── scripts/              # 构建脚本
│   ├── connections.py
│   ├── evaluation.py
│   ├── example_evaluation.xml
│   └── requirements.txt
└── reference/            # 参考文档
    ├── evaluation.md
    ├── mcp_best_practices.md
    ├── node_mcp_server.md
    └── python_mcp_server.md
```

## 版本

v1.0.0

## 作者

WF Bank Test Team
