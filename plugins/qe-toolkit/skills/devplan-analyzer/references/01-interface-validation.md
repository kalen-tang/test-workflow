# 接口路径校验与微服务映射规则

## 接口路径校验规则

提取接口路径后，必须进行以下校验。

### 1. 网关接口检测

**检测规则**：
- 如果接口路径中包含 `dmb`，则判定为网关接口
- **必须提示用户**：检测到网关接口，测试左移需要使用微服务接口，请替换为对应的微服务接口路径
- 停止该接口的后续分析，等待用户提供微服务接口

**示例**：
```
检测到的路径: /dmb/api/activity/list
提示: 检测到网关接口，测试左移需要使用微服务接口，请提供对应的微服务接口路径
```

### 2. 微服务识别

如果路径中不包含 `dmb`，则根据路径前缀自动识别所属微服务。

**微服务映射规则**：

| 路径前缀 | 微服务名称 | 服务说明 |
|---------|-----------|---------|
| /activity/* | zabank_imc_activity_service | 活动服务 |
| /rc/* | zabank_rcs_core | RCS权益服务 |
| /cuber/* | zabank_imc_cubercore_service | Cuber核心服务 |
| /reward/* | zabank_imc_reward_service | 奖励服务 |
| /act/* | zabank_act_core_service | ACT核心服务 |
| /batch/* | zabank_bms_batch_service | 批处理服务 |

### 3. 完整路径格式

**标准格式**：
```
微服务域名 + 接口路径
```

**示例**：
```
zabank_imc_activity_service/activity/list
zabank_rcs_core/rc/points/query
zabank_imc_reward_service/reward/claim
```

**路径补全规则**：
- 如果文档中只提供了接口路径（如 `/activity/list`）
- 需要根据上述映射规则补充微服务域名
- 完整路径：`zabank_imc_activity_service/activity/list`

## 接口信息提取来源

### 来源 1：直接提取

如果开发文档直接列出了接口定义，则直接提取接口信息。

### 来源 2：从 UDoc 链接提取

如果开发文档中只附上了接口链接（域名为 `udoc.in.za`）：

1. 使用 Playwright 从链接中提取网页内容
2. 登录信息：
   - 账号：`admin`
   - 密码：`Za123456`
3. 提取完整的接口定义（包括入参、出参）

**注意**：确保入参、出参和接口对应正确。

## 基础接口信息提取清单

提取以下接口信息：

- **接口名称**：API 接口的业务名称
- **接口路径**：RESTful API 的 URL 路径（需包含微服务域名+接口路径）
- **请求方法**：HTTP 方法（GET、POST、PUT、DELETE等）
- **功能描述**：接口实现的业务功能

## 详细参数信息提取清单

### 请求参数

- 路径参数（Path Parameters）
- 查询参数（Query Parameters）
- 请求头参数（Headers）
- 请求体参数（Request Body）
- 参数类型、是否必填、默认值、取值范围

### 响应参数

- 响应状态码
- 响应头信息
- 响应体结构
- 数据类型和字段说明
- 错误响应格式

## Playwright MCP 安装

如果当前用户没有安装 Playwright 的 MCP：

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

如果用户提供了网页链接但需要登录，提示用户提供用户名密码。
