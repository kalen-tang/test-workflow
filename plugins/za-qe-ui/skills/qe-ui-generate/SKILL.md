---
name: qe-ui-generate
description: 将Playwright录制的原生测试代码转换为混合架构的优化测试脚本。用于：转换原生录制代码、生成组件YAML、生成测试数据YAML、完整转换工作流。当用户说"转换测试"、"优化测试代码"、"生成测试脚本"、"把录制的代码转成优化版"、"convert test"、"generate test"时触发。从testcase-native读取，输出到testcase-optimized，支持组件驱动、智能等待、AI上下文增强、混合断言、API注解、aiAssert注解处理。
metadata:
  category: ui-testing
  version: 2.0.0
---

# Playwright原生代码优化转换器

## 核心功能

将Playwright Codegen录制的原生代码转换为项目优化架构：

- **组件驱动**: 选择器提取到YAML组件库，使用 `componentClick/Input/Check`
- **智能等待**: `page.waitForTimeout()` → `waitForComponentVisible()`
- **混合架构**: Playwright优先 → Midscene AI补偿
- **数据分离**: 硬编码数据提取到YAML配置
- **AI上下文增强**: testStepManager 提供多层次上下文
- **混合断言**: `createHybridAssert` 断言失败时自动AI补偿
- **选择器自动发现**: `selectorFallbackRegistry` 运行时回写YAML

---

## 转换流程

### 步骤1：读取原始文件

从 `testcase-native/{system}/{module}/{name}.test.ts` 读取原生代码。

### 步骤2：识别系统和模块

从 `page.goto()` URL 推断系统标识：
- `uat-business-internet-banking.zaintl.com` → `za-bank`
- 其他系统参考 `config/system-mapping.yaml`

**CRITICAL**: 识别系统后，检查 `component/{system}/RULES.md` 是否存在，若存在**必须先读取**并遵守所有强制规则。
- 已知规则文件：`component/invest/RULES.md`

### 步骤3：识别特殊注解

扫描原生代码中的注解并按规则转换（详见 `references/conversion-detailed.md`）：

| 注解 | 作用 | 转换目标 |
|------|------|---------|
| `// api:funcName` | 调用后端接口 | 插入 API 调用，YAML 增加 `apiConfig` 段 |
| `// aiAssert: 描述` | AI智能断言 | 断言文本存入 YAML `testData.assertions`，代码引用变量 |

### 步骤4：生成组件 YAML

**命名规范（必须遵守）**: `{Module}-{FileName}-{componentName}`
```
Transfer-single-transfer-continueButton   ✅ (模块-文件名-功能)
ContinueButton                            ❌ (太通用，易冲突)
```

**组件结构**:
```yaml
components:
  Auth-login-usernameInput:
    playwright:
      primary: "page.getByRole('textbox', { name: '用戶名 忘記用戶名' })"
    description: 用户名输入框
    category: input
```

### 步骤5：生成测试脚本

**操作转换对照**:

| 原生操作 | 优化操作 |
|---------|---------|
| `page.getByRole(...).click()` | `await componentClick(helpers, 'ComponentName')` |
| `page.getByRole(...).fill('val')` | `await componentInput(helpers, 'ComponentName', 'val')` |
| `page.getByLabel(...).check()` | `await componentCheck(helpers, 'ComponentName')` |
| 连续6位OTP输入 | `await componentInputOTP(helpers, '123456')` |
| 步骤间等待 | `await waitForComponentVisible(helpers, 'NextComponent')` |
| `page.waitForEvent('download')` | `await triggerAndVerifyDownload(page, async () => {...})` |

**CRITICAL 规则**:
1. **禁止在业务步骤中直接 `await aiAct(...)`**，必须用 `componentClick/Input/Check`
2. **用例末尾必须追加** `await aiAct("执行结束")`（保证Midscene报告录像可播放）
3. **禁止使用 `expect()`**，所有断言必须通过 `hybridAssert`
4. **aiAssert 禁止硬编码字符串**，必须通过 `assertions.xxx` 变量引用

**断言写法**:
```typescript
const hybridAssert = createHybridAssert(helpers);

// 可见性断言（直接传组件名）
await hybridAssert.toBeVisible('ComponentName');

// 文本断言（传 Locator）
const locator = getComponentLocator(helpers, 'ComponentName');
await hybridAssert.toContainText(locator, testData.verification.expectedText);

// AI 断言（文本必须来自 YAML）
await aiAssert(assertions.stockStatementMonths);
```

**test 函数必须包含的 fixture 参数**:
```typescript
// 无 API 调用
async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page })

// 有 // api:xxx 注解
async ({ aiAct, aiAssert, aiLocate, aiString, aiWaitFor, recordToReport, page, request })
```

**createHybridHelpers 必须传入 aiLocate**:
```typescript
const helpers = await createHybridHelpers(page, { recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert });
```

### 步骤6：生成测试数据 YAML

文件路径与测试脚本 1:1 对应：
- 测试脚本：`testcase-optimized/bib/withdrawal/xxx.test.ts`
- 数据文件：`data/bib/withdrawal/xxx.yaml`

YAML 必须包含：`metadata`、`config`、`testData`、`testSteps`（对象分组，按业务阶段）。

详细 YAML 结构模板见 `references/conversion-detailed.md`。

### 步骤7：输出文件

```
testcase-optimized/{system}/{module}/{name}.test.ts
data/{system}/{module}/{name}.yaml
component/{system}/{module}/{file}.yaml   (新增或更新组件)
```

导入路径规则：
- 根目录 `testcase-optimized/`：`'../utils/...'`
- 一级子目录：`'../../utils/...'`
- 二级子目录：`'../../../utils/...'`

---

## 完整导入模板

```typescript
import { test as base } from '@playwright/test';
import type { PlayWrightAiFixtureType } from '@midscene/web/playwright';
import { PlaywrightAiFixture } from '@midscene/web/playwright';
import {
  createHybridHelpers, componentClick, componentInput,
  componentCheck, componentInputOTP, getComponentLocator
} from '../utils/hybrid-helpers';
import { waitForComponentVisible } from '../utils/smart-wait-helpers';
import { createHybridAssert } from '../utils/hybrid-assert-helpers';
import { componentLoader } from '../component/component-loader';
import { loadTestDataUnified, loadTestStepsFlatUnified } from '../utils/data-loader';
import { NETWORK_CONFIG } from '../config/test-config';
import { testStepManager } from '../utils/test-step-manager';
import { selectorFallbackRegistry } from '../utils/selector-discovery';
// 含 // api:xxx 注解时按需导入：
// import { processDrawDown } from '../api/eln-api';
```

**标准生命周期钩子**:
```typescript
test.beforeAll(async () => {
  componentLoader.loadFromDirectory('./component/za-bank', true);
  const testSteps = loadTestStepsFlatUnified('业务域/测试用例名');
  testStepManager.initialize('测试场景名称', testSteps);
});

test.beforeEach(async ({ page }) => {
  await page.goto(testData.config.baseUrl);
  await page.setViewportSize(testData.config.viewport);
});

test.afterEach(async () => { testStepManager.reset(); });

test.afterAll(async () => {
  selectorFallbackRegistry.printReport();
  await selectorFallbackRegistry.applyToYaml();
  selectorFallbackRegistry.clear();
});
```

---

## 故障排除

**组件命名冲突**（多文件重名后加载会覆盖前者）:
```bash
cd component/bib && grep -h "^  [A-Z].*:" ./**/*.yaml | sed 's/:.*//g' | sed 's/^  //g' | sort | uniq -d
```
解决：按 `{Module}-{FileName}-{componentName}` 规范重命名。

**下载验证**（原生代码含 `page.waitForEvent('download')` 时必须替换）:
```typescript
import { triggerAndVerifyDownload } from '../../../utils/download-helpers';
const result = await triggerAndVerifyDownload(page, async () => {
  await componentClick(helpers, 'ComponentName-downloadButton');
});
```
内置验证：文件落盘、文件非空、文件名存在。详细用法见 `references/conversion-detailed.md`。

**意外弹窗**：`waitForComponentVisible` 超时时 AI 补偿会优先检测并关闭弹窗再重试原操作。

**`ELEMENT_TIMEOUTS.ACTION`（默认8秒）**：`click/fill/check` 超时后自动回退 AI，避免弹窗阻挡时长时间卡住。

---

## 参考资源

- **详细转换步骤 + 代码模板**: `references/conversion-detailed.md`
- **转换检查清单（30+项）**: `references/conversion-checklist.md`
- **原生代码示例**: `testcase-native/`
- **优化代码示例**: `testcase-optimized/bib/loan/drawdown.test.ts`
- **组件库**: `component/za-bank/`、`component/invest/`
- **测试数据**: `data/`
- **工具方法**: `utils/hybrid-helpers.ts`、`utils/smart-wait-helpers.ts`、`utils/download-helpers.ts`
