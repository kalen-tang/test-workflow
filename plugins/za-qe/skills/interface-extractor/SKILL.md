---
name: interface-extractor
description: 当用户要求"提取接口信息"、"分析开发方案"、"接口数据提取"、"提取接口"、"接口校验"、"微服务映射"、"分析设计文档接口"、"从udoc提取接口"，或提到接口提取、接口分析、测试左移分析时，应使用此技能。
status: active
---

# 接口数据提取器

## 技能目标

从规范化设计文档中提取结构化的接口信息，输出符合 `08-interface-data-report` 格式规范的**接口数据报告**，供 `case-designer` 和 `api-generator` 消费。

**职责边界**：
- **做**：接口信息提取、接口路径校验（dmb 网关检测）、微服务识别与映射、接口参数结构化、接口间依赖关系分析
- **不做**：测试场景设计（由 case-designer 负责）、测试用例推荐（由 case-designer 负责）

## 输入

### 必须输入

- **规范化设计文档**（design-parser 产出的 md 文件，**不读取原始 doc/docx**）
  - 提供接口技术规格（路径、请求参数、响应参数）
  - 提供接口间的技术调用关系

### 可选输入

- **规范化需求文档**（req-parser 产出的 md 文件）
  - 用于补充接口的业务上下文（功能描述、关联需求编号）
  - 有需求文档时，输出的接口信息会包含"关联需求"字段

## 输出

**接口数据报告**（Markdown 格式），符合 `references/interface-data-report.md` 规范。

输出文件：`<输出目录>/<项目名>_接口数据报告.md`

## 执行流程

### 步骤 1：读取输入文档

1. 读取规范化设计文档（md 格式）
2. 如提供了规范化需求文档，也一并读取
3. 识别文档结构和章节

### 步骤 2：提取接口信息

从设计文档中提取每个接口的完整信息：

**基础信息**：
- **接口名称**：API 接口的业务名称
- **接口路径**：RESTful API 的 URL 路径（需包含微服务域名+接口路径）
- **请求方法**：HTTP 方法（GET、POST、PUT、DELETE 等）
- **Content-Type**：请求内容类型
- **功能描述**：接口实现的业务功能

**参数信息**：
- **请求参数**：参数名、类型、是否必填、说明、示例值、取值范围
- **响应参数**：字段名、类型、说明、示例值（含嵌套结构）
- **错误码**：错误码、HTTP 状态码、说明

**业务规则**：
- 接口级别的业务规则和约束

**提取来源**：
1. **直接提取**：设计文档中直接列出的接口定义
2. **从 UDoc 链接提取**：如文档中包含 UDoc 链接（域名 `udoc.in.za`），使用 Playwright MCP 提取接口定义

### 步骤 3：接口路径校验

提取接口路径后，执行以下校验：

1. **网关接口检测**：
   - 路径包含 `dmb` → 判定为网关接口
   - **必须提示用户**：检测到网关接口，需替换为微服务接口路径
   - 暂停该接口分析，等待用户提供微服务接口

2. **微服务识别**：
   - 路径不含 `dmb` → 根据路径前缀识别微服务
   - 映射规则参见 `references/interface-validation.md`

3. **完整路径格式**：
   - 标准格式：`微服务域名 + 接口路径`
   - 示例：`zabank_imc_activity_service/activity/list`
   - 如文档只提供接口路径，根据映射规则补充微服务域名

> 详细规则：`references/interface-validation.md`

### 步骤 4：接口依赖关系分析

分析接口间的数据传递关系：

1. **ID 传递识别**：接口 A 响应中的 `xxxId` 字段出现在接口 B 请求参数中
2. **状态关联识别**：接口 A 修改状态后，接口 B 查询该状态
3. **数据流向识别**：接口 A 创建数据，接口 B 查询/修改/删除该数据
4. **CRUD 模式识别**：
   - create/add/save → get/query/list → update/modify → delete/remove
   - submit → review/audit → approve/reject

### 步骤 5：关联需求（可选）

如提供了规范化需求文档：
- 将接口与需求功能编号（F001、F002 等）关联
- 从需求文档补充接口的业务描述

### 步骤 6：生成接口数据报告

按照 `08-interface-data-report` 格式输出 Markdown 文件，包含：

1. **概览**：接口总数、微服务列表、网关接口数
2. **接口路径校验**：网关检测结果、微服务接口清单
3. **接口详情**：每个接口的完整信息
4. **接口依赖关系**：依赖链 + 依赖关系图
5. **微服务映射**：按微服务分组的接口清单

## 文档质量检查

提取前检查设计文档质量：
- 是否包含完整的接口设计信息（直接列出或提供 UDoc 链接）
- 接口参数说明是否详细完整
- 是否包含错误码信息

如文档不符合规范，提示用户完善文档信息。

## UDoc 接口提取

如设计文档中包含 UDoc 链接：

**Playwright MCP 安装**（如未安装）：
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

**UDoc 登录信息**（域名 `udoc.in.za`）：
- 账号：`admin`
- 密码：`Za123456`

## 额外资源

### 参考文件

- **`references/interface-validation.md`** - 接口路径校验与微服务映射规则
- **`references/output-format.md`** - 接口数据报告输出格式参考

### 示例文件

- **`examples/sample-analysis-report.md`** - 接口数据报告示例
- **`examples/interface-mapping.json`** - 微服务映射配置示例

### 相关 Artifact Schemas

- **`references/interface-data-report.md`** - 接口数据报告格式规范
- **`references/normalized-design.md`** - 输入：标准化设计文档格式

### 下游 Skills

- **`../case-designer/SKILL.md`** - 消费接口数据报告，设计测试场景
- **`../api-generator/SKILL.md`** - 消费接口数据报告，生成测试代码
