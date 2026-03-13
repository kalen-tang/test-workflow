# Model类实例化规范

## ⚠️ 极其重要的规范

生成测试代码时,**必须**使用正确方式实例化Model类。这是框架核心约定,错误的写法会导致代码不可维护。

## ✅ 正确写法 (必须使用)

### 步骤1: 导入model模块

```python
from service.zabank_imc_activity_service import model
```

### 步骤2: 直接使用Model类实例化

```python
params = model.ActivityZaZoneGetVerifyCode()
params.json_data = {
    "revIdType": "EMAIL",
    "revId": "test@example.com",
    "redeemCode": "ABC123"
}
```

### 步骤3: 调用接口

```python
resp = activity_sc.controller.activity_za_zone_get_verify_code(
    load=params,
    headers=header
)
```

## ❌ 错误写法 (禁止使用)

### 错误1: 使用 method_to_model 动态查找

```python
# ❌ 绝对不要这样写!
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

**问题**:
1. 代码可读性差,无法直观看出使用的Model类
2. IDE无法提供自动补全和类型检查
3. 重构时难以追踪和修改
4. 运行时动态查找有性能开销
5. 违反Python最佳实践 (明确的静态导入 > 动态查找)

### 错误2: 直接导入类但不通过model模块

```python
# ❌ 不推荐这样写
from service.zabank_imc_activity_service.model.activity_za_zone_get_verify_code import ActivityZaZoneGetVerifyCode
params = ActivityZaZoneGetVerifyCode()
```

**问题**:
1. 导入路径过长,不够简洁
2. 不符合框架约定 (统一通过model模块导入)
3. 重构时需要修改多处导入语句

## 为什么必须使用正确写法?

### 1. 代码可读性

```python
# ✅ 清晰明了
params = model.ActivityZaZoneGetVerifyCode()

# ❌ 难以理解
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

一眼就能看出使用的Model类,无需追踪method_to_model的实现。

### 2. IDE支持

```python
# ✅ IDE可以提供:
# - 自动补全: model. → 显示所有可用Model类
# - 类型检查: params.json_data → 检查字段类型
# - 跳转定义: Ctrl+Click跳转到Model类定义
# - 查找引用: 查找所有使用该Model类的地方
params = model.ActivityZaZoneGetVerifyCode()

# ❌ IDE无法提供上述功能
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

### 3. 维护性

```python
# ✅ 重构时容易追踪和修改
# 如果ActivityZaZoneGetVerifyCode重命名为ActivityZaZoneVerifyCode
# IDE可以自动重构所有引用
params = model.ActivityZaZoneGetVerifyCode()

# ❌ 重构时需要手动查找字符串
# IDE无法识别字符串中的类名,容易遗漏
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

### 4. 性能

```python
# ✅ 编译时确定,无额外开销
params = model.ActivityZaZoneGetVerifyCode()

# ❌ 运行时动态查找,有额外开销
# 每次调用都需要:
# 1. 查找method_to_model方法
# 2. 传入字符串参数
# 3. 在mapping字典中查找
# 4. 返回对应的Model类
# 5. 实例化
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

### 5. 符合Python最佳实践

```python
# ✅ Explicit is better than implicit (Python之禅)
params = model.ActivityZaZoneGetVerifyCode()

# ❌ Magic is not Pythonic
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

## Model类命名规则

### 转换算法

从接口方法名(snake_case)转换为Model类名(PascalCase):

```python
def method_to_model_name(method_name: str) -> str:
    """
    接口方法名 → Model类名转换算法

    算法步骤:
    1. 按下划线分割字符串
    2. 每个单词首字母大写
    3. 拼接所有单词
    """
    words = method_name.split('_')
    words = [word.capitalize() for word in words]
    model_name = ''.join(words)
    return model_name
```

### 转换示例

| 接口方法名 (snake_case) | Model类名 (PascalCase) |
|------------------------|------------------------|
| `activity_za_zone_get_verify_code` | `ActivityZaZoneGetVerifyCode` |
| `activity_za_zone_entry_page` | `ActivityZaZoneEntryPage` |
| `activity_za_zone_homepage` | `ActivityZaZoneHomepage` |
| `activity_za_zone_verify` | `ActivityZaZoneVerify` |
| `activity_za_zone_quit` | `ActivityZaZoneQuit` |
| `reward_points_redeem` | `RewardPointsRedeem` |
| `reward_points_query` | `RewardPointsQuery` |
| `cuber_config_query` | `CuberConfigQuery` |
| `cuber_config_update` | `CuberConfigUpdate` |

### 详细转换过程示例

```python
# 示例1: activity_za_zone_get_verify_code
"activity_za_zone_get_verify_code"
→ 分割: ["activity", "za", "zone", "get", "verify", "code"]
→ 首字母大写: ["Activity", "Za", "Zone", "Get", "Verify", "Code"]
→ 拼接: "ActivityZaZoneGetVerifyCode"

# 示例2: reward_points_redeem
"reward_points_redeem"
→ 分割: ["reward", "points", "redeem"]
→ 首字母大写: ["Reward", "Points", "Redeem"]
→ 拼接: "RewardPointsRedeem"

# 示例3: cuber_config_query
"cuber_config_query"
→ 分割: ["cuber", "config", "query"]
→ 首字母大写: ["Cuber", "Config", "Query"]
→ 拼接: "CuberConfigQuery"
```

## 完整代码示例

### 示例1: Activity服务

```python
"""
@Project : zabank_imc_case
@File    : test_za_zone_get_verify_code.py
@Author  : Auto Generated
"""
import allure
import pytest
from pytest_zati_base.utils.assertion import Assertion
from pytest_zati_base.utils import logging

# ✅ 步骤1: 导入model模块
from service.zabank_imc_activity_service import model


@allure.epic("ZA Zone活动")
@allure.feature("验证码获取")
class TestZaZoneGetVerifyCode:
    """获取验证码接口测试类"""

    @allure.title("正常场景-获取验证码成功")
    @pytest.mark.data('za_zone/get_verify_code_01_success.yaml')
    @pytest.mark.P1
    def test_get_verify_code_01(self, activity_sc, data):
        """测试场景: 使用有效的邮箱和邀请码获取验证码"""
        step = data[0]

        header = {"language": "ca"}

        # ✅ 步骤2: 直接使用Model类实例化
        params = model.ActivityZaZoneGetVerifyCode()
        params.json_data = {
            "revIdType": step.get("revIdType", "EMAIL"),
            "revId": step.get("revId", ""),
            "redeemCode": step.get("redeemCode", "")
        }

        # ✅ 步骤3: 调用接口
        logging.info("测试获取验证码接口")
        resp = activity_sc.controller.activity_za_zone_get_verify_code(
            load=params,
            headers=header
        )

        # 验证响应码
        expected_code = step.get("expected_code", "000000")
        Assertion.str_assert(resp.json()["code"], expected_code)
        logging.info(f"响应码验证通过: {resp.json()['code']}")
```

### 示例2: Reward服务

```python
"""
@Project : zabank_imc_case
@File    : test_reward_points_redeem.py
@Author  : Auto Generated
"""
import allure
import pytest
from pytest_zati_base.utils.assertion import Assertion
from pytest_zati_base.utils import logging

# ✅ 步骤1: 导入model模块
from service.zabank_imc_reward_service import model


@allure.epic("积分系统")
@allure.feature("积分兑换")
class TestRewardPointsRedeem:
    """积分兑换接口测试类"""

    @allure.title("正常场景-积分兑换成功")
    @pytest.mark.data('reward/points_redeem_01_success.yaml')
    @pytest.mark.P0
    def test_points_redeem_01(self, reward_sc, data):
        """测试场景: 使用足够的积分兑换商品"""
        step = data[0]

        user_id = step.get("user_id", "")
        header = {"userid": user_id, "language": "ca"}

        # ✅ 步骤2: 直接使用Model类实例化
        params = model.RewardPointsRedeem()
        params.json_data = {
            "customerNo": step.get("customer_no", ""),
            "points": step.get("points", 0),
            "itemCode": step.get("item_code", "")
        }

        # ✅ 步骤3: 调用接口
        logging.info("测试积分兑换接口")
        resp = reward_sc.controller.reward_points_redeem(
            load=params,
            headers=header
        )

        # 验证响应码
        expected_code = step.get("expected_code", "000000")
        Assertion.str_assert(resp.json()["code"], expected_code)
        logging.info(f"响应码验证通过: {resp.json()['code']}")
```

### 示例3: Cuber服务

```python
"""
@Project : zabank_imc_case
@File    : test_cuber_config_query.py
@Author  : Auto Generated
"""
import allure
import pytest
from pytest_zati_base.utils.assertion import Assertion
from pytest_zati_base.utils import logging

# ✅ 步骤1: 导入model模块
from service.zabank_imc_cubercore_service import model


@allure.epic("配置管理")
@allure.feature("配置查询")
class TestCuberConfigQuery:
    """配置查询接口测试类"""

    @allure.title("正常场景-查询配置成功")
    @pytest.mark.data('cuber/config_query_01_success.yaml')
    @pytest.mark.P1
    def test_config_query_01(self, cuber_core_sc, data):
        """测试场景: 查询指定配置项"""
        step = data[0]

        header = {"language": "ca"}

        # ✅ 步骤2: 直接使用Model类实例化
        params = model.CuberConfigQuery()
        params.json_data = {
            "configKey": step.get("config_key", ""),
            "configType": step.get("config_type", "")
        }

        # ✅ 步骤3: 调用接口
        logging.info("测试配置查询接口")
        resp = cuber_core_sc.controller.cuber_config_query(
            load=params,
            headers=header
        )

        # 验证响应码
        expected_code = step.get("expected_code", "000000")
        Assertion.str_assert(resp.json()["code"], expected_code)
        logging.info(f"响应码验证通过: {resp.json()['code']}")
```

## 验证Model类是否存在

在生成测试代码前,验证Model类是否存在:

```python
def verify_model_class_exists(service_name: str, model_class_name: str) -> bool:
    """
    验证Model类是否存在于service层

    Args:
        service_name: 服务名称 (如 "zabank_imc_activity_service")
        model_class_name: Model类名 (如 "ActivityZaZoneGetVerifyCode")

    Returns:
        bool: 如果Model类存在返回True,否则返回False
    """
    try:
        # 尝试导入model模块
        model_module = __import__(f"service.{service_name}.model", fromlist=[''])

        # 检查类是否存在
        if hasattr(model_module, model_class_name):
            return True
        else:
            return False
    except ImportError:
        return False


# 使用示例
service_name = "zabank_imc_activity_service"
model_class_name = "ActivityZaZoneGetVerifyCode"

if verify_model_class_exists(service_name, model_class_name):
    print(f"✅ Model类 {model_class_name} 存在")
    # 生成测试代码: params = model.ActivityZaZoneGetVerifyCode()
else:
    print(f"❌ Model类 {model_class_name} 不存在")
    # 提示用户需要先创建Model类,或自动创建
```

## 自动创建缺失的Model类

如果Model类不存在,可以自动创建:

```python
def auto_create_model_class(
    service_name: str,
    model_class_name: str,
    api_path: str,
    http_method: str = "POST"
) -> str:
    """
    自动创建Model类文件

    Returns:
        str: 生成的Model类代码
    """
    # 转换类名为文件名: ActivityZaZoneGetVerifyCode → activity_za_zone_get_verify_code
    file_name = ''.join(['_' + c.lower() if c.isupper() else c for c in model_class_name]).lstrip('_')

    model_code = f'''"""
@Project : zabank_imc_case
@File    : {file_name}.py
@Author  : Auto Generated
"""
from pytest_zati_base.core.model import BaseModel


class {model_class_name}(BaseModel):
    """{api_path} 接口Model"""

    def __init__(self):
        super().__init__()
        self.method = "{http_method}"
        self.path = "{api_path}"
        self.json_data = {{}}
'''

    # 写入文件
    model_file_path = f"service/{service_name}/model/{file_name}.py"
    with open(model_file_path, 'w', encoding='utf-8') as f:
        f.write(model_code)

    print(f"✅ 已自动创建Model类: {model_file_path}")
    return model_code
```

## 更新__init__.py的mapping

创建Model类后,需要更新`service/{service_name}/__init__.py`的mapping:

```python
def update_service_mapping(
    service_name: str,
    method_name: str,
    model_class_name: str,
    interface_name: str
):
    """
    更新service的__init__.py的mapping字典

    Args:
        service_name: 服务名称
        method_name: 方法名 (snake_case)
        model_class_name: Model类名 (PascalCase)
        interface_name: 接口显示名称
    """
    init_file_path = f"service/{service_name}/__init__.py"

    # 读取现有内容
    with open(init_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 新增mapping条目
    new_mapping_entry = f'''
    "{method_name}": {{
        "method": model.{model_class_name},
        "action": "{interface_name}",
        "name": "{interface_name}"
    }},'''

    # 在mapping字典中添加新条目 (在最后一个}之前)
    # 简化实现: 这里只是示例,实际需要更复杂的解析逻辑
    updated_content = content.replace(
        "}\n}",  # mapping字典的结尾
        f"{new_mapping_entry}\n}}\n}}"
    )

    # 写回文件
    with open(init_file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✅ 已更新service mapping: {init_file_path}")
```

## 总结: 代码生成规范

生成测试代码时,**必须**:

1. ✅ 导入语句: `from service.{service_name} import model`
2. ✅ 实例化语句: `params = model.{ModelClassName}()`
3. ❌ 禁止使用: `params = {fixture}.controller.method_to_model("{method_name}")()`
4. ✅ 验证Model类存在,不存在时提示用户或自动创建
5. ✅ 使用正确的命名转换算法 (snake_case → PascalCase)

这是框架的核心约定,违反此规范会导致代码不可维护!
