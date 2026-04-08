# API 测试案例格式规范

**版本**: v1.0
**创建时间**: 2026-03-18
**适用阶段**: 第四阶段（自动化测试用例生成）
**输出工具**: api-case-generator Skill
**下游消费者**: CI/CD 自动化执行、测试报告系统

---

## 📋 目录

- [概述](#概述)
- [文件结构](#文件结构)
- [Python 测试代码规范](#python-测试代码规范)
- [YAML 测试数据规范](#yaml-测试数据规范)
- [测试配置规范](#测试配置规范)
- [使用场景](#使用场景)

---

## 概述

### 目标

将标准化需求文档（01）和设计文档（02）转换为可直接执行的 Python 自动化测试代码，配合 YAML 格式的测试数据，实现接口测试的自动化执行。

### 核心原则

1. **代码与数据分离**：测试逻辑用 Python，测试数据用 YAML
2. **多环境支持**：同一份代码，不同环境（sit/auto_qe/uat）使用不同数据
3. **可读性优先**：代码清晰易懂，数据结构明确
4. **可扩展性**：支持新增测试场景，支持自定义断言
5. **与 Claude Code 集成**：生成的代码符合项目规范（PEP 8、类型注解）

### 输入输出

- **输入1**：`01-normalized-requirement.yaml`（提供测试场景、业务规则）
- **输入2**：`02-normalized-design.yaml`（提供接口定义、请求/响应格式）
- **输入3**：`06-manual-test-cases.yaml`（可选，提供测试思路参考）
- **输出**：
  - Python 测试代码文件（`tests/test_*.py`）
  - YAML 测试数据文件（`data/*.yaml`）
  - 测试配置文件（`pytest.ini`、`conftest.py`）

---

## 文件结构

### 标准输出目录结构

```
result/{project_name}/
├── tests/                           # Python 测试代码目录
│   ├── __init__.py
│   ├── conftest.py                  # pytest 配置和共享 fixtures
│   ├── test_voucher_list.py         # 消费券列表接口测试
│   ├── test_voucher_use.py          # 消费券使用接口测试
│   └── test_voucher_issue.py        # 消费券发放接口测试
├── data/                            # YAML 测试数据目录
│   ├── voucher_list.yaml            # 消费券列表接口测试数据
│   ├── voucher_use.yaml             # 消费券使用接口测试数据
│   └── voucher_issue.yaml           # 消费券发放接口测试数据
├── config/                          # 测试配置目录
│   ├── config.yaml                  # 环境配置（域名、超时时间等）
│   └── secrets.yaml                 # 敏感配置（账号、密码等，不提交到git）
├── pytest.ini                       # pytest 配置文件
└── README.md                        # 测试项目说明文档
```

---

## Python 测试代码规范

### 基本结构模板

```python
"""
消费券列表接口测试模块

测试接口：
- 查询消费券列表（GET /api/v1/voucher/list）
"""
import pytest
from typing import Dict, Any
from utils.http_client import HttpClient
from utils.assertion_helper import assert_response_schema, assert_business_rule


class TestVoucherList:
    """消费券列表接口测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, http_client: HttpClient) -> None:
        """测试前置配置

        :param http_client: HTTP 客户端 fixture
        """
        self.client = http_client
        self.base_path = "/api/v1/voucher/list"

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_voucher_list_success(
        self, test_data: Dict[str, Any], expected_response: Dict[str, Any]
    ) -> None:
        """测试查询消费券列表成功（正向场景）

        测试步骤：
        1. 准备测试数据（用户ID、卡类型）
        2. 发送 GET 请求
        3. 验证响应状态码为 200
        4. 验证响应结构符合预期
        5. 验证业务规则：返回的消费券卡类型与请求参数一致

        :param test_data: 测试数据（从 YAML 加载）
        :param expected_response: 预期响应（从 YAML 加载）
        """
        # 1. 准备测试数据
        params = {
            "userId": test_data["userId"],
            "cardType": test_data["cardType"],
        }

        # 2. 发送请求
        response = self.client.get(self.base_path, params=params)

        # 3. 验证状态码
        assert response.status_code == 200, f"期望状态码 200，实际状态码 {response.status_code}"

        # 4. 验证响应结构
        response_data = response.json()
        assert_response_schema(
            response_data,
            expected_response["schema"],
            message="响应结构验证失败"
        )

        # 5. 验证业务规则
        if response_data["vouchers"]:
            for voucher in response_data["vouchers"]:
                assert voucher["cardType"] == params["cardType"], \
                    f"业务规则验证失败：消费券卡类型不一致"

    @pytest.mark.negative
    def test_voucher_list_missing_user_id(self) -> None:
        """测试缺少用户ID（异常场景）

        测试步骤：
        1. 不传 userId 参数
        2. 发送 GET 请求
        3. 验证响应状态码为 400
        4. 验证错误码为 E001
        """
        # 1. 准备测试数据（缺少 userId）
        params = {"cardType": "CREDIT"}

        # 2. 发送请求
        response = self.client.get(self.base_path, params=params)

        # 3. 验证状态码
        assert response.status_code == 400, f"期望状态码 400，实际状态码 {response.status_code}"

        # 4. 验证错误码
        response_data = response.json()
        assert response_data["errorCode"] == "E001", \
            f"期望错误码 E001，实际错误码 {response_data['errorCode']}"

    @pytest.mark.boundary
    def test_voucher_list_empty_result(self, test_data: Dict[str, Any]) -> None:
        """测试查询结果为空（边界场景）

        测试步骤：
        1. 使用没有消费券的用户ID
        2. 发送 GET 请求
        3. 验证响应状态码为 200
        4. 验证 vouchers 数组为空
        """
        # 1. 准备测试数据（无消费券用户）
        params = {
            "userId": test_data["userId_without_vouchers"],
            "cardType": "CREDIT",
        }

        # 2. 发送请求
        response = self.client.get(self.base_path, params=params)

        # 3. 验证状态码
        assert response.status_code == 200

        # 4. 验证结果为空
        response_data = response.json()
        assert response_data["vouchers"] == [], \
            f"期望 vouchers 为空数组，实际为 {response_data['vouchers']}"
```

### 代码规范要点

#### 1. 导入规范

```python
# 标准库
import json
from typing import Dict, Any, List

# 第三方库
import pytest
import requests

# 本地模块
from utils.http_client import HttpClient
from utils.assertion_helper import assert_response_schema
```

#### 2. 类型注解

```python
# ✅ 正确：使用类型注解
def test_voucher_list_success(
    self, test_data: Dict[str, Any], expected_response: Dict[str, Any]
) -> None:
    """测试查询消费券列表成功"""
    pass

# ❌ 错误：缺少类型注解
def test_voucher_list_success(self, test_data, expected_response):
    pass
```

#### 3. 文档字符串

```python
def test_voucher_list_success(self, test_data: Dict[str, Any]) -> None:
    """测试查询消费券列表成功（正向场景）

    测试步骤：
    1. 准备测试数据（用户ID、卡类型）
    2. 发送 GET 请求
    3. 验证响应状态码为 200
    4. 验证响应结构符合预期

    :param test_data: 测试数据（从 YAML 加载）
    """
    pass
```

#### 4. pytest 标记

```python
# 测试类型标记
@pytest.mark.smoke          # 冒烟测试
@pytest.mark.positive       # 正向场景
@pytest.mark.negative       # 异常场景
@pytest.mark.boundary       # 边界场景

# 优先级标记
@pytest.mark.p0             # P0级（核心功能）
@pytest.mark.p1             # P1级（重要功能）
@pytest.mark.p2             # P2级（一般功能）

# 业务模块标记
@pytest.mark.voucher        # 消费券模块
@pytest.mark.payment        # 支付模块
```

#### 5. 断言规范

```python
# ✅ 正确：清晰的断言消息
assert response.status_code == 200, \
    f"期望状态码 200，实际状态码 {response.status_code}"

# ✅ 正确：使用工具函数
assert_response_schema(
    response_data,
    expected_schema,
    message="响应结构验证失败"
)

# ❌ 错误：缺少断言消息
assert response.status_code == 200
```

---

## YAML 测试数据规范

### 基本结构

```yaml
# data/voucher_list.yaml

# ============================================
# SIT 环境测试数据
# ============================================
sit:
  # 正向场景：Credit卡用户查询消费券列表
  test_voucher_list_success:
    # 测试数据
    userId: "user_credit_001"
    cardType: "CREDIT"

    # 预期响应
    expected:
      status_code: 200
      schema:
        type: object
        required: ["vouchers"]
        properties:
          vouchers:
            type: array
            items:
              type: object
              required: ["voucherId", "amount", "cardType", "status"]
              properties:
                voucherId:
                  type: string
                  example: "V001"
                amount:
                  type: number
                  example: 100.00
                cardType:
                  type: string
                  enum: ["DEBIT", "CREDIT"]
                status:
                  type: string
                  enum: ["ACTIVE", "USED", "EXPIRED"]

  # 异常场景：缺少用户ID
  test_voucher_list_missing_user_id:
    # 测试数据（缺少 userId）
    cardType: "CREDIT"

    # 预期响应
    expected:
      status_code: 400
      errorCode: "E001"
      errorMessage: "用户ID不能为空"

  # 边界场景：查询结果为空
  test_voucher_list_empty_result:
    # 测试数据（无消费券用户）
    userId: "user_without_vouchers"
    cardType: "CREDIT"

    # 预期响应
    expected:
      status_code: 200
      vouchers: []

# ============================================
# AUTO_QE 环境测试数据
# ============================================
auto_qe:
  test_voucher_list_success:
    userId: "auto_qe_user_001"
    cardType: "CREDIT"
    expected:
      status_code: 200

  test_voucher_list_missing_user_id:
    cardType: "CREDIT"
    expected:
      status_code: 400
      errorCode: "E001"

# ============================================
# UAT 环境测试数据
# ============================================
uat:
  test_voucher_list_success:
    userId: "uat_user_001"
    cardType: "CREDIT"
    expected:
      status_code: 200
```

### 数据字段说明

#### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `{environment}` | object | 环境名称（sit/auto_qe/uat） |
| `{test_case_name}` | object | 测试用例名称（对应测试方法名） |
| `expected.status_code` | integer | 预期响应状态码 |

#### 可选字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `expected.schema` | object | 预期响应结构（JSON Schema） |
| `expected.errorCode` | string | 预期错误码 |
| `expected.errorMessage` | string | 预期错误消息 |

---

## 测试配置规范

### pytest.ini 配置文件

```ini
[pytest]
# 测试文件匹配模式
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 命令行选项
addopts =
    -v                          # 详细输出
    -s                          # 显示print输出
    --strict-markers            # 严格标记模式
    --tb=short                  # 简短的traceback
    --alluredir=./allure-results # Allure报告输出目录

# 标记注册
markers =
    smoke: 冒烟测试
    positive: 正向场景测试
    negative: 异常场景测试
    boundary: 边界场景测试
    p0: P0级测试（核心功能）
    p1: P1级测试（重要功能）
    p2: P2级测试（一般功能）
    voucher: 消费券模块
    payment: 支付模块

# 环境变量
env =
    SIT
    AUTO_QE
    UAT
```

### conftest.py 配置文件

```python
"""
pytest 共享配置和 fixtures
"""
import pytest
import yaml
from typing import Dict, Any
from pathlib import Path
from utils.http_client import HttpClient


def pytest_addoption(parser: pytest.Parser) -> None:
    """添加命令行选项

    :param parser: pytest 解析器
    """
    parser.addoption(
        "--env",
        action="store",
        default="sit",
        help="测试环境：sit, auto_qe, uat"
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> str:
    """获取测试环境

    :param request: pytest 请求对象
    :return: 环境名称
    """
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env: str) -> Dict[str, Any]:
    """加载测试配置

    :param env: 环境名称
    :return: 配置字典
    """
    config_path = Path(__file__).parent / "config" / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        all_config = yaml.safe_load(f)
    return all_config.get(env, {})


@pytest.fixture(scope="session")
def http_client(config: Dict[str, Any]) -> HttpClient:
    """HTTP 客户端 fixture

    :param config: 配置字典
    :return: HTTP 客户端实例
    """
    base_url = config.get("base_url", "https://sit-api.zabank.com")
    timeout = config.get("timeout", 30)
    return HttpClient(base_url=base_url, timeout=timeout)


@pytest.fixture
def test_data(request: pytest.FixtureRequest, env: str) -> Dict[str, Any]:
    """加载测试数据

    :param request: pytest 请求对象
    :param env: 环境名称
    :return: 测试数据字典
    """
    # 从测试文件名推导数据文件名
    test_file = Path(request.fspath)
    data_file = test_file.parent.parent / "data" / f"{test_file.stem}.yaml"

    # 加载 YAML 数据
    with open(data_file, "r", encoding="utf-8") as f:
        all_data = yaml.safe_load(f)

    # 获取当前环境的数据
    env_data = all_data.get(env, {})

    # 获取当前测试用例的数据
    test_name = request.node.name
    return env_data.get(test_name, {})


@pytest.fixture
def expected_response(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """获取预期响应

    :param test_data: 测试数据
    :return: 预期响应字典
    """
    return test_data.get("expected", {})
```

### config.yaml 配置文件

```yaml
# config/config.yaml

# SIT 环境配置
sit:
  base_url: "https://sit-api.zabank.com"
  timeout: 30
  retry_times: 3
  retry_delay: 1

# AUTO_QE 环境配置
auto_qe:
  base_url: "https://auto-qe-api.zabank.com"
  timeout: 30
  retry_times: 3
  retry_delay: 1

# UAT 环境配置
uat:
  base_url: "https://uat-api.zabank.com"
  timeout: 60
  retry_times: 5
  retry_delay: 2
```

---

## 使用场景

### 场景1：本地执行测试

```bash
# 执行所有测试
pytest

# 执行指定环境的测试
pytest --env sit

# 执行指定文件的测试
pytest tests/test_voucher_list.py

# 执行指定标记的测试
pytest -m smoke
pytest -m "p0 and voucher"

# 执行指定测试用例
pytest tests/test_voucher_list.py::TestVoucherList::test_voucher_list_success
```

### 场景2：CI/CD 集成

```yaml
# .github/workflows/api-test.yml
name: API Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [sit, auto_qe, uat]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.14'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run API tests
      run: pytest --env ${{ matrix.env }} --alluredir=./allure-results

    - name: Generate Allure report
      uses: allure-framework/allure-action@master
      with:
        results: ./allure-results
```

### 场景3：测试报告生成

```bash
# 生成 Allure 报告
pytest --alluredir=./allure-results
allure serve ./allure-results

# 生成 HTML 报告
pytest --html=./reports/report.html --self-contained-html
```

---

## 生成逻辑

### 从 Artifact 到测试代码的映射

```yaml
# 输入：01-normalized-requirement.yaml
scenarios:
  - id: S001
    name: "Credit卡用户正常查询消费券列表"
    type: positive
    given: "Credit卡用户已登录，且有可用消费券"
    when: "用户查询消费券列表"
    then: "返回该用户的所有Credit卡消费券"

# 输入：02-normalized-design.yaml
interfaces:
  - id: IF001
    name: "查询消费券列表"
    path: "/api/v1/voucher/list"
    method: GET
    request_params:
      - name: "userId"
        type: string
        required: true
      - name: "cardType"
        type: string
        enum_values: ["DEBIT", "CREDIT"]
    response_schema:
      success_response:
        - name: "vouchers"
          type: array
```

**生成 Python 测试代码**：

```python
def test_voucher_list_success(self, test_data: Dict[str, Any]) -> None:
    """测试Credit卡用户正常查询消费券列表（正向场景）

    Given: Credit卡用户已登录，且有可用消费券
    When: 用户查询消费券列表
    Then: 返回该用户的所有Credit卡消费券
    """
    # Given: 准备测试数据
    params = {
        "userId": test_data["userId"],
        "cardType": test_data["cardType"],
    }

    # When: 发送请求
    response = self.client.get("/api/v1/voucher/list", params=params)

    # Then: 验证结果
    assert response.status_code == 200
    response_data = response.json()
    assert "vouchers" in response_data
```

**生成 YAML 测试数据**：

```yaml
sit:
  test_voucher_list_success:
    userId: "user_credit_001"
    cardType: "CREDIT"
    expected:
      status_code: 200
```

---

## 最佳实践

### 1. 测试用例命名

```python
# ✅ 正确：清晰描述测试场景
def test_voucher_list_success(self): pass
def test_voucher_list_missing_user_id(self): pass
def test_voucher_list_empty_result(self): pass

# ❌ 错误：命名不清晰
def test_case_1(self): pass
def test_voucher(self): pass
```

### 2. 测试数据管理

```yaml
# ✅ 正确：按环境和用例组织
sit:
  test_voucher_list_success:
    userId: "sit_user_001"
uat:
  test_voucher_list_success:
    userId: "uat_user_001"

# ❌ 错误：硬编码在代码中
def test_voucher_list_success(self):
    userId = "user_001"  # 不便于多环境切换
```

### 3. 断言完整性

```python
# ✅ 正确：全面验证
assert response.status_code == 200
assert "vouchers" in response_data
for voucher in response_data["vouchers"]:
    assert voucher["cardType"] == "CREDIT"

# ❌ 错误：断言不充分
assert response.status_code == 200  # 仅验证状态码
```

### 4. 测试独立性

```python
# ✅ 正确：每个测试独立准备数据
def test_voucher_list_success(self):
    params = {"userId": "user_001", "cardType": "CREDIT"}
    # ...

def test_voucher_list_empty(self):
    params = {"userId": "user_without_vouchers", "cardType": "CREDIT"}
    # ...

# ❌ 错误：测试之间有依赖
class TestVoucherList:
    user_id = None  # 共享状态

    def test_create_user(self):
        TestVoucherList.user_id = "user_001"

    def test_voucher_list(self):
        # 依赖前一个测试创建的用户
        params = {"userId": TestVoucherList.user_id}
```

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03-18 | 初始版本，定义 Python 代码和 YAML 数据格式 |

---

## 附录

### 相关文档

- [00-overview.md](./00-overview.md) - Artifact Schemas 总览
- [01-normalized-requirement-v2.md](./01-normalized-requirement-v2.md) - 标准化需求文档格式
- [02-normalized-design.md](./02-normalized-design.md) - 标准化设计文档格式

### 参考实现

- [api-case-generator SKILL.md](../../skills/api-case-generator/SKILL.md)
- [api-case-generator references/01-test-code-template.md](../../skills/api-case-generator/references/01-test-code-template.md)
- [api-case-generator references/00-yaml-format.md](../../skills/api-case-generator/references/00-yaml-format.md)

---

**文档版本**: v1.0
**最后更新**: 2026-03-18
**维护者**: qa-toolkit 团队