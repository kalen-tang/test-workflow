---
name: playwright-test-update
description: 已优化测试脚本的增量更新专家。无需重新录制或重新生成，通过自然语言描述直接对testcase-optimized目录下的测试脚本、组件YAML和数据YAML进行精准的增量修改。支持新增步骤、修改步骤、删除步骤、更新组件定义、更新测试数据等场景。
---

# 测试脚本增量更新专家

## 核心定位

专为"**已有优化脚本，需要局部修改**"场景设计。用户只需用自然语言描述改动内容，无需重新录制和生成完整脚本。

**适用场景**:
- 在现有流程中新增操作步骤（如新增一个填写字段）
- 修改某个步骤的操作内容或目标组件
- 删除不再需要的步骤
- 更新组件的 Playwright 选择器
- 修改测试数据（如账号、金额、URL）
- 在流程中插入断言验证

**不适用场景** (请使用 `/playwright-to-optimized`):
- 全新测试用例，没有任何已有脚本
- 改动超过 60% 的步骤（建议重新生成）

---

## 执行流程

### 第一阶段：理解改动需求

接收用户的自然语言描述，解析以下信息：

1. **目标文件**：哪个测试脚本需要修改（从上下文或用户指定中获取）
2. **改动类型**：
   - `add-step` 新增步骤
   - `modify-step` 修改步骤
   - `delete-step` 删除步骤
   - `add-component` 新增组件定义
   - `modify-component` 修改组件定义
   - `update-data` 更新测试数据
   - `add-assertion` 新增断言
3. **改动位置**：在哪个步骤之前/之后插入，或修改第几步
4. **改动内容**：具体要做什么操作，操作哪个 UI 元素

**解析示例**:

用户描述：
> "在登录按钮点击后，新增一步：点击'我知道了'弹窗关闭按钮"

解析结果：
```
改动类型: add-step
位置: LoginButton 点击之后
操作: click
目标元素: 弹窗关闭按钮（可能是 "我知道了" 按钮）
需要新增组件: 是（需要在对应 YAML 中添加组件定义）
```

---

### 第二阶段：读取目标文件

**必须先读取**以下相关文件再进行修改：

```
1. testcase-optimized/{path}/{test-name}.test.ts    # 测试脚本
2. data/{path}/{test-name}.yaml                     # 测试数据和步骤定义
3. component/{system}/{module}/{file}.yaml           # 涉及到的组件定义文件
4. component/{system}/RULES.md                      # 应用级组件规则（若存在必须读取）
```

**应用级规则加载**：根据测试脚本中 `componentLoader.loadFromDirectory` 的路径识别系统，检查对应的 `RULES.md` 是否存在，若存在必须读取并遵守其中的强制组件规则。

已知规则文件：
- `component/invest/RULES.md` — invest 投资运营系统组件规则

**文件定位策略**:

若用户未明确指定文件，按以下顺序推断：
1. 从当前对话上下文中找到最近操作的文件
2. 让用户提供文件路径
3. 扫描 `testcase-optimized/` 目录，列出候选文件供用户选择

**读取后确认改动范围**:

```
📁 目标文件已读取:
- 测试脚本: testcase-optimized/bib/withdrawal/cross-border-ecommerce-revolving.test.ts
  → 共 X 个测试步骤，当前使用 N 个组件
- 测试数据: data/bib/withdrawal/cross-border-ecommerce-revolving.yaml
  → testSteps 共 M 个步骤
- 组件文件: component/bib/auth/otp.yaml
  → 当前包含 K 个组件

📋 计划改动:
1. [新增组件] 在 component/bib/auth/otp.yaml 中添加 Auth-otp-dismissButton
2. [修改测试脚本] 在 LoginButton 点击后插入新步骤
3. [更新测试数据] 在 testSteps.loginSteps 中插入新步骤定义（index 重新排序）

确认后继续执行...
```

---

### 第三阶段：执行增量修改

#### 3.1 新增/修改组件定义

当需要新增组件时，在对应 YAML 文件末尾追加，遵循命名规范：

**命名规范**（必须遵守）:
```
{Module}-{FileName}-{componentName}
示例: Auth-otp-dismissButton, Loan-withdrawal-amountConfirmText
```

**组件 YAML 追加格式**:
```yaml
  Auth-otp-dismissButton:
    playwright:
      primary: "page.getByRole('button', { name: '我知道了' })"
    description: 弹窗关闭按钮
    category: button
```

**修改现有组件选择器**:
```yaml
# 修改前
  Auth-otp-continueButton:
    playwright:
      primary: "page.getByRole('button', { name: '繼 續' })"

# 修改后（更新选择器）
  Auth-otp-continueButton:
    playwright:
      primary: "page.getByRole('button', { name: '繼續' })"
```

#### 3.2 修改测试脚本（.test.ts）

**新增步骤**（在指定位置插入）:
```typescript
// 新增步骤示例：在 componentClick(helpers, 'Auth-login-loginButton') 之后插入
await componentClick(helpers, 'Auth-login-loginButton');
// ↓ 新增以下步骤
await waitForComponentVisible(helpers, 'Auth-otp-dismissButton', { timeout: 5000, optional: true });
await componentClick(helpers, 'Auth-otp-dismissButton', { skipIfNotFound: true });
// ↑ 新增结束
await waitForComponentVisible(helpers, 'Auth-otp-otpInput1');
```

**关键注意事项**:
- 步骤间等待：新增步骤后，检查是否需要调整后续的 `waitForComponentVisible`
- `skipIfNotFound: true`：对于条件性出现的元素（如弹窗），使用此选项
- 保持代码风格与现有代码一致

**修改步骤**（更新操作或目标）:
```typescript
// 修改前
await componentInput(helpers, 'Loan-withdrawal-amountInput', '10000');

// 修改后（改用测试数据中的字段）
await componentInput(helpers, 'Loan-withdrawal-amountInput', testData.loanApplication.withdrawal.amount.toString());
```

**删除步骤**（移除整行或代码块）:
```typescript
// 删除此步骤
// await componentClick(helpers, 'Loan-withdrawal-obsoleteButton');
// await waitForComponentVisible(helpers, 'Loan-withdrawal-nextPage');
```

#### 3.3 更新测试数据 YAML

**在 testSteps 中插入新步骤**（重要：需要重新排序 index）:

```yaml
testSteps:
  loginSteps:
    - index: 1
      componentName: Auth-login-usernameInput
      action: input
      description: 输入用户名

    - index: 2
      componentName: Auth-login-passwordInput
      action: input
      description: 输入密码

    - index: 3
      componentName: Auth-login-loginButton
      action: click
      description: 点击登录按钮

    # 新增步骤（在 loginButton 之后插入）
    - index: 4
      componentName: Auth-otp-dismissButton
      action: click
      description: 关闭登录后弹窗（若存在）
      optional: true

  otpVerificationSteps:
    - index: 5        # ← 原来是 4，受新增步骤影响，后续 index 全部 +1
      componentName: Auth-otp-otpInput1
      action: input
      description: 输入OTP验证码第1位
```

**重要**: 插入新步骤后，必须对后续所有步骤的 `index` 重新递增排序，确保全局 index 连续无重复。

**更新测试数据字段**:
```yaml
testData:
  loanApplication:
    withdrawal:
      amount: 20000    # 修改前是 13000
```

**更新元数据**:
```yaml
metadata:
  totalSteps: 28    # 原来是 27，新增1步后更新
  lastUpdated: 2026-03-23
```

---

### 第四阶段：输出变更摘要

完成修改后，输出清晰的变更摘要：

```
✅ 增量更新完成

📝 变更摘要:
1. [组件新增] component/bib/auth/otp.yaml
   + Auth-otp-dismissButton (弹窗关闭按钮)

2. [脚本修改] testcase-optimized/bib/withdrawal/cross-border-ecommerce-revolving.test.ts
   + 在第3步（点击登录按钮）之后新增弹窗关闭步骤（skipIfNotFound: true）
   ~ 调整后续 waitForComponentVisible 的目标

3. [数据更新] data/bib/withdrawal/cross-border-ecommerce-revolving.yaml
   + testSteps.loginSteps 新增 index=4 步骤
   ~ 后续 10 个步骤的 index 已重新排序 (4→5, 5→6, ...)
   ~ metadata.totalSteps 更新为 28

⚠️  建议验证:
- 运行测试确认弹窗处理正常
- 若弹窗并非每次出现，skipIfNotFound: true 已设置，可安全跳过
```

---

## 常见改动模式

### 模式1：新增条件性弹窗处理

**描述**: "登录后可能出现XX弹窗，需要关闭"

```typescript
// 使用 skipIfNotFound 处理条件性元素
await componentClick(helpers, 'Auth-login-loginButton');
await waitForComponentVisible(helpers, 'Auth-otp-dismissPopupButton', {
  timeout: 3000,
  optional: true  // 不强制等待
});
await componentClick(helpers, 'Auth-otp-dismissPopupButton', {
  skipIfNotFound: true  // 元素不存在时跳过
});
```

### 模式2：在流程中新增表单字段填写

**描述**: "提款申请中需要新增填写备注字段"

```typescript
// 在现有字段填写之后插入
await componentInput(helpers, 'Loan-withdrawal-amountInput', testData.loanApplication.withdrawal.amount.toString());
// ↓ 新增
await componentInput(helpers, 'Loan-withdrawal-remarkInput', testData.loanApplication.withdrawal.remark);
// ↑ 新增
await componentClick(helpers, 'Loan-withdrawal-continueButton');
```

```yaml
# 同步更新 testData
testData:
  loanApplication:
    withdrawal:
      amount: 13000
      remark: "测试备注"    # 新增字段
```

### 模式3：新增断言验证

**描述**: "点击提交后，需要验证页面显示'申请成功'"

**可见性断言** — 使用 `toBeVisible`，直接传组件名：

```typescript
// 在提交操作后新增可见性断言
await componentClick(helpers, 'Loan-withdrawal-submitButton');
await waitForComponentVisible(helpers, 'Loan-withdrawal-successMessage');

const hybridAssert = createHybridAssert(helpers);
// 直接传组件名，AI回退时自动使用组件YAML中的description字段
await hybridAssert.toBeVisible('Loan-withdrawal-successMessage');
```

- 无需 `getComponentLocator`，无需 `errorMsg`
- AI 回退提示词自动取自组件 `description`，如 `"提交成功提示文字" should be visible on the page`

**文本内容断言** — 使用 `toContainText`，传 Locator：

```typescript
const hybridAssert = createHybridAssert(helpers);
const successMsgLocator = getComponentLocator(helpers, 'Loan-withdrawal-successMessage');
await hybridAssert.toContainText(successMsgLocator, testData.verification.successText);
```

```yaml
# 同步更新 testData 和组件
testData:
  verification:
    successText: "申請成功"
```

```yaml
# 同步更新组件 YAML
  Loan-withdrawal-successMessage:
    playwright:
      primary: "page.getByText('申請成功')"
    description: 提交成功提示文字
    category: text
```

### 模式4：修改导航路径

**描述**: "贷款菜单的路径变了，需要更新导航步骤"

```typescript
// 修改前
await componentClick(helpers, 'Loan-nav-loanMenu');
await componentClick(helpers, 'Loan-nav-withdrawalSubMenu');

// 修改后（新增一级菜单）
await componentClick(helpers, 'Loan-nav-productMenu');   // 新增
await componentClick(helpers, 'Loan-nav-loanMenu');
await componentClick(helpers, 'Loan-nav-withdrawalSubMenu');
```

### 模式5：更新组件选择器

**描述**: "登录按钮的文字从'登入'改成了'登錄'，需要更新选择器"

```yaml
# 修改组件 YAML
  Auth-login-loginButton:
    playwright:
      primary: "page.getByRole('button', { name: '登錄', exact: true })"  # 修改此行
    description: 登录按钮
    category: button
```

### 模式6：新增或修改下载验证

**描述**: "需要验证点击下载按钮后，文件是否成功下载到本地"

**正确做法** — 使用 `triggerAndVerifyDownload`：

```typescript
// 在 import 区域添加
import { triggerAndVerifyDownload } from '../../../utils/download-helpers';

// 在下载操作处使用（替代内联写法）
const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadButton'); }
);
console.log(`下载成功: ${downloadResult.filename} (${downloadResult.fileSize} bytes)`);
```

**需要校验文件格式时**：
```typescript
const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadButton'); },
  { expectedExtension: /\.(pdf|xlsx|csv)$/i }
);
```

**`triggerAndVerifyDownload` 内置验证内容**（无需额外断言）：
1. `download.path() !== null` — 文件已完整落盘（核心验证）
2. `fileSize >= minFileSize` — 文件内容非空
3. `suggestedFilename` 非空 — 文件名存在

**禁止的写法**（需要迁移到上述模式）：
```typescript
// ❌ 错误：download.failure() 只验证 HTTP 层，不代表文件落盘
const downloadFailure = await download.failure();
expect(downloadFailure).toBeNull();

// ❌ 错误：手动 import fs 内联验证
import * as fs from 'fs';
const filePath = await download.path();
const fileSize = fs.statSync(filePath!).size;
```

### 模式7：新增或修改 aiAssert 断言

**描述**: "需要新增/修改 AI 智能断言"

**规则：aiAssert 的断言文本必须存入 YAML `testData.assertions`，禁止在 `.test.ts` 中硬编码字符串。**

**步骤1：在 YAML `testData.assertions` 下新增或修改键值**

```yaml
# data/{path}/{test-name}.yaml
testData:
  # ... 其他数据 ...

  assertions:
    stockStatementMonths: "查询截止到当前每个月份的结单，例如：当前是2026年3月1号，那最新一个结单月份为202602，第二个为202601"
    # 多个断言各自一个键
    pageTitle: "页面标题应显示'客户信息维护'"
```

键名规则：camelCase，语义描述断言内容。

**步骤2：测试代码解构 `assertions` 并引用**

```typescript
// 顶部解构时加入 assertions（若尚未包含）
const { testUser, customer, assertions } = testData;

// 使用变量引用，禁止硬编码
await aiAssert(assertions.stockStatementMonths);
```

**新增 aiAssert 时完整改动清单**：
1. YAML `testData.assertions` 新增键值对
2. `.test.ts` 顶部解构加入 `assertions`（若已有则无需重复）
3. 在对应位置调用 `await aiAssert(assertions.xxx)`

**禁止的写法**：
```typescript
// ❌ 错误：直接硬编码断言字符串
await aiAssert('查询截止到当前每个月份的结单...');

// ✅ 正确：从 testData 读取
await aiAssert(assertions.stockStatementMonths);
```

### 模式8：为旧脚本补齐选择器自动发现机制

**描述**: "现有脚本缺少 selector discovery 机制，需要补全"

判断是否需要补全（缺少任一项即补）:
- import 中没有 `selectorFallbackRegistry`
- test 函数签名没有 `aiLocate` 参数
- `createHybridHelpers` 调用没有传 `aiLocate`
- 没有 `afterAll` 调用 `selectorFallbackRegistry` 三件套

补全内容:

```typescript
// 1. import 补充
import { selectorFallbackRegistry } from '../../../utils/selector-discovery';

// 2. test 函数签名加入 aiLocate
test('用例名', async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page }) => {

// 3. createHybridHelpers 传入 aiLocate
const helpers = await createHybridHelpers(page, { recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert });

// 4. afterAll（afterEach 保留 testStepManager.reset()，两者不合并）
test.afterAll(async () => {
  selectorFallbackRegistry.printReport();
  await selectorFallbackRegistry.applyToYaml();
  selectorFallbackRegistry.clear();
});
```

---

## 执行约束

### 必须遵守的规则

1. **先读后改**: 必须先完整读取目标文件，再进行修改，禁止凭记忆修改
2. **最小化改动**: 只修改必要的部分，不重构无关代码
3. **命名规范**: 新增组件必须遵守 `{Module}-{FileName}-{componentName}` 格式
4. **index 连续性**: 在 testSteps YAML 中插入/删除步骤后，必须重新排序所有 index
5. **元数据同步**: 修改步骤数量后，更新 `metadata.totalSteps` 和 `lastUpdated`
6. **代码风格一致**: 新增代码风格必须与现有代码保持一致（缩进、引号、await 等）
7. **selector discovery 完整性**: 每个测试文件必须包含 `aiLocate` 参数、`selectorFallbackRegistry` import 及 `afterAll` 三件套；修改现有文件时若缺失则补全（参考模式8）

### 禁止事项

- 不删除或修改 `afterAll` 中的 `selectorFallbackRegistry.printReport/applyToYaml/clear` 调用
- 不从 `createHybridHelpers` 中移除 `aiLocate` 参数
- 不修改 `test.beforeAll`、`test.afterEach` 等框架代码（除非明确要求）
- 不修改 import 语句（除非新增了新的工具方法）
- 不删除已有的组件定义（除非明确要求）
- 不重命名已有的组件（会破坏其他引用）
- 不使用 `download.failure()` 作为下载验证的唯一手段（应改用 `triggerAndVerifyDownload`）
- 不在业务步骤中直接调用 `await aiAct(...)` 操作 UI（应使用 `componentClick/Input/Check`）；唯一例外是用例末尾的 `await aiAct("执行结束")`
- 不在 `.test.ts` 中硬编码 `aiAssert` 字符串参数（应存入 YAML `testData.assertions.xxx` 并通过变量引用）
- **不在测试文件中直接使用 `expect()` 进行断言**：包括 `expect(locator).toContainText()`、`expect(locator).toMatchAriaSnapshot()` 等所有形式；发现已有 `expect()` 断言时必须迁移到 `hybridAssert` 对应方法，同时从 `import` 中移除 `expect`

---

## 与其他工具的协同

| 场景 | 推荐工具 |
|------|----------|
| 全新测试用例 | `/playwright-to-optimized` |
| 已有脚本局部修改 | `/za:playwright-test-update`（本工具）|
| 执行测试并修复失败 | `playwright-test-execute` skill |
| 运行完整工作流 | `playwright-to-optimized` skill |

---

## 注意事项

1. **组件文件路径推断**: 根据组件名称的 Module 前缀推断组件所在文件。例如 `Auth-otp-*` 对应 `component/bib/auth/otp.yaml`，`Loan-withdrawal-*` 对应 `component/bib/loan/withdrawal.yaml`

2. **系统区分**: BIB 系统组件在 `component/bib/`，OPS 系统组件在 `component/za-bank-ops/`

3. **waitForComponentVisible 调整**: 新增步骤时，检查原有的 `waitForComponentVisible` 是否还合理：
   - 若新步骤在等待目标之前，等待逻辑通常不需要修改
   - 若新步骤会导致页面状态变化，可能需要在新步骤前后调整等待

4. **skipIfNotFound 使用场景**:
   - 条件性弹窗（不一定每次出现）
   - 可选的引导提示
   - 测试环境偶发性的 UI 差异
