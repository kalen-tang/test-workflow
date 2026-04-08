# 标准化需求文档格式规范

**版本**: v1.0
**创建时间**: 2026-03-18
**适用阶段**: 第一阶段（需求文档规范化）
**输出工具**: requirement-normalizer Skill

---

## 📋 目录

- [概述](#概述)
- [YAML 结构定义](#yaml-结构定义)
- [字段说明](#字段说明)
- [提取规则](#提取规则)
- [一致性检查](#一致性检查)
- [使用示例](#使用示例)
- [与后续阶段对接](#与后续阶段对接)

---

## 概述

### 目标

将原始需求文档（Word/PDF/Markdown/文本）标准化为结构化的 YAML 格式，为后续阶段提供统一的输入接口。

### 核心原则

1. **结构化优先**：使用 YAML 定义关键信息，便于程序解析
2. **可追溯性**：保留原文来源，记录置信度
3. **可测性导向**：输出包含测试重点、风险等级、测试场景
4. **质量保证**：三级一致性检查（P0/P1/P2）
5. **前向兼容**：支持格式版本升级

### 输入输出

- **输入**：需求文档（Word/PDF/Markdown/文本）
- **输出**：标准化的 YAML 格式文档 + 一致性检查报告

---

## YAML 结构定义

### 完整结构

```yaml
# ============================================
# 元数据（Metadata）
# ============================================
artifact_type: normalized_requirement  # 固定值，标识产出物类型
version: "1.0"                        # 格式版本，当前为 1.0
source_files:                         # 必须，源文件列表
  - "需求文档V1.0.docx"
  - "补充需求.pdf"
created_at: "2026-03-18T10:30:00+08:00"  # 必须，ISO 8601 格式
normalizer: "requirement-normalizer"  # 必须，规范化工具名称

metadata:                             # 文档元数据
  module: "用户管理模块"               # 必须，模块名称
  doc_version: "V1.2"                 # 文档版本，如无则填"未知"
  processed_by: "requirement-normalizer v1.0"  # 可选

# ============================================
# 概览（Overview）
# ============================================
overview:
  description: "实现用户注册、登录、权限管理等核心功能"  # 必须，功能概述
  business_value: "提升用户体验，降低运营成本"           # 可选，业务价值

# ============================================
# 功能列表（Features）
# ============================================
features:                             # 必须，至少一个功能
  - id: F001                          # 必须，唯一标识
    name: "用户登录"                  # 必须，功能名称
    description: "用户可通过手机号和密码登录系统"  # 必须
    priority: high                    # 必须，枚举值：high/medium/low
    test_focus: true                  # 必须，是否为测试重点（新增字段）
    risk_level: medium                # 必须，枚举值：high/medium/low（新增字段）
    related_interfaces:               # 可选，关联接口（新增字段）
      - "/user/login"
      - "/user/verify"
    source: "需求文档 3.1 节"          # 可选，来源章节
    confidence: high                  # 可选，置信度：high/medium/low

  - id: F002
    name: "密码重置"
    description: "用户忘记密码时可通过短信验证码重置"
    priority: medium
    test_focus: false
    risk_level: low
    related_interfaces:
      - "/user/reset-password"
    source: "需求文档 3.2 节"
    confidence: high

# ============================================
# 用户故事（User Stories）
# ============================================
user_stories:                         # 可选，如果有则填入
  - id: US001
    as: "普通用户"                    # 角色
    want: "通过手机号快速登录"        # 需求
    so_that: "无需记住复杂的用户名"   # 价值
    status: confirmed                 # 枚举值：confirmed/pending
    relates_to: F001                  # 关联功能ID

# ============================================
# 验收标准（Acceptance Criteria）
# ============================================
acceptance_criteria:                  # 必须，每个功能至少一条
  - id: AC001
    description: "用户输入正确的手机号和密码，点击登录按钮，跳转到首页"
    relates_to: F001                  # 可选，关联功能ID
    source: "需求文档 3.1.1"          # 可选，来源章节
    confidence: high                  # 可选，置信度

  - id: AC002
    description: "用户输入错误的密码，显示错误提示'密码错误'"
    relates_to: F001
    source: "需求文档 3.1.2"
    confidence: high

  - id: AC003
    description: "用户连续输错密码3次，账号锁定30分钟"
    relates_to: F001
    source: "推断自安全要求"           # 标注来源
    confidence: medium                # 置信度为 medium

# ============================================
# 业务规则（Business Rules）
# ============================================
business_rules:                       # 可选，如有则填
  - id: BR001
    rule: "手机号必须为11位数字，且以1开头"
    type: data_rule                   # 枚举值：data_rule/calculation_rule/process_rule/permission_rule
    source: "需求文档 4.1"
    confidence: high
    relates_to: [F001, F002]          # 可选，关联功能ID列表

  - id: BR002
    rule: "密码长度必须为8-20位，包含字母和数字"
    type: data_rule
    source: "需求文档 4.2"
    confidence: high
    relates_to: [F001, F002]

  - id: BR003
    rule: "用户连续输错密码3次，账号锁定30分钟"
    type: process_rule
    source: "需求文档 4.3"
    confidence: high
    relates_to: [F001]

# ============================================
# 测试场景（Scenarios）
# ============================================
scenarios:                            # 必须，每个验收标准至少一个场景
  - id: S001
    name: "正常登录-正确账号密码"
    type: positive                    # 必须，枚举值：positive/negative/boundary
    relates_to: AC001                 # 关联验收标准
    given: "用户已注册，手机号为13800138000，密码为Test1234"  # 必须，前置条件
    when: "用户输入手机号13800138000，密码Test1234，点击登录"  # 必须，操作步骤
    then: "跳转到首页，显示用户昵称"                          # 必须，预期结果
    source: requirement               # 可选，来源：requirement/history_bug/supplement
    confidence: high

  - id: S002
    name: "异常登录-错误密码"
    type: negative
    relates_to: AC002
    given: "用户已注册，手机号为13800138000，正确密码为Test1234"
    when: "用户输入手机号13800138000，密码WrongPass，点击登录"
    then: "停留在登录页，显示错误提示'密码错误'"
    source: requirement
    confidence: high

  - id: S003
    name: "异常登录-连续错误3次"
    type: negative
    relates_to: AC003
    given: "用户已注册，已连续输错密码2次"
    when: "用户第3次输入错误密码"
    then: "显示'账号已锁定30分钟'，登录按钮禁用"
    source: requirement
    confidence: medium                # 原文未明确说明UI表现

  - id: S004
    name: "边界-手机号格式错误"
    type: boundary
    relates_to: BR001
    given: "用户在登录页"
    when: "用户输入手机号12345678（不足11位），点击登录"
    then: "显示提示'手机号格式错误'"
    source: supplement                # 从业务规则推断
    confidence: medium

# ============================================
# 字段定义（Fields）
# ============================================
fields:                               # 可选，如果涉及输入输出字段
  - name: "mobile"
    display_name: "手机号"
    type: string
    format: "11位数字"
    required: true
    rules: [BR001]                    # 关联业务规则
    source: "需求文档 5.1"

  - name: "password"
    display_name: "密码"
    type: string
    format: "8-20位，字母+数字"
    required: true
    rules: [BR002]
    source: "需求文档 5.2"

  - name: "remember_me"
    display_name: "记住密码"
    type: boolean
    format: "true/false"
    required: false
    rules: []
    source: "需求文档 5.3"

# ============================================
# 缺失项记录（Missing Items）
# ============================================
missing_items:                        # 必须，记录缺失的内容
  - "未明确说明账号锁定30分钟后是否自动解锁"
  - "未说明密码输入框是否需要显示/隐藏切换"
  - "未说明是否支持第三方登录（微信/支付宝）"

# ============================================
# 一致性检查报告（Consistency Check）
# ============================================
consistency_check:
  summary:
    total_features: 2
    total_ac: 3
    total_scenarios: 4
    total_business_rules: 3
    missing_items_count: 3

  # P0级检查（必须通过）
  p0_checks:
    - check: "功能与验收标准对应"
      rule: "每个功能至少有一个验收标准关联"
      result: pass                    # 枚举值：pass/fail
      failures: []                    # 如果失败，列出缺失的功能ID

    - check: "场景内部逻辑完整"
      rule: "每个场景的given-when-then不能有逻辑矛盾"
      result: pass
      failures: []

    - check: "字段约束一致性"
      rule: "字段定义与业务规则不能冲突"
      result: pass
      failures: []

  # P1级检查（必须记录）
  p1_checks:
    - check: "验收标准与场景对应"
      rule: "每个验收标准至少有一个对应的测试场景"
      result: pass                    # 枚举值：pass/partial/fail
      missing: []                     # 列出没有对应场景的验收标准ID

    - check: "业务规则与场景对应"
      rule: "每个业务规则至少在一个场景中被验证"
      result: partial
      missing: [BR002]                # BR002（密码长度规则）未在场景中验证

    - check: "必填字段测试覆盖"
      rule: "每个必填字段，应有'不填'的负向场景"
      result: partial
      missing: ["password"]           # password 字段缺少"不填"的负向场景

  # P2级检查（建议项）
  p2_checks:
    - check: "正负场景比例"
      rule: "负向场景数量应不少于正向场景数量"
      result: pass                    # 枚举值：pass/suggest_optimize
      positive_count: 1
      negative_count: 2
      boundary_count: 1

    - check: "缺失项记录"
      rule: "所有必须但缺失的内容已在missing_items中记录"
      result: pass
      unrecorded: []

# ============================================
# 建议（Recommendations）
# ============================================
recommendations:                      # 可选，基于检查结果的改进建议
  - priority: high
    action: "补充业务规则 BR002（密码长度）的验证场景"
    reason: "P1 检查发现该业务规则未被场景覆盖"

  - priority: medium
    action: "增加 password 字段的'不填'负向场景"
    reason: "必填字段应有对应的边界场景"

  - priority: low
    action: "明确账号锁定后的解锁机制（自动/手动）"
    reason: "missing_items 中记录的缺失内容"
```

---

## 字段说明

### 必选字段（MUST）

以下字段在任何情况下都必须存在：

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `artifact_type` | string | 固定值 `normalized_requirement`，标识产出物类型 |
| `version` | string | 格式版本，当前为 `"1.0"` |
| `source_files` | array | 源文件列表，至少一个 |
| `created_at` | string | 创建时间，ISO 8601 格式 |
| `normalizer` | string | 规范化工具名称，如 `requirement-normalizer` |
| `metadata.module` | string | 模块名称，从文档标题或内容推断 |
| `metadata.doc_version` | string | 文档版本，如无则填 `"未知"` |
| `overview.description` | string | 功能概述，一句话描述 |
| `features` | array | 功能列表，至少一个功能 |
| `features[].id` | string | 功能唯一标识，建议格式 `F001`, `F002` |
| `features[].name` | string | 功能名称 |
| `features[].description` | string | 功能描述 |
| `features[].priority` | enum | 优先级：`high` / `medium` / `low` |
| `features[].test_focus` | boolean | 是否为测试重点 |
| `features[].risk_level` | enum | 风险等级：`high` / `medium` / `low` |
| `acceptance_criteria` | array | 验收标准列表，每个功能至少一条 |
| `acceptance_criteria[].id` | string | 验收标准唯一标识，建议格式 `AC001` |
| `acceptance_criteria[].description` | string | 验收标准描述 |
| `scenarios` | array | 测试场景列表，每个验收标准至少一个场景 |
| `scenarios[].id` | string | 场景唯一标识，建议格式 `S001` |
| `scenarios[].name` | string | 场景名称 |
| `scenarios[].type` | enum | 场景类型：`positive` / `negative` / `boundary` |
| `scenarios[].given` | string | 前置条件 |
| `scenarios[].when` | string | 操作步骤 |
| `scenarios[].then` | string | 预期结果 |
| `missing_items` | array | 缺失项列表 |
| `consistency_check` | object | 一致性检查报告 |

### 可选字段（OPTIONAL）

以下字段根据实际情况选择性填写：

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `overview.business_value` | string | 业务价值 |
| `features[].related_interfaces` | array | 关联接口列表 |
| `features[].source` | string | 来源章节 |
| `features[].confidence` | enum | 置信度：`high` / `medium` / `low` |
| `user_stories` | array | 用户故事列表 |
| `business_rules` | array | 业务规则列表 |
| `fields` | array | 字段定义列表 |
| `recommendations` | array | 改进建议列表 |

### 新增字段说明（相比原 SpecKit）

以下字段是为了支持 qa-toolkit 完整模式而新增的：

1. **`artifact_type`**：统一标识产出物类型，便于后续阶段识别
2. **`version`**：格式版本，支持未来升级
3. **`normalizer`**：规范化工具名称，可追溯
4. **`features[].test_focus`**：标注测试重点，指导第三阶段优先生成哪些用例
5. **`features[].risk_level`**：风险等级，支持风险驱动测试
6. **`features[].related_interfaces`**：关联接口，供第四阶段 API 用例生成使用

---

## 提取规则

### 1. 置信度标记

在提取时，对每个字段标注置信度（写在 `confidence` 字段中）：

| 置信度 | 说明 | 示例 |
|--------|------|------|
| `high` | 原文明确写出，无歧义 | "手机号必须为11位数字"（原文原话） |
| `medium` | 原文隐含，需要推断或确认 | "用户需注册才能登录"（原文未明确，从上下文推断） |
| `low` | 原文未提，从上下文或常识推测 | "支持记住密码"（原文未提，从业界惯例推测） |

**原则**：
- 如果置信度为 `medium` 或 `low`，应在 `source` 字段说明原因
- 低置信度的内容应在 `missing_items` 中记录，提醒人工确认

### 2. 测试重点标注（test_focus）

判断是否为测试重点的标准：

| 标准 | test_focus |
|------|-----------|
| 核心业务流程（如登录、支付） | `true` |
| 高风险功能（涉及资金、隐私） | `true` |
| 原文明确标注为"重要"、"核心" | `true` |
| 辅助功能（如记住密码、显示历史记录） | `false` |
| 低优先级功能（priority: low） | `false` |

### 3. 风险等级标注（risk_level）

判断风险等级的标准：

| 风险等级 | 判断标准 |
|---------|---------|
| `high` | 涉及资金、隐私、安全；业务影响范围大；技术复杂度高 |
| `medium` | 核心业务流程；有一定技术难度；影响部分用户 |
| `low` | 辅助功能；技术成熟；影响范围小 |

### 4. 关联接口提取（related_interfaces）

- **优先从设计文档提取**：如果需求文档附带接口设计，直接提取
- **从功能描述推断**：如"用户登录" → 推断接口为 `/user/login`
- **标注推断来源**：如果是推断的，在 `source` 中说明
- **如果无法推断**：留空，在 `missing_items` 中记录

### 5. 缺失处理

如果必须字段在原文中完全找不到：
- 在 `missing_items` 中记录
- 相应字段留空或填 `"待补充"`
- 如果是推断的，置信度标记为 `low`

---

## 一致性检查

完成提取后，必须执行以下检查，并在 `consistency_check` 部分输出结果。

### P0 级检查（必须通过，否则返回修复）

| 检查项 | 规则 | 失败处理 |
|-------|------|---------|
| 功能与验收标准对应 | 每个功能至少有一个验收标准关联 | 返回修复，补充验收标准 |
| 场景内部逻辑完整 | 每个场景的 given-when-then 不能有逻辑矛盾 | 返回修复，修正逻辑 |
| 字段约束一致性 | 字段定义与业务规则不能冲突 | 返回修复，统一约束 |

**P0 检查失败时，不继续生成后续内容，直接返回错误报告。**

### P1 级检查（必须记录，可后续补充）

| 检查项 | 规则 | 结果类型 |
|-------|------|---------|
| 验收标准与场景对应 | 每个验收标准至少有一个对应的测试场景 | `pass` / `partial` / `fail` |
| 业务规则与场景对应 | 每个业务规则至少在一个场景中被验证 | `pass` / `partial` / `fail` |
| 必填字段测试覆盖 | 每个必填字段，应有"不填"的负向场景 | `pass` / `partial` / `fail` |

**P1 检查失败时，记录在 `missing` 字段中，并在 `recommendations` 中给出改进建议。**

### P2 级检查（建议项，记录但不阻塞）

| 检查项 | 规则 | 结果类型 |
|-------|------|---------|
| 正负场景比例 | 负向场景数量应不少于正向场景数量 | `pass` / `suggest_optimize` |
| 缺失项记录 | 所有必须但缺失的内容已在 missing_items 中记录 | `pass` / `fail` |

**P2 检查失败时，仅在 `recommendations` 中记录，不影响后续流程。**

---

## 使用示例

### 输入文档示例

```
用户管理模块需求文档 V1.2

1. 功能概述
本模块实现用户注册、登录、权限管理等核心功能，提升用户体验。

2. 用户登录
2.1 功能描述
用户可以通过手机号和密码登录系统。

2.2 验收标准
- 用户输入正确的手机号和密码，点击登录按钮，跳转到首页
- 用户输入错误的密码，显示错误提示"密码错误"
- 用户连续输错密码3次，账号锁定30分钟

3. 业务规则
- 手机号必须为11位数字，且以1开头
- 密码长度必须为8-20位，包含字母和数字
```

### 输出 YAML 示例

参见 [YAML 结构定义](#yaml-结构定义) 部分的完整示例。

---

## 与后续阶段对接

### 第二阶段：requirement-validator（需求验证）

**输入**：本格式的标准化需求文档

**使用字段**：
- `features[].priority`：优先级分析
- `features[].risk_level`：风险评估
- `acceptance_criteria`：验收标准完整性检查
- `business_rules`：业务规则一致性检查
- `consistency_check`：质量评分依据

**输出**：`05-validation-report.md` 格式的需求检查报告

### 第三阶段：manual-case-generator（手工案例生成）

**输入**：本格式的标准化需求文档

**使用字段**：
- `features[].test_focus`：优先生成哪些功能的用例
- `features[].risk_level`：风险驱动用例设计
- `scenarios`：直接转换为手工测试用例
- `business_rules`：生成边界场景

**输出**：`06-manual-test-cases.md` 格式的手工测试用例

### 第四阶段：api-case-generator（API 用例生成）

**输入**：本格式的标准化需求文档 + 标准化设计文档

**使用字段**：
- `features[].related_interfaces`：匹配接口
- `scenarios.given/when/then`：转换为自动化测试代码
- `business_rules`：生成断言逻辑

**输出**：`07-api-test-cases.md` 格式的 API 自动化测试用例

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03-18 | 初始版本，融合 SpecKit 提示词 + artifact-schemas 设计 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [02-normalized-design.md](./02-normalized-design.md) - 标准化设计文档格式
- [05-validation-report.md](./05-validation-report.md) - 需求检查报告格式

### 参考实现

- [requirement-normalizer SKILL.md](../../skills/requirement-normalizer/SKILL.md)
