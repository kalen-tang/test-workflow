---
name: code-diff-analysis
description: 此技能用于分析需求的代码变更，识别潜在的质量风险，输出变更内容及可执行的测试策略。当用户说"分析代码变更"、"分析代码diff"、"分析代码差异"、"分析需求的PR"、"分析BANK-XXXXX的代码变更"、"查看代码变更风险"、"帮我分析这个需求的代码改动"时应触发。
status: active
allowed-tools: Read Write Glob Grep Bash(curl *) Bash(git *) Bash(python *) Bash(ls *) Bash(mkdir *)
---

# 代码变更分析器

## 技能目标

通过 Jira OpenAPI 获取需求的开发提交信息，使用 `git diff` 比较各服务分支与 master 的代码差异，识别潜在质量风险，输出结构化的变更分析报告和可执行的测试策略。

**产出物**：
1. **代码变更分析报告**：变更概览、各服务变更详情、业务流程 & 数据库信息、质量风险汇总
2. **测试策略文档**：按 P0/P1/P2 优先级排列的可执行测试用例

---

## 阶段 0：启动信息收集（最优先执行）

前两项均已知才能继续，第三项为可选：

**收集项 1 - 需求编号**：若用户指令中已包含（如"分析 BANK-89156"），直接使用；否则提示用户提供。

**收集项 2 - 本地工作目录**：询问本地项目根目录（如 `C:\workspace`），各服务仓库均在该目录下。
- Windows 路径转换为 bash 路径：`C:\workspace` → `/c/workspace`，`D:\projects` → `/d/projects`
- 记录为 `WORKSPACE` 变量（bash 路径格式），后续所有命令基于此路径

**收集项 3 - 开发人员（可选）**：若用户指定了开发人员（姓名或用户名，可多个，如"张三"或"zhang.san"），记录为 `DEV_FILTER` 列表；未提供则分析该需求**所有**开发人员的变更。
- 支持中文姓名（如"高原"）或英文用户名（如"yuan.gao"）匹配
- 多人时以逗号分隔，如"张三,李四"
- Jira 评论中开发人员信息格式：`[姓名|http://gitlab.in.za/username]`，两种格式均可匹配

---

## 阶段 1：获取 Jira 信息

将响应**保存到文件再解析**（避免管道传输 JSON 丢失）：

```bash
JIRA_TMP="${WORKSPACE}/.jira_tmp_${ISSUE_KEY}.json"
curl -sk \
  -H "Authorization: Bearer ${JIRA_TOKEN:-MTE4MDMxOTEyNjMwOogU+AFSs09tgxWWFhWCY8gjzP2b}" \
  -H "Accept: application/json" \
  "https://jira.in.za/rest/api/2/issue/${ISSUE_KEY}" \
  -o "${JIRA_TMP}"
wc -c "${JIRA_TMP}"   # 验证文件非空
```

解析时用文件读取，不用管道：

```bash
PYTHON=$(which python 2>/dev/null || which python3 2>/dev/null)
${PYTHON} - << 'PYEOF'
import json
with open('${JIRA_TMP}', encoding='utf-8') as f:
    data = json.load(f)
# 提取：summary / issuetype.name / fixVersions / components / comment.comments
PYEOF
```

提取字段详见 `references/jira-api.md`。解析完成后执行 `rm -f "${JIRA_TMP}"`。

**优化需求判断**：issuetype 或 summary/description 含"优化"、"重构"、"性能"、`refactor`、`optimize` 等关键词时，标记为优化需求，额外输出优化影响分析。

---

## 阶段 2：提取开发分支信息

**首选：从 Jira 评论提取**（ZA Bank 实际分支信息所在）。Infra-DevOps 机器人在 MR 创建时自动发评论，格式：
```
[高原|http://gitlab.in.za/yuan.gao] mentioned this issue in [a merge request|http://...] 
of [zabank / imc / zabank-imc-cubercore-service|http://...] 
on branch [BANK-89156_20260414_1632|http://...]:{quote}feat(BANK-89156):...{quote}
```

正则提取（详见 `references/jira-api.md`），**若指定了 `DEV_FILTER`，需先过滤开发人员**：

```python
import re, json

with open(jira_tmp_file, encoding='utf-8') as f:
    data = json.load(f)

comments = data['fields']['comment']['comments']
repo_branch_map = {}   # {service_name: (branch_name, developer)}
dev_filter = []  # 从阶段0收集，空列表=不过滤

for comment in comments:
    body = comment.get('body', '')
    
    # 提取评论中的开发人员（中文姓名或英文用户名）
    # 格式：[姓名|http://gitlab.in.za/username] 或 [username|...]
    dev_match = re.match(r'^\[([^\|]+)\|[^\]]*gitlab[^\]]*\]', body.strip())
    developer = dev_match.group(1).strip() if dev_match else ''
    
    # 若指定了过滤条件，判断是否匹配（姓名或 URL 中的用户名任一命中即可）
    if dev_filter:
        url_username = ''
        if dev_match:
            url_match = re.match(r'^\[[^\|]+\|[^\]]*gitlab\.in\.za/([^\]]+)\]', body.strip())
            url_username = url_match.group(1).strip() if url_match else ''
        matched = any(
            f.strip().lower() in developer.lower() or
            f.strip().lower() in url_username.lower()
            for f in dev_filter
        )
        if not matched:
            continue  # 跳过不匹配的评论
    
    # 提取仓库名（路径最后一段）
    repo_match = re.search(r'of \[.*?([a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+)\|', body)
    # 提取分支名
    branch_match = re.search(r'on branch \[([^\]|]+)', body)
    
    if repo_match and branch_match:
        repo_name = repo_match.group(1)
        branch_name = branch_match.group(1)
        repo_branch_map[repo_name] = (branch_name, developer)

for repo, (branch, dev) in repo_branch_map.items():
    print(f"服务: {repo}, 分支: {branch}, 开发: {dev}")
```

若指定了 `DEV_FILTER` 但过滤后结果为空，则提示用户：
> 未在 Jira 评论中找到指定开发人员 `{DEV_FILTER}` 的提交记录，请确认姓名/用户名是否正确，或检查该需求是否有 MR 关联。

结果记录为 `{仓库名: (分支名, 开发人员)}` 映射，去重后得到涉及服务列表。**备选**：Development API（见 `references/jira-api.md`）。

---

## 阶段 3：检查本地仓库并获取代码变更

对每个服务逐一处理：

**步骤 3.1 - 检查仓库**：仓库目录名为评论中路径最后一段（如 `zabank-imc-cubercore-service`）：
```bash
[ -d "${WORKSPACE}/<service-name>/.git" ] && echo "存在" || echo "不存在"
```

**步骤 3.2 - 仓库不存在时**：立即告知用户，给出克隆命令，**等待用户操作后再继续**，不静默跳过：
```
git clone git@gitlab.in.za:zabank/<group>/<service-name>.git ${WORKSPACE}/<service-name>
```

**步骤 3.3 - 执行 git diff**：使用 `git -C` 绝对路径避免 cd 上下文丢失：
```bash
# fetch 并确认分支
git -C "${WORKSPACE}/<svc>" fetch origin 2>&1 | tail -3
git -C "${WORKSPACE}/<svc>" branch -r | grep "<branch>"

# 变更统计
git -C "${WORKSPACE}/<svc>" diff origin/master...origin/<branch> --stat

# 分段 diff（单服务超 800 行时按模块分批）
# 1. SQL/DB 变更（最优先）
git -C "${WORKSPACE}/<svc>" diff origin/master...origin/<branch> -- "*.sql" "*/migration*" -U3

# 2. 核心业务代码
git -C "${WORKSPACE}/<svc>" diff origin/master...origin/<branch> \
  -- "*/controller/*" "*/service/*" "*/mq/*" "*/powerjob/*" \
  --exclude="*Test*" --exclude="*DTO*" -U3

# 3. 配置和依赖
git -C "${WORKSPACE}/<svc>" diff origin/master...origin/<branch> \
  -- "*/application.yml" "*/application.properties" "pom.xml" "go.mod" -U3
```

---

## 变更分析维度

### 1. 变更范围识别

按文件类型分类：接口层（Controller）、业务逻辑层（Service）、数据访问层（DAO/Mapper）、DB变更（SQL）、配置变更（yml）、依赖变更（pom.xml）、测试代码。

### 2. 业务流程 & 数据库信息分析

从代码调用链（Controller → Service → DAO）还原主要业务流程，并梳理每个流程的数据库操作。

**业务流程识别**：
- 描述流程入口 → 核心逻辑 → 外部调用（MQ/Feign/Job）的完整步骤
- 标注关键判断（开关、状态机、并发控制）

**数据库操作表（每个流程一张）**：

| 表名 | 操作 | 关键字段 / 条件 | 索引 | 备注 |
|------|------|--------------|------|------|
| t_xxx | SELECT | WHERE user_id = ? | 无索引（⚠️） | 全表扫描风险 |
| t_yyy | INSERT | user_id, status | PRIMARY KEY | 正常 |

**DDL 变更单独列出**：字段类型变更（nullable→NOT NULL 的存量 NULL 风险）、新建表（索引覆盖情况）、新增字段（是否需要唯一索引）。

### 3. 质量风险识别

风险分类及识别模式详见 `references/risk-patterns.md`：
- **P0 高风险**：DB Schema 变更、接口契约变更、核心业务逻辑修改、并发/事务变更、安全变更
- **P1 中风险**：缓存策略变更、外部服务依赖变更、配置项变更、批量/定时任务变更
- **P2 低风险**：日志变更、代码重构、依赖版本升级

### 4. 优化需求额外分析

若标记为优化需求：性能预期影响（N+1 改善/引入、缓存命中变化、接口响应时间）、兼容性风险（存量数据、API 消费方、配置预置）、回归风险（重构边界、隐式依赖）。

---

## 输出格式

生成两份 Markdown 文件至 `./result/` 目录（模板详见 `references/output-template.md`）：

**`<需求ID>_代码变更分析.md`**：
1. 需求概览（含分析范围：全量开发人员 or 指定人员名单）→ 2. 变更概览表 → 3. 各服务变更详情 → 4. 业务流程 & 数据库信息 → 5. 质量风险汇总 → 6. [优化需求] 优化影响分析

**`<需求ID>_测试策略.md`**：
1. 测试范围和目标 → 2. P0 必测用例 → 3. P1 建议用例 → 4. P2 可选用例 → 5. 回归测试建议 → 6. 测试数据准备 → 7. 测试环境依赖

---

## 注意事项（环境兼容性）

| 问题 | 解决方案 |
|------|---------|
| Python 命令 | `which python 2>/dev/null \|\| which python3 2>/dev/null`，不硬编码 `python3` |
| Windows 路径 | Git Bash 用 `/c/workspace`，不是 `/mnt/c/`（WSL 路径） |
| 临时文件 | 写入 `${WORKSPACE}/.jira_tmp_xxx.json`，不用 `/tmp/` |
| JSON 解析 | `curl -o <file>` 保存后 Python 读文件，不用管道传 JSON |
| git 路径 | 用 `git -C "${WORKSPACE}/<svc>"` 绝对路径，不用 `cd` |
| 分支已合并 | `git log --first-parent master --merges --grep="<ISSUE_KEY>"` 找合入 commit |
| Token 安全 | 不在输出报告中记录 Token 明文 |

---

## 参考文件

- **`references/jira-api.md`** - Jira API 字段说明及 ZA Bank 分支信息提取规则（含完整 Python 解析脚本）
- **`references/risk-patterns.md`** - P0/P1/P2 风险识别模式详解（12种风险类型）
- **`references/output-template.md`** - 两份输出文件的完整 Markdown 模板
