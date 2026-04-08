# Fixture 设计指南

**版本**: 1.0
**创建日期**: 2026-03-19
**适用框架**: pytest_zabank 系列插件（银行标准测试框架）
**适用项目**: 所有遵循银行测试架构规范的测试项目

---

## 📋 Fixture 设计原则

### 核心原则

1. ✅ **本服务简化命名**：主服务 fixture 使用核心名称（如 `core_sc`）
2. ✅ **跨服务完整命名**：其他服务 fixture 使用完整前缀（如 `act_core_sc`）
3. ✅ **Function Scope**：默认使用 `scope="function"`（每个测试方法独立）
4. ✅ **依赖插件 Fixture**：依赖 `env` 和 `lock` fixture（来自插件）
5. ✅ **类型注解**：使用类型注解提高代码可读性

---

## 🏗️ Fixture 命名规则

### 规则说明

| 服务类型 | Service 名称示例 | Scenario Class | Fixture 命名规则 | 说明 |
|---------|----------------|---------------|----------------|-----|
| **本服务** | zabank_eln_core_service | CoreScenario | `core_sc` | 简化命名（仅保留核心名称） |
| **其他服务** | zabank_act_activity_service | ActActivityScenario | `act_activity_sc` | 完整命名（保留中间层前缀） |
| **其他服务** | zabank_imc_activity_service | ImcActivityScenario | `imc_activity_sc` | 完整命名（保留中间层前缀） |
| **其他服务** | zabank_imc_reward_service | ImcRewardScenario | `imc_reward_sc` | 完整命名（保留中间层前缀） |

### 命名模式

**本服务（简化命名）**：

```python
# 规则：仅保留服务核心名称（最后一个部分）
# zabank_{project}_{core}_service → {core}_sc

# 示例：
# 当前项目：zabank-eln-case
# zabank_eln_core_service → core_sc（本服务，简化）
# zabank_eln_approval_service → approval_sc（本服务，简化）
```

**其他服务（完整命名）**：

```python
# 规则：移除 zabank_ 前缀和 _service 后缀，保留中间所有层级
# zabank_{module}_{domain}_service → {module}_{domain}_sc

# 示例：
# zabank_act_activity_service → act_activity_sc
# zabank_imc_activity_service → imc_activity_sc
# zabank_imc_reward_service → imc_reward_sc
# zabank_act_core_service → act_core_sc
```

### 命名逻辑（带判断）

**核心原则**：根据当前项目名称判断是否为本服务

```python
def generate_fixture_name(service_name: str, current_project: str) -> str:
    """
    生成 Fixture 名称

    参数:
    - service_name: 服务名称（如 "zabank_eln_core_service"）
    - current_project: 当前项目名称（如 "eln"，从 "zabank-eln-case" 提取）

    返回:
    - Fixture 名称
    """
    # 移除前缀和后缀
    core = service_name.replace("zabank_", "").replace("_service", "")

    # 判断是否为本服务
    if current_project in core:
        # 本服务：简化命名（仅保留最后一个部分）
        parts = core.split('_')
        return f"{parts[-1]}_sc"  # core_sc、approval_sc
    else:
        # 其他服务：完整命名（保留所有中间层）
        return f"{core}_sc"  # act_activity_sc、imc_activity_sc
```

**示例**：

```python
# 当前项目：zabank-eln-case（提取项目名称：eln）
current_project = "eln"

# 判断示例：
generate_fixture_name("zabank_eln_core_service", "eln")
# → 包含 "eln" → 本服务 → core_sc

generate_fixture_name("zabank_imc_activity_service", "eln")
# → 不包含 "eln" → 其他服务 → imc_activity_sc

generate_fixture_name("zabank_act_core_service", "eln")
# → 不包含 "eln" → 其他服务 → act_core_sc
```

**原因**：
- ✅ 本服务简化命名，提高可读性（`core_sc` 比 `eln_core_sc` 更简洁）
- ✅ 其他服务完整命名，避免冲突（`imc_activity_sc` 和 `act_activity_sc` 不会冲突）
- ✅ 自动判断逻辑，减少手动配置

---

## 📝 Conftest.py 模板

### 完整示例（zabank-eln-case 项目）

```python
# conftest.py

import pytest
# 导入第三方插件 fixtures
from pytest_zabank_wholesale.plugin import lock
from pytest_zabank_wholesale.scenario import ZeroScenario
from pytest_zati_base.plugin import data, mysql
# 导入本项目 Scenario 类
from scenario import CoreScenario, ApprovalScenario
# 导入其他服务 Scenario 类（来自插件）
from pytest_zabank_imc.scenario import ImcActivityScenario, ImcRewardScenario


# ===== 本服务 Fixtures（简化命名） =====

@pytest.fixture(scope="function")
def core_sc(env, lock) -> CoreScenario:
    """
    核心服务 Scenario（本服务，简化命名）

    服务：zabank_eln_core_service
    命名：core_sc（简化，仅保留 core）

    依赖:
    - env: 环境配置 fixture（来自插件）
    - lock: 锁机制 fixture（来自插件）
    """
    return CoreScenario(env, lock)


@pytest.fixture(scope="function")
def approval_sc(env, lock) -> ApprovalScenario:
    """
    审批服务 Scenario（本服务，简化命名）

    服务：zabank_eln_approval_service
    命名：approval_sc（简化，仅保留 approval）
    """
    return ApprovalScenario(env, lock)


# ===== 其他服务 Fixtures（完整命名） =====

@pytest.fixture(scope="function")
def imc_activity_sc(env, lock) -> ImcActivityScenario:
    """
    IMC 活动服务 Scenario（其他服务，完整命名）

    服务：zabank_imc_activity_service
    命名：imc_activity_sc（完整，保留 imc 前缀）
    """
    return ImcActivityScenario(env, lock)


@pytest.fixture(scope="function")
def imc_reward_sc(env, lock) -> ImcRewardScenario:
    """
    IMC 积分服务 Scenario（其他服务，完整命名）

    服务：zabank_imc_reward_service
    命名：imc_reward_sc（完整，保留 imc 前缀）
    """
    return ImcRewardScenario(env, lock)


# ===== 第三方服务 Fixtures（可选） =====

@pytest.fixture(scope="function")
def zero_sc(env) -> ZeroScenario:
    """
    数据池服务 Scenario（第三方插件）

    用途:
    - 从数据池获取测试数据
    - 设置测试数据到数据池
    """
    return ZeroScenario(env)


# ===== 钩子函数（可选） =====

def pytest_report_teststatus(report: pytest.TestReport, config: pytest.Config):
    """
    自定义测试状态报告

    功能:
    - 将依赖失败的 skip 转换为 failed
    """
    if report.when == 'setup':
        if report.skipped:
            if 'depends on' in report.longrepr[2]:
                report.outcome = 'failed'


# ===== 导出所有 fixture =====

__all__ = [
    # 本服务 fixtures（简化命名）
    "core_sc",
    "approval_sc",
    # 其他服务 fixtures（完整命名）
    "imc_activity_sc",
    "imc_reward_sc",
    # 第三方 fixtures
    "zero_sc",
    # 插件 fixtures
    "data",
    "mysql",
    "lock",
]
```

---

## 🔧 Scenario 类设计

### 标准 Scenario 类

```python
# scenario/core.py

from pytest_zabank_wholesale.scenario import Base, base_log
from pytest_zabank_wholesale.scenario import SSOScenario, BBMScenario
from service import controller, model
import allure


class CoreScenario(Base):
    """
    核心服务 Scenario 类

    职责:
    - 封装 Controller 调用
    - 处理登录和认证
    - 自动断言响应码
    - 记录日志和 Allure 步骤
    """

    def __init__(self, env, lock):
        """
        初始化 CoreScenario

        参数:
        - env: 环境配置字典（包含 hosts 信息）
        - lock: 锁机制对象（用于并发控制）
        """
        self.host = env["hosts"]["eln"]
        self.controller = controller.Controller(self.host)
        self.controller.default_timeout = 30
        self.controller.headers = {}
        self.sso_bss = SSOScenario(env)
        self.bbm_bss = BBMScenario(env)
        self.lock = lock
        self.common_expectation = {"code": "EL0000"}

    @allure.step("登录")
    def login(self, step: dict):
        """
        登录方法

        参数:
        - step: Step 对象（来自 data[index]）

        功能:
        - 调用 SSO 登录
        - 设置 Controller headers（token）
        """
        with base_log("ELN登录"):
            login_data = step["login"]
            kw = {
                "username": login_data["username"],
                "password": login_data["password"],
                "service": "ZA-Bank-ELN",
            }
            ticket, token = self.bbm_bss.new_login(**kw)
            self.controller.headers["token"] = token
            self.controller.headers["X-Usercenter-Session"] = token

    @allure.step("根据贷款账号查询借据列表")
    def web_bank_query_by_loan_account_no(self, step: dict):
        """
        根据贷款账号查询借据列表

        参数:
        - step: Step 对象（来自 data[index]）

        返回:
        - 业务数据字典（resp["value"]）

        异常:
        - 响应码不符合预期时抛出 AssertionError
        """
        with base_log("根据贷款账号查询借据列表"):
            # 步骤1: 构造 Model 实例
            data = model.WebBankQueryByLoanAccountNo()
            data.json_data = step["web_bank_query_by_loan_account_no"]["json"]["reqBody"]

            # 步骤2: 调用 Controller
            resp = self.controller.web_bank_query_by_loan_account_no(data)

            # 步骤3: 自动断言
            assert resp["code"] == self.common_expectation["code"], f"响应码错误: {resp['code']}"

            # 步骤4: 返回业务数据
            return resp.get("value", {})
```

---

## 🎯 Fixture 依赖关系

### 依赖图

```
pytest 插件
├── pytest_zabank_lns
│   └── lns_sc (fixture)
├── pytest_zabank_wholesale
│   ├── ticket_sc (fixture)
│   ├── lock (fixture)
│   └── ZeroScenario (class)
└── pytest_zati_base
    ├── data (fixture)
    ├── mysql (fixture)
    └── xxljob (fixture)

项目 conftest.py
├── core_sc (depends on: env, lock)
├── approval_sc (depends on: env)
├── small_loan_sc (depends on: env)
├── zero_sc (depends on: env)
└── ui_sc (depends on: lock)
```

### env Fixture

**来源**: pytest 插件（如 `pytest_zati_base`）

**内容**:

```python
# env fixture 提供的数据结构
env = {
    "hosts": {
        "eln": "https://eln-sit.za.group",
        "lns": "https://lns-sit.za.group",
        "act": "https://act-sit.za.group",
    },
    "databases": {
        "app": {
            "host": "db-sit.za.group",
            "port": 3306,
            "user": "test",
            "password": "test123"
        }
    }
}
```

### lock Fixture

**来源**: pytest 插件（如 `pytest_zabank_wholesale`）

**用途**:
- 并发控制
- 防止多个测试同时修改共享资源

---

## 📚 使用示例

### 在测试中使用 Fixture

```python
# testcases/test_web_bank.py

import allure
import pytest


@allure.epic("企网贷款接口")
@pytest.mark.P1
@pytest.mark.xdist_group("web_group")
class TestWebBank:

    @pytest.mark.data("core/web_bank.yaml")
    @allure.title("根据贷款账号查询借据列表")
    def test_web_bank_query(self, data, core_sc, zero_sc):
        """
        测试方法依赖的 fixtures:
        - data: 框架自动注入的 YAML 数据
        - core_sc: 本项目主服务 Scenario
        - zero_sc: 数据池服务 Scenario
        """
        # 使用 zero_sc 获取数据
        loan_account_no = self.get_loan_account_no(data, zero_sc)

        # 使用 core_sc 调用接口
        data.render(loanAccountNo=loan_account_no)
        core_sc.web_bank_query_by_loan_account_no(data[0])
```

---

## 🔄 跨服务测试场景

### 场景: 调用多个服务

```python
@pytest.mark.data("integration/cross_service.yaml")
def test_cross_service_integration(self, data, core_sc, act_core_sc, activity_sc):
    """
    跨服务集成测试

    涉及服务:
    - core_sc: zabank-eln-core-service（本服务）
    - act_core_sc: zabank_act_core_service（行动服务）
    - activity_sc: zabank_imc_activity_service（活动服务）

    测试流程:
    1. 使用 core_sc 创建贷款
    2. 使用 act_core_sc 触发行动
    3. 使用 activity_sc 查询活动状态
    """
    # 步骤1: 创建贷款（本服务）
    resp1 = core_sc.create_loan(data[0])
    loan_no = resp1["loanNo"]

    # 步骤2: 触发行动（其他服务）
    data.render(loanNo=loan_no)
    resp2 = act_core_sc.trigger_action(data[1])
    action_id = resp2["actionId"]

    # 步骤3: 查询活动状态（其他服务）
    data.render(actionId=action_id)
    activity_sc.query_activity_status(data[2])
```

---

## 🛠️ Fixture 生成规则

### 生成算法（带自动判断）

```python
def generate_fixture_name(service_name: str, current_project: str) -> str:
    """
    生成 Fixture 名称（自动判断本服务/其他服务）

    参数:
    - service_name: 服务名称（如 "zabank_eln_core_service"）
    - current_project: 当前项目名称（如 "eln"，从 "zabank-eln-case" 提取）

    返回:
    - Fixture 名称（如 "core_sc" 或 "imc_activity_sc"）

    示例:
    >>> generate_fixture_name("zabank_eln_core_service", "eln")
    'core_sc'
    >>> generate_fixture_name("zabank_imc_activity_service", "eln")
    'imc_activity_sc'
    """
    # 移除 zabank_ 前缀和 _service 后缀
    core = service_name.replace("zabank_", "").replace("_service", "")

    # 判断是否为本服务
    if current_project in core:
        # 本服务：简化命名（仅保留最后一个部分）
        parts = core.split('_')
        return f"{parts[-1]}_sc"
    else:
        # 其他服务：完整命名（保留所有中间层）
        return f"{core}_sc"


def extract_project_name(project_path: str) -> str:
    """
    从项目路径提取项目名称

    示例:
    >>> extract_project_name("zabank-eln-case")
    'eln'
    >>> extract_project_name("zabank-imc-case")
    'imc'
    """
    # 移除 zabank- 和 -case 前缀/后缀
    return project_path.replace("zabank-", "").replace("-case", "")
```

### 生成示例

| 服务名称 | 是否主服务 | Fixture 名称 |
|---------|----------|-------------|
| zabank_eln_core_service | ✅ | `core_sc` |
| zabank_act_core_service | ❌ | `act_core_sc` |
| zabank_imc_activity_service | ❌ | `activity_sc` |
| zabank_imc_reward_service | ❌ | `reward_sc` |
| zabank_imc_cubercore_service | ❌ | `cuber_core_sc` |

---

## 📖 Scenario 类命名规范

### 命名规则

```python
# 服务名称 → Scenario 类名
# zabank_eln_core_service → CoreScenario
# zabank_act_core_service → ActCoreScenario
# zabank_imc_activity_service → ActivityScenario
# zabank_imc_reward_service → RewardScenario
```

### 转换算法

```python
def service_to_scenario_class(service_name: str) -> str:
    """
    服务名称 → Scenario 类名

    示例:
    - zabank_eln_core_service → CoreScenario
    - zabank_act_core_service → ActCoreScenario
    - zabank_imc_activity_service → ActivityScenario
    """
    # 移除 zabank_ 和 _service 前缀/后缀
    core = service_name.replace("zabank_", "").replace("_service", "")

    # 转换为 PascalCase
    words = core.split('_')
    class_name = ''.join([word.capitalize() for word in words])

    # 添加 Scenario 后缀
    return f"{class_name}Scenario"
```

---

## ✅ Fixture 检查清单

生成 conftest.py 后，检查以下几点：

- [ ] 本服务 fixture 使用简化命名（如 `core_sc`）
- [ ] 其他服务 fixture 使用完整命名（如 `act_core_sc`）
- [ ] 所有 fixture 使用 `scope="function"`
- [ ] 所有 fixture 依赖 `env` 或 `lock` fixture
- [ ] 所有 fixture 包含类型注解
- [ ] 所有 fixture 包含文档字符串
- [ ] 导出所有 fixture 到 `__all__`
- [ ] 导入所有必要的插件 fixture
- [ ] Scenario 类正确初始化（传入 `env` 和 `lock`）

---

## 🚫 常见错误对比

### ❌ 错误 1: 本服务使用完整命名

```python
# ❌ 错误：本服务使用完整命名
@pytest.fixture(scope="function")
def eln_core_sc(env, lock) -> CoreScenario:
    return CoreScenario(env, lock)

# ❌ 错误：本服务使用完整命名
@pytest.fixture(scope="function")
def zabank_eln_approval_sc(env, lock) -> ApprovalScenario:
    return ApprovalScenario(env, lock)
```

### ✅ 正确 1: 本服务使用简化命名

```python
# ✅ 正确：本服务使用简化命名
@pytest.fixture(scope="function")
def core_sc(env, lock) -> CoreScenario:
    return CoreScenario(env, lock)

# ✅ 正确：本服务使用简化命名
@pytest.fixture(scope="function")
def approval_sc(env, lock) -> ApprovalScenario:
    return ApprovalScenario(env, lock)
```

---

### ❌ 错误 2: 其他服务使用简化命名

```python
# ❌ 错误：其他服务简化命名（可能冲突）
@pytest.fixture(scope="function")
def activity_sc(env, lock) -> ImcActivityScenario:
    return ImcActivityScenario(env, lock)

# ❌ 冲突：如果有多个 activity 服务
@pytest.fixture(scope="function")
def activity_sc(env, lock) -> ActActivityScenario:
    return ActActivityScenario(env, lock)
```

### ✅ 正确 2: 其他服务使用完整命名

```python
# ✅ 正确：其他服务使用完整命名（避免冲突）
@pytest.fixture(scope="function")
def imc_activity_sc(env, lock) -> ImcActivityScenario:
    return ImcActivityScenario(env, lock)

# ✅ 正确：不同前缀，不会冲突
@pytest.fixture(scope="function")
def act_activity_sc(env, lock) -> ActActivityScenario:
    return ActActivityScenario(env, lock)
```

---

### ❌ 错误 2: 使用 session scope

```python
# ❌ 错误：使用 session scope（共享状态，可能导致测试污染）
@pytest.fixture(scope="session")
def core_sc(env, lock) -> CoreScenario:
    return CoreScenario(env, lock)
```

### ✅ 正确 2: 使用 function scope

```python
# ✅ 正确：使用 function scope（每个测试独立）
@pytest.fixture(scope="function")
def core_sc(env, lock) -> CoreScenario:
    return CoreScenario(env, lock)
```

---

### ❌ 错误 3: 缺少类型注解

```python
# ❌ 错误：缺少类型注解
@pytest.fixture(scope="function")
def core_sc(env, lock):
    return CoreScenario(env, lock)
```

### ✅ 正确 3: 包含类型注解

```python
# ✅ 正确：包含类型注解
@pytest.fixture(scope="function")
def core_sc(env, lock) -> CoreScenario:
    return CoreScenario(env, lock)
```

---

## 📋 实际项目参考

### 实际项目示例

**关键特点**：

- ✅ 使用业务域名命名（`core_sc`、`activity_sc`）
- ✅ 移除项目前缀和组织层级
- ✅ 所有 fixture 使用 `function` scope
- ✅ 所有 fixture 依赖 `env` 和 `lock`
- ✅ 导出所有 fixture 到 `__all__`

---

**版本历史**:
- **v1.0** (2026-03-19): 初始版本，定义 Fixture 设计规范

---

**注意**: 这是基于**银行标准测试框架**（pytest_zabank 系列插件）的 Fixture 设计指南，适用于所有遵循银行测试架构规范的项目。
