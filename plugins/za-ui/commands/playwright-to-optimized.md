---
allowed-tools: Task(playwright-to-optimized-converter-agent:*), Bash, Read, Skill
description: Playwright完整工作流：转换优化 + 测试执行 + 自动修复 🎯 一站式解决方案
---

## Context
- 操作模式和文件路径: $ARGUMENT

## Your task

{% if ARGUMENT %}

根据$ARGUMENT智能识别并执行:

### 模式识别

- **转换模式**: 路径包含`testcase-native` → 转换原生代码为优化架构
- **测试模式**: 路径包含`testcase-optimized`或`--test` → 执行测试并自动修复(最多3轮)
- **完整模式**: 包含`--full` → 转换+测试+修复一气呵成

---

## 执行流程

### 转换模式
1. 调用`playwright-to-optimized-converter-agent`转换代码
2. 生成优化代码、YAML配置、更新组件库
3. **询问**: "转换完成！是否立即执行测试验证？[Y/N]"
   - Y → 自动进入测试模式
   - N → 结束

### 测试模式
1. 激活`playwright-test-execute` SKILL
2. 执行`npx playwright test [文件路径]`
3. 测试结果:
   - ✅ 通过 → 显示成功摘要
   - ❌ 失败 → 自动修复流程(最多3轮)

**自动修复流程**:
- 第1轮: 快速修复(导入路径、语法、配置)
- 第2轮: 等待优化(添加waitForComponentVisible、调整超时)
- 第3轮: 深度修复(更新组件定义、修复数据、调整断言)
- 3轮后仍失败 → 生成详细诊断报告

### 完整模式
顺序执行: 转换 → 测试 → 修复(无需中间确认)

---

## 参数说明

| 参数 | 说明 |
|------|------|
| `testcase-native/...` | 转换模式 |
| `testcase-optimized/...` | 测试模式 |
| `--test` | 强制测试模式 |
| `--full` | 完整工作流 |
| `--debug` | Playwright调试模式 |
| `--no-fix` | 禁用自动修复 |
| `--max-rounds=N` | 最大修复轮次(默认3) |

---

## 使用示例

```bash
# 转换原生代码
/playwright-to-optimized testcase-native/login-test.test.ts

# 测试优化后代码
/playwright-to-optimized testcase-optimized/bib/withdrawal/test.test.ts

# 完整工作流
/playwright-to-optimized testcase-native/test.test.ts --full

# 调试模式
/playwright-to-optimized testcase-optimized/test.test.ts --debug
```

---

## 相关SKILL

- **playwright-test-generate** - 转换规则和优化策略
- **playwright-test-execute** - 测试执行和自动修复规则

详细规则、错误分析、修复策略参见对应SKILL文档。

{% else %}

请提供文件路径或操作参数。

## 快速使用

```bash
# 转换原生代码
/playwright-to-optimized testcase-native/test.test.ts

# 测试优化后代码
/playwright-to-optimized testcase-optimized/bib/withdrawal/test.test.ts

# 完整工作流
/playwright-to-optimized testcase-native/test.test.ts --full
```

{% endif %}
