# 增量更新模式参考

## 8种常见更新模式

### 模式1：新增条件性弹窗处理

**触发场景**: "登录后可能出现XX弹窗，需要关闭"

```typescript
await componentClick(helpers, 'Auth-login-loginButton');
await waitForComponentVisible(helpers, 'Auth-otp-dismissPopupButton', {
  timeout: 3000,
  optional: true  // 不强制等待
});
await componentClick(helpers, 'Auth-otp-dismissPopupButton', {
  skipIfNotFound: true  // 元素不存在时跳过
});
```

### 模式2：新增表单字段填写

**触发场景**: "提款申请中需要新增填写备注字段"

```typescript
await componentInput(helpers, 'Loan-withdrawal-amountInput', testData.loanApplication.withdrawal.amount.toString());
// ↓ 新增
await componentInput(helpers, 'Loan-withdrawal-remarkInput', testData.loanApplication.withdrawal.remark);
```

```yaml
# 同步更新 testData
testData:
  loanApplication:
    withdrawal:
      remark: "测试备注"    # 新增字段
```

### 模式3：新增可见性断言

**触发场景**: "点击提交后，需要验证页面显示'申请成功'"

```typescript
await componentClick(helpers, 'Loan-withdrawal-submitButton');
await waitForComponentVisible(helpers, 'Loan-withdrawal-successMessage');

const hybridAssert = createHybridAssert(helpers);
// 直接传组件名，无需 getComponentLocator，无需 errorMsg
await hybridAssert.toBeVisible('Loan-withdrawal-successMessage');
```

```yaml
# 同步更新组件 YAML
  Loan-withdrawal-successMessage:
    playwright:
      primary: "page.getByText('申請成功')"
    description: 提交成功提示文字
    category: text
```

### 模式4：新增文本内容断言

**触发场景**: "需要验证特定文字内容"

```typescript
const hybridAssert = createHybridAssert(helpers);
const successMsgLocator = getComponentLocator(helpers, 'Loan-withdrawal-successMessage');
await hybridAssert.toContainText(successMsgLocator, testData.verification.successText);
```

```yaml
testData:
  verification:
    successText: "申請成功"
```

### 模式5：更新导航路径

**触发场景**: "贷款菜单的路径变了，需要更新导航步骤"

```typescript
// 修改前
await componentClick(helpers, 'Loan-nav-loanMenu');

// 修改后（新增一级菜单）
await componentClick(helpers, 'Loan-nav-productMenu');   // 新增
await componentClick(helpers, 'Loan-nav-loanMenu');
```

### 模式6：更新组件选择器

**触发场景**: "登录按钮的文字从'登入'改成了'登錄'"

```yaml
  Auth-login-loginButton:
    playwright:
      primary: "page.getByRole('button', { name: '登錄', exact: true })"  # 修改
    description: 登录按钮
    category: button
```

### 模式7：新增或修改下载验证

**触发场景**: "需要验证文件成功下载到本地"

```typescript
import { triggerAndVerifyDownload } from '../../../utils/download-helpers';

const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadButton'); },
  { expectedExtension: /\.(pdf|xlsx|csv)$/i }  // 可选
);
console.log(`下载成功: ${downloadResult.filename} (${downloadResult.fileSize} bytes)`);
```

**禁止**：使用 `download.failure()` 或手动 `import * as fs from 'fs'` 内联验证。

### 模式8：新增或修改 aiAssert 断言

**触发场景**: "需要新增 AI 智能断言"

```yaml
# 步骤1：断言文本存入 YAML
testData:
  assertions:
    stockStatementMonths: "查询截止到当前每个月份的结单，例如：当前是2026年3月1号，那最新一个结单月份为202602"
```

```typescript
// 步骤2：解构并引用
const { testUser, customer, assertions } = testData;
await aiAssert(assertions.stockStatementMonths);
```

**禁止**：`await aiAssert('直接硬编码的断言字符串')`

---

## 补全 Selector Discovery 机制（模式8扩展）

判断是否需要补全（缺少任一项即补）：
- `import` 中没有 `selectorFallbackRegistry`
- `test` 函数签名没有 `aiLocate` 参数
- `createHybridHelpers` 调用没有传 `aiLocate`
- 没有 `afterAll` 调用 `selectorFallbackRegistry` 三件套

```typescript
// 1. import 补充
import { selectorFallbackRegistry } from '../../../utils/selector-discovery';

// 2. test 函数签名加入 aiLocate
test('用例名', async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page }) => {

// 3. createHybridHelpers 传入 aiLocate
const helpers = await createHybridHelpers(page, { recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert });

// 4. afterAll 补充（与 afterEach 分开，不合并）
test.afterAll(async () => {
  selectorFallbackRegistry.printReport();
  await selectorFallbackRegistry.applyToYaml();
  selectorFallbackRegistry.clear();
});
```

---

## testSteps index 重排规则

插入或删除步骤后，必须对**后续所有步骤**重新递增排序，确保全局 index 连续无重复：

```yaml
testSteps:
  loginSteps:
    - index: 1
      componentName: Auth-login-usernameInput
      action: input

    - index: 2
      componentName: Auth-login-loginButton
      action: click

    # 新增步骤
    - index: 3
      componentName: Auth-otp-dismissButton
      action: click
      optional: true

  otpVerificationSteps:
    - index: 4        # ← 原来是 3，受插入影响，后续全部 +1
      componentName: Auth-otp-otpInput1
      action: input
```

---

## 执行约束速查

### 必须遵守
1. 先读后改：必须先完整读取目标文件再修改
2. 最小化改动：只修改必要部分
3. 命名规范：`{Module}-{FileName}-{componentName}`
4. index 连续性：插入/删除后重新排序所有 index
5. 元数据同步：修改步骤数量后更新 `metadata.totalSteps` 和 `lastUpdated`

### 禁止事项
- 不删除/修改 `afterAll` 中 `selectorFallbackRegistry` 三件套
- 不从 `createHybridHelpers` 移除 `aiLocate`
- 不修改 `beforeAll`、`afterEach` 等框架代码（除非明确要求）
- 不使用 `download.failure()` 作为唯一下载验证
- 不在业务步骤中直接 `await aiAct(...)` 操作 UI（唯一例外：末尾 `await aiAct("执行结束")`）
- 不在 `.test.ts` 中硬编码 `aiAssert` 字符串参数
- **不使用 `expect()` 进行断言**（包括所有形式；发现时必须迁移到 `hybridAssert`）
