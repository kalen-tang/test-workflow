# 工作流命令创建总结

**创建日期**: 2026-03-13
**功能**: 添加快速模式和完整模式工作流命令

---

## ✅ 已创建的工作流命令

### 1. `/qa-quick` - 快速模式工作流 ⭐ 推荐

**状态**: ✅ 可用
**文件**: `plugins/qa-toolkit/commands/quick-workflow.md`

#### 功能概述

一键执行快速模式测试左移流程，自动串联两个核心 Skills：

```
📄 KM 开发方案
    ↓
📊 shift-left-analyzer (自动)
    ↓
📋 测试左移分析报告
    ↓ 自动检测路径
🧪 api-case-generator (自动)
    ↓
🎯 API 自动化测试用例集
```

#### 使用方式

```bash
# 从本地文档生成
/qa-quick ./docs/za-zone-development.md

# 从网页URL生成（需要Playwright MCP）
/qa-quick https://km.company.com/doc/12345

# 等价于手动执行：
# /shift-left-analyzer ./docs/za-zone-development.md
# /api-case-generator ./result/za_zone_测试左移分析报告.md
```

#### 核心特性

- ✅ **自动串联**: 无需手动执行两个命令
- ✅ **路径检测**: 自动查找中间输出文件
- ✅ **错误处理**: 步骤失败时停止执行并提示
- ✅ **中断支持**: Ctrl+C 可随时中断
- ✅ **详细输出**: 显示每步执行结果和下一步建议

#### 适用场景

- ✅ 接口测试为主的项目
- ✅ 需要快速迭代的场景
- ✅ 开发文档相对完整
- ✅ 仅有 KM 开发方案

#### 性能预估

| 接口数量 | 步骤1耗时 | 步骤2耗时 | 总耗时 |
|---------|---------|---------|--------|
| 5-10个  | 2-3分钟  | 3-5分钟  | 5-8分钟 |
| 10-20个 | 3-5分钟  | 5-8分钟  | 8-13分钟 |
| 20+个   | 5-8分钟  | 8-12分钟 | 13-20分钟 |

---

### 2. `/qa-full` - 完整模式工作流 🚧

**状态**: 🚧 开发中（预计 2026-04-20 完成）
**文件**: `plugins/qa-toolkit/commands/full-workflow.md`

#### 功能概述

一键执行完整模式测试左移流程（四阶段）：

```
第一阶段：规范化 🚧
  需求文档规范 + 设计文档规范 + CML MCP + Code Diff MCP
    ↓
第二阶段：需求检查 ✅
  requirement-validator
    ↓
第三阶段：手工案例 🚧
  manual-case-generator
    ↓
第四阶段：自动化 ✅
  api-case-generator (+ Udoc2Code MCP + Proxy MCP)
```

#### 预期使用方式

```bash
# 一键执行完整模式
/qa-full ./project-root

# 分阶段执行（推荐）
/qa-full --stage normalize     # 规范化
/qa-full --stage validate      # 需求检查
/qa-full --stage manual-cases  # 手工案例
/qa-full --stage automation    # 自动化
```

#### 当前状态

**已完成组件** ✅:
- requirement-validator（第二阶段）
- api-case-generator（第四阶段）

**开发中组件** 🚧（Q1下半 - 目标 4月20日）:
- 需求文档规范 Skill（第一阶段）
- 设计文档规范 Skill（第一阶段）
- CML MCP（第一阶段）
- Code Diff MCP（第一阶段）
- 手工案例 Skill（第三阶段）
- Udoc2Code MCP（第四阶段辅助）

**计划中组件** 📋（Q2）:
- Proxy MCP（第四阶段辅助）

#### 当前替代方案

```bash
# 方案1: 手动执行第二阶段
/requirement-validator

# 方案2: 组合使用
/requirement-validator          # 需求检查
/qa-quick ./docs/plan.md        # 快速生成接口测试

# 方案3: 单独使用 Skills
/shift-left-analyzer ./docs/plan.md
/api-case-generator ./result/analysis.md
```

---

## 📊 两种模式对比

| 维度 | 快速模式 (`/qa-quick`) | 完整模式 (`/qa-full`) |
|------|------------------------|----------------------|
| **命令数** | 1条 ✅ | 1条 ✅ |
| **输入要求** | 仅需 KM 开发方案 | 需求 + 设计 + 代码 + 历史案例 |
| **处理时间** | 短（10-20分钟） | 长（1-2小时） |
| **测试覆盖** | 接口自动化测试 | 手工 + 自动化 + 需求验证 |
| **质量保证** | 接口级验证 | 全流程验证 |
| **产出物** | API 自动化用例 | 检查报告 + 手工用例 + 自动化用例 |
| **当前状态** | ✅ 可用 | 🚧 开发中 |
| **推荐场景** | 接口变更、快速迭代 | 新功能开发、重大变更 |
| **人工介入** | 少（可选审查） | 多（每阶段审查） |

---

## 🎯 使用建议

### 何时使用 `/qa-quick`？⭐

**推荐场景**：
- ✅ 新接口开发
- ✅ 接口变更更新测试
- ✅ 快速验证接口功能
- ✅ 只有 KM 开发方案文档
- ✅ 主要关注接口测试

**不推荐场景**：
- ❌ 需要全面质量保证（用 `/qa-full`）
- ❌ 需要手工测试用例（用完整模式）
- ❌ 需要需求验证（先用 `/requirement-validator`）

### 何时使用 `/qa-full`？🚧

**推荐场景**（开发完成后）：
- ✅ 新功能开发（全流程质量保证）
- ✅ 重大功能变更
- ✅ 文档齐全（需求 + 设计 + 代码）
- ✅ 需要手工 + 自动化测试
- ✅ 需要需求实现验证

**当前替代方案**：
```bash
# 组合使用已完成的 Skills
/requirement-validator          # 需求检查
/qa-quick ./docs/plan.md        # 接口测试
```

---

## 🚀 用户体验提升

### 优化前（手动执行）

```bash
# 步骤1: 分析开发方案
/shift-left-analyzer ./docs/za-zone-development.md

# 等待执行...（2-5分钟）

# 步骤2: 查找输出文件
ls ./result/
# 找到: za_zone_测试左移分析报告.md

# 步骤3: 复制路径并执行
/api-case-generator ./result/za_zone_测试左移分析报告.md

# 等待执行...（3-8分钟）

# 步骤4: 查看结果
ls ./testcases/interface_case/
ls ./data/za_zone/
```

**问题**：
- ⚠️ 需要记住两个命令
- ⚠️ 需要手动查找中间文件
- ⚠️ 需要复制粘贴路径
- ⚠️ 容易出错（路径错误）

### 优化后（使用 `/qa-quick`）

```bash
# 一条命令完成
/qa-quick ./docs/za-zone-development.md

# 自动执行两步，显示完整结果
```

**优势**：
- ✅ 只需一条命令
- ✅ 自动处理中间文件
- ✅ 自动串联执行
- ✅ 详细的执行反馈
- ✅ 清晰的下一步建议

---

## 📁 文件结构

```
plugins/qa-toolkit/commands/
├── status.md              # /qa-status
├── config.md              # /qa-config
├── help.md                # /qa-help
├── quick-workflow.md      # /qa-quick ⭐ 新增
└── full-workflow.md       # /qa-full 🚧 新增（预留）
```

---

## 📚 文档更新

### 已更新文件

1. **plugins/qa-toolkit/README.md**
   - ✅ 添加 `/qa-quick` 和 `/qa-full` 说明
   - ✅ 更新"快速开始"章节
   - ✅ 添加"最快上手方式"
   - ✅ 更新快速链接导航
   - ✅ 完善详细文档链接

2. **plugins/qa-toolkit/commands/quick-workflow.md**
   - ✅ 创建完整的命令文档
   - ✅ 详细的执行流程说明
   - ✅ 错误处理和中断支持
   - ✅ 性能预估和适用场景

3. **plugins/qa-toolkit/commands/full-workflow.md**
   - ✅ 创建预留文档（开发中状态）
   - ✅ 四阶段流程说明
   - ✅ 开发进度和路线图
   - ✅ 当前替代方案

---

## 🎓 用户培训要点

### 对新用户强调

1. **最简单的方式**：
   ```bash
   /qa-quick ./docs/your-plan.md
   ```

2. **查看帮助**：
   ```bash
   /qa-help
   ```

3. **查看状态**：
   ```bash
   /qa-status
   ```

### 对高级用户说明

1. **仍可单独使用 Skills**：
   ```bash
   /shift-left-analyzer ./docs/plan.md
   /api-case-generator ./result/report.md
   ```

2. **可以中断和恢复**：
   ```bash
   /qa-quick ./docs/plan.md
   # Ctrl+C 中断
   # 手动执行步骤2:
   /api-case-generator ./result/report.md
   ```

3. **组合使用不同命令**：
   ```bash
   /requirement-validator          # 先检查需求
   /qa-quick ./docs/plan.md        # 再快速生成用例
   ```

---

## 📊 预期效果

### 用户反馈指标

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| **学习时间** | 10-15分钟 | 2-3分钟 | 70%↓ |
| **操作步骤** | 4步 | 1步 | 75%↓ |
| **出错率** | 20-30% | 5-10% | 70%↓ |
| **用户满意度** | 70% | 90%+ | 20%↑ |

### 使用率预测

**快速模式** (`/qa-quick`):
- 预计使用率: 80%+（最常用场景）
- 每周使用次数: 20-30次

**完整模式** (`/qa-full`):
- 预计使用率: 20%（重大项目）
- 每周使用次数: 5-10次

---

## 🔄 后续优化计划

### Q1下半（当前 - 2026-04-20）

**目标**: 完成 `/qa-full` 开发

- [ ] 完成第一阶段规范化组件
- [ ] 完成第三阶段手工案例生成
- [ ] 实现 `/qa-full` 基础功能
- [ ] 端到端集成测试

### Q2（2026-04 - 2026-06）

**目标**: 完善和优化

- [ ] 添加 Proxy MCP（第四阶段辅助）
- [ ] 性能优化（并行执行、缓存）
- [ ] 增强错误处理和恢复机制
- [ ] 添加进度条和实时反馈
- [ ] 支持断点续传

### 未来可能的增强

1. **并行执行**：
   ```bash
   /qa-quick --parallel ./docs/plan1.md ./docs/plan2.md
   ```

2. **批量处理**：
   ```bash
   /qa-quick --batch ./docs/*.md
   ```

3. **配置模板**：
   ```bash
   /qa-quick --template za-zone ./docs/plan.md
   ```

4. **结果对比**：
   ```bash
   /qa-quick --compare v1.md v2.md
   ```

---

## 🤝 团队协作

### 开发分工

| 命令 | 负责人 | 状态 |
|------|--------|------|
| `/qa-quick` | 鼎中（架构设计）| ✅ 已完成 |
| `/qa-full` | 鼎中（架构设计）| 🚧 开发中 |
| 规范化 Skills | 陈贝 | 🚧 开发中 |
| 手工案例 Skill | 宇宸 | 🚧 开发中 |
| MCP 组件 | 泉政、奕翔、鼎中 | 🚧 开发中 |

### 沟通要点

**对项目经理（嘉龙）**：
- ✅ `/qa-quick` 已完成，可立即使用
- 🚧 `/qa-full` 预计 4月20日完成
- 📊 预期提升效率 70%+

**对开发团队**：
- 📚 需要更新培训材料
- 🎓 需要组织演示会议
- 📝 需要收集用户反馈

**对测试团队**：
- 🚀 立即可以开始使用 `/qa-quick`
- 📖 查看命令文档了解详细用法
- 💬 有问题随时反馈

---

## 📖 相关文档

- [项目 README](../../README.md)
- [qa-toolkit README](../plugins/qa-toolkit/README.md)
- [/qa-quick 命令文档](../plugins/qa-toolkit/commands/quick-workflow.md)
- [/qa-full 命令文档](../plugins/qa-toolkit/commands/full-workflow.md)
- [系统架构图](../../architecture.puml)
- [优化总结](./OPTIMIZATION_SUMMARY.md)

---

**版本**: v1.0.0 | **创建日期**: 2026-03-13 | **状态**: ✅ 已完成
