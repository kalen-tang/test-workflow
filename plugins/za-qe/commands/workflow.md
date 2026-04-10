---
name: qe-workflow
description: 测试左移全流程工作流：自动探测环境、转换文档、串联分析技能，从需求/设计文档生成API自动化测试用例
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
---

# 测试左移全流程工作流

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
  → devplan-analyzer → 测试左移分析报告
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
   - 如果不存在，使用 `mkdir -p` 创建

4. **自动化项目目录验证**（如果非空）：
   - 必须存在 `pytest.ini` 文件

---

## 阶段 2：文档转换

### 步骤 2.1：转换需求文档

对需求文档目录中的每个 `.doc`/`.docx` 文件，执行转换：

```bash
uvx markitdown '<需求文档路径>' > '<案例输出目录>/<原文件名>.md'
```

**示例**：
```bash
uvx markitdown './docs/req/ZA Search产品需求-part5.docx' > './result/ZA Search产品需求-part5.md'
```

**注意事项**：
- 文件名保持与原文件一致，仅将扩展名改为 `.md`
- 如果文件名包含空格或特殊字符，使用引号包裹路径
- 逐个文件转换，每个转换完成后检查是否成功（文件是否存在且非空）
- 如果某个文件转换失败，记录错误并继续处理下一个文件

### 步骤 2.2：转换设计文档（可选）

如果设计文档目录非空且存在 doc/docx 文件：

```bash
uvx markitdown '<设计文档路径>' > '<案例输出目录>/design_<原文件名>.md'
```

**注意**：设计文档输出时添加 `design_` 前缀，避免与需求文档同名冲突。

**如果设计文档目录与需求文档目录相同**：跳过此步骤（需求文档已在步骤 2.1 中转换）。此时无法区分哪些是需求文档、哪些是设计文档，后续阶段 3 会将所有 md 文件同时作为输入。

### 步骤 2.3：编码检查与修复

对阶段 2 生成的**所有 md 文件**，逐一执行编码检查：

```bash
python -c "
import sys
path = sys.argv[1]
with open(path, 'rb') as f:
    raw = f.read()
try:
    raw.decode('utf-8')
    print(f'OK: {path} is valid UTF-8')
except UnicodeDecodeError:
    for enc in ['utf-8-sig', 'gb18030', 'big5', 'utf-16']:
        try:
            text = raw.decode(enc)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'FIXED: {path} converted from {enc} to UTF-8')
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        print(f'WARN: {path} encoding unknown, may need manual check')
" '<md文件路径>'
```

**编码检测优先级**：`utf-8` → `utf-8-sig`（带BOM） → `gb18030`（覆盖 gbk/gb2312） → `big5` → `utf-16`

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

### 决策逻辑

根据阶段 2 生成的文件，自动决定调用哪些 Skills：

```
有需求 md 且有设计 md？
  → req-parser → design-parser → devplan-analyzer（完整模式）→ api-generator

仅有设计 md（无需求文档）？
  → design-parser → devplan-analyzer（基础模式）→ api-generator

仅有需求 md（无设计文档）？
  → req-parser → 提示用户可手动调用 case-designer 或 devplan-analyzer
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

### 步骤 3.3：调用 devplan-analyzer

**触发条件**：步骤 3.1 或 3.2 至少有一个产出

**两种模式**：

1. **完整模式**（有需求文档 + 设计文档）：
   - 输入：规范化需求文档 + 规范化设计文档
   - 按 devplan-analyzer「模式二」执行
   - 输出：完整的测试左移分析报告（含场景用例 + 需求覆盖度分析）

2. **基础模式**（仅有设计文档）：
   - 输入：规范化设计文档
   - 按 devplan-analyzer「模式一」执行
   - 输出：基础的测试左移分析报告

**输出文件**：`<案例输出目录>/<项目名>_测试左移分析报告.md`

### 步骤 3.4：调用 api-generator

**触发条件**：步骤 3.3 产出了测试左移分析报告

- **输入**：测试左移分析报告路径
- **输出目录**：
  - 如果指定了自动化项目目录 → 测试代码和数据输出到该目录下
  - 否则 → 输出到案例输出目录下

**调用方式**：按照 api-generator Skill 的流程执行

### 仅有需求文档的特殊处理

如果用户仅提供了需求文档（无设计文档），在 req-parser 完成后：
1. 输出已完成的分析结果
2. 提示用户后续可选操作：
   ```
   需求文档分析已完成，由于未提供设计文档，无法自动生成接口测试用例。

   后续可选操作：
     1. /za-qe:qe-gencase <规范化需求文档路径>  — 生成手工测试案例（PlantUML流程图 + MindMap）
     2. 提供设计文档后重新执行 /za-qe:qe-workflow — 生成完整的 API 自动化测试
     3. /devplan-analyzer <设计文档路径> — 手动分析设计文档
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

📄 阶段1 - 文档转换 ✅
   需求文档：3 个已转换
   设计文档：1 个已转换
   编码修复：1 个（gb18030 → UTF-8）

📊 阶段2 - 需求分析 ✅
   输出：./result/xxx_规范化需求文档.md

🔧 阶段3 - 设计分析 ✅
   输出：./result/xxx_规范化开发方案.md

📋 阶段4 - 测试左移分析 ✅
   输出：./result/xxx_测试左移分析报告.md
   识别接口：11 个
   场景用例：5 个

🧪 阶段5 - API 用例生成 ✅
   输出目录：./zabank_imc_case/
   测试代码：11 个
   测试数据：33 个

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 下一步操作：
  1. 查看测试左移分析报告：
     cat ./result/xxx_测试左移分析报告.md

  2. 执行测试用例：
     cd ./zabank_imc_case && pytest --envId sit

  3. 生成手工测试案例（可选）：
     /za-qe:qe-gencase ./result/xxx_规范化需求文档.md
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

- `/za-qe:qe-gencase` - 生成场景测试案例（PlantUML流程图 + MindMap）
- `/za-qe:qe-help` - 查看详细帮助
- `/req-parser` - 独立执行需求文档标准化
- `/design-parser` - 独立执行设计文档规范化
- `/devplan-analyzer` - 独立执行测试左移分析
- `/api-generator` - 独立执行 API 用例生成

## 详细文档

- [devplan-analyzer 文档](../skills/devplan-analyzer/SKILL.md)
- [req-parser 文档](../skills/req-parser/SKILL.md)
- [design-parser 文档](../skills/design-parser/SKILL.md)
- [api-generator 文档](../skills/api-generator/SKILL.md)
- [插件 README](../README.md)

---

**版本**: v2.0.0 | **状态**: ✅ 可用
