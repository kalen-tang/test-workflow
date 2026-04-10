# UDOC 接口文档抓取方案

本文档说明如何从 `udoc.in.za` 提取完整的接口数据，供 design-parser 技能在规范化开发方案文档时使用。

---

## UDOC 链接格式

```
https://udoc.in.za/#/view/{docId}
```

`docId` 即链接 `#/view/` 后面的字符串，例如 `2kqePaEX`。这是文档ID，需要通过详情接口再换取实际的 `spaceId` 才能查询接口数据。

---

## 抓取流程

### 第一步：登录获取 Token

UDOC 登录接口使用 RSA 加密密码，**密码密文固定**，直接使用以下 curl 命令登录并提取 token：
页面有多个接口，设计多个udoc链接的时候，只需要登录一次，拿到token就行了，其他接口可以共用一个token

```bash
TOKEN=$(curl -s -X POST 'https://udoc.in.za/system/login' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'authorization: Bearer' \
  -H 'content-type: application/json;charset=UTF-8' \
  -H 'origin: https://udoc.in.za' \
  -H 'referer: https://udoc.in.za/' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  --data-raw '{"username":"admin","password":"eMQEfDC0SC8qst/5Q0YCY1snO8K+Vvi1RKzAst0c43B/szl9E4D8edFnHm8ThCnseaJtc6gbq3abjNTN9ApJvgJNRhey7op17vWOf28IfBYzaS5XKI4kYH/jtl2WzNEm9waM8idR3EsJ73YRKyR5Duu+lyYeO0DXAAEuE8QvXwc=","source":"register"}' \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('token',''))")

echo "Token: $TOKEN"
```

Token 格式示例：`pqXbE8vD:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### 第二步：用 docId 查询文档详情，获取 spaceId

从 UDOC 链接中提取 `docId`（`#/view/` 后的部分），请求文档详情接口，从响应中取出 `spaceId`：

```bash
DOC_ID="{从链接提取的docId}"

SPACE_ID=$(curl -s "https://udoc.in.za/doc/view/detail?id=${DOC_ID}" \
  -H 'accept: application/json, text/plain, */*' \
  -H 'cache-control: no-cache' \
  -H 'pragma: no-cache' \
  -H "authorization: Bearer ${TOKEN}" \
  -H 'referer: https://udoc.in.za/' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('spaceId',''))")

echo "spaceId: $SPACE_ID"
```

---

### 第三步：用 spaceId 获取完整接口数据

```bash
curl -s "https://udoc.in.za/doc/view/data?spaceId=${SPACE_ID}" \
  -H 'accept: application/json, text/plain, */*' \
  -H 'cache-control: no-cache' \
  -H 'pragma: no-cache' \
  -H "authorization: Bearer ${TOKEN}" \
  -H 'referer: https://udoc.in.za/' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  > result/_tmp_udoc_${DOC_ID}.json
```

用 Read 工具读取 `result/_tmp_udoc_${DOC_ID}.json` 进行后续分析。

---

### 第四步：从响应中提取字段

对返回的 JSON 按以下映射提取数据：

| 目标字段 | UDOC 字段路径（常见） | 说明 |
|---------|---------------------|------|
| 接口所属微服务 | `serviceName` / `module` / URL 前缀 | 如 `zabank_imc_activity_service` |
| 接口路径 | `path` / `url` | 如 `/activity/list` |
| 请求方法 | `method` | GET / POST / PUT / DELETE |
| Content-Type | `contentType` / `reqBodyType` / `content_type` | 如 `application/json`、`application/x-www-form-urlencoded`；若未找到则按请求方法推断默认值（POST → `application/json`，GET → 无） |
| 功能描述 | `title` / `description` / `name` | 接口说明文字 |
| 请求参数 | `req_params` / `requestParams` / `params` | 含字段名、类型、是否必填、说明 |
| 响应参数 | `res_params` / `responseParams` / `response` | 含字段名、类型、说明，注意嵌套结构 |

**嵌套结构处理**：响应参数若有 `children` / `subParams` 嵌套字段，展开为多行，子字段名用 `└─` 标注。

---

### 第五步：写入规范化文档

将提取到的数据按以下格式回填到规范化 MD 文档中对应接口节点：

```markdown
##### 接口N：[功能描述]

- **所属微服务**：`[微服务名，如 zabank-imc-cubercore-service]`
- **接口路径**：`[接口路径，如 /cubercore/approval/add]`
- **请求方法**：[GET/POST/...]
- **Content-Type**：[application/json / application/x-www-form-urlencoded / ...]
- **UDOC**：[原始链接]
- **功能描述**：[从UDOC提取的description]

**请求参数**

| 序号 | 参数名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| 1    | xxx    | String | 是  | xxx  |

**响应参数**

| 序号 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 1    | code   | Integer | 响应码 |
| 2    | data   | Object  | 响应数据 |
| 2.1  | └─ id  | Long    | 记录ID |
```

---

## 异常处理

| 异常情况 | 处理方式 |
|---------|---------|
| 登录接口返回错误（非200或token为空） | 在接口下方标注 `> ⚠️ UDOC 登录失败，请联系管理员确认账号权限` |
| Token 有效但文档详情接口返回空数据 | 说明 docId 已失效，标注 `> ⚠️ UDOC 文档不存在或已删除（docId：xxx）` |
| 网络不通（curl 超时/连接拒绝） | 标注 `> ⚠️ UDOC 服务不可达，接口信息需人工确认` |
| 返回数据字段不完整（部分为空） | 已提取的字段正常填入，缺失字段用 `—` 占位，并标注 `> ℹ️ 以下字段从 UDOC 未获取到，已用原文内容填充` |

---

## 注意事项

1. 每个 UDOC 链接独立处理，抓取失败不影响其他链接的处理
2. 抓取完成后删除临时文件 `result/_tmp_udoc_*.json`
3. 同一文档中多个接口若指向同一 docId，只需抓取一次，复用结果
