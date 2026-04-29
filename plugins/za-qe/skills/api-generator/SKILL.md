---
name: api-generator
description: 此技能应在用户询问"生成API测试用例"、"生成接口测试代码"、"根据接口文档生成自动化测试"、"生成API自动化测试"、"创建接口测试用例"或"为API端点生成测试数据"时使用。基于银行标准测试框架（pytest_zabank系列插件）生成标准化测试代码和YAML数据。
version: 2.0.0
status: active
allowed-tools: Read Write Edit Glob Grep
---

# 银行标准测试框架 - API测试用例生成器

## 技能目标

从接口数据和场景案例生成完整的API自动化测试套件，基于银行标准测试框架（pytest_zabank系列插件），包含标准化测试代码、变量化测试数据和执行脚本。

## 核心特性

- 银行标准框架：基于 pytest_zabank 系列插件（pytest_zabank_wholesale、pytest_zati_base）
- 数据驱动测试：使用 `@pytest.mark.data()` 装饰器自动加载 YAML
- 变量化配置：使用 `variables` 定义测试变量，支持 `data.render()` 动态渲染
- Scenario 模式：测试方法传入 Step 对象，Scenario 内部处理断言和日志
- 智能 Fixture：本服务简化命名，跨服务完整命名，自动检测

## 输入来源

按优先级：
1. **接口数据报告 + 场景案例表**（推荐）：interface-extractor 产出 + case-designer 产出
2. **仅接口数据报告**：基于接口定义生成基础测试用例（无场景串联）
3. **旧格式兼容**：直接传入包含接口信息和测试用例的 Markdown 文件

### 格式 A：接口数据报告 + 场景案例表（推荐）

两个独立的 Markdown 文件：

1. **接口数据报告**（`08-interface-data-report` 格式）— 提供接口路径、请求方法、请求参数表、响应参数表、错误码表、接口依赖关系
2. **场景案例表**（`09-scenario-table` 格式）— 提供场景总览、场景详情（前置条件、步骤表、验证点）、数据传递标记（`{{步骤N.字段名}}`）

**消费方式**：
- 从接口数据报告获取接口定义 → 生成 pytest 函数骨架和 YAML 数据结构
- 从场景案例表获取测试场景 → 生成 Scenario 测试和断言逻辑
- 将 `{{步骤N.字段名}}` 转换为变量提取和传递代码

### 格式 B：仅接口数据报告

只有接口定义，无场景案例表时，为每个接口生成独立的单接口测试用例（正常/异常/边界），不生成跨接口的场景测试。

## 实施工作流

### 步骤1：分析输入并识别服务

1. 解析文档：提取所有接口信息（路径、方法、参数、响应）和测试用例场景，识别优先级（P0/P1/P2）
2. 从 API 路径前缀自动检测服务类型，定位对应的 service 目录
3. 从项目路径提取项目名称（如 `zabank-eln-case` → `eln`），用于判断本服务 vs 跨服务

### 步骤2：获取服务信息

1. 读取 `service/{service_name}/__init__.py` 获取接口映射和 Model 类
2. 根据服务映射定位 scenario 文件
3. 从 `config/{env}.yaml` 获取服务 host 配置

> Service层缺失时的处理方案参见 `references/edge-cases.md`

### 步骤3：确保 Scenario Fixture

**Fixture 命名规则**：

使用自动检测逻辑判断本服务 vs 跨服务：
- 本服务（current_project 在 service_name 中）：简化命名，仅保留最后部分 + `_sc`
- 跨服务：完整命名，保留所有中间层 + `_sc`

| 服务名称 | 当前项目 | Fixture 名称 | 说明 |
|---------|---------|-------------|-----|
| zabank_eln_core_service | eln | `core_sc` | 本服务，简化 |
| zabank_eln_approval_service | eln | `approval_sc` | 本服务，简化 |
| zabank_act_core_service | eln | `act_core_sc` | 跨服务，完整 |
| zabank_imc_activity_service | eln | `imc_activity_sc` | 跨服务，完整 |

> 完整 Fixture 设计规则参见 `references/fixture-design.md`

### 步骤4：生成测试代码

**核心原则**：
- 使用 `@pytest.mark.data()` 装饰器（不是 parametrize）
- 直接接收 `data` fixture（框架自动加载 YAML）
- 调用 `data.render()` 动态渲染变量
- 调用 `scenario.method(data[index])`（传入 Step 对象）
- 异常测试合并在一个方法中，使用 `data[key]` 访问

> 完整代码模板参见 `references/test-code-template.md`

### 步骤5：生成测试数据 YAML

**核心原则**：
- 使用 `variables` 定义全局变量（不是 `env` 多环境）
- `input` 中包含方法名和 `json.reqBody` 结构
- 移除 `expected` 字段（断言由 Scenario 处理）
- 正常场景和异常场景分离为不同文件

> 完整 YAML 格式参见 `references/yaml-format.md`

### 步骤6：生成执行脚本

生成按优先级执行的 bash 脚本：P0 → P1 → P2，最后生成 Allure 报告。

## 智能特性

1. **Controller方法名推断**：从 API 路径自动生成（`/account/query` → `query_account_info`）
2. **Model类名推断**：snake_case → PascalCase（`query_account_info` → `QueryAccountInfo`）
3. **智能测试数据**：正常场景使用变量，异常场景使用固定无效值，自动检测特殊字段模式
4. **Scenario 自动断言**：Scenario 方法接受 Step 对象，内部处理参数提取、Model 构造、Controller 调用、响应断言

> Scenario 设计参见 `references/scenario-design.md`

## 文件组织

```
test_automation_case/
├── testcases/
│   └── test_{module}.py
├── data/
│   └── {module}/
│       ├── {interface_group}.yaml
│       └── {interface_group}_fail.yaml
├── scenario/
│   ├── account_scenario.py
│   └── resource_scenario.py
├── service/
│   ├── account_service/
│   └── resource_service/
└── conftest.py
```

## 常见错误处理

| 情况 | 处理方式 |
|------|---------|
| Service层缺失接口方法 | 自动生成 Model 类和接口映射，提示用户检查 |
| 测试数据缺失 | 使用 `TODO_REPLACE_*` 占位符，生成数据准备指南 |
| Fixture命名冲突 | 提示复用现有 fixture 或使用不同服务名称 |

> 详细处理方案参见 `references/edge-cases.md`

## 附加资源

### 参考文件

- **`references/yaml-format.md`** - YAML 文件格式详情（variables、tests 结构）
- **`references/test-code-template.md`** - 完整测试代码模板（包含所有模式）
- **`references/edge-cases.md`** - 边界情况处理（Service层缺失、测试数据缺失）
- **`references/fixture-design.md`** - Fixture 设计指南（命名规则、自动检测算法）
- **`references/scenario-design.md`** - Scenario 层设计指南（业务逻辑封装、方法模式、断言处理）

### 示例文件

- **`examples/example-test-code.py`** - 完整测试类示例
- **`examples/example-yaml-normal.yaml`** - 正常场景 YAML
- **`examples/example-yaml-exception.yaml`** - 异常场景 YAML

---

**状态**: ✅ 可用
