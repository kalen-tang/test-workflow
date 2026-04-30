# 工程全局视图概览

> **项目名称**：银行测试自动化工具集（基于 Claude Code 插件系统）
> **Marketplace**：`alfie-qe`（owner: Alfie）
> **仓库**：`gitlab.in.za/claude/alfie/qe`
> **生成时间**：2026-04-30

---

## 1. 项目定位

基于 **Claude Code 插件系统**构建的测试左移工具集，覆盖从需求分析到自动化测试代码生成的全链路，服务于银行业务的研发测试流程。

核心特征：

- **插件化架构**：一个 Marketplace 聚合四个独立插件，职责清晰、可选装
- **Skill 驱动**：每个功能单元是一个带 frontmatter 的 `SKILL.md`，由命令按需激活
- **文档即代码**：命令（`commands/*.md`）和 Skills（`skills/*/SKILL.md`）都是 Markdown，易维护
- **工具链基于 uv + Python**：所有脚本使用 PEP 723 内联依赖声明，无 `pyproject.toml`

---

## 2. 顶层目录结构

```
qe/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场定义（注册 3 个插件）
├── CLAUDE.md                     # Claude Code 在此仓库的操作指南
├── README.md                     # 安装说明 + 架构图
├── architecture.puml             # 系统架构 PlantUML 源文件
├── docs/
│   ├── alfie-plugin-spec.md      # 插件扩展规范
│   ├── MCP.md / Skills.md        # MCP 和 Skill 概念文档
│   └── architecture-redesign.md  # 架构演进记录
└── plugins/
    ├── za-qe/                    # 核心插件：测试左移（8 Skills + 3 Commands）
    ├── za-qe-tools/              # 通用工具：Hook 驱动的 4 个模块
    ├── za-qe-ui/                 # UI 自动化：Playwright 代码优化
    └── za-qe-perf/               # 性能与规范：INVEST 框架规范（未注册到 marketplace）
```

### 2.1 插件注册关系

| 插件 | 版本 | 注册方式 | 类型 |
|---|---|---|---|
| `za-qe` | v2.5.9 | marketplace.json 的 `core` 分类 | 核心 |
| `za-qe-tools` | v3.3.1 | marketplace.json 的 `optional` 分类 | 可选 |
| `za-qe-ui` | v1.0.0 | marketplace.json 的 `optional` 分类 | 可选 |
| `za-qe-perf` | v1.0.0 | **未注册** 到 marketplace.json，独立存在 | 独立 |

---

## 3. 全局架构图

```
┌────────────────────────────────────────────────────────────────────┐
│                          用户交互层                                │
│     命令（/za-qe:xxx、/za-qe-tools:xxx、/za-qe-ui:xxx 等）       │
└────────────────────────────────────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  za-qe 插件  │     │ za-qe-ui     │     │ za-qe-perf       │
│              │     │              │     │                  │
│ 测试左移主线 │     │ UI 自动化    │     │ 规范检查         │
│ 文档→用例    │     │ Playwright   │     │ INVEST 框架      │
└──────┬───────┘     └──────────────┘     └──────────────────┘
       │
       │ 调用 Skill
       ▼
┌────────────────────────────────────────────────────────────┐
│ req-parser → design-parser → interface-extractor →        │
│   case-designer → api-generator                            │
│                                                            │
│ + 独立 Skills: doc-converter / doc-reviewer / code-diff-   │
│                analysis                                    │
└────────────────────────────────────────────────────────────┘
                               │
                               ▼
                   ┌────────────────────────┐
                   │ za-qe-tools（横向能力）│
                   │  Hook 驱动：            │
                   │  - 状态栏                │
                   │  - 系统通知              │
                   │  - 命令审批（Dippy）     │
                   │  - 事件流（ESP）         │
                   └────────────────────────┘
```

---

## 4. 模块深度拆解

### 4.1 `za-qe`：测试左移核心插件

#### 4.1.1 定位

从**原始需求/设计文档**到**可执行 API 测试代码**的全流程自动化。

#### 4.1.2 三个命令

| 命令 | 作用 | 主要能力 |
|---|---|---|
| `/za-qe:qe-workflow [需求ID]` | **全流程编排**，自动串联 5 个核心 Skill | 环境探测、断点续传、交互式配置、阶段任务追踪 |
| `/za-qe:qe-gencase [doc_paths]` | 独立生成场景测试案例（不依赖 workflow） | PlantUML 流程图 + 两层 MindMap |
| `/za-qe:qe-help [topic]` | 分类帮助（skills / workflow / examples） | 工具集自述文档 |

#### 4.1.3 八个 Skill

| Skill | v | 核心职责 | 输入 | 输出 |
|---|---|---|---|---|
| `doc-converter` | 1.0 | docx/doc → UTF-8 Markdown，自动修复编码 | docx/doc 文件或目录 | 同名 `.md` 文件 |
| `req-parser` | 2.0 | 需求文档 → 7 章 PRD 标准模板 | .md/.docx/.txt/.pdf | `{ID}_规范化需求文档.md` |
| `design-parser` | 1.0 | 设计文档规范化 + UDoc 补全 | 原始开发方案 | `{ID}_规范化开发方案.md` |
| `interface-extractor` | 1.0 | 接口信息结构化提取（可走 UDoc） | 规范化设计文档 | `{ID}_接口数据报告.md` |
| `case-designer` | 2.0 | 生成 PlantUML 流程图 + MindMap + 场景表 | 规范化需求（+ 接口数据） | `{ID}_CASE.md` + `.xmind` + `CASE_TABLE.md` |
| `api-generator` | 2.0 | 生成 pytest 测试代码 + YAML 数据 | 接口数据 + 场景案例表 | `test_{module}.py` + data YAML + scenario/service |
| `doc-reviewer` | 1.0 | 三方文档质量评分 + 对齐分析 | 需求/设计/代码差异目录 | `{ID}_需求实现检查报告.md` |
| `code-diff-analysis` | — | 从 Jira + git diff 提取代码变更，输出风险 | 需求 ID + 工作目录 | `{ID}_代码变更分析.md` + `测试策略.md` |

#### 4.1.4 workflow 命令的四个阶段

```
阶段 0：续传检测
  ↓ 检测 workflow.md → 询问继续 / 清除

阶段 1：环境探测 + 交互式配置
  ↓ 并行 Glob 扫描文件、需求 ID、pytest.ini
  ↓ 单次 AskUserQuestion 合并展示 4 个配置项
  ↓ 确认执行计划 → 写 workflow.md + NOTES.md

阶段 2：文档转换
  ↓ doc-converter（uvx markitdown）
  ↓ 输出 BANK-XXXX_PRD.md / DESIGN.md

阶段 3：Skill 串联（按分支决策）
  ├─ 仅需求：req-parser → case-designer
  └─ 需求+设计：req-parser + design-parser（并行）
                  → interface-extractor → case-designer → api-generator
```

**分支决策矩阵**：

| 需求 | 设计 | 自动化目录 | 路径 |
|---|---|---|---|
| ✅ | ✅ | ✅ | 完整链路，5 Skills |
| ✅ | ✅ | ❌ | 跳过 api-generator |
| ✅ | ❌ | * | req-parser → case-designer |
| ❌ | * | * | **中止** |

#### 4.1.5 关键脚本

| 脚本 | 所属 Skill | 用途 |
|---|---|---|
| `convert_docx.py` | doc-converter | docx/doc 批量转 md + 编码修复 |
| `validate_plantuml.py` | case-designer | PlantUML 语法验证（HTTP 调用 `plantuml.in.za`） |
| `plantuml_to_xmind.py` | case-designer | PlantUML MindMap → XMind 文件 |

#### 4.1.6 关键约定

- **所有 Bash 命令使用绝对路径**，禁止 `cd`
- **Windows 路径转 Git Bash**：`C:\workspace` → `/c/workspace`
- **禁止 `;` 连接命令**，只用 `&&`
- **文件命名**：`BANK-\d{5,}` 或 `IP-\d{5,}`，数字 ≥ 10000
- **PlantUML 主题**：流程图 `materia`，MindMap `blueprint + materia`

---

### 4.2 `za-qe-tools`：通用工具集（Hook 驱动）

#### 4.2.1 定位

为所有 Claude Code 会话提供横向能力，四个模块独立开关：**状态栏、系统通知、命令审批（Dippy）、事件流查看（ESP）**。

#### 4.2.2 Hook 注册机制

插件通过 `plugin.json` 的 `hooks` 字段注册 6 个生命周期事件，全部指向 `scripts/hook-router.py` 做统一路由：

| 事件 | Async | 路由目标 |
|---|---|---|
| `SessionStart` | — | `auto-setup.py`（状态栏初始化） |
| `PreToolUse` (Bash) | 否 | `hook-router.py --event PreToolUse`（命令审批） |
| `PostToolUse` | 是 | `hook-router.py --event PostToolUse`（事件流） |
| `PostToolUseFailure` | 是 | `hook-router.py --event PostToolUseFailure` |
| `Stop` | 是 | `hook-router.py --event Stop`（会话结束通知） |
| `PermissionRequest` | 是 | `hook-router.py --event PermissionRequest` |

#### 4.2.3 脚本清单

| 脚本 | 功能 |
|---|---|
| `hook-router.py` | 统一 Hook 路由，根据 `~/.claude/za-qe-tools.json` 配置决策执行哪些模块 |
| `auto-setup.py` | SessionStart 初始化，写入 `~/.claude/settings.json` 的 `statusLine` |
| `statusline.py` | 纯 ASCII 状态栏 |
| `statusline-powerline.py` | Powerline 风格状态栏，支持 Nerd Font 图标 |
| `notify.py` | 跨平台通知（Windows winotify / macOS osascript） |
| `notify-permission.py` | 权限等待超时提醒 |
| `clear-permission-flag.py` | 清理权限等待临时标记文件 |

#### 4.2.4 命令与二进制

| 命令 / 文件 | 作用 |
|---|---|
| `/za-qe-tools:config [module on/off]` | 交互式或直接开关 dippy/notify/esp/statusline |
| `/za-qe-tools:esp [-w]` | 启动事件流查看器（新终端或当前交互式） |
| `bin/claude-esp.exe` | ESP 预编译二进制（事件流查看器） |

#### 4.2.5 配置文件

```json
// ~/.claude/za-qe-tools.json
{
  "notify": { "enabled": false },
  "dippy":  { "enabled": false },
  "esp":    { "enabled": false }
}
```

**Dippy 命令审批**：已独立为 `claude-dippy` 包，通过 `uvx claude-dippy` 调用；双层规则（全局 `~/.dippy/config` + 项目 `.dippy`）；日志 `~/.claude/hook-approvals.log`。

---

### 4.3 `za-qe-ui`：UI 自动化测试

#### 4.3.1 定位

将 Playwright 录制脚本（原生代码）转化为**可维护的企业级自动化测试代码**，并提供自动执行与修复能力。

#### 4.3.2 三个 Skill 的分工

| Skill | 输入 | 输出 | 用途 |
|---|---|---|---|
| `qe-ui-generate` | `testcase-native/*.test.ts` | `testcase-optimized/` + 组件/数据 YAML | 录制代码 → 优化架构代码 |
| `qe-ui-execute` | `testcase-optimized/*.test.ts` | 测试结果 + 修复报告 | 运行测试 + 自动修复（最多 3 轮） |
| `qe-ui-update` | 优化脚本 + 改动描述 | 修改后的脚本 | 增量维护（新增步骤、改数据、更新选择器） |

#### 4.3.3 子代理 `qe-ui-agent`

**端到端工作流协调器**，支持三种模式：

- **转换模式**（路径含 `testcase-native`）：转换后询问是否执行测试
- **测试模式**（路径含 `testcase-optimized` 或 `--test`）：仅执行 + 修复
- **完整模式**（`--full`）：转换 + 测试 + 修复，无需人工确认

**修复循环**（最多 3 轮）：

- 第 1 轮：快速修复（导入、语法、配置）
- 第 2 轮：等待优化（加 wait、调超时）
- 第 3 轮：深度修复（更新选择器、修数据、调断言）

#### 4.3.4 两个命令

| 命令 | 参数 | 作用 |
|---|---|---|
| `/za-qe-ui:ui-generate` | 原生脚本路径 `[--full]` | 转换（+ 可选完整测试修复） |
| `/za-qe-ui:ui-update` | 改动描述 / 脚本路径 + 描述 | 增量更新已有优化脚本 |

#### 4.3.5 技术特性

- 组件驱动架构：`componentClick()`、`componentInput()` 等抽象操作
- 混合断言：Playwright 原生 + Midscene AI 辅助
- 智能等待：自动插入恰当的 wait 策略
- 选择器抽取：将 CSS 选择器收敛到 YAML 组件库

---

### 4.4 `za-qe-perf`：INVEST 框架规范检查

#### 4.4.1 定位

面向**众安银行 INVEST 微服务框架**（Spring Boot 2.1.6 + MyBatis-Plus 3.4.0 + OpenFeign）的规范指南与代码分析工具集。**未注册到 marketplace.json，独立存在**。

#### 4.4.2 三个命令

| 命令 | 作用 |
|---|---|
| `/za-qe-perf:overview` | 框架技术栈、分层架构概览（新人 onboarding） |
| `/za-qe-perf:spec-check` | 依次激活 Controller/Service/DAO/DTO/Entity/Exception 6 个规范 Skills 做代码审查 |
| `/za-qe-perf:test-analysis` | 基于 git diff 或指定文件生成测试点分析报告 |

#### 4.4.3 十个 Skill 分类

**架构基础（1）**：

- `invest-framework-overview`

**分层规范（6）**：

| Layer | Skill | 关键约束 |
|---|---|---|
| Controller | `invest-controller-spec` | ResponseData 响应结构、Swagger 注解 |
| Service | `invest-service-spec` | **禁止 @Transactional**，改用 `TransactionUtils.execute()` |
| DAO | `invest-dao-spec` | SBS 用 BaseMapper / FTC 用 CrudMapper |
| DTO | `invest-dto-spec` | BaseReq 继承、PageReqDTO/PageRspDTO |
| Entity | `invest-entity-spec` | @TableName/@TableField 规范 |
| Exception | `invest-exception-spec` | BusinessException + 错误码枚举 |

**技术指南（2）**：

| 技术 | Skill | 内容 |
|---|---|---|
| Database/ORM | `invest-database-guide` | MyBatis-Plus、IPage、LambdaQueryWrapper |
| RPC | `invest-feign-guide` | OpenFeign、Hystrix 熔断、上下文传递 |

**测试分析（1）**：

- `smart-interface-spec`：基于 git diff 自动生成接口/数据层/异常/回归测试方案

#### 4.4.4 核心规范亮点

| 规范 | 关键约束 |
|---|---|
| 事务管理 | **禁用 @Transactional**，统一 `TransactionUtils.execute()`，范围仅包裹写操作 |
| 异常处理 | 统一 `BusinessException`，错误码 `模块前缀+编号`（如 `ORD001`），`ResourceHandler` 国际化 |
| 数据访问 | 大数据量强制分页，避免全表扫描；条件查询用 `LambdaQueryWrapper` |
| Feign | Hystrix 超时 > Feign 超时；处理降级熔断；请求上下文透传 |

---

## 5. 跨模块数据流

以完整的测试左移场景为例（用户触发 `/za-qe:qe-workflow BANK-90819`）：

```
┌───────────────────────────────────────────────────────────────┐
│ 输入                                                           │
│  原始需求文档.docx + 原始开发方案.docx                         │
└───────────────────────────────────────────────────────────────┘
                                │
                                ▼
         ┌────────────────────────────────────────┐
         │ 阶段 2：doc-converter                  │
         │   uvx markitdown + 编码修复            │
         │   → BANK-90819_PRD.md                 │
         │   → BANK-90819_DESIGN.md              │
         └────────────────────────────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                   ▼
    ┌──────────────────┐              ┌──────────────────────┐
    │   req-parser     │              │    design-parser     │
    │  （并行 Task）    │              │   （并行 Task）        │
    │                  │              │                      │
    │ → 规范化需求文档 │              │  UDoc OpenAPI 补全   │
    │   (7 章 PRD)     │              │ → 规范化开发方案     │
    └──────────────────┘              └──────────────────────┘
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │ interface-extractor   │
                                      │                       │
                                      │ 网关检测(dmb)、微服务 │
                                      │ 映射、依赖识别        │
                                      │ → 接口数据报告.md     │
                                      └───────────────────────┘
              │                                   │
              └─────────────────┬─────────────────┘
                                ▼
                   ┌───────────────────────────┐
                   │     case-designer         │
                   │                           │
                   │ 子代理：PlantUML 验证     │
                   │ 主题：materia + blueprint │
                   │ → CASE.md                 │
                   │ → CASE.xmind              │
                   │ → CASE_TABLE.md           │
                   └───────────────────────────┘
                                │
                                ▼
                   ┌───────────────────────────┐
                   │      api-generator        │
                   │                           │
                   │ pytest_zabank 框架        │
                   │ @pytest.mark.data()       │
                   │ Scenario 模式             │
                   │ → test_*.py               │
                   │ → *.yaml（data/scenario） │
                   └───────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│ 产出                                                           │
│  规范化文档 + 测试设计 + pytest 测试代码 + YAML 数据          │
└───────────────────────────────────────────────────────────────┘
```

### 5.1 关键数据契约

| 数据产物 | 产生者 | 消费者 | 格式 |
|---|---|---|---|
| 规范化需求文档 | req-parser | case-designer、api-generator、doc-reviewer | Markdown（7 章 PRD） |
| 规范化设计文档 | design-parser | interface-extractor、api-generator | Markdown |
| 接口数据报告 | interface-extractor | case-designer、api-generator | Markdown（08-interface-data-report 格式） |
| 场景案例 | case-designer | 用户 + workflow 汇总 | Markdown + PlantUML |
| 场景案例表 | case-designer | api-generator | Markdown（结构化表格） |
| 测试代码 + YAML | api-generator | 最终产物 | Python + YAML |
| 代码变更分析 | code-diff-analysis | 独立产物 | Markdown 报告 |

---

## 6. 权限与工具约束模型

### 6.1 两级权限

| 级别 | 文件 | 作用 |
|---|---|---|
| 插件级 | `plugins/za-qe/settings.json` | workflow 命令可用的工具 + 可调用的 Skills 白名单 |
| Skill 级 | 每个 `SKILL.md` 的 `allowed-tools` frontmatter | 单个 Skill 的工具约束 |

### 6.2 Bash 白名单

只允许：

- `Bash(uv run *)` — 执行 Python 脚本（带 PEP 723 内联依赖）
- `Bash(uvx *)` — 运行第三方工具（主要是 `markitdown`）
- `Bash(git *)` / `Bash(curl *)` — 仅 code-diff-analysis 使用

**不允许**任意 shell 命令。

### 6.3 可调用 Skills（workflow 命令）

```
Skill(za-qe:doc-converter)
Skill(za-qe:req-parser)
Skill(za-qe:design-parser)
Skill(za-qe:interface-extractor)
Skill(za-qe:case-designer)
Skill(za-qe:api-generator)
```

---

## 7. 工具链依赖

| 工具 | 用途 | 调用方式 |
|---|---|---|
| **uv** | Python 包管理 + 脚本运行 | `uv run`、`uvx` |
| **markitdown** | docx/doc → markdown | `uvx markitdown` |
| **PlantUML** | 流程图 + MindMap 渲染 + 校验 | HTTP API `plantuml.in.za` |
| **Playwright MCP**（可选） | UDoc 接口文档提取 | `claude mcp add playwright npx @playwright/mcp@latest` |
| **Jira OpenAPI** | code-diff-analysis 获取需求信息 | `curl https://jira.in.za/rest/api/2/issue/{ISSUE_KEY}` |
| **UDoc OpenAPI** | design-parser 补全接口 | `curl https://udoc.in.za/sync/doc?moduleName=...&url=...` |
| **claude-dippy** | Bash 命令审批 | `uvx claude-dippy`（za-qe-tools 依赖） |

### 7.1 PEP 723 内联依赖模式

所有 Python 脚本头部采用：

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx>=0.27.0"]
# ///
```

无需 `pyproject.toml`，`uv run` 自动管理依赖。

---

## 8. 开发与扩展规范

### 8.1 命名规范

- **插件名**：`za-{域}` 格式（如 `za-qe`、`za-qe-ui`）
- **命令前缀**：`/za-qe:xxx`、`/za-qe-tools:xxx`
- **Skill 命名**：`{功能域}-{类型后缀}`（`req-parser`、`case-designer`）
- **SKILL.md frontmatter status**：纯文本 `active`，不用 emoji

### 8.2 新增 Skill 的同步清单

1. `skills/<skill-name>/SKILL.md`（含 frontmatter）
2. `skills/<skill-name>/references/` 参考文档（`01-xxx.md` 编号前缀）
3. `skills/<skill-name>/examples/` 示例
4. `commands/<command-name>.md`（如需新命令）
5. `.claude-plugin/marketplace.json` + `plugins/<plugin>/.claude-plugin/plugin.json`（版本升级）
6. 对应插件 `README.md`、`commands/help.md`
7. 根 `README.md` 和 `CLAUDE.md`

### 8.3 版本管理（SemVer）

- 新增 Skill / Command → 次版本升级（`1.3.0 → 1.4.0`）
- 修复 bug → 补丁升级（`1.3.0 → 1.3.1`）
- 所有文档中 Skills 数量和版本号必须一致

### 8.4 Skill 引用路径约定

无 `./` 前缀的相对路径：

```
references/xxx.md        ✅
./references/xxx.md      ❌
```

---

## 9. 核心技术点速查

| 技术点 | 详情 |
|---|---|
| **接口路径校验** | 路径含 `dmb` → 网关接口，必须替换为微服务接口<br>格式：`微服务域名/接口路径`（如 `zabank_imc_activity_service/activity/list`） |
| **YAML 三环境** | `sit` / `auto_qe` / `uat` |
| **pytest 规范** | pytest + zabank 插件（`pytest_zabank_wholesale`、`pytest_zati_base`），PEP 8，180 字符行长 |
| **PlantUML 主题** | 流程图 `!theme materia`；MindMap `!theme blueprint + materia` |
| **MindMap 层级** | 测试功能点 ≥ 3 层；详细测试案例 ≥ 4 层 |
| **Fixture 命名** | 本服务简化 `{last}_sc`；跨服务完整 `{full}_sc` |
| **断点续传** | workflow.md 记录 `[x]` 完成、`[ ]` 待执行、`[!]` 失败 |
| **繁简转换** | req-parser 自动识别繁体并转简体 |

---

## 10. 重要文档索引

| 文档 | 路径 | 说明 |
|---|---|---|
| 安装指南 | `README.md` | SSH 配置、marketplace 添加、插件安装 |
| Claude 操作指南 | `CLAUDE.md` | 本仓库的开发规范 |
| 插件扩展规范 | `docs/alfie-plugin-spec.md` | hooks、MCP、多插件拆分参考 |
| 系统架构 | `architecture.puml` | PlantUML 源文件 |
| 工作流权限 | `plugins/za-qe/settings.json` | workflow 命令权限白名单 |
| 工作流命令 | `plugins/za-qe/commands/workflow.md` | 30KB 编排脚本（文档即代码） |
| PRD 模板 | `plugins/za-qe/skills/req-parser/references/prd-template.md` | 7 章需求模板 |
| YAML 格式 | `plugins/za-qe/skills/api-generator/references/yaml-format.md` | 测试数据格式规范 |
| 接口校验规则 | `plugins/za-qe/skills/interface-extractor/references/interface-validation.md` | 微服务/网关判定规则 |

---

## 11. 一句话总结

> 这是一个**以 Claude Code 插件系统为载体、以 Skill 为核心、以 Markdown 文档驱动**的银行测试左移工具集：
>
> - `za-qe` 是主线，把需求/设计文档串成一条**自动化流水线**，产出 pytest 测试代码；
> - `za-qe-tools` 是基础设施，通过 **Hook 注入**状态栏、通知、命令审批、事件流；
> - `za-qe-ui` 把手工 **Playwright 录制脚本**升级为可维护的企业级 UI 自动化；
> - `za-qe-perf` 是 **INVEST 框架的规范内化**，让开发和测试都基于同一套规则做检查和生成。
