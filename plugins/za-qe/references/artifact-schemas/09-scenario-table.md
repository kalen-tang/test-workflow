# 场景案例表格式规范

**版本**: v1.0
**创建时间**: 2026-04-10
**适用阶段**: 场景案例设计（case-designer 产出）
**输出工具**: case-designer Skill
**下游消费者**: api-generator

---

## 概述

### 定位

场景案例表是 `case-designer` Skill 的结构化输出格式之一，与 PlantUML 可视化产出（流程图、MindMap）并列。场景表以 Markdown 表格形式输出，供 `api-generator` 直接解析消费，生成自动化测试代码。

### 与其他 Artifact 的关系

```
01-normalized-requirement（输入）
08-interface-data-report（输入，可选）
        ↓
09-scenario-table（本格式）
        ↓
07-api-test-cases（api-generator 消费）
```

### 与 06-scenario-cases 的关系

- **06-scenario-cases**（原 manual-test-cases）：PlantUML 流程图 + MindMap + XMind，面向人工评审
- **09-scenario-table**（本格式）：结构化 Markdown 表格，面向 api-generator 程序消费

两者由 case-designer 同时产出，场景内容一致，只是格式不同。

---

## Markdown 结构定义

```markdown
# 场景案例表

> 本场景表由 case-designer 生成，供 api-generator 消费。
> 需求文档：{规范化需求文档路径}
> 接口数据：{接口数据报告路径，如有}
> 生成时间：{ISO 8601}

---

## 场景总览

| 场景ID | 场景名称 | 类型 | 优先级 | 涉及接口 | 来源 |
|--------|---------|------|--------|---------|------|
| SC-001 | 正常创建活动 | positive | P0 | IF-001, IF-002 | AC-001 |
| SC-002 | 创建活动参数校验 | negative | P1 | IF-001 | BR-001 |
| SC-003 | 活动状态流转 | flow | P0 | IF-001, IF-003, IF-004 | US-001 |
| SC-004 | 边界-活动名称长度 | boundary | P2 | IF-001 | BR-002 |

### 类型说明

| 类型 | 说明 |
|------|------|
| positive | 正向场景，验证正常业务流程 |
| negative | 异常场景，验证错误处理和参数校验 |
| flow | 业务流程场景，涉及多接口串联和状态流转 |
| boundary | 边界场景，验证参数边界值和极限条件 |

### 来源说明

| 来源前缀 | 说明 |
|---------|------|
| AC-xxx | 来自验收标准（Acceptance Criteria） |
| US-xxx | 来自用户故事（User Story） |
| BR-xxx | 来自业务规则（Business Rule） |
| INFER | 基于接口依赖关系推断 |

---

## 场景详情

### SC-001 正常创建活动

**类型**：positive
**优先级**：P0
**来源**：AC-001
**前置条件**：用户已登录，具有创建权限

**步骤**：

| 步骤 | 操作 | 调用接口 | 请求要点 | 预期结果 |
|------|------|---------|---------|---------|
| 1 | 创建活动 | POST IF-001 /activity/create | name="测试活动", type=1, startTime="2026-04-15" | code=0000, 返回 activityId |
| 2 | 查询活动详情 | GET IF-002 /activity/detail | activityId={{步骤1.activityId}} | 活动名称="测试活动", status="DRAFT" |

**验证点**：
- [ ] 活动创建成功，返回有效 activityId
- [ ] 查询结果与创建参数一致（name、type、startTime）
- [ ] 活动初始状态为 DRAFT

---

### SC-002 创建活动参数校验

**类型**：negative
**优先级**：P1
**来源**：BR-001
**前置条件**：用户已登录

**步骤**：

| 步骤 | 操作 | 调用接口 | 请求要点 | 预期结果 |
|------|------|---------|---------|---------|
| 1 | 缺少必填参数 name | POST IF-001 /activity/create | name=空, type=1 | code=参数错误码 |
| 2 | type 超出范围 | POST IF-001 /activity/create | name="测试", type=999 | code=参数错误码 |
| 3 | startTime 早于当前时间 | POST IF-001 /activity/create | name="测试", startTime="2020-01-01" | code=业务错误码 |

**验证点**：
- [ ] 缺少 name 时返回明确的参数校验错误
- [ ] type 非法值时返回参数错误
- [ ] 开始时间不合法时返回业务错误

---

### SC-003 活动状态流转

**类型**：flow
**优先级**：P0
**来源**：US-001
**前置条件**：用户已登录，具有管理权限

**步骤**：

| 步骤 | 操作 | 调用接口 | 请求要点 | 预期结果 |
|------|------|---------|---------|---------|
| 1 | 创建活动 | POST IF-001 /activity/create | name="流转测试" | activityId, status=DRAFT |
| 2 | 提交审核 | POST IF-003 /activity/submit | activityId={{步骤1.activityId}} | status=PENDING |
| 3 | 审核通过 | POST IF-004 /activity/approve | activityId={{步骤1.activityId}}, action=APPROVE | status=ACTIVE |
| 4 | 查询确认 | GET IF-002 /activity/detail | activityId={{步骤1.activityId}} | status=ACTIVE |

**验证点**：
- [ ] 状态从 DRAFT → PENDING → ACTIVE 正确流转
- [ ] 每步操作后查询状态一致
- [ ] 非法状态流转被拒绝（如 DRAFT 直接到 ACTIVE）

---
```

---

## 字段说明

### 场景总览表（必选）

| 列 | 类型 | 必填 | 说明 |
|----|------|------|------|
| 场景ID | String | 是 | 格式 `SC-NNN`，全局唯一 |
| 场景名称 | String | 是 | 简短描述，如"正常创建活动" |
| 类型 | Enum | 是 | positive / negative / flow / boundary |
| 优先级 | Enum | 是 | P0 / P1 / P2 |
| 涉及接口 | String | 是 | 接口 ID 列表（来自 08-interface-data-report），逗号分隔 |
| 来源 | String | 是 | AC-xxx / US-xxx / BR-xxx / INFER |

### 场景详情（必选）

| 字段 | 必填 | 说明 |
|------|------|------|
| 类型 | 是 | 同总览表 |
| 优先级 | 是 | 同总览表 |
| 来源 | 是 | 同总览表 |
| 前置条件 | 是 | 执行场景前需要满足的条件 |
| 步骤表 | 是 | 每步的操作、接口、请求、预期 |
| 验证点 | 是 | 该场景需要验证的断言列表 |

### 步骤表列定义

| 列 | 必填 | 说明 |
|----|------|------|
| 步骤 | 是 | 步骤序号 |
| 操作 | 是 | 操作描述（如"创建活动"） |
| 调用接口 | 是 | 格式：`{METHOD} {IF-ID} {PATH}` |
| 请求要点 | 是 | 关键请求参数，使用 `{{步骤N.字段名}}` 标记数据传递 |
| 预期结果 | 是 | 预期响应的关键字段或状态 |

---

## 数据传递标记

场景步骤间的数据传递使用 `{{步骤N.字段名}}` 格式：

| 标记 | 含义 |
|------|------|
| `{{步骤1.activityId}}` | 使用步骤 1 响应中的 activityId 字段 |
| `{{步骤2.status}}` | 使用步骤 2 响应中的 status 字段 |
| `{{步骤1.data.list[0].id}}` | 使用步骤 1 响应中嵌套字段 |

api-generator 在生成代码时，将 `{{}}` 标记转换为变量提取和传递逻辑。

---

## 生成规则

### 场景来源优先级

当同时拥有规范化需求文档和接口数据报告时：

1. **从验收标准生成**（最优先）：每个 AC 至少对应一个场景
2. **从用户故事生成**：构建端到端业务流程场景
3. **从业务规则生成**：生成边界和异常场景
4. **从接口依赖推断**：补充接口串联的 flow 场景

### 仅有需求文档时

- 场景的"调用接口"列可留空或填写推断的接口描述
- api-generator 无法直接消费，需等待接口数据补充

### 优先级分配规则

| 优先级 | 分配条件 |
|--------|---------|
| P0 | 核心业务主流程、涉及资金/安全的场景 |
| P1 | 常见异常流程、非核心但重要的功能 |
| P2 | 边界值测试、低频使用场景 |

---

## 下游消费方式

### api-generator 消费

1. **解析场景总览表**：获取场景列表和涉及的接口
2. **解析步骤表**：
   - 从"调用接口"列提取接口 ID 和方法
   - 结合 08-interface-data-report 获取完整的请求/响应参数
   - 从"请求要点"列提取测试数据
   - 从"预期结果"列生成断言
3. **处理数据传递**：将 `{{步骤N.字段名}}` 转换为变量提取代码
4. **生成测试代码**：每个场景生成一个 pytest 测试函数（或测试类）

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-04-10 | 初始版本 |
