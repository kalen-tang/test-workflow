# 需求验证报告格式规范

**版本**: v1.0
**创建时间**: 2026-03-18
**适用阶段**: 第二阶段（需求检查）
**输出工具**: requirement-validator Skill
**下游消费者**: manual-case-generator、项目决策

---

## 📋 目录

- [概述](#概述)
- [YAML 结构定义](#yaml-结构定义)
- [字段说明](#字段说明)
- [检查规则](#检查规则)
- [报告生成逻辑](#报告生成逻辑)
- [使用场景](#使用场景)

---

## 概述

### 目标

将需求文档（01-normalized-requirement）和设计文档（02-normalized-design）进行一致性验证，生成结构化的验证报告，为测试用例生成提供质量保证。

### 核心原则

1. **三级检查机制**：P0（必须通过）→ P1（必须记录）→ P2（建议项）
2. **追溯性**：每个检查结果关联具体的需求/设计条目
3. **可操作性**：问题和建议清晰明确，便于开发团队改进
4. **决策支持**：提供通过/有条件通过/不通过的明确结论

### 输入输出

- **输入1**：`01-normalized-requirement.yaml`（标准化需求文档）
- **输入2**：`02-normalized-design.yaml`（标准化设计文档）
- **输入3**：`04-code-diff-report.yaml`（代码差异报告，可选）
- **输出**：需求验证报告（YAML + Markdown 双格式）

---

## YAML 结构定义

### 完整结构

```yaml
# ============================================
# 元数据（Metadata）
# ============================================
artifact_type: validation_report      # 固定值
version: "1.0"                        # 格式版本
source_files:                         # 必须，输入源文件
  - "01-normalized-requirement-v2.yaml"
  - "02-normalized-design.yaml"
  - "04-code-diff-report.yaml"        # 可选
created_at: "2026-03-18T16:00:00+08:00"  # 必须，ISO 8601 格式
validator: "requirement-validator"     # 必须，验证工具名称

metadata:
  project_name: "卡消费回赠券增加Credit消费场景"
  requirement_version: "V1.01"        # 需求文档版本
  design_version: "V2.3"              # 设计文档版本
  validated_by: "requirement-validator v1.0"

# ============================================
# 验证结论（Validation Summary）
# ============================================
validation_summary:
  overall_result: "conditional_pass"  # pass | conditional_pass | fail
  overall_score: 85                   # 0-100 分

  # 统计摘要
  statistics:
    total_checks: 15                  # 总检查项数
    passed: 12                        # 通过项数
    warnings: 2                       # 警告项数
    failed: 1                         # 失败项数

  # 关键指标
  key_metrics:
    requirement_coverage: 100%        # 需求覆盖率
    design_coverage: 100%             # 设计覆盖率
    interface_coverage: 100%          # 接口覆盖率
    test_focus_coverage: 80%          # 测试重点覆盖率

# ============================================
# P0 级检查（必须通过）
# ============================================
p0_checks:
  - check_id: P0-001
    check_name: "功能与接口对应关系"
    description: "每个需求功能必须至少有一个对应的接口实现"
    result: "pass"                    # pass | fail
    details:
      - requirement_id: "F001"
        requirement_name: "Credit卡消费回赠发放"
        interface_id: "IF001"
        interface_name: "查询消费券列表"
        status: "mapped"
      - requirement_id: "F002"
        requirement_name: "消费券使用流程优化"
        interface_id: "IF002"
        interface_name: "使用消费券"
        status: "mapped"
    failures: []

  - check_id: P0-002
    check_name: "验收标准与测试场景对应"
    description: "每个验收标准必须至少有一个对应的测试场景"
    result: "pass"
    details:
      - acceptance_criteria_id: "AC001"
        acceptance_criteria: "Credit卡用户可查询消费券列表"
        test_scenarios:
          - scenario_id: "S001"
            scenario_name: "Credit卡用户正常查询消费券列表"
          - scenario_id: "S002"
            scenario_name: "Debit卡用户查询消费券列表（对比验证）"
        status: "covered"
    failures: []

  - check_id: P0-003
    check_name: "核心功能风险等级标注"
    description: "所有标记为test_focus=true的功能必须有风险等级标注"
    result: "fail"
    details:
      - requirement_id: "F001"
        requirement_name: "Credit卡消费回赠发放"
        test_focus: true
        risk_level: "high"
        status: "ok"
      - requirement_id: "F004"
        requirement_name: "消费券过期提醒"
        test_focus: true
        risk_level: null               # ❌ 未标注风险等级
        status: "missing_risk_level"
    failures:
      - requirement_id: "F004"
        field: "risk_level"
        issue: "核心功能缺少风险等级标注"
        severity: "high"
        action: "需要补充风险等级（high/medium/low）"

# ============================================
# P1 级检查（必须记录）
# ============================================
p1_checks:
  - check_id: P1-001
    check_name: "性能需求与接口响应时间对应"
    description: "性能需求必须在接口设计中有对应的响应时间约束"
    result: "warning"
    details:
      - performance_requirement_id: "PERF001"
        requirement: "开户材料校验 < 3秒"
        related_interface: "IF003"
        interface_name: "开户材料校验接口"
        interface_response_time: "2秒"
        status: "covered"
      - performance_requirement_id: "PERF002"
        requirement: "消费券查询 < 1秒"
        related_interface: "IF001"
        interface_name: "查询消费券列表"
        interface_response_time: null   # ⚠️ 设计文档未标注
        status: "missing_in_design"
    warnings:
      - performance_requirement_id: "PERF002"
        issue: "设计文档未标注接口响应时间"
        recommendation: "在设计文档中补充接口响应时间要求"

  - check_id: P1-002
    check_name: "业务规则与接口实现一致性"
    description: "需求文档中的业务规则必须与接口设计中的规则一致"
    result: "warning"
    details:
      - business_rule_id: "BR001"
        rule_description: "Credit卡消费满HKD 8000才可参与"
        design_implementation:
          interface_id: "IF001"
          parameter: "minAmount"
          value: "8000"
        status: "consistent"
      - business_rule_id: "BR003"
        rule_description: "开关LoanRestructureIDRP关闭时，重组Pending录入没有IDLP pending/IDP pending选项"
        design_implementation: null     # ⚠️ 设计文档未体现
        status: "not_found_in_design"
    warnings:
      - business_rule_id: "BR003"
        issue: "设计文档未体现该业务规则的实现"
        recommendation: "确认该业务规则是否需要在新版本中实现"

# ============================================
# P2 级检查（建议项）
# ============================================
p2_checks:
  - check_id: P2-001
    check_name: "测试场景覆盖度"
    description: "建议每个功能至少有正向、异常、边界三类测试场景"
    result: "warning"
    details:
      - requirement_id: "F001"
        requirement_name: "Credit卡消费回赠发放"
        test_scenarios:
          positive: 3                  # 正向场景数
          negative: 2                  # 异常场景数
          boundary: 1                  # 边界场景数
        coverage: "good"
      - requirement_id: "F002"
        requirement_name: "消费券使用流程优化"
        test_scenarios:
          positive: 1
          negative: 0                  # ⚠️ 缺少异常场景
          boundary: 0
        coverage: "insufficient"
    recommendations:
      - requirement_id: "F002"
        recommendation: "建议补充异常场景测试用例（如：消费券已过期、消费券金额不足等）"

  - check_id: P2-002
    check_name: "文档完整性"
    description: "检查需求文档和设计文档的缺失项"
    result: "warning"
    details:
      - source: "01-normalized-requirement"
        missing_items:
          - "第3.6章 Finance需求：GL账户、记账规则待补充"
          - "第3.7章 MMO需求：交易类型、MMO编码待确认"
      - source: "02-normalized-design"
        missing_items:
          - "降级方案未覆盖所有外部依赖"
    recommendations:
      - "补充Finance需求的GL账户信息"
      - "补充MMO需求的交易类型"
      - "完善降级方案覆盖范围"

# ============================================
# 一致性分析（Consistency Analysis）
# ============================================
consistency_analysis:
  # 需求与设计的对应关系
  requirement_design_mapping:
    - requirement_id: "F001"
      requirement_name: "Credit卡消费回赠发放"
      mapped_interfaces: ["IF001", "IF002"]
      mapped_database_tables: ["t_voucher"]
      mapping_status: "complete"

    - requirement_id: "F002"
      requirement_name: "消费券使用流程优化"
      mapped_interfaces: ["IF002"]
      mapped_database_tables: ["t_voucher_usage"]
      mapping_status: "complete"

  # 设计与需求的差异
  design_gap_analysis:
    - interface_id: "IF004"
      interface_name: "消费券批量导入"
      related_requirements: []         # 设计文档有接口，但需求文档未提及
      issue: "设计文档新增接口，需求文档未更新"
      severity: "medium"
      recommendation: "确认是否需要补充需求说明"

# ============================================
# 风险评估（Risk Assessment）
# ============================================
risk_assessment:
  overall_risk_level: "medium"         # low | medium | high

  high_risk_items:
    - item_id: "F001"
      item_name: "Credit卡消费回赠发放"
      risk_type: "financial"
      risk_description: "涉及资金发放，需要严格的财务对账机制"
      mitigation: "建议增加资金对账测试和异常审计测试"

  medium_risk_items:
    - item_id: "P0-003"
      item_name: "核心功能风险等级标注缺失"
      risk_type: "quality"
      risk_description: "测试优先级可能判断错误，导致高风险功能测试不足"
      mitigation: "立即补充风险等级标注"

  low_risk_items:
    - item_id: "P2-002"
      item_name: "文档完整性不足"
      risk_type: "documentation"
      risk_description: "部分非核心配置待补充"
      mitigation: "在后续迭代中补充文档"

# ============================================
# 改进建议（Recommendations）
# ============================================
recommendations:
  # 高优先级建议（必须处理）
  high_priority:
    - action: "补充F004功能的风险等级标注"
      reason: "P0-003检查失败，影响测试优先级判断"
      assignee: "产品经理"
      deadline: "2026-03-20"

    - action: "确认业务规则BR003的实现方案"
      reason: "设计文档未体现该业务规则"
      assignee: "开发团队"
      deadline: "2026-03-22"

  # 中优先级建议（建议处理）
  medium_priority:
    - action: "补充F002功能的异常测试场景"
      reason: "测试场景覆盖度不足"
      assignee: "测试团队"
      deadline: "2026-03-25"

    - action: "补充Finance需求的GL账户信息"
      reason: "文档完整性不足"
      assignee: "产品经理"
      deadline: "2026-03-23"

  # 低优先级建议（可选处理）
  low_priority:
    - action: "完善降级方案覆盖范围"
      reason: "提升系统稳定性"
      assignee: "开发团队"
      deadline: "2026-03-30"

# ============================================
# 决策建议（Decision Recommendation）
# ============================================
decision_recommendation:
  # 是否可以进入下一阶段（手工测试用例生成）
  can_proceed_to_next_stage: true

  # 前提条件
  prerequisites:
    - "修复P0-003检查失败项：补充F004风险等级标注"
    - "确认业务规则BR003的实现方案"

  # 后续跟踪事项
  follow_up_items:
    - "在手工测试用例生成时，重点关注高风险功能F001"
    - "在API测试用例生成时，补充性能测试断言（PERF002）"

# ============================================
# 附录（Appendix）
# ============================================
appendix:
  # 检查规则配置
  check_rules_config:
    p0_rules_file: "references/p0-check-rules.md"
    p1_rules_file: "references/p1-check-rules.md"
    p2_rules_file: "references/p2-check-rules.md"

  # 验证工具信息
  validator_info:
    tool_name: "requirement-validator"
    version: "1.0.0"
    documentation: "skills/requirement-validator/SKILL.md"
```

---

## 字段说明

### 必选字段（MUST）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `artifact_type` | string | 固定值 `validation_report` |
| `version` | string | 格式版本，当前为 `"1.0"` |
| `source_files` | array | 输入源文件列表 |
| `created_at` | string | 创建时间，ISO 8601 格式 |
| `validator` | string | 验证工具名称 |
| `validation_summary` | object | 验证结论摘要 |
| `p0_checks` | array | P0级检查结果 |
| `risk_assessment` | object | 风险评估 |
| `decision_recommendation` | object | 决策建议 |

### 可选字段（OPTIONAL）

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `p1_checks` | array | P1级检查结果 |
| `p2_checks` | array | P2级检查结果 |
| `consistency_analysis` | object | 一致性分析详情 |
| `recommendations` | object | 改进建议 |

---

## 检查规则

### P0 级检查（必须通过）

**定义**：影响测试核心质量，发现问题时必须立即修复

| 检查项 | 检查规则 | 失败后果 |
|-------|---------|---------|
| P0-001 功能与接口对应 | 每个需求功能必须有对应的接口实现 | 无法生成接口测试用例 |
| P0-002 验收标准与场景对应 | 每个验收标准必须有对应的测试场景 | 测试覆盖不完整 |
| P0-003 核心功能风险标注 | test_focus=true的功能必须有risk_level | 测试优先级错误 |
| P0-004 接口路径有效性 | 接口路径不能包含dmb（网关接口） | 测试环境无法访问 |
| P0-005 必填参数完整性 | 接口必填参数必须有类型定义 | 测试数据生成失败 |

### P1 级检查（必须记录）

**定义**：影响测试质量，必须记录问题并给出建议

| 检查项 | 检查规则 | 处理方式 |
|-------|---------|---------|
| P1-001 性能需求对应 | 性能需求与接口响应时间约束一致 | 记录到warnings，建议补充 |
| P1-002 业务规则一致 | 业务规则与接口实现一致 | 记录到warnings，确认实现 |
| P1-003 数据库字段对应 | 需求字段与数据库设计对应 | 记录到warnings，确认设计 |
| P1-004 兼容性场景覆盖 | 兼容性分析有对应的测试场景 | 记录到warnings，补充场景 |

### P2 级检查（建议项）

**定义**：影响测试效率，建议优化

| 检查项 | 检查规则 | 处理方式 |
|-------|---------|---------|
| P2-001 测试场景覆盖度 | 每个功能有正向/异常/边界场景 | 记录到recommendations |
| P2-002 文档完整性 | 缺失项已记录在missing_items | 记录到recommendations |
| P2-003 埋点需求实现 | 埋点需求与接口/日志对应 | 记录到recommendations |
| P2-004 降级方案完整 | 外部依赖有对应的降级方案 | 记录到recommendations |

---

## 报告生成逻辑

### 三阶段验证流程

```
阶段1：数据加载
├── 加载 01-normalized-requirement.yaml
├── 加载 02-normalized-design.yaml
└── 加载 04-code-diff-report.yaml（可选）

阶段2：一致性检查
├── P0 级检查（必须通过）
│   ├── 检查功能与接口对应关系
│   ├── 检查验收标准与场景对应
│   ├── 检查核心功能风险标注
│   ├── 检查接口路径有效性
│   └── 检查必填参数完整性
├── P1 级检查（必须记录）
│   ├── 检查性能需求对应
│   ├── 检查业务规则一致
│   ├── 检查数据库字段对应
│   └── 检查兼容性场景覆盖
└── P2 级检查（建议项）
    ├── 检查测试场景覆盖度
    ├── 检查文档完整性
    ├── 检查埋点需求实现
    └── 检查降级方案完整

阶段3：报告生成
├── 生成 YAML 格式报告
├── 生成 Markdown 格式报告（人类可读）
└── 输出决策建议
```

### 通过条件判断

| overall_result | 判断条件 |
|----------------|---------|
| **pass** | 所有P0检查通过，P1/P2无严重问题 |
| **conditional_pass** | P0检查有1-2个可快速修复的问题 |
| **fail** | P0检查有3个以上问题，或有关键性问题 |

---

## 使用场景

### 场景1：项目决策会议

**输入**：需求验证报告

**输出**：是否进入开发阶段的决策

**使用字段**：
- `validation_summary.overall_result` - 整体结论
- `decision_recommendation.can_proceed_to_next_stage` - 是否可进入下一阶段
- `recommendations.high_priority` - 必须处理的问题

### 场景2：手工测试用例生成

**输入**：需求验证报告 + 标准化需求文档

**输出**：针对性的手工测试用例

**使用字段**：
- `risk_assessment.high_risk_items` - 重点关注的高风险功能
- `consistency_analysis.requirement_design_mapping` - 功能与接口对应关系
- `p1_checks.warnings` - 需要在测试中重点验证的点

### 场景3：文档完善

**输入**：需求验证报告

**输出**：完善后的需求/设计文档

**使用字段**：
- `recommendations` - 改进建议（按优先级）
- `p2_checks.details.missing_items` - 文档缺失项

---

## Markdown 报告模板

除了 YAML 格式，还需生成人类可读的 Markdown 报告：

```markdown
# 需求验证报告

**项目名称**：卡消费回赠券增加Credit消费场景
**验证时间**：2026-03-18 16:00
**验证结论**：✅ 有条件通过（conditional_pass）
**综合评分**：85/100

---

## 📊 验证摘要

| 指标 | 数值 |
|------|------|
| 总检查项 | 15 |
| 通过项 | 12 ✅ |
| 警告项 | 2 ⚠️ |
| 失败项 | 1 ❌ |

---

## 🚨 P0 级检查结果

### ❌ 失败项

| 检查项 | 问题描述 | 影响范围 | 处理建议 |
|-------|---------|---------|---------|
| P0-003 核心功能风险标注 | F004功能缺少风险等级 | 测试优先级判断 | 立即补充risk_level |

---

## ⚠️ P1 级检查结果

### 警告项

| 检查项 | 问题描述 | 建议 |
|-------|---------|------|
| P1-001 性能需求对应 | PERF002接口未标注响应时间 | 补充接口响应时间要求 |
| P1-002 业务规则一致 | BR003业务规则未在设计中体现 | 确认是否需要实现 |

---

## 💡 改进建议

### 🔴 高优先级（必须处理）

- [ ] 补充F004功能的风险等级标注（负责人：产品经理，截止日期：2026-03-20）
- [ ] 确认业务规则BR003的实现方案（负责人：开发团队，截止日期：2026-03-22）

### 🟡 中优先级（建议处理）

- [ ] 补充F002功能的异常测试场景（负责人：测试团队，截止日期：2026-03-25）
- [ ] 补充Finance需求的GL账户信息（负责人：产品经理，截止日期：2026-03-23）

---

## ✅ 决策建议

**是否可进入下一阶段**：✅ 是

**前提条件**：
1. 修复P0-003检查失败项：补充F004风险等级标注
2. 确认业务规则BR003的实现方案

**后续跟踪事项**：
- 在手工测试用例生成时，重点关注高风险功能F001
- 在API测试用例生成时，补充性能测试断言（PERF002）
```

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03-18 | 初始版本，定义三级检查机制和报告格式 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [01-normalized-requirement-v2.md](./01-normalized-requirement-v2.md) - 标准化需求文档格式
- [02-normalized-design.md](./02-normalized-design.md) - 标准化设计文档格式

### 参考实现

- [requirement-validator SKILL.md](../../skills/requirement-validator/SKILL.md)

---

**文档版本**: v1.0
**最后更新**: 2026-03-18
**维护者**: qa-toolkit 团队