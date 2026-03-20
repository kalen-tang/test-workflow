# WF Bank Test - 银行测试自动化工具集

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/your-org/wf-bank-test)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/your-org/wf-bank-test)
[![Updated](https://img.shields.io/badge/updated-2026--03--20-blue.svg)](https://github.com/your-org/wf-bank-test)

## 📑 目录

- [系统概述](#-系统概述)
- [快速上手](#-快速上手)
- [系统架构](#️-系统架构)
- [两种工作流模式](#-两种工作流模式)
- [完整模式四阶段设计](#-完整模式四阶段设计)
- [Artifact Schemas 体系](#-artifact-schemas-体系)
- [实施计划](#-实施计划)
- [团队与协作](#-团队与协作)
- [附录](#-附录)

---

## 📊 系统概述

基于 Claude Code 插件系统构建的**银行测试自动化工具集**，提供从需求分析到用例生成的全流程测试左移解决方案，建立从需求到测试执行的完整自动化流水线。

### 核心价值

1. **标准化流程**: 将原始文档转换为标准化格式，确保信息一致性
2. **智能生成**: AI 驱动的测试案例自动生成，提高案例质量和覆盖度
3. **质量保证**: 多维度的需求实现检查，降低缺陷泄漏风险
4. **自动化执行**: 从手工案例到自动化执行的完整链路，提升执行效率
5. **持续优化**: 基于执行结果的案例优化建议，形成闭环反馈

### 预期效果

| 指标 | 目标 | 说明 |
| ---- | ---- | ---- |
| 效率提升 | 80%+ | 测试案例生成效率大幅提升 |
| 质量保证 | 95%+ | 需求覆盖率达到高标准 |
| 风险控制 | 提前识别 | 在开发早期标注测试重点和风险点 |
| 成本降低 | 人力释放 | 减少重复性工作，释放测试人员创造力 |

---

## 🚀 快速上手

```bash
/qa-quick ./docs/your-plan.md
```

一条命令完成：KM文档分析 → 测试左移报告 → API自动化用例生成

> 详细使用指南见 [qa-toolkit 用户手册](./plugins/qa-toolkit/README.md)

### 组件概览

**六个核心 Skills**：

| Skill | 用途 | 负责人 | 状态 |
| ----- | ---- | ------ | ---- |
| `shift-left-analyzer` | 分析 KM 文档，生成测试左移分析报告 | 奕翔 | ✅ |
| `requirement-validator` | 检查需求实现对齐度，生成质量评分报告 | 宇豪 | ✅ |
| `manual-case-generator` | 生成手工测试案例（PlantUML流程图+MindMap） | 鼎中 | ✅ |
| `api-case-generator` | 生成接口自动化测试用例代码和数据 | 泉政 | ✅ |
| `requirement-normalizer` | 将原始需求文档转为标准化 YAML | 陈贝 | ✅ |
| `design-normalizer` | 将原始设计文档转为标准化 YAML | 陈贝 | 🚧 |

**六个工作流命令**：

| 命令 | 功能 | 状态 |
| ---- | ---- | ---- |
| `/qa-quick` | 一键执行快速模式 | ✅ |
| `/qa-manual` | 手工测试案例生成 | ✅ |
| `/qa-status` | 查看工具状态 | ✅ |
| `/qa-config` | 配置工具参数 | ✅ |
| `/qa-help` | 显示帮助信息 | ✅ |
| `/qa-full` | 完整模式工作流 | 🚧 |

> 每个命令和 Skill 的详细参数、示例、输出说明见 [qa-toolkit 用户手册](./plugins/qa-toolkit/README.md)

---

## 🏗️ 系统架构

### 架构文档

📋 **PlantUML 源文件**: [architecture.puml](./architecture.puml)

![测试案例生成与自动化流程](https://plantuml.in.za/svg/bLTTJnj757sVNp6bgWIE2CLIfTGFbS0yj59H0scVIbLjrWjUOUywwxL8KY6PJuCDjX4j2Y8230MSFfYcIGGOG_zBwvbTF-KlT7PcTptxOL1vOcVkd7lkdNlFN7-Y9wMq13CfGLP0TbPMCe8cfE5JGPoTqTISaeYhALM3SqbPbxZz3DaNPgGd-ekK13L9r0Lb9iKRY6eweogIeljDW2xhP05_A9ddl-7QMlksPFnwWDUgxSkoMVW35UjeOmT_M33g9G1iDx0FbG_GMQdTF4E5fh7-fW_-0Y3vSxqu5ftNUVns4UyKSEsu3mfPg0bpazApCLKCjpSRjsQZvhKVaxBoZ19sf9L7bQtszR5nk42DiveOLnDIE3GghwBANon21_fhEQkhsWimpuNslQgciav0xkgJMJdLNVOvuACqpvRDZIL8xQSKL3dlvDTZw6WV5G_91qappf_Xupm-E64aQ3AeDVnqz8lubwEFmZpmUU4zK8o4aw1xOV1w2LsSi1nm06b1oGcfk92LR8IHHnP6xr1HOzye_yd2u718CF6a9CxQA1QBaN0UvHDKENRBYuCGCdAG0xaUpsMCnn_tk8du-BUGx4ufk59jt-wHJnPi--yQNZZttGVRCj_NEuMAURwCrbOf1J6T6XSpToN1AZ8u9azFyxvO7QAB1cej4YYyN_LV_yrRjBr9hWxjlMS6xFO83lNNErq_95GnIfro_bWEkUhFMLOYiRg7_MDDVVx2WrJSHXihB4KKAMDP-3dDUxg45I6vEqu3o4b5rT92Iduf9RxBwPcSdWqAGr0IGlKWe0I9dZBWR-oatTK-E_k2Agzm8F-JKaRLT2l0EqiT5q_GLj5JwkoacwXkWeA26YAIV3zEAVt6zJRUNxRqzh25MfK1NtDc0pbozRaRl93JLMRiZGQldvcr3UhXDHUzz5mI9wLiBgK3u6ep74oeSyhWLxmw0LwflFim1aU-UT1kDaaiwFTDV7ZPZuit96NHppyReB2kXBidlPe5V18MiBhVXItbxb7MnS1kPcVLBWq2Xu_U6TLLL2tpvGE0_OHq6R3k14wNyklstSSWwMyY8Qpr7_1j3a2m8RZSyHKKW-RjDbev0LuH7TJacQGUPivAqbowGSMzk_nmzMDHNQbtbkgsAx_kkywyP_1kaxXXHGm0l-Vuw1QT-ryNh5jY5XOjGm0yOkMQTa_7e3s5qAO5hYA5cZ8fxEIlpTijuBuWuQRKlvCraZPTWazLNLVJK9tszLeamlSdunE90Bh3CXWZdn3oYlPlVe5NBlB9rnVv3AeG0sJmUEUAD3w33JxMdfleYWKhNKb9G2kSG53Uog7EUadR_u-kLpWMGg794Fx97q5xTE7UMjW_CZGw51yQ6x1DU5Be_AfpKqNDKyRE0Q6QsYbi6ejNwBffDXhEqUDoP_SDMSM71Vokxiy5BGGh5PpQiUlrQsACPS32D4zNZRqTermmhWz8nFQgqMfsTYzGPRDpkkQmOXD6wnMv2vjLrx_x7enO0qxW0OX49eRRbqMqMVpOMfiOVZZyiRKUYP31uQ1frFAklhDwdLAekx3PoTuAL0nRTwSYwyCpJD0tuDdmpyEUWI50i4G83ar4UQPHyktIvGTJyhk1RnZcjFU4J5DzrtHBs4KzCwsNNPIniqX57qPjFgpEMEqGFknkhIcirUJv1CTOEr_U-SvQSeScnYbgSNBUV8iKpU7WZqavaP2KdvZoKEhERZIuIq30_7y0)

### 项目结构

```
wf_bank_test/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场配置
├── plugins/
│   └── qa-toolkit/               # 测试自动化工具集（核心插件）
│       ├── .claude-plugin/       # 插件元数据
│       ├── commands/             # 6 个工作流命令
│       ├── skills/               # 6 个核心 Skills
│       │   ├── shift-left-analyzer/
│       │   ├── requirement-validator/
│       │   ├── manual-case-generator/
│       │   ├── api-case-generator/
│       │   ├── requirement-normalizer/
│       │   └── design-normalizer/
│       ├── references/           # 公共参考文档（含 artifact-schemas）
│       └── README.md             # 插件用户手册
├── result/                       # 输出结果
├── architecture.puml             # 系统架构图
├── CLAUDE.md                     # 开发指南
└── README.md                     # 本文档
```

### MCP 组件（规划中）

| 组件名称 | 用途 | 负责人 | 状态 |
| -------- | ---- | ------ | ---- |
| `cml-mcp` | 梳理历史案例，转成规范化可参考的历史案例 | 泉政 | 🚧 规划中 |
| `udoc2code-mcp` | 生成与更新接口自动化底层 service 接口代码 | 鼎中 | 🚧 规划中 |
| `code-diff-mcp` | 比对迭代代码差异，产出差异报告 | 奕翔 | 🚧 规划中 |
| `proxy-mcp` | 提供抓包接口逻辑，辅助接口自动化 | - | 📋 计划中 |

---

## 🔄 两种工作流模式

### 模式一：快速模式 ✅

**适用场景**：接口测试为主，快速迭代，仅有 KM 开发方案

```
📄 KM 开发方案文档
    ↓
🔄 /qa-quick（一条命令）
    ↓ [自动串联]
📊 shift-left-analyzer → 测试左移分析报告
    ↓
🧪 api-case-generator → API 自动化测试用例集
```

### 模式二：完整模式 🚧

**适用场景**：完整项目，需要全面质量保证，有齐全的需求/设计/代码文档

```
📦 原始文档（需求+设计+代码+历史案例）
    ↓
【第一阶段】规范化 → 标准化产出物
    ↓
【第二阶段】requirement-validator → 需求检查报告
    ↓
【第三阶段】manual-case-generator → 手工测试用例
    ↓
【第四阶段】api-case-generator → API 自动化用例集
```

### 两种模式对比

| 维度 | 快速模式 | 完整模式 |
|-----|---------|-----------|
| **执行命令** | `/qa-quick ./docs/plan.md` | `/qa-full ./project-root` 🚧 |
| **执行步骤** | 1条命令（自动串联2个Skills） | 1条命令（自动串联4个阶段） |
| **输入要求** | 仅需 KM 开发方案 | 需求 + 设计 + 代码 + 历史案例 |
| **处理时间** | 短（10-20分钟） | 长（1-2小时） |
| **测试覆盖** | 接口自动化测试 | 手工 + 自动化 + 需求验证 |
| **产出物** | API 自动化用例 | 检查报告 + 手工用例 + 自动化用例 |
| **当前状态** | ✅ 立即可用 | 🚧 开发中（预计 2026-04-20） |
| **推荐场景** | 接口变更、快速迭代 | 新功能开发、重大变更 |

---

## 📐 完整模式四阶段设计

> 对应架构图 `architecture.puml` 中的完整模式流程

### 第一阶段：原始产出物规范化

**目标**：将各种原始文档标准化为统一格式

| 输入 | 处理工具 | 输出 |
|------|---------|------|
| 原始需求文档 | `requirement-normalizer` ✅ | 标准化需求文档（YAML） |
| 原始设计文档 | `design-normalizer` 🚧 | 标准化设计文档（YAML） |
| 原始历史案例 | CML MCP 🚧 | 规范化历史案例（YAML） |
| 开发代码 | Code Diff MCP 🚧 | 代码变更分析报告 |

四个规范化任务可**并行执行**，输出遵循 [Artifact Schemas](#-artifact-schemas-体系) 标准格式。

### 第二阶段：需求实现检查

- **输入**：规范化产出物（需求、设计、代码差异）
- **处理**：`requirement-validator` ✅
- **输出**：需求实现检查报告（质量评分 A/B/C/D、需求对齐度、风险标注）

### 第三阶段：手工案例生成

- **输入**：全部规范化产出物
- **处理**：`manual-case-generator` ✅
- **输出**：结构化手工测试用例（PlantUML 流程图 + MindMap）

### 第四阶段：自动化案例生成与执行

- **输入**：手工测试用例（第三阶段） + 规范化产出物（第一阶段）
- **处理**：`api-case-generator` ✅
- **辅助**：Udoc2Code MCP 🚧、Proxy MCP 🚧
- **输出**：Python pytest 代码 + 多环境 YAML 测试数据 + 执行结果分析

### 关键设计要点

1. **并行处理**：第一阶段四个规范化任务并行执行
2. **质量检查前置**：第二阶段在用例生成前进行质量检查
3. **双输入源**：第四阶段同时使用手工用例和规范化文档
4. **辅助增强**：Udoc2Code 和 Proxy MCP 提供底层代码和抓包支持
5. **闭环反馈**：执行结果分析反馈给测试团队

---

## 📦 Artifact Schemas 体系

完整模式各 Skill 之间通过标准化 YAML 格式通信，定义在 `plugins/qa-toolkit/references/artifact-schemas/`。

> 详细规范见 [Artifact Schemas 总览](./plugins/qa-toolkit/references/artifact-schemas/00-overview.md)

| 编号 | 格式 | 产出工具 | 状态 |
|------|------|---------|------|
| 01 | normalized-requirement | requirement-normalizer | ✅ v2.0 |
| 02 | normalized-design | design-normalizer | ✅ v1.0 |
| 03 | normalized-cases | case-normalizer (CML MCP) | 📋 计划中 |
| 04 | code-diff-report | code-diff-mcp | 📋 计划中 |
| 05 | validation-report | requirement-validator | ✅ v1.0 |
| 06 | manual-test-cases | manual-case-generator | ✅ v1.0 |
| 07 | api-test-cases | api-case-generator | ✅ v1.0 |

核心原则：
- **结构化 > 自然语言**：YAML 定义关键信息
- **可解析性**：包含 `artifact_type`、`version` 元数据
- **前向兼容**：version 字段支持格式升级
- **可追溯性**：`source_file`、`created_at`、`normalizer` 元数据

---

## 📅 实施计划

### ✅ 已完成 (Q1 上半)

**核心 Skills**：
- ✅ `shift-left-analyzer` - 测试左移分析器
- ✅ `requirement-validator` - 需求验证器
- ✅ `manual-case-generator` - 手工案例生成器
- ✅ `api-case-generator` - API 用例生成器
- ✅ `requirement-normalizer` - 需求文档规范化器

**工作流命令**：
- ✅ `/qa-quick`、`/qa-manual`、`/qa-status`、`/qa-config`、`/qa-help`

**Artifact Schemas**：
- ✅ 全部 7 个标准化产出物格式定义完成

### 🚧 进行中 (Q1 下半 - 目标 4 月 20 日)

**高优先级**（完整模式核心依赖）：
- 🚧 `design-normalizer` - 设计文档规范化器（陈贝）
- 🚧 Code Diff MCP - 代码差异分析服务（奕翔）⚠️ 建议从Q2提前
- 🚧 CML MCP - 历史案例服务（泉政）
- 🚧 `/qa-full` - 完整模式工作流命令

**中优先级**（辅助增强）：
- 🚧 Udoc2Code MCP - 接口代码生成服务（鼎中）

### 📋 计划中 (Q2)

- 📋 Proxy MCP - 抓包服务
- 📋 集成测试与优化 - 完整模式端到端流程验证

### 资源投入

- **项目投入占比**: 测试工程师总时间的 10%
- **协作方式**: 每周例会同步进度，技术问题即时支持
- **质量保证**: 代码 Review + 集成测试 + 用户验收

---

## 🤝 团队与协作

### 团队

| 角色 | 成员 | 职责 |
| ---- | ---- | ---- |
| 项目管理 | 嘉龙 | 整体统筹、进度把控、质量审核 |
| 技术架构 | 鼎中 | 技术评审、培训指导、架构设计 |
| Skills 开发 | 泉政、陈贝、宇豪 | Skills 组件开发 |
| MCP 开发 | 泉政、鼎中、奕翔 | MCP 组件开发 |
| 质量保证 | 慧芳 | 质量复核与验证 |

### 协作机制

- **每周例会**: 嘉龙主持，同步进度和解决问题
- **技术评审**: 鼎中主导技术架构组评审
- **培训答疑**: 鼎中每周二答疑时间
- **进度把控**: 嘉龙负责整体统筹，确保 4 月中旬分批投产

---

## 📚 附录

### 项目文档

| 文档 | 路径 |
|------|------|
| 插件用户手册 | [plugins/qa-toolkit/README.md](./plugins/qa-toolkit/README.md) |
| 系统架构图 | [architecture.puml](./architecture.puml) |
| Artifact Schemas 总览 | [references/artifact-schemas/00-overview.md](./plugins/qa-toolkit/references/artifact-schemas/00-overview.md) |
| 开发指南 | [CLAUDE.md](./CLAUDE.md) |

### 优化总结文档

- [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) - 结构优化总结
- [WORKFLOW_COMMANDS_SUMMARY.md](./WORKFLOW_COMMANDS_SUMMARY.md) - 工作流命令总结
- [REFERENCES_UPDATE_REPORT.md](./REFERENCES_UPDATE_REPORT.md) - 引用路径更新报告

<details>
<summary>团队培训记录 (2026年1月已完成)</summary>

#### Claude 培训 (2026 年 1 月 27 日-31 日)

- **第 1 次** (1月28日): Claude Code CLI 基础操作、开发环境搭建、Prompt 基础（鼎中主讲）
- **第 2 次** (1月30日): Skills 开发、MCP 开发（鼎中主讲）
- **持续支持**: 每周二技术答疑

</details>

### 远期展望

- **流程优化**: 基于使用数据优化各阶段的处理效率
- **质量提升**: 增强 AI 模型的准确性和智能化水平
- **功能扩展**: 支持更多类型的测试场景和文档格式
- **集成增强**: 与更多外部工具和平台的深度集成

### 推荐官方插件

| 类别 | 插件 | 说明 |
|------|------|------|
| 插件开发 | plugin-dev | 最全面的开发套件 |
| 代码质量 | pr-review-toolkit | PR 全面审查 |
| 工作流 | commit-commands | 简化 Git 提交流程 |

---

**版本**: v1.2.0 | **更新**: 2026-03-20 | **维护**: WF Bank Test Team
