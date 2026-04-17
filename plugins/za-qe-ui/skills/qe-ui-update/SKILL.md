---
name: qe-ui-update
description: 对已优化的Playwright测试脚本进行增量更新，无需重新录制或重新生成。用于：新增步骤、修改步骤、删除步骤、更新组件选择器、修改测试数据、新增断言。当用户说"更新测试"、"修改测试步骤"、"新增一步"、"删除某步骤"、"改一下选择器"、"更新测试数据"、"update test"、"add step"、"modify test"时触发。直接修改testcase-optimized目录下的.test.ts、组件YAML和数据YAML，改动最小化，禁止重构无关代码。
metadata:
  category: ui-testing
  version: 2.0.0
---

# 测试脚本增量更新专家

## 适用场景

**适用**（已有优化脚本，局部修改）：
- 新增/修改/删除操作步骤
- 更新组件 Playwright 选择器
- 修改测试数据（账号、金额、URL）
- 插入断言验证

**不适用**（请使用 `qe-ui-generate`）：
- 全新测试用例，没有任何已有脚本
- 改动超过 60% 的步骤

---

## 执行流程

### 第一阶段：解析改动需求

从用户描述中提取：
- **目标文件**：哪个测试脚本
- **改动类型**：`add-step` / `modify-step` / `delete-step` / `add-component` / `modify-component` / `update-data` / `add-assertion`
- **改动位置**：在哪个步骤前/后
- **改动内容**：操作什么 UI 元素

### 第二阶段：读取目标文件（必须先读后改）

**文件定位策略**（若用户未明确指定文件）：
1. 从对话上下文中找到最近操作的文件
2. 根据用户描述的业务关键词扫描 `testcase-optimized/` 目录列出候选文件
3. 仍不确定时询问用户提供路径

**系统区分**：
- BIB 系统（网银）：组件在 `component/bib/`，测试在 `testcase-optimized/bib/`
- OPS 系统（运营）：组件在 `component/za-bank-ops/`，测试在 `testcase-optimized/ops/`
- invest 系统（投资）：组件在 `component/invest/`，必须读取 `component/invest/RULES.md`

```
1. testcase-optimized/{path}/{test-name}.test.ts
2. data/{path}/{test-name}.yaml
3. component/{system}/{module}/{file}.yaml
4. component/{system}/RULES.md（若存在必须读取）
```

读取后输出确认：
```
📁 目标文件已读取:
- 测试脚本: testcase-optimized/bib/withdrawal/xxx.test.ts (X个步骤)
- 测试数据: data/bib/withdrawal/xxx.yaml (M个步骤)
- 组件文件: component/bib/auth/otp.yaml (K个组件)

📋 计划改动:
1. [新增组件] component/bib/auth/otp.yaml → Auth-otp-dismissButton
2. [修改测试脚本] 在第3步后插入新步骤
3. [更新测试数据] loginSteps 新增 index=4
```

### 第三阶段：执行增量修改

#### 新增/修改组件

```yaml
  Auth-otp-dismissButton:
    playwright:
      primary: "page.getByRole('button', { name: '我知道了' })"
    description: 弹窗关闭按钮
    category: button
```

命名规范：`{Module}-{FileName}-{componentName}`

#### 新增步骤到测试脚本

```typescript
await componentClick(helpers, 'Auth-login-loginButton');
// ↓ 新增（条件性弹窗使用 skipIfNotFound）
await waitForComponentVisible(helpers, 'Auth-otp-dismissButton', { timeout: 5000, optional: true });
await componentClick(helpers, 'Auth-otp-dismissButton', { skipIfNotFound: true });
await waitForComponentVisible(helpers, 'Auth-otp-otpInput1');
```

#### 更新 testSteps YAML（插入后重排 index）

```yaml
testSteps:
  loginSteps:
    - index: 3
      componentName: Auth-login-loginButton
      action: click
    - index: 4          # 新增
      componentName: Auth-otp-dismissButton
      action: click
      optional: true
  otpSteps:
    - index: 5          # 原来是 4，受插入影响 +1
      componentName: Auth-otp-otpInput1
      action: input
```

**重要**：插入/删除步骤后，必须对后续所有 index 重新递增排序，同步更新 `metadata.totalSteps` 和 `lastUpdated`。

### 第四阶段：输出变更摘要

```
✅ 增量更新完成

📝 变更摘要:
1. [组件新增] component/bib/auth/otp.yaml
   + Auth-otp-dismissButton (弹窗关闭按钮)

2. [脚本修改] testcase-optimized/bib/withdrawal/xxx.test.ts
   + 第3步后新增弹窗关闭步骤（skipIfNotFound: true）

3. [数据更新] data/bib/withdrawal/xxx.yaml
   + loginSteps 新增 index=4
   ~ 后续 10 个步骤 index 已重排 (4→5, 5→6, ...)
   ~ metadata.totalSteps 更新为 28
```

---

## 断言写法速查

| 场景 | 写法 |
|------|------|
| 元素可见 | `await hybridAssert.toBeVisible('ComponentName')` |
| 文本包含 | `await hybridAssert.toContainText(getComponentLocator(helpers, 'X'), text)` |
| AI 断言 | `await aiAssert(assertions.xxxKey)`（文本必须存入 YAML） |

**禁止**：`expect()`、硬编码 `aiAssert` 字符串参数

---

## 执行约束

**必须**：先读后改 / 最小化改动 / 命名规范 / index 连续性 / 元数据同步  
**禁止**：删除 `selectorFallbackRegistry` 三件套 / 移除 `aiLocate` 参数 / 直接 `aiAct()` 操作 UI / `expect()` 断言 / 硬编码 `aiAssert` 字符串

详细约束和全部8种更新模式代码示例见 `references/update-patterns.md`。

---

## 参考资源

- **8种更新模式 + 约束速查**: `references/update-patterns.md`
- **转换工具（全新用例）**: `qe-ui-generate` skill
- **执行测试**: `qe-ui-execute` skill
- **工具方法**: `utils/hybrid-helpers.ts`、`utils/hybrid-assert-helpers.ts`
- **组件库**: `component/` 目录
