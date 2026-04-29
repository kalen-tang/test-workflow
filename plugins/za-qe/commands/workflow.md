---
description: 测试左移全流程工作流：自动探测环境、断点续传、统一命名规范，从需求/设计文档生成API自动化测试用例
argument-hint: [需求ID]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(uv run:*), Bash(uvx *), Bash, AskUserQuestion, Skill(za-qe:doc-converter), Skill(za-qe:req-parser), Skill(za-qe:design-parser), Skill(za-qe:interface-extractor), Skill(za-qe:case-designer), Skill(za-qe:api-generator), Task
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

## 阶段 0：续传检测 + 环境预扫描（并行）

在主流程中同时发起以下 `Glob` 调用（一次性并行，**禁止使用 Task/Agent 子代理**）：

1. `Glob("workflow.md", path=CWD)` — 检测 workflow.md 是否存在
2. `Glob("*.docx", path=CWD)` + `Glob("*.doc", path=CWD)` — 扫描文档文件
3. `Glob("pytest.ini", path=CWD)` — 检测 pytest.ini

所有 Glob 结果返回后，主流程在本地完成：
- 按关键词将文件分类为需求候选、设计候选、未分类
- 从文件名中用正则提取 `BANK-\d+` / `IP-\d+` ID
- 汇总结果，进入步骤 0.1

### 步骤 0.1：处理 workflow.md 检测结果

根据 Glob 结果判断：

**如果 CWD 下不存在 workflow.md**：直接进入阶段1（使用上述扫描结果）。

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

### 步骤 1.1：使用阶段0预扫描结果

阶段0已完成扫描，直接使用其结果，**无需重复扫描**。

预扫描结果包含：
- CWD 下所有 `*.docx`/`*.doc` 文件，已按关键词分类为需求候选、设计候选、未分类
  - **需求文档关键词**（大小写不敏感）：`prd`, `req`, `requirement`, `需求`, `产品需求`, `功能需求`, `用户需求`, `业务需求`, `需求说明`, `需求规格`
  - **设计文档关键词**（大小写不敏感）：`design`, `设计`, `方案`, `开发方案`, `技术方案`, `详细设计`, `概要设计`, `系统设计`, `接口设计`, `架构设计`
  - 文件名同时命中两类 → 需求优先，标注"(需求关键词优先匹配)"
- 文件名中提取到的 `BANK-\d+` / `IP-\d+` ID 列表
- pytest.ini 是否存在

**输出探测摘要**：

```
环境探测结果：
  找到文件：N 个 docx/doc（需求候选：X 个，设计候选：Y 个，未分类：Z 个）
  检测到ID：BANK-XXXXX（来自文件名 xxx.docx）/ 无有效ID（过滤后）
  pytest.ini：✅ 检测到 / ❌ 未检测到
```

> 探测摘要中仅展示数字部分 ≥ 10000 的有效 ID；过滤掉的 ID（如 `BANK-999`）不显示。

---

### 步骤 1.2：交互式配置（单次合并展示）

将四个配置项合并为**一次 `AskUserQuestion` 调用**，`questions` 数组同时展示，用户在同一界面完成所有配置。

**选项构建规则（每个配置项）**：
- 检测到的候选最多取前 3 个，每个作为一个选项（标注来源说明）
- **严禁添加任何"手动输入"/"手动指定"/"自定义"类选项**（`AskUserQuestion` 自带 "Other"（即 "Type something"）输入框，这就是手动输入功能，再加选项完全重复）
- options 中只允许出现：检测到的候选项、"无"（可选项用）、"无，中断退出"（必填项无候选时用）
- 设计文档和自动化目录：末位加"无"选项
- 需求ID和需求文档为必填项，不加"无"选项

**需求ID 过滤规则**：

检测到的 ID 须同时满足以下条件才作为候选选项：
- 数字部分 ≥ 10000（即 `BANK-10000`/`IP-10000` 及以上）；小于 10000 的 ID（如 `BANK-999`）**忽略，不作为选项**
- 格式符合 `BANK-\d{5,}` 或 `IP-\d{5,}`

**无候选时的处理**：
- 需求ID 过滤后无有效候选：options 仅放一个"无，中断退出"选项（用户通过 Other 输入ID，或选此项中止流程）
- 需求文档无候选：同上，options 仅放"无，中断退出"
- 设计文档/自动化目录无候选：options 仅放"无"选项（可选项，不需要中断退出）

**`AskUserQuestion` 调用结构**：

> **⚠️ 严格按下方模板构建 options，不得添加模板中未列出的任何选项。用户自定义输入通过自带的 Other 完成。**

**示例：有1个需求ID候选、1个需求候选、无设计候选、无 pytest.ini 时的实际调用**：

```
questions:
  - header: "需求ID"
    question: "请选择或输入需求ID："
    multiSelect: false
    options:
      - label: "BANK-90819"
        description: "来自文件名：BANK-90819/"
  - header: "需求文档"
    question: "请选择需求文档（必填）："
    multiSelect: false
    options:
      - label: "ZA Search产品需求-part5.docx"
        description: "关键词匹配：产品需求"
  - header: "设计文档"
    question: "请选择设计文档（可选）："
    multiSelect: false
    options:
      - label: "无"
        description: "不提供设计文档，仅生成场景案例"
  - header: "自动化目录"
    question: "请选择自动化项目根目录（可选）："
    multiSelect: false
    options:
      - label: "无"
        description: "不关联自动化工程"
```

**完整模板（含所有可能的候选项占位）**：

```
questions:
  - header: "需求ID"
    question: "请选择或输入需求ID："
    multiSelect: false
    options:                              # ⚠️ 只放候选ID + 无候选时的"无，中断退出"，不得加其他选项
      - label: "{检测到的ID1}"          # 数字≥10000 的 ID 才加入
        description: "来自文件名：{来源文件名}"
      - label: "{检测到的ID2}"          # 若有（数字≥10000）
        description: "来自文件名：{来源文件名}"
      # 无候选时仅保留下面这一个选项：
      - label: "无，中断退出"
        description: "中止工作流，请确认文件名包含 BANK-XXXXX 后重试"

  - header: "需求文档"
    question: "请选择需求文档（必填）："
    multiSelect: false
    options:                              # ⚠️ 只放候选文件 + 无候选时的"无，中断退出"，不得加其他选项
      - label: "{需求候选文件1}"
        description: "关键词匹配：{命中的关键词}"
      - label: "{需求候选文件2}"          # 若有
        description: "关键词匹配：{命中的关键词}"
      # 无候选时仅保留下面这一个选项：
      - label: "无，中断退出"
        description: "中止工作流，请将需求文档放入当前目录后重试"

  - header: "设计文档"
    question: "请选择设计文档（可选）："
    multiSelect: false
    options:                              # ⚠️ 只放候选文件 + "无"，不得加其他选项
      - label: "{设计候选文件1}"
        description: "关键词匹配：{命中的关键词}"
      - label: "无"
        description: "不提供设计文档，仅生成场景案例"

  - header: "自动化目录"
    question: "请选择自动化项目根目录（可选）："
    multiSelect: false
    options:                              # ⚠️ 只放候选目录 + "无"，不得加其他选项
      - label: "当前目录"               # 仅当检测到 pytest.ini 时加入
        description: "检测到 pytest.ini：{CWD绝对路径}"
      - label: "无"
        description: "不关联自动化工程"
```

> 用户通过参数传入 `[需求ID]` 时，需求ID 问题仍然展示，但将传入的 ID 作为第一个选项（标注"来自命令参数"），方便用户确认或通过 Other 修改。
> 用户选择"无，中断退出"时，输出"工作流已中止"并停止执行。
> 用户通过 Other 输入自定义值时，直接使用该值（需求ID须校验格式：BANK-XXXXX 或 IP-XXXXX，数字≥10000，不合规则重询）。

**用户选 Other 输入值后的处理**：

收到 `AskUserQuestion` 结果后，检查各项是否为用户自定义输入（非选项中的 label）：
- 需求ID 为自定义输入 → 校验格式（BANK-XXXXX 或 IP-XXXXX，数字部分≥10000），不合规则用 `AskUserQuestion` 重询
- 需求文档 为自定义输入 → 校验文件是否存在，不存在则重询
- 设计文档 为自定义输入 → 输入 `无`/`-`/空 视为不提供；有效路径校验存在性
- 自动化目录 为自定义输入 → 输入 `无`/`-`/空 视为不提供；有效路径用 `Glob` 校验 `pytest.ini`，不存在则警告不阻断

---

### 步骤 1.2.5：补充检测需求文档所在目录

用户在步骤1.2中确认需求文档路径后，确定**根目录 = 需求文档所在目录**，立即执行：

**若根目录 ≠ CWD**（用户指定了其他目录的文档），同时并行执行以下两项：

**A. 扫描根目录文档和ID**

以根目录为基准重新扫描，结果用于更新设计文档和需求ID的候选选项：
- 用 `Glob` 扫描根目录下的 `*.docx`/`*.doc` 文件，按关键词分类（规则同步骤1.1）
- 扫描文件名中的 `BANK-\d+`/`IP-\d+` ID
- 检测根目录下是否存在 `pytest.ini`

扫描完成后，若发现新的候选（设计文档、ID、pytest.ini）与 CWD 扫描结果不同，**重新询问**设计文档、需求ID、自动化目录这三个配置项（需求文档已确认，不重询）。

> **终止条件**：根目录由步骤1.2首次确认的需求文档路径唯一决定，步骤1.2.5-A 的重询不允许用户更改需求文档路径，因此根目录不会再次变化，不存在循环风险。

**B. 检测根目录的 workflow.md**

- 用 `Glob` 检查根目录下是否存在 `workflow.md`
- 若存在 → 读取内容，用 `AskUserQuestion` 询问：
  ```
  在需求文档目录中检测到未完成的工作流记录：
    需求ID：BANK-XXXX
    上次执行到：<最后完成的步骤>

  选项：
    A. 继续该目录的未完成工作流
    B. 忽略，重新开始
  ```
  - 选A → 按步骤0.2进行有效性校验后续传（覆盖步骤1.2的配置）
  - 选B → 继续步骤1.3

**若根目录 = CWD**：跳过此步骤（阶段0已扫描，步骤1.2使用的就是该目录的结果）。

---

### 步骤 1.2.9：配置确认与执行计划展示

所有配置项（含步骤 1.2.5 的重询结果）确定后，在写入 workflow.md 之前，先向用户展示最终配置和执行计划，等待确认。

使用 `AskUserQuestion` 展示：

```
questions:
  - header: "确认配置"
    question: |
      请确认以下配置和执行计划：

      ━━━ 配置 ━━━
        需求ID：{BANK-XXXX}
        需求文档：{需求文档文件名}
        设计文档：{设计文档文件名 或 无}
        自动化目录：{自动化目录路径 或 无}
        根目录：{根目录绝对路径}

      ━━━ 执行计划 ━━━
        □ 阶段2：文档转换（docx → md + 编码修复）
        □ 阶段3.1：req-parser — 需求文档标准化
        □ 阶段3.2：design-parser — 设计文档规范化（如有设计文档）
        □ 阶段3.3：interface-extractor — 接口数据提取（如有设计文档）
        □ 阶段3.4：case-designer — 场景案例 + XMind 生成
        □ 阶段3.5：api-generator — API 测试代码生成（如有自动化目录且有接口数据）

      确认后将写入 workflow.md 并开始执行。
    multiSelect: false
    options:
      - label: "确认，开始执行"
        description: "写入 workflow.md 并按上述计划执行"
      - label: "重新配置"
        description: "返回步骤 1.2 重新选择配置项"
```

> 执行计划中，根据实际配置动态显示：无设计文档时不显示 3.2 和 3.3；无自动化目录时不显示 3.5。

**用户选"确认，开始执行"**：

1. 使用 `TaskCreate` 为执行计划中的每个阶段创建一个任务（根据配置动态决定创建哪些），示例：

```
TaskCreate: subject="阶段2：文档转换", description="docx → md + 编码修复", activeForm="转换文档"
TaskCreate: subject="阶段3.1：req-parser", description="需求文档标准化", activeForm="标准化需求文档"
TaskCreate: subject="阶段3.2：design-parser", description="设计文档规范化", activeForm="规范化设计文档"       # 仅有设计文档时
TaskCreate: subject="阶段3.3：interface-extractor", description="接口数据提取", activeForm="提取接口数据"     # 仅有设计文档时
TaskCreate: subject="阶段3.4：case-designer", description="场景案例 + XMind 生成", activeForm="生成场景案例"
TaskCreate: subject="阶段3.5：api-generator", description="API 测试代码生成", activeForm="生成API测试代码"   # 仅有自动化目录且有接口数据时
```

2. 进入步骤 1.3 写入 workflow.md
3. 后续每个阶段开始时用 `TaskUpdate` 将对应任务标记为 `in_progress`，完成后标记为 `completed`

**用户选"重新配置"**：回到步骤 1.2（重新展示四个配置项，使用当前已有的扫描结果）。

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

调用 `doc-converter` Skill，使用**单文件模式**直接转换到目标路径：
- 输入文件：需求文档（绝对路径）
- 输出文件：`<根目录绝对路径>/BANK-XXXX_PRD.md`

`doc-converter` 的单文件模式会自动创建输出目录并直接输出到指定路径，无需中间 temp/ 目录和 mv 操作。

---

### 步骤 2.2：转换设计文档（如有）

**触发条件**：阶段1配置的设计文档非空。

**分支A：设计文档与需求文档在同一目录**

步骤2.1 使用单文件模式已完成需求文档转换。设计文档同样使用单文件模式直接转换：

调用 `doc-converter` Skill，传入：
- 输入文件：设计文档（绝对路径）
- 输出文件：`<根目录绝对路径>/BANK-XXXX_DESIGN.md`

**分支B：设计文档在不同目录**

同样使用单文件模式：

调用 `doc-converter` Skill，传入：
- 输入文件：设计文档（绝对路径）
- 输出文件：`<根目录绝对路径>/BANK-XXXX_DESIGN.md`

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

### 步骤 3.1 + 3.2：req-parser 和 design-parser

> **重要分支判断（必须先执行）**：
> - **仅需求（无设计文档）时**：**禁止**使用 Task 工具派发子代理。直接在主流程中调用 `Skill(za-qe:req-parser)`，完成后将 3.1 标记为 `[x]`，跳过 3.2 和 3.3，直接进入步骤 3.4。
> - **同时存在需求文档和设计文档时**：使用 `Task` 工具同时派发两个子代理并行执行（见下文）。

#### 有设计文档时：并行派发子代理

派发前准备：读取以下两个 Skill 文件内容，后续传入各自子代理 prompt：
- req-parser 规范：`<插件根目录>/skills/req-parser/SKILL.md`
- design-parser 规范：`<插件根目录>/skills/design-parser/SKILL.md`

#### 子代理A：req-parser

Task prompt 须包含：
- req-parser SKILL.md 的完整内容（让子代理知晓规范）
- 输入文件绝对路径：`<根目录>/BANK-XXXX_PRD.md`
- 输出文件绝对路径：`<根目录>/BANK-XXXX_PRD.md`（覆盖写入）
- 可用工具：Read, Write, Edit, Glob, Grep
- 约束：不得修改 `workflow.md`
- 要求：输出中包含 `---STATUS---\nOK\n---END---` 或 `---STATUS---\nERROR <原因>\n---END---`

#### 子代理B：design-parser

Task prompt 须包含：
- design-parser SKILL.md 的完整内容（让子代理知晓规范）
- 输入文件绝对路径：`<根目录>/BANK-XXXX_DESIGN.md`
- 输出文件绝对路径：`<根目录>/BANK-XXXX_DESIGN.md`（覆盖写入）
- 可用工具：Read, Write, Edit, Glob, Grep
- 约束：不得修改 `workflow.md`
- 要求：输出中包含 `---STATUS---\nOK\n---END---` 或 `---STATUS---\nERROR <原因>\n---END---`

#### 等待两个子代理完成后，主流程处理结果

主流程用正则从各子代理输出中提取 `---STATUS---\n(.*?)\n---END---` 判断状态（全文扫描，不依赖最后一行）：

- 两者均 `OK` → 用 `Edit` 将 `workflow.md` 中 3.1 和 3.2 均标记为 `[x]`，追加产出文件记录，立即进入步骤3.3
- 子代理A失败 → 将 3.1 标记为 `[!]`，中止后续执行（design-parser 结果已产出可保留）
- 子代理B失败 → 将 3.2 标记为 `[!]`，中止后续执行（req-parser 结果已产出可保留）

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
- `/za-qe:req-parser` — 独立执行需求文档标准化
- `/za-qe:design-parser` — 独立执行设计文档规范化
- `/za-qe:interface-extractor` — 独立执行接口数据提取
- `/za-qe:case-designer` — 独立执行场景案例设计
- `/za-qe:api-generator` — 独立执行 API 用例生成


