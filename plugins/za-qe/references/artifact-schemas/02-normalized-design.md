# 标准化设计文档格式规范（基于 ZA Bank 设计文档模板）

**版本**: v1.0（基于设计文档标准）
**创建时间**: 2026-03-18
**适用阶段**: 第一阶段（设计文档规范化）
**输出工具**: design-parser Skill
**基准模板**: ZA Bank 设计文档模板

---

## 📋 目录

- [概述](#概述)
- [YAML 结构定义](#yaml-结构定义)
- [字段说明](#字段说明)
- [提取规则](#提取规则)
- [与设计文档模板映射关系](#与设计文档模板映射关系)
- [与后续阶段对接](#与后续阶段对接)

---

## 概述

### 目标

将 **ZA Bank 设计文档**（Confluence/Word 格式）标准化为结构化的 YAML 格式，为后续测试阶段（特别是 API 用例生成）提供接口信息和技术实现细节。

### 核心原则

1. **以设计文档标准为主**：对齐 ZA Bank 设计文档模板的章节结构
2. **聚焦测试相关内容**：重点提取接口信息、数据库变更、兼容性场景、测试重点
3. **结构化优先**：使用 YAML 定义关键信息，便于程序解析
4. **补充 PRD 不足**：提供 PRD 缺失的技术实现细节（接口路径、参数、响应）

### 输入输出

- **输入**：ZA Bank 设计文档（Confluence/Word）
- **输出**：标准化的 YAML 格式文档（聚焦测试相关内容）

---

## YAML 结构定义

### 完整结构（聚焦测试相关章节）

```yaml
# ============================================
# 元数据（Metadata）
# ============================================
artifact_type: normalized_design      # 固定值
version: "1.0"                        # 格式版本
source_files:                         # 必须，源文件列表
  - "卡消费券增加Credit消费场景需求设计文档"
source_url: "https://confluence.zatech.io/xxx"  # 可选，Confluence 链接
created_at: "2026-03-18T16:00:00+08:00"  # 必须，ISO 8601 格式
normalizer: "design-parser"       # 必须，规范化工具名称

metadata:                             # 文档元数据
  requirement_summary: "卡消费券增加Credit消费场景需求文档"  # 需求概要
  requirement_doc_link: "卡消费回赠券需求"  # 原始需求文档链接
  ue_reference: "详见需求"            # UE 参考
  doc_write_date: "2024/09/09"        # 文档编写时间
  doc_author: "何英才"                # 文档撰写人
  design_reviewers: ["丁晶晶", "高原", "廖展亮"]  # 设计概要复核人
  design_review_date: "2024/09/11"    # 设计概要复核时间
  requirement_stage: "已投产"          # 需求进度
  processed_by: "design-parser v1.0"

# ============================================
# 第 1 章：需求背景描述
# ============================================
requirement_background:
  background: |                       # 1.1 背景
    原卡消费回赠券需求设计文档：卡消费回赠券需求
    本次需求在原有基础上，新增 Credit 消费场景支持
  features_and_effects: |             # 1.2 功能简介&业务效果
    支持 Credit 卡消费场景的消费券发放和使用
    预期提升 Credit 卡活跃度 15%

# ============================================
# 第 2 章：整体设计概要
# ============================================
design_overview: |                    # 整体设计概要（可以是文本或结构化）
  整体设计概要内容...
  （如果内容很长，可以是纯文本；如果有结构，可以解析为子字段）

# ============================================
# 第 3 章：架构变更及评审
# ============================================
architecture_changes:                 # 可选，架构变更
  has_changes: false                  # 是否涉及架构变更
  description: "不涉及"               # 描述

# ============================================
# 第 4 章：需求模块拆解
# ============================================
requirement_modules:                  # 可选，需求模块拆解
  description: "已在整体设计概要中描述，这里不做赘述"
  modules: []                         # 如果有具体模块列表，在此定义

# ============================================
# 第 5 章：分模块概要设计（核心章节，测试最需要）
# ============================================
module_design:

  # 接口设计
  interfaces:                         # 必须，接口列表
    - id: IF001
      name: "查询消费券列表"
      microservice: "za-mks-points-service"  # 微服务名称
      path: "/voucher/list"           # 接口路径
      method: GET                     # HTTP 方法：GET/POST/PUT/DELETE
      description: "查询用户的消费券列表"

      request_params:                 # 请求参数
        - name: "userId"
          type: string
          required: true
          description: "用户ID"
          example: "123456"
          validation: "不能为空"

        - name: "cardType"
          type: string
          required: false
          description: "卡类型"
          example: "CREDIT"
          enum_values: ["DEBIT", "CREDIT"]
          default: "DEBIT"

      response_schema:                # 响应结构
        success_response:
          - name: "code"
            type: string
            description: "响应码"
            example: "0000"

          - name: "message"
            type: string
            description: "响应消息"
            example: "Success"

          - name: "data"
            type: object
            description: "数据对象"
            children:
              - name: "vouchers"
                type: array
                description: "消费券列表"
                children:
                  - name: "voucherId"
                    type: string
                    description: "消费券ID"
                    example: "V123456"

                  - name: "amount"
                    type: number
                    description: "金额"
                    example: 100.00

                  - name: "status"
                    type: string
                    description: "状态"
                    example: "ACTIVE"
                    enum_values: ["ACTIVE", "USED", "EXPIRED"]

        error_response:               # 错误响应
          - error_code: "E001"
            description: "用户不存在"
            http_status: 400

          - error_code: "E002"
            description: "系统异常"
            http_status: 500

      business_rules:                 # 业务规则（可选）
        - "只返回有效期内的消费券"
        - "CREDIT 卡类型的消费券单独标注"

      test_focus: true                # 是否测试重点
      related_requirements: [F001]    # 关联需求功能（引用 01-normalized-requirement.yaml）
      source: "设计文档 第5章"
      confidence: high

    - id: IF002
      name: "使用消费券"
      microservice: "za-mks-points-service"
      path: "/voucher/use"
      method: POST
      description: "用户使用消费券进行消费"

      request_params:
        - name: "userId"
          type: string
          required: true
          description: "用户ID"
          example: "123456"

        - name: "voucherId"
          type: string
          required: true
          description: "消费券ID"
          example: "V123456"

        - name: "amount"
          type: number
          required: true
          description: "消费金额"
          example: 50.00

      response_schema:
        success_response:
          - name: "code"
            type: string
            example: "0000"

          - name: "message"
            type: string
            example: "Success"

          - name: "data"
            type: object
            children:
              - name: "remainingAmount"
                type: number
                description: "剩余金额"
                example: 50.00

        error_response:
          - error_code: "E003"
            description: "消费券不存在"
            http_status: 400

          - error_code: "E004"
            description: "消费券已过期"
            http_status: 400

          - error_code: "E005"
            description: "消费金额超过消费券额度"
            http_status: 400

      business_rules:
        - "消费券一次只能使用一张"
        - "消费金额不能超过消费券面额"
        - "使用后消费券状态变为 USED"

      test_focus: true
      related_requirements: [F002]
      source: "设计文档 第5章"
      confidence: high

  # 数据库设计
  database_design:                    # 可选，数据库设计
    tables:
      - table_name: "t_voucher"
        description: "消费券表"
        operation: "modify"           # 操作类型：create/modify/delete
        fields:
          - name: "id"
            type: "bigint"
            nullable: false
            primary_key: true
            description: "主键ID"

          - name: "user_id"
            type: "varchar(32)"
            nullable: false
            index: true
            description: "用户ID"

          - name: "voucher_id"
            type: "varchar(32)"
            nullable: false
            unique: true
            description: "消费券ID"

          - name: "card_type"
            type: "varchar(16)"
            nullable: false
            description: "卡类型：DEBIT/CREDIT"
            default: "DEBIT"
            comment: "本次新增字段"

          - name: "amount"
            type: "decimal(10,2)"
            nullable: false
            description: "金额"

          - name: "status"
            type: "varchar(16)"
            nullable: false
            description: "状态：ACTIVE/USED/EXPIRED"

          - name: "expire_time"
            type: "datetime"
            nullable: false
            description: "过期时间"

        indexes:
          - name: "idx_user_card_type"
            columns: ["user_id", "card_type"]
            type: "BTREE"

        ddl: |
          ALTER TABLE t_voucher ADD COLUMN card_type varchar(16) NOT NULL DEFAULT 'DEBIT' COMMENT '卡类型：DEBIT/CREDIT';
          CREATE INDEX idx_user_card_type ON t_voucher(user_id, card_type);

        source: "设计文档 第10.2章 SQL物料"

# ============================================
# 第 6 章：整体兼容性分析（测试需要）
# ============================================
compatibility_analysis:

  # 6.1 上游调用方分析
  upstream_callers:                   # 可选，上游调用方
    - service: "za-app-service"
      description: "App 端调用"
      impact: "需要传递新的 cardType 参数"
      compatibility: "向后兼容（cardType 默认为 DEBIT）"

  # 6.2 下游被调用方分析
  downstream_callees:                 # 可选，下游被调用方
    - service: "za-risk-service"
      description: "风控服务"
      impact: "需要支持 CREDIT 卡类型的风控规则"
      compatibility: "需要升级风控规则"

  # 6.3 App 兼容性分析
  app_compatibility:
    old_app_new_code:                 # 6.3.1 老版本 app + 新代码
      compatible: true
      description: "不涉及"

    old_app_new_data:                 # 6.3.2 老版本 app + 新数据
      compatible: true
      description: |
        后台要在风控下发的 ms+da 判断 app 版本，低版本 app 降级到 ms 验证
      test_scenarios:
        - scenario: "老版本 app 查询消费券列表"
          expected: "不返回 CREDIT 类型的消费券"

    new_app_old_data:                 # 6.3.3 新版本 app + 老数据
      compatible: true
      description: "不涉及"

  # 6.4 数据兼容性分析
  data_compatibility:
    new_data_old_code:                # 6.4.1 新数据 + 老代码
      compatible: true
      description: "详见 6.3"

    new_code_old_data:                # 6.4.2 新代码 + 老数据
      compatible: true
      description: "详见 6.3"

  # 6.5 后管兼容性分析
  backend_compatibility:
    compatible: true
    description: "不涉及"

  # 6.6 发布机房兼容性分析
  deployment_compatibility:
    new_old_room_traffic:             # 6.6.1 新老机房流量兼容
      compatible: true
      description: "前后向都兼容，发布顺序无影响"

    deployment_traffic_switch:        # 6.6.2 发布切流兼容性
      compatible: true
      description: "前后向都兼容，发布顺序无影响"

    deployment_sequence:              # 6.6.3 发布时序顺序
      compatible: true
      description: "前后向都兼容，发布顺序无影响"

# ============================================
# 第 7 章：兼容性方案
# ============================================
compatibility_solution:
  description: "不涉及"
  solutions: []

# ============================================
# 第 8 章：业务降级和数据一致性梳理（测试需要）
# ============================================
degradation_and_consistency:
  upstream_downstream_diagram: |      # 上下游调用关系全览图
    此处缺图：上下游调用关系全览图

  degradation_scenarios:              # 降级场景
    - scenario: "风控服务降级"
      trigger: "风控服务不可用"
      action: "降级到默认风控规则"
      data_consistency: "确保消费券状态一致"
      test_points:
        - "验证降级触发条件"
        - "验证降级后业务逻辑正确"
        - "验证降级恢复后数据一致"

# ============================================
# 第 9 章：多线程安全梳理
# ============================================
thread_safety:
  has_concurrency_issue: false
  description: "不涉及"
  analysis: []

# ============================================
# 第 10 章：发布物料（部分测试需要）
# ============================================
deployment_materials:

  # 10.1 发布系统
  deployment_systems:                 # 发布系统清单
    - system_name: "za-mks-points-service"
      system_id: 1
      description: "积分服务"

  # 10.2 SQL 物料
  sql_materials:                      # SQL 物料（已在 database_design 中定义）
    description: "详见 module_design.database_design"

  # 10.3 定时任务物料
  scheduled_tasks:
    has_tasks: false
    description: "不涉及"
    tasks: []

  # 10.4 Activity 配置
  activity_config:
    has_config: false
    description: "不涉及"
    configs: []

  # 10.5 DBFF 接口
  dbff_interfaces:                    # DBFF 接口配置
    - interface_name: "queryVoucherList"
      description: "查询消费券列表"
      service: "za-mks-points-service"
      path: "/voucher/list"
      method: GET

  # 10.6 Apollo 配置
  apollo_config:                      # Apollo 配置
    system: "za-mks-points-service"
    new_configs:
      - key: "voucher.credit.enabled"
        value: "true"
        description: "是否启用 CREDIT 卡消费券"

    modified_configs: []
    deleted_configs: []

  # 10.7 错误码国际化物料
  error_code_i18n:                    # 错误码国际化
    - error_code: "E003"
      simplified_chinese: "消费券不存在"
      traditional_chinese: "消費券不存在"
      english: "Voucher not found"

    - error_code: "E004"
      simplified_chinese: "消费券已过期"
      traditional_chinese: "消費券已過期"
      english: "Voucher expired"

# ============================================
# 第 11 章：测试重点关注要点列举（测试核心）
# ============================================
test_focus_points:                    # 必须，测试重点
  - id: TEST001
    point: "CREDIT 卡消费券查询"
    description: "验证 CREDIT 卡类型的消费券能够正确查询"
    priority: high
    test_types: ["功能测试", "兼容性测试"]

  - id: TEST002
    point: "老版本 app 兼容性"
    description: "验证老版本 app 不会看到 CREDIT 类型消费券"
    priority: high
    test_types: ["兼容性测试"]

  - id: TEST003
    point: "消费券使用流程"
    description: "验证 CREDIT 卡消费券的使用流程完整"
    priority: medium
    test_types: ["功能测试", "业务流程测试"]

# ============================================
# 第 12 章：发布后生产配置清单
# ============================================
post_deployment_config:
  - item: "dbff 新接口"
    description: "配置 dbff 新接口权限"
    responsible: "运维"

# ============================================
# 第 13 章：下线配置清单
# ============================================
offline_config:
  has_offline: false
  description: "不涉及，无需单独下线"
  items: []

# ============================================
# 缺失项记录（Missing Items）
# ============================================
missing_items:                        # 必须，记录设计文档中缺失或不明确的内容
  - "第8章：上下游调用关系全览图缺失"
  - "第5章：部分接口缺少完整的错误码定义"
  - "第11章：测试重点关注要点仅列举了概要，缺少详细测试场景"

# ============================================
# 一致性检查报告（Consistency Check）
# ============================================
consistency_check:
  summary:
    total_interfaces: 2
    total_database_tables: 1
    total_test_focus_points: 3
    missing_items_count: 3

  # P0级检查（必须通过）
  p0_checks:
    - check: "接口定义完整性"
      rule: "每个接口必须包含 path、method、request_params、response_schema"
      result: pass
      failures: []

    - check: "数据库变更合理性"
      rule: "数据库变更必须有 DDL/DML"
      result: pass
      failures: []

  # P1级检查（必须记录）
  p1_checks:
    - check: "接口与需求对应"
      rule: "每个接口应关联到需求功能（related_requirements）"
      result: pass
      missing: []

    - check: "测试重点覆盖"
      rule: "测试重点应覆盖所有核心接口"
      result: pass
      missing: []

  # P2级检查（建议项）
  p2_checks:
    - check: "错误码国际化完整性"
      rule: "所有错误码应有三语翻译"
      result: pass
      unrecorded: []

# ============================================
# 建议（Recommendations）
# ============================================
recommendations:
  - priority: high
    action: "补充上下游调用关系全览图"
    reason: "missing_items 中记录的缺失内容，影响降级方案设计"

  - priority: medium
    action: "补充完整的错误码定义"
    reason: "部分接口缺少错误码，影响异常测试用例设计"

  - priority: low
    action: "补充详细测试场景"
    reason: "第11章仅列举概要，建议补充详细的测试步骤和预期结果"
```

---

## 字段说明

### 必选字段（MUST）- 基于设计文档模板

| 字段路径 | 类型 | 说明 | 对应设计文档章节 |
|---------|------|------|----------------|
| `artifact_type` | string | 固定值 `normalized_design` | - |
| `version` | string | 格式版本，当前为 `"1.0"` | - |
| `source_files` | array | 源文件列表 | - |
| `created_at` | string | 创建时间，ISO 8601 格式 | - |
| `normalizer` | string | 规范化工具名称 | - |
| `metadata` | object | 文档元数据 | 文档头部 |
| `module_design.interfaces` | array | **接口列表（核心）** | 第5章 |
| `test_focus_points` | array | **测试重点（核心）** | 第11章 |

### 可选字段（OPTIONAL）

| 字段路径 | 类型 | 说明 | 对应设计文档章节 |
|---------|------|------|----------------|
| `requirement_background` | object | 需求背景 | 第1章 |
| `design_overview` | string | 整体设计概要 | 第2章 |
| `architecture_changes` | object | 架构变更 | 第3章 |
| `module_design.database_design` | object | 数据库设计 | 第5章 + 第10.2章 |
| `compatibility_analysis` | object | 兼容性分析 | 第6章 |
| `degradation_and_consistency` | object | 业务降级 | 第8章 |
| `deployment_materials` | object | 发布物料 | 第10章 |

---

## 提取规则

### 1. 接口信息提取（最重要）

**识别模式**：
- 章节标题包含"分模块概要设计"、"接口设计"
- 表格包含"接口名称"、"请求参数"、"响应参数"
- 代码块包含 HTTP Method（GET/POST/PUT/DELETE）

**提取字段**：
```yaml
interfaces:
  - id: IF001                         # 自动生成
    name: "查询消费券列表"             # 从接口名称提取
    microservice: "za-mks-points-service"  # 从服务名称提取
    path: "/voucher/list"             # 从接口路径提取
    method: GET                       # 从 HTTP Method 提取
    request_params:                   # 从请求参数表格提取
      - name: "userId"
        type: string
        required: true
        description: "用户ID"
    response_schema:                  # 从响应结构提取
      success_response: [...]
      error_response: [...]
```

**置信度判断**：
- `high`：接口文档完整（包含路径、参数、响应）
- `medium`：接口文档不完整（缺少部分字段）
- `low`：接口信息从其他地方推断（如从代码注释）

### 2. 数据库变更提取

**识别模式**：
- 章节标题包含"SQL 物料"、"数据库设计"
- 包含 DDL 语句（CREATE TABLE、ALTER TABLE）
- 包含 DML 语句（INSERT、UPDATE、DELETE）

**提取字段**：
```yaml
database_design:
  tables:
    - table_name: "t_voucher"
      operation: "modify"             # 从 DDL 推断（ALTER → modify）
      fields: [...]
      ddl: "ALTER TABLE t_voucher ADD COLUMN ..."
```

### 3. 兼容性场景提取

**识别模式**：
- 章节标题包含"兼容性分析"、"App 兼容性"
- 段落包含"老版本 app"、"新数据"、"降级"

**提取为测试场景**：
```yaml
compatibility_analysis:
  app_compatibility:
    old_app_new_data:
      compatible: true
      test_scenarios:
        - scenario: "老版本 app 查询消费券列表"
          expected: "不返回 CREDIT 类型的消费券"
```

### 4. 测试重点提取

**识别模式**：
- 章节标题包含"测试重点关注要点列举"
- 列表形式的测试点

**提取字段**：
```yaml
test_focus_points:
  - id: TEST001
    point: "CREDIT 卡消费券查询"
    description: "验证 CREDIT 卡类型的消费券能够正确查询"
    priority: high                    # 从序号或描述推断
    test_types: ["功能测试", "兼容性测试"]
```

---

## 与设计文档模板映射关系

### 完整映射表（聚焦测试相关）

| 设计文档章节 | 设计文档内容 | YAML 字段 | 测试价值 | 提取优先级 |
|------------|-------------|----------|---------|-----------|
| **第1章** | 需求背景 | `requirement_background` | 低 | P2 |
| **第2章** | 整体设计概要 | `design_overview` | 低 | P2 |
| **第3章** | 架构变更 | `architecture_changes` | 低 | P2 |
| **第5章** | **接口设计** | `module_design.interfaces` | **极高** | **P0** |
| **第5章** | **数据库设计** | `module_design.database_design` | **高** | **P1** |
| **第6章** | **兼容性分析** | `compatibility_analysis` | **高** | **P1** |
| **第8章** | **业务降级** | `degradation_and_consistency` | **中** | **P1** |
| **第10.2章** | SQL 物料 | `deployment_materials.sql_materials` | 中 | P1 |
| **第10.5章** | DBFF 接口 | `deployment_materials.dbff_interfaces` | 中 | P1 |
| **第10.6章** | Apollo 配置 | `deployment_materials.apollo_config` | 中 | P1 |
| **第10.7章** | 错误码国际化 | `deployment_materials.error_code_i18n` | 中 | P1 |
| **第11章** | **测试重点** | `test_focus_points` | **极高** | **P0** |

### 不提取的章节（与测试关系不大）

| 设计文档章节 | 原因 |
|------------|------|
| 第4章 需求模块拆解 | 通常引用第2章，重复内容 |
| 第7章 兼容性方案 | 实施细节，测试不关心 |
| 第9章 多线程安全 | 开发内部实现，测试黑盒无法验证 |
| 第10.1章 发布系统 | 运维配置，测试不关心 |
| 第10.3章 定时任务 | 除非有定时任务测试需求 |
| 第12章 发布后配置 | 运维配置，测试不关心 |
| 第13章 下线配置 | 运维配置，测试不关心 |

---

## 与后续阶段对接

### 第二阶段：doc-reviewer（需求验证）

**输入**：01-normalized-requirement.yaml + 02-normalized-design.yaml

**使用字段**：
- `module_design.interfaces`：验证需求功能是否有对应接口实现
- `compatibility_analysis`：验证兼容性需求是否被设计覆盖

### 第三阶段：case-designer（手工案例生成）

**输入**：01-normalized-requirement.yaml + 02-normalized-design.yaml

**使用字段**：
- `module_design.interfaces`：生成接口测试用例
- `compatibility_analysis.app_compatibility`：生成兼容性测试用例
- `test_focus_points`：指导测试优先级

### 第四阶段：api-generator（API 用例生成）✅ 核心

**输入**：01-normalized-requirement.yaml + 02-normalized-design.yaml

**使用字段**：
- **`module_design.interfaces`**：提取接口路径、参数、响应 → 生成 API 测试代码
- `module_design.database_design`：生成数据准备脚本
- `compatibility_analysis`：生成兼容性测试场景
- `degradation_and_consistency`：生成降级测试场景
- `deployment_materials.error_code_i18n`：生成错误码断言
- `test_focus_points`：指导测试优先级

**示例**：
```python
# 从 02-normalized-design.yaml 生成的测试代码
def test_query_voucher_list_credit():
    """测试查询 CREDIT 卡消费券列表"""
    # 从 interfaces[0] 提取
    response = requests.get(
        url="https://api.zabank.com/voucher/list",
        params={
            "userId": "123456",
            "cardType": "CREDIT"
        }
    )

    # 从 response_schema 生成断言
    assert response.status_code == 200
    assert response.json()["code"] == "0000"
    assert response.json()["data"]["vouchers"] is not None
```

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03-18 | 初始版本，基于 ZA Bank 设计文档模板 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [01-normalized-requirement.md](./01-normalized-requirement-v2.md) - 标准化需求文档格式
- [07-api-test-cases.md](./07-api-test-cases.md) - API 自动化用例格式

### 参考实现

- [design-parser SKILL.md](../../skills/design-parser/SKILL.md)
