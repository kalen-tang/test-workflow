# Alfie UI - Playwright UI 自动化测试工具集 用户手册

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://gitlab.in.za/claude/alfie/qe)
[![Category](https://img.shields.io/badge/category-ui--testing-green.svg)](https://gitlab.in.za/claude/alfie/qe)

## 📋 概述

za-ui 是一个完整的 Playwright UI 自动化测试解决方案，提供从原生录制代码转换到测试执行修复的全流程能力。通过**三个核心 Skills**、**两个工作流命令**和**一个智能 Agent** 的协同工作，帮助测试团队快速将手工录制的 Playwright 脚本转化为可维护的自动化测试代码。

> 项目架构、实施计划、团队信息见 [项目主文档](../../README.md)

---

## 🚀 快速开始

### 最快上手

```bash
# 转换原生 Playwright 代码为优化架构
/za-ui:playwright-to-optimized testcase-native/login-test.test.ts
```

自动完成：分析原生代码 → 生成优化架构代码 → 生成组件 YAML + 测试数据 YAML

### 首次使用推荐流程

```bash
# 1. 转换原生录制代码
/za-ui:playwright-to-optimized testcase-native/your-test.test.ts

# 2. 执行测试并自动修复
/za-ui:playwright-to-optimized testcase-optimized/your-module/test.test.ts

# 3. 全流程一键执行（转换+测试+修复）
/za-ui:playwright-to-optimized testcase-native/your-test.test.ts --full

# 4. 对已有脚本进行增量更新
/za-ui:playwright-test-update 在登录后新增关闭弹窗步骤
```

---

## ⚡ 工作流命令

### `/za-ui:playwright-to-optimized` - Playwright 完整工作流 ⭐ 推荐

**一站式**处理 Playwright 测试脚本：代码转换优化、测试执行、失败自动修复。

```bash
# 转换原生代码（转换模式）
/za-ui:playwright-to-optimized testcase-native/login-test.test.ts

# 测试已优化代码（测试模式）
/za-ui:playwright-to-optimized testcase-optimized/bib/withdrawal/test.test.ts

# 完整工作流（转换+测试+修复）
/za-ui:playwright-to-optimized testcase-native/test.test.ts --full

# 调试模式
/za-ui:playwright-to-optimized testcase-optimized/test.test.ts --debug
```

**执行流程**：
```
📄 原生 Playwright 录制代码 (testcase-native/)
    ↓
🔄 playwright-test-generate（代码转换）
    ↓ 自动生成
📁 优化架构代码 + 组件 YAML + 数据 YAML
    ↓
🧪 playwright-test-execute（测试执行）
    ↓ 自动修复（最多3轮）
✅ 稳定可维护的自动化测试
```

**智能模式识别**：

| 参数特征 | 识别模式 | 执行动作 |
|---------|---------|---------|
| 路径含 `testcase-native` | 转换模式 | 转换原生代码为优化架构 |
| 路径含 `testcase-optimized` | 测试模式 | 执行测试 + 自动修复 |
| 包含 `--full` | 完整模式 | 转换 + 测试 + 修复 |

**参数说明**：

| 参数 | 说明 |
|------|------|
| `testcase-native/...` | 指定转换模式 |
| `testcase-optimized/...` | 指定测试模式 |
| `--test` | 强制测试模式 |
| `--full` | 完整工作流 |
| `--debug` | Playwright 调试模式 |
| `--no-fix` | 禁用自动修复 |
| `--max-rounds=N` | 最大修复轮次（默认3） |

---

### `/za-ui:playwright-test-update` - 增量更新专家

对**已有**测试脚本进行增量更新，无需重新录制或重新生成，通过自然语言描述直接精准修改。

```bash
# 新增操作步骤
/za-ui:playwright-test-update 在登录按钮点击后，新增关闭"我知道了"弹窗的步骤

# 指定文件并描述改动
/za-ui:playwright-test-update testcase-optimized/bib/withdrawal/cross-border.test.ts 新增填写备注字段

# 修改测试数据
/za-ui:playwright-test-update 将提款金额从 13000 改为 20000

# 新增断言
/za-ui:playwright-test-update 在提交后，验证页面出现"申請成功"文字

# 更新组件选择器
/za-ui:playwright-test-update 登录按钮文字从"登入"改成了"登錄"，需要更新选择器

# 删除过时步骤
/za-ui:playwright-test-update 删除 Auth-otp-obsoletePopup 的点击步骤
```

**适用场景**：

- 新增操作步骤（点击、输入、勾选）
- 修改步骤的目标组件或操作值
- 删除不再需要的步骤
- 更新组件的 Playwright 选择器
- 修改测试数据（账号、金额、URL 等）
- 在流程中插入断言验证
- 处理新出现的弹窗或条件性 UI 元素

> 如需全新生成测试脚本，请使用 `/za-ui:playwright-to-optimized`

---

## 🔬 核心 Skills

### 1. playwright-test-generate（代码转换器）

将 Playwright 原生录制代码转换为可维护的优化架构。

- 智能等待优化（`page.waitForTimeout()` → `waitForComponentVisible()`）
- 组件驱动架构（选择器抽取为 YAML 配置）
- 混合架构实现（Playwright 原生优先 → Midscene AI 回退）
- 测试数据分离（统一 YAML 结构，支持多环境）
- AI 上下文增强（多层 Prompt 提升定位准确性）
- 混合断言工具（`createHybridAssert`）

```bash
# 通过 playwright-to-optimized 命令触发
/za-ui:playwright-to-optimized testcase-native/your-test.test.ts
```

**输出**：优化后测试代码（`testcase-optimized/`）+ 组件 YAML（`component/`）+ 测试数据 YAML（`data/`）

**组件命名规范**：`{Module}-{FileName}-{componentName}`

示例：`Transfer-single-transfer-continueButton`

---

### 2. playwright-test-execute（测试执行器）

执行优化后的测试文件，智能分析失败原因，自动修复常见问题。

- 执行前步骤校验（对比原生与优化步骤序列）
- 智能错误分类与根因分析
- 定位器失败自动修复
- 等待策略智能调整
- 最多 3 轮迭代修复

**自动修复轮次**：

| 轮次 | 修复内容 |
|------|---------|
| 第1轮 | 快速修复：导入路径、语法、配置问题 |
| 第2轮 | 等待优化：添加 `waitForComponentVisible`、调整超时 |
| 第3轮 | 深度修复：更新组件定义、修复数据、调整断言 |
| 超限 | 生成详细诊断报告，提供人工处理建议 |

**错误分类**：

| 错误类型 | 常见原因 |
|---------|---------|
| Locator Not Found | 元素变更、未加载、被隐藏、选择器有误 |
| Timeout Error | 网络慢、组件未出现、SPA 路由问题 |
| Data Issue | 数据过期、账号锁定、测试环境不一致 |
| Assertion Error | 业务逻辑变更、文本变更、异步未完成 |
| Import Error | 移动文件后路径未更新、目录深度有误 |

```bash
# 通过 playwright-to-optimized 命令触发
/za-ui:playwright-to-optimized testcase-optimized/bib/withdrawal/test.test.ts
```

---

### 3. playwright-test-update（增量更新器）

对已有优化测试脚本进行最小化、精准的增量修改。

- 自然语言解析改动意图
- 先读后改约束（严禁凭记忆修改）
- 最小化改动原则（仅修改必要部分）
- 同步更新关联组件 YAML 和测试数据 YAML
- 保证 `testSteps` index 连续性

**常用修改模式**：

| 模式 | 使用场景 |
|------|---------|
| 新增弹窗处理 | 流程中出现条件性弹窗 |
| 新增表单字段 | 业务新增填写项 |
| 新增断言验证 | 加强流程关键节点检查 |
| 修改导航路径 | UI 菜单路径调整 |
| 更新组件选择器 | 前端元素文本/属性变更 |
| 新增下载验证 | 导出/下载功能验证 |
| 新增 aiAssert | 增强 AI 视觉断言 |

```bash
# 通过 playwright-test-update 命令触发
/za-ui:playwright-test-update 在登录后新增关闭弹窗步骤
```

---

## 🤖 智能 Agent

### playwright-to-optimized-converter-agent

端到端执行 Playwright 测试工作流的智能 Agent，协调转换与测试能力。

**核心职责**：

| 能力域 | 职责 |
|--------|------|
| 代码转换 | 执行代码转换、系统识别、路径推断、组件库维护、质量校验 |
| 测试执行 | 测试运行管理、错误分析、自动修复执行、迭代修复流程（最多3轮）、修复报告生成 |

---

## 🎯 适用场景

### 适合

- Playwright 录制代码转换为可维护架构
- 已有 UI 自动化测试需要持续维护和更新
- 测试执行失败后的自动化诊断和修复
- 需要混合 AI（Midscene）与原生定位策略的场景
- 多环境（SIT/UAT/QE）UI 测试数据管理

### 不适合

- 纯 API/接口测试（建议使用 za-qe）
- 性能测试（需要专门的性能测试工具）
- 移动端原生 App 测试

---

## 🔧 架构说明

### 文件目录约定

```
your-project/
├── testcase-native/          # 原始录制代码（转换输入）
│   └── module/
│       └── test.test.ts
├── testcase-optimized/       # 优化后代码（转换输出 / 测试输入）
│   └── module/
│       └── test.test.ts
├── component/                # 组件选择器 YAML
│   └── module/
│       └── components.yaml
└── data/                     # 测试数据 YAML（支持多环境）
    └── module/
        └── test-data.yaml
```

### 混合架构策略

- **Playwright 原生优先**：精确选择器场景，执行速度快
- **Midscene AI 回退**：动态内容或选择器不稳定场景，靠视觉理解定位
- **统一断言接口**：`hybridAssert` 自动选择最优断言方式

### 测试数据 YAML 结构

```yaml
environments:
  sit:
    account: "xxx"
    amount: 10000
  auto_qe:
    account: "xxx"
    amount: 10000
  uat:
    account: "xxx"
    amount: 10000
```

---

## 📚 详细文档

### 命令文档

| 命令 | 文档 | 说明 |
|------|------|------|
| `/za-ui:playwright-to-optimized` ⭐ | [playwright-to-optimized.md](./commands/playwright-to-optimized.md) | 完整工作流：转换+测试+修复 |
| `/za-ui:playwright-test-update` | [playwright-test-update.md](./commands/playwright-test-update.md) | 增量更新已有测试脚本 |

### Skills 文档

| Skill | 文档 | 说明 |
|-------|------|------|
| playwright-test-generate | [SKILL.md](./skills/playwright-test-generate/SKILL.md) | 原生代码转换规则和优化策略 |
| playwright-test-execute | [SKILL.md](./skills/playwright-test-execute/SKILL.md) | 测试执行和自动修复规则 |
| playwright-test-update | [SKILL.md](./skills/playwright-test-update/SKILL.md) | 增量更新规则和命名规范 |

### Agent 文档

| Agent | 文档 | 说明 |
|-------|------|------|
| playwright-to-optimized-converter-agent | [agent.md](./agents/playwright-to-optimized-converter-agent.md) | 端到端工作流协调 Agent |

---

**版本**: v1.0.0 | [项目主文档](../../README.md) | ZA Bank Test Team
