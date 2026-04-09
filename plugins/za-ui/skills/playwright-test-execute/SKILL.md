---
name: playwright-test-execute
description: Playwright测试执行和自动修复专家。自动执行优化后的test.ts测试文件，分析测试失败原因，智能修复常见问题(定位器失效、等待超时、数据问题)，支持迭代修复直到测试通过。用于执行playwright测试、调试测试失败、自动修复测试代码。
---

# Playwright测试执行和自动修复专家

## 🎯 Skill主要内容

这个skill提供Playwright测试的**智能执行、分析和自动修复**能力:

- **核心功能**: 执行Playwright测试并自动修复常见问题
- **适用场景**: 测试调试、CI/CD集成、测试维护
- **关键特性**:
  - 智能错误分析和分类
  - 自动修复定位器失效
  - 智能调整等待策略
  - 测试数据问题诊断
  - 迭代修复直到通过

---

## 🔍 执行前核对：优化步骤 vs 原始录制步骤

**在执行测试前，必须先完成步骤核对检查**，确保优化后的测试文件步骤与原始录制文件逻辑一致，避免因步骤遗漏或顺序错误导致测试失败。

### 核对流程

#### 第一步：定位两个文件

根据优化文件路径推断原始文件路径：

```
testcase-optimized/{system}/{module}/{name}.test.ts
       ↓
testcase-native/{system}/{module}/{name}.test.ts
```

**示例**:
```
testcase-optimized/invest/fund/fund-order.test.ts
       ↓
testcase-native/invest/fund/fund-order.test.ts
```

若原始文件不存在，跳过核对步骤并记录。

#### 第二步：提取并对比操作序列

从原始文件提取**所有 `await page.xxx()` 操作行**（按顺序），与优化文件中的 **`componentClick/Input/Check/waitForComponentVisible`** 操作行（按顺序）逐一对比：

| 原始录制操作 | 优化后对应操作 | 核对结果 |
|-------------|---------------|---------|
| `page.locator('input[name="username"]').fill(...)` | `componentInput(helpers, 'Xxx-usernameInput', ...)` | ✅ 对应 |
| `page.getByRole('button', { name: '登 录' }).click()` | `componentClick(helpers, 'Xxx-loginButton')` | ✅ 对应 |
| `page.getByText('明细订单').nth(1).click()` | `componentClick(helpers, 'Xxx-detailOrderTabClick')` | ✅ 对应 |

**核对重点**：
1. **步骤数量**：优化文件的操作步骤数不少于原始文件（允许新增等待步骤，不允许遗漏业务操作）
2. **操作顺序**：业务操作的前后顺序必须与原始录制保持一致
3. **选择器对应**：组件 YAML 中的 `playwright.primary` 选择器必须与原始录制的定位器**逻辑等价**（相同元素，允许换用等价选择器）
4. **操作类型匹配**：`fill` → `componentInput`，`click` → `componentClick`，`check` → `componentCheck`

#### 第三步：检查常见不一致问题

以下问题是转换过程中的高频错误，必须逐项检查：

**问题1：使用了错误的组件（选择器不等价）**

```
原始: page.getByText('明细订单').nth(1).click()
错误: componentClick(helpers, 'Fund-order-detailOrderTab')
      → 组件选择器是 getByRole('tab', ...) 而非 getByText().nth(1)，不等价

正确: componentClick(helpers, 'Fund-order-detailOrderTabClick')
      → 组件选择器应为 page.getByText('明细订单').nth(1)
```

**问题2：步骤遗漏（原始有但优化没有）**

```
原始: page.getByRole('combobox', { name: '上手 :' }).click()  ← 遗漏
      page.locator('div').filter({ hasText: /^AAIM$/ }).nth(2).click()  ← 遗漏
      page.getByRole('button', { name: '查 询' }).click()
```

**问题3：步骤顺序错乱**

```
原始顺序: 点击日期 → 选择上手 → 点击查询
错误顺序: 点击日期 → 点击查询 → 选择上手   ← 顺序错误
```

**问题4：验证用组件和操作用组件混用**

有些组件专为**验证存在**（`toBeVisible`）设计，另一些专为**点击操作**设计，二者选择器可能不同，不可混用：

```
验证用: Fund-order-detailOrderTab → getByRole('tab', { name: '明细订单' })
点击用: Fund-order-detailOrderTabClick → getByText('明细订单').nth(1)
```

#### 第四步：输出核对报告

核对完成后输出报告：

```
📋 步骤核对报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原始文件: testcase-native/invest/fund/fund-order.test.ts (共15个操作步骤)
优化文件: testcase-optimized/invest/fund/fund-order.test.ts (共19个步骤，含4个等待)

✅ 核对通过 (15/15 操作步骤均有对应)

核对详情:
  ✅ 步骤1: fill(username) → componentInput('Invest-auth-login-usernameInput')
  ✅ 步骤2: fill(password) → componentInput('Invest-auth-login-passwordInput')
  ...
  ✅ 步骤14: getByText('明细订单').nth(1).click() → componentClick('Fund-order-detailOrderTabClick')
  ✅ 步骤15: getByText('详情').first().click() → componentClick('Fund-order-detailButton')

▶ 核对通过，继续执行测试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

若发现不一致：

```
⚠️ 核对发现问题，暂停执行，先修复以下问题：

  ❌ 步骤13: getByText('明细订单').nth(1).click()
     优化文件使用: componentClick(helpers, 'Fund-order-detailOrderTab')
     组件选择器: page.getByRole('tab', { name: '明细订单' })
     问题: 选择器与原始录制不等价，原始用 .nth(1) 文本定位
     建议: 新增 Fund-order-detailOrderTabClick 组件，选择器为 page.getByText('明细订单').nth(1)

修复后重新运行核对，确认通过后再执行测试。
```

---

## 🚀 使用指南

### 基本用法

执行单个测试文件:
```bash
npx playwright test testcase-optimized/bib/withdrawal/playwright-native2-loan-withdrawal.test.ts
```

执行整个目录:
```bash
npx playwright test testcase-optimized/bib/
```

带调试模式:
```bash
npx playwright test testcase-optimized/bib/withdrawal/playwright-native2-loan-withdrawal.test.ts --debug
```

### 自动修复流程

1. **[新增] 步骤核对检查**（执行前必做，见上方"执行前核对"章节）
2. **执行测试**
3. **分析失败原因**
4. **智能修复代码**
5. **重新执行验证**
6. **迭代修复**(最多3轮)
7. **生成修复报告**

---

## 📊 错误分析和分类

### 常见错误类型

#### 1. 定位器失效 (Locator Not Found)

**错误特征**:
```
Error: locator.click: Target closed
Error: locator.fill: Element not found
TimeoutError: Timeout 30000ms exceeded.
```

**可能原因**:
- 页面元素已变化(文本、属性、结构)
- 元素尚未加载完成
- 元素被遮挡或不可见
- 选择器表达式错误

**修复策略**:
1. 检查组件库定义是否正确
2. 尝试更新Playwright选择器
3. 添加AI补偿机制
4. 优化等待策略

#### 2. 等待超时 (Timeout Error)

**错误特征**:
```
TimeoutError: page.goto: Timeout 30000ms exceeded
TimeoutError: locator.waitFor: Timeout exceeded
```

**可能原因**:
- 网络慢导致页面加载时间长
- 等待的组件未出现
- SPA路由切换未检测到
- 配置的超时时间不足

**修复策略**:
1. 增加超时配置时间
2. 使用更智能的等待方法
3. 添加waitForComponentVisible等待下一个组件
4. 检查网络请求是否完成

#### 3. 测试数据问题 (Data Issue)

**错误特征**:
```
Error: Invalid username or password
AssertionError: Expected "Approved" but got "Pending"
```

**可能原因**:
- 测试数据已过期或被删除
- 测试账号被锁定
- 测试环境数据不一致
- YAML配置数据错误

**修复策略**:
1. 检查data/目录下的YAML配置
2. 验证测试账号可用性
3. 更新测试数据
4. 添加数据前置准备步骤

#### 4. 断言失败 (Assertion Error)

**错误特征**:
```
AssertionError: expected 'Success' but got 'Failed'
Error: Locator expected to contain text "Approved"
```

**可能原因**:
- 业务逻辑变更
- 页面文案变更
- 异步操作未完成
- 断言条件不准确

**修复策略**:
1. 使用混合断言(Playwright → AI补偿)
2. 调整断言条件
3. 添加等待确保状态稳定
4. 更新预期结果数据

#### 5. 导入路径错误 (Import Error)

**错误特征**:
```
Error: Cannot find module '../utils/hybrid-helpers'
Error: Cannot find module '../../component/component-loader'
```

**可能原因**:
- 文件移动后路径未更新
- 目录层级计算错误
- 文件不存在

**修复策略**:
1. 根据测试文件位置计算正确相对路径
2. 验证被导入文件是否存在
3. 统一路径计算规则

---

## 🔧 自动修复策略

### 修复优先级

```
1. 导入路径修复 (快速修复) ⚡
2. 等待策略优化 (高优先级) 🔥
3. 定位器修复 (中优先级) 🛠️
4. 测试数据更新 (低优先级) 📝
5. 断言条件调整 (需人工确认) ⚠️
```

### 修复决策树

```
测试失败?
│
├─ 导入错误? → 修正导入路径 → 重新执行
│
├─ 等待超时?
│  ├─ page.goto超时? → 增加timeout配置
│  ├─ 组件未出现? → 添加waitForComponentVisible
│  └─ 网络请求慢? → 调整waitForNetworkIdleTimeout
│
├─ 定位器失败?
│  ├─ Playwright选择器失效? → 尝试AI补偿
│  ├─ 组件未定义? → 检查组件库并补充
│  └─ 选择器表达式错误? → 更新组件YAML
│
├─ 测试数据问题?
│  ├─ 用户名密码错误? → 检查YAML配置
│  ├─ 测试账号锁定? → 提示人工处理
│  └─ 数据格式错误? → 修正YAML数据结构
│
└─ 断言失败?
   ├─ 预期结果变更? → 更新YAML中的验证数据
   ├─ 文案变更? → 使用模糊匹配或AI断言
   └─ 业务逻辑变更? → 提示人工Review
```

---

## 🔄 迭代修复流程

### 第1轮: 快速修复

**目标**: 修复明显的低级错误
- ✅ 导入路径错误
- ✅ 语法错误
- ✅ 明显的配置问题

**方法**: 静态代码分析 + 简单替换

### 第2轮: 等待优化

**目标**: 解决等待和时序问题
- ✅ 添加智能等待
- ✅ 调整超时配置
- ✅ 优化页面加载等待

**方法**: 分析错误日志 + 动态插入等待

### 第3轮: 深度修复

**目标**: 解决定位器和数据问题
- ✅ 更新组件定义
- ✅ 修复测试数据
- ✅ 调整断言条件

**方法**: 深度分析 + 智能决策

### 第4轮: 人工介入

如果3轮后仍未通过,生成详细报告提示人工处理:
- 📋 失败原因分析
- 🔍 可能的根因
- 💡 修复建议
- ⚠️ 需要人工确认的点

---

## 📝 执行输出示例

### 成功执行

```
🚀 执行Playwright测试...

命令: npx playwright test testcase-optimized/bib/withdrawal/playwright-native2-loan-withdrawal.test.ts

✅ 测试通过!

执行摘要:
- 测试文件: playwright-native2-loan-withdrawal.test.ts
- 执行时间: 45.3秒
- 通过用例: 1/1
- 失败用例: 0/1

📊 测试报告已生成
```

### 失败并自动修复

```
🚀 执行Playwright测试...

❌ 测试失败 (第1次)

错误分类: 定位器失效
错误信息: TimeoutError: locator.click: Target closed

🔍 分析失败原因...
- 组件 'SubmitButton' 定位器可能已失效
- 页面可能尚未完全加载

🛠️ 应用修复策略...
✅ 在点击前添加 waitForComponentVisible(helpers, 'SubmitButton')
✅ 检查组件库定义

🔄 重新执行测试 (第2次)...

✅ 测试通过!

修复摘要:
- 修复轮次: 1轮
- 修复类型: 等待策略优化
- 修改文件: playwright-native2-loan-withdrawal.test.ts

📊 修复前后对比:
// 修复前
await componentClick(helpers, 'SubmitButton');

// 修复后
await waitForComponentVisible(helpers, 'SubmitButton');
await componentClick(helpers, 'SubmitButton');
```

### 多轮修复

```
🚀 执行Playwright测试...

❌ 测试失败 (第1次) - 定位器失效
🛠️ 修复: 添加等待策略

❌ 测试失败 (第2次) - 导入路径错误
🛠️ 修复: 更正相对路径 ../../../utils/hybrid-helpers

✅ 测试通过 (第3次)!

总修复摘要:
- 总执行次数: 3次
- 修复轮次: 2轮
- 修复操作:
  1. 添加 waitForComponentVisible 等待
  2. 修正导入路径层级

✨ 所有问题已自动解决!
```

---

## 🎯 最佳实践

### 1. 测试前检查

执行测试前建议检查:
- ✅ **[新增] 与原始录制步骤核对**（参考上方"执行前核对"章节）
- ✅ 测试文件路径正确
- ✅ 导入语句路径正确
- ✅ YAML配置文件存在
- ✅ 组件库已完整定义
- ✅ 测试环境可访问

### 2. 逐步调试

遇到复杂问题时:
1. 先执行单个测试文件
2. 使用 `--debug` 模式查看详情
3. 检查Playwright trace
4. 验证测试数据可用性

### 3. 组件库维护

- 定期更新组件库定义
- 使用一致的命名规范
- 为关键组件添加多个选择器备份

### 4. 等待策略

- 优先使用 `waitForComponentVisible`
- 为慢页面增加超时配置
- 在关键操作后添加等待

### 5. 测试数据管理

- 使用环境隔离的测试数据
- 定期清理过期数据
- 避免硬编码敏感信息

---

## 🔍 故障排查指南

### 问题: 测试一直超时

**检查项**:
1. 网络连接是否正常
2. 测试环境URL是否可访问
3. 超时配置是否足够
4. 是否有死循环等待

**解决方法**:
- 增加 `timeout` 配置
- 使用 `--headed` 模式查看实际页面
- 检查网络请求瀑布流

### 问题: 组件定位失败

**检查项**:
1. 组件库YAML定义是否正确
2. 页面元素是否真实存在
3. 元素是否被遮挡或隐藏
4. 选择器表达式是否准确

**解决方法**:
- 使用浏览器开发者工具验证选择器
- 尝试AI补偿机制
- 更新组件库定义

### 问题: 修复后仍失败

**可能原因**:
- 业务逻辑变更(需人工确认)
- 测试环境异常
- 复杂的竞态条件
- 测试代码逻辑错误

**解决方法**:
- 查看详细错误日志
- 使用 `--trace on` 生成trace文件
- 人工Review测试代码
- 对比优化前的原始录制代码

---

## 📚 相关资源

- **测试框架**: Playwright官方文档
- **项目架构**: `playwright-test-generate` SKILL
- **工具方法**: `utils/hybrid-helpers.ts`, `utils/smart-wait-helpers.ts`
- **组件库**: `component/` 目录
- **测试数据**: `data/` 目录
- **配置中心**: `config/test-config.ts`

---

## 🎓 使用场景示例

### 场景1: 本地开发调试

```bash
# 开发者完成代码转换后,本地执行测试
npx playwright test testcase-optimized/bib/withdrawal/cross-border-loan.test.ts

# 如果失败,自动修复并重新执行
# 最多3轮迭代修复
```

### 场景2: CI/CD集成

```bash
# Jenkins/GitLab CI执行所有测试
npx playwright test testcase-optimized/

# 失败时自动修复常见问题
# 生成详细测试报告
```

### 场景3: 批量测试维护

```bash
# 页面大改版后,批量执行测试
npx playwright test testcase-optimized/bib/

# 自动修复定位器失效问题
# 生成修复摘要报告
```

---

## ⚙️ 配置选项

### 超时配置

```typescript
// config/test-config.ts
export const SPECIAL_TIMEOUTS = {
  PAGE_LOAD: 60000,      // 页面加载超时
  COMPONENT_WAIT: 30000, // 组件等待超时
  NETWORK_IDLE: 5000,    // 网络空闲超时
};
```

### 重试配置

```typescript
// playwright.config.ts
export default defineConfig({
  retries: 2,           // 失败重试2次
  timeout: 60000,       // 单个测试超时
  expect: {
    timeout: 10000,     // 断言超时
  },
});
```

### 修复策略配置

```typescript
// 可配置的修复行为
const autoFixConfig = {
  maxFixRounds: 3,               // 最多修复轮次
  enableAutoFix: true,           // 是否启用自动修复
  fixTypes: [                    // 启用的修复类型
    'import-path',
    'wait-strategy',
    'locator-update',
    'data-refresh',
  ],
  requireConfirmation: false,    // 修复前是否需要确认
};
```

---

## 🚨 注意事项

1. **自动修复限制**:
   - 只能修复常见的技术问题
   - 无法修复业务逻辑错误
   - 复杂问题需要人工介入

2. **数据安全**:
   - 不会修改敏感数据
   - 不会删除测试文件
   - 修改前自动备份

3. **执行环境**:
   - 确保网络连接稳定
   - 测试环境URL可访问
   - 浏览器版本兼容

4. **性能考虑**:
   - 多轮修复会增加执行时间
   - 建议先修复明显问题
   - 大批量测试分批执行

---

## 📖 术语表

| 术语 | 说明 |
|------|------|
| **定位器(Locator)** | Playwright用于查找页面元素的表达式 |
| **组件库** | YAML格式的UI组件定义集合 |
| **混合断言** | Playwright断言失败时自动切换AI断言 |
| **智能等待** | 根据页面状态动态调整等待策略 |
| **迭代修复** | 多轮执行-分析-修复的循环过程 |
| **AI补偿** | Playwright方法失败时使用Midscene AI |

---

## 🎯 成功指标

测试执行成功的标准:
- ✅ 所有测试用例通过
- ✅ 执行时间在合理范围
- ✅ 无随机失败(flaky test)
- ✅ 错误日志清晰可读
- ✅ 测试报告完整

修复成功的标准:
- ✅ 3轮内修复成功
- ✅ 修改最小化
- ✅ 不影响其他测试
- ✅ 修复逻辑清晰
- ✅ 生成详细报告
