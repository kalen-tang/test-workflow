# Scenario 层设计指南

**版本**: 1.0
**创建日期**: 2026-03-19
**适用框架**: pytest_zabank 系列插件（银行标准测试框架）
**适用项目**: 所有遵循银行测试架构规范的测试项目

---

## 📋 Scenario 层职责

Scenario 层是银行标准测试框架的**核心业务逻辑封装层**,负责:

1. ✅ **封装业务流程**: 将多个接口调用组合成完整的业务场景
2. ✅ **参数构造**: 从 Step 对象提取参数,构造 Model 实例
3. ✅ **自动断言**: 统一处理响应码断言和业务规则验证
4. ✅ **日志记录**: 使用 `base_log()` 和 `@allure.step()` 记录执行步骤
5. ✅ **数据返回**: 返回解析后的业务数据供后续步骤使用

**设计原则**: 测试代码**只负责场景编排**,Scenario 层**负责业务逻辑**。

---

## 🏗️ 标准 Scenario 类结构

### 基础结构

```python
# scenario/core.py

import allure
from pytest_zabank_wholesale.scenario import Base, base_log
from pytest_zabank_wholesale.scenario import SSOScenario, BBMScenario
from pytest_zati_base.model import Step, Response
from service import controller, model


class CoreScenario(Base):
    """
    核心服务 Scenario 类

    职责:
    - 封装核心服务的所有接口调用
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
        self.host = env["hosts"]["core"]
        self.controller = controller.Controller(self.host)
        self.controller.default_timeout = 30
        self.controller.headers = {}
        self.sso_bss = SSOScenario(env)
        self.bbm_bss = BBMScenario(env)
        self.lock = lock
        self.common_expectation = {"code": "EL0000"}

    @allure.step("登录")
    def login(self, step: Step):
        """
        登录方法

        参数:
        - step: Step 对象（来自 data[index]）

        功能:
        - 调用 SSO 登录
        - 设置 Controller headers（token）
        """
        with base_log("系统登录"):
            login_data = step["login"]
            kw = {
                "username": login_data["username"],
                "password": login_data["password"],
                "service": "ZA-Bank-Core",
            }
            ticket, token = self.bbm_bss.new_login(**kw)
            self.controller.headers["token"] = token
            self.controller.headers["X-Usercenter-Session"] = token
```

### 关键组件说明

| 组件 | 类型 | 用途 | 示例 |
|------|------|------|------|
| `self.host` | str | 服务地址 | `env["hosts"]["core"]` |
| `self.controller` | Controller | 接口调用器 | `controller.Controller(self.host)` |
| `self.sso_bss` | SSOScenario | SSO 登录场景 | 处理认证 |
| `self.bbm_bss` | BBMScenario | BBM 业务场景 | 业务操作 |
| `self.lock` | Lock | 并发锁 | 防止资源冲突 |
| `self.common_expectation` | dict | 通用期望响应 | `{"code": "EL0000"}` |

---

## 📝 Scenario 方法设计模式

### 模式 1: 简单接口调用（最常用）

**特点**: 接收 Step 对象,构造 Model,调用 Controller,返回 JSON

```python
@allure.step("查询账户信息")
def query_account_info(self, step: Step):
    """
    查询账户信息

    参数:
    - step: Step 对象（来自 data[0]）

    返回:
    - dict: 响应 JSON 数据
    """
    # 步骤1: 构造 Model 实例（使用 ** 解包）
    data = model.QueryAccountInfo(**step["query_account_info"])

    # 步骤2: 调用 Controller
    resp = self.controller.query_account_info(data)

    # 步骤3: 返回 JSON（框架自动断言响应码）
    return resp.json()
```

**关键点**:
- ✅ 使用 `**step["method_name"]` 解包参数
- ✅ Model 构造器自动处理 `json.reqBody` 结构
- ✅ 返回 `.json()` 而非 Response 对象
- ✅ 框架自动断言 `code` 字段（通过 `self.common_expectation`）

---

### 模式 2: 手动参数赋值

**特点**: 手动从 Step 提取参数,逐个赋值到 Model

```python
@allure.step("查询换算汇率")
def query_exchange_rate(self, step: Step):
    """
    查询换算汇率

    参数:
    - step: Step 对象

    返回:
    - dict: 汇率信息
    """
    with base_log("查询换算汇率"):
        # 步骤1: 构造空 Model
        data = model.ContractQueryExchangeRate()

        # 步骤2: 手动赋值参数
        data.json_data.base_ccy = step["baseCcy"]
        data.json_data.exchange_ccy = step["exchangeCcy"]

        # 步骤3: 调用接口
        resp = self.controller.contract_query_exchange_rate(data)

        # 步骤4: 返回结果
        return resp.json()
```

**适用场景**:
- 需要参数转换或计算
- 参数结构与 YAML 不完全一致
- 需要添加默认值

---

### 模式 3: 复杂业务流程（多步骤）

**特点**: 多个接口调用组合,步骤间数据传递,业务逻辑处理

```python
@allure.step("放款申请（GP产品）")
def draw_down_gp(self, step: Step):
    """
    放款申请（GP产品）- 复杂业务流程

    参数:
    - step: Step 对象（包含 loan_account_no、submit、rolloverFlag 等）

    功能:
    1. 查询放款信息返显
    2. 计算到期日
    3. 获取担保信息
    4. 组装并保存放款数据
    5. 提交审批

    返回:
    - dict: 放款单号等信息
    """
    common_expectation = {"code": "EL0000"}

    # ===== 步骤1: 放款信息返显 =====
    with base_log("放款信息返显"):
        data = model.DrawDownContract()
        data.json_data.loan_account_no = step["loan_account_no"]
        resp = self.controller.draw_down_contract(data)
        self.soft_assert(resp.json(), common_expectation)
        draw_down: dict = resp.json()["value"]

        # 日期计算
        temp = parse(draw_down["valueDate"]) + timedelta(days=step["submit"].get("add_days", 0))
        draw_down["valueDate"] = temp.strftime("%Y-%m-%d")

        # 构造提交数据（合并 step 和返显数据）
        submit_data = model.DrawDownSave(**{"json": step["submit"] | draw_down})

    # ===== 步骤2: 获取到期日 =====
    with base_log("获取到期日"):
        data = model.DrawDownGetMaturityDate(
            **dict(
                json={
                    "valueDate": draw_down["valueDate"],
                    "loanPeriods": submit_data.json_data.loan_periods,
                    "termUnit": submit_data.json_data.term_unit,
                    "loanAccountNo": step["loan_account_no"],
                }
            )
        )
        resp = self.controller.draw_down_get_maturity_date(data)
        self.soft_assert(resp.json(), common_expectation)
        maturity_date = resp.json()["value"]

    # ===== 步骤3: 获取担保信息 =====
    with base_log("获取HKMIC担保信息"):
        model.ContractHkMciGuarantor()
        resp = self.controller.contract_hk_mci_guarantor(step["loan_account_no"])
        self.soft_assert(resp.json(), common_expectation)

    # ===== 步骤4: 保存放款信息 =====
    with base_log("保存放款信息"):
        # 参数计算和转换
        if submit_data.json_data.withdrawal_fee:
            withdrawal_fee = self.del_commas(str(submit_data.json_data.withdrawal_fee))
        else:
            withdrawal_fee = 0.0

        # 参数组装
        loan_amount = self.del_commas(str(submit_data.json_data.loan_amount))
        submit_data.json_data.loan_amount = float(loan_amount)
        submit_data.json_data.actual_pay_amount = float(loan_amount - withdrawal_fee)
        submit_data.json_data.maturity_date = maturity_date
        submit_data.json_data.exchange_rate = int(1)

        # 展期标志处理
        if step["rolloverFlag"]:
            submit_data.json_data.rollover_amount = step["submit"]["loanAmount"]
            submit_data.json_data.rollover_flag = "Y"
            submit_data.json_data.rollover_term_unit = step["submit"]["termUnit"]
            submit_data.json_data.rollover_loan_periods = step["submit"]["loanPeriods"]
        else:
            submit_data.json_data.rollover_flag = "N"

        # 调用保存接口
        resp = self.controller.draw_down_save(submit_data)
        self.soft_assert(resp.json(), common_expectation)
        draw_down_no = resp.json()["value"]

    # ===== 步骤5: 提交审批 =====
    with base_log("提交审批"):
        submit_approval_data = model.DrawDownSubmit()
        submit_approval_data.json_data.draw_down_no = draw_down_no
        resp = self.controller.draw_down_submit(submit_approval_data)
        self.soft_assert(resp.json(), common_expectation)

    # 返回关键信息
    return {"draw_down_no": draw_down_no, "loan_account_no": step["loan_account_no"]}
```

**关键技术**:
- ✅ 使用 `with base_log()` 记录每个子步骤
- ✅ 使用 `self.soft_assert()` 断言响应码
- ✅ 步骤间数据传递（`draw_down` → `submit_data` → `draw_down_no`）
- ✅ 业务逻辑处理（日期计算、金额计算、条件判断）
- ✅ 字典合并语法（`step["submit"] | draw_down`）

---

### 模式 4: 查询并返回业务数据

**特点**: 查询数据,提取关键字段,返回供后续使用

```python
@allure.step("还款回退（查询并组装数据）")
def draw_down_repayment_rollover(self, step: Step):
    """
    还款回退 - 复杂查询组装场景

    参数:
    - step: Step 对象（包含 loan_no、loan_account_no）

    功能:
    1. 查询待回退数据
    2. 查询借据详情
    3. 查询还款计划
    4. 查询银行账户
    5. 组装还款信息并提交

    返回:
    - dict: 还款信息
    """
    common_expectation = {"code": "EL0000"}

    # ===== 步骤1: 查询待回退数据 =====
    with base_log("查询待回退数据"):
        loan_list_data = model.AuditApprovalExistReturn()
        resp = self.controller.audit_approval_exist_return(loan_list_data)
        self.soft_assert(resp.json(), common_expectation)

    # ===== 步骤2: 查询借据详情内容 =====
    with base_log("查询借据详情内容"):
        loan_list_data = model.LoanInfoContent()
        loan_list_data.params_data.loan_no = step["loan_no"]
        resp = self.controller.loan_info_content(loan_list_data)
        loan_detail = resp.json()["value"]
        self.soft_assert(resp.json(), common_expectation)

    # ===== 步骤3: 查询贷款账户列表 =====
    with base_log("查询贷款账户列表"):
        loan_list_data = model.RepaymentList()
        loan_list_data.json_data.loan_no = step["loan_no"]
        loan_list_data.json_data.curr_page = 1
        loan_list_data.json_data.page_size = 10
        resp = self.controller.repayment_list(loan_list_data)
        plan_no = resp.json()["value"]["list"][0]["planNo"]
        self.soft_assert(resp.json(), common_expectation)

    # ===== 步骤4: 查询还款详情 =====
    with base_log("查询还款详情"):
        data = model.RepaymentDetail()
        data.params_data.plan_no = plan_no
        resp = self.controller.repayment_detail(data)
        repayment_detail = resp.json()["value"]
        self.soft_assert(resp.json(), common_expectation)

    # ===== 步骤5: 查询放款信息 =====
    with base_log("查询放款信息"):
        draw_down_data = model.DrawDownContract()
        draw_down_data.json_data.loan_account_no = step["loan_account_no"]
        resp = self.controller.draw_down_contract(draw_down_data)
        self.soft_assert(resp.json(), common_expectation)
        draw_down_detail = resp.json()["value"]

    # ===== 步骤6: 查询银行账户详情 =====
    with base_log("查询银行账户详情"):
        bank_account_data = model.RepaymentQueryBankAccountDetailInfo()
        bank_account_data.params_data.ccy = draw_down_detail["ccy"]
        bank_account_data.params_data.bank_account_no = draw_down_detail["repaymentAccountNo"]
        resp = self.controller.repayment_query_bank_account_detail_info(bank_account_data)
        self.soft_assert(resp.json(), common_expectation)

    # ===== 步骤7: 查询内部账户 =====
    with base_log("查询内部账户"):
        internal_account_data = model.DrawDownQueryInternalAccount()
        resp = self.controller.draw_down_query_internal_account(internal_account_data)
        self.soft_assert(resp.json(), common_expectation)
        internal_account = resp.json()["value"]

    # ===== 步骤8: 组装还款信息并提交 =====
    with base_log("组装还款信息"):
        # ... 组装逻辑 ...
        pass

    # 返回关键信息
    return {
        "loan_detail": loan_detail,
        "repayment_detail": repayment_detail,
        "plan_no": plan_no
    }
```

**关键技术**:
- ✅ 多个接口顺序调用,步骤间数据传递
- ✅ 从响应中提取字段（`resp.json()["value"]["list"][0]["planNo"]`）
- ✅ 参数动态赋值（使用前一步查询结果）
- ✅ 返回组装后的数据供测试代码使用

---

## 🔧 关键技术细节

### 1. Step 对象访问

**Step 结构**（来自 YAML）:

```yaml
- step: 0查询账户信息
  input:
    query_account_info:
      json:
        reqBody:
          accountId: ${account_id}
          userId: ${user_id}
```

**Scenario 中访问**:

```python
def query_account_info(self, step: Step):
    # 方式1: 使用 ** 解包（推荐,自动处理嵌套）
    data = model.QueryAccountInfo(**step["query_account_info"])

    # 方式2: 手动访问嵌套字段
    req_body = step["query_account_info"]["json"]["reqBody"]
    data = model.QueryAccountInfo()
    data.json_data.account_id = req_body["accountId"]
    data.json_data.user_id = req_body["userId"]
```

---

### 2. 断言处理

**自动断言**（框架处理）:

```python
# Model 类内部定义了 common_expectation
self.common_expectation = {"code": "EL0000"}

# 调用接口时框架自动断言
resp = self.controller.query_account_info(data)
# 框架检查: resp.json()["code"] == "EL0000"
```

**手动断言**（需要额外验证）:

```python
# 使用 soft_assert（不中断执行）
resp = self.controller.query_account_info(data)
self.soft_assert(resp.json(), {"code": "EL0000"})

# 使用 assert（中断执行）
resp = self.controller.query_account_info(data)
assert resp.json()["code"] == "EL0000", f"响应码错误: {resp.json()['code']}"
```

---

### 3. 日志和 Allure 集成

**双层日志**:

```python
@allure.step("查询账户信息")  # Allure 报告步骤
def query_account_info(self, step: Step):
    with base_log("查询账户信息"):  # 控制台日志
        data = model.QueryAccountInfo(**step["query_account_info"])
        resp = self.controller.query_account_info(data)
        return resp.json()
```

**嵌套步骤**:

```python
@allure.step("放款申请")
def draw_down_gp(self, step: Step):
    with base_log("放款信息返显"):  # 子步骤1
        # ...
    with base_log("获取到期日"):    # 子步骤2
        # ...
    with base_log("保存放款信息"):  # 子步骤3
        # ...
```

---

### 4. 参数处理技巧

**字典合并**（Python 3.9+）:

```python
# 合并 step 参数和查询结果
submit_data = model.DrawDownSave(**{"json": step["submit"] | draw_down})

# 等价于:
merged = {**step["submit"], **draw_down}
submit_data = model.DrawDownSave(**{"json": merged})
```

**参数转换**:

```python
# 移除千分位分隔符
loan_amount = self.del_commas(str(submit_data.json_data.loan_amount))
submit_data.json_data.loan_amount = float(loan_amount)

# 日期计算
temp = parse(draw_down["valueDate"]) + timedelta(days=step["submit"].get("add_days", 0))
draw_down["valueDate"] = temp.strftime("%Y-%m-%d")
```

**条件赋值**:

```python
# 根据标志位设置不同参数
if step["rolloverFlag"]:
    submit_data.json_data.rollover_flag = "Y"
    submit_data.json_data.rollover_amount = step["submit"]["loanAmount"]
else:
    submit_data.json_data.rollover_flag = "N"
    submit_data.json_data.rollover_amount = None
```

---

## 📂 Scenario 文件组织

### 标准目录结构

```
scenario/
├── __init__.py
├── core.py              # 核心服务 Scenario
├── approval.py          # 审批服务 Scenario
├── account.py           # 账户服务 Scenario
└── options.py           # 枚举类和常量
```

### 导入规范

```python
# scenario/__init__.py

from .core import CoreScenario
from .approval import ApprovalScenario
from .account import AccountScenario

__all__ = [
    "CoreScenario",
    "ApprovalScenario",
    "AccountScenario",
]
```

---

## ✅ Scenario 设计检查清单

生成 Scenario 类后,检查以下几点:

- [ ] 继承 `Base` 类（来自 `pytest_zabank_wholesale.scenario`）
- [ ] `__init__` 方法接收 `env` 和 `lock` 参数
- [ ] 初始化 `self.controller`（Controller 实例）
- [ ] 定义 `self.common_expectation`（通用响应码）
- [ ] 所有方法接收 `step: Step` 参数
- [ ] 使用 `@allure.step()` 装饰器
- [ ] 使用 `with base_log()` 记录日志
- [ ] 使用 `self.soft_assert()` 或 `assert` 断言
- [ ] 返回解析后的数据（`.json()` 或 `.json()["value"]`）
- [ ] 文档字符串清晰描述功能和参数

---

## 🚫 常见错误对比

### ❌ 错误 1: 返回 Response 对象

```python
# ❌ 错误：返回 Response 对象
def query_account_info(self, step: Step):
    data = model.QueryAccountInfo(**step["query_account_info"])
    return self.controller.query_account_info(data)  # ❌ Response 对象
```

### ✅ 正确 1: 返回 JSON 数据

```python
# ✅ 正确：返回 JSON 数据
def query_account_info(self, step: Step):
    data = model.QueryAccountInfo(**step["query_account_info"])
    resp = self.controller.query_account_info(data)
    return resp.json()  # ✅ dict
```

---

### ❌ 错误 2: 缺少日志记录

```python
# ❌ 错误：没有日志记录
@allure.step("查询账户信息")
def query_account_info(self, step: Step):
    data = model.QueryAccountInfo(**step["query_account_info"])
    resp = self.controller.query_account_info(data)
    return resp.json()
```

### ✅ 正确 2: 使用 base_log

```python
# ✅ 正确：使用 base_log 记录日志
@allure.step("查询账户信息")
def query_account_info(self, step: Step):
    with base_log("查询账户信息"):
        data = model.QueryAccountInfo(**step["query_account_info"])
        resp = self.controller.query_account_info(data)
        return resp.json()
```

---

### ❌ 错误 3: 手动构造 Model 而不使用 Step

```python
# ❌ 错误：测试代码中手动构造 Model
def test_query_account(self, data, account_sc):
    params = model.QueryAccountInfo()
    params.json_data.account_id = "ACC_123"
    account_sc.query_account_info(params)  # ❌ 传入 Model 对象
```

### ✅ 正确 3: Scenario 接收 Step 对象

```python
# ✅ 正确：测试代码传入 Step 对象
def test_query_account(self, data, account_sc):
    account_sc.query_account_info(data[0])  # ✅ 传入 Step 对象

# Scenario 方法内部构造 Model
def query_account_info(self, step: Step):
    data = model.QueryAccountInfo(**step["query_account_info"])
    resp = self.controller.query_account_info(data)
    return resp.json()
```

---

## 📖 完整示例

### 标准 Scenario 类

```python
# scenario/account.py

import allure
from pytest_zabank_wholesale.scenario import Base, base_log
from pytest_zati_base.model import Step
from service import controller, model


class AccountScenario(Base):
    """账户服务 Scenario 类"""

    def __init__(self, env, lock):
        """初始化"""
        self.host = env["hosts"]["account"]
        self.controller = controller.Controller(self.host)
        self.controller.default_timeout = 30
        self.controller.headers = {}
        self.lock = lock
        self.common_expectation = {"code": "AC0000"}

    @allure.step("查询账户信息")
    def query_account_info(self, step: Step):
        """查询账户信息（简单调用）"""
        with base_log("查询账户信息"):
            data = model.QueryAccountInfo(**step["query_account_info"])
            resp = self.controller.query_account_info(data)
            return resp.json()

    @allure.step("创建账户")
    def create_account(self, step: Step):
        """创建账户（手动参数赋值）"""
        with base_log("创建账户"):
            data = model.CreateAccount()
            data.json_data.account_name = step["accountName"]
            data.json_data.account_type = step["accountType"]
            data.json_data.currency = step.get("currency", "HKD")
            resp = self.controller.create_account(data)
            self.soft_assert(resp.json(), self.common_expectation)
            return resp.json()["value"]

    @allure.step("账户开户流程")
    def account_open_flow(self, step: Step):
        """账户开户流程（复杂业务）"""
        common_expectation = {"code": "AC0000"}

        # 步骤1: 验证客户信息
        with base_log("验证客户信息"):
            data = model.VerifyCustomer()
            data.json_data.customer_no = step["customerNo"]
            resp = self.controller.verify_customer(data)
            self.soft_assert(resp.json(), common_expectation)

        # 步骤2: 创建账户
        with base_log("创建账户"):
            data = model.CreateAccount()
            data.json_data.customer_no = step["customerNo"]
            data.json_data.account_type = step["accountType"]
            resp = self.controller.create_account(data)
            self.soft_assert(resp.json(), common_expectation)
            account_id = resp.json()["value"]["accountId"]

        # 步骤3: 激活账户
        with base_log("激活账户"):
            data = model.ActivateAccount()
            data.json_data.account_id = account_id
            resp = self.controller.activate_account(data)
            self.soft_assert(resp.json(), common_expectation)

        # 返回账户ID
        return {"account_id": account_id, "customer_no": step["customerNo"]}
```

---

**版本历史**:
- **v1.0** (2026-03-19): 初始版本,定义 Scenario 层设计规范

---

**注意**: 这是基于**银行标准测试框架**（pytest_zabank 系列插件）的 Scenario 层设计指南,适用于所有遵循银行测试架构规范的项目。
