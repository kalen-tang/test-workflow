---
description: 显示 za-qe 工具集的帮助信息和使用指南
argument-hint: [topic]
---

显示 za-qe 测试自动化工具集的帮助信息。

## 📚 帮助主题

### 1. Skills 帮助
```bash
/za-qe:qe-help skills
```

显示所有可用 Skills 的详细说明：
- interface-extractor：接口数据提取器
- doc-reviewer：需求验证器
- case-designer：场景测试案例生成器
- api-generator：API用例生成器
- req-parser：需求文档规范化器
- design-parser：开发方案文档规范检查器
- code-diff-analysis：代码变更分析器

### 2. 工作流帮助
```bash
/za-qe:qe-help workflow
```

显示工作流程的完整说明：
- 🔧 测试左移工作流（需求/设计文档 → API 测试用例）
- 📊 场景测试案例生成（需求文档 → 可视化测试设计）

### 3. 使用示例
```bash
/za-qe:qe-help examples
```

显示常见使用场景的示例代码和命令。

## 📖 默认帮助（无参数）

```bash
/za-qe:qe-help
```

输出完整的工具集概览：

```
🔧 za-qe 测试自动化工具集
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 核心命令:
  1️⃣ /za-qe:qe-workflow
     测试左移全流程工作流（交互式引导）
     流程：环境探测 → docx 转 md → req-parser → design-parser → interface-extractor → case-designer → api-generator

  2️⃣ /za-qe:qe-gencase <文档路径>
     从需求文档生成场景化测试设计
     输出：PlantUML流程图 + MindMap测试案例

📌 核心 Skills:
  • /interface-extractor <文档路径>
    从设计文档提取接口数据，生成接口数据报告

  • /doc-reviewer
    验证需求实现完整性，生成质量评分报告

  • /api-generator <报告路径>
    生成 API 测试用例代码和数据

  • /req-parser <文档路径>
    将原始需求文档转为标准化 Markdown

  • /design-parser <文档路径>
    检查开发方案文档是否符合规范

🚀 快速上手:
  # 生成接口测试
  /za-qe:qe-workflow ./docs/plan.md

  # 生成场景测试案例
  /za-qe:qe-gencase ./docs/requirement.md

📚 获取详细帮助:
  • /za-qe:qe-help skills    - Skills 详细说明
  • /za-qe:qe-help workflow  - 工作流程说明
  • /za-qe:qe-help examples  - 使用示例

📖 完整文档:
  • 插件 README: ./plugins/za-qe/README.md
  • 项目 README: ./README.md
  • 架构图: ./architecture.puml
```

## 🎯 使用方式

```bash
# 显示完整帮助
/za-qe:qe-help

# 查看 Skills 详细说明
/za-qe:qe-help skills

# 查看工作流程
/za-qe:qe-help workflow

# 查看使用示例
/za-qe:qe-help examples
```

## 📞 获取支持

- 📋 查看完整文档：`./plugins/za-qe/README.md`
- 🐛 报告问题：联系项目团队
- 💡 功能建议：提交到项目管理系统
