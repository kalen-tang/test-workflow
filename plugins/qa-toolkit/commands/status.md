---
name: qa-status
description: 查看 qa-toolkit 工具集当前状态和可用功能
---

显示 qa-toolkit 测试自动化工具集的当前状态信息：

## 📊 执行内容

1. **列出所有可用 Skills**
   - shift-left-analyzer（测试左移分析器）
   - requirement-validator（需求验证器）
   - api-case-generator（API用例生成器）

2. **检查工作模式**
   - ⚡ 快速模式：shift-left-analyzer → api-case-generator
   - 📊 完整模式：规范化 → requirement-validator → 手工案例 → api-case-generator

3. **显示最近的输出目录**
   - 检查 `./result/` 目录下的最新生成文件
   - 列出最近 5 个生成的报告

4. **环境检查**
   - Python 版本
   - 必要的依赖包（pytest, pyyaml 等）

## 📋 输出格式

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

🔍 环境检查:
  • Python: 3.14 ✅
  • pytest: 7.4.0 ✅
  • pyyaml: 6.0 ✅
```

## 🎯 使用方式

```bash
/qa-status
```
