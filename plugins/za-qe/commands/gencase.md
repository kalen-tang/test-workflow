---
description: 从需求文档生成场景化测试案例（PlantUML流程图和MindMap测试设计）
argument-hint: [doc_paths] [--output dir]
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Bash(uv *), Bash(uv run *)
---

# 场景测试案例生成器

从需求文档生成场景化的测试设计，包括 PlantUML 流程图和 MindMap 测试案例，适用于测试设计、测试评审和团队协作场景。

## 🎯 功能概览

```
📄 需求文档（支持多种格式）
        ↓
🔍 文档解析
   - 自动识别文档结构
   - 提取业务流程和功能点
   - 容错处理不规范文档
        ↓
📊 生成输出
   ├─ 业务流程图（PlantUML Activity Diagram）
   ├─ 测试功能点（PlantUML MindMap，三层）
   └─ 详细测试案例（PlantUML MindMap，四层）
        ↓
📋 Markdown 测试设计文档
```

## 📝 使用方式

### 基本用法

```bash
# 从单个文档生成
/za-qe:qe-gencase ./docs/requirement.md

# 从多个文档生成（自动合并）
/za-qe:qe-gencase ./docs/req1.md ./docs/req2.docx ./docs/req3.txt

# 指定输出目录
/za-qe:qe-gencase ./docs/requirement.md --output ./review
```

### 支持的文档格式

- **Markdown**（.md）：推荐格式，解析效果最佳
- **Word**（.doc, .docx）：支持自动解析章节结构
- **纯文本**（.txt）：基础支持
- **PDF**（.pdf）：支持文本提取

### 参数说明

| 参数 | 说明 | 示例 | 默认值 |
|-----|------|------|--------|
| `<doc_paths>` | 需求文档路径（必填，支持多个） | `./docs/req.md` | - |
| `--output <目录>` | 输出目录（可选） | `--output ./output` | `./result/` |

## 🎨 输出内容

生成的 Markdown 文件包含以下部分：

### 1. 业务流程图

PlantUML Activity Diagram，展示完整的业务流程：
- ✅ 主要业务步骤和操作
- ✅ 关键决策点和条件分支
- ✅ 异常处理和回滚流程
- ✅ 复杂步骤的注释说明

**主题**：`!theme materia`

### 2. 测试功能点 MindMap

PlantUML MindMap，至少三层结构：
- ✅ 根节点：项目或模块名称
- ✅ 一级节点：主要功能模块（左右交替分布）
- ✅ 二级节点：具体功能点
- ✅ 三级节点：验证点或子功能

**主题**：`!theme blueprint + materia`

**命名规范**：
- 去掉"测试"后缀（如 `搜索栏` 而非 `搜索栏测试`）
- 简化验证点表达（如 `显示正常` 而非 `验证搜索栏显示正常`）
- 功能模块-验证点结构（父子节点关系）

### 3. 详细测试案例 MindMap

PlantUML MindMap，至少四层结构：
- ✅ 根节点：测试案例集名称
- ✅ 一级节点：测试场景（左右交替分布）
- ✅ 二级节点：测试步骤（操作节点）
- ✅ 三级节点：验证点（预期结果节点）
- ✅ 四级节点：详细验证内容（可选）

**命名规范**：
- 动作与结果分离（操作节点 + 验证节点）
- 数据传递标记（可选）：`{{步骤N.字段名}}`

### 4. 测试策略建议

包含以下内容：
- 测试重点（核心业务流程、异常场景）
- 测试优先级（P0/P1/P2 分布）
- 测试方法（功能测试、边界值测试、兼容性测试）

## 📊 输出文件

**文件路径**：`<output_dir>/<项目名>_场景测试案例.md`

**默认路径示例**：
- `./result/requirement_场景测试案例.md`

**文件内容**：
1. 文档信息（生成时间、来源、模式）
2. 业务流程图（PlantUML 代码块）
3. 测试功能点（PlantUML 代码块）
4. 详细测试案例（PlantUML 代码块）
5. 测试策略建议

## 🎯 使用场景

### 场景 1：快速生成测试设计

```bash
# 产品提供需求文档后立即生成测试设计
/za-qe:qe-gencase ./docs/new-feature.md
```

**预期输出**：
- `./result/new_feature_场景测试案例.md`
- 包含流程图、测试功能点、详细测试案例

**适用情况**：
- ✅ 需求明确，文档完整
- ✅ 快速迭代，时间紧张
- ✅ 需要可视化测试设计

---

### 场景 2：多文档整合

```bash
# 多个需求文档整合为一个测试方案
/za-qe:qe-gencase ./docs/req1.md ./docs/req2.md ./docs/req3.docx
```

**预期输出**：
- `./result/integrated_场景测试案例.md`
- 自动合并所有文档的流程和功能点

**适用情况**：
- ✅ 需求分散在多个文档
- ✅ 需要整体测试视图
- ✅ 多人协作，文档分散

---

### 场景 3：测试评审

```bash
# 生成可视化测试用例用于评审
/za-qe:qe-gencase ./docs/requirement.docx --output ./review
```

**预期输出**：
- `./review/requirement_场景测试案例.md`
- 团队可以在线查看 PlantUML 渲染结果

**适用情况**：
- ✅ 需要团队评审测试设计
- ✅ 需要可视化展示
- ✅ 需要共享测试方案

## 💡 最佳实践

### 文档准备建议

虽然本命令支持完全不规范的文档，但文档质量直接影响生成效果。包含以下内容可获得更佳结果：

- ✅ **清晰的功能描述**：说明每个功能的目的和作用
- ✅ **明确的业务流程**：描述用户操作步骤和系统响应
- ✅ **具体的验收标准**：定义功能是否合格的标准
- ✅ **异常场景说明**：列举可能的错误和异常处理

文档过于简单或不规范时，生成的测试用例可能不够全面。

### PlantUML 渲染

生成的 PlantUML 代码可以使用以下工具渲染：

- **在线渲染**：[PlantUML Online](http://www.plantuml.com/plantuml/uml/)
- **VS Code 插件**：PlantUML
- **本地渲染**：安装 PlantUML CLI
- **Markdown 预览**：支持 PlantUML 的 Markdown 编辑器

### 后续优化

生成的测试案例适合人工 Review 和调整：

- 📝 人工补充遗漏的测试点
- 📝 调整测试优先级
- 📝 细化测试步骤
- 📝 添加边界值和异常场景

如需生成自动化测试代码，可将此输出作为参考，结合 `/za-qe:qe-workflow` 命令。

## ⚠️ 注意事项

### 文档格式兼容性

- **Markdown**：最佳支持，推荐使用
- **Word**：需要文档结构清晰（标题、段落、列表）
- **PDF**：仅支持文本提取，复杂格式可能丢失
- **纯文本**：基础支持，需要人工检查生成结果

### 多文档合并

当提供多个文档时：
- ✅ 自动合并所有文档的流程和功能点
- ✅ 去重相似的测试点
- ⚠️ 可能需要人工调整合并后的结构

### 数据传递标记

测试案例中的数据传递标记（`{{步骤N.字段名}}`）是可选的：
- ✅ 有助于理解测试步骤间的依赖
- ✅ 便于后续对接自动化测试
- ⚠️ 需要人工 Review 标记的准确性

## 📚 相关命令

- `/za-qe:qe-workflow` - 测试左移工作流（KM 文档 → 接口测试）
- `/za-qe:qe-help` - 查看帮助信息
- `/doc-reviewer` - 需求文档验证
- `/api-generator` - 生成自动化测试代码

## 📖 详细文档

### Skill 文档

- [SKILL.md](../skills/case-designer/SKILL.md) - 完整的技能文档

### 参考文档

- [PlantUML 流程图生成规则](../skills/case-designer/references/flowchart-generation.md)
- [测试功能点 MindMap 生成规则](../skills/case-designer/references/test-points-mindmap.md)
- [详细测试案例 MindMap 生成规则](../skills/case-designer/references/test-cases-mindmap.md)
- [测试案例命名规范详解](../skills/case-designer/references/naming-conventions.md)

### 示例文件

- [示例需求文档](../skills/case-designer/examples/sample-requirement.md)
- [完整输出示例](../skills/case-designer/examples/sample-output.md)
- [流程图示例](../skills/case-designer/examples/sample-flowchart.puml)
- [测试功能点示例](../skills/case-designer/examples/sample-test-points.puml)
- [测试案例示例](../skills/case-designer/examples/sample-test-cases.puml)

## 🎓 示例演示

### 示例 1：单文档生成

**输入**：
```bash
/za-qe:qe-gencase ./docs/search-feature.md
```

**输出**：
```
✅ 场景测试案例生成完成

📄 输入文档: ./docs/search-feature.md
📋 输出文件: ./result/search_feature_场景测试案例.md

📊 生成内容:
   - 业务流程图: 1个 (包含主流程、决策分支、异常处理)
   - 测试功能点: 6个一级模块, 30+个功能点
   - 详细测试案例: 12个场景, 50+个测试步骤

🎯 下一步操作:
   1. 查看生成的测试案例:
      cat ./result/search_feature_场景测试案例.md

   2. 渲染 PlantUML 图:
      使用 PlantUML Online 或 VS Code 插件

   3. 团队评审:
      分享文件给团队成员进行 Review

   4. 生成自动化测试（可选）:
      /za-qe:qe-workflow ./docs/api-plan.md
```

---

### 示例 2：多文档合并

**输入**：
```bash
/za-qe:qe-gencase ./docs/ui-requirement.md ./docs/api-requirement.md ./docs/business-rules.docx
```

**输出**：
```
✅ 场景测试案例生成完成

📄 输入文档:
   - ./docs/ui-requirement.md
   - ./docs/api-requirement.md
   - ./docs/business-rules.docx

📋 输出文件: ./result/integrated_场景测试案例.md

📊 生成内容:
   - 业务流程图: 1个 (整合了3个文档的流程)
   - 测试功能点: 8个一级模块, 45+个功能点
   - 详细测试案例: 18个场景, 80+个测试步骤

⚠️ 提示:
   - 已自动合并所有文档的功能点
   - 建议人工 Review 合并后的结构
   - 可能需要调整部分测试点的优先级

🎯 下一步操作:
   1. 查看生成的测试案例
   2. 人工 Review 并调整
   3. 团队评审
```

---

## 🔧 故障排除

### 问题 1：文档未找到

```
❌ 错误: 文档文件不存在
   路径: ./docs/requirement.md

建议:
- 检查文件路径是否正确
- 确认文件是否存在
- 使用绝对路径或相对路径
```

**解决方法**：检查文档路径，确保文件存在。

---

### 问题 2：文档格式不支持

```
⚠️ 警告: 文档格式可能不完全支持
   文件: requirement.pdf
   格式: PDF

建议:
- PDF 格式仅支持文本提取
- 复杂格式可能丢失
- 推荐使用 Markdown 或 Word 格式
```

**解决方法**：将 PDF 转换为 Markdown 或 Word 格式。

---

### 问题 3：生成结果不完整

```
⚠️ 提示: 生成的测试用例可能不够全面

原因:
- 文档过于简单或不规范
- 缺少业务流程描述
- 缺少验收标准

建议:
- 补充文档内容（功能描述、业务流程、验收标准）
- 人工 Review 并补充遗漏的测试点
- 参考示例文档格式
```

**解决方法**：优化需求文档质量，补充必要信息。

---

**版本**: v1.4.0 | **状态**: ✅ 可用
