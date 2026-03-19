# 标准化需求文档格式规范（基于 ZA Bank PRD 模板）

**版本**: v2.0（基于产品标准）
**创建时间**: 2026-03-18
**适用阶段**: 第一阶段（需求文档规范化）
**输出工具**: requirement-normalizer Skill
**基准模板**: ZA Bank PRD 模板 V1.01

---

## 📋 目录

- [概述](#概述)
- [YAML 结构定义](#yaml-结构定义)
- [字段说明](#字段说明)
- [提取规则](#提取规则)
- [与 PRD 模板映射关系](#与-prd-模板映射关系)
- [与后续阶段对接](#与后续阶段对接)

---

## 概述

### 目标

将 **ZA Bank PRD 模板**（Word/PDF 格式）标准化为结构化的 YAML 格式，为后续测试阶段提供统一的输入接口。

### 核心原则

1. **以产品标准为主**：完全对齐 ZA Bank PRD 模板的章节结构
2. **保留完整信息**：PRD 的 7 个章节全部映射到 YAML
3. **增强测试能力**：在 PRD 基础上增加 test_focus、risk_level、置信度等测试导向字段
4. **结构化优先**：使用 YAML 定义关键信息，便于程序解析
5. **前向兼容**：支持格式版本升级

### 输入输出

- **输入**：ZA Bank PRD 文档（Word/PDF）
- **输出**：标准化的 YAML 格式文档（完整映射 PRD 内容）

---

## YAML 结构定义

### 完整结构（对齐 PRD 模板 7 章）

```yaml
# ============================================
# 元数据（Metadata）
# ============================================
artifact_type: normalized_requirement  # 固定值
version: "2.0"                        # 格式版本（v2.0 基于产品标准）
source_files:                         # 必须，源文件列表
  - "ZA Bank xxxx项目 产品需求说明书 V1.01.docx"
created_at: "2026-03-18T15:00:00+08:00"  # 必须，ISO 8601 格式
normalizer: "requirement-normalizer"  # 必须，规范化工具名称

metadata:                             # 文档元数据
  project_name: "xxxx项目"            # 项目名称
  doc_version: "V1.01"                # PRD 文档版本
  prd_template_version: "V1.01"       # PRD 模板版本
  revision_history:                   # 修订历史
    - version: "1.01"
      date: "2025/5/26"
      content: "PRD文档模板建立"
      author: "产品经理"
      reviewer: "--"
  processed_by: "requirement-normalizer v2.0"

# ============================================
# 第 1 章：需求背景与目标（回答"为什么做"）
# ============================================
background_and_objectives:
  pain_points:                        # 必须，业务痛点（需数据支撑）
    - description: "线下企业开户需提交 5 类纸质材料，平均耗时 5 个工作日"
      data_support: "2024 年 Q3 因材料不合规导致的驳回率达 23%"
      source: "PRD 第1章 1.1节"
      confidence: high

  objectives:                         # 必须，可量化目标
    - description: "线上开户流程上线后，开户平均耗时缩短至 2 个工作日，材料驳回率降至 8% 以下"
      metric: "平均耗时 < 2 天，驳回率 < 8%"
      baseline: "当前平均 5 天，驳回率 23%"
      target: "2 天，8%"
      source: "PRD 第1章 1.2节"
      confidence: high

# ============================================
# 第 2 章：专业术语表（避免歧义）
# ============================================
glossary:                             # 必须，专业术语列表
  - term: "DRP"
    full_name: "Debt Relief Plan"
    definition: "债务舒缓计划，由债务人及个别债权人直接协商贷款重组的还款方案"
    source: "PRD 第2章"

  - term: "IVA"
    full_name: "Individual Voluntary Arrangement"
    definition: "个人自愿安排。债务人将委任律所为代理人，代理人拟定债务重组方案，在经过法庭聆讯及颁布命令后，代理人确保债务人的还款按重组计划分派给债权人。DRP和为IVA的最大分别在于，DRP无需透过法律程序，可以与个别债权人直接协商新的还款方案。"
    source: "PRD 第2章"

  - term: "IDRP"
    full_name: "Interbank Debt Relief Plan"
    definition: "综合债务舒缓计划。当债务人有多个债权人时，债务人只需与最大债权人商谈重组方案，其他债权人的欠款都合并到最大债权人之下。债务人还款后，由最大债权人向其他债权人分配还款。IDRP与DRP的最大分别在于，IDRP可以一揽子将在不同债权人的欠款合并重组。"
    source: "PRD 第2章"

# ============================================
# 第 3 章：业务逻辑与功能需求（回答"做什么"）
# ============================================
business_logic_and_functional_requirements:

  # 3.1 关键业务流程
  key_business_flows:                 # 必须，关键业务流程
    - id: FLOW001
      name: "用户登录流程"
      description: "用户通过手机号和密码登录系统的完整流程"
      flow_diagram: "附件中的流程图链接或Base64"
      steps:
        - step: 1
          action: "用户输入手机号和密码"
          actor: "用户"
        - step: 2
          action: "系统校验手机号格式"
          actor: "系统"
        - step: 3
          action: "系统校验密码正确性"
          actor: "系统"
        - step: 4
          action: "登录成功，跳转首页"
          actor: "系统"
      source: "PRD 第3章 3.1节"

  # 3.2 功能需求
  features:                           # 必须，功能列表
    - id: F001
      name: "广告配置列表模块化展示"
      description: |
        弹窗的列表记录需要统一调整为大图展示的模式，如下结构：
        - 大图区域：悬停大图上方可见预览入口，可预览三语配置及样式
        - 广告信息区域：广告ID、广告名称、状态标签
        - 投放规则区域：投放页面、推送人群、用户状态
        - 操作区域：编辑、排序、下线/上线、复制、导出、详情
      applicable_scope: "弹窗"
      priority: high                  # 从 PRD 推断或明确标注
      test_focus: true                # 新增：测试重点（核心功能标注为 true）
      risk_level: medium              # 新增：风险等级（根据业务影响判断）
      related_interfaces: []          # 新增：关联接口（从设计文档提取）
      related_flows: [FLOW001]        # 关联业务流程
      source: "PRD 第3章 3.2节 功能1"
      confidence: high

    - id: F002
      name: "广告配置配置页面优化"
      description: |
        点击列表弹窗新增弹窗选择界面（仅适用于弹窗）：
        - 场景：新增、复制、详情
        - 适用范围：弹窗、Banner、公告
        - 页面结构：基础信息、内容配置、投放规则
        - 图片上传组件对接素材库
        - 下架时间改为点选：长期有效、指定时间
      applicable_scope: "弹窗、Banner、公告"
      priority: medium
      test_focus: false
      risk_level: low
      related_interfaces: []
      related_flows: []
      source: "PRD 第3章 3.2节 功能2"
      confidence: high

  # 3.3 界面需求
  ui_requirements:                    # 可选，界面需求
    - id: UI001
      scene: "设 ZA Bank 为出粮账户"
      description: |
        界面元素：
        1. 返回：点击返回至来源页
        2. 遇到问题：点击进入遇到问题页
        3. 复制全部：复制全部账户资料，弹出 Toast"复制成功"
        4. 复制 icon：复制对应的信息，弹出 Toast"复制成功"
        5. 邮件通知雇主：调起系统邮件，自动录入邮件内容
      screenshot: "图片Base64或链接"
      source: "PRD 第3章 3.3节"

  # 3.4 通知需求
  notification_requirements:          # 可选，通知需求
    - id: NOTIF001
      scene: "已认证-待成团"
      channels: ["Push", "Email"]
      template_id: "NOTIF_TEMPLATE_001"
      source: "PRD 第3章 3.4节"

    - id: NOTIF002
      scene: "已认证-TierX已成团"
      channels: ["Push", "Email"]
      template_id: "NOTIF_TEMPLATE_002"
      source: "PRD 第3章 3.4节"

    - id: NOTIF003
      scene: "因退出导致该团将在下月降级"
      channels: ["Push", "Email"]
      send_limit: "当月仅通知两次"
      send_rules:
        - "当月首次因有人退出导致下月将会降级时通知"
        - "当月月底的倒数第2日早上10:00，再次检查是否因人数不足导致将会在下月降级，如有则通知"
      source: "PRD 第3章 3.4节"

  # 3.5 后台管理与 CS/OPS 需求
  backend_ops_requirements:           # 可选，后台管理需求
    - id: OPS001
      category: "登记时间配置"
      description: |
        出粮爽活动的登记时间配置：
        - 第 2 期：2025 年 10 月 1 日 00:00 ~ 2025 年 12 月 31 日 23:59
        - 第 1 期：2025 年 7 月 1 日 00:00 ~ 2025 年 9 月 31 日 23:59
      config_table:
        - period: "第 2 期"
          start_time: "2025-10-01 00:00:00"
          end_time: "2025-12-31 23:59:59"
        - period: "第 1 期"
          start_time: "2025-07-01 00:00:00"
          end_time: "2025-09-31 23:59:59"
      source: "PRD 第3章 3.5节"

    - id: OPS002
      category: "出粮奖赏配置"
      description: "出粮奖赏的合资格薪金金额和奖池 ID 配置"
      config_table:
        - reward_type: "首笔出粮奖赏"
          qualified_amount: "HKD 8,000"
          pool_id: "xxxxxxxxxxx"
        - reward_type: "连续两个月出粮奖赏"
          qualified_amount: "HKD 8,000"
          pool_id: "xxxxxxxxxxx"
        - reward_type: "连续三个月出粮奖赏"
          qualified_amount: "HKD 8,000"
          pool_id: "xxxxxxxxxxx"
      source: "PRD 第3章 3.5节"

  # 3.6 Finance 需求
  finance_requirements:               # 可选，Finance 需求
    - id: FIN001
      description: "如果涉及收费等，需申请GL等，明确如何记账、对账"
      gl_account: "待确认"
      accounting_rules: "待补充"
      source: "PRD 第3章 3.6节"

  # 3.7 MMO、账户状态、风控需求
  mmo_risk_requirements:              # 可选，MMO/风控需求
    - id: MMO001
      description: "如果涉及新的交易类型，需要申请MMO或者复用现有MMO"
      transaction_type: "待确认"
      mmo_code: "待确认"
      account_status_restrictions: []
      customer_status_restrictions: []
      risk_control_rules: []
      fcc_requirements: []
      source: "PRD 第3章 3.7节"

  # 3.8 文案
  copywriting:                        # 可选，文案需求
    - id: COPY001
      scene: "防诈骗提示"
      screenshot: "图片Base64或链接"
      simplified_chinese: "谨防诈骗 保护资金安全"
      traditional_chinese: "慎防詐騙 保護資金安全"
      english: "Beware of scams!"
      source: "PRD 第3章 3.8节"

    - id: COPY002
      scene: "防诈骗提示详情"
      simplified_chinese: "ZA Bank 提醒你：想一想，再转账"
      traditional_chinese: "ZA Bank 提提你：想一想，再轉賬"
      english: "ZA Bank reminds you: Rethink before transferring"
      source: "PRD 第3章 3.8节"

# ============================================
# 第 4 章：非功能需求
# ============================================
non_functional_requirements:

  # 4.1 性能需求
  performance:                        # 必须，性能需求
    - id: PERF001
      category: "响应时间"
      metric: "开户材料校验 < 3秒"
      source: "PRD 第4章 4.1节"

    - id: PERF002
      category: "响应时间"
      metric: "风险评分计算 < 1秒"
      source: "PRD 第4章 4.1节"

    - id: PERF003
      category: "吞吐"
      metric: "峰值时段支持5000用户同时访问"
      source: "PRD 第4章 4.1节"

    - id: PERF004
      category: "吞吐"
      metric: "系统吞吐 > 100TPS"
      source: "PRD 第4章 4.1节"

  # 4.2 数据与埋点
  data_tracking:                      # 可选，埋点需求
    - id: TRACK001
      page: "登录页"
      event_name: "点击登录按钮"
      screenshot: "图片Base64或链接"
      source: "PRD 第4章 4.2节"

  # 4.3 开关控制
  feature_toggle:                     # 可选，开关控制
    - id: TOGGLE001
      code: "LoanRestructureIDRP"
      name: "贷款重组IDRP"
      default_status: "关闭"
      location: "LCS后管>系统管理>开关管理"
      description: "开关关闭时重组Pending录入没有IDLP pending/IDP pending选项"
      source: "PRD 第4章 4.3节"

  # 4.4 App 版本更新机制
  app_version_update:                 # 可选，App版本更新机制
    - id: VERSION001
      version_number: "V3.7.0及更早"
      update_strategy: "强制升级原生版本"
      user_experience: "打开App后即弹窗提示需要升级到最新原生版本，更新前无法使用任何功能"
      source: "PRD 第4章 4.4节"

    - id: VERSION002
      version_number: "V3.7.1 ~ V3.7.4"
      update_strategy: "强制热更新"
      user_experience: "App进入转账功能后即强制进行热更新"
      test_requirement: "需要测试 4个版本 * 2类设备（Android+iOS）"
      source: "PRD 第4章 4.4节"

# ============================================
# 第 5 章：验收标准（回答"怎样算做好"）
# ============================================
acceptance_criteria:                  # 必须，验收标准列表
  - id: AC001
    functional_point: "登录"
    given: "一个已登录的用户"
    when: "用户进入首页时"
    then: "应在顶部明显位置显示其账户余额"
    source: "PRD 第5章"
    confidence: high

  - id: AC002
    functional_point: "线上开户"
    given: "用户提交开户材料"
    when: "系统进行材料校验"
    then: "材料校验通过率≥96%"
    metric: "通过率 >= 96%"
    source: "PRD 第5章"
    confidence: high

  - id: AC003
    functional_point: "线上开户"
    given: "用户进行人脸识别"
    when: "系统进行人脸识别校验"
    then: "人脸识别通过率≥98%"
    metric: "通过率 >= 98%"
    source: "PRD 第5章"
    confidence: high

# ============================================
# 测试场景（Scenarios）- 从验收标准生成
# ============================================
scenarios:                            # 必须，测试场景（从验收标准生成）
  - id: S001
    name: "正常登录-显示账户余额"
    type: positive
    relates_to: AC001
    given: "用户已登录，账户余额为 HKD 10,000"
    when: "用户进入首页"
    then: "顶部明显位置显示'HKD 10,000'"
    source: requirement
    confidence: high

  - id: S002
    name: "正常开户-材料校验通过"
    type: positive
    relates_to: AC002
    given: "用户提交的开户材料完整且格式正确"
    when: "系统进行材料校验"
    then: "校验通过，进入下一步"
    source: requirement
    confidence: high

  - id: S003
    name: "异常开户-材料校验失败"
    type: negative
    relates_to: AC002
    given: "用户提交的开户材料不完整或格式错误"
    when: "系统进行材料校验"
    then: "校验失败，显示错误提示"
    source: supplement
    confidence: medium

# ============================================
# 业务规则（Business Rules）- 从各章节提取
# ============================================
business_rules:                       # 从 PRD 各章节提取的业务规则
  - id: BR001
    rule: "开户材料校验响应时间必须 < 3秒"
    type: performance_rule
    source: "PRD 第4章 4.1节"
    confidence: high
    relates_to: [AC002]

  - id: BR002
    rule: "人脸识别通过率必须 ≥ 98%"
    type: data_rule
    source: "PRD 第5章"
    confidence: high
    relates_to: [AC003]

  - id: BR003
    rule: "开关 LoanRestructureIDRP 关闭时，重组Pending录入没有IDLP pending/IDP pending选项"
    type: process_rule
    source: "PRD 第4章 4.3节"
    confidence: high
    relates_to: []

# ============================================
# 第 6 章：版本规划与迭代衔接（长期视角）
# ============================================
version_plan:                         # 可选，版本规划
  roadmap:                            # 中长期规划
    - version: "MVP"
      timeline: "2025-Q4"
      core_features: ["港股交易"]
      source: "PRD 第6章 6.1节"

    - version: "1.0"
      timeline: "2026-Q1"
      core_features: ["融资融券"]
      source: "PRD 第6章 6.1节"

    - version: "2.0"
      timeline: "2026-Q3"
      core_features: ["衍生品交易"]
      source: "PRD 第6章 6.1节"

  extensibility_design:               # 可扩展性设计
    - id: EXT001
      category: "功能预留"
      description: "账户体系预留多国股票市场交易，为后续扩展更多国家投资交易能力做好预留"
      source: "PRD 第6章 6.2节"

    - id: EXT002
      category: "复用设计"
      description: "抽取圣诞卡片的功能以及后台配置做成通用能力，后续类似活动可以复用"
      source: "PRD 第6章 6.2节"

# ============================================
# 第 7 章：附件
# ============================================
attachments:                          # 可选，附件
  - type: "高保真原型"
    format: "Figma"
    link: "Figma 链接 URL"
    source: "PRD 第7章"

  - type: "业务流程图"
    format: "Visio"
    file: "文件Base64或链接"
    source: "PRD 第7章"

  - type: "其他参考文档"
    format: "PDF"
    file: "文件Base64或链接"
    source: "PRD 第7章"

# ============================================
# 缺失项记录（Missing Items）
# ============================================
missing_items:                        # 必须，记录 PRD 中缺失或不明确的内容
  - "第3章 Finance需求：GL账户、记账规则待补充"
  - "第3章 MMO需求：交易类型、MMO编码待确认"
  - "第4章 数据埋点：具体埋点事件列表待补充"

# ============================================
# 一致性检查报告（Consistency Check）
# ============================================
consistency_check:
  summary:
    total_features: 2
    total_ac: 3
    total_scenarios: 3
    total_business_rules: 3
    missing_items_count: 3

  # P0级检查（必须通过）
  p0_checks:
    - check: "功能与验收标准对应"
      rule: "每个功能至少有一个验收标准关联"
      result: pass
      failures: []

    - check: "PRD 章节完整性"
      rule: "PRD 7个章节全部映射到 YAML"
      result: pass
      failures: []

  # P1级检查（必须记录）
  p1_checks:
    - check: "验收标准与场景对应"
      rule: "每个验收标准至少有一个对应的测试场景"
      result: pass
      missing: []

  # P2级检查（建议项）
  p2_checks:
    - check: "缺失项记录"
      rule: "所有必须但缺失的内容已在missing_items中记录"
      result: pass
      unrecorded: []

# ============================================
# 建议（Recommendations）
# ============================================
recommendations:
  - priority: high
    action: "补充 Finance 需求：明确 GL 账户和记账规则"
    reason: "missing_items 中记录的缺失内容，影响财务系统对接"

  - priority: high
    action: "补充 MMO 需求：明确交易类型和 MMO 编码"
    reason: "missing_items 中记录的缺失内容，影响交易流程"

  - priority: medium
    action: "补充数据埋点详细列表"
    reason: "当前仅有示例，缺少完整的埋点事件列表"
```

---

## 字段说明

### 必选字段（MUST）- 基于 PRD 模板

| 字段路径 | 类型 | 说明 | 对应 PRD 章节 |
|---------|------|------|--------------|
| `artifact_type` | string | 固定值 `normalized_requirement` | - |
| `version` | string | 格式版本，当前为 `"2.0"` | - |
| `source_files` | array | 源文件列表 | - |
| `created_at` | string | 创建时间，ISO 8601 格式 | - |
| `normalizer` | string | 规范化工具名称 | - |
| `metadata.project_name` | string | 项目名称 | PRD 标题 |
| `metadata.doc_version` | string | PRD 文档版本 | PRD 版本 |
| `background_and_objectives` | object | 需求背景与目标 | PRD 第1章 |
| `glossary` | array | 专业术语表 | PRD 第2章 |
| `business_logic_and_functional_requirements` | object | 业务逻辑与功能需求 | PRD 第3章 |
| `non_functional_requirements` | object | 非功能需求 | PRD 第4章 |
| `acceptance_criteria` | array | 验收标准 | PRD 第5章 |
| `version_plan` | object | 版本规划 | PRD 第6章 |

### 可选字段（OPTIONAL）

| 字段路径 | 类型 | 说明 | 对应 PRD 章节 |
|---------|------|------|--------------|
| `business_logic_and_functional_requirements.ui_requirements` | array | 界面需求 | PRD 第3.3章 |
| `business_logic_and_functional_requirements.notification_requirements` | array | 通知需求 | PRD 第3.4章 |
| `business_logic_and_functional_requirements.backend_ops_requirements` | array | 后台管理需求 | PRD 第3.5章 |
| `non_functional_requirements.data_tracking` | array | 埋点需求 | PRD 第4.2章 |
| `attachments` | array | 附件 | PRD 第7章 |

---

## 提取规则

### 1. PRD 章节识别

**自动识别 PRD 模板**：
- 检查文档是否包含"第 X 章"、"需求背景与目标"等关键字
- 检查文档是否包含"ZA Bank"、"产品需求说明书"等标识
- 检查文档是否包含修订历史记录表格

**章节映射规则**：
```python
prd_chapter_mapping = {
    "第 1 章 需求背景与目标": "background_and_objectives",
    "第 2 章 专业术语表": "glossary",
    "第 3 章 业务逻辑与功能需求": "business_logic_and_functional_requirements",
    "第 4 章 非功能需求": "non_functional_requirements",
    "第 5 章 验收标准": "acceptance_criteria",
    "第 6 章 版本规划与迭代衔接": "version_plan",
    "第 7 章 附件": "attachments"
}
```

### 2. 第 5 章验收标准提取（Given-When-Then）

**ZA Bank PRD 模板的验收标准格式**：

```
| 功能点 | 验收标准 |
|--------|---------|
| 登录   | 1. 给定一个已登录的用户，当用户进入首页时，那么应在顶部明显位置显示其账户余额 |
```

**提取逻辑**：
1. 识别表格结构（功能点 + 验收标准）
2. 解析验收标准文本：
   - "给定" / "Given" → `given`
   - "当" / "When" → `when`
   - "那么" / "Then" → `then`
3. 自动生成 `acceptance_criteria` 和 `scenarios`

### 3. 测试重点标注（test_focus）

**自动判断规则**（基于 PRD 内容）：

| 判断依据 | test_focus |
|---------|-----------|
| 功能出现在"第5章 验收标准"中 | `true` |
| 功能描述包含"核心"、"关键"、"重要" | `true` |
| 功能关联"第4章 性能需求" | `true` |
| 功能描述包含"辅助"、"可选" | `false` |

### 4. 风险等级标注（risk_level）

**自动判断规则**：

| 判断依据 | risk_level |
|---------|-----------|
| 功能涉及"资金"、"支付"、"转账" | `high` |
| 功能涉及"安全"、"风控"、"FCC" | `high` |
| 功能出现在"第4章 4.4 App版本更新机制" | `high` |
| 功能出现在"第3.5章 后台管理" | `medium` |
| 功能仅涉及"界面优化"、"文案调整" | `low` |

---

## 与 PRD 模板映射关系

### 完整映射表

| PRD 章节 | PRD 内容 | YAML 字段 | 提取方式 |
|---------|---------|----------|---------|
| **第 1 章** | 业务痛点 | `background_and_objectives.pain_points` | 直接提取 + 数据支撑 |
| **第 1 章** | 可量化目标 | `background_and_objectives.objectives` | 直接提取 + metric 拆分 |
| **第 2 章** | 专业术语表 | `glossary` | 表格解析（名称 + 说明） |
| **第 3.1 章** | 关键业务流程 | `business_logic_and_functional_requirements.key_business_flows` | 流程图提取 + 步骤分解 |
| **第 3.2 章** | 功能需求 | `business_logic_and_functional_requirements.features` | 直接提取 + 测试标注 |
| **第 3.3 章** | 界面需求 | `business_logic_and_functional_requirements.ui_requirements` | 表格解析 + 截图保留 |
| **第 3.4 章** | 通知需求 | `business_logic_and_functional_requirements.notification_requirements` | 表格解析（场景 + 渠道） |
| **第 3.5 章** | 后台管理需求 | `business_logic_and_functional_requirements.backend_ops_requirements` | 配置表提取 |
| **第 3.6 章** | Finance 需求 | `business_logic_and_functional_requirements.finance_requirements` | 直接提取 |
| **第 3.7 章** | MMO/风控需求 | `business_logic_and_functional_requirements.mmo_risk_requirements` | 直接提取 |
| **第 3.8 章** | 文案 | `business_logic_and_functional_requirements.copywriting` | 表格解析（简/繁/英） |
| **第 4.1 章** | 性能需求 | `non_functional_requirements.performance` | 表格解析（类别 + 指标） |
| **第 4.2 章** | 数据与埋点 | `non_functional_requirements.data_tracking` | 表格解析 |
| **第 4.3 章** | 开关控制 | `non_functional_requirements.feature_toggle` | 直接提取 + 配置位置 |
| **第 4.4 章** | App版本更新 | `non_functional_requirements.app_version_update` | 表格解析（版本 + 策略） |
| **第 5 章** | 验收标准 | `acceptance_criteria` + `scenarios` | Given-When-Then 解析 |
| **第 6.1 章** | 中长期规划 | `version_plan.roadmap` | 表格解析（版本 + 时间 + 功能） |
| **第 6.2 章** | 可扩展性设计 | `version_plan.extensibility_design` | 直接提取 |
| **第 7 章** | 附件 | `attachments` | 链接/文件路径保留 |

---

## 与后续阶段对接

### 第二阶段：requirement-validator（需求验证）

**输入**：本格式的标准化需求文档（完整 PRD 内容）

**使用字段**：
- `background_and_objectives.objectives`：目标对齐度检查
- `features[].test_focus`：测试重点分析
- `features[].risk_level`：风险评估
- `acceptance_criteria`：验收标准完整性检查
- `non_functional_requirements.performance`：性能指标验证

### 第三阶段：manual-case-generator（手工案例生成）

**输入**：本格式的标准化需求文档

**使用字段**：
- `key_business_flows`：业务流程转测试路径
- `features[].test_focus`：优先生成哪些功能的用例
- `ui_requirements`：界面测试用例
- `scenarios`：直接转换为手工测试用例

### 第四阶段：api-case-generator（API 用例生成）

**输入**：本格式的标准化需求文档 + 标准化设计文档

**使用字段**：
- `features[].related_interfaces`：匹配接口
- `scenarios.given/when/then`：转换为自动化测试代码
- `non_functional_requirements.performance`：生成性能测试断言

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v2.0 | 2026-03-18 | 基于 ZA Bank PRD 模板 V1.01，完整映射 7 个章节 |
| v1.0 | 2026-03-18 | 初始版本，融合 SpecKit 提示词 + artifact-schemas 设计 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [02-normalized-design.md](./02-normalized-design.md) - 标准化设计文档格式
- [05-validation-report.md](./05-validation-report.md) - 需求检查报告格式

### 参考实现

- [requirement-normalizer SKILL.md](../../skills/requirement-normalizer/SKILL.md)
