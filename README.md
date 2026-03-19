# WF Bank Test - 银行测试自动化工具集

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/your-org/wf-bank-test)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-org/wf-bank-test)
[![Updated](https://img.shields.io/badge/updated-2026--03--17-blue.svg)](https://github.com/your-org/wf-bank-test)

## 📑 目录

- [📊 系统概述](#-系统概述)
- [🚀 快速开始](#-快速开始) ⭐ **最快上手：`/qa-quick ./docs/plan.md`**
- [🔄 完整工作流](#-完整工作流)
- [🔧 系统组件详解](#-系统组件详解)
- [📅 实施计划](#-实施计划)
- [📚 附录](#-附录) - 包含优化总结、工作流命令、引用路径更新报告

## 💡 快速上手

**新用户最快开始方式**：
```bash
/qa-quick ./docs/your-plan.md
```
一条命令完成：KM文档分析 → 测试左移报告 → API自动化用例生成 ✅

---

## 📊 系统概述

基于 Claude Code 插件系统构建的**银行测试自动化工具集**,提供从需求分析到用例生成的全流程测试左移解决方案,建立从需求到测试执行的完整自动化流水线,大幅提升测试效率和质量。

### ✨ 最新更新 (v1.2.0 - 2026-03-17)

- 🎉 **新增核心 Skill**: `manual-case-generator` 手工测试案例生成器
- ⭐ **新增工作流命令**: `/qa-manual` 一键生成手工测试案例（PlantUML流程图+MindMap）
- ✅ **完整模式第三阶段完成**: 打通手工案例生成流程
- 📚 **完善文档**: 新增 manual-case-generator 完整参考文档和示例

### 历史更新 (v1.1.0 - 2026-03-13)

- ⭐ **新增工作流命令**: `/qa-quick` 一键执行快速模式（效率提升75%）
- 🔧 **新增辅助命令**: `/qa-status`、`/qa-config`、`/qa-help`
- 📚 **文档规范化**: references 文档编号命名，引用路径全部更新
- 📖 **完善文档**: 3份优化总结报告，详细使用指南

### 🏗️ 系统架构

📋 **架构文档**: [architecture.puml](./architecture.puml)

#### 架构图示

![测试案例生成与自动化流程](https://plantuml.in.za/svg/bLTTJnj757sVNp6bgWIE2CLIfTGFbS0yj59H0scVIbLjrWjUOUywwxL8KY6PJuCDjX4j2Y8230MSFfYcIGGOG_zBwvbTF-KlT7PcTptxOL1vOcVkd7lkdNlFN7-Y9wMq13CfGLP0TbPMCe8cfE5JGPoTqTISaeYhALM3SqbPbxZz3DaNPgGd-ekK13L9r0Lb9iKRY6eweogIeljDW2xhP05_A9ddl-7QMlksPFnwWDUgxSkoMVW35UjeOmT_M33g9G1iDx0FbG_GMQdTF4E5fh7-fW_-0Y3vSxqu5ftNUVns4UyKSEsu3mfPg0bpazApCLKCjpSRjsQZvhKVaxBoZ19sf9L7bQtszR5nk42DiveOLnDIE3GghwBANon21_fhEQkhsWimpuNslQgciav0xkgJMJdLNVOvuACqpvRDZIL8xQSKL3dlvDTZw6WV5G_91qappf_Xupm-E64aQ3AeDVnqz8lubwEFmZpmUU4zK8o4aw1xOV1w2LsSi1nm06b1oGcfk92LR8IHHnP6xr1HOzye_yd2u718CF6a9CxQA1QBaN0UvHDKENRBYuCGCdAG0xaUpsMCnn_tk8du-BUGx4ufk59jt-wHJnPi--yQNZZttGVRCj_NEuMAURwCrbOf1J6T6XSpToN1AZ8u9azFyxvO7QAB1cej4YYyN_LV_yrRjBr9hWxjlMS6xFO83lNNErq_95GnIfro_bWEkUhFMLOYiRg7_MDDVVx2WrJSHXihB4KKAMDP-3dDUxg45I6vEqu3o4b5rT92Iduf9RxBwPcSdWqAGr0IGlKWe0I9dZBWR-oatTK-E_k2Agzm8F-JKaRLT2l0EqiT5q_GLj5JwkoacwXkWeA26YAIV3zEAVt6zJRUNxRqzh25MfK1NtDc0pbozRaRl93JLMRiZGQldvcr3UhXDHUzz5mI9wLiBgK3u6ep74oeSyhWLxmw0LwflFim1aU-UT1kDaaiwFTDV7ZPZuit96NHppyReB2kXBidlPe5V18MiBhVXItbxb7MnS1kPcVLBWq2Xu_U6TLLL2tpvGE0_OHq6R3k14wNyklstSSWwMyY8Qpr7_1j3a2m8RZSyHKKW-RjDbev0LuH7TJacQGUPivAqbowGSMzk_nmzMDHNQbtbkgsAx_kkywyP_1kaxXXHGm0l-Vuw1QT-ryNh5jY5XOjGm0yOkMQTa_7e3s5qAO5hYA5cZ8fxEIlpTijuBuWuQRKlvCraZPTWazLNLVJK9tszLeamlSdunE90Bh3CXWZdn3oYlPlVe5NBlB9rnVv3AeG0sJmUEUAD3w33JxMdfleYWKhNKb9G2kSG53Uog7EUadR_u-kLpWMGg794Fx97q5xTE7UMjW_CZGw51yQ6x1DU5Be_AfpKqNDKyRE0Q6QsYbi6ejNwBffDXhEqUDoP_SDMSM71Vokxiy5BGGh5PpQiUlrQsACPS32D4zNZRqTermmhWz8nFQgqMfsTYzGPRDpkkQmOXD6wnMv2vjLrx_x7enO0qxW0OX49eRRbqMqMVpOMfiOVZZyiRKUYP31uQ1frFAklhDwdLAekx3PoTuAL0nRTwSYwyCpJD0tuDdmpyEUWI50i4G83ar4UQPHyktIvGTJyhk1RnZcjFU4J5DzrtHBs4KzCwsNNPIniqX57qPjFgpEMEqGFknkhIcirUJv1CTOEr_U-SvQSeScnYbgSNBUV8iKpU7WZqavaP2KdvZoKEhERZIuIq30_7y0)

### 📁 项目结构

```
wf_bank_test/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场配置
│
├── plugins/                      # 插件目录
│   └── qa-toolkit/               # 测试自动化工具集
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/              # ✅ 工作流命令
│       │   ├── status.md          # /qa-status
│       │   ├── config.md          # /qa-config
│       │   ├── help.md            # /qa-help
│       │   ├── quick-workflow.md  # /qa-quick ⭐
│       │   ├── manual-case.md     # /qa-manual
│       │   └── full-workflow.md   # /qa-full 🚧
│       ├── skills/                # 核心能力
│       │   ├── shift-left-analyzer/
│       │   ├── requirement-validator/
│       │   ├── manual-case-generator/
│       │   └── api-case-generator/
│       └── README.md
│
├── result/                       # 输出结果
├── architecture.puml             # 系统架构图
├── OPTIMIZATION_SUMMARY.md       # 优化总结
├── WORKFLOW_COMMANDS_SUMMARY.md  # 工作流命令总结
└── REFERENCES_UPDATE_REPORT.md   # 引用路径更新报告
```

### 🎯 核心价值

1. **标准化流程**: 将原始文档转换为标准化格式,确保信息一致性
2. **智能生成**: AI 驱动的测试案例自动生成,提高案例质量和覆盖度
3. **质量保证**: 多维度的需求实现检查,降低缺陷泄漏风险
4. **自动化执行**: 从手工案例到自动化执行的完整链路,提升执行效率
5. **持续优化**: 基于执行结果的案例优化建议,形成闭环反馈

### 🚀 预期效果

| 指标 | 目标 | 说明 |
| ---- | ---- | ---- |
| 📈 效率提升 | 80%+ | 测试案例生成效率大幅提升 |
| ✅ 质量保证 | 95%+ | 需求覆盖率达到高标准 |
| ⚠️ 风险控制 | 提前识别 | 在开发早期标注测试重点和风险点 |
| 💰 成本降低 | 人力释放 | 减少重复性工作,释放测试人员创造力 |

## 🚀 快速开始

### 🎯 qa-toolkit 测试工具集

当前已实现四个核心 Skills 和六个便捷 Commands，支持**快速模式**和**完整模式**两种测试左移工作流：

#### ⚡ 工作流命令（推荐使用）

| 命令 | 功能 | 使用方式 | 状态 |
| ---- | ---- | ------ | ---- |
| **`/qa-quick`** ⭐ | 一键执行快速模式 | `/qa-quick ./docs/plan.md` | ✅ 立即可用 |
| **`/qa-manual`** | 手工测试案例生成 | `/qa-manual ./docs/req.md` | ✅ 可用 |
| **`/qa-status`** | 查看工具状态 | `/qa-status` | ✅ 可用 |
| **`/qa-config`** | 配置工具参数 | `/qa-config mode quick` | ✅ 可用 |
| **`/qa-help`** | 显示帮助信息 | `/qa-help` | ✅ 可用 |
| **`/qa-full`** | 完整模式工作流 | `/qa-full ./project-root` | 🚧 开发中 |

#### 🔧 核心 Skills（高级使用）

| Skill | 功能 | 使用命令 | 状态 |
| ----- | ---- | -------- | ---- |
| **shift-left-analyzer** | 分析 KM 文档，生成测试左移分析报告 | `/shift-left-analyzer ./docs/plan.md` | ✅ |
| **requirement-validator** | 验证需求实现完整性，生成质量评分报告 | `/requirement-validator` | ✅ |
| **manual-case-generator** | 生成手工测试案例（PlantUML流程图+MindMap） | `/qa-manual ./docs/req.md` | ✅ |
| **api-case-generator** | 生成 API 测试用例代码和数据 | `/api-case-generator ./reports/analysis.md` | ✅ |

#### 🎯 推荐工作流

**⚡ 快速模式（推荐）** - **一条命令完成**：
```bash
/qa-quick ./docs/za-zone-development.md
```
等价于手动执行：`shift-left-analyzer` → `api-case-generator`

**📊 完整模式（开发中）** - 四阶段流程：
- 规范化 → `requirement-validator` → 手工案例生成 → `api-case-generator`
- 当前替代方案：`/requirement-validator` + `/qa-manual ./docs/req.md` + `/qa-quick ./docs/plan.md`

> 💡 **新用户建议**：一键使用 `/qa-quick`，高级用户可单独使用 Skills

### 📝 使用示例

#### 一键快速模式（推荐）

```bash
# 一条命令完成快速模式测试左移
/qa-quick ./docs/development-plan.md

# 自动执行：
# 1. 分析 KM 开发方案
# 2. 生成 API 自动化测试用例
# 3. 显示执行结果
```

#### 分步使用示例（高级）

```bash
# 步骤 1: 分析 KM 开发方案
/shift-left-analyzer ./docs/development-plan.md

# 步骤 2: 生成 API 自动化测试用例
/api-case-generator ./result/test-analysis.md
```

#### 完整模式使用示例（组合使用）

```bash
# 完整模式替代方案（当前建议）：
# 1. 需求实现检查
/requirement-validator

# 2. 手工测试案例生成
/qa-manual ./docs/requirement.md

# 3. 一键执行快速模式（API自动化）
/qa-quick ./docs/development-plan.md

# 完整模式工作流（开发中，预计 2026-04-20）：
# /qa-full ./project-root
```

## 🔄 完整工作流

### 🎯 两种测试左移模式

系统支持两种独立的测试左移模式，根据项目需求和文档完整性选择合适的模式。

#### 模式一：快速模式 (一键完成) ✅

**适用场景**：接口测试为主，快速迭代，仅有 KM 开发方案

```
┌──────────────────────────────────────────┐
│     快速模式 - 一键完成接口测试           │
└──────────────────────────────────────────┘

📄 KM 开发方案文档
        ↓
🔄 /qa-quick 工作流命令 ⭐
        ↓ [自动执行]
📊 shift-left-analyzer (负责人: 奕翔)
   - 提取接口信息（微服务路径、参数、响应）
   - 生成单接口测试用例建议
   - 识别业务流程场景用例
        ↓
📋 测试左移分析报告
   - 接口信息汇总
   - 单接口测试用例（正常/异常/边界）
   - 场景测试用例（业务流程）
        ↓ [自动检测路径]
🧪 api-case-generator
   - 生成 Python 测试代码
   - 生成多环境测试数据（sit/auto_qe/uat）
   - 生成执行脚本
        ↓
🎯 API 自动化测试用例集
   - 可直接执行的 pytest 测试代码
   - 标准化的 YAML 测试数据
```

**特点**：
- ⭐ **一键完成**，无需手动执行多步
- ✅ 自动检测中间文件路径，不易出错
- ✅ 详细执行反馈和错误处理
- ✅ 支持中断和恢复功能
- 💡 最适合接口变更、快速迭代场景

**使用方式**：
```bash
# 最简单：一条命令搞定
/qa-quick ./docs/za-zone-development.md

# 等价于手动执行：
/shift-left-analyzer ./docs/za-zone-development.md
/api-case-generator ./result/za_zone_测试左移分析报告.md
```

---

#### 模式二：完整模式 (目标架构) 🚧

**适用场景**：完整项目，需要全面质量保证，有齐全的需求/设计/代码文档

```
┌─────────────────────────────────────────┐
│     完整模式 - 全面质量保证（四阶段）    │
└─────────────────────────────────────────┘

第一阶段：原始产出物规范化
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 原始需求文档 → 需求文档规范 Skill → 需求文档
📄 原始设计文档 → 设计文档规范 Skill → 设计文档
📄 原始历史案例 → CML MCP → 历史案例
💻 开发代码 → Code Diff MCP → 代码变更分析
        ↓
📦 规范化产出物
   - 标准化需求文档
   - 标准化设计文档
   - 规范化历史案例
   - 代码差异分析报告

第二阶段：需求实现检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 规范化产出物（需求、设计、代码差异）
        ↓
✅ requirement-validator
        ↓
📊 需求实现检查报告
   - 文档质量评分（A/B/C/D）
   - 需求对齐度分析
   - 测试重点和风险标注

第三阶段：手工案例生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 规范化产出物（需求、设计、历史案例、代码差异）
        ↓
📝 manual-case-generator ✅
        ↓
📄 结构化手工测试用例

第四阶段：自动化案例生成与执行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 手工测试用例 + 📦 规范化产出物
        ↓
🧪 api-case-generator
   辅助工具：
   - Udoc2Code MCP（生成接口代码）
   - Proxy MCP（提供抓包逻辑）
        ↓
🎯 自动化测试用例集
        ↓
📈 执行结果分析
   - 覆盖率统计
   - 缺陷反馈
   - 案例优化建议
```

**最终产出物**：
- ✅ 需求实现检查报告（质量评分、风险标注）
- ✅ 结构化手工测试用例
- ✅ API 自动化测试用例集
- ✅ 执行结果分析报告

**当前状态**：
- ✅ requirement-validator (已完成)
- ✅ manual-case-generator (已完成)
- ✅ api-case-generator (已完成)
- 🚧 需求文档规范 Skill (规划中)
- 🚧 设计文档规范 Skill (规划中)
- 🚧 CML MCP (规划中)
- 🚧 Code Diff MCP (规划中)
- 🚧 Udoc2Code MCP (规划中)
- 🚧 Proxy MCP (规划中)

---

#### 两种模式对比

| 维度 | 快速模式 | 完整模式 |
|-----|---------|-----------|
| **执行命令** | `/qa-quick ./docs/plan.md` ⭐ | `/qa-full ./project-root` 🚧 |
| **执行步骤** | 1条命令（自动串联2个Skills） | 1条命令（自动串联4个阶段） |
| **输入要求** | 仅需 KM 开发方案 | 需求 + 设计 + 代码 + 历史案例 |
| **处理时间** | 短（10-20分钟） | 长（1-2小时） |
| **测试覆盖** | 接口自动化测试 | 手工 + 自动化 + 需求验证 |
| **质量保证** | 接口级验证 | 全流程验证（规范化→检查→生成→执行） |
| **产出物** | API 自动化用例 | 检查报告 + 手工用例 + 自动化用例 |
| **当前状态** | ✅ 立即可用 | 🚧 开发中（预计 2026-04-20） |
| **推荐场景** | 接口变更、快速迭代 | 新功能开发、重大变更 |
| **与架构图关系** | 独立快速通道 | 对应架构图四阶段流程 |

---

### 系统完整流程 (四阶段设计 - 完整模式详解)

> 💡 **说明**：以下四阶段流程对应架构图 `architecture.puml` 中的完整模式设计

#### 完整流程逻辑图

```
原始产出物（Raw Inputs）
├── 原始需求文档
├── 原始设计文档
├── 开发代码
└── 原始历史案例
        ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第一阶段】原始产出物规范化
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ↓
    [并行处理]
    ├─→ 需求文档规范 Skill → 标准化需求文档
    ├─→ 设计文档规范 Skill → 标准化设计文档
    ├─→ CML MCP → 规范化历史案例
    └─→ Code Diff MCP → 代码变更分析报告
        ↓
规范化产出物（Normalized Outputs）
├── 标准化需求文档
├── 标准化设计文档
├── 规范化历史案例
└── 代码变更分析报告
        ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第二阶段】需求实现检查（质量保证）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ↓
规范化产出物（需求、设计、代码差异）
        ↓
requirement-validator ✅
        ↓
需求实现检查报告
├── 文档质量评分 (A/B/C/D)
├── 需求对齐度分析
├── 测试重点建议
└── 风险点标注
        ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第三阶段】手工案例生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ↓
规范化产出物（需求、设计、历史案例、代码差异）
        ↓
manual-case-generator ✅
        ↓
结构化手工测试用例
├── 功能测试用例
├── 异常测试用例
└── 边界测试用例
        ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【第四阶段】自动化案例生成与执行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ↓
    [双输入]
    ├── 手工测试用例（第三阶段产出）
    └── 规范化产出物（第一阶段产出）
        ↓
api-case-generator ✅
    [辅助工具]
    ├── Udoc2Code MCP 🚧（生成接口代码）
    └── Proxy MCP 🚧（提供抓包逻辑）
        ↓
自动化测试用例集
├── Python 测试代码（pytest）
├── 多环境测试数据（YAML）
└── 执行脚本
        ↓
测试执行
        ↓
执行结果分析
├── 覆盖率统计
├── 缺陷反馈
└── 案例优化建议
```

#### 关键设计要点

1. **并行处理**：第一阶段的四个规范化任务可以并行执行，提升效率
2. **质量检查前置**：第二阶段在用例生成前进行质量检查，确保后续工作基于高质量文档
3. **双输入源**：第四阶段自动化生成同时使用手工用例和规范化文档，确保用例完整性
4. **辅助增强**：Udoc2Code 和 Proxy MCP 在自动化生成阶段提供底层代码和抓包支持
5. **闭环反馈**：执行结果分析反馈给测试团队，持续优化测试策略

#### 当前实施状态说明

**已完成阶段** ✅：
- **第二阶段**：requirement-validator（提前完成）
- **第四阶段**：api-case-generator（部分功能，当前需手动准备输入）

**开发中阶段** 🚧：
- **第一阶段**：规范化工具（目标 4月20日）
  - 需求文档规范 Skill
  - 设计文档规范 Skill
  - CML MCP
  - Code Diff MCP（建议从Q2提前）
- **第三阶段**：手工案例 Skill（目标 4月20日）

**实施策略**：
- 虽然第二阶段已完成，但当前依赖手动准备规范化文档
- 待第一阶段完成后，可实现完整模式的全自动化流程
- 第四阶段的 api-case-generator 已支持多输入源，待第三阶段完成后可实现双输入

**建议优化**：
⚠️ **Code Diff MCP 优先级调整**：建议从 Q2 提前到 Q1下半（4月20日前），原因：
1. 是 requirement-validator 的关键输入（第二阶段需要代码差异分析）
2. 属于第一阶段规范化的核心组件
3. 当前 requirement-validator 缺少代码差异输入，功能不完整

#### 第一阶段: 原始产出物规范化

**目标**: 将各种原始文档标准化

- **输入**: 原始需求文档、原始设计文档、开发代码、原始历史案例
- **处理工具**:
  - 需求文档规范 Skill (可选增加可测性检查)
  - 设计文档规范 Skill
  - CML MCP (提供历史案例信息,可选案例质量评分)
  - Code Diff MCP (代码差异分析,可选影响范围分析)
- **输出**: 规范化产出物
  - 标准化需求文档
  - 标准化设计文档
  - 规范化历史案例
  - 代码变更分析报告
- **质量保证**: AI+人工复核(抽检 20%)

#### 第二阶段: 需求实现检查

**目标**: 验证需求实现一致性，识别风险点

- **输入**: 规范化产出物（需求文档、设计文档、代码变更分析）
- **处理**: requirement-validator (需求实现检查 Skill) ✅
- **输出**: 需求实现检查报告
  - 文档质量评分 (A/B/C/D)
  - 需求实现对齐度检查
  - 测试重点建议
  - 风险点标注
- **价值**: 为整体测试流程提供质量保障

#### 第三阶段: 手工案例生成

**目标**: 智能生成结构化测试案例

- **输入**: 全部规范化产出物（需求文档、设计文档、历史案例、代码变更分析）
- **处理**: manual-case-generator (手工案例 Skill) 智能生成
- **输出**: 结构化格式的手工测试案例

#### 第四阶段: 自动化案例生成与执行

**目标**: 生成自动化测试用例并执行

- **输入**:
  - 手工测试用例（第三阶段产出）
  - 规范化产出物（第一阶段产出）
- **处理**: api-case-generator ✅ (接口自动化 Skill)
- **辅助工具**:
  - Udoc2Code MCP: 生成接口代码
  - Proxy MCP: 提供抓包接口逻辑
- **输出**:
  - 自动化测试用例集
  - 执行结果分析
    - 覆盖率统计
    - 缺陷反馈
    - 案例优化建议

## 🔧 系统组件详解

### Skills 组件

> *斜体标注的组件名称为建议命名，可根据实际情况调整*

| 组件名称 | 描述名称 | 用途 | 负责人 | 状态 |
| -------- | -------- | ---- | ------ | ---- |
| `shift-left-analyzer` | 测试左移分析器 | 分析 KM 文档，生成测试左移分析报告（快速模式专用） | 奕翔 | ✅ 已完成 |
| `requirement-validator` | 需求验证器 | 检查需求实现对齐度,生成质量评分报告 | 宇豪 | ✅ 已完成 |
| `api-case-generator` | API用例生成器 | 生成接口自动化测试用例代码和数据 | 泉政 | ✅ 已完成 |
| *`requirement-normalizer` (建议)* | 需求文档规范化器 | 规范化转化原始需求文档 | 陈贝 | 🚧 规划中 |
| *`design-normalizer` (建议)* | 设计文档规范化器 | 规范化转化原始设计文档 | 陈贝 | 🚧 规划中 |
| `manual-case-generator` | 手工案例生成器 | 生成手工测试案例（PlantUML流程图+MindMap） | 宇宸 | ✅ 已完成 |

### MCP 组件

> *斜体标注的组件名称为建议命名，可根据实际情况调整*

| 组件名称 | 描述名称 | 用途 | 负责人 | 状态 |
| -------- | -------- | ---- | ------ | ---- |
| *`cml-mcp` (建议)* | CML历史案例服务 | 梳理历史案例,转成规范化可参考的历史案例 | 泉政 | 🚧 规划中 |
| *`udoc2code-mcp` (建议)* | 接口代码生成服务 | 生成与更新接口自动化底层 service 接口代码 | 鼎中 | 🚧 规划中 |
| *`code-diff-mcp` (建议)* | 代码差异分析服务 | 比对迭代代码差异,产出差异报告,用于检查开发实现内容 | 奕翔 | 🚧 规划中 |
| *`proxy-mcp` (建议)* | 抓包服务 | 提供抓包接口逻辑,辅助接口自动化 | - | 🚧 规划中 |

## 🛠️ 开发指南

### 新增或更新 Skill 的完整流程

当创建新 Skill 或更新现有 Skill 时，需要更新以下文件以保持项目文档的一致性：

#### 1. 核心 Skill 文件

**位置**: `plugins/qa-toolkit/skills/<skill-name>/`

- **SKILL.md** - Skill 定义文件
  - 必须包含 YAML frontmatter（name、description、status）
  - description 字段应包含触发关键词（口语化表达）
  - 详细说明 Skill 的目标、功能、使用方式

- **references/** - 参考文档目录
  - 使用编号前缀命名：`01-xxx.md`、`02-xxx.md`
  - 编号顺序反映文档的重要性和阅读顺序
  - 在 SKILL.md 中引用时使用相对路径

- **examples/** - 示例文件目录
  - 提供实际使用示例
  - 包括输入输出示例

#### 2. 工作流命令（可选）

**位置**: `plugins/qa-toolkit/commands/<command-name>.md`

如果 Skill 需要便捷的工作流命令（推荐使用 `/qa-` 前缀）：

- 文件名对应命令（如 `manual-case.md` → `/qa-manual`）
- 必须包含 YAML frontmatter（name、description、arguments）
- 详细描述命令的功能、使用方式、执行流程
- Claude Code 会自动识别 commands/ 目录下的 .md 文件，无需手动注册

#### 3. 插件配置文件（必须更新）

**`.claude-plugin/marketplace.json`**
- 更新 `description` 字段，反映正确的核心能力数量
- 示例：从"三大核心能力"改为"四大核心能力"

**`plugins/qa-toolkit/.claude-plugin/plugin.json`**
- 更新 `version` 字段（遵循语义化版本）
- 更新 `description` 字段，与 marketplace.json 保持一致

#### 4. 插件级文档（必须更新）

**`plugins/qa-toolkit/README.md`**
- 更新"核心 Skills"数量描述
- 在"工作流命令"表格中添加新命令（如有）
- 在"核心 Skills"部分添加新 Skill 的完整文档
- 更新 Skills 文档链接列表

**`plugins/qa-toolkit/commands/help.md`**
- 更新 Skills 数量
- 在 Skills 列表中添加新 Skill

**`plugins/qa-toolkit/commands/status.md`**
- 更新 Skills 数量
- 在输出示例中添加新命令（如有）

#### 5. 项目级文档（必须更新）

**`README.md`** （项目主文档）
- 更新版本徽章和日期
- 在"最新更新"部分添加更新说明
- 更新项目结构图（添加新的 skill 目录和 command 文件）
- 更新"核心 Skills"和"工作流命令"数量描述
- 在工作流命令表格中添加新命令
- 在核心 Skills 表格中添加新 Skill
- 更新完整模式流程图（如涉及）
- 更新 Skills 组件表格（状态、描述等）
- 更新实施计划（已完成/进行中/计划中）
- 在"Commands 文档"和"Skills 文档"部分添加链接
- 更新完整模式替代方案（如涉及）
- 更新底部版本信息

**`CLAUDE.md`** （开发指南）
- 更新项目概述（Skills 和 Commands 数量）
- 在"最常用命令"或"核心 Skills 使用"中添加示例
- 更新项目结构图
- 更新工作流模式说明（如涉及）
- 在"重要文档"部分添加新 Skill 的 SKILL.md 路径
- 更新开发状态（已完成/开发中）

#### 6. 文档更新清单

创建或更新 Skill 时，请按照以下清单逐项检查：

**核心文件** ✅
- [ ] 创建/更新 `skills/<skill-name>/SKILL.md`
- [ ] 创建/更新 `skills/<skill-name>/references/` 参考文档
- [ ] 创建/更新 `skills/<skill-name>/examples/` 示例文件
- [ ] 创建/更新 `commands/<command-name>.md`（如需要工作流命令）

**配置文件** ✅
- [ ] 更新 `.claude-plugin/marketplace.json` 描述和能力数量
- [ ] 更新 `plugins/qa-toolkit/.claude-plugin/plugin.json` 版本和描述

**插件文档** ✅
- [ ] 更新 `plugins/qa-toolkit/README.md`
  - [ ] Skills 数量
  - [ ] 工作流命令表格
  - [ ] Skills 详细文档
  - [ ] 文档链接列表
- [ ] 更新 `plugins/qa-toolkit/commands/help.md`
- [ ] 更新 `plugins/qa-toolkit/commands/status.md`

**项目文档** ✅
- [ ] 更新 `README.md`
  - [ ] 版本徽章和日期
  - [ ] 最新更新说明
  - [ ] 项目结构图
  - [ ] Skills/Commands 数量
  - [ ] 工作流命令表格
  - [ ] 核心 Skills 表格
  - [ ] 完整模式流程图
  - [ ] Skills 组件表格
  - [ ] 实施计划
  - [ ] Commands 文档链接
  - [ ] Skills 文档链接
  - [ ] 完整模式替代方案
  - [ ] 底部版本信息
- [ ] 更新 `CLAUDE.md`
  - [ ] 项目概述
  - [ ] 最常用命令/核心 Skills 使用
  - [ ] 项目结构图
  - [ ] 工作流模式
  - [ ] 重要文档
  - [ ] 开发状态

#### 7. 版本管理

**语义化版本规则**：
- **主版本号（Major）**：重大架构变更或不兼容的 API 修改
- **次版本号（Minor）**：新增功能、新增 Skill、新增 Command
- **修订号（Patch）**：Bug 修复、文档更新、小幅优化

**示例**：
- `1.0.0` → `1.1.0`：新增 `/qa-quick` 命令
- `1.1.0` → `1.2.0`：新增 `manual-case-generator` Skill
- `1.2.0` → `1.2.1`：修复 Bug 或更新文档

#### 8. 最佳实践

1. **命名规范**
   - Skill 目录：使用 kebab-case（如 `manual-case-generator`）
   - Command 文件：使用 kebab-case（如 `manual-case.md`）
   - Command 名称：使用 `/qa-` 前缀保持一致性（如 `/qa-manual`）

2. **文档质量**
   - SKILL.md 的 description 字段使用口语化表达，便于触发
   - references 文档使用编号前缀，体现阅读顺序
   - 提供完整的使用示例和输出示例

3. **渐进式披露**
   - SKILL.md 保持简洁，详细内容放在 references
   - README.md 提供概览，详细文档链接到 SKILL.md

4. **一致性检查**
   - 确保所有文档中的 Skills 数量一致
   - 确保所有文档中的 Commands 数量一致
   - 确保版本号在所有配置文件中同步

#### 9. 参考示例

参考 `manual-case-generator` Skill 的完整实现：
- [SKILL.md](./plugins/qa-toolkit/skills/manual-case-generator/SKILL.md)
- [Command 定义](./plugins/qa-toolkit/commands/manual-case.md)
- [v1.2.0 更新清单](#-最新更新-v120---2026-03-17)

## 📅 实施计划

### 当前进度 (截至 2026-03-13)

#### ✅ 已完成 (Q1 上半)

**核心 Skills**:
- ✅ **shift-left-analyzer** - 测试左移分析器
- ✅ **requirement-validator** - 需求验证器
- ✅ **manual-case-generator** - 手工案例生成器
- ✅ **api-case-generator** - API用例生成器

**工作流命令** (新增):
- ✅ **`/qa-quick`** - 快速模式工作流 ⭐ 一键执行
- ✅ **`/qa-manual`** - 手工测试案例生成
- ✅ **`/qa-status`** - 查看工具状态
- ✅ **`/qa-config`** - 配置工具参数
- ✅ **`/qa-help`** - 显示帮助信息

**文档优化**:
- ✅ **references 文档规范化命名**（添加编号前缀）
- ✅ **SKILL.md 引用路径更新**（20处引用已全部更新）
- ✅ **项目文档完善**（3份优化总结报告）

#### 🚧 进行中 (Q1 下半 - 目标 4 月 20 日)

**完整模式工作流**:
- 🚧 **`/qa-full`** - 完整模式工作流命令（预留接口）

**第一阶段组件** (规范化)

**高优先级**（完整模式核心依赖）：
- 🚧 **需求文档规范 Skill** - 需求文档规范化器 (陈贝负责)
- 🚧 **设计文档规范 Skill** - 设计文档规范化器 (陈贝负责)
- 🚧 **Code Diff MCP** - 代码差异分析服务 (奕翔负责) ⚠️ 建议从Q2提前
- 🚧 **CML MCP** - CML历史案例服务 (泉政负责)

**中优先级**（辅助增强）：
- 🚧 **Udoc2Code MCP** - 接口代码生成服务 (鼎中负责)

#### 📋 计划中 (Q2)
- 📋 **Proxy MCP** - 抓包服务（辅助工具，根据需求排期）
- 📋 **集成测试与优化** - 完整模式端到端流程验证

### 开发阶段划分

#### Q1 上半（Q1.1）- 基础自动化能力 🟦 ✅
**已完成组件**：
- shift-left-analyzer（快速模式）
- requirement-validator（完整模式第二阶段）⭐ 提前完成
- api-case-generator（两种模式通用）

**说明**：requirement-validator 虽属于完整模式第二阶段，但提前开发完成，当前需要手动准备规范化文档作为输入。

#### Q1 下半（Q1.2）- 文档规范与案例生成 🟩 🚧
- **目标日期**: 2026 年 4 月 20 日
- **开发重点**: 补齐完整模式第一阶段和第三阶段组件
- **预期交付**: 5 个组件（建议将 Code Diff MCP 从 Q2 提前）
  - 需求文档规范 Skill（第一阶段）
  - 设计文档规范 Skill（第一阶段）
  - CML MCP（第一阶段）
  - **Code Diff MCP（第一阶段）⚠️ 建议提前**
  - Udoc2Code MCP（第四阶段辅助）

**已完成里程碑** ✅：
- ✅ 手工案例生成器（manual-case-generator），打通完整模式第三阶段

**关键里程碑**：
- 4 月 20 日前完成规范化工具，实现 requirement-validator 的全自动输入

#### Q2（Q2.1-Q2.2）- 辅助工具与集成优化 🟨 📋
- **Proxy MCP**: 根据实际需求排期（第四阶段辅助工具，优先级较低）
- **端到端集成测试**: 验证完整模式四阶段流程
- **优化迭代**: 基于使用反馈持续改进各组件
- **文档完善**: 补充完整模式使用手册和最佳实践

### ⏰ 资源投入

- **项目投入占比**: 测试工程师总时间的 10%
- **协作方式**: 每周例会同步进度,技术问题即时支持
- **质量保证**: 代码 Review + 集成测试 + 用户验收

## 📚 附录

### 📖 项目文档

#### 核心文档
- **[README.md](./README.md)** - 项目主文档（本文档）
- **[architecture.puml](./architecture.puml)** - 系统架构图
- **[plugins/qa-toolkit/README.md](./plugins/qa-toolkit/README.md)** - qa-toolkit 插件使用指南

#### 优化总结文档 (2026-03-13 新增)
- **[OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md)** - 结构优化总结
  - references 文档规范化命名
  - Commands 目录创建
  - api-case-generator 结构评估
  - 优化前后对比

- **[WORKFLOW_COMMANDS_SUMMARY.md](./WORKFLOW_COMMANDS_SUMMARY.md)** - 工作流命令总结
  - `/qa-quick` 快速模式命令详解
  - `/qa-full` 完整模式命令详解
  - 用户体验提升分析
  - 使用场景和最佳实践

- **[REFERENCES_UPDATE_REPORT.md](./REFERENCES_UPDATE_REPORT.md)** - 引用路径更新报告
  - 20处引用路径更新详情
  - 文件重命名对照表
  - 验证结果和后续建议

#### Commands 文档
- **[commands/status.md](./plugins/qa-toolkit/commands/status.md)** - `/qa-status` 命令文档
- **[commands/config.md](./plugins/qa-toolkit/commands/config.md)** - `/qa-config` 命令文档
- **[commands/help.md](./plugins/qa-toolkit/commands/help.md)** - `/qa-help` 命令文档
- **[commands/quick-workflow.md](./plugins/qa-toolkit/commands/quick-workflow.md)** - `/qa-quick` 命令文档 ⭐
- **[commands/manual-case.md](./plugins/qa-toolkit/commands/manual-case.md)** - `/qa-manual` 命令文档
- **[commands/full-workflow.md](./plugins/qa-toolkit/commands/full-workflow.md)** - `/qa-full` 命令文档 🚧

#### Skills 文档
- **[shift-left-analyzer/SKILL.md](./plugins/qa-toolkit/skills/shift-left-analyzer/SKILL.md)**
  - [references/](./plugins/qa-toolkit/skills/shift-left-analyzer/references/) - 4个参考文档（已编号）
  - [examples/](./plugins/qa-toolkit/skills/shift-left-analyzer/examples/) - 使用示例

- **[requirement-validator/SKILL.md](./plugins/qa-toolkit/skills/requirement-validator/SKILL.md)**

- **[manual-case-generator/SKILL.md](./plugins/qa-toolkit/skills/manual-case-generator/SKILL.md)**
  - [references/](./plugins/qa-toolkit/skills/manual-case-generator/references/) - 4个参考文档（已编号）
  - [examples/](./plugins/qa-toolkit/skills/manual-case-generator/examples/) - 示例需求和输出

- **[api-case-generator/SKILL.md](./plugins/qa-toolkit/skills/api-case-generator/SKILL.md)**
  - [references/](./plugins/qa-toolkit/skills/api-case-generator/references/) - 6个参考文档（已编号）
  - [examples/](./plugins/qa-toolkit/skills/api-case-generator/examples/) - 使用示例

### 🔧 插件配置

#### 两级配置结构

**1. 项目级配置**
`.claude-plugin/marketplace.json` - 定义所有可用插件

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "wf-bank-test",
  "plugins": [
    {
      "name": "qa-toolkit",
      "source": "./plugins/qa-toolkit",
      "category": "testing"
    }
  ]
}
```

**2. 插件级配置**
`plugins/qa-toolkit/.claude-plugin/plugin.json` - 插件元数据

```json
{
  "name": "qa-toolkit",
  "description": "银行测试自动化工具集...",
  "version": "1.0.0",
  "author": {...}
}
```

### 📚 团队培训 (历史)

<details>
<summary>📖 点击展开: Claude 培训计划详情 (2026年1月已完成)</summary>

#### 🎯 1 月底 Claude 培训 (2026 年 1 月 27 日-31 日)

**培训周安排**:
- **1 月 27 日**: 准备工作,环境检查和材料准备
- **1 月 28 日**: 第 1 次培训会话 (1.5 小时)
- **1 月 29 日**: 自主学习和实践时间
- **1 月 30 日**: 第 2 次培训会话 (1.5 小时)
- **1 月 31 日**: 培训总结和开发准备

**第 1 次培训会话 (1.5 小时) - Claude 基础能力**

时间: 1 月 28 日下午 14:00-15:30 (鼎中主讲)
参与者: 全员

培训内容:
- **Claude Code CLI 基础操作** (30 分钟)
  - 基本命令和工作流
  - 项目初始化和管理
  - 代码生成和编辑能力
- **Claude 开发环境搭建** (30 分钟)
  - VS Code + Claude 扩展安装配置
  - API 密钥设置和认证
  - 开发工具链集成
- **Claude 对话与 Prompt 基础** (30 分钟)
  - 有效 Prompt 编写技巧
  - Claude 能力边界和最佳实践
  - 调试和问题排查方法

**第 2 次培训会话 (1.5 小时) - Skills 与 MCP 开发**

时间: 1 月 30 日下午 14:00-15:30 (鼎中主讲)
参与者: 全员

培训内容:
- **Claude Skills 开发** (45 分钟)
  - Skills 框架原理和架构
  - 业务逻辑到 AI 逻辑转换
  - Skill 创建、测试和部署流程
- **Claude MCP 开发** (45 分钟)
  - MCP 框架和通信机制
  - 外部系统集成方法
  - Claude API 使用和集成实践

**培训成果**

达成目标:
- ✅ 团队熟练使用 Claude Code CLI 进行开发
- ✅ 掌握 Claude Prompt 工程基础
- ✅ 了解 Skills 和 MCP 开发流程
- ✅ 能够独立搭建开发环境

**持续技术支持**

技术指导 (鼎中提供):
- **每周二**: 技术答疑会 (1 小时)
- **问题升级**: 重大技术问题即时支持
- **专项指导**: Code Diff MCP 开发深度技术支持

</details>

### 🤝 协作机制

#### 项目管理
- **每周例会**: 嘉龙主持,同步进度和解决问题
- **技术评审**: 鼎中主导技术架构组评审
- **跨组协调**: 鼎中负责技术架构统一性
- **组件集成**: 鼎中负责 MCP 组件间技术集成和 Skills 业务逻辑集成

#### 培训与支持
- **培训答疑**: 鼎中每周二答疑时间,解决开发中的技术问题
- **技术架构组指导**: 鼎中负责 MCP 开发指导和技术攻关

#### 质量保证
- **代码 Review**: 鼎中负责技术架构组 Review
- **集成测试**: 每个里程碑节点进行集成测试,鼎中负责技术架构验证
- **进度把控**: 嘉龙负责整体项目统筹,确保 4 月中旬分批投产
- **质量审核**: 嘉龙负责项目整体质量审核和验收
- **假期协调**: 春节期间保持必要的远程协作和进度跟踪

### 🔮 远期展望

随着核心功能的稳定运行和团队经验的积累,可以考虑以下增强方向:

- **流程优化**: 基于使用数据优化各阶段的处理效率
- **质量提升**: 增强 AI 模型的准确性和智能化水平
- **功能扩展**: 支持更多类型的测试场景和文档格式
- **集成增强**: 与更多外部工具和平台的深度集成

### 🔌 推荐官方插件

如需扩展更多能力,推荐以下官方插件:

#### 插件开发
- **plugin-dev** - 最全面的开发套件,包含 `agent-creator`、`skill-reviewer` 等工具
- **skill-creator** - Skill 专用创建和优化工具

#### 代码质量
- **pr-review-toolkit** - PR 全面审查（6个专业 Agents）
- **code-simplifier** - 代码简化和重构

#### 工作流
- **commit-commands** - 简化 Git 提交流程
- **feature-dev** - 功能开发全流程助手

**官方仓库**: [claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

### 📚 相关文档

- [qa-toolkit 使用指南](./plugins/qa-toolkit/README.md)
- [系统架构图](./architecture.puml)
- [Claude Code 文档](https://claude.ai/code)

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 📄 许可证

MIT License

### 👥 团队

**WF Bank Test Team**

| 角色 | 成员 | 职责 |
| ---- | ---- | ---- |
| 项目管理 | 嘉龙 | 整体统筹、进度把控、质量审核 |
| 技术架构 | 鼎中 | 技术评审、培训指导、架构设计 |
| Skills 开发 | 泉政、陈贝、宇宸、宇豪 | Skills 组件开发 |
| MCP 开发 | 泉政、鼎中、奕翔 | MCP 组件开发 |
| 质量保证 | 慧芳 | 质量复核与验证 |

---

**版本**: v1.2.0 | **更新**: 2026-03-17 | **维护**: WF Bank Test Team
