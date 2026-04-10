# za-qe Skill 架构重新设计

> 本文档为架构规划，不涉及具体实施。确认后再逐步改造。

## 1. 问题分析

### 当前架构问题

| 问题 | 说明 |
|------|------|
| `devplan-analyzer` 职责过重 | 同时做接口提取、场景用例设计、单接口用例推荐，混在一个报告里 |
| `devplan-analyzer` 命名不准确 | 名字暗示只分析"开发方案"，但实际还做用例设计 |
| `case-designer` 游离于主流程 | 产出 PlantUML 可视化给人看，api-generator 无法消费 |
| `api-generator` 输入来源单一 | 只能消费 devplan-analyzer 的报告，无法利用 case-designer 的场景设计 |
| "手工案例" 命名不当 | 案例不区分执行形式（手工/自动化），应统一叫"场景案例"或"流程案例" |

### 核心矛盾

```
当前：devplan-analyzer 一个 skill 产出"接口数据 + 场景设计"，case-designer 独立产出"可视化案例"
期望：职责分离，接口提取归接口提取，场景设计归场景设计，两者产出共同喂给 api-generator
```

---

## 2. 新架构设计

### 2.1 Skill 职责重新划分

```
┌─────────────┐    ┌──────────────┐
│  req-parser  │    │ design-parser │
│  需求文档分析 │    │  设计文档分析  │
│ （不变）      │    │  （不变）      │
└──────┬───────┘    └──────┬────────┘
       │ 规范化需求.md      │ 规范化设计.md
       ▼                   ▼
┌──────────────────────────────────┐
│     devplan-analyzer（收窄）       │
│     → 改名：interface-extractor   │
│                                  │
│  职责：仅做接口提取               │
│  - 从规范化设计文档提取接口信息     │
│  - 接口路径校验（dmb 网关检测）    │
│  - 微服务识别与映射               │
│  - 接口间依赖关系分析             │
│  - 接口参数结构化                 │
│                                  │
│  不再做：场景设计、用例推荐        │
└──────────────┬───────────────────┘
               │ 接口数据报告.md
               ▼
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│ case-designer │ │              │
│ （增强）       │ │              │
│              │ │              │
│ 输入：        │ │              │
│ · 规范化需求  │ │              │
│ · 接口数据    │ │              │
│              │ │              │
│ 输出：        │ │              │
│ · PlantUML   │ │              │
│   流程图      │ │              │
│ · MindMap    │ │              │
│ · XMind      │ │              │
│ · 场景表.md  │ │              │
│  （新增）     │ │              │
└──────┬───────┘ │              │
       │ 场景表   │              │
       ▼         │              │
┌──────────────────────────────┐
│        api-generator          │
│                              │
│  输入：                       │
│  · 接口数据报告（接口信息）    │
│  · 场景表（场景+步骤+验证点） │
│                              │
│  输出：                       │
│  · pytest 测试代码            │
│  · YAML 测试数据              │
└──────────────────────────────┘
```

### 2.2 Skill 变更清单

| Skill | 变更类型 | 变更内容 |
|-------|---------|---------|
| `req-parser` | **不变** | 需求文档 → 规范化需求 Markdown |
| `design-parser` | **不变** | 设计文档 → 规范化设计 Markdown |
| `devplan-analyzer` | **改名 + 收窄** | 改名为 `interface-extractor`，只做接口提取和校验 |
| `case-designer` | **增强** | 新增"场景表"Markdown 输出，接受接口数据作为可选输入 |
| `api-generator` | **改输入** | 输入从"测试左移分析报告"改为"接口数据 + 场景表" |
| `doc-reviewer` | **不变** | 需求验证，独立运行 |

### 2.3 各 Skill 详细定义

#### interface-extractor（原 devplan-analyzer，收窄）

**输入**：
- 规范化设计文档（design-parser 产出）（必须）
- 规范化需求文档（req-parser 产出）（可选，用于补充业务上下文）

**输出**：接口数据报告 Markdown，结构如下：

```markdown
# 接口数据报告

## 概览
- 接口总数：N
- 所属微服务：列表
- 网关接口检测：N 个需替换

## 接口路径校验
| 序号 | 接口路径 | 状态 | 说明 |
|------|---------|------|------|

## 接口信息

### 接口1：{名称}
- **所属微服务**：xxx
- **接口路径**：xxx
- **请求方法**：POST
- **Content-Type**：application/json
- **功能描述**：xxx

**请求参数**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|

**响应参数**
| 字段名 | 类型 | 说明 |
|--------|------|------|

## 接口依赖关系
| 上游接口 | 传递字段 | 下游接口 |
|---------|---------|---------|
```

**不再包含**：单接口测试用例推荐、场景测试用例设计、优先级建议

---

#### case-designer（增强）

**定位改名**：从"手工案例生成器"改为"场景案例设计器"

**输入**：
- 规范化需求文档（必须）
- 接口数据报告（可选，有则生成更精准的场景）

**输出**（在现有基础上新增第 4 项）：
1. PlantUML 业务流程图（不变）
2. PlantUML 测试功能点 MindMap（不变）
3. PlantUML 详细测试案例 MindMap（不变）
4. **场景表 Markdown**（新增，供 api-generator 消费）

**场景表格式**：

```markdown
# 场景案例表

## 场景总览
| 场景ID | 场景名称 | 类型 | 优先级 | 涉及接口 |
|--------|---------|------|--------|---------|
| SC-001 | 正常创建活动 | positive | P0 | 接口1, 接口2 |
| SC-002 | 创建活动参数校验 | negative | P1 | 接口1 |

## 场景详情

### SC-001 正常创建活动

**类型**：positive
**优先级**：P0
**前置条件**：用户已登录，具有创建权限

**步骤**：

| 步骤 | 操作 | 调用接口 | 请求要点 | 预期结果 |
|------|------|---------|---------|---------|
| 1 | 创建活动 | POST /activity/create | name=xxx, type=1 | 返回 activityId |
| 2 | 查询活动详情 | GET /activity/detail | activityId={{步骤1.activityId}} | 活动信息一致 |

**验证点**：
- [ ] 活动创建成功，返回有效 activityId
- [ ] 查询结果与创建参数一致
- [ ] 活动状态为"草稿"

---

### SC-002 创建活动参数校验

**类型**：negative
**优先级**：P1
**前置条件**：用户已登录

**步骤**：

| 步骤 | 操作 | 调用接口 | 请求要点 | 预期结果 |
|------|------|---------|---------|---------|
| 1 | 缺少必填参数 | POST /activity/create | name=空 | 返回参数校验错误 |

**验证点**：
- [ ] 返回错误码，提示 name 不能为空
```

---

#### api-generator（改输入）

**输入**（新）：
- 接口数据报告（interface-extractor 产出）— 提供接口定义（路径、参数、响应）
- 场景表（case-designer 产出）— 提供测试场景（步骤、验证点、数据传递）

**输入**（兼容旧）：
- 仍支持直接传入"测试左移分析报告"（旧格式兼容）

**输出**（不变）：
- pytest 测试代码
- YAML 测试数据（sit/auto_qe/uat）

---

### 2.4 新版 Workflow 串联流程

```
/za-qe:qe-workflow

阶段 1：环境探测 + 目录配置（不变）

阶段 2：文档转换（不变）
  docx/doc → markitdown → md → UTF-8 编码修复

阶段 3：Skill 串联（调整）

  3.1  req-parser         ← 需求 md
       输出：规范化需求文档

  3.2  design-parser      ← 设计 md
       输出：规范化设计文档

  3.3  interface-extractor ← 规范化设计文档 + 规范化需求文档（可选）
       输出：接口数据报告

  3.4  case-designer       ← 规范化需求文档 + 接口数据报告（可选）
       输出：PlantUML + MindMap + XMind + 场景表

  3.5  api-generator       ← 接口数据报告 + 场景表
       输出：pytest 代码 + YAML 数据
```

**分支逻辑**：

| 有需求文档 | 有设计文档 | 执行路径 |
|-----------|-----------|---------|
| ✅ | ✅ | req-parser → design-parser → interface-extractor → case-designer → api-generator |
| ✅ | ❌ | req-parser → case-designer（仅基于需求，无接口数据） |
| ❌ | ✅ | design-parser → interface-extractor → api-generator（无场景表，基于接口生成基础用例） |

---

## 3. Artifact Schemas 影响

| 编号 | 名称 | 变更 |
|------|------|------|
| 01 | normalized-requirement | 不变 |
| 02 | normalized-design | 不变 |
| **08** | **interface-data-report** | **新增**，interface-extractor 产出格式 |
| **09** | **scenario-table** | **新增**，case-designer 场景表产出格式 |
| 03 | normalized-cases | 保持计划中 |
| 04 | code-diff-report | 保持计划中 |
| 05 | validation-report | 保持计划中 |
| 06 | manual-test-cases → scenario-cases | **改名**，从"手工测试案例"改为"场景案例" |
| 07 | api-test-cases | 输入源从 devplan-analyzer 报告改为 08 + 09 |

---

## 4. 文件变更清单（实施时参考）

### 改名/移动

| 操作 | 原路径 | 新路径 |
|------|-------|-------|
| 改名 | `skills/devplan-analyzer/` | `skills/interface-extractor/` |
| 改名 | `skills/devplan-analyzer/SKILL.md` | `skills/interface-extractor/SKILL.md` |
| 移动 | `skills/devplan-analyzer/references/` | `skills/interface-extractor/references/` |
| 移动 | `skills/devplan-analyzer/examples/` | `skills/interface-extractor/examples/` |

### 修改

| 文件 | 变更内容 |
|------|---------|
| `skills/interface-extractor/SKILL.md` | 重写，收窄职责为接口提取 |
| `skills/case-designer/SKILL.md` | 增加"场景表"输出格式，改称"场景案例设计器" |
| `skills/api-generator/SKILL.md` | 输入改为"接口数据报告 + 场景表" |
| `commands/workflow.md` | 更新串联逻辑 |
| `commands/help.md` | 更新 skill 描述 |
| `commands/gencase.md` | 更新 case-designer 描述 |
| `hooks/session-start-content.md` | 更新提示 |
| `README.md` | 更新架构图、skill 列表 |
| `.claude-plugin/plugin.json` | 版本号升级 |
| 项目根 `CLAUDE.md` | 更新 skill 列表和工作流描述 |

### 新增

| 文件 | 内容 |
|------|------|
| `references/artifact-schemas/08-interface-data-report.md` | 接口数据报告格式规范 |
| `references/artifact-schemas/09-scenario-table.md` | 场景表格式规范 |

### 清理

| 文件 | 说明 |
|------|------|
| `skills/devplan-analyzer/references/02-output-format.md` | 旧输出格式，合并到 interface-extractor 后删除多余部分 |
| `skills/devplan-analyzer/references/03-scenario-identification.md` | 场景识别指南，移到 case-designer |
| `skills/devplan-analyzer/references/04-test-case-patterns.md` | 用例设计模式，移到 case-designer |
| `skills/devplan-analyzer/references/05-requirement-integration.md` | 需求结合指南，拆分到 interface-extractor 和 case-designer |

---

## 5. 实施建议

### 分步实施顺序

1. **Phase 1**：创建 artifact-schemas（08、09），确定数据契约
2. **Phase 2**：改造 interface-extractor（从 devplan-analyzer 收窄）
3. **Phase 3**：增强 case-designer（新增场景表输出）
4. **Phase 4**：改造 api-generator（支持新输入格式）
5. **Phase 5**：更新 workflow 串联逻辑
6. **Phase 6**：更新文档（README、CLAUDE.md、help 等）

### 兼容性

- api-generator 应同时支持旧格式（devplan-analyzer 报告）和新格式（接口数据 + 场景表），过渡期保持向后兼容
- interface-extractor 保留 devplan-analyzer 的 description 触发词，避免用户习惯断裂

---

**版本**: 架构设计 v1.0 | **日期**: 2026-04-10 | **状态**: ✅ 已实施
