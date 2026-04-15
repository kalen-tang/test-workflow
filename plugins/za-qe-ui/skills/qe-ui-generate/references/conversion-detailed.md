# 转换流程详细说明

## 步骤3：系统识别和组件路径推断

### 3.1 自动识别系统

**方法1: URL域名映射（推荐）**
```typescript
const url = 'https://uat-business-internet-banking.zaintl.com/cib-new/user/login';
const system = identifySystem(url); // → za-bank
const componentBasePath = `component/${system}`;
```

**方法2: 业务模块识别**
```typescript
// URL包含 /user/login + 组件含"用户名","密码" → auth模块
// URL包含 /loan + 组件含"提款","金额" → loan模块
```

### 3.2 智能推断组件文件路径

```typescript
const url = 'https://uat-business-internet-banking.zaintl.com/cib-new/user/login';
const system = identifySystem(url); // → za-bank
const componentLabel = '用戶名 忘記用戶名';
const module = identifyModule(url, componentLabel); // → auth
const func = identifyFunction(componentLabel); // → login

const componentFilePath = `component/${system}/${module}/${func}.yaml`;
// 结果: component/za-bank/auth/login.yaml
```

### 3.4 应用级组件规则

识别出系统后，检查 `component/{system}/RULES.md` 是否存在，若存在**必须先读取**，所有生成代码须遵守其中的强制规则。

已知规则文件：
- `component/invest/RULES.md` — invest 投资运营系统组件规则

---

## 步骤4：识别 API 注解（// api:xxx）

### 注解语法

```typescript
// api:processDrawDown
```

格式：`// api:` 前缀 + 接口函数名（camelCase），注解放在需要插入 API 调用的位置。

### 转换规则

**步骤1：扫描 `api/` 目录确认函数存在**
```bash
grep -r "export async function processDrawDown" api/
```

**步骤2：在对应位置插入调用**
```typescript
await componentClick(helpers, 'Loan-drawdown-viewProgressLink');

// ==================== N. 调用后端接口: processDrawDown ====================
await processDrawDown(request, apiConfig.processDrawDown, recordToReport);
```

**步骤3：补充导入和参数**
```typescript
// import 中增加
import { processDrawDown } from '../../../api/eln-api';

// test 函数参数增加 request
test('测试用例', async ({ ..., page, request }) => {

// 顶部解构增加 apiConfig
const { testUser, drawdown, verification, apiConfig } = testData;
```

**YAML testData 增加 apiConfig**:
```yaml
testData:
  apiConfig:
    processDrawDown:
      env: sit
      loanAccountNo: "880000007647"
      approve: false
```

### 多个 API 注解

```typescript
// api:processDrawDown
// api:triggerApproval
```
对应 YAML 中各自独立配置段，测试代码中按顺序调用。

---

## 步骤5：识别 aiAssert 注解（// aiAssert: ...）

### 注解语法

```typescript
// aiAssert: <断言描述>
```

适合无法用 Playwright locator 直接验证的业务规则（如时间推算、数据逻辑等）。

### 转换规则

**断言文本必须存入 YAML `testData.assertions`，禁止在 `.test.ts` 中硬编码字符串。**

**YAML 增加 assertions**:
```yaml
testData:
  assertions:
    stockStatementMonths: "查询截止到当前每个月份的结单，例如：当前是2026年3月1号，那最新一个结单月份为202602，第二个为202601"
```

**测试代码通过变量引用**:
```typescript
const { testUser, customer, assertions } = testData;
await aiAssert(assertions.stockStatementMonths);
```

键名规则：camelCase，语义描述断言内容。

### 注解使用建议

- 时间/日期逻辑：`// aiAssert: 最新月份为当前月份减1，格式YYYYMM`
- 业务规则验证：`// aiAssert: 申请状态为银行审批中`
- 下载/操作结果：`// aiAssert: 文件下载成功，无错误提示`
- 列表完整性：`// aiAssert: 表格包含所有必要列且无空行`

---

## 步骤6：生成优化代码

### 6.1 文件头部和完整导入

```typescript
/**
 * [测试名称] (智能等待优化版)
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
import { waitForComponentVisible } from '../utils/smart-wait-helpers';
import { createHybridAssert } from '../utils/hybrid-assert-helpers';
import { componentLoader } from '../component/component-loader';
import { loadTestDataUnified, loadTestStepsFlatUnified } from '../utils/data-loader';
import { SPECIAL_TIMEOUTS, NETWORK_CONFIG } from '../config/test-config';
import { testStepManager } from '../utils/test-step-manager';
import { selectorFallbackRegistry } from '../utils/selector-discovery';
// 仅当原生代码含 // api:xxx 注解时导入对应函数
// import { processDrawDown } from '../api/eln-api';
```

**含 API 注解时 test 函数签名需加 `request`**：
```typescript
test('测试用例', async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page, request }) => {
```

**`aiLocate` 必须传入 `createHybridHelpers`**:
```typescript
const helpers = await createHybridHelpers(page, { recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert });
```

### 6.2 测试配置完整模板

```typescript
const test = base.extend<PlayWrightAiFixtureType>(PlaywrightAiFixture({
  waitForNetworkIdleTimeout: NETWORK_CONFIG.IDLE_TIMEOUT,
}));

const testData = loadTestDataUnified('业务域/测试用例名');

test.beforeAll(async () => {
  componentLoader.loadFromDirectory('./component/za-bank', true);
  const testSteps = loadTestStepsFlatUnified('业务域/测试用例名');
  testStepManager.initialize('测试场景名称', testSteps);
  console.log(`\n📋 ${testData.metadata.testName}\n`);
});

test.beforeEach(async ({ page }) => {
  await page.goto(testData.config.baseUrl);
  await page.setViewportSize(testData.config.viewport);
});

test.afterEach(async () => {
  testStepManager.reset();
});

test.afterAll(async () => {
  selectorFallbackRegistry.printReport();
  await selectorFallbackRegistry.applyToYaml();
  selectorFallbackRegistry.clear();
});
```

### 6.3 下载验证场景

当原生代码含 `page.waitForEvent('download')` 时，**必须使用 `triggerAndVerifyDownload`**：

```typescript
import { triggerAndVerifyDownload } from '../../../utils/download-helpers';

const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadLink'); }
);
console.log(`下载成功: ${downloadResult.filename} (${downloadResult.fileSize} bytes)`);
```

可选参数（更严格验证）:
```typescript
const downloadResult = await triggerAndVerifyDownload(
  page,
  async () => { await componentClick(helpers, 'ComponentName-downloadLink'); },
  {
    minFileSize: 1000,
    expectedExtension: /\.(pdf|xlsx|csv)$/i
  }
);
```

**内置验证**：文件落盘（`path() !== null`）、文件非空（`fileSize >= minFileSize`）、文件名存在。

---

## 步骤7：生成测试数据配置

### 7.2 完整统一 YAML 结构

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
    processDrawDown:
      env: sit
      loanAccountNo: "880000000419"
      approve: false

  # AI 断言文本（仅当原生代码含 // aiAssert: 注解时添加）
  assertions:
    stockStatementMonths: "查询截止到当前每个月份的结单..."

# ==================== 测试步骤 ====================
testSteps:
  loginSteps:
    - index: 1
      componentName: Auth-login-usernameInput
      action: input
      selector: "page.getByRole('textbox', { name: '用戶名 忘記用戶名' })"
      description: 输入用户名

    - index: 2
      componentName: Auth-login-passwordInput
      action: input
      selector: "page.getByRole('textbox', { name: '密碼 忘記密碼' })"
      description: 输入密码

  otpVerificationSteps:
    - index: 3
      componentName: Auth-otp-otpInput1
      action: input
      selector: "page.getByRole('spinbutton', { name: 'Please enter OTP character 1' })"
      description: 输入OTP验证码第1位

# ==================== 敏感字段 ====================
sensitiveFields:
  - testData.testUser.password
  - testData.testUser.verification
```

### 7.3 testSteps 格式要求

- 必须使用对象分组结构，按业务阶段组织
- 分组命名：驼峰命名 + `Steps` 后缀
- 必需字段：`index`（全局递增）、`componentName`、`action`
- 推荐字段：`description`（中文业务描述，直接用于AI提示词）

---

## 步骤8：AI Prompt 构建策略

多层次上下文增强，让 AI 准确理解业务意图：

```
[第1层] testStepManager 提供完整测试流程上下文
[第2层] 当前操作业务描述（优先级最高）
[第3层] 技术定位信息（辅助）
```

完整 Prompt 示例：
```
我的测试用例【贷款提款申请完整流程】有以下步骤：
1、输入用户名，值为"kyc81240lp"
2、输入密码，值为"Aa@123123"
3、点击登录按钮
...
当前执行步骤：点击OTP继续按钮
当前操作详情：Click on "OTP验证后继续按钮"
Technical selector: page.getByRole('button', { name: '繼續' })
```
