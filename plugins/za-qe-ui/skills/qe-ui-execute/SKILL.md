---
name: qe-ui-execute
description: 执行Playwright UI自动化测试并智能修复失败。用于：执行测试、调试失败、自动修复测试代码、分析错误原因。当用户说"执行测试"、"运行测试"、"跑一下测试"、"测试失败了"、"帮我修复测试"、"run test"、"fix test"时触发。支持定位器失效、等待超时、数据问题的自动修复，最多3轮迭代，执行前自动核对优化步骤与原始录制步骤是否一致。
metadata:
  category: ui-testing
  version: 2.0.0
---

# Playwright测试执行和自动修复专家

## 核心能力

- 执行优化后的测试脚本（`testcase-optimized/`）
- **执行前**自动核对步骤与原始录制一致性（见 `references/pre-execution-checklist.md`）
- 智能分析失败原因并分类修复
- 最多3轮迭代修复，超出则生成人工介入报告

---

## 执行前核对（必做）

**在执行测试前，先完成步骤核对**，确保优化文件步骤与原始录制逻辑一致。

### 快速核对流程

1. 定位原始文件：`testcase-native/{system}/{module}/{name}.test.ts`
2. 提取原始所有 `await page.xxx()` 操作行（按顺序）
3. 与优化文件中 `componentClick/Input/Check` 操作行逐一对比
4. 输出核对报告，发现问题则暂停执行

**核对重点**：
- 步骤数量不少于原始（允许新增等待，不允许遗漏业务步骤）
- 操作顺序与原始一致
- 组件选择器与原始录制定位器**逻辑等价**
- 操作类型匹配：`fill→componentInput`、`click→componentClick`、`check→componentCheck`

**通过报告示例**：
```
📋 步骤核对报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原始文件: testcase-native/invest/fund/fund-order.test.ts (共15个操作步骤)
优化文件: testcase-optimized/invest/fund/fund-order.test.ts (共19个步骤，含4个等待)

✅ 核对通过 (15/15 操作步骤均有对应)
▶ 核对通过，继续执行测试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**发现问题则暂停**，修复后重新核对。详细核对规则和高频错误示例见 `references/pre-execution-checklist.md`。

---

## 执行命令

```bash
# 执行单个文件
npx playwright test testcase-optimized/bib/withdrawal/cross-border-loan.test.ts

# 执行整个目录
npx playwright test testcase-optimized/bib/

# 调试模式（可视化查看每步执行）
npx playwright test testcase-optimized/bib/withdrawal/cross-border-loan.test.ts --debug

# 生成 trace 文件（用于深度诊断复杂失败）
npx playwright test testcase-optimized/bib/withdrawal/cross-border-loan.test.ts --trace on
# trace 文件生成后用以下命令查看：
npx playwright show-trace test-results/xxx/trace.zip
```

---

## 错误类型与修复策略

| 错误类型 | 典型特征 | 修复策略 |
|---------|---------|---------|
| **导入路径错误** | `Cannot find module '../utils/...'` | 根据文件层级修正相对路径 |
| **等待超时** | `TimeoutError: Timeout XXXms exceeded` | 增加 `waitForComponentVisible`，调整超时配置 |
| **定位器失效** | `locator.click: Target closed` | 更新组件 YAML 选择器，或启用 AI 补偿 |
| **测试数据问题** | `Invalid username or password` | 检查 YAML 配置，验证账号可用性 |
| **断言失败** | `expected 'X' but got 'Y'` | 更新预期值，或改用 AI 断言 |

**修复优先级**：导入路径 → 等待策略 → 定位器 → 测试数据 → 断言条件

---

## 迭代修复流程

```
执行前核对 → 执行测试
      ↓ 失败
第1轮: 导入路径 + 语法错误（快速修复，静态分析）
      ↓ 仍失败
第2轮: 等待超时 + 时序问题（分析日志，动态插入等待）
      ↓ 仍失败
第3轮: 定位器更新 + 数据修复（深度分析，更新组件YAML或测试数据）
      ↓ 仍失败
生成人工介入报告（失败原因 + 根因分析 + 修复建议）
```

**第3轮深度修复方法**：
- 定位器失效 → 使用浏览器开发者工具重新验证选择器，更新组件 YAML 中 `playwright.primary`
- 测试数据失效 → 检查 `data/` 下 YAML 配置，验证账号/密码/业务数据是否过期
- 断言失败 → 确认业务逻辑是否变更，若文案变更则改用 `aiAssert(assertions.xxx)` 替代精确断言

### 修复输出示例

```
❌ 测试失败 (第1次)
错误: TimeoutError: locator.click: Target closed
分析: 组件 'SubmitButton' 点击前页面未就绪

🛠️ 修复: 添加 waitForComponentVisible(helpers, 'SubmitButton')

🔄 重新执行 (第2次)...
✅ 测试通过!

修复摘要:
- 修复轮次: 1轮 | 类型: 等待策略优化
- 修改: 在 componentClick('SubmitButton') 前插入 waitForComponentVisible
```

---

## 执行前检查清单

- [ ] 已完成步骤核对（与原始录制一致）
- [ ] 测试文件路径正确
- [ ] 导入语句路径层级正确（根据目录深度：`../../` 或 `../../../`）
- [ ] YAML 数据文件存在且格式正确
- [ ] 组件库已加载（`componentLoader.loadFromDirectory` 指向正确目录）
- [ ] 测试环境 URL 可访问

---

## 最佳实践

1. **先核对再执行**：执行前必做步骤核对，避免因步骤遗漏浪费调试时间
2. **逐步调试**：遇到复杂问题先执行单文件，再用 `--debug` 模式查看详情，再看 trace
3. **导入路径层级规则**：根据文件深度调整 — 根目录 `../utils/`，一级 `../../utils/`，二级 `../../../utils/`
4. **等待策略**：优先用 `waitForComponentVisible`（检测组件实际出现），避免硬编码 `page.waitForTimeout()`
5. **测试数据管理**：账号密码放 YAML，不要硬编码；测试账号被锁时需人工处理，无法自动修复

---

## 故障排查

| 现象 | 检查项 | 解决 |
|------|--------|------|
| 测试一直超时 | 网络/URL可达性；`TIMEOUTS.FULL_LOAD` 配置是否足够 | 增加 `timeout`；用 `--headed` 看实际页面 |
| 组件定位失败 | 组件 YAML `playwright.primary` 是否与实际 DOM 匹配 | 浏览器开发者工具验证选择器；更新组件 YAML |
| 3轮修复后仍失败 | 业务逻辑是否已变更；是否有竞态条件 | 查看 `--trace on` 生成的 trace 文件；人工 Review |
| 修复后其他用例失败 | 改动是否波及共用组件 | 检查改动的组件是否被其他测试使用 |

---

## 人工介入场景

以下情况自动修复无法处理，需人工确认：
- 业务逻辑变更（预期结果已发生变化）
- 测试账号被锁定
- 复杂竞态条件
- 3轮修复后仍失败

---

## 参考资源

- **执行前步骤核对详细流程**: `references/pre-execution-checklist.md`
- **工具方法**: `utils/hybrid-helpers.ts`、`utils/smart-wait-helpers.ts`
- **组件库**: `component/` 目录
- **测试数据**: `data/` 目录
- **配置中心**: `config/test-config.ts`
