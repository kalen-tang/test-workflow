# wf_bank_test

## 📊 系统概述

这是一个**测试案例生成与自动化流程系统**，旨在建立一个完整的从需求到测试执行的自动化流水线，大幅提升测试效率和质量。

## 🏗️ 系统架构

📋 **架构文档**: [architecture.puml](./architecture.puml)

### 🖼️ 架构图示

![测试案例生成与自动化流程](https://plantuml.in.za/svg/jLTRJ-D657xthvXILGj1X4rwqJPIAq5GrKf5NQ1zAbNbJGo9IEniueYbrKhX6X8W0R55K5P0e42eLg7RNGfhGlfVsipOUU8lTCPZEsCx0GdKF20yS-PSlZddctFUaoD2N02961yLkTH4L4pmIJuEdl2XYV6ab1R3GIac9S5a92eBp7u2x_FZmeWy5HD0KWZ9l3WUOmN2mXYVZibVIA8y4lr90Bw7pAOeXOMKa02Vi8j9Nfmm5ZavAcEzw6n9E_q5bHRhjINrnIvQNArV5BJixp1VXiiRw6nQBIzndE4Aw825NNYyL5UEOLPHSoSTu6SEu5z8YYSaKH1bKwBnCeDUpw2DB2eTT00-XIrF3WjF1wHGQtcjKjCg9RlyW92AZekjZbGpiBXMlpnGzwPruLGo5CJXjbOD2mkm-2UDq5JzPJGbIyafxZaJshUI54kP0Lch8nFHM7FPOO2DKZkUqvPdWIu_AiBYQIEJ2y3z7PZVmnyOPfGvHWSPj7j8dT31qAN1-_qV1p_jVzJA0eiBQq7N4JO1kbKDoYt1yqEA0QCWpejfFXRaKuAXeUyHqT4-L5ZPKGj_q30OFJYOO4G8JHXQY1TzhVqe7CBYWPLUZ0e-4NNxWA_7TXc3mSTjRY8u-3N0kwCYAgxMQzluamPR_xk4fayTzq6tjBVbHhQedSx1nGNTXL0yDXXAt0G2IJ8m41qROstHF8Jd5LYTmQhGpghp-gzUm_KLV7Lm-oqLeBU7zUZssiFrNLWA-NMZZ3sA8PFzQI8LmbAtUFyuAJsRicdAhyFbUGgHhYb199m-FRTL2Kr2V7SC1-2JefICyp5CGk5lqd8YBQVSnE2cX9Pyu6A2S5iQS1PsnAXgXvnnGSLDvC9_M4X8IPa4U6Ege_mXNClRKfsUj81g0kGcr1OaoTRZgDYfNgwZdJd2jtjLM2rsEOepvSB8ukTcy7nQbgYmFHgKEzPAoxg5bqpqmZCXD2oayFF1SGy-kykFUm3KLw_g5vd6vb-eSdPT_TNnE82Upu5EgfsKH7jnwdMHHNSEtTK5x8FF2zmqZ7Lprei3UiBIf8ZjCfpBiVnhtmS1qFTLTrrHy0t1trRGtaKdob_XHF0__A2BMFHxWPkM3OlMcsKfjPCqv-1ibzIjrZ_q0ZRnqVuRTNM1QxvfbafAPvp1QkQgKIFO33q9LmkiEcBX8ozmSnfdlB5DZobzSIQDiUj6SGG09a3CiLHFDyk3zqmwPTbAEdSoaHHhLyDtJZGtmJ5Pmp9206YrTJX_oDaVnPvaT3mYjnAdxccpLp2_VTzQpDq4IpUjHW8Fop__0oGCTP4ac2ytPii6AiwMmyB5VWPjAHWHof_t0mLkRrkWsDeWGaHs7gN84BgyCoPi52OQJMQs_ck6tUHX4ZKrVi_QU675Qzst8z3hwg9McuVv4mhmTJLtvu1jpOSLLJFG032c2frHEAl3Q2bAMvj6vbAhhN5MHzXQL8VAh1gSYx80daYoBCM1D6PB9lnuUZpipLE7F1wyeU_Hp0pe2-nJyczcckLv_Cao9VvqDnQcIce2RRp3hpbLxEx0RJdUx01eJGfY692ON94vw4EtrexixX9Y-vY8Zgn2TVoJsGV6wyTqqQ2phxU_DzWxq6M8i8x1qtUDgrMe754FJILwjzJ8hgWpx-2bebKgvj63GcFh1A-YlInwKtO2egS4mOEf7-EYdUrEm8I1gDME5jJj3RMGLIztSTZ6gbfL6bldiBZIE5eq7QFZGtKJtudXMDC5gzdh8zEBgxlpU8PyzOiyNCdZGXloUNsum3mUF1NiAcefOzKYJTvHKJVNQZ0ojboPGzUjaOTys2O5lS5xwllHPvi6N0ukOGTxX_oiftxyRRdBjZVrYm9RFDHe-_5NX_gcqHLxvxSDh7Rl_DGxufJVwpVyeQb6qmVxGs-NZ5XLXVN7FQCQUDc7Dx9aJKJK9p_nYPbyz3ywZZtVHwBXi23-GAb8Tz_SzRjtiIBSXVy7)

## 功能描述

#### Skills 组件

| 组件               | 用途                                                               |
| ------------------ | ------------------------------------------------------------------ |
| 需求文档规范 Skill | 用于规范化转化原始需求文档                                         |
| 设计文档规范 Skill | 用于规范化转化原始设计文档                                         |
| 手工案例 Skill     | 用于收集规范化产出物后，生成手工案例                               |
| 接口自动化 Skill   | 用于用产出的手工案例，结合自动化项目产出自动化案例                 |
| 需求实现检查 Skill | 用于检查需求与实现的对齐度，顺便输出风险点、测试建议、文档质量评分 |

#### MCP 组件

| 组件          |
| ------------- | -------------------------------------------------------- |
| CML MCP       | 用来梳理历史案例，以便于转成规范化可参考的历史案例       |
| Udoc2Code MCP | 用于生成与更新接口自动化底层 service 接口代码            |
| Code Diff MCP | 用于比对迭代代码差异，产出差异报告，用于检查开发实现内容 |

## 🔄 流程分析

### 第一阶段：原始产出物规范化

**目标**: 将各种原始文档标准化

- **输入**: 原始需求文档、设计文档、开发代码、历史案例
- **处理工具**:
  - 需求文档规范 Skill (可选增加可测性检查)
  - 设计文档规范 Skill
  - CML MCP (提供历史案例信息，可选案例质量评分)
  - Code Diff MCP (代码差异分析，可选影响范围分析)
- **输出**: 标准化的需求文档、设计文档、历史案例、代码变更分析报告
- **质量保证**: AI+人工复核(抽检 20%)

### 第二阶段：手工案例生成

**目标**: 智能生成结构化测试案例

- **输入**: 全部规范化产出物
- **处理**: 手工案例 Skill 智能生成
- **输出**: 结构化格式的手工测试案例

### 第三阶段：自动化执行

**目标**: 将手工案例转换为自动化案例并执行

- **流程**: 手工案例 → 自动化案例 → 执行结果分析
- **输出**: 执行结果分析，包括：
  - 覆盖率统计
  - 缺陷反馈
  - 案例优化建议

### 第四阶段：辅助工具增强

**目标**: 通过辅助工具提升自动化案例质量和手工案例生成增强

- **核心增强工具**:

  - Udoc2Code MCP: 生成接口代码
  - Proxy MCP: 提供抓包接口逻辑
  - 接口自动化 Skill: 提供执行能力

- **质量增强功能** (后期):
  - 需求实现检查 Skill: 验证需求与实现一致性，为手工案例生成提供质量反馈
    - 输出文档质量评分 (A/B/C/D)
    - 需求实现对齐度检查
    - 测试重点建议和风险点标注
    - 增强手工案例生成的针对性和准确性

## 📅 实施计划

### Q1 上半（Q1.1）- 基础自动化能力 🟦

- 接口自动化 Skill
- 手工案例 Skill
- CML MCP
- Udoc2Code MCP

### Q1 下半/Q2 上半（Q1.2/Q2.1）- 文档规范与案例生成 🟩

- 需求文档规范 Skill
- 设计文档规范 Skill

### Q2 下半（Q2.2）- 质量检查与分析增强 🟨

- 需求实现检查 Skill
- Code Diff MCP
- Proxy MCP

## 🎯 核心价值

1. **标准化流程**: 将原始文档转换为标准化格式，确保信息一致性
2. **智能生成**: AI 驱动的测试案例自动生成，提高案例质量和覆盖度
3. **质量保证**: 多维度的需求实现检查，降低缺陷泄漏风险
4. **自动化执行**: 从手工案例到自动化执行的完整链路，提升执行效率
5. **持续优化**: 基于执行结果的案例优化建议，形成闭环反馈

## ⏰ 开发与投产计划

### 📋 投产时间节点 (基于 2026 年，1 月 27 日后启动)

- **2026 年 4 月投产目标**: 所有 Skills 和 CML、Udoc2Code MCP 上线 (分批投产)
- **2026 年 6 月前**: Code Diff MCP 投产
- **2026 年 Q2 目标**: 功能优化和增强 (6 月底)

### 🚀 全面开发计划 (1 月 27 日后启动)

**开发周期**:

- **Skills+CML/Udoc2Code MCP**: 2026 年 2 月-4 月 (2 个月)
- **Code Diff MCP**: 2026 年 2 月-6 月 (4 个月)

#### ⏰ 时间投入分析

- **培训期**: 1 月 27 日-31 日 (5 天紧急培训)
- **春节假期**: 2 月 16 日-28 日 (13 天)
- **额外休假**: 人均 3 天
- **工作日计算**:
  - 2 月工作日: 10 天 (去除春节假期和周末)
  - 3 月工作日: 22 天
  - 4 月工作日: 22 天
  - 5 月前半月工作日: 11 天
  - 总计: 65 个工作日
- **重要约束**: 所有参与者为测试工程师，项目投入仅占总时间 10%
- **实际可投入**: 每人约 6.5 个工作日 (65 天 ×10%)

#### Skills 组件

| 组件               | 负责人 | 实际投入     | 开发周期 | 投产时间   | 复核人 |
| ------------------ | ------ | ------------ | -------- | ---------- | ------ |
| 手工案例 Skill     | 宇宸   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 | 陈贝   |
| 需求文档规范 Skill | 陈贝   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 | 泉政   |
| 设计文档规范 Skill | 陈贝   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 | 泉政   |
| 接口自动化 Skill   | 泉政   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 | 奕翔   |
| 需求实现检查 Skill | 宇豪   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 | 慧芳   |

_注：泉政负责接口自动化 Skill 的开发和 CML MCP 开发，同时复核需求和设计文档规范 Skills_
_需求实现检查 Skill 作为第四阶段增强功能，用于进一步提升手工案例生成质量_
_实际投入：按 2 个月工作日约 44 天计算（去除周末），项目投入约 4.4 天(10%)_

#### MCP 组件

| 组件          | 负责人 | 实际投入     | 开发周期 | 投产时间   |
| ------------- | ------ | ------------ | -------- | ---------- |
| CML MCP       | 泉政   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 |
| Udoc2Code MCP | 鼎中   | 4.4 天 (10%) | 2 个月   | 4 月 10 日 |
| Code Diff MCP | 奕翔   | 8.8 天 (10%) | 4 个月   | 6 月 15 日 |

_实际投入：按开发周期工作日计算（去除周末），项目投入占总时间 10%_
_CML、Udoc2Code MCP: 2 个月约 44 个工作日，投入 4.4 天_
_Code Diff MCP: 4 个月约 88 个工作日，投入 8.8 天_

### 🎯 调整后开发策略 (1 月 27 日启动)

**2 月上半月 (2 月 1-15 日)**:

- **正式启动**: 基于 1 月底紧急培训，正式进入开发阶段
- **MCP 组开发**: 泉政(CML)、鼎中(Udoc2Code)、奕翔(Code Diff)启动 MCP 开发
- **Skills 设计**: 陈贝、宇宸进行 Skills 设计和架构准备

**春节假期 (2 月 16-28 日)**:

- **弹性安排**: 部分人员可选择性进行设计工作
- **远程协调**: 维持必要的技术沟通

**3 月冲刺 (3 月 1-31 日)**:

- **全面并行**: 所有组件进入开发高峰期
- **每周 Review**: 定期进度 Review，加强进度管控
- **技术支持**: 鼎中为 Skills 开发提供技术指导

**4 月投产冲刺 (4 月 1-30 日)**:

- **集成测试**: 组件间集成和系统测试
- **分批投产**: 按完成度分批上线
- **4 月 10 日**: 文档规范 Skills 投产 (陈贝负责开发，泉政负责复核)
- **4 月 15 日**: CML MCP 投产 (泉政负责)
- **4 月 20 日**: 手工案例、接口自动化 Skills 投产 (宇宸、泉政负责)
- **4 月 20 日**: Udoc2Code MCP 投产 (鼎中负责)

**Code Diff MCP 延期开发**:

- **4-6 月**: 奕翔继续 Code Diff MCP 开发 (技术复杂度最高)
- **6 月 15 日**: Code Diff MCP 最终投产

### 📈 Q2 优化阶段

**Q2 (4-6 月)**: 功能增强和用户反馈优化

## 🔮 远期展望

### 质量增强阶段 (后期规划)

**需求实现检查 Skill** 作为系统增强功能，在核心流程稳定运行后开发：

**主要价值**:

- **文档质量评估**: 为需求文档和设计文档提供 A/B/C/D 评分
- **实现一致性检查**: 验证需求与代码实现的对齐度
- **测试重点识别**: 智能标注高风险点和测试重点
- **案例生成增强**: 基于质量反馈优化手工案例的针对性和准确性

**集成方式**:

- 与手工案例生成形成反馈循环，持续提升案例质量
- 为测试人员提供更精准的测试指导
- 建立从需求到测试的完整质量追溯链条

**开发时机**: 在核心 4 个 Skills 和主要 MCPs 稳定运行，团队积累足够经验后启动

## 📚 Claude 培训计划 (开发前必修)

### 🎯 1 月底 Claude 培训 (2026 年 1 月 27 日-31 日启动)

**培训周安排**:

- **1 月 27 日**: 准备工作，环境检查和材料准备
- **1 月 28 日**: 第 1 次培训会话 (1.5 小时)
- **1 月 29 日**: 自主学习和实践时间
- **1 月 30 日**: 第 2 次培训会话 (1.5 小时)
- **1 月 31 日**: 培训总结和开发准备

#### 第 1 次培训会话 (1.5 小时) - Claude 基础能力

**时间**: 1 月 28 日下午 14:00-15:30 (鼎中主讲)
**参与者**: 全员

**培训内容**:

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

#### 第 2 次培训会话 (1.5 小时) - Skills 与 MCP 开发

**时间**: 1 月 30 日下午 14:00-15:30 (鼎中主讲)
**参与者**: 全员

**培训内容**:

- **Claude Skills 开发** (45 分钟)

  - Skills 框架原理和架构
  - 业务逻辑到 AI 逻辑转换
  - Skill 创建、测试和部署流程

- **Claude MCP 开发** (45 分钟)
  - MCP 框架和通信机制
  - 外部系统集成方法
  - Claude API 使用和集成实践

### 📋 培训目标

**必达标准**:

- 熟练使用 Claude Code CLI 进行开发
- 掌握 Claude Prompt 工程基础
- 了解 Skills 和 MCP 开发流程
- 能够独立搭建开发环境

### 🚀 培训后支持 (2 月开始)

**持续指导** (鼎中提供):

- **每周二**: 技术答疑会 (1 小时)
- **问题升级**: 重大技术问题即时支持
- **Code Diff MCP 专项**: 4-6 月期间为奕翔提供深度技术指导

## 🤝 协作机制

### 项目管理

- **每周例会**: 嘉龙主持，同步进度和解决问题
- **技术评审**: 鼎中主导技术架构组评审
- **跨组协调**: 鼎中负责技术架构统一性
- **组件集成**: 鼎中负责 MCP 组件间技术集成和 Skills 业务逻辑集成

### 培训与支持

- **培训答疑**: 鼎中每周二答疑时间，解决开发中的技术问题
- **技术架构组指导**: 鼎中负责 MCP 开发指导和技术攻关

### 质量保证

- **代码 Review**: 鼎中负责技术架构组 Review
- **集成测试**: 每个里程碑节点进行集成测试，鼎中负责技术架构验证
- **进度把控**: 嘉龙负责整体项目统筹，确保 4 月中旬分批投产
- **质量审核**: 嘉龙负责项目整体质量审核和验收
- **假期协调**: 春节期间保持必要的远程协作和进度跟踪

## 🚀 预期效果

- **效率提升**: 测试案例生成效率提升 80%以上
- **质量保证**: 需求覆盖率达到 95%以上
- **风险控制**: 提前识别并标注测试重点和风险点
- **成本降低**: 减少人工重复性工作，释放测试人员创造力
