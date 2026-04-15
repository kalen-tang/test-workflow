# 执行前步骤核对详细流程

执行测试前，确保优化后的测试文件步骤与原始录制文件逻辑一致。

## 第一步：定位两个文件

根据优化文件路径推断原始文件路径：

```
testcase-optimized/{system}/{module}/{name}.test.ts
       ↓
testcase-native/{system}/{module}/{name}.test.ts
```

若原始文件不存在，跳过核对步骤并记录。

## 第二步：提取并对比操作序列

从原始文件提取**所有 `await page.xxx()` 操作行**（按顺序），与优化文件中的 **`componentClick/Input/Check/waitForComponentVisible`** 操作行（按顺序）逐一对比：

| 原始录制操作 | 优化后对应操作 | 核对结果 |
|-------------|---------------|---------|
| `page.locator('input[name="username"]').fill(...)` | `componentInput(helpers, 'Auth-login-usernameInput', ...)` | ✅ 对应 |
| `page.getByRole('button', { name: '登 录' }).click()` | `componentClick(helpers, 'Auth-login-loginButton')` | ✅ 对应 |

**核对重点**：
1. **步骤数量**：优化文件操作步骤数不少于原始文件（允许新增等待步骤，不允许遗漏业务操作）
2. **操作顺序**：业务操作的前后顺序必须与原始录制保持一致
3. **选择器对应**：组件 YAML 中的 `playwright.primary` 必须与原始录制的定位器**逻辑等价**
4. **操作类型匹配**：`fill` → `componentInput`，`click` → `componentClick`，`check` → `componentCheck`

## 第三步：高频错误检查

**错误1：使用了逻辑不等价的选择器**
```
原始: page.getByText('明细订单').nth(1).click()
错误: componentClick(helpers, 'Fund-order-detailOrderTab')
      → 组件选择器是 getByRole('tab', ...) 而非 getByText().nth(1)，不等价

正确: componentClick(helpers, 'Fund-order-detailOrderTabClick')
      → 组件选择器应为 page.getByText('明细订单').nth(1)
```

**错误2：步骤遗漏**
```
原始: page.getByRole('combobox', { name: '上手 :' }).click()  ← 遗漏
      page.locator('div').filter({ hasText: /^AAIM$/ }).nth(2).click()  ← 遗漏
      page.getByRole('button', { name: '查 询' }).click()
```

**错误3：步骤顺序错乱**
```
原始顺序: 点击日期 → 选择上手 → 点击查询
错误顺序: 点击日期 → 点击查询 → 选择上手   ← 顺序错误
```

**错误4：验证用组件和操作用组件混用**
```
验证用: Fund-order-detailOrderTab → getByRole('tab', { name: '明细订单' })
点击用: Fund-order-detailOrderTabClick → getByText('明细订单').nth(1)
```

## 第四步：输出核对报告

**通过**:
```
📋 步骤核对报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原始文件: testcase-native/invest/fund/fund-order.test.ts (共15个操作步骤)
优化文件: testcase-optimized/invest/fund/fund-order.test.ts (共19个步骤，含4个等待)

✅ 核对通过 (15/15 操作步骤均有对应)
▶ 核对通过，继续执行测试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**发现问题**:
```
⚠️ 核对发现问题，暂停执行，先修复以下问题：

  ❌ 步骤13: getByText('明细订单').nth(1).click()
     优化文件使用: componentClick(helpers, 'Fund-order-detailOrderTab')
     组件选择器: page.getByRole('tab', { name: '明细订单' })
     问题: 选择器与原始录制不等价
     建议: 新增 Fund-order-detailOrderTabClick 组件

修复后重新运行核对，确认通过后再执行测试。
```

---

## 修复决策树

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

## 修复优先级

```
1. 导入路径修复 (快速修复) ⚡
2. 等待策略优化 (高优先级) 🔥
3. 定位器修复 (中优先级) 🛠️
4. 测试数据更新 (低优先级) 📝
5. 断言条件调整 (需人工确认) ⚠️
```
