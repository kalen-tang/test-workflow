---
name: qe-workflow
description: 测试左移全流程工作流：自动探测环境、转换文档、串联分析技能，从需求/设计文档生成API自动化测试用例
argument-hint: [--req_dir dir] [--design_dir dir] [--output_dir dir] [--project_dir dir]
arguments:
  - name: req_dir
    description: 需求文档目录路径（可选，跳过交互引导直接使用）
    required: false
  - name: design_dir
    description: 设计文档目录路径（可选，默认同需求文档目录，传 "none" 表示无设计文档）
    required: false
  - name: output_dir
    description: 案例输出目录路径（可选，默认同需求文档目录）
    required: false
  - name: project_dir
    description: 自动化项目目录路径（含 pytest.ini，可选）
    required: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Skill
  - Bash(uv *)
---

# 测试左移全流程工作流

> **执行约束（必须遵守）**：
> - 所有 Bash 命令必须使用**绝对路径**，禁止 `cd` 切换目录
> - **禁止使用分号 `;` 连接命令**，包括 `; echo "Exit code: $?"`、`; echo "EXIT:$?"`、`|| echo "失败"` 等任何退出码检查形式
> - 命令失败时 Bash 会直接报错，无需手动检查退出码；需要顺序执行时改用 `&&`

自动完成从原始文档到 API 自动化测试用例的全流程：环境探测 → 目录配置 → docx/doc 转 md → 编码修复 → 需求/设计分析 → API 用例生成。

## 工作流概览

```
阶段1：环境探测 + 目录配置
  扫描当前目录 → 检测 docx/doc 文件 → 检测 pytest.ini
  → 交互式确认/修改四个目录

阶段2：文档转换
  需求文档 docx/doc → markitdown → .md
  设计文档 docx/doc → markitdown → .md（可选）
  → 编码检查 → UTF-8 修复

阶段3：Skill 串联
  需求 md → req-parser → 规范化需求文档
  设计 md → design-parser → 规范化设计文档
  → interface-extractor → 接口数据报告
  → case-designer → 场景案例 + 场景案例表
  → api-generator → API 自动化测试用例
```

## 使用方式

```bash
# 交互模式（推荐）：自动探测环境后引导配置
/za-qe:qe-workflow

# 指定参数模式：跳过交互直接执行
/za-qe:qe-workflow --req_dir ./docs/requirement --output_dir ./result

# 完整参数模式
/za-qe:qe-workflow --req_dir ./docs/req --design_dir ./docs/design --output_dir ./result --project_dir ./zabank_imc_case
```

---

## 阶段 1：环境探测 + 目录配置

### 步骤 1.1：自动探测当前环境

**如果用户未提供任何参数**，自动执行环境探测：

1. **扫描 docx/doc 文件**：使用 `Glob` 工具搜索当前工作目录下的 `*.docx` 和 `*.doc` 文件
   - 如果找到 docx/doc 文件，将当前目录预设为**需求文档目录**默认值
   - 记录找到的文件数量和文件名列表

2. **检测 pytest.ini**：使用 `Glob` 工具检查当前目录是否存在 `pytest.ini`
   - 如果找到，将当前目录预设为**自动化项目目录**默认值

3. **输出探测结果**：
   ```
   环境探测结果：
     docx/doc 文件：找到 N 个（当前目录）
     pytest.ini：✅ 检测到 / ❌ 未检测到
   ```

### 步骤 1.2：交互式目录配置

使用 `AskUserQuestion` 工具向用户展示探测到的默认值，引导配置四个目录。

**配置项说明**：

| 配置项 | 是否必填 | 默认值逻辑 | 说明 |
|--------|---------|-----------|------|
| 需求文档目录 | 必填 | 如当前目录有 docx/doc → 当前目录 | 存放 .doc/.docx 需求文档的目录 |
| 设计文档目录 | 可选 | 默认同需求文档目录 | 存放 .doc/.docx 设计文档的目录，置空表示无设计文档 |
| 案例输出目录 | 可选 | 默认同需求文档目录 | 转换后的 md 及后续产出的存放目录 |
| 自动化项目目录 | 可选 | 如当前目录有 pytest.ini → 当前目录 | 存在 pytest.ini 的自动化项目根目录 |

**交互方式**：

向用户展示以下配置表，让用户确认或修改：

```
当前配置（基于环境探测）：

  1. 需求文档目录：{探测到的默认值 或 "未检测到，请输入"}
     找到文件：file1.docx, file2.doc, ...

  2. 设计文档目录：{默认同需求文档目录}
     说明：可置空表示无设计文档

  3. 案例输出目录：{默认同需求文档目录}

  4. 自动化项目目录：{探测到的默认值 或 "未检测到，可留空"}
```

- 用户可以对任意项进行修改
- 用户可以将非必填项置空（输入空字符串或 "none"）
- 设计文档目录如果与需求文档目录相同，后续扫描时会区分文件类型

**如果用户提供了参数**（如 `--req_dir ./docs`），直接使用参数值，跳过交互引导。

### 步骤 1.3：验证配置

1. **需求文档目录验证**：
   - 目录必须存在
   - 目录下至少存在一个 `.doc` 或 `.docx` 文件
   - 如果不满足，提示用户重新输入

2. **设计文档目录验证**（如果非空）：
   - 目录必须存在
   - 扫描 `.doc`/`.docx` 文件列表

3. **案例输出目录**：
   - 如果不存在，使用 `uv run mkdir -p` 创建（或通过 Glob 检测后用 Write 工具写入占位）
   - 目录确认后，立即使用 Write 工具在输出目录下写入 `.workflow_session` 文件（内容为当前时间戳），**触发一次文件写入权限确认**，让用户选择 "Yes, allow all edits during this session"，后续所有文件写入不再逐个询问

4. **自动化项目目录验证**（如果非空）：
   - 必须存在 `pytest.ini` 文件

---

## 阶段 2：文档转换

步骤 2.1、2.2、2.3 统一使用 `convert_docx.py` 脚本完成，转换和编码修复一次完成。

### 步骤 2.1：转换需求文档

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/scripts/convert_docx.py" '<需求文档目录绝对路径>' '<案例输出目录绝对路径>'
```

**示例**：
```bash
uv run "${CLAUDE_PLUGIN_ROOT}/scripts/convert_docx.py" 'D:/story/2026/BANK-91153' 'D:/story/2026/BANK-91153'
```

### 步骤 2.2：转换设计文档（可选）

如果设计文档目录非空且与需求文档目录不同：

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/scripts/convert_docx.py" '<设计文档目录绝对路径>' '<案例输出目录绝对路径>' --prefix design_
```

`--prefix design_` 确保输出文件名加 `design_` 前缀，避免与需求文档同名冲突。

**如果设计文档目录与需求文档目录相同**：跳过此步骤（需求文档已在步骤 2.1 中转换）。

### 步骤 2.3：编码检查与修复

已由 `convert_docx.py` 内置处理，无需单独执行。脚本输出：
- `OK: <path>` — 已是 UTF-8
- `FIXED: <path> from <enc>` — 已从 enc 转换为 UTF-8
- `WARN: <path>` — 编码无法识别，需人工检查
- `ERROR: <path> <msg>` — 转换失败

### 步骤 2.4：转换结果汇报

转换完成后，输出汇总：

```
文档转换完成：
  需求文档：N 个转换成功，M 个失败
  设计文档：N 个转换成功，M 个失败
  编码修复：N 个已修复

生成的 md 文件列表：
  - ./result/需求文档1.md (UTF-8 ✅)
  - ./result/需求文档2.md (UTF-8 ✅, 从 gb18030 转换)
  - ./result/design_设计文档1.md (UTF-8 ✅)
```

如果有失败的文件，列出失败原因并提示用户检查原始文档。

---

## 阶段 3：Skill 串联

> **重要原则**：阶段 3 的所有 Skill 一律读取阶段 2 产出的 **md 文件**，**不得直接读取原始 doc/docx 文件**。原始文档仅在阶段 2 由 markitdown 处理。

### 决策逻辑

根据阶段 2 生成的文件，自动决定调用哪些 Skills：

```
有需求 md 且有设计 md？
  → req-parser → design-parser → interface-extractor → case-designer → api-generator

仅有设计 md（无需求文档）？
  → design-parser → interface-extractor → api-generator（无场景表，基于接口生成基础用例）

仅有需求 md（无设计文档）？
  → req-parser → case-designer（仅基于需求，无接口数据）
```

### 步骤 3.1：调用 req-parser（如有需求 md）

**触发条件**：存在需求文档转换后的 md 文件

对每个需求 md 文件调用 `req-parser` Skill：
- **输入**：转换后的需求 md 文件路径
- **输出**：`<案例输出目录>/<模块名>_规范化需求文档.md`

**调用方式**：按照 req-parser Skill 的流程执行，即：
1. 解析 md 文档结构
2. 提取功能、验收标准、业务规则
3. 生成 given-when-then 测试场景
4. 执行三级一致性检查
5. 输出规范化需求文档

### 步骤 3.2：调用 design-parser（如有设计 md）

**触发条件**：存在设计文档转换后的 md 文件（`design_*.md`）

对每个设计 md 文件调用 `design-parser` Skill：
- **输入**：转换后的设计 md 文件路径
- **输出**：`<案例输出目录>/<需求ID>_规范化开发方案.md`

**调用方式**：按照 design-parser Skill 的流程执行，即：
1. 读取 md 文档
2. 提取 UDOC 链接中的接口数据（如有）
3. 检查并补全内容
4. 生成规范化 MD 文档
5. 输出待补充清单（如有缺失）

### 步骤 3.3：调用 interface-extractor（如有设计文档产出）

**触发条件**：步骤 3.2 产出了规范化设计文档

- **输入**：
  - 规范化设计文档（必须）
  - 规范化需求文档（可选，用于补充业务上下文）
- **输出**：`<案例输出目录>/<项目名>_接口数据报告.md`

**调用方式**：按照 interface-extractor Skill 的流程执行：
1. 提取接口信息（路径、参数、响应）
2. 接口路径校验（dmb 网关检测）
3. 微服务识别与映射
4. 接口依赖关系分析
5. 输出接口数据报告

### 步骤 3.4：调用 case-designer（如有需求文档产出）

**触发条件**：步骤 3.1 产出了规范化需求文档

- **输入**：
  - 规范化需求文档（必须）
  - 接口数据报告（可选，步骤 3.3 产出）
- **输出**：
  - `<案例输出目录>/<项目名>_场景案例.md`（PlantUML 流程图 + MindMap）
  - `<案例输出目录>/<项目名>_场景案例表.md`（结构化场景表，供 api-generator 消费）
  - `.puml` 文件和 `.xmind` 文件

**调用方式**：按照 case-designer Skill 的流程执行

### 步骤 3.5：调用 api-generator

**触发条件**：步骤 3.3 产出了接口数据报告

- **输入**：
  - 接口数据报告（必须，步骤 3.3 产出）
  - 场景案例表（可选，步骤 3.4 产出，有则生成场景测试代码）
- **输出目录**：
  - 如果指定了自动化项目目录 → 测试代码和数据输出到该目录下
  - 否则 → 输出到案例输出目录下

**调用方式**：按照 api-generator Skill 的流程执行

### 仅有需求文档的特殊处理

如果用户仅提供了需求文档（无设计文档），在 req-parser + case-designer 完成后：
1. 输出已完成的分析结果（规范化需求文档 + 场景案例）
2. 提示用户后续可选操作：
   ```
   需求文档分析和场景案例设计已完成。由于未提供设计文档，无法提取接口数据，因此无法自动生成 API 测试代码。

   已生成：
     - 规范化需求文档
     - 场景案例（PlantUML 流程图 + MindMap + XMind）
     - 场景案例表（步骤中的"调用接口"列为空，待补充接口数据）

   后续可选操作：
     1. 提供设计文档后重新执行 /za-qe:qe-workflow — 生成完整的 API 自动化测试
     2. 手动补充场景案例表中的接口信息后调用 /api-generator
   ```

---

## 执行成功输出

```
🚀 测试左移全流程工作流执行完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 目录配置：
   需求文档目录：./docs/req
   设计文档目录：./docs/design
   案例输出目录：./result
   自动化项目目录：./zabank_imc_case

📄 文档转换 ✅
   需求文档：3 个已转换
   设计文档：1 个已转换
   编码修复：1 个（gb18030 → UTF-8）

📊 需求分析 (req-parser) ✅
   输出：./result/xxx_规范化需求文档.md

🔧 设计分析 (design-parser) ✅
   输出：./result/xxx_规范化开发方案.md

🔌 接口提取 (interface-extractor) ✅
   输出：./result/xxx_接口数据报告.md
   识别接口：11 个
   接口依赖链：3 条

📋 场景案例 (case-designer) ✅
   输出：./result/xxx_场景案例.md
   输出：./result/xxx_场景案例表.md
   场景数量：8 个（P0: 3, P1: 3, P2: 2）

🧪 API 用例生成 (api-generator) ✅
   输出目录：./zabank_imc_case/
   测试代码：11 个
   测试数据：33 个

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 下一步操作：
  1. 查看接口数据报告：
     cat ./result/xxx_接口数据报告.md

  2. 查看场景案例：
     cat ./result/xxx_场景案例表.md

  3. 执行测试用例：
     cd ./zabank_imc_case && pytest --envId sit
```

---

## 错误处理

### 错误 1：需求文档目录无 doc/docx 文件

```
❌ 错误：需求文档目录下未找到 .doc/.docx 文件
   目录：./docs/req

建议：
- 检查目录路径是否正确
- 确认目录下存在 Word 格式的需求文档
- 如果文档已经是 .md 格式，可直接使用 /req-parser 处理
```

**处理**：停止执行，要求用户重新输入需求文档目录。

### 错误 2：markitdown 转换失败

```
⚠️ 警告：文档转换失败
   文件：./docs/req/需求文档V2.doc
   错误：markitdown 执行错误

建议：
- 检查文件是否损坏
- 尝试用 Word 打开后另存为 .docx 格式
- 手动转换为 Markdown 格式
```

**处理**：跳过失败文件，继续处理其他文件。全部完成后汇报失败列表。

### 错误 3：编码无法识别

```
⚠️ 警告：文件编码无法自动识别
   文件：./result/xxx.md

建议：
- 手动检查文件编码
- 尝试用文本编辑器打开并另存为 UTF-8
```

**处理**：标记警告，继续后续流程。

### 错误 4：Skill 执行失败

```
❌ 步骤 N 失败：{Skill名称} 执行未完成

已完成的步骤：
  ✅ 步骤 1 - 文档转换
  ✅ 步骤 2 - 需求分析
  ❌ 步骤 3 - 设计分析（失败）
  ⏸️ 步骤 4 - 测试左移分析（未执行）
  ⏸️ 步骤 5 - API 用例生成（未执行）

建议：
- 检查步骤 N 的输入文件
- 查看错误详情
- 修复问题后可从失败步骤手动继续
```

**处理**：停止后续 Skill 串联，保留已完成步骤的输出。

---

## 相关命令

- `/za-qe:qe-gencase` - 生成场景案例（PlantUML流程图 + MindMap）
- `/za-qe:qe-help` - 查看详细帮助
- `/req-parser` - 独立执行需求文档标准化
- `/design-parser` - 独立执行设计文档规范化
- `/interface-extractor` - 独立执行接口数据提取
- `/case-designer` - 独立执行场景案例设计
- `/api-generator` - 独立执行 API 用例生成

## 详细文档

- [interface-extractor 文档](../skills/interface-extractor/SKILL.md)
- [case-designer 文档](../skills/case-designer/SKILL.md)
- [req-parser 文档](../skills/req-parser/SKILL.md)
- [design-parser 文档](../skills/design-parser/SKILL.md)
- [api-generator 文档](../skills/api-generator/SKILL.md)
- [插件 README](../README.md)

---

**版本**: v2.0.0 | **状态**: ✅ 可用
