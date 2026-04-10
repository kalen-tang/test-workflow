---
name: api-generator
description: 此技能应在用户询问"生成API测试用例"、"生成接口测试代码"、"根据接口文档生成自动化测试"、"生成API自动化测试"、"创建接口测试用例"或"为API端点生成测试数据"时使用。基于银行标准测试框架（pytest_zabank系列插件）生成标准化测试代码和YAML数据。
version: 2.0.0
---

# 银行标准测试框架 - API测试用例生成器

## 技能用途

从接口数据和场景案例生成完整的API自动化测试套件,基于**银行标准测试框架**（pytest_zabank系列插件）,包含标准化测试代码、变量化测试数据和执行脚本。

## 🏦 核心特性

- ✅ **银行标准框架**: 基于 pytest_zabank 系列插件（pytest_zabank_wholesale、pytest_zati_base）
- ✅ **数据驱动测试**: 使用 `@pytest.mark.data()` 装饰器自动加载 YAML
- ✅ **变量化配置**: 使用 `variables` 定义测试变量,支持 `data.render()` 动态渲染
- ✅ **Scenario 模式**: 测试方法传入 Step 对象,Scenario 内部处理断言和日志
- ✅ **智能 Fixture**: 本服务简化命名,跨服务完整命名,自动检测

## 使用场景

在用户需要以下操作时应用此技能:

1. 为任何微服务API端点生成自动化测试
2. 快速从接口文档创建测试套件
3. 生成标准化的变量化测试数据文件
4. 验证和测试特定API端点

**输入来源**（按优先级）:
1. **接口数据报告 + 场景案例表**（推荐）：interface-extractor 产出 + case-designer 产出
2. **仅接口数据报告**：基于接口定义生成基础测试用例（无场景串联）
3. **旧格式兼容**：直接传入包含接口信息和测试用例的 Markdown 文件

## 输入格式要求

### 格式 A：接口数据报告 + 场景案例表（推荐）

两个独立的 Markdown 文件：

1. **接口数据报告**（`08-interface-data-report` 格式）— 提供接口定义
   - 接口路径、请求方法、Content-Type
   - 请求参数表（参数名、类型、必填、说明）
   - 响应参数表（字段名、类型、说明）
   - 错误码表
   - 接口依赖关系

2. **场景案例表**（`09-scenario-table` 格式）— 提供测试场景
   - 场景总览（ID、名称、类型、优先级、涉及接口）
   - 场景详情（前置条件、步骤表、验证点）
   - 数据传递标记（`{{步骤N.字段名}}`）

**消费方式**：
- 从接口数据报告获取接口定义（路径、参数、响应）→ 生成 pytest 函数骨架和 YAML 数据结构
- 从场景案例表获取测试场景（步骤、验证点）→ 生成 Scenario 测试和断言逻辑
- 将 `{{步骤N.字段名}}` 转换为变量提取和传递代码

### 格式 B：仅接口数据报告

只有接口定义，无场景案例表。此时：
- 为每个接口生成独立的单接口测试用例（正常/异常/边界）
- 不生成跨接口的场景测试

### 格式 C：旧格式（兼容）

包含接口信息和测试用例的单一 Markdown 文件（如旧版 devplan-analyzer 输出）：

```markdown
## 接口X: 接口名称

### 接口信息
- **接口路径**: `/path/to/api`
- **请求方法**: POST/GET
- **功能描述**: 功能说明

### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| param1 | String | 是 | 参数说明 | example |

### 响应参数
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| code | String | 响应码 | 000000 |

### 接口X测试用例

#### 功能测试
##### 1. 正常场景 - 场景描述
- **用例描述**: ...
- **前置条件**: ...
- **请求参数**: ```json {...} ```
- **预期结果**: ```json {...} ```

#### 异常测试
##### 1. 参数错误测试
...
```

### 调用示例

```bash
# 方式1: 从文档文件生成
"请根据doc/Interface_Design.md生成接口自动化测试"

# 方式2: 为指定服务生成
"为账户服务的查询接口生成测试用例"

# 方式3: 快速测试端点
"测试资源服务的create接口"

# 方式4: 仅生成测试数据
"为支付服务的处理接口生成测试数据"
```

## 实施工作流

### 步骤1: 分析输入并识别服务

当用户提供文档或接口信息时:

1. **解析文档**
   - 提取所有接口信息（路径、方法、参数、响应）
   - 提取所有测试用例场景
   - 识别优先级（P0/P1/P2）

2. **识别目标服务**
   - 从API路径前缀自动检测服务类型
   - 定位对应的 service 目录
   - 查找匹配的 scenario 类

3. **确定当前项目名称**
   - 从项目路径提取项目名称（如 `zabank-eln-case` → `eln`）
   - 用于判断本服务 vs 跨服务（影响 Fixture 命名）

### 步骤2: 获取服务信息

基于识别的服务,自动获取:

1. **Service层信息**
   - 读取 `service/{service_name}/__init__.py` 获取接口映射
   - 解析 mapping 字典获取可用方法和 Model 类
   - ⚠️ 如Service层缺失: 自动创建或提示用户（参见 `references/02-edge-cases.md`）

2. **Scenario层信息**
   - 根据服务映射定位 scenario 文件
   - 示例: `account_service` → `scenario/account_scenario.py`

3. **配置信息**
   - 从 `config/{env}.yaml` 或插件配置获取服务 host 配置

### 步骤3: 确保 Scenario Fixture

**关键**: 必须在 `conftest.py` 中添加对应的 scenario fixture,否则测试会失败!

**Fixture 命名规则**（重要）:

使用自动检测逻辑判断本服务 vs 跨服务:

```python
def generate_fixture_name(service_name: str, current_project: str) -> str:
    """
    生成 Fixture 名称（自动判断本服务/跨服务）

    参数:
    - service_name: 服务名称（如 "zabank_eln_core_service"）
    - current_project: 当前项目名称（如 "eln"，从 "zabank-eln-case" 提取）

    返回:
    - Fixture 名称（如 "core_sc" 或 "imc_activity_sc"）
    """
    # 移除 zabank_ 前缀和 _service 后缀
    core = service_name.replace("zabank_", "").replace("_service", "")

    # 判断是否为本服务
    if current_project in core:
        # 本服务：简化命名（仅保留最后一个部分）
        parts = core.split('_')
        return f"{parts[-1]}_sc"
    else:
        # 跨服务：完整命名（保留所有中间层）
        return f"{core}_sc"
```

**示例**:

| 服务名称 | 当前项目 | Fixture 名称 | 说明 |
|---------|---------|-------------|-----|
| zabank_eln_core_service | eln | `core_sc` | 本服务,简化 |
| zabank_eln_approval_service | eln | `approval_sc` | 本服务,简化 |
| zabank_act_core_service | eln | `act_core_sc` | 跨服务,完整 |
| zabank_imc_activity_service | eln | `imc_activity_sc` | 跨服务,完整 |

**Conftest.py 示例**:

```python
# conftest.py
import pytest
from pytest_zabank_wholesale.plugin import lock
from pytest_zati_base.plugin import data, mysql
from scenario import CoreScenario, ApprovalScenario

# 本服务 fixtures（简化命名）
@pytest.fixture(scope="function")
def core_sc(env, lock) -> CoreScenario:
    """核心服务 Scenario（本服务）"""
    return CoreScenario(env, lock)

@pytest.fixture(scope="function")
def approval_sc(env, lock) -> ApprovalScenario:
    """审批服务 Scenario（本服务）"""
    return ApprovalScenario(env, lock)

# 跨服务 fixtures（完整命名）
@pytest.fixture(scope="function")
def imc_activity_sc(env, lock) -> ImcActivityScenario:
    """IMC活动服务 Scenario（跨服务）"""
    return ImcActivityScenario(env, lock)
```

详细设计参见 `references/03-fixture-design.md`。

### 步骤4: 生成测试代码

**核心原则**:
- ✅ **使用 `@pytest.mark.data()` 装饰器**（不是 parametrize）
- ✅ **直接接收 `data` fixture**（框架自动加载 YAML）
- ✅ **调用 `data.render()` 动态渲染变量**
- ✅ **调用 `scenario.method(data[index])`**（传入 Step 对象）
- ✅ **异常测试合并在一个方法中**

**测试代码模板**:

```python
import allure
import pytest
import json
import datetime

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")

@allure.epic("账户管理接口")
@pytest.mark.P1
@pytest.mark.xdist_group("account_group")
class TestAccount:
    """账户管理接口测试类"""

    @pytest.mark.data("account/query_account.yaml")
    @allure.title("查询账户信息")
    def test_query_account_info(self, data, account_sc, data_pool_sc):
        """
        正常场景 - 查询账户基本信息

        测试步骤:
        1. 从数据池获取有效的账户ID
        2. 动态渲染 accountId 变量
        3. 调用账户查询接口

        预期结果:
        - 返回成功响应码
        - 账户信息不为空
        """
        # 步骤1: 获取账户ID
        account_id = self.get_account_id(data, data_pool_sc)

        # 步骤2: 动态渲染
        data.render(accountId=account_id)

        # 步骤3: 调用接口（传入 Step 对象）
        account_sc.query_account_info(data[0])

    @pytest.mark.data("account/query_account_fail.yaml")
    def test_query_account_info_fail(self, data, account_sc):
        """异常场景测试（合并多个异常）"""
        account_sc.query_account_info(data["查询参数错误"])
        account_sc.query_account_info(data["账户不存在"])
        account_sc.query_account_info(data["用户无权限"])

    def get_account_id(self, data, data_pool_sc):
        """辅助方法 - 从数据池获取账户ID"""
        data.render(created_date=TODAY)
        data_list = data_pool_sc.get_data(data[11])
        return json.loads(data_list.json())[0]["account_id"]
```

**关键点**:
- ✅ 使用 `@pytest.mark.data()` 声明数据文件
- ✅ 直接接收 `data` fixture（不是 `yaml_file` + `config`）
- ✅ 使用 `data.render()` 动态替换变量
- ✅ 调用 `scenario.method(data[index])`（不是手动构造 Model）
- ✅ 异常测试使用 `data[key]` 访问（不是 `data[index]`）

完整模板参见 `references/01-test-code-template.md`。

### 步骤5: 生成测试数据 YAML

**核心原则**:
- ✅ **使用 `variables` 定义全局变量**（不是 `env` 多环境）
- ✅ **`input` 中包含方法名和 `json.reqBody` 结构**
- ✅ **移除 `expected` 字段**（断言由 Scenario 处理）
- ✅ **正常场景和异常场景分离为不同文件**

**YAML 结构**:

```yaml
# data/{module}/{interface_group}.yaml

# ===== 全局变量（必须） =====
variables:
  username: TestUser
  password: TestPass123
  account_id: 'ACC_123456'
  user_id: 'USER_001'

# ===== 测试用例（必须） =====
tests:
  - case: 账户信息查询
    data:
      - step: 0查询账户信息
        input:
          query_account_info:  # 关键：方法名作为 key
            json:
              reqBody:  # 关键：对应 Model 的 json_data 结构
                accountId: ${account_id}
                userId: ${user_id}
                pageSize: '10'
                currPage: '1'
```

**关键点**:
- ✅ `variables` 定义全局变量（支持环境变量替换 `${ENV_VAR}`）
- ✅ `input` 中包含方法名（便于 Scenario 识别）
- ✅ 使用 `${variable}` 语法引用变量
- ✅ 正常场景使用变量,异常场景使用固定无效值

**异常场景 YAML**:

```yaml
# data/{module}/{interface_group}_fail.yaml

variables:
  invalid_account_id: 'INVALID_ACC_999'

tests:
  - case: 账户查询异常场景
    data:
      - step: 查询参数错误
        input:
          query_account_info:
            json:
              reqBody:
                wrongParam: ${invalid_account_id}

      - step: 账户不存在
        input:
          query_account_info:
            json:
              reqBody:
                accountId: ${invalid_account_id}
```

详细示例参见 `references/00-yaml-format.md`。

### 步骤6: 生成执行脚本

生成便捷的按优先级执行的测试脚本:

```bash
#!/bin/bash
# run_{module}_tests.sh

echo "开始 {Module Name} API测试..."

# P0级别测试（核心业务流程）
pytest testcases/test_{module}.py -m P0 -v

# P1级别测试（重要功能）
pytest testcases/test_{module}.py -m P1 -v

# P2级别测试（辅助功能）
pytest testcases/test_{module}.py -m P2 -v

# 生成Allure报告
allure generate ./allure-results -o ./allure-report --clean

echo "测试执行完成!"
```

## 智能特性

### 1. Controller方法名推断

从API路径自动生成 controller 方法名:

```python
# /account/query → query_account_info
# /resource/create → create_resource
# /payment/process → process_payment
```

### 2. Model类名推断

将 snake_case 方法名转换为 PascalCase 类名:

```python
# query_account_info → QueryAccountInfo
# create_resource → CreateResource
# process_payment → ProcessPayment
```

### 3. 智能测试数据生成

根据参数类型和场景生成测试数据:

- **正常场景**: 使用 `variables` 中的变量
- **异常场景**: 使用固定无效值（如 `INVALID_XXX_999`）
- **特殊字段**: 自动检测 email、mobile、userId、accountNo 模式

### 4. Scenario 自动断言

**重要**: Scenario 方法内部自动处理断言,测试代码无需手动断言:

```python
# scenario/account.py

@allure.step("查询账户信息")
def query_account_info(self, step: dict):
    """
    Scenario 方法接受 Step 对象（来自 data[0]）

    内部处理:
    1. 从 Step 提取参数
    2. 构造 Model 实例
    3. 调用 Controller
    4. 自动断言响应码
    5. 返回业务数据
    """
    with base_log("查询账户信息"):
        data = model.QueryAccountInfo()
        data.json_data = step["query_account_info"]["json"]["reqBody"]
        resp = self.controller.query_account_info(data)
        # 自动断言
        assert resp["code"] == self.common_expectation["code"]
        return resp["value"]
```

**设计原则**: Scenario 封装业务逻辑,测试代码专注场景编排。

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
├── scripts/
│   └── run_{module}_tests.sh
└── conftest.py
```

## 常见错误处理

### 1. Service层缺失接口方法

```
⚠️  Service层没有找到接口 'query_account_info'

✅ 已自动生成:
   - Model类: service/account_service/model/query_account_info.py
   - 接口映射: service/account_service/__init__.py

📌 请检查生成的代码是否符合接口规范
```

参见 `references/02-edge-cases.md` 的自动生成解决方案。

### 2. 测试数据缺失

```
⚠️  检测到项目中没有可用的测试账号数据

已生成:
📄 data/account/query_account.yaml（使用 TODO_REPLACE_* 占位符）
📄 docs/test_data_preparation_query_account.md（数据准备指南）

📌 下一步操作:
1. 查看数据准备指南
2. 获取测试账号（推荐从现有YAML复制）
3. 替换占位符
```

参见 `references/02-edge-cases.md` 的占位符和数据准备策略。

### 3. Fixture命名冲突

如果生成的 fixture 名称已存在,提示用户:

```
⚠️  Fixture 'account_sc' 已存在于 conftest.py

建议:
- 复用现有 fixture（推荐）
- 或使用不同的服务名称
```

## 最佳实践

1. **文档先行**: 确保接口文档完整准确
2. **增量生成**: 先生成一个接口测试验证,再批量生成
3. **及时 Review**: 生成后检查代码并进行必要调整
4. **持续维护**: 接口变更时同步更新测试代码
5. **变量化管理**:
   - 使用 `variables` 定义可复用变量
   - 使用 `data.render()` 动态替换
   - 正常场景使用变量,异常场景使用固定值
6. **数据复用**:
   - 优先从现有 YAML 复制测试数据
   - 建立测试数据管理机制
   - 定期更新测试数据有效性

## 工作流示例

### 示例1: 生成账户查询接口测试

**输入**: "请根据 doc/Account_API.md 生成接口自动化测试"

**执行步骤**:
1. 读取 `doc/Account_API.md`
2. 识别接口属于 `account_service`
3. 当前项目: `zabank-eln-case` → 项目名 `eln`
4. 服务判断: `account_service` 不包含 `eln` → 跨服务 → `account_sc`
5. 扫描 `service/account_service/__init__.py` 获取接口映射
6. 生成:
   - `testcases/test_account.py`（使用 `@pytest.mark.data()`）
   - `data/account/query_account.yaml`（使用 `variables`）
   - `data/account/query_account_fail.yaml`（异常场景）
7. 更新 `conftest.py`（如需要）

### 示例2: 本服务接口生成

**输入**: "为核心服务的查询接口生成测试"

**执行步骤**:
1. 识别服务: `zabank_eln_core_service`
2. 当前项目: `zabank-eln-case` → 项目名 `eln`
3. 服务判断: `eln_core` 包含 `eln` → 本服务 → `core_sc`（简化命名）
4. 生成测试代码和数据
5. Fixture 使用简化命名 `core_sc`

### 示例3: 快速测试单个接口

**输入**: "快速测试资源服务的 create 接口"

**执行步骤**:
1. 识别服务和接口
2. 构造测试请求
3. 执行并展示结果
4. 提供进一步测试建议

## 附加资源

### 参考文件

详细实施指导:
- **`references/00-yaml-format.md`** - YAML 文件格式详情（variables、tests 结构）
- **`references/01-test-code-template.md`** - 完整测试代码模板（包含所有模式）
- **`references/02-edge-cases.md`** - 边界情况处理（Service层缺失、测试数据缺失）
- **`references/03-fixture-design.md`** - Fixture 设计指南（命名规则、自动检测算法）
- **`references/04-scenario-design.md`** - Scenario 层设计指南（业务逻辑封装、方法模式、断言处理）

### 示例文件

`examples/` 中的工作示例:
- **`example-test-code.py`** - 完整测试类示例
- **`example-yaml-normal.yaml`** - 正常场景 YAML
- **`example-yaml-exception.yaml`** - 异常场景 YAML

## 版本历史

- **v1.0** (2026-02-25): 初始版本,支持通用接口测试生成
- **v1.1** (2026-02-25): 新增多环境 YAML 格式支持（sit/auto_qe/uat）
- **v1.2** (2026-02-25): 简化断言逻辑,仅验证 code 字段
- **v1.3** (2026-02-25): 新增边界情况处理（Service层缺失、测试数据缺失）
- **v1.4** (2026-02-25): 优化 YAML 生成策略（1方法=1文件,使用 data[0]）
- **v1.5** (2026-03-11): 修正 Model 类实例化（使用静态导入,非动态查找）
- **v1.6** (2026-03-13): 应用渐进式披露设计（压缩主文档,详细内容移至 references）
- **v2.0** (2026-03-19): **[重大重构]** 适配银行标准测试框架
  - ✅ 使用 `@pytest.mark.data()` 装饰器替代 parametrize
  - ✅ 使用 `variables` 配置替代 `env` 多环境
  - ✅ Scenario 接收 Step 对象,自动处理断言
  - ✅ Fixture 智能命名（本服务简化,跨服务完整）
  - ✅ 完全通用化（移除所有项目特定示例）
  - ✅ 更新所有 references 文档为 v2.0
  - ✅ 重新编号 references 文件（00-03）

---

**注意**: 这是基于**银行标准测试框架**（pytest_zabank 系列插件）的测试用例生成器,适用于所有遵循银行测试架构规范的项目。
