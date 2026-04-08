# 标准化历史案例格式规范

**版本**: v1.0
**创建时间**: 2026-03-19
**适用阶段**: 第一阶段（规范化）
**输出工具**: case-normalizer Skill（计划中）/ CML MCP（计划中）
**下游消费者**: case-designer

---

## 📋 目录

- [概述](#概述)
- [YAML 结构定义](#yaml-结构定义)
- [字段说明](#字段说明)
- [提取规则](#提取规则)
- [使用场景](#使用场景)

---

## 概述

### 目标

将历史测试案例（Excel、XMind、测试管理系统）标准化为结构化的 YAML 格式，为新功能的测试案例生成提供参考和复用基础。

### 核心价值

1. **案例复用**：相似功能可以参考历史案例，减少重复设计
2. **知识沉淀**：建立测试案例知识库，避免知识流失
3. **智能推荐**：基于功能相似度推荐相关历史案例
4. **质量基准**：历史案例作为测试覆盖度的参考基准

### 输入输出

- **输入**：
  - Excel 测试案例文件（.xlsx）
  - XMind 思维导图（.xmind）
  - 测试管理系统导出文件（CSV/JSON）
- **输出**：标准化的 YAML 格式文档

---

## YAML 结构定义

### 完整结构

```yaml
# ============================================
# 元数据（Metadata）
# ============================================
artifact_type: normalized_cases        # 固定值
version: "1.0"                        # 格式版本
source_files:                         # 必须，源文件列表
  - "历史测试案例_消费券模块_2025Q4.xlsx"
  - "消费券功能测试用例.xmind"
created_at: "2026-03-19T10:00:00+08:00"  # 必须，ISO 8601 格式
normalizer: "case-normalizer"          # 必须，规范化工具名称

metadata:
  project_name: "消费券模块历史案例"
  case_count: 45                      # 案例总数
  source_system: "Excel + XMind"      # 来源系统
  date_range:                         # 案例时间范围
    start: "2025-10-01"
    end: "2025-12-31"
  processed_by: "case-normalizer v1.0"

# ============================================
# 功能模块分组（Feature Groups）
# ============================================
feature_groups:
  - group_id: "FG001"
    group_name: "消费券查询功能"
    description: "包含消费券列表查询、详情查询、筛选等功能的历史测试案例"
    related_requirements: ["F001", "F002"]  # 关联需求ID（从需求文档映射）
    tags: ["查询", "消费券", "核心功能"]
    priority: high

  - group_id: "FG002"
    group_name: "消费券使用功能"
    description: "包含消费券使用、核销、退款等功能的历史测试案例"
    related_requirements: ["F003", "F004"]
    tags: ["使用", "消费券", "资金操作"]
    priority: high

# ============================================
# 测试案例列表（Test Cases）
# ============================================
test_cases:
  # ----------------------------------------
  # 正向场景案例
  # ----------------------------------------
  - case_id: "TC001"
    case_name: "Credit卡用户查询可用消费券列表"
    feature_group: "FG001"            # 关联功能分组
    case_type: "positive"             # positive | negative | boundary
    priority: "P0"                    # P0 | P1 | P2

    # 测试环境
    test_environment: ["sit", "auto_qe", "uat"]

    # 前置条件
    preconditions:
      - "用户已登录"
      - "用户拥有Credit卡"
      - "用户有可用的消费券"

    # 测试步骤
    test_steps:
      - step: 1
        action: "进入消费券列表页面"
        expected_result: "页面正常加载，显示消费券列表"

      - step: 2
        action: "选择卡类型为Credit"
        expected_result: "列表仅显示Credit卡的消费券"

      - step: 3
        action: "查看消费券详情"
        expected_result: "消费券信息完整显示（金额、有效期、使用条件）"

    # 预期结果
    expected_results:
      - "消费券列表显示正确"
      - "消费券状态为可用"
      - "消费券金额与发放记录一致"

    # 测试数据（脱敏后）
    test_data:
      user_id: "user_credit_test_001"
      card_type: "CREDIT"
      voucher_status: "ACTIVE"

    # 执行记录
    execution_history:
      - execution_date: "2025-11-15"
        environment: "sit"
        result: "pass"
        executor: "张三"
        duration: "5分钟"
        defects: []

      - execution_date: "2025-11-16"
        environment: "auto_qe"
        result: "pass"
        executor: "李四"
        duration: "4分钟"
        defects: []

    # 关联信息
    related_requirements: ["F001"]    # 关联需求ID
    related_interfaces: ["IF001"]     # 关联接口ID
    related_defects: []                # 关联缺陷ID

    # 标签和分类
    tags: ["查询", "Credit卡", "正向场景", "P0"]
    category: "功能测试"

    # 案例来源
    source:
      file: "历史测试案例_消费券模块_2025Q4.xlsx"
      sheet: "查询功能"
      row: 15
      original_case_id: "TC-QUERY-001"

    # 置信度
    confidence: high                   # high | medium | low

  # ----------------------------------------
  # 异常场景案例
  # ----------------------------------------
  - case_id: "TC002"
    case_name: "缺少必填参数查询消费券列表"
    feature_group: "FG001"
    case_type: "negative"
    priority: "P1"

    test_environment: ["sit", "auto_qe", "uat"]

    preconditions:
      - "用户已登录"

    test_steps:
      - step: 1
        action: "调用查询消费券接口，不传userId参数"
        expected_result: "接口返回错误码E001"

      - step: 2
        action: "验证错误信息"
        expected_result: "错误信息为'用户ID不能为空'"

    expected_results:
      - "接口返回状态码400"
      - "错误码为E001"
      - "错误信息正确"

    test_data:
      card_type: "CREDIT"
      # 缺少 user_id

    execution_history:
      - execution_date: "2025-11-15"
        environment: "sit"
        result: "pass"
        executor: "张三"
        defects: []

    related_requirements: ["F001"]
    related_interfaces: ["IF001"]
    related_defects: []

    tags: ["查询", "异常场景", "参数校验", "P1"]
    category: "功能测试"

    source:
      file: "历史测试案例_消费券模块_2025Q4.xlsx"
      sheet: "查询功能"
      row: 32
      original_case_id: "TC-QUERY-018"

    confidence: high

  # ----------------------------------------
  # 边界场景案例
  # ----------------------------------------
  - case_id: "TC003"
    case_name: "查询结果为空（无可用消费券）"
    feature_group: "FG001"
    case_type: "boundary"
    priority: "P2"

    test_environment: ["sit", "auto_qe", "uat"]

    preconditions:
      - "用户已登录"
      - "用户没有可用的消费券"

    test_steps:
      - step: 1
        action: "进入消费券列表页面"
        expected_result: "页面显示空状态提示"

      - step: 2
        action: "查看空状态文案"
        expected_result: "文案为'暂无可用消费券'"

    expected_results:
      - "消费券列表为空数组"
      - "显示友好的空状态提示"

    test_data:
      user_id: "user_without_vouchers"
      card_type: "CREDIT"

    execution_history:
      - execution_date: "2025-11-15"
        environment: "sit"
        result: "pass"
        executor: "张三"
        defects: []

    related_requirements: ["F001"]
    related_interfaces: ["IF001"]
    related_defects: []

    tags: ["查询", "边界场景", "空状态", "P2"]
    category: "功能测试"

    source:
      file: "历史测试案例_消费券模块_2025Q4.xlsx"
      sheet: "查询功能"
      row: 45
      original_case_id: "TC-QUERY-025"

    confidence: high

  # ----------------------------------------
  # 兼容性场景案例
  # ----------------------------------------
  - case_id: "TC004"
    case_name: "老版本App查看新数据格式消费券"
    feature_group: "FG001"
    case_type: "compatibility"
    priority: "P1"

    test_environment: ["sit", "uat"]

    preconditions:
      - "使用V3.7.0版本App"
      - "服务端已新增消费券类型字段"

    test_steps:
      - step: 1
        action: "使用老版本App查询消费券列表"
        expected_result: "列表正常显示，新字段被忽略"

      - step: 2
        action: "查看消费券详情"
        expected_result: "详情页正常显示，不崩溃"

    expected_results:
      - "老版本App正常使用"
      - "新字段不影响老版本功能"
      - "无崩溃和异常"

    test_data:
      app_version: "V3.7.0"
      user_id: "user_compatibility_test"
      card_type: "CREDIT"

    execution_history:
      - execution_date: "2025-12-10"
        environment: "sit"
        result: "pass"
        executor: "王五"
        defects: []

    related_requirements: ["F001"]
    related_interfaces: ["IF001"]
    related_defects: []

    tags: ["查询", "兼容性", "老版本App", "P1"]
    category: "兼容性测试"

    source:
      file: "消费券功能测试用例.xmind"
      node: "兼容性测试/老版本App"

    confidence: medium

  # ----------------------------------------
  # 性能场景案例
  # ----------------------------------------
  - case_id: "TC005"
    case_name: "消费券列表查询响应时间验证"
    feature_group: "FG001"
    case_type: "performance"
    priority: "P1"

    test_environment: ["sit", "uat"]

    preconditions:
      - "用户已登录"
      - "用户有大量消费券（> 100张）"

    test_steps:
      - step: 1
        action: "发起消费券列表查询请求"
        expected_result: "请求在1秒内返回"

      - step: 2
        action: "记录响应时间"
        expected_result: "响应时间 < 1秒"

    expected_results:
      - "响应时间 < 1秒"
      - "列表数据完整"
      - "无超时错误"

    test_data:
      user_id: "user_performance_test"
      card_type: "CREDIT"
      voucher_count: 150

    execution_history:
      - execution_date: "2025-12-05"
        environment: "sit"
        result: "pass"
        executor: "赵六"
        duration: "2分钟"
        actual_response_time: "0.8秒"
        defects: []

    related_requirements: ["F001"]
    related_interfaces: ["IF001"]
    related_defects: []

    tags: ["查询", "性能测试", "响应时间", "P1"]
    category: "性能测试"

    source:
      file: "历史测试案例_消费券模块_2025Q4.xlsx"
      sheet: "性能测试"
      row: 8
      original_case_id: "TC-PERF-008"

    confidence: high

# ============================================
# 缺陷关联记录（Defect Mapping）
# ============================================
defect_mapping:
  - defect_id: "DEF001"
    defect_title: "查询消费券列表时偶现超时"
    severity: "high"
    status: "closed"
    related_cases: ["TC005"]
    root_cause: "数据库索引缺失"
    fix_date: "2025-12-10"

  - defect_id: "DEF002"
    defect_title: "老版本App查看新消费券类型崩溃"
    severity: "critical"
    status: "closed"
    related_cases: ["TC004"]
    root_cause: "新字段类型与老版本不兼容"
    fix_date: "2025-12-12"

# ============================================
# 统计摘要（Statistics Summary）
# ============================================
statistics_summary:
  total_cases: 45
  by_type:
    positive: 20                      # 正向场景
    negative: 15                      # 异常场景
    boundary: 5                       # 边界场景
    compatibility: 3                  # 兼容性场景
    performance: 2                    # 性能场景

  by_priority:
    P0: 15                            # 核心功能
    P1: 20                            # 重要功能
    P2: 10                            # 一般功能

  by_feature_group:
    FG001: 25                         # 查询功能
    FG002: 20                         # 使用功能

  execution_summary:
    total_executions: 120             # 总执行次数
    pass_rate: 95%                    # 通过率
    avg_duration: "5分钟"             # 平均执行时长

# ============================================
# 质量评估（Quality Assessment）
# ============================================
quality_assessment:
  overall_quality: "good"             # good | medium | poor

  strengths:
    - "正向场景覆盖完整"
    - "边界场景考虑充分"
    - "兼容性场景有针对性"

  weaknesses:
    - "异常场景覆盖不足（缺少网络异常、并发场景）"
    - "性能测试案例较少"

  recommendations:
    - priority: high
      recommendation: "补充网络异常场景测试案例"
      reason: "当前缺少弱网、超时、重试等场景"

    - priority: medium
      recommendation: "增加并发场景测试案例"
      reason: "消费券使用涉及并发，需要补充并发测试"

# ============================================
# 一致性检查报告（Consistency Check）
# ============================================
consistency_check:
  # 案例与需求对应关系检查
  case_requirement_mapping:
    result: "pass"
    unmapped_cases: []                # 未关联需求案例
    unmapped_requirements: ["F005"]   # 需求未覆盖

  # 案例与接口对应关系检查
  case_interface_mapping:
    result: "pass"
    unmapped_cases: []
    unmapped_interfaces: []           # 接口未覆盖

  # 数据完整性检查
  data_completeness:
    result: "warning"
    missing_fields:
      - case_id: "TC003"
        field: "test_data.user_id"
        issue: "测试数据中的user_id需要脱敏处理"

# ============================================
# 复用建议（Reuse Recommendations）
# ============================================
reuse_recommendations:
  - scenario: "新功能：消费券批量发放"
    recommended_cases:
      - case_id: "TC001"
        reuse_type: "partial"         # full | partial | reference
        reuse_suggestion: "可复用查询消费券的前置步骤"

    recommended_patterns:
      - pattern: "参数校验模式"
        description: "TC002展示了参数校验的标准模式，可应用到新功能"

  - scenario: "新功能：消费券过期提醒"
    recommended_cases:
      - case_id: "TC003"
        reuse_type: "reference"
        reuse_suggestion: "参考空状态文案验证模式"
```

---

## 字段说明

### 必选字段（MUST）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `artifact_type` | string | 固定值 `normalized_cases` |
| `version` | string | 格式版本，当前为 `"1.0"` |
| `source_files` | array | 源文件列表 |
| `created_at` | string | 创建时间，ISO 8601 格式 |
| `normalizer` | string | 规范化工具名称 |
| `feature_groups` | array | 功能模块分组 |
| `test_cases` | array | 测试案例列表 |
| `statistics_summary` | object | 统计摘要 |

### 可选字段（OPTIONAL）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `defect_mapping` | array | 缺陷关联记录 |
| `quality_assessment` | object | 质量评估 |
| `consistency_check` | object | 一致性检查报告 |
| `reuse_recommendations` | array | 复用建议 |

---

## 提取规则

### 1. Excel 测试案例提取

**标准 Excel 格式**：

| 案例ID | 案例名称 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 类型 |
|--------|---------|---------|---------|---------|--------|------|
| TC001  | 查询消费券列表 | 用户已登录 | 1. 进入列表页... | 列表显示正确 | P0 | 正向 |

**提取逻辑**：

```python
def extract_excel_cases(file_path: str) -> List[Dict]:
    """从 Excel 文件提取测试案例

    :param file_path: Excel 文件路径
    :return: 测试案例列表
    """
    import pandas as pd

    df = pd.read_excel(file_path)
    cases = []

    for _, row in df.iterrows():
        case = {
            "case_id": row["案例ID"],
            "case_name": row["案例名称"],
            "preconditions": parse_preconditions(row["前置条件"]),
            "test_steps": parse_test_steps(row["测试步骤"]),
            "expected_results": parse_expected_results(row["预期结果"]),
            "priority": row["优先级"],
            "case_type": map_case_type(row["类型"]),
            "source": {
                "file": file_path,
                "row": _ + 2,  # Excel行号（从1开始，+1是表头）
                "original_case_id": row["案例ID"]
            }
        }
        cases.append(case)

    return cases
```

### 2. XMind 思维导图提取

**XMind 节点结构**：

```
消费券功能测试
├── 查询功能
│   ├── 正向场景
│   │   ├── 查询可用消费券列表
│   │   └── 查询消费券详情
│   ├── 异常场景
│   │   └── 缺少必填参数
│   └── 边界场景
│       └── 查询结果为空
└── 使用功能
    ├── 正向场景
    │   └── 正常使用消费券
    └── 异常场景
        └── 消费券已过期
```

**提取逻辑**：

```python
def extract_xmind_cases(file_path: str) -> List[Dict]:
    """从 XMind 文件提取测试案例

    :param file_path: XMind 文件路径
    :return: 测试案例列表
    """
    from xmindparser import xmind_to_dict

    xmind_data = xmind_to_dict(file_path)
    cases = []

    def traverse_node(node: Dict, path: List[str]):
        """递归遍历 XMind 节点

        :param node: XMind 节点
        :param path: 当前路径
        """
        topic = node.get("title", "")

        # 如果是叶子节点（测试案例）
        if not node.get("topics"):
            case = {
                "case_id": generate_case_id(topic),
                "case_name": topic,
                "feature_group": path[0] if len(path) > 0 else "未分类",
                "case_type": path[-2] if len(path) > 1 else "未分类",
                "source": {
                    "file": file_path,
                    "node": "/".join(path + [topic])
                }
            }
            cases.append(case)
        else:
            # 递归遍历子节点
            for child in node.get("topics", []):
                traverse_node(child, path + [topic])

    # 从根节点开始遍历
    for sheet in xmind_data:
        traverse_node(sheet["topic"], [])

    return cases
```

### 3. 案例类型映射

| 原始类型 | 标准类型 |
|---------|---------|
| 正向、正常、成功 | `positive` |
| 异常、失败、错误 | `negative` |
| 边界、临界、极限 | `boundary` |
| 兼容、版本、适配 | `compatibility` |
| 性能、响应、压力 | `performance` |

### 4. 优先级映射

| 原始优先级 | 标准优先级 |
|-----------|-----------|
| P0、高、High、关键 | `P0` |
| P1、中、Medium、重要 | `P1` |
| P2、低、Low、一般 | `P2` |

---

## 使用场景

### 场景1：为新功能推荐历史案例

**输入**：新功能需求（如"消费券批量发放"）

**处理逻辑**：
1. 分析新功能关键词（"消费券"、"批量"、"发放"）
2. 在 `feature_groups` 中查找相似功能（FG001、FG002）
3. 在 `test_cases` 中查找相似案例
4. 根据 `tags` 进行匹配度计算
5. 返回推荐案例列表

**输出**：`reuse_recommendations`

```python
def recommend_historical_cases(new_feature: Dict, historical_cases: Dict) -> List[Dict]:
    """为新功能推荐历史案例

    :param new_feature: 新功能需求
    :param historical_cases: 历史案例
    :return: 推荐案例列表
    """
    recommendations = []

    # 提取新功能关键词
    new_keywords = extract_keywords(new_feature["description"])

    # 遍历历史案例
    for case in historical_cases["test_cases"]:
        # 计算关键词匹配度
        case_keywords = case["tags"] + [case["case_name"]]
        similarity = calculate_similarity(new_keywords, case_keywords)

        if similarity > 0.5:  # 相似度阈值
            recommendations.append({
                "case_id": case["case_id"],
                "case_name": case["case_name"],
                "similarity": similarity,
                "reuse_type": "partial" if similarity < 0.8 else "full",
                "reuse_suggestion": generate_reuse_suggestion(case, new_feature)
            })

    # 按相似度排序
    recommendations.sort(key=lambda x: x["similarity"], reverse=True)

    return recommendations[:5]  # 返回前5个推荐
```

### 场景2：分析历史缺陷模式

**输入**：历史案例 + 缺陷记录

**输出**：缺陷模式分析报告

```yaml
defect_patterns:
  - pattern_id: "DP001"
    pattern_name: "参数校验缺失"
    occurrence_count: 8
    severity: "high"
    affected_features: ["查询功能", "使用功能"]
    typical_cases: ["TC002"]
    prevention_suggestion: "增加参数校验测试案例模板"
```

### 场景3：测试覆盖度分析

**输入**：历史案例 + 当前需求

**输出**：覆盖度分析报告

```yaml
coverage_analysis:
  overall_coverage: 85%

  covered_requirements:
    - requirement_id: "F001"
      coverage: 100%
      cases: ["TC001", "TC002", "TC003"]

  uncovered_requirements:
    - requirement_id: "F005"
      reason: "新需求，无历史案例"

  partial_coverage_requirements:
    - requirement_id: "F002"
      coverage: 60%
      missing_scenarios: ["并发场景", "网络异常场景"]
```

---

## 最佳实践

### 1. 案例命名规范

```yaml
# ✅ 正确：清晰描述测试场景
case_name: "Credit卡用户查询可用消费券列表"

# ❌ 错误：命名不清晰
case_name: "测试查询功能"
```

### 2. 测试步骤结构化

```yaml
# ✅ 正确：步骤清晰，预期结果明确
test_steps:
  - step: 1
    action: "进入消费券列表页面"
    expected_result: "页面正常加载，显示消费券列表"

# ❌ 错误：步骤不清晰
test_steps:
  - step: 1
    action: "测试查询"
    expected_result: "成功"
```

### 3. 测试数据脱敏

```yaml
# ✅ 正确：脱敏后的测试数据
test_data:
  user_id: "user_test_001"
  card_type: "CREDIT"

# ❌ 错误：包含真实用户信息
test_data:
  user_id: "real_user_123456"
  phone: "13800138000"
```

### 4. 标签规范化

```yaml
# ✅ 正确：标准化标签
tags: ["查询", "Credit卡", "正向场景", "P0"]

# ❌ 错误：标签不规范
tags: ["test", "查询功能测试", "重要"]
```

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03-19 | 初始版本，定义历史案例标准化格式 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [01-normalized-requirement-v2.md](./01-normalized-requirement-v2.md) - 标准化需求文档格式
- [06-manual-test-cases.md](./06-manual-test-cases.md) - 手工测试用例格式

### 参考实现

- [case-designer SKILL.md](../../skills/case-designer/SKILL.md)

---

**文档版本**: v1.0
**最后更新**: 2026-03-19
**维护者**: za-qe 团队