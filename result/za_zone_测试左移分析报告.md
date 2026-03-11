# 企业福利（ZA Zone）测试左移分析报告

## 开发方案文档质量评估

✅ **文档符合规范**

开发方案文档包含了完整的接口设计信息，包括：
- 接口路径、请求方法、请求参数、响应参数等详细信息
- 业务流程描述清晰
- 数据模型定义完整
- 包含错误处理和兼容性分析

## 接口路径校验结果

⚠️ **检测到网关接口，需要替换为微服务接口**

以下接口为网关接口（包含 `dmb`），测试左移需要使用对应的微服务接口：

| 网关接口 | 建议微服务接口 |
|---------|---------------|
| /dmb/nok9iy/activity/zazone/getVerifyCode | zabank_imc_activity_service/activity/zazone/getVerifyCode |
| /dmb/npo9iy/activity/zazone/verify | zabank_imc_activity_service/activity/zazone/verify |
| /dmb/nqe3iy/activity/zazone/entryPage | zabank_imc_activity_service/activity/zazone/entryPage |
| /dmb/nwe5iy/activity/zazone/homePage | zabank_imc_activity_service/activity/zazone/homePage |
| /dmb/ngui7y/activity/zazone/queryInviteRecord | zabank_imc_activity_service/activity/zazone/queryInviteRecord |
| /dmb/npo9iy/activity/zazone/quitActivity | zabank_imc_activity_service/activity/zazone/quitActivity |
| /dmb/n5kliy/activity/zazone/queryInterest | zabank_imc_activity_service/activity/zazone/queryInterest |

---

## 接口信息汇总

### 接口1：获取验证码
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/getVerifyCode
- **请求方法**: POST
- **功能描述**: 用户通过企业/校园邮箱获取验证码，用于企业福利认证
- **请求参数**:
```json
{
  "revIdType": "EMAIL",
  "revId": "xxx@xxx",
  "redeemCode": "xxxx"
}
```

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| revIdType | String | 是 | 认证类型，固定值EMAIL | "EMAIL" |
| revId | String | 是 | 邮箱地址 | "user@company.com" |
| redeemCode | String | 是 | 邀请码 | "ABC123" |

- **响应参数**:
```json
{
  "code": "000000",
  "responseCode": "UMP000000",
  "status": "SUCCESS",
  "value": {
    "tokenId": "XXX"
  },
  "msg": "SUCCESS",
  "serverTime": "2025-07-29 18:32:05",
  "success": true
}
```

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| code | String | 业务状态码 | "000000" |
| status | String | 处理状态 | "SUCCESS" |
| value.tokenId | String | 验证令牌ID | "XXX" |
| success | Boolean | 是否成功 | true |

---

### 接口2：企业认证
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/verify
- **请求方法**: POST
- **功能描述**: 用户通过验证码完成企业认证，加入企业福利团队
- **业务逻辑**:
  1. 参与成功且当前团队组团中，当前用户发activity
  2. 参与成功且当前团队已成团，由rcs企业会员模块触发activity发放流程
  3. 用户获得试用权益时发通知：push/email/activity
  4. 新增用户参与记录user_verify_mgm，后续增加校验专属邀请码只能使用一次

- **请求参数**:
```json
{
  "customerNo": "XXX",
  "tokenId": "XXX",
  "revIdType": "EMAIL",
  "revId": "xxx@xxx",
  "verifyCode": "XXX",
  "redeemCode": "xxx"
}
```

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| customerNo | String | 是 | 客户编号 | "C123456" |
| tokenId | String | 是 | 验证令牌ID（来自getVerifyCode） | "XXX" |
| revIdType | String | 是 | 认证类型 | "EMAIL" |
| revId | String | 是 | 邮箱地址 | "user@company.com" |
| verifyCode | String | 是 | 验证码 | "123456" |
| redeemCode | String | 是 | 邀请码 | "ABC123" |

- **响应参数**:
```json
{
  "code": "000000",
  "responseCode": "UMP000000",
  "status": "SUCCESS",
  "value": {
    "revId": "xxx@xxx",
    "currentLevel": 1,
    "currentTeamCount": 50,
    "levelChange": true,
    "advCodeUseSuccessFlag": true,
    "levelsConfig": [{
      "level": 1,
      "peopleNum": 20
    }]
  },
  "success": true
}
```

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| value.revId | String | 认证邮箱 | "user@company.com" |
| value.currentLevel | Integer | 当前等级（0=未成团） | 1 |
| value.currentTeamCount | Integer | 已成团人数 | 50 |
| value.levelChange | Boolean | 等级是否变化 | true |
| value.advCodeUseSuccessFlag | Boolean | 专属邀请码是否核销成功 | true |
| value.levelsConfig | Array | 等级配置列表 | [...] |

---

### 接口3：活动状态查询
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/entryPage
- **请求方法**: POST
- **功能描述**: 查询用户在企业福利活动中的参与状态和当前等级

- **请求参数**:
```json
{
  "customerNo": "XXX"
}
```

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| customerNo | String | 是 | 客户编号 | "C123456" |

- **响应参数**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": {
    "employeeFlag": false,
    "employeeRelativesFlag": true,
    "joinFlag": true,
    "currentLevel": 1,
    "currentTeamCount": 50,
    "rewardNum": 7,
    "levelsConfig": [{
      "level": 1,
      "peopleNum": 20
    }]
  },
  "success": true
}
```

| 字段名 | 类型 | 说明 | 示例值 |
|-------|------|------|-------|
| value.employeeFlag | Boolean | 是否员工 | false |
| value.employeeRelativesFlag | Boolean | 是否亲友 | true |
| value.joinFlag | Boolean | 是否已参与 | true |
| value.currentLevel | Integer | 当前等级 | 1 |
| value.currentTeamCount | Integer | 已成团人数 | 50 |
| value.rewardNum | Integer | 当前等级奖励数量 | 7 |

---

### 接口4：活动首页信息查询
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/homePage
- **请求方法**: POST
- **功能描述**: 获取活动首页完整信息，包括用户状态、邀请信息、权益列表等

- **请求参数**:
```json
{
  "customerNo": "XXX"
}
```

- **响应参数**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": {
    "employeeFlag": false,
    "employeeRelativesFlag": true,
    "joinFlag": true,
    "redeemCode": "xxx",
    "advCodeUseSuccessFlag": true,
    "advCodeExpireTime": 123,
    "advRightExpireFlag": false,
    "nickName": "昵称",
    "inviteSuccessCount": 4,
    "teamTag": "@xxx",
    "currentLevel": 1,
    "preLevel": 1,
    "currentTeamCount": 50,
    "levelsConfig": [{
      "level": 1,
      "peopleNum": 20,
      "rewards": [{
        "interestType": "27",
        "subInterestType": "1",
        "interestNo": "xxx",
        "couponNo": "xxx",
        "interestName": "权益名称",
        "interestDesc": "权益描述",
        "interestJumpUrl": "跳转链接",
        "interestSendState": "1",
        "couponState": "1",
        "interestIconUrl": "图标URL",
        "interestTag": "zone_deposit"
      }]
    }]
  },
  "success": true
}
```

**权益类型映射关系**:
- 懒人钱罐权益：interestType=27, subInterestType=1
- 股票佣金权益：interestType=28, subInterestType=1
- 优惠券-咖啡消费回赠：interestType=16, subInterestType=65
- 优惠券-保险折扣：interestType=16, subInterestType=32
- 优惠券-海外汇款返现：interestType=16, subInterestType=54
- 优惠券-货币兑换立减：interestType=16, subInterestType=76

---

### 接口5：邀请记录查询
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/queryInviteRecord
- **请求方法**: POST
- **功能描述**: 分页查询用户的邀请记录

- **请求参数**:
```json
{
  "startKey": "分页查询Key",
  "pageSize": 10
}
```

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| startKey | String | 否 | 分页查询Key，首次查询不需要 | "key123" |
| pageSize | Integer | 是 | 每页查询返回数 | 10 |

- **响应参数**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": {
    "details": [{
      "nickName": "昵称",
      "inviteTime": 1234567890
    }],
    "pageInfo": {
      "nextKey": "下一页键值"
    }
  },
  "success": true
}
```

---

### 接口6：退出活动
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/quitActivity
- **请求方法**: POST
- **功能描述**: 用户退出企业福利活动
- **业务逻辑**:
  1. 退出成功，当前用户发activity、push、email
  2. 人数不足下月将会降级/退团时（当月首次才触发），异步：全员发push、email
  3. 销户增加退出处理（监听销户MQ）

- **请求参数**:
```json
{
  "customerNo": "XXX"
}
```

- **响应参数**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": null,
  "success": true
}
```

---

### 接口7：福利详情权益列表查询
- **所属微服务**: zabank_imc_activity_service
- **接口路径**: zabank_imc_activity_service/activity/zazone/queryInterest
- **请求方法**: POST
- **功能描述**: 查询用户的权益详情列表，包括不同等级的权益配置

- **请求参数**:
```json
{
  "customerNo": "XXX"
}
```

- **响应参数**:
```json
{
  "code": "000000",
  "responseCode": "UMP000000",
  "value": {
    "currentLevel": 1,
    "advCodeExpireTime": 123,
    "advRightExpireFlag": false,
    "interestList": [{
      "interestType": "DISCOUNT",
      "subInterestType": "4",
      "interestName": "权益产品名",
      "interestDesc": "权益产品描述",
      "interestIconUrl": "图标URL",
      "interestJumpUrl": "跳转链接",
      "interestTag": "zone_deposit",
      "levelInterestConfigList": [{
        "level": 2,
        "interestDesc": "权益产品描述"
      }]
    }]
  },
  "success": true
}
```

---

### 接口8：用户升级/降级接口（RCS模块）
- **所属微服务**: zabank_rcs_core
- **接口路径**: zabank_rcs_core/rc/groupMembership/user/updategrade
- **请求方法**: POST
- **功能描述**: RCS权益模块接口，处理用户等级变更和权益发放
- **业务逻辑**:
  - 用户升级时：立即发放新等级权益，团队升级需同步处理触发用户，异步处理其他团员
  - 用户降级时：更新用户等级，次月按新等级发放权益
  - 幂等性保证：同一用户同一等级同一月份仅发放一次

- **请求参数**:
```json
{
  "serialNo": "流水id",
  "memberType": "4",
  "userId": 123456789,
  "teamLevel": "T1",
  "operationType": "1",
  "businessId": "TEAM_001",
  "teamLevelChange": false,
  "eventTime": "2025-07-29 18:32:05"
}
```

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| serialNo | String | 是 | 流水id，幂等 | "SN123456" |
| memberType | String | 是 | 会员类型，固定值"4" | "4" |
| userId | Long | 是 | 用户ID | 123456789 |
| teamLevel | String | 是 | 用户的团队等级 | "T1" |
| operationType | String | 是 | 用户参与标识（1参加，2退出） | "1" |
| businessId | String | 是 | 团队标识 | "TEAM_001" |
| teamLevelChange | Boolean | 是 | 团队等级是否变动 | false |
| eventTime | String | 是 | 事件发生时间 | "2025-07-29 18:32:05" |

- **响应参数**:
```json
{
  "code": "000000",
  "responseCode": "UMP000000",
  "status": "SUCCESS",
  "success": true
}
```

---

### 接口9：查询用户权益信息（RCS模块）
- **所属微服务**: zabank_rcs_core
- **接口路径**: zabank_rcs_core/rc/rights/interest/list
- **请求方法**: POST
- **功能描述**: 查询用户已获得的权益列表

- **请求参数**:
```json
{
  "userId": 123456789,
  "customerNo": "",
  "productType": "ZAZone"
}
```

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| userId | Long | 是 | 用户ID | 123456789 |
| customerNo | String | 否 | 客户编号 | "C123456" |
| productType | String | 是 | 产品类型，固定值"ZAZone" | "ZAZone" |

- **响应参数**:
```json
{
  "interestList": [{
    "interestName": "权益产品名称1",
    "interestDesc": "权益产品描述1",
    "interestInstruction": "权益说明1",
    "productId": "PROD001",
    "interestId": "INT001",
    "interestType": "DISCOUNT",
    "subInterestType": "4",
    "interestIconUrl": "https://example.com/icon1.png",
    "interestJumpUrl": "https://example.com/jump1",
    "interestTag": "zone_deposit",
    "interestSendState": "1",
    "couponState": "1"
  }]
}
```

---

# 测试左移用例推荐

## 一、单接口测试用例

### 接口1：获取验证码（getVerifyCode）

#### 功能测试

##### 1. 正常场景测试
- **用例描述**: 使用有效的企业邮箱和邀请码获取验证码
- **前置条件**:
  - 邮箱格式正确
  - 邀请码有效
- **测试步骤**:
  - 步骤1: 调用获取验证码接口
- **请求参数**:
```json
{
  "revIdType": "EMAIL",
  "revId": "test@company.com",
  "redeemCode": "ABC123"
}
```
- **预期结果**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": {
    "tokenId": "TOKEN_123456"
  },
  "success": true
}
```

#### 异常测试

##### 1. 参数校验测试 - 邮箱格式错误
- **用例描述**: 邮箱格式不正确
- **请求参数**:
```json
{
  "revIdType": "EMAIL",
  "revId": "invalid-email",
  "redeemCode": "ABC123"
}
```
- **预期结果**:
```json
{
  "code": "400",
  "message": "邮箱格式错误",
  "success": false
}
```

##### 2. 参数校验测试 - 必填参数缺失
- **用例描述**: revId参数缺失
- **请求参数**:
```json
{
  "revIdType": "EMAIL",
  "redeemCode": "ABC123"
}
```
- **预期结果**:
```json
{
  "code": "400",
  "message": "参数错误：revId不能为空",
  "success": false
}
```

##### 3. 业务规则测试 - 邀请码无效
- **用例描述**: 使用无效或已过期的邀请码
- **请求参数**:
```json
{
  "revIdType": "EMAIL",
  "revId": "test@company.com",
  "redeemCode": "INVALID_CODE"
}
```
- **预期结果**:
```json
{
  "code": "BIZ_ERROR",
  "message": "邀请码无效或已过期",
  "success": false
}
```

---

### 接口2：企业认证（verify）

#### 功能测试

##### 1. 正常场景测试 - 首次认证成功
- **用例描述**: 用户首次通过验证码完成企业认证
- **前置条件**:
  - 已获取有效的tokenId
  - 验证码正确
  - 用户未参与活动
- **请求参数**:
```json
{
  "customerNo": "C123456",
  "tokenId": "TOKEN_123456",
  "revIdType": "EMAIL",
  "revId": "test@company.com",
  "verifyCode": "123456",
  "redeemCode": "ABC123"
}
```
- **预期结果**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": {
    "revId": "test@company.com",
    "currentLevel": 0,
    "currentTeamCount": 1,
    "levelChange": true,
    "advCodeUseSuccessFlag": true
  },
  "success": true
}
```

##### 2. 正常场景测试 - 认证后团队升级
- **用例描述**: 用户认证后，团队人数达到升级阈值
- **前置条件**: 团队当前19人，达到20人后升级到Lv.1
- **请求参数**: 同上
- **预期结果**:
```json
{
  "code": "000000",
  "value": {
    "currentLevel": 1,
    "currentTeamCount": 20,
    "levelChange": true
  },
  "success": true
}
```

#### 异常测试

##### 1. 参数校验测试 - tokenId无效
- **用例描述**: 使用无效或过期的tokenId
- **请求参数**:
```json
{
  "customerNo": "C123456",
  "tokenId": "INVALID_TOKEN",
  "revIdType": "EMAIL",
  "revId": "test@company.com",
  "verifyCode": "123456",
  "redeemCode": "ABC123"
}
```
- **预期结果**:
```json
{
  "code": "AUTH_ERROR",
  "message": "tokenId无效或已过期",
  "success": false
}
```

##### 2. 参数校验测试 - 验证码错误
- **用例描述**: 输入错误的验证码
- **请求参数**:
```json
{
  "customerNo": "C123456",
  "tokenId": "TOKEN_123456",
  "revIdType": "EMAIL",
  "revId": "test@company.com",
  "verifyCode": "000000",
  "redeemCode": "ABC123"
}
```
- **预期结果**:
```json
{
  "code": "VERIFY_ERROR",
  "message": "验证码错误",
  "success": false
}
```

##### 3. 业务规则测试 - 专属邀请码已使用
- **用例描述**: 专属邀请码只能使用一次
- **前置条件**: 该邀请码已被使用过
- **请求参数**: 同正常场景
- **预期结果**:
```json
{
  "code": "BIZ_ERROR",
  "message": "专属邀请码已被使用",
  "value": {
    "advCodeUseSuccessFlag": false
  },
  "success": false
}
```

##### 4. 业务规则测试 - 用户已参与活动
- **用例描述**: 用户重复参与活动
- **前置条件**: 用户已参与该活动
- **请求参数**: 同正常场景
- **预期结果**:
```json
{
  "code": "BIZ_ERROR",
  "message": "用户已参与活动",
  "success": false
}
```

---

### 接口3：活动状态查询（entryPage）

#### 功能测试

##### 1. 正常场景测试 - 已参与用户
- **用例描述**: 查询已参与活动用户的状态
- **请求参数**:
```json
{
  "customerNo": "C123456"
}
```
- **预期结果**:
```json
{
  "code": "000000",
  "value": {
    "employeeFlag": false,
    "employeeRelativesFlag": false,
    "joinFlag": true,
    "currentLevel": 1,
    "currentTeamCount": 50,
    "rewardNum": 7
  },
  "success": true
}
```

##### 2. 正常场景测试 - 未参与用户
- **用例描述**: 查询未参与活动用户的状态
- **请求参数**: 同上
- **预期结果**:
```json
{
  "code": "000000",
  "value": {
    "employeeFlag": false,
    "employeeRelativesFlag": false,
    "joinFlag": false,
    "currentLevel": 0,
    "currentTeamCount": 0,
    "rewardNum": 0
  },
  "success": true
}
```

#### 异常测试

##### 1. 参数校验测试 - customerNo为空
- **用例描述**: 必填参数缺失
- **请求参数**:
```json
{
  "customerNo": ""
}
```
- **预期结果**:
```json
{
  "code": "400",
  "message": "参数错误：customerNo不能为空",
  "success": false
}
```

---

### 接口4：活动首页信息查询（homePage）

#### 功能测试

##### 1. 正常场景测试 - 完整信息返回
- **用例描述**: 查询用户活动首页完整信息
- **请求参数**:
```json
{
  "customerNo": "C123456"
}
```
- **预期结果**: 返回包含用户状态、邀请信息、权益列表的完整数据

#### 异常测试

##### 1. 参数校验测试 - customerNo无效
- **用例描述**: 使用不存在的customerNo
- **预期结果**: 返回错误提示

---

### 接口5：邀请记录查询（queryInviteRecord）

#### 功能测试

##### 1. 正常场景测试 - 首页查询
- **用例描述**: 第一页邀请记录查询
- **请求参数**:
```json
{
  "pageSize": 10
}
```
- **预期结果**: 返回最多10条邀请记录

##### 2. 正常场景测试 - 分页查询
- **用例描述**: 使用nextKey进行分页查询
- **请求参数**:
```json
{
  "startKey": "KEY_FROM_PREVIOUS_PAGE",
  "pageSize": 10
}
```
- **预期结果**: 返回下一页的邀请记录

#### 异常测试

##### 1. 边界值测试 - pageSize为0
- **用例描述**: pageSize为无效值
- **请求参数**:
```json
{
  "pageSize": 0
}
```
- **预期结果**: 返回参数错误

---

### 接口6：退出活动（quitActivity）

#### 功能测试

##### 1. 正常场景测试 - 普通退出
- **用例描述**: 用户主动退出活动
- **前置条件**: 用户已参与活动
- **请求参数**:
```json
{
  "customerNo": "C123456"
}
```
- **预期结果**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "value": null,
  "success": true
}
```

##### 2. 正常场景测试 - 退出导致团队降级
- **用例描述**: 用户退出导致团队人数不足，触发降级提醒
- **前置条件**: 团队当前20人（Lv.1），退出后19人
- **预期结果**: 退出成功，异步发送降级提醒

#### 异常测试

##### 1. 业务规则测试 - 用户未参与活动
- **用例描述**: 未参与活动的用户尝试退出
- **请求参数**: 同上
- **预期结果**:
```json
{
  "code": "BIZ_ERROR",
  "message": "用户未参与活动",
  "success": false
}
```

---

### 接口7：福利详情权益列表查询（queryInterest）

#### 功能测试

##### 1. 正常场景测试 - 权益列表查询
- **用例描述**: 查询用户的权益详情列表
- **请求参数**:
```json
{
  "customerNo": "C123456"
}
```
- **预期结果**: 返回当前等级的权益列表，包括不同等级的权益配置

---

### 接口8：用户升级/降级接口（updategrade）

#### 功能测试

##### 1. 正常场景测试 - 用户升级
- **用例描述**: 团队达到升级条件，用户等级提升
- **请求参数**:
```json
{
  "serialNo": "SN123456",
  "memberType": "4",
  "userId": 123456789,
  "teamLevel": "T1",
  "operationType": "1",
  "businessId": "TEAM_001",
  "teamLevelChange": true,
  "eventTime": "2025-07-29 18:32:05"
}
```
- **预期结果**:
```json
{
  "code": "000000",
  "status": "SUCCESS",
  "success": true
}
```
- **验证点**:
  - 用户等级更新为T1
  - 立即发放新等级权益
  - 如果是团队升级，需异步处理其他团员

##### 2. 正常场景测试 - 用户退出
- **用例描述**: 用户退出团队
- **请求参数**:
```json
{
  "serialNo": "SN123457",
  "memberType": "4",
  "userId": 123456789,
  "teamLevel": "T1",
  "operationType": "2",
  "businessId": "TEAM_001",
  "teamLevelChange": false,
  "eventTime": "2025-07-29 18:32:05"
}
```
- **预期结果**: 退出成功，权益到当月底

#### 异常测试

##### 1. 幂等性测试 - 重复请求
- **用例描述**: 使用相同serialNo重复请求
- **请求参数**: 与正常场景相同的serialNo
- **预期结果**: 第二次请求返回成功，但不重复处理业务逻辑

##### 2. 参数校验测试 - serialNo为空
- **用例描述**: 必填参数缺失
- **预期结果**: 返回参数错误

---

### 接口9：查询用户权益信息（interest/list）

#### 功能测试

##### 1. 正常场景测试 - 权益列表查询
- **用例描述**: 查询用户已获得的权益
- **请求参数**:
```json
{
  "userId": 123456789,
  "customerNo": "C123456",
  "productType": "ZAZone"
}
```
- **预期结果**: 返回用户的权益列表

#### 异常测试

##### 1. 参数校验测试 - productType错误
- **用例描述**: 使用错误的产品类型
- **请求参数**:
```json
{
  "userId": 123456789,
  "productType": "INVALID_TYPE"
}
```
- **预期结果**: 返回参数错误或空列表

---

## 二、场景测试用例

### 场景1：新用户完整加入流程（获取验证码 → 企业认证 → 查询状态 → 查看权益）

**场景描述**: 测试新用户从获取验证码到完成认证并查看权益的完整流程

**涉及接口**:
1. 接口1: getVerifyCode - 获取验证码
2. 接口2: verify - 企业认证
3. 接口3: entryPage - 活动状态查询
4. 接口4: homePage - 活动首页信息查询

**接口调用关系图**:
```
getVerifyCode（获取验证码） → verify（企业认证） → entryPage（查询状态） → homePage（查看权益）
        ↓                            ↓                      ↓                       ↓
    返回tokenId                使用tokenId              验证joinFlag=true      返回权益列表
```

#### 测试用例1：正向流程 - 新用户加入成功

- **用例描述**: 测试新用户从获取验证码到查看权益的完整流程
- **前置条件**:
  - 用户未参与活动
  - 邀请码有效
  - 团队当前人数19人（即将达到20人升级阈值）

- **测试步骤**:

  **步骤1**: 调用getVerifyCode获取验证码
  - 请求参数:
  ```json
  {
    "revIdType": "EMAIL",
    "revId": "newuser@company.com",
    "redeemCode": "ABC123"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "status": "SUCCESS",
    "value": {
      "tokenId": "TOKEN_NEW_USER_001"
    },
    "success": true
  }
  ```

  **步骤2**: 使用步骤1返回的tokenId，调用verify进行企业认证
  - 请求参数:
  ```json
  {
    "customerNo": "C_NEW_001",
    "tokenId": "{{步骤1返回的tokenId}}",
    "revIdType": "EMAIL",
    "revId": "newuser@company.com",
    "verifyCode": "123456",
    "redeemCode": "ABC123"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "status": "SUCCESS",
    "value": {
      "revId": "newuser@company.com",
      "currentLevel": 1,
      "currentTeamCount": 20,
      "levelChange": true,
      "advCodeUseSuccessFlag": true
    },
    "success": true
  }
  ```

  **步骤3**: 调用entryPage查询活动状态
  - 请求参数:
  ```json
  {
    "customerNo": "C_NEW_001"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "joinFlag": true,
      "currentLevel": 1,
      "currentTeamCount": 20,
      "rewardNum": 7
    },
    "success": true
  }
  ```

  **步骤4**: 调用homePage查询完整信息和权益
  - 请求参数:
  ```json
  {
    "customerNo": "C_NEW_001"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "joinFlag": true,
      "currentLevel": 1,
      "inviteSuccessCount": 0,
      "levelsConfig": [{
        "level": 1,
        "peopleNum": 20,
        "rewards": [...]
      }]
    },
    "success": true
  }
  ```

- **验证点**:
  - ✓ 每个步骤返回的状态码正确
  - ✓ tokenId在步骤1和步骤2之间正确传递
  - ✓ 认证成功后joinFlag从false变为true
  - ✓ 团队人数从19增加到20
  - ✓ 团队等级从0升级到1（currentLevel从0变为1）
  - ✓ levelChange=true表示触发了升级
  - ✓ 权益数量rewardNum正确（7个权益）
  - ✓ 最终查询结果与预期一致

---

#### 测试用例2：异常流程 - 验证码错误

- **用例描述**: 测试验证码错误时的处理
- **测试步骤**:
  1. 调用getVerifyCode获取验证码（同步骤1）
  2. 调用verify时输入错误的验证码
     - 请求参数:
     ```json
     {
       "customerNo": "C_NEW_001",
       "tokenId": "{{步骤1返回的tokenId}}",
       "revIdType": "EMAIL",
       "revId": "newuser@company.com",
       "verifyCode": "000000",
       "redeemCode": "ABC123"
     }
     ```
     - 预期结果: 返回错误，提示验证码错误
     ```json
     {
       "code": "VERIFY_ERROR",
       "message": "验证码错误",
       "success": false
     }
     ```
  3. 调用entryPage查询状态
     - 预期结果: joinFlag仍为false，用户未成功参与

- **验证点**:
  - ✓ 验证失败后用户状态未改变
  - ✓ 团队人数未增加
  - ✓ 错误信息明确提示验证码错误

---

#### 测试用例3：边界场景 - tokenId过期

- **用例描述**: 测试tokenId超时后的处理
- **测试步骤**:
  1. 调用getVerifyCode获取验证码
  2. 等待tokenId过期（假设5分钟超时）
  3. 使用过期的tokenId调用verify
     - 预期结果: 返回tokenId无效或已过期错误
     ```json
     {
       "code": "AUTH_ERROR",
       "message": "tokenId无效或已过期",
       "success": false
     }
     ```
  4. 重新调用getVerifyCode获取新的tokenId
  5. 使用新的tokenId完成认证

- **验证点**:
  - ✓ 过期tokenId无法通过认证
  - ✓ 重新获取tokenId后可以正常认证
  - ✓ 错误提示清晰

---

### 场景2：用户邀请与团队升级流程（企业认证 → 团队升级 → 权益发放）

**场景描述**: 测试用户加入后触发团队升级，RCS模块处理权益发放的完整流程

**涉及接口**:
1. 接口2: verify - 企业认证
2. 接口8: updategrade - 用户升级接口（RCS）
3. 接口9: interest/list - 查询用户权益信息（RCS）
4. 接口4: homePage - 活动首页信息查询

**接口调用关系图**:
```
verify（企业认证） → updategrade（权益升级） → interest/list（查询权益） → homePage（验证权益展示）
      ↓                      ↓                        ↓                          ↓
 levelChange=true      发放新等级权益           返回权益列表              权益正确展示
 触发升级流程          (RCS模块处理)
```

#### 测试用例1：正向流程 - 团队升级触发权益发放

- **用例描述**: 测试团队达到升级阈值后，所有团员权益正确发放
- **前置条件**:
  - 团队当前99人（Lv.1），即将升级到Lv.2（100人）
  - 已有用户A、B、C在团队中

- **测试步骤**:

  **步骤1**: 新用户D完成企业认证，触发团队升级
  - 请求参数:
  ```json
  {
    "customerNo": "C_USER_D",
    "tokenId": "TOKEN_D",
    "revIdType": "EMAIL",
    "revId": "userd@company.com",
    "verifyCode": "123456",
    "redeemCode": "ABC123"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "currentLevel": 2,
      "currentTeamCount": 100,
      "levelChange": true
    },
    "success": true
  }
  ```

  **步骤2**: RCS模块调用updategrade处理用户D的权益升级（同步）
  - 请求参数:
  ```json
  {
    "serialNo": "SN_UPGRADE_D_001",
    "memberType": "4",
    "userId": 123456789,
    "teamLevel": "T2",
    "operationType": "1",
    "businessId": "TEAM_001",
    "teamLevelChange": true,
    "eventTime": "2025-07-29 18:32:05"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "status": "SUCCESS",
    "success": true
  }
  ```

  **步骤3**: RCS模块异步调用updategrade处理其他团员（A、B、C）的权益升级
  - 请求参数（用户A）:
  ```json
  {
    "serialNo": "SN_UPGRADE_A_001",
    "memberType": "4",
    "userId": 123456788,
    "teamLevel": "T2",
    "operationType": "1",
    "businessId": "TEAM_001",
    "teamLevelChange": true,
    "eventTime": "2025-07-29 18:32:05"
  }
  ```
  - 预期响应: 成功

  **步骤4**: 调用interest/list查询用户D的权益
  - 请求参数:
  ```json
  {
    "userId": 123456789,
    "productType": "ZAZone"
  }
  ```
  - 预期响应:
  ```json
  {
    "interestList": [{
      "interestName": "Lv.2专属权益1",
      "interestType": "27",
      "interestSendState": "1"
    }, {
      "interestName": "Lv.2专属权益2",
      "interestType": "28",
      "interestSendState": "1"
    }]
  }
  ```

  **步骤5**: 调用homePage验证用户D的首页展示
  - 请求参数:
  ```json
  {
    "customerNo": "C_USER_D"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "currentLevel": 2,
      "currentTeamCount": 100,
      "levelsConfig": [{
        "level": 2,
        "peopleNum": 100,
        "rewards": [...]
      }]
    },
    "success": true
  }
  ```

- **验证点**:
  - ✓ 认证成功后levelChange=true表示触发了升级
  - ✓ 团队等级从1升级到2
  - ✓ 团队人数从99增加到100
  - ✓ RCS模块正确处理用户D的权益升级（同步）
  - ✓ RCS模块正确处理其他团员的权益升级（异步）
  - ✓ 用户D的权益列表包含Lv.2的专属权益
  - ✓ 权益发放状态为"正常发放"（interestSendState="1"）
  - ✓ 首页展示的等级和权益正确

---

#### 测试用例2：异常流程 - 幂等性验证

- **用例描述**: 测试权益发放的幂等性，同一用户同一等级同一月份仅发放一次
- **测试步骤**:
  1. 用户完成认证，触发权益发放（同场景1步骤1-2）
  2. 使用相同的serialNo再次调用updategrade
     - 请求参数:
     ```json
     {
       "serialNo": "SN_UPGRADE_D_001",
       "memberType": "4",
       "userId": 123456789,
       "teamLevel": "T2",
       "operationType": "1",
       "businessId": "TEAM_001",
       "teamLevelChange": true,
       "eventTime": "2025-07-29 18:32:05"
     }
     ```
     - 预期响应: 返回成功，但不重复发放权益
     ```json
     {
       "code": "000000",
       "status": "SUCCESS",
       "success": true
     }
     ```
  3. 查询用户权益列表
     - 预期结果: 权益数量与第一次发放相同，未重复发放

- **验证点**:
  - ✓ 相同serialNo的请求不会重复处理
  - ✓ 权益未重复发放
  - ✓ 返回成功状态，保证接口幂等性

---

#### 测试用例3：边界场景 - 升级时权益替换

- **用例描述**: 测试用户升级时，需要替换的权益（如加息券）正确处理
- **前置条件**:
  - 用户当前Lv.1，已有加息券A（1.0%利率）
  - 升级到Lv.2后，加息券应替换为加息券B（1.5%利率）

- **测试步骤**:
  1. 查询用户当前权益（Lv.1）
     - 预期结果: 包含加息券A（1.0%）
  2. 触发团队升级到Lv.2
  3. RCS模块处理权益升级
     - 预期结果: 回收加息券A，发放加息券B
  4. 查询用户升级后的权益
     - 预期结果:
       - 不再包含加息券A
       - 包含加息券B（1.5%）
       - 其他权益累加（不替换）

- **验证点**:
  - ✓ 升级时需要替换的权益正确回收
  - ✓ 新等级的权益正确发放
  - ✓ 不需要替换的权益保持不变
  - ✓ 权益替换是原子性操作

---

### 场景3：用户退出与团队降级流程（退出活动 → 团队降级 → 通知发送）

**场景描述**: 测试用户退出导致团队降级或解散的完整流程

**涉及接口**:
1. 接口6: quitActivity - 退出活动
2. 接口8: updategrade - 用户降级接口（RCS）
3. 接口3: entryPage - 活动状态查询

**接口调用关系图**:
```
quitActivity（退出活动） → updategrade（处理降级） → entryPage（验证状态）
       ↓                          ↓                        ↓
  返回成功                   更新团员等级            团队等级已降低
  触发降级检查               次月生效新等级
```

#### 测试用例1：正向流程 - 用户退出导致团队降级

- **用例描述**: 测试用户退出后，团队人数不足，触发降级提醒和处理
- **前置条件**:
  - 团队当前20人（Lv.1的最低人数）
  - 用户E准备退出

- **测试步骤**:

  **步骤1**: 用户E调用quitActivity退出活动
  - 请求参数:
  ```json
  {
    "customerNo": "C_USER_E"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "status": "SUCCESS",
    "value": null,
    "success": true
  }
  ```

  **步骤2**: 系统检测到团队人数不足（19人 < 20人），异步发送降级提醒
  - 验证点:
    - 全员收到push通知："团队人数不足，下月将降级"
    - 全员收到email通知

  **步骤3**: RCS模块调用updategrade更新用户E的状态
  - 请求参数:
  ```json
  {
    "serialNo": "SN_QUIT_E_001",
    "memberType": "4",
    "userId": 123456790,
    "teamLevel": "T1",
    "operationType": "2",
    "businessId": "TEAM_001",
    "teamLevelChange": false,
    "eventTime": "2025-07-29 18:32:05"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "status": "SUCCESS",
    "success": true
  }
  ```

  **步骤4**: 次月1日0点，系统执行降级任务
  - RCS模块批量调用updategrade更新所有团员等级
  - 请求参数（示例）:
  ```json
  {
    "serialNo": "SN_DOWNGRADE_A_001",
    "memberType": "4",
    "userId": 123456788,
    "teamLevel": "T0",
    "operationType": "1",
    "businessId": "TEAM_001",
    "teamLevelChange": true,
    "eventTime": "2025-08-01 00:00:00"
  }
  ```
  - 全员收到降级通知（activity + email）

  **步骤5**: 调用entryPage查询其他团员的状态
  - 请求参数:
  ```json
  {
    "customerNo": "C_USER_A"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "joinFlag": true,
      "currentLevel": 0,
      "currentTeamCount": 19,
      "rewardNum": 0
    },
    "success": true
  }
  ```

- **验证点**:
  - ✓ 用户E退出成功
  - ✓ 系统正确检测到人数不足（19 < 20）
  - ✓ 当月首次触发时发送降级提醒（push + email）
  - ✓ 次月1日0点执行降级任务
  - ✓ 所有团员等级从1降到0
  - ✓ 团员权益到当月底失效
  - ✓ 次月不再发放Lv.1的权益
  - ✓ 所有团员收到降级通知

---

#### 测试用例2：异常流程 - 用户未参与活动尝试退出

- **用例描述**: 测试未参与活动的用户尝试退出
- **测试步骤**:
  1. 调用quitActivity
     - 请求参数:
     ```json
     {
       "customerNo": "C_NOT_JOINED"
     }
     ```
     - 预期结果: 返回错误
     ```json
     {
       "code": "BIZ_ERROR",
       "message": "用户未参与活动",
       "success": false
     }
     ```

- **验证点**:
  - ✓ 未参与用户无法退出
  - ✓ 错误信息明确

---

#### 测试用例3：边界场景 - 月底倒数第2天提醒

- **用例描述**: 测试月底倒数第2天10:00的降级提醒
- **前置条件**:
  - 团队人数不足（19人 < 20人）
  - 当前日期为当月倒数第2天

- **测试步骤**:
  1. 定时任务在10:00执行
  2. 系统检测团队人数不足
  3. 发送push和email提醒全员
     - 内容："团队人数不足，次月将降级，请尽快邀请同事加入"

- **验证点**:
  - ✓ 定时任务在正确时间执行
  - ✓ 所有团员收到提醒
  - ✓ 提醒内容清晰明确

---

### 场景4：邀请记录查询流程（邀请用户 → 查询邀请记录 → 分页展示）

**场景描述**: 测试用户邀请后，查询邀请记录的分页展示

**涉及接口**:
1. 接口2: verify - 企业认证（被邀请人）
2. 接口5: queryInviteRecord - 邀请记录查询（邀请人）
3. 接口4: homePage - 活动首页信息查询（邀请人）

**接口调用关系图**:
```
verify（被邀请人认证） → homePage（查看邀请数） → queryInviteRecord（查询邀请记录）
         ↓                      ↓                          ↓
   使用邀请人的redeemCode    inviteSuccessCount增加     返回邀请记录列表
```

#### 测试用例1：正向流程 - 邀请记录正确展示

- **用例描述**: 测试用户邀请他人后，邀请记录正确展示
- **前置条件**:
  - 用户F已参与活动，redeemCode为"F_CODE_123"
  - 用户F邀请了3位同事（G、H、I）

- **测试步骤**:

  **步骤1**: 用户G使用用户F的邀请码完成认证
  - 请求参数:
  ```json
  {
    "customerNo": "C_USER_G",
    "tokenId": "TOKEN_G",
    "revIdType": "EMAIL",
    "revId": "userg@company.com",
    "verifyCode": "123456",
    "redeemCode": "F_CODE_123"
  }
  ```
  - 预期响应:认证成功

  **步骤2**: 用户F调用homePage查看邀请数
  - 请求参数:
  ```json
  {
    "customerNo": "C_USER_F"
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "inviteSuccessCount": 1,
      "redeemCode": "F_CODE_123"
    },
    "success": true
  }
  ```

  **步骤3**: 用户H、I依次使用用户F的邀请码完成认证
  - 完成后inviteSuccessCount变为3

  **步骤4**: 用户F调用queryInviteRecord查询邀请记录（第一页）
  - 请求参数:
  ```json
  {
    "pageSize": 2
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "details": [{
        "nickName": "用户I昵称",
        "inviteTime": 1234567893
      }, {
        "nickName": "用户H昵称",
        "inviteTime": 1234567892
      }],
      "pageInfo": {
        "nextKey": "KEY_PAGE_2"
      }
    },
    "success": true
  }
  ```

  **步骤5**: 用户F使用nextKey查询第二页
  - 请求参数:
  ```json
  {
    "startKey": "{{步骤4返回的nextKey}}",
    "pageSize": 2
  }
  ```
  - 预期响应:
  ```json
  {
    "code": "000000",
    "value": {
      "details": [{
        "nickName": "用户G昵称",
        "inviteTime": 1234567891
      }],
      "pageInfo": {
        "nextKey": null
      }
    },
    "success": true
  }
  ```

- **验证点**:
  - ✓ 被邀请人使用邀请码后，邀请人的inviteSuccessCount正确增加
  - ✓ 邀请记录按时间倒序排列（最新的在前）
  - ✓ 分页功能正常，每页返回指定数量的记录
  - ✓ nextKey正确返回，用于下一页查询
  - ✓ 最后一页nextKey为null，表示查询完毕
  - ✓ 邀请记录包含昵称和邀请时间

---

#### 测试用例2：边界场景 - 无邀请记录

- **用例描述**: 测试用户没有邀请任何人时的查询
- **测试步骤**:
  1. 新用户J完成认证（未邀请他人）
  2. 调用queryInviteRecord查询邀请记录
     - 请求参数:
     ```json
     {
       "pageSize": 10
     }
     ```
     - 预期响应:
     ```json
     {
       "code": "000000",
       "value": {
         "details": [],
         "pageInfo": {
           "nextKey": null
         }
       },
       "success": true
     }
     ```

- **验证点**:
  - ✓ 返回空列表，不报错
  - ✓ nextKey为null

---

### 场景5：跨月权益发放流程（月底预发 → 次月生效 → 等级变化处理）

**场景描述**: 测试月底预发权益、次月生效以及跨月期间等级变化的处理流程

**涉及接口**:
1. 接口8: updategrade - 用户升级接口（RCS）
2. 接口9: interest/list - 查询用户权益信息（RCS）

**接口调用关系图**:
```
月底预发权益 → 等级变化（升级/降级） → 回收预发权益 → 重新发放新等级权益 → 次月1日生效
     ↓                 ↓                    ↓                  ↓                    ↓
  预发下月权益      检测等级变化          取消预发计划        发放新等级权益      权益生效
  (状态：预发待生效)
```

#### 测试用例1：正向流程 - 月底预发权益次月生效

- **用例描述**: 测试月底预发权益，次月1日自动生效
- **前置条件**:
  - 当前日期为7月31日
  - 用户K当前等级为Lv.1

- **测试步骤**:

  **步骤1**: 7月31日0点，系统执行预发任务
  - RCS模块批量生成8月份的发放计划
  - 权益状态：预发待生效（send_status="6"）
  - benefit_type=2（预发权益）

  **步骤2**: 7月31日，查询用户K的权益
  - 请求参数:
  ```json
  {
    "userId": 123456791,
    "productType": "ZAZone"
  }
  ```
  - 预期响应:
  ```json
  {
    "interestList": [{
      "interestName": "Lv.1权益1",
      "interestSendState": "1"
    }, {
      "interestName": "Lv.1权益2",
      "interestSendState": "1"
    }]
  }
  ```
  - 验证点: 当月权益正常展示，预发权益不展示

  **步骤3**: 8月1日0点，系统执行权益生效任务
  - 将预发权益状态从"预发待生效"改为"正常发放"
  - send_status从"6"改为"1"

  **步骤4**: 8月1日，查询用户K的权益
  - 请求参数: 同步骤2
  - 预期响应:
  ```json
  {
    "interestList": [{
      "interestName": "Lv.1权益1",
      "interestSendState": "1"
    }, {
      "interestName": "Lv.1权益2",
      "interestSendState": "1"
    }]
  }
  ```
  - 验证点: 8月份的权益正常展示

- **验证点**:
  - ✓ 7月31日预发计划正确生成
  - ✓ 预发权益状态为"预发待生效"
  - ✓ 7月31日查询时不展示预发权益
  - ✓ 8月1日0点权益状态正确变更
  - ✓ 8月1日查询时权益正常展示

---

#### 测试用例2：异常流程 - 预发后等级变化（升级）

- **用例描述**: 测试预发权益后，月底前用户升级，系统回收预发权益并重新发放
- **前置条件**:
  - 7月31日已预发Lv.1的8月份权益
  - 7月31日下午，团队升级到Lv.2

- **测试步骤**:

  **步骤1**: 7月31日14:00，团队达到100人，升级到Lv.2
  - RCS模块调用updategrade
  - 请求参数:
  ```json
  {
    "serialNo": "SN_UPGRADE_K_001",
    "memberType": "4",
    "userId": 123456791,
    "teamLevel": "T2",
    "operationType": "1",
    "businessId": "TEAM_001",
    "teamLevelChange": true,
    "eventTime": "2025-07-31 14:00:00"
  }
  ```

  **步骤2**: RCS模块检测到预发权益存在，执行回收
  - 将预发的Lv.1权益状态改为"已取消"（send_status="4"）

  **步骤3**: RCS模块重新发放Lv.2的权益
  - 立即发放7月份剩余时间的Lv.2权益（当月生效）
  - 预发8月份的Lv.2权益（预发待生效）

  **步骤4**: 查询用户K的权益
  - 请求参数:
  ```json
  {
    "userId": 123456791,
    "productType": "ZAZone"
  }
  ```
  - 预期响应:
  ```json
  {
    "interestList": [{
      "interestName": "Lv.2权益1",
      "interestSendState": "1"
    }, {
      "interestName": "Lv.2权益2",
      "interestSendState": "1"
    }]
  }
  ```

  **步骤5**: 8月1日，查询用户K的权益
  - 预期响应: Lv.2的权益正常展示

- **验证点**:
  - ✓ 系统检测到升级后，正确回收预发的Lv.1权益
  - ✓ 立即发放当月剩余时间的Lv.2权益
  - ✓ 重新预发次月的Lv.2权益
  - ✓ 权益状态流转正确：预发待生效 → 已取消
  - ✓ 用户查询时展示正确等级的权益
  - ✓ 8月1日权益正常生效

---

#### 测试用例3：异常流程 - 预发后等级变化（降级）

- **用例描述**: 测试预发权益后，月底前团队降级，系统回收预发权益并重新发放
- **前置条件**:
  - 7月31日已预发Lv.2的8月份权益
  - 7月31日下午，用户退出导致团队降级到Lv.1

- **测试步骤**:
  1. 用户退出，触发降级（同场景3）
  2. RCS模块回收预发的Lv.2权益
  3. RCS模块重新预发Lv.1的权益
  4. 次月1日，Lv.1权益生效

- **验证点**:
  - ✓ 降级时正确回收高等级的预发权益
  - ✓ 重新预发低等级的权益
  - ✓ 次月生效的是降级后的权益

---

## 三、场景用例优先级建议

| 优先级 | 场景类型 | 场景名称 | 理由 |
|-------|---------|---------|------|
| P0 | 核心业务流程 | 场景1：新用户完整加入流程 | 主流程，用户首次体验的关键路径，影响核心业务 |
| P0 | 核心业务流程 | 场景2：用户邀请与团队升级流程 | 核心业务逻辑，涉及权益发放，影响用户收益 |
| P1 | 异常恢复 | 场景3：用户退出与团队降级流程 | 异常处理，影响用户体验和权益 |
| P1 | 数据一致性 | 场景5：跨月权益发放流程 | 涉及定时任务和权益发放，数据一致性要求高 |
| P2 | 辅助功能 | 场景4：邀请记录查询流程 | 辅助功能，影响用户体验但非核心业务 |

---

## 四、测试注意事项

### 1. 接口路径注意事项
- ⚠️ **所有包含`dmb`的网关接口均需替换为微服务接口**
- 测试环境应直接调用微服务接口，不经过网关
- 微服务映射规则：
  - `/activity/*` → zabank_imc_activity_service
  - `/rc/*` → zabank_rcs_core

### 2. 数据依赖关系
- **tokenId**: getVerifyCode返回 → verify使用
- **redeemCode**: homePage返回 → 其他用户verify时使用
- **serialNo**: 幂等性保证，相同serialNo不重复处理
- **currentLevel**: 权益发放依据，需跨接口验证一致性

### 3. 时序依赖
- 场景1：必须先getVerifyCode，再verify
- 场景2：verify成功后，RCS模块异步处理，需要等待
- 场景5：月底预发 → 次月生效，需要跨天测试

### 4. 异步处理验证
- 团队升级时，触发用户同步处理，其他团员异步处理
- 退出活动时，降级提醒异步发送
- 定时任务（月底预发、次月生效）需要验证执行时间

### 5. 幂等性验证
- 所有RCS接口（updategrade）需验证幂等性
- 使用相同serialNo重复请求，不应重复处理业务逻辑

### 6. 状态流转验证
- 用户状态：未参与 → 已参与
- 团队等级：0（未成团） → 1（星云）→ 2（星球）
- 权益状态：预发待生效 → 正常发放 → 已核销 → 已过期
- 券状态：待生效 → 正常 → 锁定 → 已核销 → 过期

### 7. 通知验证
- activity通知：用户参与、退出、升级、降级
- push通知：降级提醒、退出成功
- email通知：降级提醒、退出成功、权益发放

### 8. 定时任务测试
- **每月1日0点**：降级/退团通知、权益生效
- **每月15日和28日10:00**：降级提醒
- **月底倒数第2天10:00**：降级提醒
- **月底最后一天0点**：预发次月权益

---

## 五、测试环境要求

### 1. 数据准备
- 至少准备3个测试团队（0人、19人、99人）
- 准备不同状态的用户（未参与、已参与、不同等级）
- 准备有效和无效的邀请码
- 准备测试邮箱（企业邮箱格式）

### 2. 时间控制
- 需要能够模拟跨月场景
- 需要能够触发定时任务
- 需要能够调整系统时间进行测试

### 3. 依赖服务
- RCS权益模块服务
- 活动服务
- 消息通知服务（push、email、activity）
- 定时任务调度服务

### 4. 监控验证
- 权益发放记录
- 用户等级变更日志
- 通知发送记录
- 定时任务执行日志

---

## 六、风险点分析

| 风险点 | 影响 | 建议测试重点 |
|-------|------|-------------|
| 网关接口与微服务接口差异 | 高 | 验证所有接口路径映射正确 |
| 跨服务数据一致性 | 高 | 重点测试activity服务和RCS服务的数据同步 |
| 异步处理延迟 | 中 | 验证异步任务的超时和重试机制 |
| 幂等性失效 | 高 | 重点测试serialNo的唯一性和幂等性 |
| 定时任务失败 | 高 | 验证定时任务的失败重试和告警机制 |
| 权益重复发放 | 高 | 验证"同一用户同一等级同一月份仅发放一次"的规则 |
| 跨月时等级变化处理 | 中 | 重点测试月底最后一天的等级变化场景 |
| 并发冲突 | 中 | 验证多用户同时加入团队的并发处理 |

---

## 七、总结

本测试左移分析报告基于企业福利（ZA Zone）开发方案文档，提供了：

1. **9个核心接口**的详细测试用例（单接口测试）
2. **5个业务场景**的端到端测试用例（场景测试）
3. **接口路径校验结果**，识别出需要替换的网关接口
4. **数据依赖关系分析**，明确接口间的数据传递
5. **优先级建议**，帮助测试团队合理安排测试资源

**关键测试重点**：
- ✅ 新用户加入的完整流程（场景1）
- ✅ 团队升级触发权益发放（场景2）
- ✅ 用户退出导致团队降级（场景3）
- ✅ 跨月权益发放处理（场景5）
- ✅ 幂等性验证（所有RCS接口）
- ✅ 异步处理验证（团队升级、降级通知）

通过本测试左移分析，可以在开发早期阶段介入，提前发现潜在问题，降低项目风险，提升测试效率和质量。
