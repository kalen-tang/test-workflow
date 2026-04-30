# za-qe 插件架构文档

> **版本**：对应 `za-qe` v2.5.9
> **最后更新**：2026-04-30
> **适用读者**：插件维护者、测试左移工作流使用者、Skill 扩展开发者

---

## 1. 总览

`za-qe` 是 ZA Bank 测试左移工具集，基于 Claude Code 插件机制构建。核心目标是把"需求文档 / 设计文档"一路贯通到"可执行的 API 自动化测试代码 + 可视化测试设计"，全过程由 Claude 作为执行者，各 Skill 作为单一职责单元协同完成。

### 1.1 能力定位

| 维度 | 内容 |
|------|------|
| 插件名 | `za-qe` |
| 类型 | core（marketplace `alfie-qe`） |
| 入口 Commands | `/za-qe:qe-workflow`、`/za-qe:qe-gencase`、`/za-qe:qe-help` |
| Skills 数量 | 8 个（doc-converter / req-parser / design-parser / interface-extractor / case-designer / api-generator / doc-reviewer / code-diff-analysis） |
| 主要依赖 | `uv`（Python 运行时）、`markitdown`（docx → md）、`plantuml.in.za`（UML 校验）、`udoc.in.za`（接口文档）、`jira.in.za`（Jira API） |

### 1.2 分层结构

```
┌─────────────────────────────────────────────────────────────┐
│  Command 层（编排器）                                         │
│  qe-workflow        ── 全流程 8 阶段编排                      │
│  qe-gencase         ── 单独调用 case-designer                 │
│  qe-help            ── 文档/帮助                              │
├─────────────────────────────────────────────────────────────┤
│  Skill 层（单一职责单元）                                     │
│  doc-converter      文档转换                                  │
│  req-parser         需求标准化                                │
│  design-parser      设计规范化 + UDOC 补全                    │
│  interface-extractor接口数据提取 + 网关校验                   │
│  case-designer      流程图 + MindMap + 场景案例表 + XMind     │
│  api-generator      pytest 测试代码 + YAML 数据               │
│  doc-reviewer       三方对齐质量报告                          │
│  code-diff-analysis Jira + git diff 风险分析                  │
├─────────────────────────────────────────────────────────────┤
│  基础工具层（Bash 脚本 / 第三方依赖）                          │
│  convert_docx.py   plantuml_to_xmind.py   validate_plantuml.py│
│  markitdown   md2xmind   httpx   chardet                     │
│  UDOC sync API   PlantUML Server   Jira REST API             │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 数据流概览（workflow 主链路）

```
docx/doc ──► doc-converter ──► BANK-XXXX_PRD.md / BANK-XXXX_DESIGN.md
                                        │
         ┌──────────────────────────────┤
         ▼                              ▼
   req-parser                     design-parser
   (7 章 PRD)                     (UDOC 补全接口)
         │                              │
         │                              ▼
         │                     interface-extractor
         │                     (接口数据报告 + 网关校验)
         ▼                              │
   case-designer ◄─ (可选：接口数据) ────┘
   ├─ 流程图（PlantUML Activity）
   ├─ 测试功能点 MindMap
   ├─ 详细测试案例 MindMap
   ├─ .xmind 文件（md2xmind）
   └─ 场景案例表 (CASE_TABLE.md)
         │
         ▼
   api-generator
   ├─ testcases/test_*.py（pytest + @pytest.mark.data）
   ├─ data/**/*.yaml（variables + tests）
   └─ scenario/*.py（Fixture 命名自动检测）
```

---

## 2. 插件配置与权限模型

### 2.1 两级配置

**`.claude-plugin/plugin.json`**（插件元数据）：

```json
{
  "name": "za-qe",
  "version": "2.5.9",
  "commands": ["./commands/"],
  "skills": ["./skills/"]
}
```

**`settings.json`**（插件级权限清单）：

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run *)", "Bash(uvx *)",
      "Read", "Write", "Edit", "Glob", "Grep",
      "AskUserQuestion", "Task", "TaskCreate", "TaskUpdate",
      "Skill(za-qe:doc-converter)", "Skill(za-qe:req-parser)",
      "Skill(za-qe:design-parser)", "Skill(za-qe:interface-extractor)",
      "Skill(za-qe:case-designer)", "Skill(za-qe:api-generator)"
    ]
  }
}
```

### 2.2 权限模型三层收敛

| 层次 | 文件 | 作用 |
|------|------|------|
| 插件级 | `plugins/za-qe/settings.json` | 工作流命令可调用的工具集合（例：只允许 `uv run` / `uvx`，不允许任意 shell） |
| Skill 级 | 每个 `SKILL.md` frontmatter 的 `allowed-tools` | 进一步收敛单个 Skill 所需的最小工具集 |
| 命令级 | `commands/*.md` frontmatter 的 `allowed-tools` | 命令执行时的顶层工具白名单 |

**安全设计要点**：

- Bash 命令被限定在 `uv run *` / `uvx *`，杜绝任意 shell 执行
- `code-diff-analysis` 额外允许 `curl` / `git` / `python` / `ls` / `mkdir`，因其需要抓取 Jira API 与 git diff
- Skill 默认不能读取原始 `.doc/.docx`，下游 Skill 统一消费 `doc-converter` 产出的 `.md`

---

## 3. Skill 详细解析

### 3.1 doc-converter — 文档格式转换器

| 项目 | 内容 |
|------|------|
| 版本 | 1.0.0 |
| allowed-tools | `Read, Glob, Bash(uv run:*)` |
| 核心脚本 | `scripts/convert_docx.py`（PEP 723 内联依赖） |
| 依赖 | `markitdown[docx]>=0.1.0`、`chardet>=5.0` |

**两种模式**：

- **单文件模式**（workflow 中使用）：`--file <input> --output-file <output>`，直接输出到目标路径
- **批量模式**（独立使用）：`<input_dir> <output_dir> [--prefix]`

**编码检测优先级**：`utf-8 → utf-8-sig → gb18030 → big5 → utf-16`（先用 `chardet` 检测，失败后回退手动枚举）。

**输出状态码**：`OK / FIXED:<enc> / WARN / ERROR`，便于上层解析。

---

### 3.2 req-parser — 需求文档标准化

| 项目 | 内容 |
|------|------|
| 版本 | 2.0.0 |
| allowed-tools | `Read, Write, Edit, Glob, Grep` |
| 输入 | md / docx / txt |
| 输出 | `<模块名>_规范化需求文档.md`（严格 7 章 PRD 模板） |

**7 章结构**：

1. 需求背景与目标
2. 专业术语表
3. 业务逻辑与功能需求（含 3.1-3.7 子章节）
4. 非功能需求
5. 验收标准（给定-当-则 格式）
6. 版本规划
7. 附件

**关键能力**：

- **繁简转换**：自动识别繁体中文统一转简体
- **复杂度自适应**：`≤3` 个功能模块 → 一次性 Write；`>3` 个 → 先写骨架，按 2-3 个模块分组用 Edit 追加
- **忠于原文**：原文未涉及的章节标注"原文未涉及"，不做臆造

---

### 3.3 design-parser — 设计文档规范化

| 项目 | 内容 |
|------|------|
| 版本 | 1.0.0 |
| allowed-tools | `Read, Write, Edit, Glob, Grep, Bash, TaskCreate, TaskUpdate` |
| 必须章节 | 第 2 章（整体概要设计）、第 4 章（需求模块拆解）、第 5.x.4 接口报文 |
| 按需章节 | 流程图 / UML / DB 变更（原文无则标"无"） |

**核心流程 — UDOC 补全**（design-parser 的差异化价值）：

```bash
# 按"微服务连字符名 + 接口 URL 编码"查询
curl --ssl-revoke-best-effort --location --request POST \
  'https://udoc.in.za/sync/doc?moduleName={svc}&url={path-encoded}' \
  -o result/_tmp_udoc_{id}.json
```

提取字段：`name / description / url / httpMethod / contentType / queryParams / requestParams / responseParams`，以 UDOC 数据为准覆盖原文不全处。

**规范校验结果的三态处理**：

| 情况 | 处理 |
|------|------|
| 按需章节原文为空 | 标"无" |
| 接口字段缺失 | 按规范列补全，缺失列占"—" |
| URL 含 `/dmb/` | 插入 `> ⚠️ 网关接口` 警告 |
| 必须章节缺失 | 插入 `> ❌ [缺失]` 并在末尾汇总"待补充清单" |

---

### 3.4 interface-extractor — 接口数据提取器

| 项目 | 内容 |
|------|------|
| 版本 | 1.0.0 |
| allowed-tools | `Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate` |
| 输入 | design-parser 产出 md（必须）+ req-parser 产出 md（可选） |
| 输出 | `<输出目录>/<项目名>_接口数据报告.md` |

**职责边界**（`做/不做` 严格划分）：

- ✅ 做：接口信息提取、dmb 网关检测、微服务识别映射、参数结构化、依赖关系分析
- ❌ 不做：测试场景设计、测试用例推荐（交给 case-designer）

**接口路径校验**（核心业务规则）：

```
路径含 "dmb" → 网关接口 → 暂停 + 提示用户替换为微服务接口
不含 dmb   → 根据路径前缀映射微服务，补齐 "微服务域名/接口路径" 格式
         示例：zabank_imc_activity_service/activity/list
```

**依赖关系识别模式**：

- ID 传递：A.response.xxxId → B.request.xxxId
- 状态关联：A 修改状态 → B 查询状态
- CRUD 模式：create/add/save → get/query/list → update → delete
- 审批流：submit → review/audit → approve/reject

---

### 3.5 case-designer — 场景案例设计器

| 项目 | 内容 |
|------|------|
| 版本 | 2.0.0 |
| allowed-tools | `Read, Write, Edit, Glob, Grep, Bash(uv *), Bash(uv run:*), Task, TaskCreate, TaskUpdate` |
| 脚本 | `validate_plantuml.py`、`plantuml_to_xmind.py` |
| 产出 | `BANK-XXXX_CASE.md`、`BANK-XXXX_CASE.xmind`、`temp/BANK-XXXX_CASE_TABLE.md` |

**三类可视化产出**：

| 产出 | 结构 | 主题 |
|------|------|------|
| 业务流程图 | PlantUML Activity Diagram | `!theme materia` |
| 测试功能点 MindMap | ≥3 层（项目 → 功能模块 → 功能点 → 验证点） | `blueprint + materia` |
| 详细测试案例 MindMap | ≥4 层（根 → 场景 → 操作 → 验证 → 详细） | 同上 |

**独特设计：子代理执行 + 自动重试**

流程图生成放在 **Task 子代理** 中执行，主流程只传入路径与脚本位置，子代理内部做"生成 → `validate_plantuml.py` 验证 → 失败修正重试（最多 5 次）"循环，最终通过 `---STATUS---\n(OK|WARN ...)\n---END---` 标记回传结果。

**原因**：PlantUML 语法试错过程可能耗费多轮工具调用，隔离到子代理中可避免污染主流程上下文。

**PlantUML 校验脚本原理**（`validate_plantuml.py`）：

```python
# 将 PlantUML 源码 zlib 压缩 + 自定义 base64 编码 → URL 路径
# GET https://plantuml.in.za/svg/<encoded> → 返回 SVG
# 若 SVG 中含 "Syntax Error?" → 语法错误
# 否则 → 通过
```

**XMind 生成**（`plantuml_to_xmind.py`）：

1. 正则提取 Markdown 中"详细测试案例"章节下的 `@startmindmap...@endmindmap`
2. 将 `*` 替换为 `#`（md2xmind 需要 Markdown 列表格式）
3. 调用 `md2xmind.start_trans_content()` 生成 `.xmind`

**场景案例表** 是给 api-generator 消费的结构化数据，包含：
- 场景总览（ID / 名称 / 类型 / 优先级 / 涉及接口）
- 场景详情（前置条件 / 步骤表 / 验证点）
- 数据传递标记：`{{步骤N.字段名}}`

---

### 3.6 api-generator — API 测试代码生成器

| 项目 | 内容 |
|------|------|
| 版本 | 2.0.0 |
| allowed-tools | `Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate` |
| 依赖框架 | `pytest_zabank_wholesale`、`pytest_zati_base` |

**三种输入模式优先级**：

1. **推荐**：接口数据报告 + 场景案例表 → 完整场景串联测试
2. **降级**：仅接口数据报告 → 单接口正常/异常/边界用例
3. **旧格式兼容**：单个 Markdown 包含接口 + 用例

**五大核心技术约定**：

| 约定 | 说明 |
|------|------|
| 数据驱动 | `@pytest.mark.data()` 装饰器（不是 parametrize） |
| 变量渲染 | YAML 用 `variables` + `data.render()` |
| Scenario 模式 | 测试方法传 Step 对象，Scenario 内部断言 |
| Fixture 命名 | 本服务简化（`core_sc`），跨服务完整（`imc_activity_sc`） |
| 异常用例 | 同一方法中 `data[key]` 访问，不为每个异常单写方法 |

**Fixture 自动检测算法**：

```
current_project = 提取自项目路径 (如 zabank-eln-case → eln)
service_name    = 从 API 路径识别 (如 zabank_eln_approval_service)

if current_project in service_name:
    → 本服务，简化命名：approval_sc
else:
    → 跨服务，完整命名：imc_activity_sc
```

**生成文件结构**：

```
test_automation_case/
├── testcases/test_{module}.py
├── data/{module}/{interface}.yaml           # variables + tests
├── data/{module}/{interface}_fail.yaml      # 异常场景分离
├── scenario/{module}_scenario.py
├── service/{service_name}/__init__.py       # 接口映射 + Model 类
└── conftest.py
```

---

### 3.7 doc-reviewer — 需求实现检查

| 项目 | 内容 |
|------|------|
| 版本 | 1.0.0 |
| 输入 | 需求目录（必须）+ 设计目录（可选）+ 代码差异目录（可选） |
| 输出 | `./result/<需求ID>_需求实现检查报告.md` |

**三类文档独立评分维度（各 100 分）**：

| 文档类型 | 完整性 | 明确性/合理性 | 可行性/详细度 | 规范性 | 其他 |
|---------|--------|---------------|---------------|--------|------|
| 需求 | 30 | 25 | 20 | 15 | 可测试性 10 |
| 设计 | 30 | 25 | 20 | 15 | 可维护性 10 |
| 代码差异 | 30 | 规范性 25 | 正确性 25 | 安全性 20 | — |

**对齐分析三层**：需求 vs 设计 → 设计 vs 代码 → 整体综合分

**对齐等级**：精准对齐 / 基本对齐 / 部分对齐 / 未对齐

---

### 3.8 code-diff-analysis — 代码变更分析器

| 项目 | 内容 |
|------|------|
| allowed-tools | `Read, Write, Glob, Grep, Bash(curl/git/python/ls/mkdir *), TaskCreate, TaskUpdate` |
| 输入 | Jira 需求 ID + 本地工作目录 + 可选开发人员过滤 |
| 输出 | `<需求ID>_代码变更分析.md` + `<需求ID>_测试策略.md` |

**五阶段流程**：

```
阶段 0 启动信息收集  → 需求编号 / WORKSPACE / 开发人员过滤
阶段 1 获取 Jira 信息 → Bearer Token 调用 /rest/api/2/issue/{key}
阶段 2 提取开发分支   → 从 Jira 评论正则提取 "MR + branch + 开发人"
阶段 3 检查本地仓库 + git diff (分段：SQL → 业务 → 配置)
变更分析维度         → 层级识别 + 业务流程/DB 操作表 + P0/P1/P2 风险
```

**环境兼容性设计**（Windows / Git Bash 特化）：

- Python 命令：`which python 2>/dev/null || which python3`
- Windows 路径：`C:\workspace` → `/c/workspace`（Git Bash），**不是** `/mnt/c/`（WSL）
- 临时文件：`${WORKSPACE}/.jira_tmp_xxx.json`，不用 `/tmp/`
- JSON 解析：`curl -o <file>` + Python 读文件，避免管道传 JSON 丢失
- git 操作：`git -C <abs_path>`，不用 `cd`

**风险分级**（详见 `references/risk-patterns.md`）：

| 等级 | 类型 |
|------|------|
| P0 高 | DB Schema、接口契约、核心业务、并发/事务、安全 |
| P1 中 | 缓存、外部依赖、配置、批/定时任务 |
| P2 低 | 日志、重构、依赖升级 |

---

## 4. Workflow 编排引擎（`qe-workflow`）

`/za-qe:qe-workflow` 是最复杂的 Command，下面按阶段剖析其编排逻辑。

### 4.1 阶段划分

| 阶段 | 名称 | 关键动作 |
|------|------|---------|
| 0 | 续传检测 + 预扫描 | **并行** `Glob` 检测 workflow.md、docx 文件、pytest.ini |
| 1 | 环境探测 + 交互配置 | **单次** `AskUserQuestion` 合并 4 问（ID / 需求 / 设计 / 自动化目录），配置确认后批量 `TaskCreate` |
| 2 | 文档转换 | 调用 doc-converter（单文件模式，直输目标路径） |
| 3.1 / 3.2 | req-parser / design-parser | 有设计文档时**并行派发 2 个 Task 子代理**，否则主流程直调 |
| 3.3 | interface-extractor | 消费 `BANK-XXXX_DESIGN.md` 生成 `temp/BANK-XXXX_接口数据报告.md` |
| 3.4 | case-designer | 消费 PRD + 接口数据报告，产出 CASE / CASE_TABLE / xmind |
| 3.5 | api-generator | 仅在有自动化目录 + 接口数据时执行，输出到自动化工程 |

### 4.2 核心设计模式

#### 4.2.1 断点续传（workflow.md 状态锚点）

在**根目录**（= 需求文档所在目录，非 CWD）创建 `workflow.md`：

```markdown
# Workflow 状态记录
**需求ID**：BANK-XXXX
**根目录**：<绝对路径>

## 配置
- 需求文档：xxx.docx
- 设计文档：yyy.docx 或 无
- 自动化目录：<路径> 或 无

## 执行进度
- [x] 阶段2：文档转换
- [x] 阶段3.1：req-parser → BANK-XXXX_PRD.md
- [!] 阶段3.2：design-parser → BANK-XXXX_DESIGN.md   ← 失败标记
- [ ] 阶段3.3：interface-extractor
...
```

**三态标记**：`[ ]` 未完成 / `[x]` 完成 / `[!]` 失败

**有效性校验**（续传前）：若已完成步骤的输出文件不存在 → 重置为 `[ ]` 重跑。

#### 4.2.2 交互式配置的严格约束

`AskUserQuestion` 的 options 构建有**严格模板**：

- **禁止**添加"手动输入"/"自定义"类选项（`AskUserQuestion` 自带 Other 输入框即是手动输入）
- 必填项（需求ID / 需求文档）：候选 + "无，中断退出"（≥ 2 个选项硬性约束）
- 可选项（设计 / 自动化）：候选 + "无" + "跳过"

**需求ID 过滤规则**：仅数字 ≥ 10000 的 `BANK-\d{5,}` / `IP-\d{5,}` 作为候选，小号（如 BANK-999）过滤掉。

#### 4.2.3 根目录动态确定

步骤 1.2.5 中，**根目录 = 需求文档所在目录**（不一定是 CWD）。若根目录 ≠ CWD 则：

- 并行 A：重新 Glob 根目录扫描（更新设计 / ID / pytest.ini 候选）
- 并行 B：检测根目录下的 workflow.md（若存在则询问是否续传覆盖）

**终止条件**：根目录由需求文档路径唯一决定，1.2.5 不允许改需求文档路径，避免循环。

#### 4.2.4 并行子代理（性能优化）

3.1 + 3.2 有设计文档时，用 **Task 工具同时派发 2 个子代理**并行执行 req-parser 和 design-parser。主流程等两者完成后，从子代理输出中用正则提取 `---STATUS---\n(.*?)\n---END---` 判断状态。

仅需求场景（无设计文档）则**禁用子代理**，主流程直调 `Skill(za-qe:req-parser)` 避免不必要的上下文切换。

#### 4.2.5 格式预检（绕过无用转换）

阶段 2 前检查文档扩展名：若已是 `.md` → 直接 `cp` 到目标路径，跳过 doc-converter 调用。

---

## 5. 关键脚本与工具依赖

### 5.1 脚本清单

| 脚本 | 所属 Skill | 依赖 | 核心功能 |
|------|-----------|------|---------|
| `convert_docx.py` | doc-converter | markitdown、chardet | docx/doc → md + 编码修复 |
| `validate_plantuml.py` | case-designer | httpx | zlib+base64 编码后请求 `plantuml.in.za` 校验语法 |
| `plantuml_to_xmind.py` | case-designer | md2xmind | 正则提取 MindMap → md 格式转换 → XMind |

所有脚本使用 PEP 723 内联依赖声明（`# /// script ... # ///`），`uv run` 自动管理临时虚拟环境。

### 5.2 外部服务依赖

| 服务 | 用途 | 调用方 |
|------|------|--------|
| `plantuml.in.za/svg/` | PlantUML 语法校验（返回 SVG） | case-designer |
| `udoc.in.za/sync/doc` | 接口文档同步（OpenAPI） | design-parser、interface-extractor |
| `jira.in.za/rest/api/2/issue/` | Jira 需求与评论查询 | code-diff-analysis |
| GitLab（`gitlab.in.za`） | git 仓库（本地 clone） | code-diff-analysis |

### 5.3 Python 环境约定

- Python 版本：≥ 3.10（部分脚本 ≥ 3.14，依 global CLAUDE.md）
- 包管理：`uv`，不用 pip / virtualenv
- 虚拟环境：`.venv/`（已 gitignore）
- Windows 终端：PowerShell 7+（`pwsh`），但 code-diff-analysis 脚本适配 Git Bash

---

## 6. 命名规范与版本约束

| 对象 | 规范 |
|------|------|
| 插件名 | `za-{域}`（如 `za-qe`、`za-qe-tools`） |
| 命令前缀 | `/za-qe:xxx` |
| Skill 命名 | `{功能域}-{类型后缀}`，通用名加 `qe-` 前缀 |
| frontmatter status | 纯文本 `active`，不用 emoji |
| 版本号 | SemVer，新增 Skill/Command → 次版本升级 |
| references 引用 | 无 `./` 前缀的相对路径：`references/xxx.md` |
| plugin.json | **必须**放在 `.claude-plugin/` 子目录下 |

---

## 7. 扩展开发指南

### 7.1 新增 Skill 时同步更新清单

1. `skills/<skill-name>/SKILL.md`（含 YAML frontmatter）
2. `skills/<skill-name>/references/`（编号前缀 `01-xxx.md`）
3. `skills/<skill-name>/examples/`
4. `commands/<command-name>.md`（如需工作流命令）
5. `.claude-plugin/marketplace.json`
6. `plugins/za-qe/.claude-plugin/plugin.json`（版本 + 描述）
7. `plugins/za-qe/README.md`、`commands/help.md`
8. 项目根 `README.md` 和 `CLAUDE.md`

### 7.2 参考示例

- **完整 Skill 参考**：`case-designer`（含 scripts / references / examples 三件套）
- **最简 Skill 参考**：`doc-converter`（仅单脚本 + 两种模式）
- **纯 Prompt Skill 参考**：`req-parser`（无脚本，全部靠 Prompt 规则）

### 7.3 Skill 设计原则

- **单一职责**：一个 Skill 只做一件事（对比 interface-extractor 明确标"做"/"不做"）
- **输入输出约定**：下游 Skill 消费上游 md，不直接读原始 doc
- **失败状态回传**：子代理通过 `---STATUS---\n(OK|ERROR|WARN ...)\n---END---` 回传
- **进度可视化**：每个 Skill 用 `TaskCreate` / `TaskUpdate` 追踪步骤进度

---

## 8. 常见扩展场景

| 需求 | 推荐方案 |
|------|---------|
| 新增一类输入文档格式（如 .wps） | 扩展 doc-converter 的 `MarkItDown` 调用或前置转换器 |
| 新增一类可视化产出（如时序图） | 在 case-designer 新增 references + 扩展 MindMap 生成步骤 |
| 新增一个 CI 集成的流水线阶段 | 在 `plugins/za-qe-tools` 注册 hook（PreToolUse / Stop），workflow 保持不变 |
| 替换 UDOC 源为 Swagger | 在 design-parser 的 `udoc-fetcher.md` 中新增 fetcher，保持字段映射一致 |
| 新增语言支持（如英文需求） | req-parser 增加语言识别 + 繁简/英中转换分支 |

---

## 附录 A：快速命令索引

```bash
# 全流程（推荐）
/za-qe:qe-workflow [BANK-ID]

# 独立 Skill 调用
/za-qe:req-parser <doc>
/za-qe:design-parser <doc>
/za-qe:interface-extractor <design.md>
/za-qe:case-designer <req.md>
/za-qe:api-generator <report.md>
/za-qe:doc-reviewer <req_dir> [design_dir] [diff_dir]
/za-qe:code-diff-analysis BANK-ID

# 简化命令
/za-qe:qe-gencase <req.md>      # 仅生成场景案例
/za-qe:qe-help                  # 查看帮助
```

## 附录 B：关键文件路径速查

| 用途 | 路径 |
|------|------|
| 插件清单 | `.claude-plugin/marketplace.json` |
| 插件元数据 | `plugins/za-qe/.claude-plugin/plugin.json` |
| 插件权限 | `plugins/za-qe/settings.json` |
| Workflow 命令 | `plugins/za-qe/commands/workflow.md` |
| PRD 模板 | `plugins/za-qe/skills/req-parser/references/prd-template.md` |
| UDOC fetcher | `plugins/za-qe/skills/design-parser/references/udoc-fetcher.md` |
| 系统架构图 | `architecture.puml` |
| 插件规范文档 | `docs/alfie-plugin-spec.md` |
