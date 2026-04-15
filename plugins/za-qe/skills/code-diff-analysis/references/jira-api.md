# Jira OpenAPI 字段提取规范

## 基础请求

```bash
# 获取 Issue 详情（默认 Token 可直接使用）
curl -k \
  -H "Authorization: Bearer ${JIRA_TOKEN:-MTE4MDMxOTEyNjMwOogU+AFSs09tgxWWFhWCY8gjzP2b}" \
  -H "Accept: application/json" \
  "https://jira.in.za/rest/api/2/issue/BANK-89156"

# 获取 Development 信息（分支、PR、提交）
curl -k \
  -H "Authorization: Bearer ${JIRA_TOKEN:-MTE4MDMxOTEyNjMwOogU+AFSs09tgxWWFhWCY8gjzP2b}" \
  -H "Accept: application/json" \
  "https://jira.in.za/rest/dev-status/1.0/issue/detail?issueId=<ISSUE_ID>&applicationType=stash&dataType=branch"

# 同时获取 PR 信息
curl -k \
  -H "Authorization: Bearer ${JIRA_TOKEN:-MTE4MDMxOTEyNjMwOogU+AFSs09tgxWWFhWCY8gjzP2b}" \
  -H "Accept: application/json" \
  "https://jira.in.za/rest/dev-status/1.0/issue/detail?issueId=<ISSUE_ID>&applicationType=stash&dataType=pullrequest"
```

---

## Issue 详情字段说明

### 基础信息字段

| 字段路径 | 说明 | 示例值 |
|----------|------|--------|
| `fields.summary` | 需求标题 | "MA防骗安全教育小游戏推广" |
| `fields.issuetype.name` | 需求类型 | "Story" / "Bug" / "Task" / "Sub-task" |
| `fields.status.name` | 当前状态 | "In Development" / "In QA" / "Done" |
| `fields.fixVersions[].name` | 版本号 | "2024.05.01" |
| `fields.components[].name` | 服务组件 | ["activity-service", "push-service"] |
| `fields.assignee.displayName` | 经办人 | "张三" |
| `fields.description` | 需求描述（判断是否优化需求） | 富文本内容 |
| `id` | Issue 数字 ID（用于 dev-status API） | "123456" |

### 优化需求判断逻辑

满足以下任一条件即判断为**优化需求**：

1. `fields.issuetype.name` 包含：`优化`、`Optimization`、`Improvement`、`Refactor`
2. `fields.summary` 包含（不区分大小写）：`优化`、`重构`、`性能`、`improve`、`refactor`、`optimize`、`perf`
3. `fields.labels` 包含：`optimization`、`refactor`、`performance`
4. `fields.description` 明确描述"本次变更为性能优化/代码重构"

---

## 开发分支信息提取

**ZA Bank 首选策略：从评论中提取（最可靠）**

Jira 评论中 `Infra-DevOps` 机器人在 MR 创建时会自动关联，评论格式：
```
[高原|http://gitlab.in.za/yuan.gao] mentioned this issue in [a merge request|http://...] 
of [zabank / imc / zabank-imc-cubercore-service|http://...] 
on branch [BANK-89156_20260414_1632|http://...]:{quote}feat(BANK-89156):...{quote}
```

解析逻辑（Python）：
```python
import re, json

with open(jira_tmp_file, encoding='utf-8') as f:
    data = json.load(f)

comments = data['fields']['comment']['comments']
repo_branch_map = {}  # {service_name: branch_name}

for comment in comments:
    body = comment.get('body', '')
    # 提取仓库名（路径最后一段）
    repo_match = re.search(r'of \[.*?([a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+)\|', body)
    # 提取分支名
    branch_match = re.search(r'on branch \[([^\]|]+)', body)
    
    if repo_match and branch_match:
        repo_name = repo_match.group(1)   # 如：zabank-imc-cubercore-service
        branch_name = branch_match.group(1)  # 如：BANK-89156_20260414_1632
        repo_branch_map[repo_name] = branch_name

for repo, branch in repo_branch_map.items():
    print(f"服务: {repo}, 分支: {branch}")
```

### 方式 2：Dev Status API（备选）

Development 信息通过专用 API 获取：

```bash
curl -k \
  -H "Authorization: Bearer ${JIRA_TOKEN}" \
  -H "Accept: application/json" \
  "https://jira.in.za/rest/dev-status/1.0/issue/detail?issueId=${ISSUE_ID}&applicationType=stash&dataType=branch"
```

响应结构：
```json
{
  "detail": [
    {
      "branches": [
        {
          "name": "feature/BANK-89156-activity-game",
          "url": "https://gitlab.in.za/zabank/activity-service/tree/feature/BANK-89156-activity-game",
          "repository": {
            "name": "activity-service",
            "url": "https://gitlab.in.za/zabank/activity-service"
          },
          "lastCommit": {
            "id": "abc123def",
            "message": "feat: add game entry logic",
            "authorTimestamp": "2024-04-10T10:00:00.000+0800"
          }
        }
      ]
    }
  ]
}
```

**提取逻辑**：
- 遍历 `detail[].branches[]`
- 每个 branch 记录：`name`（分支名）、`repository.name`（服务名）、`repository.url`（仓库地址）

### 方式 2：从 customfield 提取

部分 Jira 配置将分支信息存入自定义字段：

```bash
# 获取所有 customfield（用于排查）
echo "$JIRA_RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for k, v in data['fields'].items():
    if v and 'branch' in str(v).lower():
        print(k, ':', str(v)[:200])
"
```

常见字段名：
- `customfield_10100`：Development Panel（需要额外 API 解析）
- `customfield_10104`：Git branch
- `customfield_13200`：开发分支（ZA Bank 内部字段）

### 方式 3：从评论中搜索

若以上方式无结果，搜索评论中的分支信息：

```python
import json, re

comments = data['fields']['comment']['comments']
branch_pattern = r'(feature|bugfix|hotfix|release)/[A-Z]+-\d+[-\w]*'

for comment in comments:
    body = comment.get('body', '')
    matches = re.findall(branch_pattern, body)
    if matches:
        print(f"在评论中找到分支: {matches}")
```

---

## 从分支 URL 推断仓库地址

ZA Bank 仓库命名规律：
```
https://gitlab.in.za/zabank/<service-name>
```

分支命名规律：
```
feature/BANK-XXXXX-<描述>
bugfix/BANK-XXXXX-<描述>
```

从分支 URL 提取仓库 clone 地址：
```bash
# SSH 方式
git@gitlab.in.za:zabank/<service-name>.git

# HTTPS 方式
https://gitlab.in.za/zabank/<service-name>.git
```

---

## 常见问题处理

### Issue 找不到
```json
{"errorMessages": ["Issue Does Not Exist"], "errors": {}}
```
→ 检查需求编号格式，确认 Token 有效且有对应项目权限

### Token 无效
```json
{"errorMessages": [], "errors": {}, "status": 401}
```
→ 提示用户重新生成 Jira Token（用户设置 → 安全 → API Token）

### 分支信息为空
`detail[].branches` 为空列表时，说明：
1. 开发尚未提交代码或未关联 Jira
2. Git 仓库未与 Jira 集成

→ 提示用户提供分支名或仓库路径，手动指定后继续分析
