# qa-toolkit 完整模式实施计划

**版本**: v1.2
**创建时间**: 2026-03-18
**最后更新**: 2026-03-19
**截止日期**: 2026-04-20（剩余 32 天）
**项目状态**: 🚧 实施中

---

## 📋 目录

- [执行摘要](#执行摘要)
- [当前问题分析](#当前问题分析)
- [解决方案](#解决方案)
- [实施计划](#实施计划)
- [任务分解](#任务分解)
- [风险管理](#风险管理)
- [验收标准](#验收标准)

---

## 执行摘要

### 核心目标

完成 qa-toolkit 插件的**完整模式**实施，打通从需求/设计文档到自动化测试用例的全流程四阶段工作流。

### 关键挑战

1. **标准化接口缺失**：四阶段 Skills 之间没有明确的输入输出格式规范
2. **SpecKit 集成未定**：需求/设计文档规范化工具（SpecKit）的集成方案待确定
3. **时间紧迫**：仅剩 33 天完成第一阶段 4 个组件 + 标准化定义

### 成功标准

- ✅ 定义完整的 artifact schemas（7 个标准化格式）**[已完成 2026-03-19]**
- ⏳ 完成第一阶段 4 个规范化组件
- ⏳ 验证四阶段端到端流程可用
- ⏳ 实现 `/qa-full` 工作流命令

### 📊 当前进展（2026-03-19 更新）

#### ✅ 已完成

**Artifact Schemas 定义（100% 完成）**：
- ✅ `00-overview.md` - 总览文档（四阶段工作流、七种格式依赖关系）
- ✅ `01-normalized-requirement-v2.md` - 标准化需求文档格式（对齐 ZA Bank PRD 7章）
- ✅ `02-normalized-design.md` - 标准化设计文档格式（对齐 ZA Bank 设计文档模板）
- ✅ `03-normalized-cases.md` - 标准化历史案例格式（支持案例复用、智能推荐）
- ✅ `04-code-diff-report.md` - 代码差异报告格式（Git Diff 分析、影响评估）
- ✅ `05-validation-report.md` - 需求验证报告格式（三级检查 P0/P1/P2）
- ✅ `06-manual-test-cases.md` - 手工测试用例格式（PlantUML/XMind/Markdown 输出）
- ✅ `07-api-test-cases.md` - API 测试案例格式（Python + YAML 代码规范）
- ✅ `output-normalized-requirement-v2.yaml` - 完整需求文档示例（500+ 行）
- ✅ `output-normalized-design.yaml` - 完整设计文档示例（600+ 行）

**SpecKit 方案决策**：
- ✅ 确认 SpecKit 是提示词模式，非独立工具
- ✅ 确定以产品标准为主（对齐 ZA Bank 模板）
- ✅ 将 SpecKit 最佳实践（三级检查、置信度标注）融入 Skill 实现

**Skills 基础定义**：
- ✅ `requirement-normalizer` SKILL.md 已创建
- ✅ `design-normalizer` 目录结构已创建

**api-case-generator v2.0 重构（2026-03-19 完成）**：
- ✅ 完全适配银行标准测试框架（pytest_zabank 系列插件）
- ✅ 从 `env` 多环境配置升级为 `variables` 变量化配置
- ✅ 从 `parametrize` 模式升级为 `@pytest.mark.data()` 装饰器
- ✅ Scenario 层接收 Step 对象，自动处理断言
- ✅ Fixture 智能命名（本服务简化/跨服务完整，自动检测）
- ✅ 完全通用化（移除所有项目特定示例）
- ✅ 更新 5 个 references 文档（00-04）
- ✅ 新增 Scenario 层设计指南（04-scenario-design.md）

#### 🚧 进行中（截止 2026-04-14）

**第一阶段规范化组件开发**：
- [ ] requirement-normalizer Skill 完整实现 - 负责人：陈贝
- [ ] design-normalizer Skill 完整实现 - 负责人：陈贝
- [ ] CML MCP（历史案例规范化）- 负责人：泉政
- [ ] Code Diff MCP（代码差异分析）- 负责人：奕翔

**现有 Skill 适配**：
- [ ] requirement-validator 适配标准化输入（01/02/04 格式）- 负责人：宇豪

#### 📋 计划中（2026-04-15 ~ 04-20）

- [ ] manual-case-generator 适配标准化格式 - 负责人：宇宸
- [x] **api-case-generator 适配标准化格式** - 负责人：泉政 **✅ 已完成（2026-03-19）**
  - ✅ v2.0 重构完成，完全适配银行标准测试框架
  - ✅ 更新所有 references 文档为 v2.0
  - ✅ 新增 Scenario 层设计指南
- [ ] 实现 `/qa-full` 工作流命令 - 负责人：鼎中
- [ ] 端到端流程测试 - 负责人：慧芳

---

## 当前问题分析

### 问题 1：Skill 间交互标准缺失

**现状**：
- 第二阶段（requirement-validator）不知道第一阶段输出什么格式
- 第三阶段（manual-case-generator）不知道如何使用第一阶段产出
- 第四阶段（api-case-generator）需要同时兼容第一、三阶段产出

**影响**：
- 各阶段 Skill 开发无法并行
- 集成时需要大量返工
- 测试和验证困难

### 问题 2：SpecKit 定位不明

**待决策问题**：
1. SpecKit 是什么？（工具/库/服务）
2. SpecKit 能否输出结构化格式（YAML/JSON）？
3. SpecKit 适合作为 MCP 还是 Skill？

**影响**：
- 第一阶段规范化方案无法落地
- 4 月 20 日截止日期风险高

### 问题 3：完整模式复杂度高

**第一阶段需要开发的组件**：
1. 需求文档规范化（陈贝负责）
2. 设计文档规范化（陈贝负责）
3. CML MCP - 历史案例规范化（泉政负责）
4. Code Diff MCP - 代码差异分析（奕翔负责）

**挑战**：
- 4 个组件并行开发，协调成本高
- 需求规范化和设计规范化可能技术方案类似，存在重复工作
- 33 天时间紧张

---

## 解决方案

### 方案 1：定义标准化产出物格式（Artifact Schemas）

#### 实施策略

在 `plugins/qa-toolkit/references/` 创建 `artifact-schemas/` 目录，定义 7 个标准化格式：

```
plugins/qa-toolkit/references/artifact-schemas/
├── 00-overview.md                      # 总览和设计原则
├── 01-normalized-requirement.md        # 标准化需求文档格式
├── 02-normalized-design.md             # 标准化设计文档格式
├── 03-normalized-cases.md              # 规范化历史案例格式
├── 04-code-diff-report.md              # 代码差异报告格式
├── 05-validation-report.md             # 需求检查报告格式
├── 06-manual-test-cases.md             # 手工测试用例格式
└── 07-api-test-cases.md                # API 自动化用例格式
```

#### 标准化格式核心原则

1. **结构化优先**：使用 YAML/JSON 定义关键信息，便于程序解析
2. **可解析性**：每个产出物包含元数据（artifact_type, version）
3. **前向兼容**：定义 version 字段，支持未来格式升级
4. **可追溯性**：包含 source_file、created_at、normalizer

#### 示例：标准化需求文档格式（简化版）

```yaml
artifact_type: normalized_requirement  # 固定值
version: "1.0"
source_file: "原始需求文档.docx"
created_at: "2026-03-18T10:00:00Z"
normalizer: "speckit-normalizer"

requirements:
  - id: REQ-001
    title: "用户登录功能"
    priority: high  # high/medium/low
    description: "用户可以通过手机号和密码登录系统"
    acceptance_criteria:
      - "用户输入正确的手机号和密码，点击登录按钮，跳转到首页"
    related_interfaces:
      - "/user/login"
    test_focus: true
    risk_level: medium
```

### 方案 2：SpecKit 集成方案

#### 推荐方案 A：SpecKit 作为第一阶段外部依赖（MCP 集成）

**架构图**：

```
┌─────────────────────────────────────┐
│  SpecKit (外部工具/MCP)              │
│  - 输入：需求文档、设计文档          │
│  - 输出：标准化需求、标准化设计      │
│          (符合 artifact-schemas)     │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  qa-toolkit 完整模式                │
│                                      │
│  第一阶段（简化）：                  │
│  - SpecKit MCP（需求/设计规范化）    │
│  - CML MCP（历史案例规范化）         │
│  - Code Diff MCP（代码差异分析）     │
│                                      │
│  第二阶段：requirement-validator     │
│  第三阶段：manual-case-generator     │
│  第四阶段：api-case-generator        │
└─────────────────────────────────────┘
```

**优点**：
- ✅ 减少重复开发（不用再开发需求/设计规范化 Skill）
- ✅ 专业工具做专业事（假设 SpecKit 更成熟）
- ✅ 加快进度，应对 4 月 20 日截止

**前提条件**：
- SpecKit 能够输出结构化格式（YAML/JSON）
- SpecKit 可以被封装为 MCP 或提供 API 接口

#### 备选方案 B：自研需求/设计规范化 Skill

如果 SpecKit 不适合集成，则按原计划开发：
- `requirement-normalizer` Skill（陈贝负责）
- `design-normalizer` Skill（陈贝负责）

**风险**：
- ⚠️ 开发工作量大，时间紧张
- ⚠️ 需求规范化和设计规范化技术方案类似，可能重复工作

**缓解措施**：
- 先完成一个（需求规范化），验证技术方案后再复制到设计规范化
- 提取公共代码为共享模块

### 方案 3：分阶段实施策略

#### 第一阶段（Week 1-2）：定义标准 + SpecKit 验证

**时间**：2026-03-18 ~ 2026-03-31（2 周）

**任务**：
1. 完成 artifact-schemas 定义（7 个格式文档）
2. 评估 SpecKit 能力，确定集成方案
3. 实现 SpecKit MCP 适配层（或启动自研方案）

**里程碑**：
- ✅ artifact-schemas 文档完成并评审通过
- ✅ SpecKit 集成方案确定（方案 A 或方案 B）

#### 第二阶段（Week 3-4）：规范化组件开发

**时间**：2026-04-01 ~ 2026-04-14（2 周）

**任务**：
1. 实现需求/设计规范化（SpecKit MCP 或自研 Skill）
2. 实现 CML MCP（泉政负责）
3. 实现 Code Diff MCP（奕翔负责）

**里程碑**：
- ✅ 第一阶段 4 个组件全部完成
- ✅ 单元测试通过

#### 第三阶段（Week 5）：集成验证

**时间**：2026-04-15 ~ 2026-04-20（1 周）

**任务**：
1. 更新第二、三、四阶段 Skill 适配标准格式
2. 实现 `/qa-full` 工作流命令
3. 端到端流程测试

**里程碑**：
- ✅ 四阶段端到端流程可用
- ✅ `/qa-full` 命令可用

---

## 实施计划

### 时间轴（甘特图）

```
Week 1 (03-18~03-24): 定义标准 + SpecKit 评估
├─ Day 1-2: artifact-schemas 定义（00-overview, 01-04）
├─ Day 3-4: artifact-schemas 定义（05-07）
├─ Day 5: SpecKit 能力评估和方案决策
└─ Day 6-7: SpecKit MCP 适配层设计（或自研方案启动）

Week 2 (03-25~03-31): SpecKit 集成 + 规范化组件启动
├─ Day 1-3: SpecKit MCP 实现（或 requirement-normalizer 开发）
├─ Day 4-5: CML MCP 开发（泉政）
├─ Day 6-7: Code Diff MCP 开发（奕翔）

Week 3 (04-01~04-07): 规范化组件开发
├─ Day 1-3: 需求/设计规范化完成
├─ Day 4-5: CML MCP 完成
├─ Day 6-7: Code Diff MCP 完成

Week 4 (04-08~04-14): 单元测试 + 集成准备
├─ Day 1-3: 第一阶段组件单元测试
├─ Day 4-5: 更新第二阶段 requirement-validator 适配标准格式
├─ Day 6-7: 更新第三、四阶段 Skill 适配标准格式

Week 5 (04-15~04-20): 集成验证 + 上线
├─ Day 1-2: 实现 /qa-full 工作流命令
├─ Day 3-4: 端到端流程测试
├─ Day 5: Bug 修复和优化
└─ Day 6: 文档更新和发布
```

### 里程碑

| 里程碑 | 计划日期 | 实际完成 | 交付物 |
|--------|---------|---------|--------|
| M1：标准定义完成 | 2026-03-24 | **✅ 2026-03-19**（提前5天） | artifact-schemas 全部 8 个文档 + 2 个示例文件 |
| M2：SpecKit 方案确定 | 2026-03-28 | **✅ 2026-03-18** | 决策采用方案 B（自研），以产品标准为主 |
| M3：第一阶段组件完成 | 2026-04-14 | ⏳ 进行中 | 4 个规范化组件 + 单元测试 |
| M4：完整模式上线 | 2026-04-20 | ⏳ 计划中 | `/qa-full` 可用 + 端到端测试通过 |

---

## 任务分解

> **执行提示**：使用 superpowers:executing-plans 或 superpowers:subagent-driven-development skill 执行以下 Task，Steps 使用 `- [ ]` checkbox 语法跟踪进度。

### ✅ 已完成（无需实施）

| 组件 | 状态 | 说明 |
|------|------|------|
| Artifact Schemas 全部 8 个文档 | ✅ | `references/artifact-schemas/00-07`，2026-03-19 完成 |
| `requirement-normalizer` SKILL.md | ✅ | 含 examples/ |
| `api-case-generator` v2.0 | ✅ | 完全适配银行框架，2026-03-19 完成 |
| `manual-case-generator` | ✅ | 含 references/ + examples/ |
| `requirement-validator` | ✅ | SKILL.md 存在（缺 references/） |
| `shift-left-analyzer` | ✅ | 快速模式核心（不在本计划范围） |
| `/qa-full` 命令占位文件 | ✅ | `commands/full-workflow.md`（需补充内容） |

### ⏳ 待实施任务总览

| 任务 | 负责人 | 优先级 |
|------|--------|--------|
| Task 1: `design-normalizer` SKILL.md | 陈贝 | P0 |
| Task 2: `requirement-validator` references/ | 宇豪 | P1 |
| Task 3: CML MCP 骨架（Python） | 泉政 | P1 |
| Task 4: Code Diff MCP 骨架（Python） | 奕翔 | P1 |
| Task 5: `/qa-full` 完整工作流命令 | 鼎中 | P1 |
| Task 6: `manual-case-generator` 适配标准格式 | 宇宸 | P2 |
| Task 7: `requirement-validator` 适配标准格式 | 宇豪 | P2 |
| Task 8: `api-case-generator` 确认标准格式适配 | 泉政 | P2 |
| Task 9: 端到端文档验收 | 鼎中 | P2 |

### 文件结构

**将创建的文件：**

```
plugins/qa-toolkit/
├── skills/
│   ├── design-normalizer/
│   │   ├── SKILL.md                          # [新建] Task 1 核心
│   │   ├── references/
│   │   │   ├── 01-design-format-guide.md     # [新建] 设计文档结构解析指南
│   │   │   └── 02-output-spec.md             # [新建] 输出格式规范引用
│   │   └── examples/
│   │       └── (已有 output-normalized-design.yaml)
│   └── requirement-validator/
│       └── references/
│           ├── 01-validation-rules.md         # [新建] Task 2 验证规则参考
│           └── 02-artifact-schema-refs.md     # [新建] 标准格式引用说明
├── mcp-servers/
│   ├── cml-mcp/
│   │   ├── README.md                          # [新建] Task 3
│   │   ├── main.py                            # [新建] MCP 主入口
│   │   ├── normalizer.py                      # [新建] 案例规范化逻辑
│   │   └── tests/
│   │       ├── conftest.py                    # [新建] Python 路径设置
│   │       └── test_normalizer.py             # [新建] 单元测试
│   └── code-diff-mcp/
│       ├── README.md                          # [新建] Task 4
│       ├── main.py                            # [新建] MCP 主入口
│       ├── analyzer.py                        # [新建] 差异分析逻辑
│       └── tests/
│           ├── conftest.py                    # [新建] Python 路径设置
│           └── test_analyzer.py               # [新建] 单元测试
└── commands/
    └── full-workflow.md                       # [修改] Task 5 补充完整内容
```

**将修改的文件：**

```
plugins/qa-toolkit/
├── skills/
│   ├── manual-case-generator/SKILL.md        # [修改] Task 6 适配标准输入格式
│   └── requirement-validator/SKILL.md        # [修改] Task 7 适配标准输入/输出格式
├── commands/help.md                           # [修改] Task 9 添加 /qa-full 说明
├── commands/status.md                         # [修改] Task 9 更新完整模式状态
├── README.md                                  # [修改] Task 9 更新完整模式状态
└── .claude-plugin/plugin.json                # [修改] Task 9 版本 1.2.0 → 1.3.0

# 项目根目录
CLAUDE.md                                      # [修改] Task 9 添加 /qa-full 使用示例
```

---

### Task 1：design-normalizer SKILL.md（P0）

**负责人**：陈贝
**文件：**
- 创建：`plugins/qa-toolkit/skills/design-normalizer/SKILL.md`
- 创建：`plugins/qa-toolkit/skills/design-normalizer/references/01-design-format-guide.md`
- 创建：`plugins/qa-toolkit/skills/design-normalizer/references/02-output-spec.md`
- 参考：`plugins/qa-toolkit/skills/requirement-normalizer/SKILL.md`（模式参照）
- 参考：`plugins/qa-toolkit/references/artifact-schemas/02-normalized-design.md`

- [ ] **Step 1: 确认已有 SKILL.md 的结构模式**

  打开 `skills/requirement-normalizer/SKILL.md`，记录其 YAML frontmatter 字段（name, description, status）和章节结构（概述、核心功能、输入、输出、使用方式、Step-by-Step 指南、references 引用）。

- [ ] **Step 2: 确认 artifact-schema 02 的字段结构**

  打开 `references/artifact-schemas/02-normalized-design.md`，记录：
  - 输出 YAML 的顶层字段（metadata、interfaces、database_changes 等）
  - 必填字段 vs 可选字段
  - ZA Bank 设计文档的 7 个章节结构

- [ ] **Step 3: 创建 SKILL.md**

  创建 `skills/design-normalizer/SKILL.md`，内容结构如下：

  ```markdown
  ---
  name: design-normalizer
  description: 设计文档标准化器，将原始设计文档（Word/PDF/Markdown）转换为结构化 YAML 格式，提取接口定义、数据库变更、业务逻辑，输出符合 artifact-schemas 标准的规范化设计文档
  status: active
  ---

  # design-normalizer - 设计文档标准化器

  ## 📋 概述
  [说明作用：将设计文档转为 YAML，供 requirement-validator 和 api-case-generator 使用]

  ## 🎯 核心功能
  1. **接口提取**：从设计文档中提取 API 接口定义（路径、方法、参数、响应）
  2. **数据库变更识别**：提取数据库表结构变更（DDL、新增字段等）
  3. **业务逻辑梳理**：提取业务流程、规则判断、异常处理
  4. **三级检查**：P0/P1/P2 设计完整性检查
  5. **置信度标记**：对提取内容标注置信度，便于人工复核

  ## 📥 输入
  - 设计文档：Word（.docx）、PDF、Markdown（.md）、纯文本
  - 可选：need_req_doc（关联需求文档路径，用于接口-需求对齐检查）

  ## 📤 输出
  - 主产出物：标准化设计文档（YAML 格式）
    - 符合 references/artifact-schemas/02-normalized-design.md 规范
    - 包含接口列表、数据库变更、业务逻辑

  ## 🚀 使用方式
  [命令示例，参照 requirement-normalizer 格式]

  ## 📋 Step-by-Step 指南
  ### Step 1: 解析文档结构
  ### Step 2: 提取接口定义
  ### Step 3: 提取数据库变更
  ### Step 4: 填充 YAML 结构
  ### Step 5: 三级质量检查

  ## 📚 References
  - references/01-design-format-guide.md
  - references/02-output-spec.md
  - ../../references/artifact-schemas/02-normalized-design.md
  ```

- [ ] **Step 4: 创建 references/01-design-format-guide.md**

  说明 ZA Bank 设计文档的典型结构（7章）和各章节的提取策略：
  - 第1章：文档说明（元数据提取）
  - 第2章：需求背景（关联需求链接）
  - 第3章：功能设计（接口定义、业务逻辑）
  - 第4章：数据库设计（DDL、字段变更）
  - 第5章：异常处理（错误码、降级策略）
  - 第6章：安全合规（权限、日志要求）
  - 第7章：测试重点（关键场景）

- [ ] **Step 5: 创建 references/02-output-spec.md**

  说明 `02-normalized-design.md` 格式中各字段的填写规则：
  - `interfaces` 数组：每个接口的必填字段
  - `database_changes` 数组：DDL 和字段变更格式
  - `business_rules` 数组：规则描述和关联接口
  - 置信度标注规则（何时标 high/medium/low）

- [ ] **Step 6: 提交**

  ```bash
  git add plugins/qa-toolkit/skills/design-normalizer/
  git commit -m "feat(design-normalizer): add SKILL.md and references"
  ```

---

### Task 2：requirement-validator references/（P1）

**负责人**：宇豪
**文件：**
- 创建：`plugins/qa-toolkit/skills/requirement-validator/references/01-validation-rules.md`
- 创建：`plugins/qa-toolkit/skills/requirement-validator/references/02-artifact-schema-refs.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/05-validation-report.md`

- [ ] **Step 1: 阅读当前 SKILL.md**

  打开 `skills/requirement-validator/SKILL.md`，记录当前接受的输入格式、验证规则描述、需要适配标准化格式的地方。

- [ ] **Step 2: 创建 01-validation-rules.md**

  文档内容：三级检查体系（P0 阻断级 / P1 警告级 / P2 信息级）+ 各级检查规则 + 输入/输出格式引用说明。

- [ ] **Step 3: 创建 02-artifact-schema-refs.md**

  说明如何从标准化输入中读取字段：
  - 标准化需求文档（01）：`requirements[].id`、`requirements[].acceptance_criteria`、`related_interfaces`
  - 标准化设计文档（02）：`interfaces[].path`、`interfaces[].method`、`business_rules`
  - 代码差异报告（04，可选）：`changed_files`、`impact_assessment`
  - 需求验证报告（05）：`validation_summary`、`p0_issues`、`p1_issues`、`p2_issues`、`decision`

- [ ] **Step 4: 提交**

  ```bash
  git add plugins/qa-toolkit/skills/requirement-validator/references/
  git commit -m "feat(requirement-validator): add references for artifact-schema alignment"
  ```

---

### Task 3：CML MCP 骨架（P1）

**负责人**：泉政
**文件：**
- 创建：`plugins/qa-toolkit/mcp-servers/cml-mcp/README.md`
- 创建：`plugins/qa-toolkit/mcp-servers/cml-mcp/main.py`
- 创建：`plugins/qa-toolkit/mcp-servers/cml-mcp/normalizer.py`
- 创建：`plugins/qa-toolkit/mcp-servers/cml-mcp/tests/conftest.py`
- 创建：`plugins/qa-toolkit/mcp-servers/cml-mcp/tests/test_normalizer.py`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/03-normalized-cases.md`

- [ ] **Step 1: 读取 03-normalized-cases.md 确认输出 schema**

  打开 `references/artifact-schemas/03-normalized-cases.md`，记录顶层字段（`artifact_type`、`test_cases`、`quality_metrics`）和 `test_cases` 数组的必填字段。

- [ ] **Step 2: 写失败测试**

  ```python
  # tests/test_normalizer.py
  from normalizer import normalize_cases

  def test_normalize_empty_input():
      result = normalize_cases([])
      assert result["artifact_type"] == "normalized_cases"
      assert result["test_cases"] == []

  def test_normalize_single_case():
      raw_case = {
          "id": "TC-001",
          "title": "正常登录",
          "steps": ["输入用户名", "输入密码", "点击登录"],
          "expected": "跳转首页"
      }
      result = normalize_cases([raw_case])
      assert len(result["test_cases"]) == 1
      assert result["test_cases"][0]["id"] == "TC-001"
      assert result["test_cases"][0]["title"] == "正常登录"
  ```

- [ ] **Step 3: 创建 tests/conftest.py 设置 Python 路径**

  ```python
  # plugins/qa-toolkit/mcp-servers/cml-mcp/tests/conftest.py
  import sys
  import os
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
  ```

- [ ] **Step 4: 运行测试确认失败（预期 ImportError）**

  ```bash
  python -m pytest plugins/qa-toolkit/mcp-servers/cml-mcp/tests/test_normalizer.py -v
  ```
  预期：`ModuleNotFoundError: No module named 'normalizer'`

- [ ] **Step 5: 实现 normalizer.py**

  ```python
  """CML 历史案例规范化器"""
  from typing import Any
  import datetime


  def normalize_cases(raw_cases: list[dict[str, Any]]) -> dict[str, Any]:
      """将 CML 系统原始用例转换为 artifact-schema 03 标准格式。"""
      return {
          "artifact_type": "normalized_cases",
          "version": "1.0",
          "created_at": datetime.datetime.now().isoformat(),
          "normalizer": "cml-mcp",
          "test_cases": [_normalize_single(c) for c in raw_cases],
          "quality_metrics": {
              "total_count": len(raw_cases),
              "processed_count": len(raw_cases),
          },
      }


  def _normalize_single(raw: dict[str, Any]) -> dict[str, Any]:
      return {
          "id": raw.get("id", ""),
          "title": raw.get("title", ""),
          "preconditions": raw.get("preconditions", []),
          "steps": raw.get("steps", []),
          "expected_result": raw.get("expected", raw.get("expected_result", "")),
          "priority": raw.get("priority", "medium"),
          "tags": raw.get("tags", []),
      }
  ```

- [ ] **Step 6: 运行测试确认通过**

  ```bash
  python -m pytest plugins/qa-toolkit/mcp-servers/cml-mcp/tests/test_normalizer.py -v
  ```
  预期：2 tests PASSED

- [ ] **Step 7: 实现 main.py MCP 入口骨架**

  ```python
  """CML MCP - 历史案例规范化 MCP 服务入口（骨架）"""
  import json
  import sys
  from normalizer import normalize_cases


  def handle_request(request: dict) -> dict:
      if request.get("method") == "normalize_cases":
          raw_cases = request.get("params", {}).get("cases", [])
          return {"result": normalize_cases(raw_cases)}
      return {"error": f"Unknown method: {request.get('method')}"}


  if __name__ == "__main__":
      # TODO: 接入 CML 系统 API，替换为真实数据
      request = json.loads(sys.stdin.read())
      response = handle_request(request)
      print(json.dumps(response, ensure_ascii=False))
  ```

- [ ] **Step 8: 创建 README.md**

  说明功能、输出格式（`03-normalized-cases.md`）、骨架状态和运行示例：
  `echo '{"method":"normalize_cases","params":{"cases":[]}}' | python main.py`

- [ ] **Step 9: 提交**

  ```bash
  git add plugins/qa-toolkit/mcp-servers/cml-mcp/
  git commit -m "feat(cml-mcp): add skeleton implementation with normalizer and tests"
  ```

---

### Task 4：Code Diff MCP 骨架（P1）

**负责人**：奕翔
**文件：**
- 创建：`plugins/qa-toolkit/mcp-servers/code-diff-mcp/README.md`
- 创建：`plugins/qa-toolkit/mcp-servers/code-diff-mcp/main.py`
- 创建：`plugins/qa-toolkit/mcp-servers/code-diff-mcp/analyzer.py`
- 创建：`plugins/qa-toolkit/mcp-servers/code-diff-mcp/tests/conftest.py`
- 创建：`plugins/qa-toolkit/mcp-servers/code-diff-mcp/tests/test_analyzer.py`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/04-code-diff-report.md`

- [ ] **Step 1: 读取 04-code-diff-report.md 确认输出 schema**

  打开 `references/artifact-schemas/04-code-diff-report.md`，记录顶层字段（`artifact_type`、`summary`、`changed_files`、`impact_assessment`）和各字段的必填项。

- [ ] **Step 2: 创建 tests/conftest.py 设置 Python 路径**

  ```python
  # plugins/qa-toolkit/mcp-servers/code-diff-mcp/tests/conftest.py
  import sys
  import os
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
  ```

- [ ] **Step 3: 写失败测试**

  ```python
  # tests/test_analyzer.py
  from analyzer import analyze_diff

  def test_analyze_empty_diff():
      result = analyze_diff(repo_path=".", base_branch="main", target_branch="main")
      assert result["artifact_type"] == "code_diff_report"
      assert result["summary"]["total_files_changed"] == 0

  def test_analyze_mock_diff():
      mock_diff = [
          {"path": "src/service/UserService.java", "added": 10, "deleted": 5, "change_type": "modified"},
      ]
      result = analyze_diff(repo_path=".", base_branch="main", target_branch="feature/x", _mock_diff=mock_diff)
      assert result["summary"]["total_files_changed"] == 1
      assert result["changed_files"][0]["path"] == "src/service/UserService.java"
  ```

- [ ] **Step 4: 运行测试确认失败（预期 ImportError）**

  ```bash
  python -m pytest plugins/qa-toolkit/mcp-servers/code-diff-mcp/tests/test_analyzer.py -v
  ```
  预期：`ModuleNotFoundError: No module named 'analyzer'`

- [ ] **Step 5: 实现 analyzer.py**

  ```python
  """Code Diff 分析器 - 分析 Git 代码差异并输出标准化报告"""
  from typing import Any, Optional
  import datetime


  def analyze_diff(
      repo_path: str,
      base_branch: str,
      target_branch: str,
      _mock_diff: Optional[list[dict]] = None,
  ) -> dict[str, Any]:
      """分析两个分支之间的代码差异，输出符合 04-code-diff-report.md 的字典。"""
      raw_diff = _mock_diff if _mock_diff is not None else []
      # TODO: 使用 GitPython 获取真实 diff
      # import git; repo = git.Repo(repo_path); raw_diff = _get_git_diff(...)
      changed_files = [_normalize_file(f) for f in raw_diff]
      return {
          "artifact_type": "code_diff_report",
          "version": "1.0",
          "created_at": datetime.datetime.now().isoformat(),
          "analyzer": "code-diff-mcp",
          "diff_info": {"base_branch": base_branch, "target_branch": target_branch, "repo_path": repo_path},
          "summary": {
              "total_files_changed": len(changed_files),
              "total_lines_added": sum(f["lines_added"] for f in changed_files),
              "total_lines_deleted": sum(f["lines_deleted"] for f in changed_files),
          },
          "changed_files": changed_files,
          "impact_assessment": {
              "risk_level": _assess_risk(changed_files),
              "affected_interfaces": [],  # TODO: AI 辅助识别
              "test_suggestions": [],
          },
      }


  def _normalize_file(raw: dict[str, Any]) -> dict[str, Any]:
      return {
          "path": raw.get("path", ""),
          "change_type": raw.get("change_type", "modified"),
          "lines_added": raw.get("added", 0),
          "lines_deleted": raw.get("deleted", 0),
      }


  def _assess_risk(changed_files: list[dict]) -> str:
      total = sum(f["lines_added"] + f["lines_deleted"] for f in changed_files)
      if total > 500 or len(changed_files) > 20:
          return "high"
      elif total > 100 or len(changed_files) > 5:
          return "medium"
      return "low"
  ```

- [ ] **Step 6: 运行测试确认通过**

  ```bash
  python -m pytest plugins/qa-toolkit/mcp-servers/code-diff-mcp/tests/test_analyzer.py -v
  ```
  预期：2 tests PASSED

- [ ] **Step 7: 实现 main.py 入口骨架**

  ```python
  """Code Diff MCP - Git 代码差异分析 MCP 服务入口（骨架）"""
  import json
  import sys
  from analyzer import analyze_diff


  def handle_request(request: dict) -> dict:
      if request.get("method") == "analyze_diff":
          params = request.get("params", {})
          result = analyze_diff(
              repo_path=params.get("repo_path", "."),
              base_branch=params.get("base_branch", "main"),
              target_branch=params.get("target_branch", "HEAD"),
          )
          return {"result": result}
      return {"error": f"Unknown method: {request.get('method')}"}


  if __name__ == "__main__":
      # TODO: 接入 GitPython 获取真实 diff
      request = json.loads(sys.stdin.read())
      response = handle_request(request)
      print(json.dumps(response, ensure_ascii=False))
  ```

- [ ] **Step 8: 创建 README.md**

  说明功能、输出格式（`04-code-diff-report.md`）、骨架状态（TODO: GitPython 接入、AI 辅助接口识别）和运行示例：
  `echo '{"method":"analyze_diff","params":{"repo_path":".","base_branch":"main","target_branch":"feature/x"}}' | python main.py`

- [ ] **Step 9: 提交**

  ```bash
  git add plugins/qa-toolkit/mcp-servers/code-diff-mcp/
  git commit -m "feat(code-diff-mcp): add skeleton implementation with analyzer and tests"
  ```

---

### Task 5：`/qa-full` 完整工作流命令（P1）

**负责人**：鼎中
**文件：**
- 修改：`plugins/qa-toolkit/commands/full-workflow.md`
- 参考：`plugins/qa-toolkit/commands/quick-workflow.md`（模式参照）

- [ ] **Step 1: 阅读 quick-workflow.md 理解命令结构**

  打开 `commands/quick-workflow.md`，记录 YAML frontmatter 结构（name, description, arguments）和各阶段描述格式。

- [ ] **Step 2: 确认现有 full-workflow.md 中需保留的内容**

  打开 `commands/full-workflow.md`（当前约 305 行），识别：
  - **保留**：四阶段流程图（第22-68行）、分阶段执行参数 `--stage`（第124-144行）、输入/输出目录结构（第146-179行）、完整模式 vs 快速模式对比表（第181-192行）
  - **删除**：开发中状态提示（第14-20行）、"预期使用方式（4月20日后）"标题、"当前可用替代方案"章节、开发路线图章节
  - **更新**：状态从🚧开发中改为✅可用，补充实际执行流程的 Step-by-Step 说明

- [ ] **Step 3: 重写 full-workflow.md**

  新文件内容章节顺序：
  1. 状态标记：✅ 可用
  2. 四阶段流程图（保留原 ASCII 图，更新各阶段状态为✅）
  3. 执行流程 Step-by-Step（新增）：准备阶段收集输入 → 第一阶段规范化（产出至 `./result/[项目名]/artifacts/`）→ 第二阶段需求检查（P0 问题则暂停）→ 第三阶段手工案例 → 第四阶段 API 案例 → 汇总
  4. 分阶段执行参数（保留现有 `--stage` 说明）
  5. 输入/输出目录结构（保留）
  6. 完整模式 vs 快速模式对比表（保留，更新状态列为✅）
  7. 前提条件（新增：需要哪些 Skill/MCP 激活）

- [ ] **Step 4: 验证文件写入正确**

  搜索"开发中"关键词确认已删除，确认"✅ 可用"存在。

- [ ] **Step 5: 提交**

  ```bash
  git add plugins/qa-toolkit/commands/full-workflow.md
  git commit -m "feat(commands): complete qa-full workflow command with step-by-step execution guide"
  ```

---

### Task 6：manual-case-generator 适配标准格式（P2）

**负责人**：宇宸
**文件：**
- 修改：`plugins/qa-toolkit/skills/manual-case-generator/SKILL.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/01-normalized-requirement-v2.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/05-validation-report.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/06-manual-test-cases.md`

- [ ] **Step 1: 阅读当前 SKILL.md 的输入/输出规范**

  打开 `skills/manual-case-generator/SKILL.md`，记录当前输入格式、输出产物、需要改动的章节。

- [ ] **Step 2: 阅读 artifact-schemas 06 的输出格式**

  打开 `references/artifact-schemas/06-manual-test-cases.md`，确认输出 YAML 的顶层字段和手工用例的必填字段。

- [ ] **Step 3: 在 "📥 输入" 章节添加标准化输入支持**

  ```markdown
  ### 完整模式输入（推荐）
  当以下标准化文件存在时，优先使用：
  - `01-normalized-requirement.yaml`（来自 requirement-normalizer）
  - `02-normalized-design.yaml`（来自 design-normalizer，可选）
  - `05-validation-report.yaml`（来自 requirement-validator，用于测试重点识别）

  从标准化需求中读取：
  - `requirements[].acceptance_criteria` → 测试用例基础
  - `requirements[].test_focus == true` → 重点测试标记
  - `requirements[].risk_level` → 用例优先级
  - `test_scenarios[].given_when_then` → 直接转换为测试步骤
  ```

- [ ] **Step 4: 在 "📤 输出" 章节添加标准化输出说明**

  ```markdown
  ### 标准化输出
  完整模式下，同时输出：
  - `06-manual-test-cases.yaml`（符合 references/artifact-schemas/06-manual-test-cases.md）
  - `manual-cases.md`（PlantUML + XMind，供人工查阅）
  ```

- [ ] **Step 5: 提交**

  ```bash
  git add plugins/qa-toolkit/skills/manual-case-generator/SKILL.md
  git commit -m "feat(manual-case-generator): adapt to artifact-schema standard input/output"
  ```

---

### Task 7：requirement-validator 适配标准格式（P2）

**负责人**：宇豪
**文件：**
- 修改：`plugins/qa-toolkit/skills/requirement-validator/SKILL.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/01-normalized-requirement-v2.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/02-normalized-design.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/05-validation-report.md`

- [ ] **Step 1: 阅读当前 SKILL.md 的输入/输出规范**

  记录当前输入格式和输出格式，确认需要修改的章节。

- [ ] **Step 2: 更新 "📥 输入" 章节**

  添加标准化输入说明（读取 01、02、04 格式的字段位置）。

- [ ] **Step 3: 更新 "📤 输出" 章节**

  说明输出格式符合 `05-validation-report.md`，包含 `validation_summary`、`p0_issues`、`p1_issues`、`p2_issues`、`decision`（pass/fix_required/blocked）。

- [ ] **Step 4: 在 References 章节添加引用**

  ```markdown
  - references/01-validation-rules.md
  - references/02-artifact-schema-refs.md
  ```
  （无 `./` 前缀，符合项目规范）

- [ ] **Step 5: 提交**

  ```bash
  git add plugins/qa-toolkit/skills/requirement-validator/SKILL.md
  git commit -m "feat(requirement-validator): adapt to artifact-schema standard input/output"
  ```

---

### Task 8：api-case-generator 确认标准格式适配（P2）

**负责人**：泉政
**背景**：`api-case-generator` v2.0 已重构完成，本 Task 验证并在 SKILL.md 中补充标准格式引用说明。
**文件：**
- 修改：`plugins/qa-toolkit/skills/api-case-generator/SKILL.md`（仅在缺少标准格式引用时修改）
- 参考：`plugins/qa-toolkit/references/artifact-schemas/02-normalized-design.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/06-manual-test-cases.md`
- 参考：`plugins/qa-toolkit/references/artifact-schemas/07-api-test-cases.md`

- [ ] **Step 1: 阅读 SKILL.md 当前输入说明**

  打开 `skills/api-case-generator/SKILL.md`，确认 "📥 输入" 章节是否已说明读取 `02-normalized-design.yaml` 和 `06-manual-test-cases.yaml`。

- [ ] **Step 2: 若缺少标准格式引用，在输入章节补充说明**

  ```markdown
  ### 完整模式输入（推荐）
  - `02-normalized-design.yaml`（来自 design-normalizer）：
    - `interfaces[].path` → 接口路径
    - `interfaces[].method` → HTTP 方法
    - `interfaces[].request_params` → 请求参数
    - `interfaces[].response_schema` → 响应结构
  - `06-manual-test-cases.yaml`（来自 manual-case-generator，可选）：
    - `test_cases[].steps` → 辅助生成测试数据
    - `test_cases[].related_interfaces` → 用例关联接口
  ```

- [ ] **Step 3: 确认输出符合 07-api-test-cases.md**

  打开 `references/artifact-schemas/07-api-test-cases.md`，确认生成的 Python + YAML 代码符合其结构。如有差异，在输出章节注明。

- [ ] **Step 4: 提交**

  ```bash
  git add plugins/qa-toolkit/skills/api-case-generator/SKILL.md
  git commit -m "feat(api-case-generator): document standard artifact-schema input alignment"
  ```

---

### Task 9：端到端文档验收（P2）

**负责人**：鼎中
**文件：**
- 修改：`plugins/qa-toolkit/commands/help.md`
- 修改：`plugins/qa-toolkit/commands/status.md`
- 修改：`plugins/qa-toolkit/README.md`
- 修改：`plugins/qa-toolkit/.claude-plugin/plugin.json`
- 修改：`CLAUDE.md`（项目根目录）
- 修改：`PLAN.md`（更新里程碑进展）

- [ ] **Step 1: 更新 help.md**

  将 `/qa-full` 状态从「开发中」改为「可用」，补充使用说明。

- [ ] **Step 2: 更新 status.md**

  将完整模式状态从 🚧 改为 ✅，列出四个阶段的组件状态。

- [ ] **Step 3: 更新 plugins/qa-toolkit/README.md**

  完整模式状态更新为「可用」，添加 `/qa-full` 命令使用示例，更新 design-normalizer 状态为 ✅。

- [ ] **Step 4: 更新 CLAUDE.md（项目根目录）**

  在 "🚀 常用命令" 章节添加：
  ```bash
  # 完整模式（四阶段流程：规范化→需求检查→手工案例→API案例）
  /qa-full ./docs/
  ```
  在工作流模式章节将完整模式状态从 🚧 更新为 ✅。

- [ ] **Step 5: 更新 plugin.json 版本号**

  ```json
  { "version": "1.3.0" }
  ```

- [ ] **Step 6: 更新 PLAN.md 里程碑进展**

  将各完成任务标记为 ✅，更新时间戳。

- [ ] **Step 7: 验收自查清单**

  - [ ] `skills/design-normalizer/SKILL.md` 存在且包含 frontmatter
  - [ ] `skills/design-normalizer/references/` 有 2 个文档
  - [ ] `skills/requirement-validator/references/` 有 2 个文档
  - [ ] `mcp-servers/cml-mcp/` 有 main.py + normalizer.py + tests/conftest.py + tests/test_normalizer.py
  - [ ] `mcp-servers/code-diff-mcp/` 有 main.py + analyzer.py + tests/conftest.py + tests/test_analyzer.py
  - [ ] `commands/full-workflow.md` 状态为✅且有 Step-by-Step 执行说明
  - [ ] `skills/manual-case-generator/SKILL.md` 包含标准化输入说明
  - [ ] `skills/requirement-validator/SKILL.md` 包含标准化输入/输出说明
  - [ ] `skills/api-case-generator/SKILL.md` 包含 02/06 标准格式引用
  - [ ] `CLAUDE.md` 包含 `/qa-full` 使用示例
  - [ ] `plugin.json` 版本号为 1.3.0

- [ ] **Step 8: 最终提交**

  ```bash
  git add plugins/qa-toolkit/commands/help.md plugins/qa-toolkit/commands/status.md
  git add plugins/qa-toolkit/README.md plugins/qa-toolkit/.claude-plugin/plugin.json
  git add CLAUDE.md PLAN.md
  git commit -m "chore: release qa-toolkit v1.3.0 with full mode support"
  ```

---

### 里程碑检查点

| 里程碑 | 对应 Task | 验证方式 |
|--------|-----------|----------|
| design-normalizer 可用 | Task 1 完成 | `skills/design-normalizer/SKILL.md` 存在且包含 frontmatter |
| requirement-validator 文档完整 | Task 2 完成 | `skills/requirement-validator/references/` 有 2 个文档 |
| MCP 骨架可测试 | Task 3+4 完成 | `python -m pytest plugins/qa-toolkit/mcp-servers/cml-mcp/tests/ plugins/qa-toolkit/mcp-servers/code-diff-mcp/tests/ -v` 全部通过 |
| `/qa-full` 命令可调用 | Task 5 完成 | `commands/full-workflow.md` 状态为✅且有 Step-by-Step 执行说明 |
| 四个 Skill 全部适配标准格式 | Task 6+7+8 完成 | 各 SKILL.md 包含标准化格式输入/输出说明 |
| v1.3.0 发布 | Task 9 完成 | `plugin.json` 版本号 = 1.3.0，`CLAUDE.md` 包含 `/qa-full` 示例 |

### 依赖关系

```
Task 1 (design-normalizer SKILL.md) ─────────────────┐
Task 2 (requirement-validator references) ────────────┤
Task 3 (CML MCP) ──────────────────── 独立            │
Task 4 (Code Diff MCP) ─────────────── 独立           │
Task 8 (api-case-generator 确认) ───── 独立           │
                                                       ↓
Task 1 + Task 2 → Task 5 (qa-full command)         全部完成
Task 1 → Task 6 (manual-case-generator 适配)          ↓
Task 2 → Task 7 (requirement-validator 适配)        Task 9
```

**建议执行顺序**：
1. 并行：Task 1 + Task 2 + Task 3 + Task 4 + Task 8
2. 待 Task 1+2 完成：Task 5 + Task 6 + Task 7（可并行）
3. 最后：Task 9

### 阶段 1：定义标准化格式（P0）✅ 已完成（2026-03-19）

#### 任务 1.1：创建 artifact-schemas 目录结构 ✅

**负责人**：鼎中
**完成时间**：2026-03-19
**交付物**：

```
plugins/qa-toolkit/references/artifact-schemas/
├── 00-overview.md           ✅
├── 01-normalized-requirement-v2.md  ✅
├── 02-normalized-design.md  ✅
├── 03-normalized-cases.md   ✅
├── 04-code-diff-report.md   ✅
├── 05-validation-report.md  ✅
├── 06-manual-test-cases.md  ✅
└── 07-api-test-cases.md     ✅
```

#### 任务 1.2：编写 00-overview.md（总览）✅

**负责人**：鼎中
**完成时间**：2026-03-19
**内容**：
- 标准化格式的设计原则（以产品标准为主）
- 四阶段 Skill 交互流程图
- 格式版本管理策略
- 七种格式依赖关系矩阵

#### 任务 1.3：定义第一阶段输出格式（01-04）✅

**负责人**：鼎中
**完成时间**：2026-03-19

| 文档 | 状态 | 说明 |
|------|------|------|
| 01-normalized-requirement-v2.md | ✅ | 对齐 ZA Bank PRD 7章，含完整示例 |
| 02-normalized-design.md | ✅ | 对齐 ZA Bank 设计文档模板，含完整示例 |
| 03-normalized-cases.md | ✅ | 支持 Excel/XMind 提取，含案例推荐逻辑 |
| 04-code-diff-report.md | ✅ | 支持 Git Diff 分析、影响评估、发布建议 |

**重要决策**：采用"以产品的标准为主"原则，需求文档格式升级为 v2.0，100% 对齐 ZA Bank 模板。

#### 任务 1.4：定义后续阶段输出格式（05-07）✅

**负责人**：鼎中
**完成时间**：2026-03-19

| 文档 | 状态 | 说明 |
|------|------|------|
| 05-validation-report.md | ✅ | 三级检查（P0/P1/P2），含决策建议 |
| 06-manual-test-cases.md | ✅ | 支持 PlantUML/XMind/Markdown 输出 |
| 07-api-test-cases.md | ✅ | Python pytest 代码规范 + YAML 多环境数据 |

#### 任务 1.5：格式评审和修订 ⏳

**负责人**：嘉龙
**状态**：待评审
**评审要点**：
- 格式是否可解析（能否用 YAML/JSON 解析）
- 字段是否完整（覆盖业务需求）
- 是否易于扩展（可选字段和必选字段清晰）
- 示例文件是否准确反映实际项目

### 阶段 2：SpecKit 集成或自研方案（P0）✅ 决策完成（2026-03-18）

#### 任务 2.1：SpecKit 能力评估 ✅

**负责人**：鼎中
**完成时间**：2026-03-18
**评估结论**：SpecKit 是一套提示词模式，非独立工具

| 维度 | 评估结论 |
|------|---------|
| 输出格式 | SpecKit 本身是提示词，无固定输出格式 |
| 集成方式 | 将 SpecKit 提示词融入 Skill 实现中 |
| 字段覆盖 | 以 ZA Bank 产品标准为主，融合 SpecKit 最佳实践 |
| 质量保证 | 引入三级检查（P0/P1/P2）和置信度标注 |

**决策**：采用方案 B（自研 Skill），将 SpecKit 提示词模式融入 requirement-normalizer 和 design-normalizer 的实现逻辑中。

**关键原则**：「以产品的标准为主」— 格式 100% 对齐 ZA Bank PRD 和设计文档模板。

#### 任务 2.2A：SpecKit MCP 适配层开发（方案 A）

**前提**：SpecKit 评估通过
**负责人**：鼎中 + 陈贝
**时间**：3 天

**实现内容**：

```python
# plugins/qa-toolkit/mcp-servers/speckit-mcp/
#
# 功能：
# 1. 调用 SpecKit API/CLI
# 2. 将 SpecKit 输出转换为 artifact-schemas 标准格式
# 3. 验证输出格式（必选字段检查）
# 4. 处理异常情况（SpecKit 失败时的降级策略）
```

**验证标准**：
- ✅ 能够读取 .docx 需求文档并输出符合 01-normalized-requirement.md 的 YAML
- ✅ 能够读取 .docx 设计文档并输出符合 02-normalized-design.md 的 YAML
- ✅ 单元测试覆盖率 > 80%

#### 任务 2.2B：自研需求/设计规范化 Skill（方案 B）

**前提**：SpecKit 不适合集成
**负责人**：陈贝
**时间**：7 天（需求规范化 3.5 天 + 设计规范化 3.5 天）

**实现内容**：

```python
# plugins/qa-toolkit/skills/requirement-normalizer/
# plugins/qa-toolkit/skills/design-normalizer/
#
# 功能：
# 1. 解析 .docx 文档（使用 python-docx）
# 2. 提取关键信息（需求/接口/参数等）
# 3. 转换为 artifact-schemas 标准格式
# 4. AI 辅助提取（使用 Claude API）
```

**技术方案**：
- 使用 python-docx 解析 Word 文档
- 使用正则表达式提取结构化信息
- 使用 Claude API 提取复杂字段（如验收标准）
- 输出 YAML 格式

**验证标准**：
- ✅ 能够处理至少 3 种常见需求文档模板
- ✅ 关键字段提取准确率 > 90%
- ✅ 单元测试覆盖率 > 80%

### 阶段 3：其他规范化组件开发（P1）

#### 任务 3.1：CML MCP 开发（历史案例规范化）

**负责人**：泉政
**时间**：5 天
**输入**：CML 系统的历史测试用例
**输出**：符合 03-normalized-cases.md 的 YAML 文件

**实现内容**：
```python
# plugins/qa-toolkit/mcp-servers/cml-mcp/
#
# 功能：
# 1. 连接 CML 系统 API
# 2. 查询历史测试用例
# 3. 转换为标准化格式（test_cases, quality_metrics）
# 4. 可选：案例质量评分
```

**验证标准**：
- ✅ 能够从 CML 系统提取用例
- ✅ 输出符合 03-normalized-cases.md 格式
- ✅ 单元测试覆盖率 > 70%

#### 任务 3.2：Code Diff MCP 开发（代码差异分析）

**负责人**：奕翔
**时间**：5 天
**输入**：Git 仓库 + base_branch + target_branch
**输出**：符合 04-code-diff-report.md 的 YAML 文件

**实现内容**：
```python
# plugins/qa-toolkit/mcp-servers/code-diff-mcp/
#
# 功能：
# 1. 使用 GitPython 获取代码差异
# 2. 分析变更影响（文件级别 + 函数级别）
# 3. 识别关联接口（可选：AI 辅助）
# 4. 评估影响级别（high/medium/low）
```

**验证标准**：
- ✅ 能够准确统计变更文件和行数
- ✅ 输出符合 04-code-diff-report.md 格式
- ✅ 单元测试覆盖率 > 70%

### 阶段 4：现有 Skill 适配标准格式（P1）

#### 任务 4.1：更新 requirement-validator

**负责人**：宇豪
**时间**：2 天
**改动**：

1. **输入适配**：
   - 读取符合 01-normalized-requirement.md 的需求文档
   - 读取符合 02-normalized-design.md 的设计文档
   - 读取符合 04-code-diff-report.md 的代码差异报告

2. **输出适配**：
   - 输出符合 05-validation-report.md 的需求检查报告

3. **SKILL.md 更新**：
   - 在 references 中引用 artifact-schemas 文档

#### 任务 4.2：更新 manual-case-generator

**负责人**：宇宸
**时间**：2 天
**改动**：

1. **输入适配**：
   - 读取第一阶段的 4 个标准化产出物
   - 读取 05-validation-report.md 的测试重点建议

2. **输出适配**：
   - 输出符合 06-manual-test-cases.md 的手工测试用例

#### 任务 4.3：更新 api-case-generator

**负责人**：泉政
**时间**：2 天
**改动**：

1. **输入适配**：
   - 读取 02-normalized-design.md 的接口信息
   - 读取 06-manual-test-cases.md 的用例逻辑

2. **输出适配**：
   - 输出符合 07-api-test-cases.md 的 API 测试用例

### 阶段 5：工作流命令和集成测试（P1）

#### 任务 5.1：实现 /qa-full 工作流命令

**负责人**：鼎中
**时间**：2 天
**功能**：

```bash
# 用法
/qa-full ./project-root

# 执行流程
[第一阶段] 规范化
  → 需求文档规范化（SpecKit MCP）
  → 设计文档规范化（SpecKit MCP）
  → 历史案例规范化（CML MCP）
  → 代码差异分析（Code Diff MCP）
  ✅ 产出 4 个标准化文件

[第二阶段] 需求检查
  → requirement-validator
  ✅ 产出需求检查报告

[第三阶段] 手工案例生成
  → manual-case-generator
  ✅ 产出手工测试用例

[第四阶段] API 案例生成
  → api-case-generator
  ✅ 产出 API 自动化测试代码

[总结] 显示执行结果
  → 列出所有产出文件
  → 显示质量指标（覆盖率、风险点数量等）
```

**实现位置**：`plugins/qa-toolkit/commands/full-workflow.md`

**参考**：`plugins/qa-toolkit/commands/quick-workflow.md`（快速模式实现）

#### 任务 5.2：端到端流程测试

**负责人**：慧芳（质量保证）
**时间**：2 天
**测试场景**：

| 场景 | 输入 | 预期输出 |
|------|------|----------|
| 完整模式正常流程 | 需求.docx + 设计.docx + Git 仓库 | 4 阶段产出物全部生成 |
| 缺少历史案例 | 需求.docx + 设计.docx（无 CML 数据） | 第三阶段降级（不使用历史案例） |
| 需求文档格式错误 | 不规范的需求.docx | 第一阶段报错，给出明确提示 |

**验证标准**：
- ✅ 正常流程无报错
- ✅ 异常场景有明确提示
- ✅ 产出文件格式正确

#### 任务 5.3：文档更新

**负责人**：鼎中
**时间**：1 天
**需要更新的文档**：

1. **README.md**：
   - 更新完整模式状态为"✅ 已完成"
   - 更新 `/qa-full` 命令状态
   - 更新实施计划

2. **CLAUDE.md**：
   - 添加 `/qa-full` 使用示例
   - 更新工作流模式说明
   - 添加 artifact-schemas 路径

3. **plugins/qa-toolkit/README.md**：
   - 更新工作流命令表格
   - 添加完整模式使用指南

4. **plugins/qa-toolkit/commands/help.md**：
   - 添加 `/qa-full` 命令说明

5. **插件配置文件**：
   - 更新 `plugin.json` 版本号：1.2.0 → 1.3.0

---

## 风险管理

### 高风险（需要立即处理）

#### 风险 1：SpecKit 不适合集成

**概率**：中（40%）
**影响**：高（需要自研，7 天额外工作量）
**缓解措施**：
- Week 1 完成 SpecKit 评估（Day 5）
- 如果不适合，立即启动方案 B（自研）
- 需求规范化和设计规范化技术方案可复用，先完成一个

**应急计划**：
- 如果时间不够，可以先只实现需求规范化，设计规范化延后到 Q2

#### 风险 2：时间不足（33 天完成 4 个组件）

**概率**：高（60%）
**影响**：高（无法按期交付）
**缓解措施**：
- 并行开发：CML MCP 和 Code Diff MCP 与 SpecKit 集成并行进行
- 减少范围：如果时间紧张，第一版可以不包含"可选功能"（如历史案例质量评分）
- 每周评审：每周五检查进度，及时调整

**应急计划**：
- 如果无法完成所有组件，优先保证"需求规范化 + 需求检查 + API 案例生成"（砍掉手工案例生成）

#### 风险 3：标准化格式定义不合理

**概率**：中（30%）
**影响**：高（后续所有开发返工）
**缓解措施**：
- Week 1 完成格式定义后，立即进行团队评审
- 邀请各组件负责人参与评审（陈贝、泉政、奕翔、宇豪、宇宸）
- 使用一个真实案例验证格式可行性

**应急计划**：
- 如果发现格式不合理，立即修订（预留 1 天 buffer）

### 中风险（需要密切关注）

#### 风险 4：各组件开发进度不一致

**概率**：高（50%）
**影响**：中（影响集成测试）
**缓解措施**：
- 每周例会同步进度
- 使用 mock 数据提前测试集成（不等所有组件完成）

#### 风险 5：AI 辅助提取准确率不足

**概率**：中（40%）
**影响**：中（需要人工复核）
**缓解措施**：
- 在需求规范化中增加"人工复核"环节（输出待确认字段）
- 使用更强的模型（Claude Opus）提高准确率

### 低风险（持续监控）

#### 风险 6：CML 系统 API 不稳定

**概率**：低（20%）
**影响**：中（历史案例无法提取）
**缓解措施**：
- 提前与 CML 系统负责人沟通，确认 API 可用性
- 实现重试机制和降级策略（如果 CML 不可用，跳过历史案例）

---

## 验收标准

### 功能验收

#### 第一阶段：规范化组件

| 组件 | 验收标准 |
|------|----------|
| 需求规范化 | ✅ 能够读取 .docx 需求文档并输出符合 01-normalized-requirement.md 的 YAML<br>✅ 关键字段提取准确率 > 90%<br>✅ 单元测试覆盖率 > 80% |
| 设计规范化 | ✅ 能够读取 .docx 设计文档并输出符合 02-normalized-design.md 的 YAML<br>✅ 接口信息提取准确率 > 95%<br>✅ 单元测试覆盖率 > 80% |
| CML MCP | ✅ 能够从 CML 系统提取历史用例<br>✅ 输出符合 03-normalized-cases.md 格式<br>✅ 单元测试覆盖率 > 70% |
| Code Diff MCP | ✅ 能够准确统计代码变更<br>✅ 输出符合 04-code-diff-report.md 格式<br>✅ 单元测试覆盖率 > 70% |

#### 第二、三、四阶段：现有 Skill 适配

| Skill | 验收标准 |
|-------|----------|
| requirement-validator | ✅ 能够读取标准化输入格式<br>✅ 输出符合 05-validation-report.md 格式<br>✅ 需求对齐度检查准确率 > 90% |
| manual-case-generator | ✅ 能够读取标准化输入格式<br>✅ 输出符合 06-manual-test-cases.md 格式<br>✅ 生成的用例覆盖核心业务流程 |
| api-case-generator | ✅ 能够读取标准化输入格式<br>✅ 输出符合 07-api-test-cases.md 格式<br>✅ 生成的代码可执行且通过 pytest |

#### 工作流命令

| 命令 | 验收标准 |
|------|----------|
| /qa-full | ✅ 能够一键执行四阶段流程<br>✅ 自动检测输入文件路径<br>✅ 详细执行反馈和错误处理<br>✅ 支持中断和恢复功能 |

### 质量验收

| 指标 | 目标 | 验收方式 |
|------|------|----------|
| 单元测试覆盖率 | > 75%（整体） | pytest --cov |
| 端到端测试通过率 | 100%（3 个场景） | 手动测试 + 自动化测试 |
| 文档完整性 | 100% | 检查清单（见下） |
| 代码质量 | 无严重 Bug | Code Review + 静态分析 |

### 文档验收清单

- [ ] artifact-schemas 7 个文档完整且评审通过
- [ ] README.md 更新完整模式状态
- [ ] CLAUDE.md 更新 `/qa-full` 使用示例
- [ ] plugins/qa-toolkit/README.md 更新工作流命令
- [ ] plugins/qa-toolkit/commands/help.md 更新命令列表
- [ ] plugins/qa-toolkit/commands/full-workflow.md 创建完成
- [ ] 各 Skill 的 SKILL.md 引用 artifact-schemas
- [ ] plugin.json 版本号更新为 1.3.0

---

## 附录

### 团队分工

| 成员 | 负责组件 | 工作量（人天） |
|------|----------|----------------|
| 鼎中 | artifact-schemas 定义、SpecKit 集成、/qa-full 命令 | 10 天 |
| 陈贝 | 需求规范化、设计规范化（SpecKit 或自研） | 7 天 |
| 泉政 | CML MCP、api-case-generator 适配 | 7 天 |
| 奕翔 | Code Diff MCP | 5 天 |
| 宇豪 | requirement-validator 适配 | 2 天 |
| 宇宸 | manual-case-generator 适配 | 2 天 |
| 慧芳 | 端到端测试、质量验收 | 2 天 |
| 嘉龙 | 项目管理、评审、验收 | 3 天（分散） |

**总工作量**：约 38 人天
**可用资源**：5 周 × 7 人 × 10%（项目投入占比）= 35 人天
**结论**：资源紧张，需要高效协作和风险缓解措施

### 沟通机制

- **每周例会**：每周一 14:00-15:00，嘉龙主持，同步进度
- **技术评审**：Week 1 结束（03-24）评审 artifact-schemas
- **风险升级**：遇到阻塞问题，立即通知嘉龙和鼎中
- **日常沟通**：使用项目群（企业微信/钉钉），及时响应

### 关键决策记录

| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-03-18 | 定义标准化产出物格式（artifact-schemas） | 解决 Skill 间交互标准缺失问题 |
| 2026-03-18 | SpecKit 集成方案：采用方案 B（自研） | SpecKit 是提示词模式，以产品标准为主 |
| 2026-03-19 | api-case-generator v2.0 重构 | 完全适配银行标准测试框架，提升通用性和可维护性 |

### 参考文档

- [README.md](./README.md) - 项目完整文档
- [CLAUDE.md](./CLAUDE.md) - 开发指南
- [architecture.puml](./architecture.puml) - 系统架构图
- [plugins/qa-toolkit/README.md](./plugins/qa-toolkit/README.md) - qa-toolkit 使用指南

---

**计划维护**：
- 本计划每周更新一次（每周一例会后）
- 重大变更需要团队评审通过
- 版本历史记录在文件末尾

---

**版本历史**：
- v1.0 (2026-03-18)：初始版本，定义四阶段实施计划
- v1.1 (2026-03-19)：完成 artifact-schemas 定义（7个文档+2个示例）
- v1.2 (2026-03-19)：完成 api-case-generator v2.0 重构，适配银行标准测试框架
