---
description: 测试左移全流程工作流：自动探测环境、断点续传、统一命名规范，从需求/设计文档生成API自动化测试用例
argument-hint: [需求ID]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(uv run:*), Bash(uvx *), Bash, AskUserQuestion, Skill(za-qe:doc-converter), Skill(za-qe:req-parser), Skill(za-qe:design-parser), Skill(za-qe:interface-extractor), Skill(za-qe:case-designer), Skill(za-qe:api-generator), Skill, Task
---

# 测试左移全流程工作流

> **执行约束（必须遵守）**：
> - 所有 Bash 命令必须使用**绝对路径**，禁止 `cd` 切换目录
> - **禁止使用分号 `;` 连接命令**，包括 `; echo "Exit code: $?"`、`; echo "EXIT:$?"`、`|| echo "失败"` 等任何退出码检查形式
> - 命令失败时 Bash 会直接报错，无需手动检查退出码；需要顺序执行时改用 `&&`

自动完成从原始文档到 API 自动化测试用例的全流程：续传检测 → 环境探测 → 交互式配置 → docx/doc 转 md → 编码修复 → 需求/设计分析 → 用例生成。

## 工作流概览

```
阶段0：续传检测
  检测 CWD 下是否存在 workflow.md → 询问继续/清除重来

阶段1：环境探测 + 交互式配置
  扫描文件名（需求/设计关键词分类）→ 扫描 BANK-XXXX/IP-XXXX ID → 检测 pytest.ini
  → 逐项 AskUserQuestion 确认四个配置项
  → 写入 workflow.md（状态锚点）

阶段2：文档转换
  docx/doc → markitdown → .md → UTF-8 修复
  → 扫描 md 内容补充确认需求ID
  → 输出 BANK-XXXX_PRD.md / BANK-XXXX_DESIGN.md 到根目录

阶段3：Skill 串联（按分支决策）
  req-parser → BANK-XXXX_PRD.md
  design-parser → BANK-XXXX_DESIGN.md
  interface-extractor → temp/BANK-XXXX_接口数据报告.md
  case-designer → BANK-XXXX_CASE.md + temp/BANK-XXXX_CASE_TABLE.md + BANK-XXXX_CASE.xmind
  api-generator → <自动化目录>/ 或 temp/
```

---

## 阶段 0：续传检测

在执行任何操作之前，检测当前工作目录（CWD）下是否存在 `workflow.md`。

### 步骤 0.1：检测 workflow.md

使用 `Glob` 工具检查 CWD 下是否存在 `workflow.md`。

**如果不存在**：直接进入阶段1。

**如果存在**：读取文件内容，提取已记录的配置和进度，然后用 `AskUserQuestion` 询问用户：

```
检测到未完成的工作流记录：
  需求ID：BANK-XXXX
  需求文档：<路径>
  上次执行到：<最后完成的步骤>

选项：
  A. 继续未完成的工作流（从上次失败/中断的步骤继续）
  B. 清除记录，重新开始
```

> **字段来源**：模板中 `BANK-XXXX` 取 workflow.md"**需求ID**"字段值，`<路径>` 取"需求文档"配置值，`<最后完成的步骤>` 取"执行进度"中最后一个标记为 `[x]` 的步骤名（若无则显示"尚未开始"）。workflow.md 格式详见阶段1步骤1.3。

**如果选择继续**：
- 从 `workflow.md` 读取所有配置（需求ID、根目录、各文件路径）
- 找到第一个状态为 `[ ]`（未完成）或 `[!]`（失败）的步骤
- 跳转到对应阶段执行，跳过所有已标记 `[x]`（完成）的步骤（映射规则：workflow.md 执行进度中的步骤名与本文件各阶段标题一一对应，按步骤名匹配本文件对应章节执行；如步骤名为"阶段2：文档转换"则跳转执行本文件"阶段 2"章节）

**如果选择清除重来**：
- 再次确认："确认删除 workflow.md 并重新开始？(yes/no)"
- 用户确认后，使用 `Bash` 工具执行 `rm '<根目录绝对路径>/workflow.md'` 删除文件，然后进入阶段1

### 步骤 0.2：workflow.md 有效性校验（续传时）

续传前校验 workflow.md 中记录的文件路径是否仍然存在：
- 若已完成步骤的输出文件不存在 → 将该步骤状态改为 `[ ]`，需要重新执行
- 若配置的目录不存在 → 提示用户重新配置，回到阶段1对应配置项

## 阶段 1：环境探测 + 交互式配置

### 步骤 1.1：自动扫描当前目录

同时执行以下三项扫描：

**1. 文档文件扫描**

使用 `Glob` 扫描 CWD 下的 `*.docx` 和 `*.doc` 文件，按文件名关键词分类（大小写不敏感）：

- **需求文档关键词**：`prd`, `req`, `requirement`, `需求`, `产品需求`, `功能需求`, `用户需求`, `业务需求`, `需求说明`, `需求规格`
- **设计文档关键词**：`design`, `设计`, `方案`, `开发方案`, `技术方案`, `详细设计`, `概要设计`, `系统设计`, `接口设计`, `架构设计`

分类规则：
- 文件名同时命中两类关键词 → **需求优先**，在选项中标注"(需求关键词优先匹配)"
- 未命中任何关键词的 docx/doc 文件 → 也列出，供用户手动选择

**2. 需求ID扫描**

扫描所有找到的文件名，提取符合以下正则的ID：
- `BANK-\d+`（如 BANK-12345）
- `IP-\d+`（如 IP-6789）

**3. pytest.ini 检测**

使用 `Glob` 检查 CWD 下是否存在 `pytest.ini`。

**输出探测摘要**：

```
环境探测结果：
  找到文件：N 个 docx/doc（需求候选：X 个，设计候选：Y 个，未分类：Z 个）
  检测到ID：BANK-XXXX（来自文件名 xxx.docx）
  pytest.ini：✅ 检测到 / ❌ 未检测到
```

---

### 步骤 1.2：交互式配置（单次合并展示）

将四个配置项合并为**一次 `AskUserQuestion` 调用**，`questions` 数组同时展示，用户在同一界面完成所有配置。

**选项构建规则（每个配置项）**：
- 检测到的候选最多取前 3 个，每个作为一个选项（标注来源说明）
- 末位固定加"手动输入"选项
- 若候选数量 ≤ 2，末位再加"无"选项（需求ID和需求文档除外，不加"无"）

**`AskUserQuestion` 调用结构**：

```
questions:
  - header: "需求ID"
    question: "请选择或输入需求ID："
    multiSelect: false
    options:
      - label: "{检测到的ID1}"
        description: "来自文件名：{来源文件名}"
      - label: "{检测到的ID2}"          # 若有
        description: "来自文件名：{来源文件名}"
      - label: "手动输入"
        description: "自行输入 BANK-XXXX 或 IP-XXXX 格式"

  - header: "需求文档"
    question: "请选择需求文档（必填）："
    multiSelect: false
    options:
      - label: "{需求候选文件1}"
        description: "关键词匹配：{命中的关键词}"
      - label: "{需求候选文件2}"          # 若有
        description: "关键词匹配：{命中的关键词}"
      - label: "手动输入"
        description: "输入文件路径（不能为空）"

  - header: "设计文档"
    question: "请选择设计文档（可选）："
    multiSelect: false
    options:
      - label: "{设计候选文件1}"
        description: "关键词匹配：{命中的关键词}"
      - label: "手动输入"
        description: "输入文件路径，输入 - 表示无设计文档"
      - label: "无"
        description: "不提供设计文档，仅生成场景案例"

  - header: "自动化目录"
    question: "请选择自动化项目根目录（可选）："
    multiSelect: false
    options:
      - label: "当前目录"               # 仅当检测到 pytest.ini 时加入
        description: "检测到 pytest.ini：{CWD绝对路径}"
      - label: "手动输入"
        description: "输入目录路径，输入 - 表示无自动化目录"
      - label: "无"
        description: "不关联自动化工程"
```

> 若未检测到任何ID，需求ID 问题只保留"手动输入"选项，跳过检测结果选项。
> 用户未通过参数传入 `[需求ID]` 时才展示需求ID问题；若已传入则该问题从 `questions` 中移除（只展示3个问题）。

**用户选"手动输入"后的处理**：

收到 `AskUserQuestion` 结果后，检查各项是否为"手动输入"：
- 需求ID 选了"手动输入" → 再次单独调用 `AskUserQuestion` 询问具体值（格式：BANK-XXXX 或 IP-XXXX，不能为空）
- 需求文档 选了"手动输入" → 再次询问文件路径（不能为空，输入 `无`/`-` 提示错误并重询）
- 设计文档 选了"手动输入" → 再次询问文件路径（输入 `无`/`-` 视为空值，合法）
- 自动化目录 选了"手动输入" → 再次询问目录路径（输入 `无`/`-` 视为空值；输入有效路径后用 `Glob` 校验是否存在 `pytest.ini`，不存在则警告不阻断）

---

### 步骤 1.3：写入 workflow.md

配置确认后，在**需求文档所在目录（根目录）**写入 `workflow.md`。

> 根目录 = 需求文档所在目录（不一定是 CWD）

使用 `Write` 工具写入 `<根目录>/workflow.md`，内容模板如下：

```markdown
# Workflow 状态记录

**创建时间**：{当前时间，格式：YYYY-MM-DD HH:MM:SS}
**需求ID**：{BANK-XXXX}
**根目录**：{根目录绝对路径}

## 配置

- 需求文档：{需求文档文件名}
- 设计文档：{设计文档文件名 或 无}
- 自动化目录：{自动化目录绝对路径 或 无}

## 执行进度

- [ ] 阶段2：文档转换
- [ ] 阶段3.1：req-parser → BANK-XXXX_PRD.md
- [ ] 阶段3.2：design-parser → BANK-XXXX_DESIGN.md（如有设计文档）
- [ ] 阶段3.3：interface-extractor → temp/BANK-XXXX_接口数据报告.md（如有设计文档）
- [ ] 阶段3.4：case-designer → BANK-XXXX_CASE.md + temp/BANK-XXXX_CASE_TABLE.md
- [ ] 阶段3.5：api-generator（如有自动化目录）

## 产出文件

（每步完成后追加记录，格式：`步骤名: 文件绝对路径`）
（注：写入时将执行进度列表中所有 `BANK-XXXX` 替换为实际需求ID）
```

同时使用 `Write` 工具在根目录创建 `BANK-XXXX_NOTES.md`（`BANK-XXXX` 替换为实际需求ID），内容为：

```markdown
# BANK-XXXX 测试记录

> 此文件用于记录测试过程数据，包括测试数据、环境变量、mock 开关等。
```

---

## 阶段 2：文档转换

> 阶段2读取阶段1配置的文件，输出路径统一写入根目录（`workflow.md` 所在目录）。

> **格式预检**：在调用 doc-converter 前，检查阶段1配置的需求文档路径扩展名：
> - 若已是 `.md` 格式 → 跳过 doc-converter，直接用 `Bash` 将文件复制（或重命名）到根目录：
>   ```bash
>   cp '<需求文档绝对路径>' '<根目录绝对路径>/BANK-XXXX_PRD.md'
>   ```
>   然后跳转到步骤2.3（内容扫描确认ID）。
> - 若是 `.docx`/`.doc` 格式 → 正常执行步骤2.1（调用 doc-converter）。
>
> 设计文档同理：若已是 `.md` 格式，步骤2.2直接复制到根目录为 `BANK-XXXX_DESIGN.md`，跳过 doc-converter 调用。

### 步骤 2.1：转换需求文档

调用 `doc-converter` Skill，传入：
- 输入目录：需求文档所在目录（绝对路径）
- 输出目录：根目录下的 `temp/` 子目录（绝对路径）；调用前先用 `Bash` 工具确保目录存在：`mkdir -p '<根目录绝对路径>/temp'`

`doc-converter` 完成后，将需求文档对应的 md 文件从 `temp/` **重命名并移动**到根目录：

```
temp/<原文件名>.md  →  <根目录>/BANK-XXXX_PRD.md
```

使用 `Bash` 工具（绝对路径，禁止 cd）：
```bash
mv '<temp目录绝对路径>/<原文件名>.md' '<根目录绝对路径>/BANK-XXXX_PRD.md'
```

---

### 步骤 2.2：转换设计文档（如有）

**触发条件**：阶段1配置的设计文档非空。

**分支A：设计文档与需求文档在同一目录**

步骤2.1 已将该目录所有文档转换到 temp/，设计文档 md 已存在于 temp/ 中。
无需再次调用 doc-converter，直接重命名移动：

```bash
mv '<temp目录绝对路径>/<设计文档原文件名>.md' '<根目录绝对路径>/BANK-XXXX_DESIGN.md'
```

**分支B：设计文档在不同目录**

调用 `doc-converter` Skill，传入：
- 输入目录：设计文档所在目录（绝对路径）
- 输出目录：根目录下的 `temp/` 子目录
- 前缀参数：`--prefix design_`

转换后重命名移动：

```
temp/design_<原文件名>.md  →  <根目录>/BANK-XXXX_DESIGN.md
```

---

### 步骤 2.3：内容扫描补充确认需求ID

读取 `<根目录>/BANK-XXXX_PRD.md` 的**第一行和所有一级标题（`# ` 开头的行）**，使用正则提取 `BANK-\d+` 或 `IP-\d+`。

- 若提取到的ID与阶段1配置的ID **一致**（或未提取到任何ID）→ 无需操作，继续。
- 若提取到的ID与阶段1配置的ID **不同** → 用 `AskUserQuestion` 询问：

```
文档内容中检测到需求ID：{文档中的ID}
当前配置的需求ID：{阶段1配置的ID}

请选择：
  A. 使用文档中的ID：{文档中的ID}
  B. 保留当前配置的ID：{阶段1配置的ID}
```

若用户选择A（更正）：
- 用 `Edit` 工具更新 `workflow.md` 中的 `**需求ID**` 字段，并将"执行进度"和"产出文件"区域中所有旧ID（如 `旧ID_PRD.md`）替换为新ID
- 将根目录下已生成文件的名称中的旧ID替换为新ID（`BANK-XXXX_PRD.md` 重命名）
- 使用 `Bash` 工具：`mv '<根目录>/旧ID_PRD.md' '<根目录>/新ID_PRD.md'`

---

### 步骤 2.4：更新进度

在 `workflow.md` 中将"阶段2：文档转换"从 `[ ]` 改为 `[x]`，并在"产出文件"区域追加：

```
阶段2_PRD: <根目录绝对路径>/BANK-XXXX_PRD.md
阶段2_DESIGN: <根目录绝对路径>/BANK-XXXX_DESIGN.md（如有设计文档）
```

使用 `Edit` 工具修改 `workflow.md`。

---

## 阶段 3：Skill 串联

> **重要原则**：
> - 阶段3所有 Skill 一律读取阶段2产出的 md 文件，**不得直接读取原始 doc/docx 文件**
> - **每个 Skill 执行完成后，必须立即继续执行下一个 Skill，不得停下等待用户指令**
> - 每完成一个 Skill，进度更新由**主流程**统一用 `Edit` 写入 `workflow.md`，子代理不写 workflow.md

### 分支决策

根据阶段1配置的结果，在进入步骤3.1前先确定执行路径：

| 场景 | 执行路径 |
|------|---------|
| 需求 + 设计 + 自动化目录 | 3.1/3.2 并行 → 3.3 interface-extractor → 3.4 case-designer → 3.5 api-generator（输出到自动化目录） |
| 需求 + 设计 + 无自动化 | 3.1/3.2 并行 → 3.3 interface-extractor → 3.4 case-designer（结束） |
| 仅需求（无设计） | 3.1 req-parser → 3.4 case-designer（结束） |
| 仅设计（无需求） | **中止**：输出"需求文档为必填项，仅有设计文档无法执行工作流，请重新执行 /za-qe:qe-workflow" |
| 无需求 | **中止**：输出"需求文档为必填项，请重新执行 /za-qe:qe-workflow 并提供需求文档" |

---

### 步骤 3.1 + 3.2：并行调用 req-parser 和 design-parser（有设计文档时）

**触发条件**：同时存在需求文档和设计文档时，用 `Task` 工具同时派发两个子代理并行执行。

#### 子代理A：req-parser

- **任务**：按照 req-parser Skill 的流程，读取 `<根目录>/BANK-XXXX_PRD.md`，规范化后覆盖写入同路径
- **返回格式**（最后一行）：
  - 成功：`STATUS: OK`
  - 失败：`STATUS: ERROR <原因>`
- **约束**：不得修改 `workflow.md`

#### 子代理B：design-parser

- **任务**：按照 design-parser Skill 的流程，读取 `<根目录>/BANK-XXXX_DESIGN.md`，规范化后覆盖写入同路径
- **返回格式**（最后一行）：
  - 成功：`STATUS: OK`
  - 失败：`STATUS: ERROR <原因>`
- **约束**：不得修改 `workflow.md`

#### 等待两个子代理完成后，主流程处理结果

- 两者均 `OK` → 用 `Edit` 将 `workflow.md` 中 3.1 和 3.2 均标记为 `[x]`，追加产出文件记录，立即进入步骤3.3
- 子代理A失败 → 将 3.1 标记为 `[!]`，中止后续执行（design-parser 结果已产出可保留）
- 子代理B失败 → 将 3.2 标记为 `[!]`，中止后续执行（req-parser 结果已产出可保留）

> **仅需求（无设计）时**：不派发子代理，直接在主流程中执行 req-parser Skill，完成后标记 3.1 为 `[x]`，跳过3.2，进入步骤3.4。

---

### 步骤 3.3：调用 interface-extractor（有设计文档产出时执行）

**触发条件**：步骤3.2已完成

- **输入**：
  - 规范化设计文档：`<根目录>/BANK-XXXX_DESIGN.md`（必须）
  - 规范化需求文档：`<根目录>/BANK-XXXX_PRD.md`（可选，补充业务上下文）
- **输出**：`<根目录>/temp/BANK-XXXX_接口数据报告.md`

确保 `<根目录>/temp/` 存在（步骤2.1已创建，此处无需重复创建）。

**完成后**：用 `Edit` 工具将"阶段3.3：interface-extractor"标记为 `[x]`，追加：
```
阶段3.3: <根目录绝对路径>/temp/BANK-XXXX_接口数据报告.md
```
立即进入步骤3.4。

---

### 步骤 3.4：调用 case-designer（有需求文档时必须执行）

**触发条件**：步骤3.1已完成

- **输入**：
  - 规范化需求文档：`<根目录>/BANK-XXXX_PRD.md`（必须）
  - 接口数据报告：`<根目录>/temp/BANK-XXXX_接口数据报告.md`（可选；无则"调用接口"列留空）
- **输出**（明确传入以下路径）：
  - 场景案例文档：`<根目录>/BANK-XXXX_CASE.md`
  - 场景案例表：`<根目录>/temp/BANK-XXXX_CASE_TABLE.md`
  - XMind 输出目录：`<根目录>/`（脚本自动生成 `BANK-XXXX_CASE.xmind`）

**完成后**：用 `Edit` 工具将"阶段3.4：case-designer"标记为 `[x]`，追加：
```
阶段3.4_CASE: <根目录绝对路径>/BANK-XXXX_CASE.md
阶段3.4_TABLE: <根目录绝对路径>/temp/BANK-XXXX_CASE_TABLE.md
阶段3.4_XMIND: <根目录绝对路径>/BANK-XXXX_CASE.xmind
```
根据分支决策继续：有自动化目录且有接口数据报告 → 进入步骤3.5；否则输出完成汇总。

---

### 步骤 3.5：调用 api-generator（有接口数据报告且有自动化目录时执行）

**触发条件**：步骤3.3产出了接口数据报告 **且** 阶段1配置了自动化项目目录

- **输入**：
  - 接口数据报告：`<根目录>/temp/BANK-XXXX_接口数据报告.md`（必须）
  - 场景案例表：`<根目录>/temp/BANK-XXXX_CASE_TABLE.md`（可选，有则生成场景测试代码）
- **输出目录**：`<自动化项目目录>/`

**完成后**：用 `Edit` 工具将"阶段3.5：api-generator"标记为 `[x]`，在"产出文件"区域追加：
```
阶段3.5: <自动化项目目录绝对路径>/
```
然后输出最终汇总。

---

## 完成汇总输出

全部步骤执行完成后，输出以下汇总：

```
测试左移全流程工作流执行完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

需求ID：BANK-XXXX
根目录：<根目录路径>

产出文件：
  BANK-XXXX_PRD.md        ← 规范化需求文档
  BANK-XXXX_DESIGN.md     ← 规范化设计文档（如有）
  BANK-XXXX_CASE.md       ← 场景案例（流程图+MindMap）
  BANK-XXXX_CASE.xmind         ← 测试案例 XMind
  BANK-XXXX_NOTES.md      ← 测试记录文件（待手动填写）
  temp/BANK-XXXX_接口数据报告.md  ← 接口数据（如有）
  temp/BANK-XXXX_CASE_TABLE.md   ← 场景案例表

自动化测试代码：
  <自动化目录>/（如有）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**仅需求（无设计文档）时**，完成后输出：

```
已生成：
  ✅ 规范化需求文档（BANK-XXXX_PRD.md）
  ✅ 场景案例（BANK-XXXX_CASE.md）
  ✅ 测试案例 XMind（BANK-XXXX_CASE.xmind）
  ✅ 测试记录文件（BANK-XXXX_NOTES.md，待手动填写）

后续可选操作：
  1. 提供设计文档后重新执行 /za-qe:qe-workflow — 补全接口数据并生成 API 自动化测试
  2. 手动在场景案例表中填入接口信息后调用 /api-generator
```

---

## 错误处理

### 文档转换失败

```
警告：文档转换失败
文件：<文件路径>
建议：检查文件是否损坏；尝试用 Word 另存为 .docx 格式
```
处理：跳过失败文件，继续处理其他文件；全部完成后汇报失败列表。

### Skill 执行失败

```
步骤 N 失败：<Skill名称> 执行未完成

已完成步骤：
  [x] 步骤1...
  [!] 步骤N（失败）
  [ ] 步骤N+1（未执行）

workflow.md 已记录当前进度，下次执行 /za-qe:qe-workflow 可从失败步骤继续。
```
处理：用 `Edit` 工具将该步骤在 `workflow.md` 中标记为 `[!]`，停止后续执行，保留已完成步骤产出。

---

## 相关命令

- `/za-qe:qe-gencase` — 生成场景案例（PlantUML 流程图 + MindMap）
- `/za-qe:qe-help` — 查看详细帮助
- `/req-parser` — 独立执行需求文档标准化
- `/design-parser` — 独立执行设计文档规范化
- `/interface-extractor` — 独立执行接口数据提取
- `/case-designer` — 独立执行场景案例设计
- `/api-generator` — 独立执行 API 用例生成

---

**版本**: v3.0.0 | **状态**: ✅ 可用
