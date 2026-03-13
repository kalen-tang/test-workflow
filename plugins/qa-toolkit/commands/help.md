---
name: qa-help
description: 显示 qa-toolkit 工具集的帮助信息和使用指南
arguments:
  - name: topic
    description: 帮助主题（可选：skills/workflow/examples）
    required: false
---

显示 qa-toolkit 测试自动化工具集的帮助信息。

## 📚 帮助主题

### 1. Skills 帮助
```bash
/qa-help skills
```

显示所有可用 Skills 的详细说明：
- shift-left-analyzer：测试左移分析器
- requirement-validator：需求验证器
- api-case-generator：API用例生成器

### 2. 工作流帮助
```bash
/qa-help workflow
```

显示两种工作模式的完整流程：
- ⚡ 快速模式（2步到位）
- 📊 完整模式（4阶段流程）

### 3. 使用示例
```bash
/qa-help examples
```

显示常见使用场景的示例代码和命令。

## 📖 默认帮助（无参数）

```bash
/qa-help
```

输出完整的工具集概览：

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
     /shift-left-analyzer ./docs/plan.md
     /api-case-generator ./result/test-analysis.md

  📊 完整模式（全面质量保证）:
     [规范化] → /requirement-validator →
     [手工案例] → /api-case-generator

⚙️ 辅助命令:
  • /qa-status  - 查看工具状态
  • /qa-config  - 配置工具参数
  • /qa-help    - 显示帮助信息

📚 获取详细帮助:
  • /qa-help skills    - Skills 详细说明
  • /qa-help workflow  - 工作流程说明
  • /qa-help examples  - 使用示例

📖 完整文档:
  • 插件 README: ./plugins/qa-toolkit/README.md
  • 项目 README: ./README.md
  • 架构图: ./architecture.puml
```

## 🎯 快速上手

**首次使用建议**：

1. 检查状态：`/qa-status`
2. 查看帮助：`/qa-help workflow`
3. 配置工具：`/qa-config mode quick`
4. 开始使用：`/shift-left-analyzer ./docs/your-plan.md`

## 📞 获取支持

- 📋 查看完整文档：`./plugins/qa-toolkit/README.md`
- 🐛 报告问题：联系项目团队
- 💡 功能建议：提交到项目管理系统

## 🎯 使用方式

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
