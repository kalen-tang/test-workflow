---
name: plantuml-validator
description: 验证 PlantUML 代码语法正确性并自动修复错误。当用户说"验证 PlantUML"、"检查流程图语法"、"修复 PlantUML 错误"、"PlantUML 渲染报错"、"帮我检查一下这个 plantuml"时应触发。也可由其他 Skill（如 case-designer）在生成 PlantUML 后自动调用。
status: active
allowed-tools: Read, Edit, Bash(uv run:*), Bash(uv *)
---

# PlantUML 语法验证器

## 技能目标

验证 PlantUML 代码块的语法正确性，通过调用 `plantuml.in.za` 渲染服务检测，发现错误后自动修复，反复迭代直到所有代码块通过验证。

## 输入

- **PlantUML 代码块**：直接传入的 `@startuml...@enduml` 或 `@startmindmap...@endmindmap` 代码
- **Markdown 文件路径**：含 PlantUML 代码块的 `.md` 文件，脚本自动提取所有代码块逐一验证

## 执行流程

### 步骤 1：调用验证脚本

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/validate_plantuml.py" --file <文件绝对路径>
```

或直接传入代码块内容（适合单个代码块）：

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/validate_plantuml.py" "@startuml\n...\n@enduml"
```

### 步骤 2：解读脚本输出

脚本对每个代码块输出一行：

- `OK: <序号> <渲染URL>` → 该代码块语法正确，附渲染预览链接
- `ERROR: <序号> <错误描述> → <渲染URL>` → 该代码块存在语法错误

**退出码**：`0` 全部通过，`1` 存在错误，`2` 参数错误。

### 步骤 3：修复错误代码块

若存在 `ERROR` 输出：

1. 根据错误描述和序号定位对应代码块
2. 分析错误原因（常见错误见下方参考）
3. 修正代码块内容
4. 若输入是文件，用 `Edit` 工具更新文件中对应代码块
5. 重新执行步骤1，验证修复是否生效

**重复步骤1-5，直到所有代码块输出均为 `OK`。**

> **最大重试次数**：单个代码块修复尝试不超过 5 次。若 5 次后仍有错误，输出当前错误状态并提示人工介入。

### 步骤 4：输出验证结果

全部通过后输出汇总：

```
PlantUML 验证完成
  通过：N 个代码块
  渲染预览：
    代码块1: https://plantuml.in.za/svg/xxx
    代码块2: https://plantuml.in.za/svg/xxx
```

## 常见 PlantUML 错误及修复方法

### 1. `@start` 标记类型不匹配

```plantuml
@startuml          ← 应与结尾 @end 类型一致
...
@endmindmap        ← 错误：应为 @enduml
```

**修复**：确保开始和结束标记类型一致（`@startuml/@enduml`、`@startmindmap/@endmindmap`）。

### 2. MindMap 缩进层级错误

```plantuml
@startmindmap
* 根节点
*** 跳过了二级节点    ← 错误：不能直接从一级跳到三级
@endmindmap
```

**修复**：层级必须连续，不能跳跃。

### 3. Activity Diagram 语法错误

```plantuml
@startuml
if (条件) then      ← 缺少括号内的判断文字
...
@enduml
```

**修复**：`if` 语句格式为 `if (条件?) then (是) ... else (否) ... endif`。

### 4. 特殊字符未转义

中文括号、特殊符号在某些位置需要用引号包裹：

```plantuml
:用户输入（必填）;    ← 中文括号可能导致解析歧义
```

**修复**：改为 `:"用户输入（必填）";` 或使用英文括号。

### 5. 主题声明位置错误

```plantuml
@startmindmap
* 根节点
!theme materia     ← 错误：主题必须在根节点之前声明
@endmindmap
```

**修复**：`!theme` 必须紧跟在 `@start` 后，内容之前。

## 与其他 Skill 的集成

`case-designer` 生成 PlantUML 代码后，可直接调用本 Skill 验证：

```bash
# case-designer 生成 BANK-XXXX_CASE.md 后验证所有代码块
uv run "${CLAUDE_SKILL_DIR}/scripts/validate_plantuml.py" --file <根目录>/BANK-XXXX_CASE.md
```

---

**状态**: ✅ 可用 | **版本**: v1.0.0
