# 测试左移分析报告示例

> 本文档为 shift-left-analyzer 技能的完整输出示例

---

## 开发方案文档规范性检查

### 检查结果

✅ **符合规范**

### 检查项

- [x] 包含完整的接口设计信息
- [x] 接口定义清晰（直接列出或提供 UDoc 链接）
- [x] 接口参数说明详细完整
- [x] 包含接口错误码信息

---

## 接口路径校验结果

### 微服务接口识别

✅ **已识别 4 个微服务接口**：

| 序号 | 接口路径 | 所属微服务 | 完整路径 |
|-----|---------|-----------|---------|
| 1 | `/activity/create` | zabank_imc_activity_service | zabank_imc_activity_service/activity/create |
| 2 | `/activity/audit` | zabank_imc_activity_service | zabank_imc_activity_service/activity/audit |
| 3 | `/activity/publish` | zabank_imc_activity_service | zabank_imc_activity_service/activity/publish |
| 4 | `/activity/get` | zabank_imc_activity_service | zabank_imc_activity_service/activity/get |

---

## 接口信息汇总

### 接口1：创建活动

- **所属微服务**：zabank_imc_activity_service
- **接口路径**：zabank_imc_activity_service/activity/create
- **请求方法**：POST
- **功能描述**：创建一个新的营销活动

#### 请求参数

**JSON 格式**：
```json
{
  "activityName": "string",
  "startTime": "string",
  "endTime": "string",
  "activityType": "string",
  "targetUsers": ["string"]
}
```

**参数说明**：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| activityName | string | 是 | 活动名称，长度限制50字符 | "春节促销活动" |
| startTime | string | 是 | 开始时间，格式：yyyy-MM-dd HH:mm:ss | "2026-03-10 00:00:00" |
| endTime | string | 是 | 结束时间，格式：yyyy-MM-dd HH:mm:ss | "2026-03-20 00:00:00" |
| activityType | string | 是 | 活动类型：DISCOUNT/POINTS/REWARD | "DISCOUNT" |
| targetUsers | array | 否 | 目标用户ID列表 | ["U001", "U002"] |

#### 响应参数

**JSON 格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "string",
    "status": "string",
    "createdAt": "string"
  }
}
```

**参数说明**：

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| code | int | 状态码：200成功，400参数错误，500服务器错误 | 200 |
| message | string | 响应消息 | "success" |
| data.activityId | string | 活动ID | "ACT123456" |
| data.status | string | 活动状态：DRAFT/APPROVED/PUBLISHED/CLOSED | "DRAFT" |
| data.createdAt | string | 创建时间 | "2026-03-13 10:00:00" |

---

### 接口2：审核活动

- **所属微服务**：zabank_imc_activity_service
- **接口路径**：zabank_imc_activity_service/activity/audit
- **请求方法**：POST
- **功能描述**：审核活动，支持通过或拒绝

#### 请求参数

**JSON 格式**：
```json
{
  "activityId": "string",
  "action": "string",
  "comment": "string"
}
```

**参数说明**：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| activityId | string | 是 | 活动ID | "ACT123456" |
| action | string | 是 | 审核操作：APPROVE/REJECT | "APPROVE" |
| comment | string | 否 | 审核意见 | "活动内容符合规范" |

#### 响应参数

**JSON 格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "string",
    "status": "string",
    "auditedAt": "string"
  }
}
```

**参数说明**：

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| code | int | 状态码 | 200 |
| message | string | 响应消息 | "success" |
| data.activityId | string | 活动ID | "ACT123456" |
| data.status | string | 活动状态：APPROVED/REJECTED | "APPROVED" |
| data.auditedAt | string | 审核时间 | "2026-03-13 10:30:00" |

---

### 接口3：发布活动

- **所属微服务**：zabank_imc_activity_service
- **接口路径**：zabank_imc_activity_service/activity/publish
- **请求方法**：POST
- **功能描述**：发布已审核通过的活动

#### 请求参数

**JSON 格式**：
```json
{
  "activityId": "string"
}
```

**参数说明**：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| activityId | string | 是 | 活动ID | "ACT123456" |

#### 响应参数

**JSON 格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "string",
    "status": "string",
    "publishedAt": "string"
  }
}
```

**参数说明**：

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| code | int | 状态码 | 200 |
| message | string | 响应消息 | "success" |
| data.activityId | string | 活动ID | "ACT123456" |
| data.status | string | 活动状态 | "PUBLISHED" |
| data.publishedAt | string | 发布时间 | "2026-03-13 11:00:00" |

---

### 接口4：查询活动详情

- **所属微服务**：zabank_imc_activity_service
- **接口路径**：zabank_imc_activity_service/activity/get
- **请求方法**：GET
- **功能描述**：根据活动ID查询活动详情

#### 请求参数

**Query 参数**：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| activityId | string | 是 | 活动ID | "ACT123456" |

#### 响应参数

**JSON 格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "string",
    "activityName": "string",
    "status": "string",
    "startTime": "string",
    "endTime": "string",
    "activityType": "string",
    "targetUsers": ["string"],
    "createdAt": "string",
    "auditedAt": "string",
    "publishedAt": "string"
  }
}
```

**参数说明**：

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| code | int | 状态码 | 200 |
| message | string | 响应消息 | "success" |
| data.activityId | string | 活动ID | "ACT123456" |
| data.activityName | string | 活动名称 | "春节促销活动" |
| data.status | string | 活动状态 | "PUBLISHED" |
| data.startTime | string | 开始时间 | "2026-03-10 00:00:00" |
| data.endTime | string | 结束时间 | "2026-03-20 00:00:00" |
| data.activityType | string | 活动类型 | "DISCOUNT" |
| data.targetUsers | array | 目标用户ID列表 | ["U001", "U002"] |
| data.createdAt | string | 创建时间 | "2026-03-13 10:00:00" |
| data.auditedAt | string | 审核时间 | "2026-03-13 10:30:00" |
| data.publishedAt | string | 发布时间 | "2026-03-13 11:00:00" |

---

## 测试左移用例推荐

### 一、单接口测试用例

#### 接口1：创建活动

##### 功能测试

###### 1. 正常场景测试

- **用例描述**：使用有效参数创建活动
- **前置条件**：
  - 用户已登录
  - 具有创建活动权限
- **测试步骤**：
  - 步骤1：调用创建活动接口，传入有效参数
- **请求参数**：
```json
{
  "activityName": "春节促销活动",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT",
  "targetUsers": ["U001", "U002"]
}
```
- **预期结果**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "DRAFT",
    "createdAt": "2026-03-13 10:00:00"
  }
}
```

##### 边界值测试

###### 1. 活动名称长度边界测试

- **用例描述**：测试活动名称最大长度限制（50字符）
- **请求参数**：
```json
{
  "activityName": "这是一个非常非常非常非常非常非常非常非常非常非常长的活动名称1234567890",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "参数错误：activityName 长度不能超过50字符"
}
```

###### 2. 时间范围边界测试

- **用例描述**：测试活动时间跨度的边界（如最长1年）
- **请求参数**：
```json
{
  "activityName": "长期活动",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2027-03-11 00:00:00",  // 超过1年
  "activityType": "DISCOUNT"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "参数错误：活动时间跨度不能超过1年"
}
```

##### 异常测试

###### 1. 必填参数缺失

- **用例描述**：缺少必填参数 activityName
- **请求参数**：
```json
{
  "activityName": null,
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "参数错误：activityName 不能为空"
}
```

###### 2. 参数格式错误

- **用例描述**：传入错误的日期格式
- **请求参数**：
```json
{
  "activityName": "春节促销活动",
  "startTime": "2026/03/10",  // 错误格式
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "参数格式错误：startTime 格式应为 yyyy-MM-dd HH:mm:ss"
}
```

###### 3. 参数类型错误

- **用例描述**：传入错误的活动类型
- **请求参数**：
```json
{
  "activityName": "春节促销活动",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "INVALID_TYPE"  // 不支持的类型
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "参数错误：activityType 只能为 DISCOUNT/POINTS/REWARD"
}
```

##### 业务规则验证

###### 1. 活动时间校验

- **用例描述**：结束时间早于开始时间
- **请求参数**：
```json
{
  "activityName": "春节促销活动",
  "startTime": "2026-03-20 00:00:00",
  "endTime": "2026-03-10 00:00:00"  // 早于开始时间
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "业务规则错误：结束时间不能早于开始时间"
}
```

---

#### 接口2：审核活动

##### 功能测试

###### 1. 审核通过场景

- **用例描述**：审核通过活动
- **前置条件**：
  - 活动已创建（状态为 DRAFT）
  - 具有审核权限
- **请求参数**：
```json
{
  "activityId": "ACT123456",
  "action": "APPROVE",
  "comment": "活动内容符合规范"
}
```
- **预期结果**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "APPROVED",
    "auditedAt": "2026-03-13 10:30:00"
  }
}
```

###### 2. 审核拒绝场景

- **用例描述**：拒绝活动审核
- **请求参数**：
```json
{
  "activityId": "ACT123456",
  "action": "REJECT",
  "comment": "活动内容不符合规范"
}
```
- **预期结果**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "REJECTED",
    "auditedAt": "2026-03-13 10:30:00"
  }
}
```

##### 异常测试

###### 1. 活动不存在

- **用例描述**：审核不存在的活动
- **请求参数**：
```json
{
  "activityId": "INVALID_ID",
  "action": "APPROVE"
}
```
- **预期结果**：
```json
{
  "code": 404,
  "message": "活动不存在"
}
```

###### 2. 活动状态不允许审核

- **用例描述**：审核已发布的活动（状态为 PUBLISHED）
- **请求参数**：
```json
{
  "activityId": "ACT123456",
  "action": "APPROVE"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "活动状态错误：当前状态不允许审核"
}
```

---

#### 接口3：发布活动

##### 功能测试

###### 1. 正常发布场景

- **用例描述**：发布已审核通过的活动
- **前置条件**：
  - 活动已审核通过（状态为 APPROVED）
  - 具有发布权限
- **请求参数**：
```json
{
  "activityId": "ACT123456"
}
```
- **预期结果**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "PUBLISHED",
    "publishedAt": "2026-03-13 11:00:00"
  }
}
```

##### 异常测试

###### 1. 活动未审核

- **用例描述**：发布未审核的活动（状态为 DRAFT）
- **请求参数**：
```json
{
  "activityId": "ACT123456"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "活动未审核通过，无法发布"
}
```

###### 2. 活动已发布

- **用例描述**：重复发布已发布的活动
- **请求参数**：
```json
{
  "activityId": "ACT123456"
}
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "活动已发布，无需重复操作"
}
```

---

#### 接口4：查询活动详情

##### 功能测试

###### 1. 正常查询场景

- **用例描述**：查询已存在的活动详情
- **请求参数**：
```
GET /activity/get?activityId=ACT123456
```
- **预期结果**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "activityName": "春节促销活动",
    "status": "PUBLISHED",
    "startTime": "2026-03-10 00:00:00",
    "endTime": "2026-03-20 00:00:00",
    "activityType": "DISCOUNT",
    "targetUsers": ["U001", "U002"],
    "createdAt": "2026-03-13 10:00:00",
    "auditedAt": "2026-03-13 10:30:00",
    "publishedAt": "2026-03-13 11:00:00"
  }
}
```

##### 异常测试

###### 1. 活动不存在

- **用例描述**：查询不存在的活动
- **请求参数**：
```
GET /activity/get?activityId=INVALID_ID
```
- **预期结果**：
```json
{
  "code": 404,
  "message": "活动不存在"
}
```

###### 2. 缺少必填参数

- **用例描述**：缺少 activityId 参数
- **请求参数**：
```
GET /activity/get
```
- **预期结果**：
```json
{
  "code": 400,
  "message": "参数错误：activityId 不能为空"
}
```

---

### 二、场景测试用例

#### 场景1：活动创建到发布完整流程

**场景描述**：
测试从创建活动、审核活动到发布活动的完整业务流程，验证活动状态正确流转，数据一致性保持。

**涉及接口**：
1. 接口A：创建活动（`POST /activity/create`）- 返回 activityId
2. 接口B：审核活动（`POST /activity/audit`）- 使用 activityId
3. 接口C：发布活动（`POST /activity/publish`）- 使用 activityId
4. 接口D：查询活动详情（`GET /activity/get`）- 验证最终状态

**接口调用关系图**：
```
接口A（创建） → 接口B（审核） → 接口C（发布） → 接口D（查询验证）
    ↓              ↓              ↓
  返回ID        使用ID          使用ID
```

---

##### 测试用例1：正向流程-完整业务流程测试

- **用例描述**：测试从创建到发布的完整流程
- **前置条件**：
  - 用户已登录
  - 具有创建、审核、发布权限

**测试步骤**：

###### 步骤1：调用接口A创建活动

- **请求参数**：
```json
{
  "activityName": "春节促销活动",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT",
  "targetUsers": ["U001", "U002"]
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "DRAFT",
    "createdAt": "2026-03-13 10:00:00"
  }
}
```

###### 步骤2：使用步骤1返回的 activityId，调用接口B进行审核

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}",
  "action": "APPROVE",
  "comment": "活动内容符合规范"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "APPROVED",
    "auditedAt": "2026-03-13 10:30:00"
  }
}
```

###### 步骤3：调用接口C发布活动

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "PUBLISHED",
    "publishedAt": "2026-03-13 11:00:00"
  }
}
```

###### 步骤4：调用接口D查询活动详情，验证最终状态

- **请求参数**：
```
GET /activity/get?activityId={{步骤1返回的activityId}}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "activityName": "春节促销活动",
    "status": "PUBLISHED",
    "startTime": "2026-03-10 00:00:00",
    "endTime": "2026-03-20 00:00:00",
    "activityType": "DISCOUNT",
    "targetUsers": ["U001", "U002"],
    "createdAt": "2026-03-13 10:00:00",
    "auditedAt": "2026-03-13 10:30:00",
    "publishedAt": "2026-03-13 11:00:00"
  }
}
```

**验证点**：
- ✓ 每个步骤返回的状态码正确（200）
- ✓ 活动状态正确流转（DRAFT → APPROVED → PUBLISHED）
- ✓ activityId 在整个流程中保持一致
- ✓ 最终查询结果与预期一致
- ✓ 时间戳按照正确顺序生成（createdAt < auditedAt < publishedAt）

---

##### 测试用例2：异常流程-审核拒绝场景

- **用例描述**：测试审核拒绝后的处理流程

**测试步骤**：

###### 步骤1：调用接口A创建活动（同测试用例1）

###### 步骤2：调用接口B拒绝审核

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}",
  "action": "REJECT",
  "comment": "活动内容不符合规范"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "REJECTED",
    "auditedAt": "2026-03-13 10:30:00"
  }
}
```

###### 步骤3：尝试调用接口C发布活动

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}"
}
```

- **预期结果**：返回错误，提示活动未审核通过
```json
{
  "code": 400,
  "message": "活动未审核通过，无法发布"
}
```

**验证点**：
- ✓ 审核拒绝后状态变为 REJECTED
- ✓ 被拒绝的活动无法发布
- ✓ 返回清晰的错误提示

---

##### 测试用例3：边界场景-非法状态流转拦截

- **用例描述**：测试跳过审核直接发布的拦截

**测试步骤**：

###### 步骤1：创建活动（同测试用例1）

###### 步骤2：跳过审核，直接尝试发布

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}"
}
```

- **预期结果**：返回错误，提示需要先审核
```json
{
  "code": 400,
  "message": "活动尚未审核，无法发布"
}
```

**验证点**：
- ✓ 系统正确拦截非法状态流转（DRAFT → PUBLISHED）
- ✓ 返回清晰的错误提示

---

#### 场景2：查询验证场景

**场景描述**：
测试创建活动后立即查询，验证数据一致性。

**涉及接口**：
1. 接口A：创建活动（`POST /activity/create`）- 返回 activityId
2. 接口D：查询活动详情（`GET /activity/get`）- 使用 activityId

**接口调用关系图**：
```
接口A（创建） → 接口D（查询验证）
    ↓
  返回ID
```

---

##### 测试用例1：创建后立即查询

- **用例描述**：验证创建活动后数据立即可查询

**测试步骤**：

###### 步骤1：创建活动

- **请求参数**：
```json
{
  "activityName": "春节促销活动",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "data": {
    "activityId": "ACT123456",
    "status": "DRAFT"
  }
}
```

###### 步骤2：立即查询活动详情

- **请求参数**：
```
GET /activity/get?activityId={{步骤1返回的activityId}}
```

- **预期响应**：
```json
{
  "code": 200,
  "data": {
    "activityId": "ACT123456",
    "activityName": "春节促销活动",
    "status": "DRAFT",
    "startTime": "2026-03-10 00:00:00",
    "endTime": "2026-03-20 00:00:00"
  }
}
```

**验证点**：
- ✓ 创建的活动立即可查询
- ✓ 查询返回的数据与创建时一致
- ✓ activityId 正确传递

---

### 三、场景用例优先级建议

| 优先级 | 场景类型 | 场景名称 | 理由 | 预计工时 |
|-------|---------|---------|------|---------|
| **P0** | 核心业务流程 | 活动创建到发布完整流程 | 主流程，影响核心业务，用户使用频率高 | 2h |
| **P1** | 异常恢复 | 审核拒绝场景 | 异常处理，影响用户体验，需要验证回滚逻辑 | 1h |
| **P1** | 状态流转 | 非法状态流转拦截 | 保障业务规则正确性，防止数据异常 | 1h |
| **P2** | 查询验证 | 查询验证场景 | 验证数据一致性，确保创建后立即可用 | 0.5h |

**总计**：4 个场景用例，预计 4.5 小时

---

## 测试总结

### 测试覆盖情况

| 类型 | 数量 | 说明 |
|-----|------|------|
| **接口数量** | 4 | 创建、审核、发布、查询 |
| **单接口用例** | 15+ | 覆盖正常、边界、异常、业务规则 |
| **场景用例** | 4 | 覆盖核心流程、异常恢复、状态流转 |

### 风险点标注

| 风险等级 | 风险点 | 建议 |
|---------|-------|------|
| **高** | 状态流转控制 | 重点测试非法状态流转拦截，防止业务规则被绕过 |
| **中** | 并发创建活动 | 建议增加并发测试，验证数据一致性 |
| **中** | 时间校验逻辑 | 重点测试边界时间（开始时间=结束时间、跨年活动） |
| **低** | 活动名称特殊字符 | 建议测试特殊字符、表情符号的处理 |

### 测试建议

1. **优先执行 P0 场景用例**：核心业务流程必须首先验证通过
2. **关注状态流转**：重点测试各种状态流转路径，包括正向和非法流转
3. **数据一致性**：验证数据在整个流程中的一致性
4. **错误提示**：确保所有错误场景返回清晰的错误提示
5. **补充并发测试**：根据实际业务需求，增加并发场景测试
