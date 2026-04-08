# 完整输出格式参考

## 输出结构

测试左移分析报告应包含以下几个部分：

1. 开发方案文档规范性检查
2. 接口路径校验结果
3. 接口信息汇总
4. 测试左移用例推荐
   - 一、单接口测试用例
   - 二、场景测试用例
   - 三、场景用例优先级建议

---

## 第一部分：开发方案文档规范性检查

```markdown
## 开发方案文档是否符合规范

### 检查结果

✅ **符合规范** / ❌ **不符合规范**

### 检查项

- [ ] 包含完整的接口设计信息
- [ ] 接口定义清晰（直接列出或提供 UDoc 链接）
- [ ] 接口参数说明详细完整
- [ ] 包含接口错误码信息

### 建议

如果不符合规范，提示用户：
- 补充接口设计信息
- 提供 UDoc 接口文档链接
- 完善接口参数说明
```

---

## 第二部分：接口路径校验结果

```markdown
## 接口路径校验结果

### 网关接口检测

⚠️ **检测到 1 个网关接口，需要替换为微服务接口**：

| 序号 | 检测到的接口路径 | 问题 | 建议 |
|-----|----------------|------|------|
| 1 | `/dmb/api/activity/list` | 网关接口 | 请提供对应的微服务接口路径 |

### 微服务接口识别

✅ **已识别 3 个微服务接口**：

| 序号 | 接口路径 | 所属微服务 | 完整路径 |
|-----|---------|-----------|---------|
| 1 | `/activity/create` | zabank_imc_activity_service | zabank_imc_activity_service/activity/create |
| 2 | `/activity/audit` | zabank_imc_activity_service | zabank_imc_activity_service/activity/audit |
| 3 | `/activity/publish` | zabank_imc_activity_service | zabank_imc_activity_service/activity/publish |
```

---

## 第三部分：接口信息汇总

```markdown
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
  "activityType": "string"
}
```

**参数说明**：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| activityName | string | 是 | 活动名称 | "春节促销活动" |
| startTime | string | 是 | 开始时间 | "2026-03-10 00:00:00" |
| endTime | string | 是 | 结束时间 | "2026-03-20 00:00:00" |
| activityType | string | 是 | 活动类型 | "DISCOUNT" |

#### 响应参数

**JSON 格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "string",
    "status": "string"
  }
}
```

**参数说明**：

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| code | int | 状态码 | 200 |
| message | string | 响应消息 | "success" |
| data.activityId | string | 活动ID | "ACT123456" |
| data.status | string | 活动状态 | "DRAFT" |

---

### 接口2：审核活动

[同上结构...]

---

### 接口3：发布活动

[同上结构...]
```

---

## 第四部分：测试左移用例推荐

### 一、单接口测试用例

```markdown
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
  "activityType": "DISCOUNT"
}
```
- **预期结果**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "DRAFT"
  }
}
```

##### 边界值测试

###### 1. 活动名称长度边界测试

- **用例描述**：测试活动名称最大长度限制
- **请求参数**：
```json
{
  "activityName": "非常非常非常非常非常长的活动名称...[共100个字符]",
  "startTime": "2026-03-10 00:00:00",
  "endTime": "2026-03-20 00:00:00",
  "activityType": "DISCOUNT"
}
```
- **预期结果**：
  - 如果限制50字符：返回错误提示
  - 如果限制100字符：成功创建

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

[同上结构...]

---

#### 接口3：发布活动

[同上结构...]
```

---

### 二、场景测试用例

```markdown
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
  "activityType": "DISCOUNT"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "DRAFT"
  }
}
```

###### 步骤2：使用步骤1返回的 activityId，调用接口B进行审核

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}",
  "action": "APPROVE",
  "comment": "审核通过"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "APPROVED"
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
    "status": "PUBLISHED"
  }
}
```

###### 步骤4：调用接口D查询活动详情，验证最终状态

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
    "activityName": "春节促销活动",
    "status": "PUBLISHED",
    "startTime": "2026-03-10 00:00:00",
    "endTime": "2026-03-20 00:00:00"
  }
}
```

**验证点**：
- ✓ 每个步骤返回的状态码正确（200）
- ✓ 活动状态正确流转（DRAFT → APPROVED → PUBLISHED）
- ✓ activityId 在整个流程中保持一致
- ✓ 最终查询结果与预期一致

---

##### 测试用例2：异常流程-审核拒绝场景

- **用例描述**：测试审核拒绝后的处理流程

**测试步骤**：

###### 步骤1：调用接口A创建活动（同上）

###### 步骤2：调用接口B拒绝审核

- **请求参数**：
```json
{
  "activityId": "{{步骤1返回的activityId}}",
  "action": "REJECT",
  "reason": "活动内容不符合规范"
}
```

- **预期响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "activityId": "ACT123456",
    "status": "REJECTED"
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

###### 步骤1：创建活动后，跳过审核步骤，直接尝试发布

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
- ✓ 系统正确拦截非法状态流转
- ✓ 返回清晰的错误提示

---

#### 场景2：[另一个业务场景]

[同上结构...]
```

---

### 三、场景用例优先级建议

```markdown
### 三、场景用例优先级建议

| 优先级 | 场景类型 | 场景名称 | 理由 | 预计工时 |
|-------|---------|---------|------|---------|
| **P0** | 核心业务流程 | 活动创建到发布完整流程 | 主流程，影响核心业务，用户使用频率高 | 2h |
| **P1** | 异常恢复 | 审核拒绝场景 | 异常处理，影响用户体验，需要验证回滚逻辑 | 1h |
| **P1** | 状态流转 | 非法状态流转拦截 | 保障业务规则正确性，防止数据异常 | 1h |
| **P2** | 并发场景 | 并发创建活动 | 高并发下的一致性保障，验证幂等性 | 1.5h |

**总计**：4 个场景用例，预计 5.5 小时
```

---

## 完整报告示例

详细的完整报告示例请参考 `examples/sample-analysis-report.md`。
