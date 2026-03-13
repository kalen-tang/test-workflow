# 服务映射参考

## 支持的服务列表

ZA Bank微服务完整列表:

| 服务名称 | Service目录 | Scenario类 | Config配置键 | 路径前缀 |
|---------|------------|-----------|-------------|---------|
| IMC Activity | zabank_imc_activity_service | ActivityScenario | zabank_imc_activity_service | `/activity/*` |
| IMC Cubercore | zabank_imc_cubercore_service | CubercoreScenario | zabank_imc_cubercore_service | `/cuber/*` |
| IMC Reward | zabank_imc_reward_service | RewardScenario | zabank_imc_reward_service | `/reward/*` |
| IMC Interestcore | zabank_imc_interestcore_service | InterestcoreScenario | zabank_imc_interestcore_service | `/interest/*` |
| RCS Core | zabank_rcs_core | RCSScenario | zabank_rcs_core_service | `/rc/*` |
| Act Core | zabank_act_core_service | - | zabank_act_core_service | `/act/*` |
| BMS Batch | zabank_bms_batch_service | - | zabank_bms_batch_service | `/batch/*` |
| Corefront | zabank_corefront_service | - | zabank_cbs_corefront_service | `/corefront/*` |
| MBS Statistics | zabank_mbs_statistics_service | - | zabank_mbs_statistics_service | `/statistics/*` |
| MBS UserCenter | zabank_mbs_usercenter_service | - | zabank_mbs_usercenter_service | `/usercenter/*` |
| MKS Marketing | zabank_mks_marketing_service | - | zabank_mks_marketing_service | `/marketing/*` |
| Sales Coupon | zaip_sales_coupon_service | - | zaip-sales-coupon-service | `/coupon/*` |

## Scenario文件映射

Scenario类位置映射:

```python
scenario_files = {
    "zabank_imc_activity_service": "scenario/imc/activity_scenario.py",
    "zabank_imc_cubercore_service": "scenario/imc/cubercore_scenario.py",
    "zabank_imc_reward_service": "scenario/imc/reward_scenario.py",
    "zabank_imc_interestcore_service": "scenario/imc/interestcore_scenario.py",
    "zabank_rcs_core": "scenario/rcs/rcs_scenario.py",
}
```

## 自动扩展支持

遇到新服务时的处理流程:

1. **扫描 `service/` 目录**
   ```python
   import os
   services = [d for d in os.listdir("service") if os.path.isdir(f"service/{d}")]
   ```

2. **读取Service的 `__init__.py`**
   - 解析 `mapping` 字典获取可用接口方法
   - 提取Model类和controller方法

3. **查找或提示创建Scenario类**
   - 检查 `scenario/` 目录下是否存在对应的scenario文件
   - 如缺失,提示用户或直接使用Controller层

4. **自动生成适配配置**
   - 创建fixture命名: `{service_domain}_sc`
   - 映射到环境YAML文件中的配置键
   - 生成服务特定的测试模板

## 路径前缀到服务的转换算法

```python
def path_to_service(api_path: str) -> str:
    """将API路径转换为服务名称"""
    path_mapping = {
        "/activity": "zabank_imc_activity_service",
        "/rc": "zabank_rcs_core",
        "/cuber": "zabank_imc_cubercore_service",
        "/reward": "zabank_imc_reward_service",
        "/interest": "zabank_imc_interestcore_service",
        "/act": "zabank_act_core_service",
        "/batch": "zabank_bms_batch_service",
        "/corefront": "zabank_corefront_service",
        "/statistics": "zabank_mbs_statistics_service",
        "/usercenter": "zabank_mbs_usercenter_service",
        "/marketing": "zabank_mks_marketing_service",
        "/coupon": "zaip_sales_coupon_service",
    }

    # 提取域名后的第一个路径段
    # 示例: /dmb/nok9iy/activity/zazone/getVerifyCode → /activity
    segments = [s for s in api_path.split('/') if s]

    # 检查每个段是否匹配映射
    for segment in segments:
        key = f"/{segment}"
        if key in path_mapping:
            return path_mapping[key]

    raise ValueError(f"无法从路径识别服务: {api_path}")
```

## Service层结构

典型的service层结构:

```
service/zabank_imc_activity_service/
├── __init__.py          # mapping字典,包含controller方法
├── controller.py        # HTTP客户端封装
└── model/
    ├── __init__.py
    ├── activity_za_zone_get_verify_code.py  # Model类文件
    ├── activity_za_zone_verify.py
    └── ...
```

**`__init__.py` 结构**:

```python
from service.zabank_imc_activity_service import model

mapping = {
    "activity_za_zone_get_verify_code": {
        "method": model.ActivityZaZoneGetVerifyCode,
        "action": "获取ZA Zone验证码",
        "name": "getVerifyCode"
    },
    "activity_za_zone_verify": {
        "method": model.ActivityZaZoneVerify,
        "action": "ZA Zone验证码校验",
        "name": "verify"
    },
    # ... 更多映射
}
```

## Fixture命名约定

基于服务域生成fixture名称:

```python
def service_to_fixture_name(service_name: str) -> str:
    """将服务名称转换为fixture名称"""
    # zabank_imc_activity_service → activity_sc
    # zabank_imc_cubercore_service → cuber_core_sc
    # zabank_imc_reward_service → reward_sc

    if "imc_activity" in service_name:
        return "activity_sc"
    elif "imc_cubercore" in service_name:
        return "cuber_core_sc"
    elif "imc_reward" in service_name:
        return "reward_sc"
    elif "imc_interestcore" in service_name:
        return "interest_core_sc"
    elif "rcs_core" in service_name:
        return "rcs_sc"
    else:
        # 通用转换: 提取_service前的最后一部分
        parts = service_name.replace("_service", "").split("_")
        return f"{parts[-1]}_sc"
```

## 添加新服务

添加新服务支持的步骤:

1. **更新服务映射表** (上面的表格)
2. **添加路径前缀映射** (在 `path_to_service` 函数中)
3. **创建Scenario类** (如需要):
   ```python
   # scenario/{module}/{service}_scenario.py
   from pytest_zati_base.core.scenario import Scenario
   from service.{service_name}.controller import {ServiceName}Controller

   class {ServiceName}Scenario(Scenario):
       def __init__(self, config):
           super().__init__(config)
           self.controller = {ServiceName}Controller(config)
   ```
4. **在conftest.py添加Fixture**:
   ```python
   @pytest.fixture(scope="session")
   def {service}_sc(config):
       return {ServiceName}Scenario(config)
   ```
5. **测试新服务**:
   - 生成一个简单测试用例
   - 验证fixture加载正确
   - 验证API调用正常工作
