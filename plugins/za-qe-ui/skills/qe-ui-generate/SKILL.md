---
name: qe-ui-generate
description: 将Playwright录制的原生UI自动化代码转换为应用当前项目优化规则的混合架构测试代码。读取testcase-native目录下的原生代码,生成到testcase-optimized目录(与data目录结构1:1对应),支持智能等待、组件驱动、AI上下文增强、混合断言等优化模式。
---

# Playwright原生代码优化转换器

## 🎯 核心功能

将Playwright Codegen录制的原生代码转换为项目优化架构:

- **智能等待优化**: `page.waitForTimeout()` → `waitForComponentVisible()`
- **组件驱动架构**: 选择器提取到YAML组件库,使用`componentClick/Input/Check`
- **混合架构实现**: Playwright优先 → Midscene AI补偿
- **测试数据分离**: 硬编码数据提取到YAML配置
- **AI上下文增强**: 多层次prompt构建,业务描述优先,技术选择器辅助
- **混合断言工具**: 使用`createHybridAssert`实现断言失败时AI补偿

---

## 🚀 转换流程

### 1. 读取原始代码

从`testcase-native`目录读取Playwright原生测试文件。

### 2. 分析和提取

- **测试流程**: 业务步骤和操作序列
- **UI交互**: 点击、输入、勾选等操作
- **选择器**: Playwright定位器表达式
- **测试数据**: 硬编码的用户名、密码、金额等
- **等待策略**: 现有等待方式

### 3. 系统识别和组件路径推断

#### 3.1 自动识别系统

**方法1: URL域名映射(推荐)**
```typescript
// 从page.goto()提取URL
const url = 'https://uat-business-internet-banking.zaintl.com/cib-new/user/login';

// 根据config/system-mapping.yaml识别系统
const system = identifySystem(url); // → za-bank

// 确定组件路径
const componentBasePath = `component/${system}`;
```

**方法2: 业务模块识别**
```typescript
// 分析URL路径和组件关键词
// URL包含 /user/login + 组件包含"用户名","密码" → auth模块
// URL包含 /loan + 组件包含"提款","金额" → loan模块
```

#### 3.2 智能推断组件文件路径

```typescript
// 完整推断流程
const url = 'https://uat-business-internet-banking.zaintl.com/cib-new/user/login';
const system = identifySystem(url); // → za-bank
const componentLabel = '用戶名 忘記用戶名';
const module = identifyModule(url, componentLabel); // → auth
const function = identifyFunction(componentLabel); // → login

// 生成路径
const componentFilePath = `component/${system}/${module}/${function}.yaml`;
// 结果: component/za-bank/auth/login.yaml
```

#### 3.4 应用级组件规则（必须加载）

在识别出系统后，检查对应系统的 `component/{system}/RULES.md` 是否存在。若存在，**必须先读取该文件**，所有生成代码必须遵守其中定义的强制组件规则。

```typescript
// 示例：识别到 invest 系统后
// 读取 component/invest/RULES.md
// 遵守其中定义的退出登录、登录等强制规则
```

已知规则文件：
- `component/invest/RULES.md` — invest 投资运营系统组件规则

```typescript
// 递归加载系统所有组件
componentLoader.loadFromDirectory(`./component/${system}`, true);

// 检查组件是否已存在
const existingComponents = componentLoader.getAllComponents();
const missingComponents = identifyMissingComponents(selectors, existingComponents);
```

**组件YAML结构**:
```yaml
module: auth/login
description: 用户登录相关组件
system: za-bank
lastUpdated: 2026-03-06

components:
  Auth-login-usernameInput:
    playwright:
      primary: "page.getByRole('textbox', { name: '用戶名 忘記用戶名' })"
    description: 用户名输入框
    category: input
```

**组件命名规范 (重要！)**:

使用**目录-文件名-组件名**的组合命名规范，避免跨模块重名冲突：

**命名格式**：
```
{Module}-{FileName}-{componentName}
```

**命名规则**：
- 使用**PascalCase**风格
- 第一部分：模块目录名（如`Transfer`, `Loan`, `Auth`）
- 第二部分：文件名（如`single-transfer`, `withdrawal`, `login`）
- 第三部分：组件功能描述（如`continueButton`, `amountInput`）
- 各部分之间用**连字符(-)** 连接

**命名示例**：
```yaml
# component/bib/transfer/single-transfer.yaml
components:
  Transfer-single-transfer-continueButton:     # 转账流程继续按钮
    playwright:
      primary: "page.getByRole('button', { name: '繼續' })"
    description: 转账流程继续按钮

  Transfer-single-transfer-submitButton:       # 转账提交按钮
    playwright:
      primary: "page.getByRole('button', { name: '提交' })"
    description: 转账提交按钮

# component/bib/auth/otp.yaml
components:
  Auth-otp-continueButton:                      # OTP继续按钮
    playwright:
      primary: "page.getByRole('button', { name: '繼 續' })"
    description: OTP验证后继续按钮

  Auth-otp-confirmButton:                       # OTP确认按钮
    playwright:
      primary: "page.getByRole('button', { name: '確定' })"
    description: OTP确认按钮

# component/bib/loan/withdrawal.yaml
components:
  Loan-withdrawal-continueButton:               # 贷款提款继续按钮
    playwright:
      primary: "page.getByRole('button', { name: '繼續' })"
    description: 贷款提款流程继续按钮
```

**命名优势**：
- ✅ **避免冲突**: 不同模块的同类按钮（如continueButton）不会重名
- ✅ **清晰溯源**: 通过名称即可知道组件所属模块和文件
- ✅ **便于维护**: 组件重构时路径变更不影响其他模块
- ✅ **IDE友好**: 自动补全时能清楚区分不同模块的组件

**旧命名对比**：
```yaml
# ❌ 旧命名方式（容易冲突）
components:
  ContinueButton:      # 多个文件都有，后加载覆盖先加载
  SubmitButton:        # 太通用，容易冲突
  UsernameInput:       # 只能用于单一场景

# ✅ 新命名方式（无冲突风险）
components:
  Transfer-single-transfer-continueButton:   # 明确是转账模块的
  Auth-otp-continueButton:                   # 明确是OTP模块的
  Loan-withdrawal-continueButton:            # 明确是贷款提款的
```

### 4. 识别 API 注解（// api:xxx）

#### 4.1 注解语法

在原生代码中，可通过行内注解标记需要调用后端接口的位置：

```typescript
// api:processDrawDown
```

**格式规则**：
- 固定前缀 `// api:`，后接接口函数名（camelCase）
- 注解放在需要插入 API 调用的位置（通常在某个 UI 步骤之后）
- 接口函数名对应 `api/` 目录下已封装的函数

**示例原生代码**：
```typescript
// 原生代码中标注需要调用的接口
await page.getByText('查看進度').click();
// api:processDrawDown
await page.getByRole('cell', { name: 'E-commerce Loan' }).click();
```

#### 4.2 注解转换规则

识别到 `// api:xxx` 注解时，按以下规则转换：

**步骤1：扫描 `api/` 目录，找到对应函数**
```bash
# 查找函数定义
grep -r "export async function processDrawDown" api/
```

**步骤2：在对应位置插入 API 调用**
```typescript
// ✅ 转换后的代码
await componentClick(helpers, 'Loan-drawdown-viewProgressLink');

// ==================== N. 调用后端接口: processDrawDown ====================
await processDrawDown(request, apiConfig.processDrawDown, recordToReport);
```

**步骤3：补充必要的导入和参数**

1. **import** 中增加接口函数引入：
```typescript
import { processDrawDown } from '../../../api/eln-api';
```

2. **test 函数参数**中增加 `request` fixture：
```typescript
test('测试用例', async ({ aiAct, aiAssert, aiString, aiWaitFor, recordToReport, page, request }) => {
```

3. **顶部解构**中增加 `apiConfig`：
```typescript
const { testUser, drawdown, verification, apiConfig } = testData;
```

4. **YAML testData 节点**中增加 `apiConfig` 配置：
```yaml
testData:
  # ... 其他数据 ...

  # 后端 API 配置
  apiConfig:
    processDrawDown:
      env: sit
      loanAccountNo: "880000007647"
      approve: false
```

#### 4.3 多个 API 注解处理

原生代码中可出现多个注解，每个独立处理：

```typescript
// api:processDrawDown
// api:triggerApproval
```

转换为：
```typescript
await processDrawDown(request, apiConfig.processDrawDown, recordToReport);
await triggerApproval(request, apiConfig.triggerApproval, recordToReport);
```

对应 YAML 中每个函数独立配置：
```yaml
apiConfig:
  processDrawDown:
    env: sit
    loanAccountNo: "880000007647"
    approve: false
  triggerApproval:
    env: sit
    applicationId: "APP-001"
```

---

### 5. 识别 aiAssert 注解（// aiAssert: ...）

#### 5.1 注解语法

在原生代码中，可通过行内注解标记需要 AI 智能断言的位置：

```typescript
// aiAssert: <断言描述>
```

**格式规则**：
- 固定前缀 `// aiAssert: `，后接自然语言断言描述
- 注解放在需要插入 AI 断言的位置（通常在某个 UI 操作之后）
- 支持中英文描述，描述越清晰，AI 断言越准确
- 适合无法用 Playwright locator 直接验证的业务规则（如时间推算、数据逻辑等）

**示例原生代码**：
```typescript
await page.getByRole('tab', { name: '投资结单' }).click();
// aiAssert: 查询截止到当前每个月份的结单，例如：当前是2026年3月1号，那最新一个结单月份为202602，第二个为202601
await page.getByRole('tab', { name: '账户信息' }).click();
```

#### 5.2 注解转换规则

识别到 `// aiAssert: ...` 注解时，**断言文本必须存入 YAML `testData.assertions`，测试代码通过变量引用，禁止在 `.test.ts` 中硬编码字符串**。

**步骤1：在 YAML `testData.assertions` 下新增断言键值**

```yaml
# data/invest/customer/info-customer.yaml
testData:
  # ... 其他数据 ...

  assertions:
    stockStatementMonths: "查询截止到当前每个月份的结单，例如：当前是2026年3月1号，那最新一个结单月份为202602，第二个为202601"
```

键名规则：camelCase，语义描述断言内容（如 `stockStatementMonths`、`pageTitle`、`tableNotEmpty`）。

**步骤2：测试代码通过 `testData.assertions` 引用**

```typescript
// 顶部解构时加入 assertions
const { testUser, customer, assertions } = testData;

// ✅ 转换后的代码
await componentClick(helpers, 'Customer-info-customer-stockStatementTabRole');

// AI 断言：投资结单列表包含截止当前每月份结单
await aiAssert(assertions.stockStatementMonths);
```

**无需新增 import**：`aiAssert` 已由 test 函数参数提供，无需额外引入。

#### 5.3 多个 aiAssert 注解处理

原生代码中可出现多个注解，每个对应 YAML 中一个独立键，保持原始顺序：

```typescript
// aiAssert: 页面标题显示正确
// aiAssert: 表格数据不为空
```

YAML：
```yaml
assertions:
  pageTitle: "页面标题显示正确"
  tableNotEmpty: "表格数据不为空"
```

转换为：
```typescript
const { assertions } = testData;
await aiAssert(assertions.pageTitle);
await aiAssert(assertions.tableNotEmpty);
```

#### 5.4 注解使用建议

- **时间/日期逻辑**：`// aiAssert: 最新月份为当前月份减1，格式YYYYMM`
- **业务规则验证**：`// aiAssert: 申请状态为银行审批中`
- **下载/操作结果**：`// aiAssert: 文件下载成功，无错误提示`
- **列表完整性**：`// aiAssert: 表格包含所有必要列且无空行`

---

### 6. 生成优化代码

#### 6.1 文件头部和导入

```typescript
/**
 * [测试名称] (智能等待优化版)
 *
 * 优化内容:
 * - 智能等待替代硬编码timeout
 * - 组件驱动架构 + AI补偿
 * - 混合断言支持
 * - AI上下文增强
 * - 选择器自动发现与YAML回写
 */

import { test as base } from '@playwright/test';
import type { PlayWrightAiFixtureType } from '@midscene/web/playwright';
import { PlaywrightAiFixture } from '@midscene/web/playwright';
import {
  createHybridHelpers,
  componentClick,
  componentInput,
  componentCheck,
  componentInputOTP,
  getComponentLocator
} from '../utils/hybrid-helpers';
import {
  waitForComponentVisible
} from '../utils/smart-wait-helpers';
import { createHybridAssert } from '../utils/hybrid-assert-helpers';
import { componentLoader } from '../component/component-loader';
import { loadTestDataUnified, loadTestStepsFlatUnified } from '../utils/data-loader';
import { SPECIAL_TIMEOUTS, NETWORK_CONFIG } from '../config/test-config';
import { testStepManager } from '../utils/test-step-manager';
import { selectorFallbackRegistry } from '../utils/selector-discovery';
// 仅当原生代码含有 // api:xxx 注解时，按需导入对应函数，例如：
// import { processDrawDown } from '../api/eln-api';
```

**含 API 注解时，test 函数签名需加 `request`**：
```typescript
// ❌ 无 API 调用时
test('测试用例', async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page }) => {

// ✅ 有 API 调用时（有 // api:xxx 注解）
test('测试用例', async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page, request }) => {
```

**`aiLocate` 必须传入 `createHybridHelpers`**（选择器自动发现依赖此参数）：
```typescript
const helpers = await createHybridHelpers(page, { recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert });
```

#### 6.2 测试配置

```typescript
const test = base.extend<PlayWrightAiFixtureType>(PlaywrightAiFixture({
  waitForNetworkIdleTimeout: NETWORK_CONFIG.IDLE_TIMEOUT,
}));

// 加载测试数据
const testData = loadTestDataUnified('业务域/测试用例名');
// 例如: 'bib/withdrawal/cross-border-ecommerce-revolving'

test.beforeAll(async () => {
  componentLoader.loadFromDirectory('./component/za-bank', true);

  // AI上下文增强
  const testSteps = loadTestStepsFlatUnified('业务域/测试用例名');
  testStepManager.initialize('测试场景名称', testSteps);

  console.log(`\n📋 ${testData.metadata.testName}\n`);
});

test.beforeEach(async ({ page }) => {
  await page.goto(testData.config.baseUrl);
  await page.setViewportSize(testData.config.viewport);
});

// afterEach: 重置步骤管理器
test.afterEach(async () => {
  testStepManager.reset();
});

// afterAll: 打印选择器发现报告并将新选择器回写到YAML（选择器自动发现机制的收尾）
test.afterAll(async () => {
  selectorFallbackRegistry.printReport();
  await selectorFallbackRegistry.applyToYaml();
  selectorFallbackRegistry.clear();
});
```

#### 6.3 转换规则

| 原生操作 | 优化操作 |
|---------|---------|
| `page.getByRole(...).click()` | `await componentClick(helpers, 'ComponentName')` |
| `page.getByRole(...).fill('value')` | `await componentInput(helpers, 'ComponentName', 'value')` |
| `page.getByLabel(...).check()` | `await componentCheck(helpers, 'ComponentName')` |
| 连续OTP输入 | `await componentInputOTP(helpers, '123456')` |
| 步骤间等待 | `await waitForComponentVisible(helpers, 'NextComponentName')` |
| 浏览器下载文件 | `await triggerAndVerifyDownload(page, async () => { ... })` |

**示例**:
```typescript
// ❌ 原生代码
await page.getByRole('textbox', { name: '用戶名' }).fill('jiajun01');
await page.getByRole('button', { name: '登入' }).click();

// ✅ 优化代码
await componentInput(helpers, 'UsernameInput', testData.testUser.username);
await componentClick(helpers, 'LoginButton');
await waitForComponentVisible(helpers, 'OTPInput1'); // 等待下一个组件
```

#### 6.3.1 下载验证场景

当原生代码中存在 `page.waitForEvent('download')` 触发浏览器下载时，**必须使用 `triggerAndVerifyDownload`** 替代内联的下载验证逻辑。

**原理**：`download.path()` 为异步方法，内部等待文件完整落盘后才返回本地路径，返回非 `null` 即确认文件已写入本地磁盘，优于 `failure()` 仅检查 HTTP 层状态。

**转换规则**:

```typescript
// ❌ 原生代码（或错误的内联写法）
const downloadPromise = page.waitForEvent('download');
await page.getByText('下载').click();
const download = await downloadPromise;
const downloadFailure = await download.failure();
expect(downloadFailure).toBeNull();

// ✅ 优化代码（使用工具函数）
import { triggerAndVerifyDownload } from '../../../utils/download-helpers';

const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadLink'); }
);
console.log(`下载成功: ${downloadResult.filename} (${downloadResult.fileSize} bytes)`);
```

**可选参数**（需要更严格验证时）:
```typescript
const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadLink'); },
  {
    minFileSize: 1000,                        // 最小文件大小（字节），默认 1
    expectedExtension: /\.(pdf|xlsx|csv)$/i  // 验证文件扩展名（可选）
  }
);
```

**`triggerAndVerifyDownload` 内置验证内容**：
1. `download.path() !== null` — 文件已完整落盘
2. `fileSize >= minFileSize` — 文件内容非空（防止空文件/错误响应页）
3. `suggestedFilename` 非空 — 文件名存在
4. 可选：文件扩展名匹配

**注意**：
- 必须 `import { triggerAndVerifyDownload } from '../../../utils/download-helpers'`（路径根据目录深度调整）
- 不要再使用 `import * as fs from 'fs'` 手动处理文件
- 删除所有 `download.failure()`、`fs.statSync()` 等内联验证代码

#### 6.4 智能等待策略

在关键操作后插入等待:

**步骤间等待下一个组件** (推荐策略):
```typescript
await componentClick(helpers, 'LoginButton');
await waitForComponentVisible(helpers, 'OTPInput1');
```

**使用场景**:
- 点击按钮后等待下一个页面/组件出现
- 输入表单后等待提交结果
- 任何需要等待UI状态变化的场景

#### 6.5 混合断言使用

**`toBeVisible` — 验证元素可见（传组件名）**:

```typescript
const hybridAssert = createHybridAssert(helpers);

// 直接传组件名，Playwright断言失败时自动用组件description作为AI提示词
await hybridAssert.toBeVisible('Customer-info-customer-fundCounterAccountCell');
await hybridAssert.toBeVisible('Customer-info-customer-accountTypeCell');
```

- 无需提前调用 `getComponentLocator`，无需传 `errorMsg`
- AI 回退时自动使用组件 YAML 中的 `description` 字段（如 `"基金柜台账号（基金账户）" should be visible on the page`）

**`toContainText` — 验证元素包含文本**:

```typescript
const hybridAssert = createHybridAssert(helpers);

// 从组件库获取定位器
const tableLocator = getComponentLocator(helpers, 'ApplicationRecordsTable');

// 混合断言 - 失败时自动AI补偿
await hybridAssert.toContainText(tableLocator, testData.verification.expectedStatus);
```

#### 6.6 用例末尾必须追加 `aiAct("执行结束")`

**所有生成的测试用例，最后一个业务步骤之后必须追加：**

```typescript
  await aiAct("执行结束");
});
```

**原因**：Midscene 报告的**录像回放功能**依赖至少一次 AI 操作调用来触发截图序列的录制。如果整个用例全部使用 Playwright 原生方式执行（无任何 `aiAct/aiAssert` 等 AI 调用），报告中只会有静态截图，无法生成可播放的录像。追加 `await aiAct("执行结束")` 可保证报告录像始终可播放。

**位置规则**：
- 放在所有业务步骤（包括 API 调用）的**最后一步**
- 放在 `});` 结束符之前
- 不受 API 注解影响，有无 `// api:xxx` 均需添加

**示例**：
```typescript
  // ==================== 最后一步业务操作 ====================
  await hybridAssert.toContainText(dialogLocator, verification.expectedAmount);

  // 如有 API 调用，在 API 调用之后
  await processDrawDown(request, apiConfig.processDrawDown, recordToReport);

  await aiAct("执行结束");  // ← 必须，保证 Midscene 报告可播放
});
```

---

### 7. 生成测试数据配置

#### 7.1 目录结构规范

```
data/
├── bib/                          # 企业网银系统
│   ├── application/               # 贷款申请
│   │   └── full-process.yaml
│   └── withdrawal/                # 贷款提款
│       └── cross-border-ecommerce-revolving.yaml
├── ops/                       # 运营后管系统
└── README.md

testcase-optimized/
└── bib/                          # 与data目录1:1对应
    └── withdrawal/
        └── cross-border-ecommerce-revolving.test.ts
```

**命名规范**: 小写英文+连字符(kebab-case),体现业务特征

#### 7.2 统一YAML结构

```yaml
# ==================== 元数据 ====================
metadata:
  testName: 跨境电商循环贷款提款流程测试
  businessDomain: bib/withdrawal
  description: 包含登录、OTP验证、导航、提款申请的完整流程
  environment: SIT
  totalSteps: 27
  lastUpdated: 2026-03-06

# ==================== 测试配置 ====================
config:
  baseUrl: https://example.com
  viewport:
    width: 1541
    height: 911

# ==================== 测试数据 ====================
testData:
  testUser:
    username: user123
    password: Pass@123
    verification:
      smsCode: "123456"

  loanApplication:
    accountNumber: "880000000419"
    withdrawal:
      amount: 13000
      currency: USD

  # 后端 API 配置（仅当原生代码含 // api:xxx 注解时添加）
  apiConfig:
    processDrawDown:          # 函数名与注解中一致
      env: sit
      loanAccountNo: "880000000419"
      approve: false

  # AI 断言文本（仅当原生代码含 // aiAssert: 注解时添加）
  # 键名使用 camelCase，语义描述断言内容
  assertions:
    stockStatementMonths: "查询截止到当前每个月份的结单，例如：当前是2026年3月1号，那最新一个结单月份为202602，第二个为202601"

# ==================== 测试步骤 ====================
# 字段说明：
# - index: 步骤序号（必需，用于排序和上下文构建）
# - componentName: 组件名称（必需，用于识别和匹配步骤）
# - action: 操作类型（必需，可选值：click/input/check，用于构建AI提示词）
# - selector: Playwright选择器（必需，用于AI提示词）
# - description: 步骤描述（可选，用于文档说明）
testSteps:
  # 登录阶段
  loginSteps:
    - index: 1
      componentName: UsernameInput
      action: input
      selector: "page.getByRole('textbox', { name: '用戶名 忘記用戶名' })"
      description: 输入用户名

    - index: 2
      componentName: PasswordInput
      action: input
      selector: "page.getByRole('textbox', { name: '密碼 忘記密碼' })"
      description: 输入密码

    - index: 3
      componentName: LoginButton
      action: click
      selector: "page.getByRole('button', { name: '登入', exact: true })"
      description: 点击登录按钮

  # OTP验证阶段
  otpVerificationSteps:
    - index: 4
      componentName: OTPInput1
      action: input
      selector: "page.getByRole('spinbutton', { name: 'Please enter OTP character 1' })"
      description: 输入OTP验证码第1位

    - index: 5
      componentName: OTPInput2
      action: input
      selector: "page.getByRole('spinbutton', { name: 'Please enter OTP character 2' })"
      description: 输入OTP验证码第2位

  # 导航到贷款产品
  navigationSteps:
    - index: 6
      componentName: LoanMenu
      action: click
      selector: "page.locator('div').filter({ hasText: /^貸款$/ }).nth(1)"
      description: 点击贷款菜单

  # 提款申请流程
  withdrawalApplicationSteps:
    - index: 7
      componentName: LoanAccountLink
      action: click
      selector: "page.locator('a').filter({ hasText: '跨境電商循環貸款' }).getByRole('button')"
      description: 点击贷款账户提款按钮

# ==================== 敏感字段 ====================
sensitiveFields:
  - testData.testUser.password
  - testData.testUser.verification
```

#### 7.3 testSteps格式规范 ⚠️

**必须使用对象分组结构**,按业务阶段组织步骤:

```yaml
testSteps:
  loginSteps:              # 按阶段分组
    - index: 1             # 全局递增序号
      componentName: UsernameInput
      action: input
      description: 输入用户名     # 中文业务描述，直接用于AI提示词

  otpVerificationSteps:    # 下一阶段
    - index: 4
      componentName: OTPInput1
      action: input
      description: 输入OTP验证码第1位
```

**分组命名**: 驼峰命名+`Steps`后缀,体现业务阶段
**必需字段**: `index`, `componentName`, `action`
**推荐字段**: `description`（description已含动词前缀则不重复拼接，如"点击登录按钮"不会变成"点击 点击登录按钮"）

#### 7.4 AI Prompt构建策略 🤖

**多层次上下文增强**,让AI准确理解业务意图:

**Prompt结构**:
```
[第1层] 完整测试流程上下文 (testStepManager提供)
  - 测试用例名称
  - 已执行步骤列表（使用description构建，input类型追加实际输入值）
  - 当前步骤说明

[第2层] 当前操作业务描述 (优先级最高)
  - Click on "贷款账户提款按钮"
  - Type "20000" into "提款金额输入框"

[第3层] 技术定位信息 (辅助定位)
  - Technical selector: page.locator('a').filter(...)
```

**步骤描述生成规则**:
- 优先使用 `description` 字段作为元素描述
- `description` 已包含动词前缀时直接使用，避免重复（如"点击登录按钮"不拼接为"点击 点击登录按钮"）
- `input` 类型追加实际输入值，如：`输入用户名，值为"kyc81240lp"`

**完整Prompt示例**:
```
我的测试用例【贷款提款申请完整流程】有以下步骤：
1、输入用户名，值为"kyc81240lp"
2、输入密码，值为"Aa@123123"
3、点击登录按钮
4、输入OTP验证码第1位，值为"1"
...
10、点击OTP继续按钮

当前执行步骤：点击OTP继续按钮

当前操作详情：Click on "OTP验证后继续按钮"
Technical selector: page.getByRole('button', { name: '繼續' })
```

**关键优化点**:
1. **业务描述优先**: AI首先理解"要做什么"，无 selector 干扰
2. **输入值可见**: input 步骤明确展示填入了什么值，帮助AI判断步骤是否已执行
3. **完整上下文**: 提供之前所有步骤，帮助AI理解当前所处阶段

### 8. 输出优化代码

```typescript
// 保存测试代码 (与data/目录1:1对应)
const outputPath = 'testcase-optimized/业务域/测试用例名.test.ts';
await writeFile(outputPath, optimizedCode);

// 保存测试数据
const dataPath = 'data/业务域/测试用例名.yaml';
await writeFile(dataPath, unifiedTestScenarioYaml);
```

**导入路径调整**:
- 根目录: `'../utils/...'`
- 一级子目录: `'../../utils/...'`
- 二级子目录: `'../../../utils/...'`

---

## ✅ 转换检查清单

**基础转换**:
- ✅ 所有UI选择器已提取到组件库
- ✅ 所有硬编码数据已提取到统一YAML
- ✅ 数据与步骤合并到单个YAML文件
- ✅ YAML文件按业务域组织
- ✅ 文件名体现业务特征(非test1/demo)
- ✅ 使用组件驱动方法(`componentClick/Input/Check`)
- ✅ 使用新的`loadTestDataUnified`加载函数
- ✅ 文件导入语句完整正确
- ✅ metadata中包含businessDomain字段

**高级优化**:
- ✅ testcase-optimized/ 和 data/ 目录1:1对应
- ✅ 导入路径根据目录深度调整
- ✅ 添加步骤间等待`waitForComponentVisible(helpers, 'NextComponentName')`
- ✅ 初始化testStepManager提供AI上下文
- ✅ testSteps使用对象分组结构,每步包含`description`字段
- ✅ 组件定义包含清晰的`description`字段(用于AI prompt)
- ✅ 可见性断言使用 `hybridAssert.toBeVisible('组件名')`，直接传组件名，无需 `getComponentLocator` 和 `errorMsg`
- ✅ 文本断言使用 `hybridAssert.toContainText(locator, text)` + `getComponentLocator`，无需传 `errorMsg`
- ✅ 所有断言中的组件已在组件库中定义，且 `description` 字段语义清晰（供 AI 回退使用）
- ✅ 使用`waitForComponentVisible`作为主要等待策略

**选择器自动发现（必须，所有用例均需包含）**:
- ✅ import `selectorFallbackRegistry` from `utils/selector-discovery`
- ✅ test 函数签名包含 `aiLocate` fixture 参数
- ✅ `createHybridHelpers` 调用中传入 `aiLocate`（格式：`{ recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert }`）
- ✅ `afterEach` 中调用 `testStepManager.reset()`
- ✅ `afterAll` 中按顺序调用：`selectorFallbackRegistry.printReport()` → `await selectorFallbackRegistry.applyToYaml()` → `selectorFallbackRegistry.clear()`

**下载验证**（原生代码含 `page.waitForEvent('download')` 时）:
- ✅ import `triggerAndVerifyDownload` from `utils/download-helpers`
- ✅ 使用 `triggerAndVerifyDownload(page, async () => { ... })` 替代内联下载逻辑
- ✅ 不使用 `import * as fs from 'fs'` 手动验证文件
- ✅ 不使用 `download.failure()` 作为唯一验证手段

**aiAct 使用限制**:
- ✅ 业务步骤中禁止直接调用 `await aiAct(...)` 操作 UI（应使用 `componentClick/Input/Check`）
- ✅ 用例末尾仅允许保留 `await aiAct("执行结束")` 一处（用于 Midscene 报告录像）

**断言方式限制（重要！）**:
- ✅ **禁止在测试文件中直接使用 `expect()` 进行断言**，包括 `expect(locator).toContainText()`、`expect(locator).toMatchAriaSnapshot()` 等所有 `expect()` 用法
- ✅ 所有断言必须使用 `hybridAssert` 封装方法：
  - 元素可见 → `await hybridAssert.toBeVisible('组件名')`
  - 文本包含 → `await hybridAssert.toContainText(locator, text)`
  - 元素数量 → `await hybridAssert.toHaveCount(locator, count)`
  - AI智能断言 → `await aiAssert(assertions.xxx)`（文本存入 YAML `testData.assertions`）
- ✅ `import` 语句中不引入 `expect`（`import { test as base } from '@playwright/test'`，无 `expect`）
- ✅ 若需验证已选中状态等特殊状态，为对应状态新增独立组件（如 `Fund-order-detailOrderTabSelected`），使用 `hybridAssert.toBeVisible` 验证

**后端 API 调用**（原生代码含 `// api:xxx` 注解时）:
- ✅ 扫描 `api/` 目录确认函数已存在
- ✅ import 中引入对应 API 函数
- ✅ test 函数参数增加 `request` fixture
- ✅ 顶部解构包含 `apiConfig`
- ✅ YAML `testData` 节点下新增 `apiConfig` 配置段（函数名与注解一致）
- ✅ API 调用传入 `recordToReport` 以记录到 Midscene 报告

**aiAssert 注解**（原生代码含 `// aiAssert: ...` 注解时）:
- ✅ 识别原生代码中所有 `// aiAssert:` 注解行
- ✅ 断言文本存入 YAML `testData.assertions.{camelCaseKey}`，禁止在 `.test.ts` 中硬编码字符串
- ✅ 测试代码解构 `assertions` 并通过 `assertions.xxx` 引用，如 `await aiAssert(assertions.stockStatementMonths)`
- ✅ 无需新增 import（aiAssert 已由 test 函数参数提供）

**Midscene 报告**:
- ✅ 用例末尾（所有业务步骤之后）追加 `await aiAct("执行结束")`，保证报告录像可播放

---

## 📚 示例参考

- **原生代码**: `testcase-native/playwright-native.test.ts`
- **优化代码**: `testcase-optimized/playwright-native2-optimized.test.ts`
- **含API调用的优化代码**: `testcase-optimized/bib/loan/drawdown.test.ts`
- **API封装目录**: `api/eln-api.ts`（`processDrawDown` 封装示例）
- **组件库**: `component/za-bank/`
- **系统映射**: `config/system-mapping.yaml`
- **测试数据**: `data/bib/loan/drawdown.yaml`（含 `apiConfig` 配置示例）
- **工具方法**: `utils/hybrid-helpers.ts`, `utils/smart-wait-helpers.ts`

---

## 📝 注意事项

1. **组件命名规范（重要！）**:
   - **必须使用** `{Module}-{FileName}-{componentName}` 格式
   - 示例：`Transfer-single-transfer-continueButton`、`Auth-otp-confirmButton`
   - 目的：避免跨模块组件重名冲突
   - 检查：转换前先扫描现有组件名，确保不重复

2. **组件复用**:
   - 优先使用现有组件，避免重复定义
   - 相同业务语义的组件应复用同一定义
   - 加载前检查组件库是否已存在该组件

3. **命名一致性**:
   - 组件命名包含完整路径信息
   - 与业务语义保持一致
   - 使用PascalCase风格

4. **等待策略**:
   - 根据场景选择合适等待方法
   - 优先使用`waitForComponentVisible`
   - 关键操作后添加智能等待

5. **数据安全**:
   - 标记敏感字段（密码、金额等）
   - 使用环境变量管理测试账号

6. **配置驱动**:
   - 使用配置常量替代魔法数字
   - 统一从`config/test-config.ts`读取配置

---

## 🔧 故障排除

### 组件命名冲突
**问题**: 后加载的组件覆盖先加载的组件
**原因**: 多个文件定义了相同名称的组件（如`ContinueButton`）
**解决**:
1. 检查重名组件：
   ```bash
   cd component/bib && grep -h "^  [A-Z].*:" ./**/*.yaml | sed 's/:.*//g' | sed 's/^  //g' | sort | uniq -d
   ```
2. 使用新命名规范重命名组件：
   - `ContinueButton` → `Auth-otp-continueButton` (OTP模块)
   - `ContinueButton` → `Transfer-single-transfer-continueButton` (转账模块)
3. 更新所有引用该组件的测试文件和数据文件

### 组件定位失败
- 检查组件库选择器是否正确
- 验证AI补偿提示词是否清晰
- 确认页面状态是否符合预期
- 检查组件是否被正确加载（`componentLoader.getComponentCount()`）

### 等待超时
- 调整配置中心超时设置（`ELEMENT_TIMEOUTS.VISIBLE` 控制元素等待，`ELEMENT_TIMEOUTS.ACTION` 控制操作执行）
- `ELEMENT_TIMEOUTS.ACTION`（默认8秒）：`click/fill/check` 操作超时后自动回退AI，避免被弹窗阻挡时长时间卡住
- 检查网络连接和页面加载速度
- 确认等待的组件是否存在于当前页面

### 意外弹窗导致操作卡住
**场景**: 执行 `componentClick` 后，页面出现意外弹窗（如会话过期、活动通知、系统提示），导致后续 `waitForComponentVisible` 等待超时触发AI补偿
**AI补偿策略**（ai-retry-compensation.ts）:
1. **优先检测并关闭弹窗**（最高优先级）：AI截图分析，识别并关闭弹窗/遮罩/底部抽屉等
2. **重试原操作**：关闭弹窗后检查上一步是否生效，未生效则重新执行
3. **验证目标元素**：确认目标组件已可见

**触发条件**: `waitForComponentVisible` 三级策略（Playwright等待 → AI等待 → AI补偿重试）

### 工具方法缺失
- 参考现有方法实现模式
- 在正确文件中添加方法
- 更新类型定义文件
- 确保导入路径正确
