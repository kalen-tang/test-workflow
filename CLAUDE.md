# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概述

这是一个基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案。核心是 `qa-toolkit` 插件，包含四个核心 Skills 和六个便捷工作流命令。

## 🚀 快速开始

### 最常用命令

```bash
# ⭐ 推荐：一键执行快速模式（最常用）
/qa-quick ./docs/your-plan.md

# 查看工具状态和可用功能
/qa-status

# 查看帮助信息
/qa-help

# 配置工具参数
/qa-config output_dir ./custom-output
```

### 核心 Skills 使用

```bash
# 1. 测试左移分析（分析 KM 文档，生成测试报告）
/shift-left-analyzer ./docs/development-plan.md

# 2. 需求验证（检查需求实现一致性）
/requirement-validator

# 3. 手工案例生成（生成PlantUML流程图和测试用例MindMap）
/qa-manual ./docs/requirement.md

# 4. API 用例生成（生成自动化测试代码）
/api-case-generator ./result/test-analysis.md
```

## 🏗️ 项目架构

### 关键目录结构

```
wf_bank_test/
├── .claude-plugin/
│   └── marketplace.json              # 插件市场配置
├── plugins/qa-toolkit/               # 核心插件
│   ├── .claude-plugin/plugin.json    # 插件元数据
│   ├── commands/                     # 工作流命令（6个 .md 文件）
│   │   ├── quick-workflow.md         # /qa-quick 命令
│   │   ├── manual-case.md            # /qa-manual 命令
│   │   ├── full-workflow.md          # /qa-full 命令（开发中）
│   │   ├── status.md                 # /qa-status 命令
│   │   ├── config.md                 # /qa-config 命令
│   │   └── help.md                   # /qa-help 命令
│   └── skills/                       # 四个核心 Skills
│       ├── shift-left-analyzer/
│       │   ├── SKILL.md              # Skill 定义（包含 frontmatter）
│       │   ├── references/           # 参考文档（01-04 编号命名）
│       │   └── examples/             # 使用示例
│       ├── requirement-validator/
│       │   └── SKILL.md
│       ├── manual-case-generator/
│       │   ├── SKILL.md
│       │   ├── references/           # 参考文档（01-04 编号命名）
│       │   └── examples/             # 使用示例（5个文件）
│       └── api-case-generator/
│           ├── SKILL.md
│           ├── references/           # 参考文档（00-05 编号命名）
│           └── examples/
├── result/                           # 输出目录（报告、测试用例）
├── docs/                             # 文档目录
├── architecture.puml                 # PlantUML 架构图
└── README.md                         # 主文档
```

### 插件系统架构

**两级配置**：
1. **项目级**：`.claude-plugin/marketplace.json` - 定义所有可用插件
2. **插件级**：`plugins/qa-toolkit/.claude-plugin/plugin.json` - 插件元数据

**Skills 定义格式**：
- 每个 Skill 的 `SKILL.md` 文件包含 YAML frontmatter（name、description）
- `description` 字段定义了 Skill 的触发条件（关键词匹配）
- references/ 目录存放详细的参考文档（使用编号前缀：01-、02-）
- examples/ 目录存放使用示例

**Commands 定义格式**：
- commands/ 目录下的 .md 文件定义工作流命令
- 文件名对应命令名（如 `quick-workflow.md` → `/qa-quick`）
- 包含 YAML frontmatter（name、description、arguments）

## 🔄 工作流模式

### 快速模式（✅ 可用，推荐）

**适用场景**：接口测试为主，快速迭代，仅有 KM 开发方案

**一键命令**：`/qa-quick ./docs/plan.md`

**执行流程**：
1. `shift-left-analyzer` - 分析 KM 文档，提取接口信息，生成测试左移分析报告
2. `api-case-generator` - 基于分析报告生成 Python 测试代码和 YAML 测试数据

**输出**：
- `./result/xxx_测试左移分析报告.md` - Markdown 格式分析报告
- `./result/xxx/` - 测试用例目录（包含 Python 代码和 YAML 数据）

### 完整模式（🚧 开发中）

**适用场景**：完整项目，需要全面质量保证

**预计命令**：`/qa-full ./project-root`（预计 2026-04-20 完成）

**四阶段流程**：
1. **规范化阶段**：需求文档规范、设计文档规范、CML MCP、Code Diff MCP
2. **需求检查阶段**：`requirement-validator`（✅ 已完成）
3. **手工案例生成**：`qa-manual` / manual-case-generator（✅ 已完成）
4. **自动化案例生成**：`api-case-generator`（✅ 已完成）

**当前替代方案**：
```bash
/requirement-validator              # 需求检查
/qa-manual ./docs/requirement.md   # 手工案例生成
/qa-quick ./docs/plan.md            # 快速生成接口测试
```

## 📝 开发规范

### 新增或更新 Skill 完整流程

当创建新 Skill 或更新现有 Skill 时，必须按照以下步骤操作以保持项目文档一致性。

#### 步骤 1: 创建/更新核心 Skill 文件

**位置**: `plugins/qa-toolkit/skills/<skill-name>/`

1. **SKILL.md** - Skill 定义文件
   - 必须包含 YAML frontmatter：`name`、`description`、`status`
   - `description` 字段使用口语化表达，包含触发关键词
   - 详细说明 Skill 的目标、功能、使用方式

2. **references/** - 参考文档目录
   - 使用编号前缀命名：`01-xxx.md`、`02-xxx.md`
   - 编号顺序反映文档的重要性和阅读顺序
   - 在 SKILL.md 中引用时使用相对路径：`references/01-xxx.md`

3. **examples/** - 示例文件目录
   - 提供实际使用示例
   - 包括输入输出示例

#### 步骤 2: 创建工作流命令（可选，推荐）

**位置**: `plugins/qa-toolkit/commands/<command-name>.md`

- 文件名对应命令（如 `manual-case.md` → `/qa-manual`）
- 推荐使用 `/qa-` 前缀保持一致性
- 必须包含 YAML frontmatter：`name`、`description`、`arguments`（可选）
- 详细描述命令的功能、使用方式、执行流程
- Claude Code 会自动识别 commands/ 目录下的 .md 文件，无需手动注册

#### 步骤 3: 更新插件配置文件

**必须更新以下文件**：

**`.claude-plugin/marketplace.json`**
```json
{
  "description": "银行测试自动化工具集 - ... X大核心能力"  // 更新核心能力数量
}
```

**`plugins/qa-toolkit/.claude-plugin/plugin.json`**
```json
{
  "version": "1.X.0",  // 遵循语义化版本，新增 Skill 通常升级次版本号
  "description": "... X大核心能力"  // 与 marketplace.json 保持一致
}
```

#### 步骤 4: 更新插件级文档

**`plugins/qa-toolkit/README.md`**
- 更新"核心 Skills"数量描述（如"三个"→"四个"）
- 在"工作流命令"表格中添加新命令（如有）
- 在"核心 Skills"部分添加新 Skill 的完整文档
- 更新 Skills 文档链接列表

**`plugins/qa-toolkit/commands/help.md`**
- 更新 Skills 数量
- 在 Skills 列表中添加新 Skill

**`plugins/qa-toolkit/commands/status.md`**
- 更新 Skills 数量
- 在输出示例中添加新命令（如有）

#### 步骤 5: 更新项目主文档

**`README.md`** 需要更新以下部分：

1. **版本信息**
   - 版本徽章：`1.X.0 → 1.Y.0`
   - 更新日期徽章

2. **最新更新**
   - 添加当前版本的更新说明
   - 将上一版本移至"历史更新"

3. **项目结构图**
   - 添加新的 command 文件
   - 添加新的 skill 目录

4. **快速开始**
   - 更新 Skills 和 Commands 数量描述
   - 在工作流命令表格中添加新命令
   - 在核心 Skills 表格中添加新 Skill

5. **完整工作流**
   - 更新完整模式流程图（如涉及）
   - 更新当前状态说明
   - 更新完整模式替代方案（如涉及）

6. **系统组件详解**
   - 在 Skills 组件表格中添加新 Skill
   - 更新状态、描述等信息

7. **实施计划**
   - 在"已完成"部分添加新 Skill
   - 从"进行中"移除已完成项
   - 更新 Q1/Q2 开发阶段说明

8. **附录 - 文档链接**
   - 在"Commands 文档"部分添加命令链接
   - 在"Skills 文档"部分添加 Skill 链接

9. **底部版本信息**
   - 更新版本号和日期

**`CLAUDE.md`** 需要更新以下部分：

1. **项目概述**
   - 更新 Skills 和 Commands 数量

2. **快速开始**
   - 在"最常用命令"或"核心 Skills 使用"中添加示例

3. **项目架构**
   - 更新关键目录结构图
   - 添加新的 command 和 skill 目录

4. **工作流模式**
   - 更新完整模式说明（如涉及）
   - 更新当前替代方案（如涉及）

5. **重要文档**
   - 在"Skills 详细文档"部分添加新 Skill 的路径

6. **开发状态**
   - 在"已完成"部分添加新 Skill 和命令
   - 从"开发中"移除已完成项

#### 步骤 6: 文档更新清单

**必查清单** - 创建/更新 Skill 时逐项检查：

**核心文件** ✅
- [ ] `skills/<skill-name>/SKILL.md`
- [ ] `skills/<skill-name>/references/` 参考文档
- [ ] `skills/<skill-name>/examples/` 示例文件
- [ ] `commands/<command-name>.md`（如需工作流命令）

**配置文件** ✅
- [ ] `.claude-plugin/marketplace.json` 描述和数量
- [ ] `plugins/qa-toolkit/.claude-plugin/plugin.json` 版本和描述

**插件文档** ✅
- [ ] `plugins/qa-toolkit/README.md` 所有相关部分
- [ ] `plugins/qa-toolkit/commands/help.md` Skills 列表
- [ ] `plugins/qa-toolkit/commands/status.md` Skills 数量

**项目文档** ✅
- [ ] `README.md` 所有 9 个部分（见步骤 5）
- [ ] `CLAUDE.md` 所有 6 个部分（见步骤 5）

#### 步骤 7: 版本管理规范

**语义化版本**（SemVer）：
- **Major（主版本）**：重大架构变更或不兼容的 API 修改
- **Minor（次版本）**：新增功能、新增 Skill、新增 Command
- **Patch（修订）**：Bug 修复、文档更新、小幅优化

**示例**：
- 新增 Skill：`1.1.0 → 1.2.0`
- 修复 Bug：`1.2.0 → 1.2.1`
- 重构架构：`1.2.1 → 2.0.0`

#### 步骤 8: 最佳实践

**命名规范**：
- Skill 目录名：`kebab-case`（如 `manual-case-generator`）
- Command 文件名：`kebab-case`（如 `manual-case.md`）
- Command 名称：`/qa-` 前缀（如 `/qa-manual`）

**文档质量**：
- description 使用口语化表达，便于触发
- references 使用编号前缀，体现阅读顺序
- 提供完整的使用示例和输出示例

**渐进式披露**：
- SKILL.md 保持简洁，详细内容放在 references
- README.md 提供概览，详细文档链接到 SKILL.md

**一致性检查**：
- 所有文档中的 Skills 数量必须一致
- 所有文档中的 Commands 数量必须一致
- 版本号在所有配置文件中必须同步

#### 步骤 9: 参考示例

参考 `manual-case-generator` Skill 的完整实现（v1.2.0）：
- Skill 定义：`plugins/qa-toolkit/skills/manual-case-generator/SKILL.md`
- Command 定义：`plugins/qa-toolkit/commands/manual-case.md`
- 文档更新：包含上述所有文件的完整更新

### 引用路径规范

- Skills 中引用 references 文档时使用相对路径
- 正确示例：`references/01-interface-validation.md`
- 错误示例：`./references/01-interface-validation.md`
- 更新引用路径后，检查所有引用是否正确

## 🔧 关键技术点

### Playwright MCP 集成

shift-left-analyzer 支持从网页提取内容（如 UDoc 接口文档）：

```bash
# 安装 Playwright MCP（如未安装）
claude mcp add playwright npx @playwright/mcp@latest
```

**UDoc 登录信息**（域名为 `udoc.in.za`）：
- 账号：`admin`
- 密码：`Za123456`

### 接口路径校验规则

**微服务接口识别**：
- 标准格式：`微服务域名 + 接口路径`
- 示例：`zabank_imc_activity_service/activity/list`
- 如果路径包含 `dmb`，判定为网关接口，必须提示用户替换为微服务接口

**详细规则**：参见 `plugins/qa-toolkit/skills/shift-left-analyzer/references/01-interface-validation.md`

### 测试数据生成规范

api-case-generator 生成的测试数据格式：
- **YAML 格式**：多环境配置（sit、auto_qe、uat）
- **参考文档**：`plugins/qa-toolkit/skills/api-case-generator/references/00-yaml-format.md`
- **代码模板**：`plugins/qa-toolkit/skills/api-case-generator/references/01-test-code-template.md`

### Python 代码规范

生成的 Python 测试代码应遵循：
- 使用 pytest 框架
- 遵循 PEP 8 风格
- 最大行长度：180 字符
- 类型注解：使用 typing 模块
- 文档字符串：reStructuredText (reST) 格式

## 🎯 常见任务

### 分析 KM 开发方案并生成测试用例

```bash
# 推荐：一键完成
/qa-quick ./docs/development-plan.md
```

### 验证需求实现一致性

```bash
# 准备文档目录
mkdir -p ./requirement_word ./design_word
cp 需求文档*.docx ./requirement_word/
cp 设计文档*.docx ./design_word/

# 执行需求验证
/requirement-validator
```

### 仅生成 API 测试用例

```bash
# 假设已有测试左移分析报告
/api-case-generator ./result/test-analysis.md
```

### 查看工具状态和配置

```bash
# 查看状态
/qa-status

# 查看配置
/qa-config

# 修改配置
/qa-config output_dir ./custom-output
/qa-config mode quick
```

## 📚 重要文档

### 核心文档
- `README.md` - 项目完整文档（包含架构、实施计划、团队信息）
- `plugins/qa-toolkit/README.md` - qa-toolkit 使用指南
- `architecture.puml` - 系统架构图（PlantUML 格式）

### 优化总结文档（2026-03-13）
- `OPTIMIZATION_SUMMARY.md` - 结构优化总结
- `WORKFLOW_COMMANDS_SUMMARY.md` - 工作流命令总结
- `REFERENCES_UPDATE_REPORT.md` - 引用路径更新报告

### Skills 详细文档
- `plugins/qa-toolkit/skills/shift-left-analyzer/SKILL.md`
- `plugins/qa-toolkit/skills/requirement-validator/SKILL.md`
- `plugins/qa-toolkit/skills/manual-case-generator/SKILL.md`
- `plugins/qa-toolkit/skills/api-case-generator/SKILL.md`

## 🚧 开发状态

### 已完成（✅）
- shift-left-analyzer - 测试左移分析器
- requirement-validator - 需求验证器
- manual-case-generator - 手工测试案例生成器
- api-case-generator - API 用例生成器
- `/qa-quick` - 快速模式工作流命令
- `/qa-manual` - 手工案例生成命令
- `/qa-status`、`/qa-config`、`/qa-help` - 辅助命令

### 开发中（🚧）- 预计 2026-04-20
- 需求文档规范 Skill
- 设计文档规范 Skill
- CML MCP
- Code Diff MCP（建议优先级提升）
- Udoc2Code MCP
- `/qa-full` - 完整模式工作流命令

### 计划中（📋）- Q2
- Proxy MCP
- 端到端集成测试
- 性能优化

## 👥 团队分工

| 角色 | 成员 | 职责 |
| ---- | ---- | ---- |
| 项目管理 | 嘉龙 | 整体统筹、进度把控、质量审核 |
| 技术架构 | 鼎中 | 技术评审、培训指导、架构设计 |
| Skills 开发 | 泉政、陈贝、宇宸、宇豪 | Skills 组件开发 |
| MCP 开发 | 泉政、鼎中、奕翔 | MCP 组件开发 |
| 质量保证 | 慧芳 | 质量复核与验证 |

## 💡 最佳实践

1. **优先使用 `/qa-quick`**：对于接口测试场景，直接使用快速模式命令，避免手动执行多步
2. **文档质量很重要**：开发方案文档应包含完整的接口设计信息（或 UDoc 链接）
3. **微服务接口优先**：测试左移需要使用微服务接口，避免使用网关接口（包含 `dmb` 的路径）
4. **使用 `/qa-config` 管理配置**：避免手动编辑配置文件
5. **查看 `/qa-status` 了解最新状态**：包括可用 Skills、最近输出、Python 环境检查
6. **保持引用路径一致**：references 目录使用编号前缀命名，引用时使用相对路径
