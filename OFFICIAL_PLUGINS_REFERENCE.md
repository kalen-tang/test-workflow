# Claude 官方插件完整参考

## 📊 统计概览

**官方插件总数**: 15个
- **Skills**: 15个
- **Agents**: 17个
- **Commands**: 18个

---

## 🔧 开发工具类

### 1. plugin-dev ⭐⭐⭐ 最全面的开发套件

**Skills (7个)**:
- `agent-development` - Agent 开发指南（文档和最佳实践）
- `skill-development` - Skill 开发指南
- `command-development` - Command 开发指南
- `hook-development` - Hook 开发指南
- `mcp-integration` - MCP 集成指南
- `plugin-settings` - 插件设置指南
- `plugin-structure` - 插件结构指南

**Agents (3个)**:
- `agent-creator` - **自动创建 Agent** ⭐
- `skill-reviewer` - 审查 Skill 质量
- `plugin-validator` - 验证插件配置

**Commands (1个)**:
- `create-plugin` - 创建新插件

**推荐用途**: 学习插件开发、创建 Agent、审查代码

---

### 2. skill-creator ⭐⭐ Skill 专用工具

**Skills (1个)**:
- `skill-creator` - 创建、优化、测试 Skills

**推荐用途**: 创建和优化 Skills、运行性能测试

---

### 3. agent-sdk-dev - Agent SDK 开发

**Agents (2个)**:
- `agent-sdk-verifier-py` - Python SDK 验证
- `agent-sdk-verifier-ts` - TypeScript SDK 验证

**Commands (1个)**:
- `new-sdk-app` - 创建新的 SDK 应用

**推荐用途**: 开发 Claude Agent SDK 应用

---

### 4. example-plugin - 示例插件

**Skills (1个)**:
- `example-skill` - 示例 Skill

**Commands (1个)**:
- `example-command` - 示例命令

**推荐用途**: 学习插件开发的参考模板

---

## 🎨 功能增强类

### 5. feature-dev ⭐⭐ 功能开发助手

**Agents (3个)**:
- `code-architect` - 代码架构师（设计方案）
- `code-explorer` - 代码探索器（理解代码库）
- `code-reviewer` - 代码审查器

**Commands (1个)**:
- `feature-dev` - 启动功能开发流程

**推荐用途**: 开发新功能时的全流程辅助

---

### 6. pr-review-toolkit ⭐⭐ PR 审查工具集

**Agents (6个)**:
- `code-reviewer` - 代码审查
- `code-simplifier` - 代码简化建议
- `comment-analyzer` - 注释分析
- `pr-test-analyzer` - 测试分析
- `silent-failure-hunter` - 静默失败检测
- `type-design-analyzer` - 类型设计分析

**Commands (1个)**:
- `review-pr` - 审查 PR

**推荐用途**: Pull Request 全面审查

---

### 7. code-review - 代码审查

**Commands (1个)**:
- `code-review` - 执行代码审查

**推荐用途**: 快速代码审查

---

### 8. code-simplifier - 代码简化器

**Agents (1个)**:
- `code-simplifier` - 自动简化代码

**推荐用途**: 重构和优化代码

---

### 9. frontend-design ⭐ 前端设计

**Skills (1个)**:
- `frontend-design` - 前端界面设计和生成

**推荐用途**: 创建高质量的前端界面

---

### 10. playground - 交互式演示

**Skills (1个)**:
- `playground` - 创建交互式 HTML playground

**推荐用途**: 创建可视化演示和文档

---

## 📝 文档和配置类

### 11. claude-md-management - CLAUDE.md 管理

**Skills (1个)**:
- `claude-md-improver` - 改进 CLAUDE.md 文件

**Commands (1个)**:
- `revise-claude-md` - 修订 CLAUDE.md

**推荐用途**: 维护项目的 CLAUDE.md 文档

---

### 12. claude-code-setup - 自动化推荐

**Skills (1个)**:
- `claude-automation-recommender` - 分析项目并推荐自动化方案

**推荐用途**: 项目初始化时获取自动化建议

---

### 13. hookify - 钩子管理

**Skills (1个)**:
- `writing-rules` - 编写规则

**Agents (1个)**:
- `conversation-analyzer` - 对话分析器

**Commands (4个)**:
- `configure` - 配置钩子
- `help` - 帮助
- `hookify` - 创建钩子
- `list` - 列出钩子

**推荐用途**: 创建自定义行为规则和钩子

---

## 🔄 工作流类

### 14. commit-commands - Git 提交命令

**Commands (3个)**:
- `commit` - 智能提交
- `commit-push-pr` - 提交、推送、创建 PR
- `clean_gone` - 清理已删除的分支

**推荐用途**: 简化 Git 工作流

---

### 15. ralph-loop - 迭代开发循环

**Commands (3个)**:
- `ralph-loop` - 启动迭代循环
- `cancel-ralph` - 取消循环
- `help` - 帮助

**推荐用途**: 迭代式开发和优化

---

## 🎯 推荐组合

### 🔰 初学者推荐

```json
{
  "plugins": [
    "plugin-dev",      // 完整开发指南
    "skill-creator",   // 创建 Skills
    "example-plugin"   // 学习参考
  ]
}
```

### 🚀 功能开发推荐

```json
{
  "plugins": [
    "feature-dev",       // 功能开发助手
    "code-review",       // 代码审查
    "commit-commands"    // Git 工作流
  ]
}
```

### ✅ 代码质量推荐

```json
{
  "plugins": [
    "pr-review-toolkit",  // 全面 PR 审查
    "code-simplifier",    // 代码优化
    "code-review"         // 代码审查
  ]
}
```

### 📚 文档和配置推荐

```json
{
  "plugins": [
    "claude-md-management",  // 文档管理
    "claude-code-setup",     // 自动化推荐
    "hookify"                // 自定义规则
  ]
}
```

---

## 🔍 关键插件详解

### plugin-dev - 最全面的开发套件

**为什么推荐**:
- ✅ 包含所有开发指南（7个 Skills）
- ✅ 自动创建工具（3个 Agents）
- ✅ 覆盖 Skill、Agent、Command、Hook、MCP 全部类型

**核心功能**:
1. **学习开发** - 通过 Skills 学习各种插件组件
2. **自动创建** - `agent-creator` 自动生成 Agent 配置
3. **质量保证** - `skill-reviewer` 和 `plugin-validator` 审查代码

**使用示例**:
```bash
# 学习 Agent 开发
/agent-development

# 创建新 Agent（自动触发 agent-creator）
"创建一个检查代码复杂度的 agent"

# 审查 Skill
# skill-reviewer 会自动触发
```

---

### skill-creator - Skill 专业工具

**为什么推荐**:
- ✅ 专注于 Skill 的完整生命周期
- ✅ 包含性能测试和优化
- ✅ 支持评估（evals）和基准测试

**核心功能**:
1. **创建 Skill** - 交互式创建
2. **优化 Skill** - 改进现有 Skill
3. **测试性能** - 运行 evals 和基准测试

**使用示例**:
```bash
/skill-creator

# 然后跟随指引：
# 1. 创建新 Skill
# 2. 优化现有 Skill
# 3. 运行性能测试
```

---

### pr-review-toolkit - 最全面的审查工具

**为什么推荐**:
- ✅ 6个专业 Agents 从不同角度审查
- ✅ 全面覆盖代码质量、测试、类型设计等
- ✅ 自动检测隐藏问题

**核心功能**:
1. **代码审查** - code-reviewer
2. **简化建议** - code-simplifier
3. **测试分析** - pr-test-analyzer
4. **问题检测** - silent-failure-hunter
5. **类型审查** - type-design-analyzer
6. **注释检查** - comment-analyzer

**使用示例**:
```bash
/review-pr

# 或直接描述
"审查这个 PR 的代码质量"
```

---

## 📋 如何添加到你的项目

### 方式 1: 引用官方路径

在 `.claude-plugin/marketplace.json` 中：

```json
{
  "plugins": [
    {
      "name": "plugin-dev",
      "source": "D:/ai/claude-plugins-official/plugins/plugin-dev",
      "category": "development"
    },
    {
      "name": "skill-creator",
      "source": "D:/ai/claude-plugins-official/plugins/skill-creator",
      "category": "development"
    }
  ]
}
```

### 方式 2: 复制到本地（如需修改）

```bash
# 复制插件
cp -r D:/ai/claude-plugins-official/plugins/plugin-dev ./plugins/

# 更新 marketplace.json
{
  "plugins": [
    {
      "name": "plugin-dev",
      "source": "./plugins/plugin-dev",
      "category": "development"
    }
  ]
}
```

---

## 🎯 常见使用场景

### 场景 1: 我想创建一个新的 Skill

**推荐插件**: `skill-creator`

```bash
/skill-creator
```

### 场景 2: 我想创建一个新的 Agent

**推荐插件**: `plugin-dev` (包含 agent-creator)

```bash
# 直接描述需求，agent-creator 会自动触发
"创建一个 agent 来分析日志文件"
```

### 场景 3: 我想审查 PR

**推荐插件**: `pr-review-toolkit`

```bash
/review-pr
```

### 场景 4: 我想学习插件开发

**推荐插件**: `plugin-dev` + `example-plugin`

```bash
/skill-development
/agent-development
```

### 场景 5: 我想简化代码

**推荐插件**: `code-simplifier`

```bash
# code-simplifier agent 会自动触发
"简化这段代码"
```

### 场景 6: 我想管理 CLAUDE.md

**推荐插件**: `claude-md-management`

```bash
/revise-claude-md
```

---

## 📚 总结

### 必备插件 Top 3

1. **plugin-dev** - 最全面的开发工具
2. **skill-creator** - Skill 专业工具
3. **pr-review-toolkit** - 代码审查工具

### 按需选择

- **前端开发**: frontend-design, playground
- **Git 工作流**: commit-commands
- **代码质量**: code-review, code-simplifier
- **文档管理**: claude-md-management
- **自定义规则**: hookify

---

**官方仓库**: https://github.com/anthropics/claude-plugins-official
