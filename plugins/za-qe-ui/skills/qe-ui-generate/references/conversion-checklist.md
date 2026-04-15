# 转换检查清单

执行转换前逐项核对，确保生成代码符合规范。

## 基础转换

- [ ] 所有UI选择器已提取到组件库 YAML
- [ ] 所有硬编码数据已提取到统一 YAML
- [ ] 数据与步骤合并到单个 YAML 文件
- [ ] YAML 文件按业务域组织（`data/{system}/{module}/`）
- [ ] 文件名体现业务特征（kebab-case，非 test1/demo）
- [ ] 使用组件驱动方法（`componentClick/Input/Check`）
- [ ] 使用 `loadTestDataUnified` 加载函数
- [ ] 文件导入语句完整正确
- [ ] `metadata` 中包含 `businessDomain` 字段

## 高级优化

- [ ] `testcase-optimized/` 和 `data/` 目录 1:1 对应
- [ ] 导入路径根据目录深度调整（一级 `../../`，二级 `../../../`）
- [ ] 步骤间添加 `waitForComponentVisible(helpers, 'NextComponentName')`
- [ ] `beforeAll` 初始化 `testStepManager` 提供 AI 上下文
- [ ] `testSteps` 使用对象分组结构，每步包含 `description` 字段
- [ ] 组件定义包含清晰的 `description` 字段（用于 AI prompt）
- [ ] 可见性断言使用 `hybridAssert.toBeVisible('组件名')`，直接传组件名
- [ ] 文本断言使用 `hybridAssert.toContainText(locator, text)` + `getComponentLocator`
- [ ] 断言组件已在组件库中定义，`description` 字段语义清晰

## 选择器自动发现（所有用例必须包含）

- [ ] `import { selectorFallbackRegistry } from '../utils/selector-discovery'`（根据目录深度调整层级）
- [ ] test 函数签名包含 `aiLocate` fixture 参数
- [ ] **`createHybridHelpers` 调用必须传入 `aiLocate`**（缺少则 selector-discovery 机制完全失效）
  ```typescript
  const helpers = await createHybridHelpers(page, { recordToReport, aiAct, aiLocate, aiString, aiWaitFor, aiAssert });
  ```
- [ ] `afterEach` 调用 `testStepManager.reset()`
- [ ] `afterAll` 按顺序调用：`printReport()` → `applyToYaml()` → `clear()`

## 下载验证（原生代码含 `page.waitForEvent('download')` 时）

- [ ] `import { triggerAndVerifyDownload } from '../utils/download-helpers'`（根据目录深度调整层级）
- [ ] 使用 `triggerAndVerifyDownload(page, async () => {...})` 替代内联逻辑
- [ ] 不使用 `import * as fs from 'fs'` 手动验证文件
- [ ] 不使用 `download.failure()` 作为唯一验证手段

## 断言规范（重要）

- [ ] **禁止在测试文件中直接使用 `expect()`**（含所有形式）
- [ ] 元素可见 → `hybridAssert.toBeVisible('组件名')`
- [ ] 文本包含 → `hybridAssert.toContainText(locator, text)`
- [ ] 元素数量 → `hybridAssert.toHaveCount(locator, count)`
- [ ] AI 智能断言 → `aiAssert(assertions.xxx)`（文本存入 YAML）
- [ ] `import` 语句中不引入 `expect`

## aiAct 使用限制

- [ ] 业务步骤中禁止直接调用 `await aiAct(...)` 操作 UI
- [ ] 用例末尾保留唯一一处 `await aiAct("执行结束")`（保证报告录像可播放）

## 后端 API 调用（含 `// api:xxx` 注解时）

- [ ] 扫描 `api/` 目录确认函数已存在
- [ ] `import` 中引入对应 API 函数
- [ ] test 函数参数增加 `request` fixture
- [ ] 顶部解构包含 `apiConfig`
- [ ] YAML `testData.apiConfig` 新增对应配置段
- [ ] API 调用传入 `recordToReport`

## aiAssert 注解（含 `// aiAssert: ...` 注解时）

- [ ] 识别所有 `// aiAssert:` 注解行
- [ ] 断言文本存入 YAML `testData.assertions.{camelCaseKey}`
- [ ] 测试代码解构 `assertions` 并通过 `assertions.xxx` 引用
- [ ] 不硬编码断言字符串

## 组件命名规范

- [ ] 使用 `{Module}-{FileName}-{componentName}` 格式（PascalCase 各部分，连字符分隔）
- [ ] 检查是否与现有组件重名
- [ ] 组件 YAML 包含 `description`、`category` 字段
