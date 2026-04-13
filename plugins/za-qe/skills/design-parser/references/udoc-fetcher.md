# UDOC 接口文档抓取方案

本文档说明如何从 `udoc.in.za` 通过 OpenAPI 同步接口提取完整接口数据，供 design-parser 技能在规范化开发方案文档时使用。

---

## 抓取方式：OpenAPI sync 接口

**无需登录**，直接使用以下接口按微服务名 + 接口路径查询：

```
POST https://udoc.in.za/sync/doc?moduleName={微服务名}&url={接口路径（URL编码）}
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `moduleName` | 微服务名，连字符格式 | `zabank-mbs-statistics-service` |
| `url` | 接口路径，需 URL 编码 | `/static/statistic/inner0/user/identity/query` → `%2Fstatic%2Fstatistic%2Finner0%2Fuser%2Fidentity%2Fquery` |

**curl 示例**：
```bash
curl --ssl-revoke-best-effort --location --request POST \
  'https://udoc.in.za/sync/doc?moduleName=zabank-mbs-statistics-service&url=%2Fstatic%2Fstatistic%2Finner0%2Fuser%2Fidentity%2Fquery' \
  --max-time 15 \
  -o result/_tmp_udoc.json
```

---

## 抓取流程

### 第一步：从开发方案文档提取接口信息

扫描原文，收集每个接口的：
- **微服务名**（下划线格式，如 `zabank_mbs_statistics_service`）→ 转为连字符格式（`zabank-mbs-statistics-service`）
- **接口路径**（如 `/static/statistic/inner0/user/identity/query`）→ URL 编码

**微服务名格式转换规则**：下划线 `_` → 连字符 `-`，例如：
- `zabank_imc_cubercore_service` → `zabank-imc-cubercore-service`
- `zabank_mbs_statistics_service` → `zabank-mbs-statistics-service`

**若原文中仅有 UDOC 链接（`https://udoc.in.za/#/view/xxxxx`）而无微服务名**，则先用 docId 查询详情获取接口路径，再结合文档上下文判断所属微服务。

---

### 第二步：调用 sync 接口获取数据

对文档中每个接口执行一次请求，将结果保存为临时文件：

```bash
# URL 编码接口路径（Python 方式）
ENCODED_URL=$(python -c "import urllib.parse; print(urllib.parse.quote('/your/api/path'))")

curl --ssl-revoke-best-effort --location --request POST \
  "https://udoc.in.za/sync/doc?moduleName={微服务名}&url=${ENCODED_URL}" \
  --max-time 15 \
  -o result/_tmp_udoc_{接口标识}.json

echo "HTTP code: $?"
```

---

### 第三步：从响应中提取字段

响应结构：`data.data` 下包含完整接口信息。

```python
import json, re

with open('result/_tmp_udoc_{接口标识}.json', encoding='utf-8') as f:
    d = json.load(f)

api = d.get('data', {}).get('data', {})  # 注意是两层 data

name        = api.get('name', '')               # 接口名称
description = api.get('description', '')        # 功能描述
url         = api.get('url', '')                # 接口路径
method      = api.get('httpMethod', '')         # 请求方法
content_type = api.get('contentType', '')       # Content-Type

# 请求参数：GET 用 queryParams，POST 用 requestParams（若空则回退 queryParams）
req_params = api.get('queryParams', []) if method == 'GET' \
             else (api.get('requestParams', []) or api.get('queryParams', []))
res_params = api.get('responseParams', [])
```

**字段映射**：

| 目标字段 | UDOC 字段路径 | 说明 |
|---------|-------------|------|
| 接口名称 | `data.data.name` | — |
| 功能描述 | `data.data.description` | — |
| 接口路径 | `data.data.url` | — |
| 请求方法 | `data.data.httpMethod` | GET / POST / PUT / DELETE |
| Content-Type | `data.data.contentType` | 若为空则按方法推断：POST → `application/json`，GET → 无 |
| 请求参数 | `data.data.queryParams`（GET）/ `data.data.requestParams`（POST） | 含 name / type / required / description |
| 响应参数 | `data.data.responseParams` | 含 name / type / required / description，注意 children 嵌套 |

**参数字段说明**：

| 参数字段 | 说明 |
|---------|------|
| `name` | 参数名 |
| `type` | 数据类型（string / int64 / boolean / object / array / enum / map / file[] 等） |
| `required` | `1` 或 `true` 表示必填 |
| `description` | 参数说明（可能含 HTML 标签，需清理） |
| `children` | 子字段列表（object 类型时存在），递归处理 |

**嵌套结构处理**：若参数 `children` 非空，子字段名用 `└─` 标注，序号用 `父序号.子序号` 格式（如 `9.1`）。

---

### 第四步：写入规范化文档

将提取到的数据按以下格式回填到规范化 MD 文档中对应接口节点：

```markdown
##### 接口N：[name]

- **所属微服务**：`[微服务名，下划线格式，如 zabank_imc_cubercore_service]`
- **接口路径**：`[url]`
- **请求方法**：[httpMethod]
- **Content-Type**：[contentType]
- **UDOC**：[原始链接，若无则"—"]
- **功能描述**：[description]

**请求参数**

| 序号 | 参数名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| 1    | userId | int64 | 是 | 用户ID |

**响应参数**

| 序号 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| 1    | code   | string | 响应码 |
| 9    | value  | object | 数据DTO |
| 9.1  | └─ maGameId | string | MA游戏ID |
```

---

## 微服务名不确定时的处理

当原文只有 UDOC 链接（`#/view/xxxxx`），没有明确标注微服务名时：

1. 先根据文档上下文（接口路径前缀、模块名）推断微服务名
2. 尝试调用 sync 接口：若返回 `code: 0` 且数据非空，说明推断正确
3. 若返回空数据或报错，调整微服务名重试（常见服务名见下表）

**常见微服务名参考**：

| 路径前缀 | 微服务名 |
|---------|---------|
| `/static/statistic/` | `zabank-mbs-statistics-service` |
| `/cubercore/` | `zabank-imc-cubercore-service` |
| `/activity/` | `zabank-imc-activity-service` |

---

## 异常处理

| 异常情况 | 处理方式 |
|---------|---------|
| HTTP 非200 或 `code` 非 `"0"` | 标注 `> ⚠️ UDOC sync 接口请求失败（moduleName 或 url 可能不正确），接口信息需人工确认` |
| `data.data` 为 null 或空 | 标注 `> ⚠️ UDOC 未找到该接口（moduleName: xxx, url: xxx），请确认微服务名和路径` |
| 网络不通（curl 超时） | 标注 `> ⚠️ UDOC 服务不可达，接口信息需人工确认` |
| 部分字段为空 | 已提取的字段正常填入，缺失字段用 `—` 占位，标注 `> ℹ️ 以下字段从 UDOC 未获取到，已用原文内容填充` |

---

## 注意事项

1. **无需登录**，直接调用 sync 接口即可，无 token 要求
2. 每个接口单独请求，失败不影响其他接口
3. 抓取完成后删除临时文件 `result/_tmp_udoc_*.json`
4. `--ssl-revoke-best-effort` 参数用于跳过 SSL 证书吊销检查（内网自签证书环境）
