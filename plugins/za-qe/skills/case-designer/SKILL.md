---
name: case-designer
description: 此技能应在用户说"帮我生成测试案例"、"把需求转成测试用例"、"生成PlantUML流程图"、"画一下测试功能点"、"需要测试MindMap"、"测试案例可视化"、"生成场景案例"时使用。用于生成场景案例和可视化测试设计。
version: 2.0.0
status: active
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv *), Bash(uv run:*), Task
---

# 场景案例设计器

## 技能目标

基于需求文档（和可选的接口数据报告）生成可视化的测试设计和结构化的场景案例表，帮助测试团队快速设计全面的测试方案，同时为 `api-generator` 提供可消费的场景数据。

**产出物**：

1. **场景案例 Markdown**（内嵌 PlantUML 业务流程图 + 测试功能点 MindMap + 详细测试案例 MindMap）
   - workflow 中输出路径：`<根目录>/BANK-XXXX_CASE.md`
   - 独立调用时输出路径：`<输出目录>/<项目名>_CASE.md`
2. **XMind 文件**（从 Markdown 中自动提取详细测试案例 MindMap 并转换）
   - workflow 中输出路径：`<根目录>/BANK-XXXX_CASE.xmind`
   - 独立调用时输出路径：`<输出目录>/BANK-XXXX_CASE.xmind`
3. **场景案例表 Markdown**（结构化，给 api-generator 消费）
   - workflow 中输出路径：`<根目录>/temp/BANK-XXXX_CASE_TABLE.md`
   - 独立调用时输出路径：`<输出目录>/<项目名>_CASE_TABLE.md`

## 输入

### 必须输入

- **规范化需求文档**（req-parser 产出的 md 文件，**不读取原始 doc/docx**）

### 可选输入

- **接口数据报告**（interface-extractor 产出的 md 文件）
  - 有接口数据时，场景步骤关联具体接口（IF-ID、路径、方法）
  - 无接口数据时，"调用接口"列留空或填写推断的接口描述

## 核心功能

### 1. 需求文档解析

> workflow 串联调用时，输入必须是 req-parser 产出的 `.md` 文件；独立调用时支持 Word（.doc/.docx）、Markdown（.md）、纯文本（.txt）、PDF（.pdf）。

解析策略：自动识别文档结构（章节、段落、列表、表格），提取功能描述、业务流程、验收标准、异常场景。即使文档不规范也尽力提取有用信息。

### 2. PlantUML 流程图生成

根据需求文档生成 PlantUML Activity Diagram，展示完整业务流程（主要流程、决策点、异常处理、注释说明）。

- 使用 `!theme materia` 主题
- 仅包含需求明确提及的内容（不添加推测）

> 详细规则参见 `references/flowchart-generation.md`

### 3. 测试功能点 MindMap

基于需求文档生成至少三层结构的 PlantUML MindMap：根节点（项目名）→ 一级（功能模块）→ 二级（功能点）→ 三级（验证点）。

使用 `!theme blueprint` + `!theme materia`，一级节点循环使用 `right side` / `left side`。

**命名规范**：去掉"测试"后缀，简化验证点表达，采用功能模块-验证点父子结构。

> 详细规则参见 `references/test-points-mindmap.md`，命名规范参见 `references/naming-conventions.md`

### 4. 详细测试案例 MindMap

基于测试功能点扩展为至少四层结构：根节点 → 一级（测试场景）→ 二级（操作节点）→ 三级（验证节点）→ 四级（详细验证，可选）。

**命名规范**：动作与结果分离（操作节点 + 验证子节点），数据传递使用 `{{步骤N.字段名}}` 标记。

> 详细规则参见 `references/test-cases-mindmap.md`

## 工作流程

### 步骤 1：文档接收与解析

接收需求文档 → 识别文档结构 → 提取业务信息 → 识别功能模块和业务流程

### 步骤 2：生成流程图（子代理执行）

流程图生成和验证在**子代理**中完成，避免验证重试循环污染主流程上下文。

#### 主流程：派发子代理

派发前准备（主流程执行）：
1. 用 `Glob` 工具定位 `validate_plantuml.py` 脚本绝对路径（`<插件根目录>/skills/case-designer/scripts/validate_plantuml.py`），不使用 `${CLAUDE_SKILL_DIR}`
2. 用 `Read` 工具读取 `<插件根目录>/skills/case-designer/references/flowchart-generation.md` 内容，嵌入子代理 prompt

用 `Task` 工具派发一个子代理，Task prompt 须包含：
- 需求文档绝对路径：`<根目录>/BANK-XXXX_PRD.md`（子代理自行 Read）
- 验证脚本绝对路径（上一步已计算）
- 临时文件路径：`<根目录>/temp/flowchart_validate.puml`
- 输出文件路径：`<根目录>/temp/flowchart_result.puml`
- `flowchart-generation.md` 的完整内容

#### 子代理任务

1. 读取需求文档，分析业务流程，识别主要步骤和决策点
2. 按照 flowchart-generation.md 规范生成 PlantUML Activity Diagram
3. 用 `Write` 写入临时文件，执行验证：`uv run '<验证脚本绝对路径>' --file '<临时文件>'`
4. 若返回 `ERROR` → 修正后重新验证（最多重试 5 次）
5. 验证通过后写入结果文件，输出 `---STATUS---\nOK\n---END---`
6. 5 次仍失败则输出 `---STATUS---\nWARN 流程图验证失败，已保留最后一次生成结果\n---END---`

#### 主流程：接收子代理结果

用正则提取 `---STATUS---\n(.*?)\n---END---` 判断状态：
1. 读取 `<根目录>/temp/flowchart_result.puml` 内容
2. 若读取失败 → 标注流程图生成失败，跳过流程图继续步骤3
3. 读取成功后删除两个临时文件
4. 状态为 `OK` → 将内容作为流程图代码块，继续步骤3
5. 状态为 `WARN` → 继续，但标注建议人工检查

### 步骤 3：生成测试功能点

提取功能模块 → 分解为功能点 → 生成三层 MindMap → 应用命名规范

### 步骤 4：生成详细测试案例

基于测试功能点 → 扩展为测试步骤 → 生成四层 MindMap → 区分操作和验证

### 步骤 5：输出 Markdown 文件

整合三个 PlantUML 代码块 → 添加测试策略说明 → 输出 Markdown 到指定目录

> PlantUML 代码全部内嵌在 Markdown 的代码块中，不单独输出 `.puml` 文件。
> 完整输出示例参见 `examples/sample-output.md`

### 步骤 6：生成场景案例表

基于步骤 3、4 的测试功能点和详细测试案例，生成结构化的场景案例表 Markdown，符合 `references/scenario-table.md` 规范。

**生成内容**：场景总览表（ID、名称、类型、优先级、涉及接口）+ 场景详情（前置条件、步骤表、验证点）

**场景来源优先级**：验收标准 → 用户故事 → 业务规则 → 接口依赖推断

**数据传递标记**：`{{步骤N.字段名}}`

**输出文件**：`<输出目录>/temp/<项目名>_CASE_TABLE.md`（始终输出到 temp/ 子目录）

> 详细格式参见 `references/scenario-table.md`
> 场景识别指南参见 `references/scenario-identification.md`
> 用例设计模式参见 `references/test-case-patterns.md`

### 步骤 7：自动生成 XMind 文件

从 Markdown 文件中提取详细测试案例 MindMap 代码块，调用转换脚本生成 XMind 格式。

**脚本路径**：`<插件根目录>/skills/case-designer/scripts/plantuml_to_xmind.py`

> 在子代理（Task）中 `${CLAUDE_SKILL_DIR}` 不可用，须由主流程预先用 `Glob` 定位脚本绝对路径后传入。

**用法**：`uv run '<脚本绝对路径>' <Markdown文件或PlantUML文件> <需求ID>`

XMind 文件生成在输入文件同目录，文件名为 `BANK-XXXX_CASE.xmind`。

## 额外资源

### 脚本工具

- **`<插件根目录>/skills/case-designer/scripts/plantuml_to_xmind.py`** - PlantUML MindMap 转 XMind 格式
- **`<插件根目录>/skills/case-designer/scripts/validate_plantuml.py`** - PlantUML 语法验证

### 参考文件

- **`references/flowchart-generation.md`** - PlantUML 流程图生成规则
- **`references/test-points-mindmap.md`** - 测试功能点 MindMap 生成规则
- **`references/test-cases-mindmap.md`** - 详细测试案例 MindMap 生成规则
- **`references/naming-conventions.md`** - 测试案例命名规范详解
- **`references/scenario-identification.md`** - 场景测试用例识别指南
- **`references/test-case-patterns.md`** - 测试用例设计模式
- **`references/requirement-integration.md`** - 需求文档结合分析指南
- **`references/scenario-table.md`** - 场景案例表格式规范
- **`references/interface-data-report.md`** - 输入：接口数据报告格式
- **`references/normalized-requirement.md`** - 输入：标准化需求文档格式

### 示例文件

- **`examples/sample-output.md`** - 完整输出示例
- **`examples/sample-requirement.md`** - 示例需求文档
- **`examples/sample-flowchart.puml`** - 流程图示例
- **`examples/sample-test-points.puml`** - 测试功能点示例
- **`examples/sample-test-cases.puml`** - 测试案例示例
- **`examples/scenario-test-cases.md`** - 场景测试用例设计示例
- **`examples/sample-with-requirement.md`** - 结合需求文档的场景示例

---

**状态**: ✅ 可用
