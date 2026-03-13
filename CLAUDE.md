# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📋 项目概述

这是一个基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案。核心是 `qa-toolkit` 插件，包含三个核心 Skills 和五个便捷工作流命令。

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

# 3. API 用例生成（生成自动化测试代码）
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
│   ├── commands/                     # 工作流命令（5个 .md 文件）
│   │   ├── quick-workflow.md         # /qa-quick 命令
│   │   ├── full-workflow.md          # /qa-full 命令（开发中）
│   │   ├── status.md                 # /qa-status 命令
│   │   ├── config.md                 # /qa-config 命令
│   │   └── help.md                   # /qa-help 命令
│   └── skills/                       # 三个核心 Skills
│       ├── shift-left-analyzer/
│       │   ├── SKILL.md              # Skill 定义（包含 frontmatter）
│       │   ├── references/           # 参考文档（01-04 编号命名）
│       │   └── examples/             # 使用示例
│       ├── requirement-validator/
│       │   └── SKILL.md
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
3. **手工案例生成**：manual-case-generator（🚧 开发中）
4. **自动化案例生成**：`api-case-generator`（✅ 已完成）

**当前替代方案**：
```bash
/requirement-validator              # 需求检查
/qa-quick ./docs/plan.md            # 快速生成接口测试
```

## 📝 开发规范

### 新增或修改 Skills

1. **Skill 定义文件**：`plugins/qa-toolkit/skills/<skill-name>/SKILL.md`
   - 必须包含 YAML frontmatter：name、description
   - description 应包含触发该 Skill 的关键词
   - 详细说明 Skill 的目标、功能、使用方式

2. **参考文档**：`plugins/qa-toolkit/skills/<skill-name>/references/`
   - 使用编号前缀命名：`01-xxx.md`、`02-xxx.md`
   - 编号顺序反映文档的重要性和阅读顺序
   - 在 SKILL.md 中引用时使用相对路径：`references/01-xxx.md`

3. **示例文件**：`plugins/qa-toolkit/skills/<skill-name>/examples/`
   - 提供实际使用示例
   - 包括输入输出示例

### 新增工作流命令

1. **命令文件**：`plugins/qa-toolkit/commands/<command-name>.md`
   - 文件名对应命令（如 `quick-workflow.md` → `/qa-quick`）
   - 必须包含 YAML frontmatter：name、description、arguments（可选）
   - 详细描述命令的功能、使用方式、执行流程

2. **命令注册**：
   - Claude Code 会自动识别 commands/ 目录下的 .md 文件
   - 无需手动注册

### 文档更新规范

- **主文档**：`README.md` - 面向最终用户的完整文档
- **插件文档**：`plugins/qa-toolkit/README.md` - qa-toolkit 使用指南
- **架构图**：`architecture.puml` - PlantUML 格式的系统架构图
- **优化总结**：项目根目录的 `*_SUMMARY.md` 文件记录优化历史

### 引用路径规范

- Skills 中引用 references 文档时使用相对路径
- 示例：`references/01-interface-validation.md`（不是 `./references/01-interface-validation.md`）
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
- `plugins/qa-toolkit/skills/api-case-generator/SKILL.md`

## 🚧 开发状态

### 已完成（✅）
- shift-left-analyzer - 测试左移分析器
- requirement-validator - 需求验证器
- api-case-generator - API 用例生成器
- `/qa-quick` - 快速模式工作流命令
- `/qa-status`、`/qa-config`、`/qa-help` - 辅助命令

### 开发中（🚧）- 预计 2026-04-20
- 需求文档规范 Skill
- 设计文档规范 Skill
- 手工案例生成 Skill
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
