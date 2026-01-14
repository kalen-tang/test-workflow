# wf_bank_test

## 📊 系统概述

这是一个**测试案例生成与自动化流程系统**，旨在建立一个完整的从需求到测试执行的自动化流水线，大幅提升测试效率和质量。

## 🏗️ 系统架构

📋 **架构文档**: [architecture.puml](./architecture.puml)

### 🖼️ 架构图示
![测试案例生成与自动化流程](https://plantuml.in.za/svg/jLTRJ-D657xthvXILGj1X4rwqJPIAq5GrKf5NQ1zAbNbJGo9IEniueYbrKhX6X8W0R55K5P0e42eLg7RNGfhGlfVsipOUU8lTCPZEsCx0GdKF20yS-PSlZddctFUaoD2N02961yLkTH4L4pmIJuEdl2XYV6ab1R3GIac9S5a92eBp7u2x_FZmeWy5HD0KWZ9l3WUOmN2mXYVZibVIA8y4lr90Bw7pAOeXOMKa02Vi8j9Nfmm5ZavAcEzw6n9E_q5bHRhjINrnIvQNArV5BJixp1VXiiRw6nQBIzndE4Aw825NNYyL5UEOLPHSoSTu6SEu5z8YYSaKH1bKwBnCeDUpw2DB2eTT00-XIrF3WjF1wHGQtcjKjCg9RlyW92AZekjZbGpiBXMlpnGzwPruLGo5CJXjbOD2mkm-2UDq5JzPJGbIyafxZaJshUI54kP0Lch8nFHM7FPOO2DKZkUqvPdWIu_AiBYQIEJ2y3z7PZVmnyOPfGvHWSPj7j8dT31qAN1-_qV1p_jVzJA0eiBQq7N4JO1kbKDoYt1yqEA0QCWpejfFXRaKuAXeUyHqT4-L5ZPKGj_q30OFJYOO4G8JHXQY1TzhVqe7CBYWPLUZ0e-4NNxWA_7TXc3mSTjRY8u-3N0kwCYAgxMQzluamPR_xk4fayTzq6tjBVbHhQedSx1nGNTXL0yDXXAt0G2IJ8m41qROstHF8Jd5LYTmQhGpghp-gzUm_KLV7Lm-oqLeBU7zUZssiFrNLWA-NMZZ3sA8PFzQI8LmbAtUFyuAJsRicdAhyFbUGgHhYb199m-FRTL2Kr2V7SC1-2JefICyp5CGk5lqd8YBQVSnE2cX9Pyu6A2S5iQS1PsnAXgXvnnGSLDvC9_M4X8IPa4U6Ege_mXNClRKfsUj81g0kGcr1OaoTRZgDYfNgwZdJd2jtjLM2rsEOepvSB8ukTcy7nQbgYmFHgKEzPAoxg5bqpqmZCXD2oayFF1SGy-kykFUm3KLw_g5vd6vb-eSdPT_TNnE82Upu5EgfsKH7jnwdMHHNSEtTK5x8FF2zmqZ7Lprei3UiBIf8ZjCfpBiVnhtmS1qFTLTrrHy0t1trRGtaKdob_XHF0__A2BMFHxWPkM3OlMcsKfjPCqv-1ibzIjrZ_q0ZRnqVuRTNM1QxvfbafAPvp1QkQgKIFO33q9LmkiEcBX8ozmSnfdlB5DZobzSIQDiUj6SGG09a3CiLHFDyk3zqmwPTbAEdSoaHHhLyDtJZGtmJ5Pmp9206YrTJX_oDaVnPvaT3mYjnAdxccpLp2_VTzQpDq4IpUjHW8Fop__0oGCTP4ac2ytPii6AiwMmyB5VWPjAHWHof_t0mLkRrkWsDeWGaHs7gN84BgyCoPi52OQJMQs_ck6tUHX4ZKrVi_QU675Qzst8z3hwg9McuVv4mhmTJLtvu1jpOSLLJFG032c2frHEAl3Q2bAMvj6vbAhhN5MHzXQL8VAh1gSYx80daYoBCM1D6PB9lnuUZpipLE7F1wyeU_Hp0pe2-nJyczcckLv_Cao9VvqDnQcIce2RRp3hpbLxEx0RJdUx01eJGfY692ON94vw4EtrexixX9Y-vY8Zgn2TVoJsGV6wyTqqQ2phxU_DzWxq6M8i8x1qtUDgrMe754FJILwjzJ8hgWpx-2bebKgvj63GcFh1A-YlInwKtO2egS4mOEf7-EYdUrEm8I1gDME5jJj3RMGLIztSTZ6gbfL6bldiBZIE5eq7QFZGtKJtudXMDC5gzdh8zEBgxlpU8PyzOiyNCdZGXloUNsum3mUF1NiAcefOzKYJTvHKJVNQZ0ojboPGzUjaOTys2O5lS5xwllHPvi6N0ukOGTxX_oiftxyRRdBjZVrYm9RFDHe-_5NX_gcqHLxvxSDh7Rl_DGxufJVwpVyeQb6qmVxGs-NZ5XLXVN7FQCQUDc7Dx9aJKJK9p_nYPbyz3ywZZtVHwBXi23-GAb8Tz_SzRjtiIBSXVy7)

## 🔄 流程分析

### 第一阶段：原始产出物规范化
**目标**: 将各种原始文档标准化

- **输入**: 原始需求文档、设计文档、开发代码、历史案例
- **处理工具**:
  - 需求文档规范Skill (可选增加可测性检查)
  - 设计文档规范 Skill
  - CML MCP (提供历史案例信息，可选案例质量评分)
  - Code Diff MCP (代码差异分析，可选影响范围分析)
- **输出**: 标准化的需求文档、设计文档、历史案例、代码变更分析报告
- **质量保证**: AI+人工复核(抽检20%)

### 第二阶段：需求实现检查
**目标**: 验证需求与实现的一致性

- **输入**: 所有规范化产出物
- **处理**: 需求实现检查 Skill
- **输出**: 需求实现检查报告，包括：
  - 文档质量评分 (A/B/C/D)
  - 需求实现对齐度检查
  - 测试重点建议
  - 风险点标注

### 第三阶段：手工案例生成
**目标**: 智能生成结构化测试案例

- **输入**: 全部规范化产出物
- **处理**: 手工案例 Skill 智能生成
- **输出**: 结构化格式的手工测试案例

### 第四阶段：自动化执行
**目标**: 将手工案例转换为自动化案例并执行

- **流程**: 手工案例 → 自动化案例 → 执行结果分析
- **输出**: 执行结果分析，包括：
  - 覆盖率统计
  - 缺陷反馈
  - 案例优化建议

### 第五阶段：辅助工具增强
**目标**: 通过辅助工具提升自动化案例质量

- **工具**:
  - Udoc2Code MCP: 生成接口代码
  - Proxy MCP: 提供抓包接口逻辑
  - 接口自动化 Skill: 提供执行能力

## 📅 实施计划

### Q1上半（Q1.1）- 基础自动化能力 🟦
- 接口自动化 Skill
- 手工案例 Skill
- CML MCP
- Udoc2Code MCP

### Q1下半/Q2上半（Q1.2/Q2.1）- 文档规范与案例生成 🟩
- 需求文档规范 Skill
- 设计文档规范 Skill

### Q2下半（Q2.2）- 质量检查与分析增强 🟨
- 需求实现检查 Skill
- Code Diff MCP
- Proxy MCP

## 🎯 核心价值

1. **标准化流程**: 将原始文档转换为标准化格式，确保信息一致性
2. **智能生成**: AI驱动的测试案例自动生成，提高案例质量和覆盖度
3. **质量保证**: 多维度的需求实现检查，降低缺陷泄漏风险
4. **自动化执行**: 从手工案例到自动化执行的完整链路，提升执行效率
5. **持续优化**: 基于执行结果的案例优化建议，形成闭环反馈

## 🛠️ 技术栈

### Skills (AI能力模块)
- 需求文档规范 Skill
- 设计文档规范 Skill
- 手工案例 Skill
- 需求实现检查 Skill
- 接口自动化 Skill

### MCP (外部工具集成)
- CML MCP: 案例管理与质量评分
- Code Diff MCP: 代码差异与影响分析
- Udoc2Code MCP: 接口代码生成
- Proxy MCP: 接口抓包与逻辑分析



## ⏰ 开发与投产计划

### 📋 投产时间节点 (基于2026年，1月27日后启动)
- **2026年4月投产目标**: 所有Skills和CML、Udoc2Code MCP上线 (分批投产)
- **2026年6月前**: Code Diff MCP投产
- **2026年Q2目标**: 功能优化和增强 (6月底)

### 🚀 全面开发计划 (1月27日后启动)
**开发周期**:
- **Skills+CML/Udoc2Code MCP**: 2026年2月-4月 (2个月)
- **Code Diff MCP**: 2026年2月-6月 (4个月)
- **1月底**: 紧急培训期

#### ⏰ 时间投入分析
- **培训期**: 1月27日-31日 (5天紧急培训)
- **春节假期**: 2月16日-28日 (13天)
- **额外休假**: 人均3天
- **工作日计算**:
  - 2月工作日: 约11天 (去除春节假期和周末)
  - 3月工作日: 约22天
  - 4月工作日: 约22天
  - 5月前半月工作日: 约11天
  - 总计: 约55-66个工作日
- **重要约束**: 所有参与者为测试工程师，项目投入仅占总时间10%
- **实际可投入**: 每人约5.5-6.6个工作日

#### Skills 组件
| 组件 | 负责人 | 实际投入 | 开发周期 | 投产时间 | 复核人 |
|------|--------|----------|----------|----------|--------|
| 手工案例 Skill | 宇宸 | 4.4天 (10%) | 2个月 | 4月20日 | 陈贝 |
| 需求实现检查 Skill | 宇豪 | 4.4天 (10%) | 2个月 | 4月20日 | 慧芳 |
| 需求文档规范 Skill | 陈贝 | 4.4天 (10%) | 2个月 | 4月10日 | 泉政 |
| 设计文档规范 Skill | 陈贝 | 4.4天 (10%) | 2个月 | 4月10日 | 泉政 |
| 接口自动化 Skill | 泉政 | 4.4天 (10%) | 2个月 | 4月20日 | 奕翔 |

*注：慧芳仅参与需求实现检查Skill的复核工作，不参与任何开发*
*泉政负责接口自动化Skill的开发，同时复核需求和设计文档规范Skills*
*实际投入：按2个月工作日约44天计算（去除周末），项目投入约4.4天(10%)*

#### MCP 组件 (技术组)
| 组件 | 负责人 | 实际投入 | 开发周期 | 投产时间 |
|------|--------|----------|----------|----------|
| CML MCP | 泉政 | 4.4天 (10%) | 2个月 | 4月15日 |
| Udoc2Code MCP | 鼎中 | 4.4天 (10%) | 2个月 | 4月20日 |
| Code Diff MCP | 奕翔 | 8.8天 (10%) | 4个月 | 6月15日 |

*实际投入：按开发周期工作日计算（去除周末），项目投入占总时间10%*
*CML、Udoc2Code MCP: 2个月约44个工作日，投入4.4天*
*Code Diff MCP: 4个月约88个工作日，投入8.8天*

### 🎯 调整后开发策略 (1月27日启动)
**2月上半月 (2月1-15日)**:
- **正式启动**: 基于1月底紧急培训，正式进入开发阶段
- **MCP组开发**: 泉政(CML)、鼎中(Udoc2Code)、奕翔(Code Diff)启动MCP开发
- **Skills设计**: 陈贝、宇宸进行Skills设计和架构准备
- **慧芳**: 制定Skills质量标准和Review流程
- **宇豪**: 专注接口自动化Skill开发
- **泉政跨组**: 同时协助文档规范类Skills的技术架构设计

**春节假期 (2月16-28日)**:
- **弹性安排**: 部分人员可选择性进行设计工作
- **远程协调**: 维持必要的技术沟通

**3月冲刺 (3月1-31日)**:
- **全面并行**: 所有组件进入开发高峰期
- **每周Review**: 慧芳主导Skills质量Review，加强进度管控
- **技术支持**: 鼎中为Skills开发提供技术指导

**4月投产冲刺 (4月1-30日)**:
- **集成测试**: 组件间集成和系统测试
- **分批投产**: 按完成度分批上线
- **4月10日**: 文档规范Skills投产 (陈贝、宇宸主导，泉政协助，慧芳验收)
- **4月15日**: CML MCP投产 (泉政负责)
- **4月20日**: 核心Skills和Udoc2Code MCP投产 (陈贝、宇宸、鼎中负责，慧芳验收)

**Code Diff MCP延期开发**:
- **4-6月**: 奕翔继续Code Diff MCP开发 (技术复杂度最高)
- **6月15日**: Code Diff MCP最终投产

### 📈 Q2优化阶段
**Q2 (4-6月)**: 功能增强和用户反馈优化

## 📚 Claude培训计划 (开发前必修)

### 🎯 1月底Claude培训 (2026年1月27日-31日启动)

#### 第1次培训会话 (1.5小时) - Claude基础能力
**时间**: 1月28日下午14:00-15:30 (鼎中主讲)
**参与者**: 全员

**培训内容**:
- **Claude Code CLI基础操作** (30分钟)
  - 基本命令和工作流
  - 项目初始化和管理
  - 代码生成和编辑能力

- **Claude开发环境搭建** (30分钟)
  - VS Code + Claude扩展安装配置
  - API密钥设置和认证
  - 开发工具链集成

- **Claude对话与Prompt基础** (30分钟)
  - 有效Prompt编写技巧
  - Claude能力边界和最佳实践
  - 调试和问题排查方法

#### 第2次培训会话 (1.5小时) - Skills与MCP开发
**时间**: 1月30日下午14:00-15:30 (鼎中主讲)
**参与者**: 全员

**培训内容**:
- **Claude Skills开发** (45分钟)
  - Skills框架原理和架构
  - 业务逻辑到AI逻辑转换
  - Skill创建、测试和部署流程

- **Claude MCP开发** (45分钟)
  - MCP框架和通信机制
  - 外部系统集成方法
  - Claude API使用和集成实践

### 📋 培训目标
**必达标准**:
- 熟练使用Claude Code CLI进行开发
- 掌握Claude Prompt工程基础
- 了解Skills和MCP开发流程
- 能够独立搭建开发环境

### 🚀 培训后支持 (2月开始)
**持续指导** (鼎中提供):
- **每周二**: 技术答疑会 (1小时)
- **问题升级**: 重大技术问题即时支持
- **Code Diff MCP专项**: 4-6月期间为奕翔提供深度技术指导

## 🤝 协作机制

### 项目管理
- **每周例会**: 嘉龙主持，同步进度和解决问题
- **技术评审**: 鼎中主导技术架构组评审
- **跨组协调**: 鼎中负责技术架构统一性
- **组件集成**: 鼎中负责MCP组件间技术集成和Skills业务逻辑集成

### 培训与支持
- **培训答疑**: 鼎中每周二答疑时间，解决开发中的技术问题
- **技术架构组指导**: 鼎中负责MCP开发指导和技术攻关

### 质量保证
- **代码Review**: 鼎中负责技术架构组Review
- **集成测试**: 每个里程碑节点进行集成测试，鼎中负责技术架构验证
- **进度把控**: 嘉龙负责整体项目统筹，确保4月中旬分批投产
- **质量审核**: 嘉龙负责项目整体质量审核和验收
- **假期协调**: 春节期间保持必要的远程协作和进度跟踪

## 🚀 预期效果

- **效率提升**: 测试案例生成效率提升80%以上
- **质量保证**: 需求覆盖率达到95%以上
- **风险控制**: 提前识别并标注测试重点和风险点
- **成本降低**: 减少人工重复性工作，释放测试人员创造力