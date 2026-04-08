# 代码差异报告格式规范

**版本**: v1.0
**创建时间**: 2026-03-19
**适用阶段**: 第一阶段（规范化）
**输出工具**: Code Diff MCP（计划中）
**下游消费者**: requirement-validator

---

## 📋 目录

- [概述](#概述)
- [YAML 结构定义](#yaml-结构定义)
- [字段说明](#字段说明)
- [分析规则](#分析规则)
- [使用场景](#使用场景)

---

## 概述

### 目标

分析代码仓库的变更内容，生成结构化的代码差异报告，为需求验证提供实现依据。

### 核心价值

1. **变更追溯**：记录每次提交的具体变更内容
2. **影响分析**：评估代码变更对系统功能的影响范围
3. **需求对齐**：验证代码实现是否与需求文档一致
4. **风险识别**：识别高风险变更（如数据库修改、接口变更）

### 输入输出

- **输入**：
  - Git Diff 结果（两次提交之间的差异）
  - 或 Pull Request 信息
- **输出**：结构化的代码差异报告（YAML 格式）

---

## YAML 结构定义

### 完整结构

```yaml
# ============================================
# 元数据（Metadata）
# ============================================
artifact_type: code_diff_report        # 固定值
version: "1.0"                        # 格式版本
source_files:                         # 源信息
  - "Git Diff: commit_a...commit_b"
created_at: "2026-03-19T14:00:00+08:00"  # ISO 8601 格式
analyzer: "code-diff-mcp"              # 分析工具名称

metadata:
  repository: "zabank-voucher-service"  # 仓库名称
  branch: "feature/credit-voucher"      # 分支名称
  base_commit: "a1b2c3d4"               # 基准提交
  target_commit: "e5f6g7h8"             # 目标提交
  author: "张三"                         # 提交作者
  commit_message: "feat: 支持Credit卡消费券功能"

# ============================================
# 变更摘要（Change Summary）
# ============================================
change_summary:
  total_files_changed: 12              # 变更文件总数
  insertions: 450                      # 新增行数
  deletions: 30                        # 删除行数
  files_added: 3                       # 新增文件数
  files_modified: 8                    # 修改文件数
  files_deleted: 1                     # 删除文件数

  # 按文件类型统计
  by_file_type:
    - type: "java"
      count: 6
      insertions: 300
      deletions: 20
    - type: "xml"
      count: 3
      insertions: 80
      deletions: 5
    - type: "sql"
      count: 2
      insertions: 50
      deletions: 0
    - type: "yaml"
      count: 1
      insertions: 20
      deletions: 5

# ============================================
# 变更文件列表（Changed Files）
# ============================================
changed_files:
  # ----------------------------------------
  # 新增文件
  # ----------------------------------------
  - file_id: "F001"
    file_path: "src/main/java/com/zabank/voucher/controller/VoucherCreditController.java"
    change_type: "added"                # added | modified | deleted
    file_type: "java"
    size: 150                           # 行数

    # 文件用途
    purpose: "新增Credit卡消费券控制器，处理Credit卡消费券相关请求"

    # 主要变更内容
    changes:
      - line_start: 1
        line_end: 150
        change_type: "added"
        content_preview: |
          @RestController
          @RequestMapping("/api/v1/voucher/credit")
          public class VoucherCreditController {
              // Credit卡消费券相关接口
          }

    # 识别的关键元素
    identified_elements:
      - type: "controller"
        name: "VoucherCreditController"
        annotations: ["@RestController", "@RequestMapping"]
        methods:
          - "getVoucherList"
          - "useVoucher"

    # 关联需求
    related_requirements: ["F001", "F002"]

    # 影响评估
    impact:
      level: "high"                     # high | medium | low
      description: "新增核心业务控制器，影响Credit卡消费券功能"
      affected_components: ["API层", "业务逻辑层"]

  # ----------------------------------------
  # 修改文件
  # ----------------------------------------
  - file_id: "F002"
    file_path: "src/main/java/com/zabank/voucher/service/VoucherService.java"
    change_type: "modified"
    file_type: "java"
    size: 80

    purpose: "扩展消费券服务，增加Credit卡支持"

    changes:
      - line_start: 45
        line_end: 60
        change_type: "modified"
        content_preview: |
          // 修改前：仅支持Debit卡
          // if ("DEBIT".equals(cardType)) { ... }

          // 修改后：支持Debit和Credit卡
          if ("DEBIT".equals(cardType) || "CREDIT".equals(cardType)) {
              // 发放消费券逻辑
          }

    identified_elements:
      - type: "service"
        name: "VoucherService"
        modified_methods:
          - method_name: "issueVoucher"
            change_description: "增加Credit卡判断逻辑"

    related_requirements: ["F001"]

    impact:
      level: "high"
      description: "核心服务修改，影响消费券发放逻辑"
      affected_components: ["业务逻辑层"]

      # 兼容性风险
      compatibility_risk:
        level: "medium"
        description: "条件判断逻辑变更，可能影响现有Debit卡功能"
        test_suggestion: "需要回归测试Debit卡消费券功能"

  # ----------------------------------------
  # 数据库变更文件
  # ----------------------------------------
  - file_id: "F003"
    file_path: "src/main/resources/db/migration/V20260319.01__add_credit_voucher_support.sql"
    change_type: "added"
    file_type: "sql"
    size: 50

    purpose: "数据库DDL变更，支持Credit卡消费券"

    changes:
      - line_start: 1
        line_end: 50
        change_type: "added"
        content_preview: |
          -- 新增消费券类型字段
          ALTER TABLE t_voucher ADD COLUMN card_type VARCHAR(10) DEFAULT 'DEBIT';

          -- 新增索引
          CREATE INDEX idx_card_type ON t_voucher(card_type);

    identified_elements:
      - type: "ddl"
        tables:
          - table_name: "t_voucher"
            operation: "ALTER TABLE"
            columns_added: ["card_type"]
            indexes_added: ["idx_card_type"]

    related_requirements: ["F001"]

    impact:
      level: "critical"                 # critical | high | medium | low
      description: "数据库表结构变更，影响所有消费券数据"
      affected_components: ["数据库层"]

      # 数据兼容性风险
      data_compatibility:
        level: "high"
        description: "新增字段设置默认值'DEBIT'，历史数据兼容"
        migration_strategy: "增量DDL，不影响历史数据"
        rollback_plan: "可回滚，删除新增列和索引"

      # 性能影响
      performance_impact:
        level: "medium"
        description: "新增索引可能影响写入性能"
        optimization_suggestion: "评估索引必要性，监控写入性能"

  # ----------------------------------------
  # 配置文件变更
  # ----------------------------------------
  - file_id: "F004"
    file_path: "src/main/resources/application-voucher.yml"
    change_type: "modified"
    file_type: "yaml"
    size: 20

    purpose: "配置文件变更，新增Credit卡消费券配置"

    changes:
      - line_start: 15
        line_end: 20
        change_type: "modified"
        content_preview: |
          voucher:
            types:
              - DEBIT
              - CREDIT  # 新增

    identified_elements:
      - type: "config"
        config_file: "application-voucher.yml"
        config_keys_added: ["voucher.types.CREDIT"]

    related_requirements: ["F001"]

    impact:
      level: "medium"
      description: "配置文件变更，影响消费券类型定义"
      affected_components: ["配置层"]

  # ----------------------------------------
  # 删除文件
  # ----------------------------------------
  - file_id: "F005"
    file_path: "src/main/java/com/zabank/voucher/util/OldVoucherValidator.java"
    change_type: "deleted"
    file_type: "java"
    size: 0

    purpose: "删除旧的验证器类，使用新的验证器替代"

    changes:
      - line_start: 0
        line_end: 0
        change_type: "deleted"

    impact:
      level: "low"
      description: "删除废弃代码，不影响现有功能"
      affected_components: ["工具类"]

# ============================================
# 接口变更分析（API Changes）
# ============================================
api_changes:
  # 新增接口
  new_apis:
    - api_id: "API001"
      http_method: "GET"
      path: "/api/v1/voucher/credit/list"
      controller: "VoucherCreditController"
      method: "getVoucherList"
      request_params:
        - name: "userId"
          type: "String"
          required: true
        - name: "cardType"
          type: "String"
          required: true
          enum_values: ["DEBIT", "CREDIT"]
      response_schema:
        type: "List<VoucherResponse>"
      related_requirements: ["F001"]

    - api_id: "API002"
      http_method: "POST"
      path: "/api/v1/voucher/credit/use"
      controller: "VoucherCreditController"
      method: "useVoucher"
      request_body: "UseVoucherRequest"
      response_schema: "VoucherUseResponse"
      related_requirements: ["F002"]

  # 修改接口
  modified_apis:
    - api_id: "API003"
      http_method: "GET"
      path: "/api/v1/voucher/list"
      controller: "VoucherController"
      method: "getVoucherList"
      change_description: "请求参数cardType新增枚举值CREDIT"
      compatibility: "backward_compatible"  # backward_compatible | breaking_change
      related_requirements: ["F001"]

  # 删除接口
  deleted_apis: []

# ============================================
# 数据库变更分析（Database Changes）
# ============================================
database_changes:
  # DDL 变更（表结构变更）
  ddl_changes:
    - table_name: "t_voucher"
      operation: "ALTER TABLE"          # CREATE TABLE | ALTER TABLE | DROP TABLE
      changes:
        - change_type: "add_column"
          column_name: "card_type"
          data_type: "VARCHAR(10)"
          default_value: "DEBIT"
          nullable: false
          description: "消费券卡类型（DEBIT/CREDIT）"

        - change_type: "add_index"
          index_name: "idx_card_type"
          columns: ["card_type"]
          index_type: "BTREE"

      migration_file: "V20260319.01__add_credit_voucher_support.sql"
      rollback_sql: |
        DROP INDEX idx_card_type ON t_voucher;
        ALTER TABLE t_voucher DROP COLUMN card_type;

  # DML 变更（数据变更）
  dml_changes:
    - table_name: "t_voucher_config"
      operation: "INSERT"
      description: "插入Credit卡消费券配置"
      affected_rows: 5
      sql_preview: |
        INSERT INTO t_voucher_config (type, name, amount, card_type)
        VALUES ('CREDIT_BONUS', 'Credit卡消费回赠', 100, 'CREDIT');

# ============================================
# 依赖变更分析（Dependency Changes）
# ============================================
dependency_changes:
  # Maven 依赖变更
  maven_changes:
    - type: "added"
      group_id: "org.springframework.boot"
      artifact_id: "spring-boot-starter-validation"
      version: "3.2.0"
      reason: "新增参数校验功能"

    - type: "updated"
      group_id: "com.zabank"
      artifact_id: "zabank-common"
      version: "1.5.0 -> 1.6.0"
      reason: "修复已知安全漏洞"

  # 内部服务依赖变更
  service_dependencies:
    - service_name: "za-mks-points-service"
      change_type: "new_dependency"
      interfaces_used: ["/api/v1/points/deduct"]
      reason: "消费券使用时扣减积分"

# ============================================
# 影响分析（Impact Analysis）
# ============================================
impact_analysis:
  # 高影响变更
  high_impact_changes:
    - change_id: "IC001"
      type: "database_schema_change"
      description: "t_voucher表新增card_type字段"
      impact_scope: "所有消费券查询和发放功能"
      risk_level: "critical"
      mitigation:
        - "执行数据库变更前备份t_voucher表"
        - "灰度发布，逐步验证"
        - "准备回滚脚本"

    - change_id: "IC002"
      type: "api_new_feature"
      description: "新增Credit卡消费券相关接口"
      impact_scope: "前端App、管理后台"
      risk_level: "high"
      mitigation:
        - "前端App需要同步更新"
        - "进行兼容性测试（老版本App + 新接口）"

  # 兼容性影响
  compatibility_impact:
    app_compatibility:
      level: "medium"
      description: "老版本App可能无法使用新功能，但不影响现有功能"
      test_scenarios:
        - "V3.7.0 App访问新接口"
        - "V3.7.1 App访问新接口"

    data_compatibility:
      level: "high"
      description: "新增字段设置默认值，历史数据兼容"
      migration_required: true
      migration_plan: "DDL执行时自动设置默认值"

  # 测试影响
  test_impact:
    regression_test_required: true
    regression_scope:
      - "Debit卡消费券查询功能"
      - "Debit卡消费券使用功能"
      - "消费券发放功能"

    new_test_required: true
    new_test_scope:
      - "Credit卡消费券查询功能"
      - "Credit卡消费券使用功能"
      - "Credit卡消费券发放功能"

# ============================================
# 风险评估（Risk Assessment）
# ============================================
risk_assessment:
  overall_risk_level: "medium"          # low | medium | high | critical

  critical_risks: []
  # 当前无critical风险

  high_risks:
    - risk_id: "R001"
      category: "data_integrity"
      description: "数据库表结构变更可能影响历史数据"
      probability: "medium"
      impact: "high"
      mitigation: "执行DDL前备份数据，使用默认值保证历史数据兼容"

  medium_risks:
    - risk_id: "R002"
      category: "compatibility"
      description: "老版本App可能无法使用新功能"
      probability: "high"
      impact: "medium"
      mitigation: "兼容性测试，确保老版本App不崩溃"

  low_risks:
    - risk_id: "R003"
      category: "performance"
      description: "新增索引可能影响写入性能"
      probability: "low"
      impact: "low"
      mitigation: "监控数据库性能，必要时优化索引"

# ============================================
# 测试建议（Test Recommendations）
# ============================================
test_recommendations:
  # 必须测试的场景
  must_test_scenarios:
    - scenario: "Credit卡消费券查询功能"
      reason: "新功能，核心业务"
      related_requirements: ["F001"]
      test_type: "功能测试"

    - scenario: "Credit卡消费券使用功能"
      reason: "新功能，涉及资金操作"
      related_requirements: ["F002"]
      test_type: "功能测试"

    - scenario: "Debit卡消费券功能回归测试"
      reason: "核心服务修改，需要回归验证"
      related_requirements: ["F001", "F002"]
      test_type: "回归测试"

  # 建议测试的场景
  suggested_test_scenarios:
    - scenario: "数据库性能测试"
      reason: "新增索引，验证写入性能"
      test_type: "性能测试"

    - scenario: "App兼容性测试"
      reason: "验证老版本App与新接口的兼容性"
      test_type: "兼容性测试"

  # 自动化测试建议
  automation_recommendations:
    - api_test: "/api/v1/voucher/credit/list"
      priority: "P0"
      reason: "新接口，核心功能"

    - api_test: "/api/v1/voucher/credit/use"
      priority: "P0"
      reason: "新接口，涉及资金操作"

    - api_test: "/api/v1/voucher/list"
      priority: "P1"
      reason: "现有接口，参数扩展，需要回归测试"

# ============================================
# 一致性检查（Consistency Check）
# ============================================
consistency_check:
  # 代码与需求对应关系检查
  code_requirement_mapping:
    result: "pass"
    mapped_requirements:
      - requirement_id: "F001"
        implementation_files: ["F001", "F002", "F003"]
        status: "implemented"
      - requirement_id: "F002"
        implementation_files: ["F001", "F002"]
        status: "implemented"

    unmapped_requirements: []          # 需求未实现
    unrequired_implementations: []      # 实现未对应需求

  # 接口与文档对应关系检查
  api_documentation_mapping:
    result: "warning"
    new_apis_documented: true
    modified_apis_documented: false
    issues:
      - api_id: "API003"
        issue: "接口参数扩展，需要更新API文档（UDoc）"

# ============================================
# 发布建议（Release Recommendations）
# ============================================
release_recommendations:
  # 发布前检查清单
  pre_release_checklist:
    - item: "数据库DDL执行确认"
      status: "pending"
      assignee: "DBA"
      deadline: "2026-03-20"

    - item: "API文档更新"
      status: "pending"
      assignee: "开发团队"
      deadline: "2026-03-20"

    - item: "自动化测试通过"
      status: "pending"
      assignee: "测试团队"
      deadline: "2026-03-21"

  # 发布策略建议
  release_strategy:
    type: "canary"                      # canary | blue_green | rolling
    description: "灰度发布，逐步验证"
    steps:
      - step: 1
        description: "发布到SIT环境，执行全量测试"
      - step: 2
        description: "发布到UAT环境，执行验收测试"
      - step: 3
        description: "生产环境灰度发布，10%流量"
      - step: 4
        description: "监控无异常，逐步扩大流量至100%"

  # 回滚计划
  rollback_plan:
    rollback_type: "automatic"          # automatic | manual
    rollback_conditions:
      - "错误率 > 5%"
      - "响应时间 > 3秒"
      - "数据库异常"
    rollback_steps:
      - step: 1
        description: "回滚应用代码到上一版本"
      - step: 2
        description: "执行数据库回滚脚本"
        sql: |
          DROP INDEX idx_card_type ON t_voucher;
          ALTER TABLE t_voucher DROP COLUMN card_type;
```

---

## 字段说明

### 必选字段（MUST）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `artifact_type` | string | 固定值 `code_diff_report` |
| `version` | string | 格式版本，当前为 `"1.0"` |
| `source_files` | array | 源信息（Git Diff 或 PR） |
| `created_at` | string | 创建时间，ISO 8601 格式 |
| `analyzer` | string | 分析工具名称 |
| `change_summary` | object | 变更摘要 |
| `changed_files` | array | 变更文件列表 |
| `impact_analysis` | object | 影响分析 |

### 可选字段（OPTIONAL）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `api_changes` | object | 接口变更分析 |
| `database_changes` | object | 数据库变更分析 |
| `dependency_changes` | object | 依赖变更分析 |
| `risk_assessment` | object | 风险评估 |
| `test_recommendations` | object | 测试建议 |
| `release_recommendations` | object | 发布建议 |

---

## 分析规则

### 1. 影响等级判断

| 影响等级 | 判断标准 |
|---------|---------|
| **critical** | 数据库表结构变更、核心业务逻辑重写 |
| **high** | 新增核心功能、修改核心服务 |
| **medium** | 新增辅助功能、配置文件变更 |
| **low** | 删除废弃代码、代码格式调整 |

### 2. 风险等级判断

| 风险等级 | 判断标准 |
|---------|---------|
| **critical** | 可能导致数据丢失、系统崩溃 |
| **high** | 可能影响核心功能、破坏兼容性 |
| **medium** | 可能影响部分功能、需要回归测试 |
| **low** | 影响范围小、风险可控 |

### 3. 接口兼容性判断

| 兼容性类型 | 判断标准 |
|-----------|---------|
| **backward_compatible** | 新增可选参数、新增接口、新增枚举值 |
| **breaking_change** | 删除接口、删除必填参数、修改参数类型 |

### 4. 数据库变更识别

**DDL 关键字识别**：
```python
ddl_keywords = [
    "CREATE TABLE", "ALTER TABLE", "DROP TABLE",
    "ADD COLUMN", "DROP COLUMN", "MODIFY COLUMN",
    "ADD INDEX", "DROP INDEX"
]
```

**DML 关键字识别**：
```python
dml_keywords = [
    "INSERT INTO", "UPDATE", "DELETE FROM"
]
```

---

## 使用场景

### 场景1：需求验证

**输入**：代码差异报告 + 标准化需求文档

**处理逻辑**：
```python
def validate_requirement_implementation(
    code_diff: Dict, requirement: Dict
) -> ValidationResult:
    """验证需求是否在代码中实现

    :param code_diff: 代码差异报告
    :param requirement: 标准化需求文档
    :return: 验证结果
    """
    result = ValidationResult()

    # 遍历需求功能
    for feature in requirement["features"]:
        # 查找对应的代码变更
        related_files = find_related_files(code_diff, feature)

        if not related_files:
            result.add_warning(
                f"功能 {feature['id']} 未找到对应的代码实现"
            )

    return result
```

**输出**：需求验证报告的一部分（05-validation-report）

### 场景2：测试范围确定

**输入**：代码差异报告

**处理逻辑**：
```python
def determine_test_scope(code_diff: Dict) -> TestScope:
    """根据代码变更确定测试范围

    :param code_diff: 代码差异报告
    :return: 测试范围
    """
    scope = TestScope()

    # 新增接口 → 新增功能测试
    for api in code_diff["api_changes"]["new_apis"]:
        scope.add_new_test(
            api_path=api["path"],
            test_type="功能测试",
            priority="P0"
        )

    # 修改接口 → 回归测试
    for api in code_diff["api_changes"]["modified_apis"]:
        scope.add_regression_test(
            api_path=api["path"],
            reason="接口参数扩展"
        )

    # 数据库变更 → 数据兼容性测试
    for ddl in code_diff["database_changes"]["ddl_changes"]:
        scope.add_data_compatibility_test(
            table_name=ddl["table_name"],
            migration_file=ddl["migration_file"]
        )

    return scope
```

**输出**：测试范围和优先级建议

### 场景3：发布决策

**输入**：代码差异报告 + 风险评估

**输出**：发布建议（是否可以发布、发布策略、回滚计划）

---

## 最佳实践

### 1. 变更分类清晰

```yaml
# ✅ 正确：清晰的变更分类
change_type: "modified"
purpose: "扩展消费券服务，增加Credit卡支持"

# ❌ 错误：变更分类不清晰
change_type: "changed"
purpose: "修改了一些代码"
```

### 2. 影响分析完整

```yaml
# ✅ 正确：完整的影响分析
impact:
  level: "high"
  description: "核心服务修改，影响消费券发放逻辑"
  affected_components: ["业务逻辑层"]
  compatibility_risk:
    level: "medium"
    description: "条件判断逻辑变更，可能影响现有Debit卡功能"

# ❌ 错误：影响分析不完整
impact:
  level: "high"
  description: "影响较大"
```

### 3. 风险评估具体

```yaml
# ✅ 正确：具体的风险评估
risk:
  category: "data_integrity"
  description: "数据库表结构变更可能影响历史数据"
  probability: "medium"
  impact: "high"
  mitigation: "执行DDL前备份数据，使用默认值保证历史数据兼容"

# ❌ 错误：风险评估不具体
risk:
  description: "有一定风险"
```

### 4. 测试建议可操作

```yaml
# ✅ 正确：可操作的测试建议
test_recommendations:
  must_test_scenarios:
    - scenario: "Credit卡消费券查询功能"
      reason: "新功能，核心业务"
      test_type: "功能测试"
      priority: "P0"

# ❌ 错误：测试建议不可操作
test_recommendations:
  must_test_scenarios:
    - "需要测试"
```

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03-19 | 初始版本，定义代码差异报告格式 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [05-validation-report.md](./05-validation-report.md) - 需求验证报告格式

### 参考实现

- Code Diff MCP（计划中）

---

**文档版本**: v1.0
**最后更新**: 2026-03-19
**维护者**: qa-toolkit 团队