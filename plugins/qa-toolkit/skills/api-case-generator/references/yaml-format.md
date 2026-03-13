# YAML测试数据格式参考

## 标准YAML文件结构

**核心原则**: 1个测试方法 = 1个YAML文件 = 1个case

```yaml
# data/{service_module}/{interface_name}_{scene_number}_{scene_name}.yaml
# 示例: data/za_zone/entry_page_01_joined.yaml

# ===== 环境配置部分 (可选,正常/边界场景需要) =====
env:
  sit:
    # 场景相关的测试账号
    {scenario}_user_id: "{实际user_id}"
    {scenario}_customer_no: "{实际customer_no}"

  auto_qe:
    {scenario}_user_id: "{实际user_id}"
    {scenario}_customer_no: "{实际customer_no}"

  uat:
    {scenario}_user_id: "{实际user_id}"
    {scenario}_customer_no: "{实际customer_no}"

# ===== 测试用例部分 (必须,且只包含1个case) =====
tests:
  - case: {用例名称}
    data:
      - step: {步骤名称}
        input:
          user_id: ${变量名}  # 引用env中的变量
          customer_no: ${变量名}
          param1: "value1"
        expected:
          expected_code: "000000"
        description: "{场景说明}"
```

## 环境配置规则

### 变量命名规范

使用`{场景}_user_id`格式,便于区分不同场景的测试账号:

```yaml
env:
  sit:
    # 正常场景
    normal_user_id: "2328059639100342784"
    normal_customer_no: "8000361216"

    # 未参与场景
    not_joined_user_id: "2328059639100342785"
    not_joined_customer_no: "8000361217"

    # VIP用户场景
    vip_user_id: "2328059639100342786"
    vip_customer_no: "8000361218"
```

### 变量引用语法

使用`${变量名}`引用环境变量,测试框架会根据`--envId`参数自动替换:

```yaml
tests:
  - case: 已参与用户查询
    data:
      - step: 查询活动状态
        input:
          user_id: ${normal_user_id}        # 自动替换为对应环境的值
          customer_no: ${normal_customer_no}
```

## 正常场景YAML示例

**特点**: 需要env配置,使用环境变量

```yaml
# data/za_zone/entry_page_01_joined.yaml

env:
  sit:
    joined_user_id: "2328059639100342784"
    joined_customer_no: "8000361216"
  auto_qe:
    joined_user_id: "2358240469768503808"
    joined_customer_no: "8000771073"
  uat:
    joined_user_id: "2351253385396617728"
    joined_customer_no: "8090337081"

tests:
  - case: 已参与用户查询
    data:
      - step: 已参与用户查询活动状态
        input:
          user_id: ${joined_user_id}
          customer_no: ${joined_customer_no}
        expected:
          expected_code: "IA0000"
        description: "用户已参与ZA Zone活动,查询返回活动状态"
```

## 边界场景YAML示例

**特点**: 需要env配置,测试边界值

```yaml
# data/za_zone/entry_page_03_boundary.yaml

env:
  sit:
    new_user_id: "2328059639100342799"
    new_customer_no: "8000361299"
  auto_qe:
    new_user_id: "2358240469768503899"
    new_customer_no: "8000771199"
  uat:
    new_user_id: "2351253385396617899"
    new_customer_no: "8090337199"

tests:
  - case: 新注册用户首次查询
    data:
      - step: 新用户首次查询活动
        input:
          user_id: ${new_user_id}
          customer_no: ${new_customer_no}
        expected:
          expected_code: "IA0000"
        description: "刚完成注册的新用户,首次查询活动状态"
```

## 异常场景YAML示例

**特点**: 不需要env配置,使用固定无效值

```yaml
# data/za_zone/entry_page_04_invalid.yaml

tests:
  - case: 客户不存在
    data:
      - step: 使用不存在的客户编号
        input:
          user_id: "9999999999999999"
          customer_no: "INVALID_CUST_NOT_EXIST"
        expected:
          expected_code: "400011"
        description: "客户编号不存在时返回错误"
```

```yaml
# data/za_zone/entry_page_05_missing_param.yaml

tests:
  - case: 缺少必填参数
    data:
      - step: 缺少customer_no参数
        input:
          user_id: "9999999999999999"
          customer_no: ""  # 缺少必填参数
        expected:
          expected_code: "400001"
        description: "缺少必填参数时返回参数错误"
```

## 文件命名规范

格式: `{interface_name}_{scene_number}_{scene_name}.yaml`

### 命名示例

| 场景类型 | 文件名 | 说明 |
|---------|-------|------|
| 正常场景1 | `entry_page_01_joined.yaml` | 已参与用户 |
| 正常场景2 | `entry_page_02_not_joined.yaml` | 未参与用户 |
| 边界场景 | `entry_page_03_boundary.yaml` | 新用户首次访问 |
| 异常场景1 | `entry_page_04_invalid.yaml` | 客户不存在 |
| 异常场景2 | `entry_page_05_missing_param.yaml` | 缺少参数 |

### 场景编号规则

- `01-09`: 正常场景
- `10-19`: 边界场景
- `20-29`: 异常场景 (参数错误)
- `30-39`: 异常场景 (业务错误)
- `40-49`: 异常场景 (系统错误)

## 文件组织结构

```
data/
├── za_zone/                           # 按模块/功能分目录
│   ├── entry_page_01_joined.yaml
│   ├── entry_page_02_not_joined.yaml
│   ├── entry_page_03_boundary.yaml
│   ├── entry_page_04_invalid.yaml
│   ├── entry_page_05_missing_param.yaml
│   ├── homepage_01_normal.yaml
│   ├── homepage_02_invalid.yaml
│   └── verify_01_success.yaml
├── reward/                            # 另一个模块
│   ├── redeem_01_normal.yaml
│   └── redeem_02_insufficient.yaml
└── cuber/                             # 第三个模块
    ├── config_query_01_normal.yaml
    └── config_query_02_invalid.yaml
```

## 特殊字段处理

### Email字段

```yaml
# 正常场景 - 使用环境变量
env:
  sit:
    test_email: "test_sit@example.com"
  auto_qe:
    test_email: "test_autoqe@example.com"

tests:
  - case: 正常邮箱验证
    data:
      - step: 发送验证码
        input:
          email: ${test_email}

# 异常场景 - 使用固定无效值
tests:
  - case: 邮箱格式错误
    data:
      - step: 无效邮箱格式
        input:
          email: "invalid-email-format"
```

### 手机号字段

```yaml
# 正常场景
env:
  sit:
    test_mobile: "12345678"
  auto_qe:
    test_mobile: "87654321"

tests:
  - case: 正常手机号验证
    data:
      - step: 发送短信验证码
        input:
          mobile: ${test_mobile}

# 异常场景
tests:
  - case: 手机号格式错误
    data:
      - step: 无效手机号
        input:
          mobile: "123"  # 位数不足
```

### 日期时间字段

```yaml
# 正常场景
tests:
  - case: 正常日期查询
    data:
      - step: 查询特定日期数据
        input:
          start_date: "2026-01-01"
          end_date: "2026-03-31"

# 异常场景
tests:
  - case: 日期格式错误
    data:
      - step: 无效日期格式
        input:
          start_date: "20260101"  # 格式错误
          end_date: "2026/03/31"  # 格式错误
```

### 金额字段

```yaml
# 正常场景
tests:
  - case: 正常金额交易
    data:
      - step: 积分兑换
        input:
          amount: "100.00"
          points: 1000

# 边界场景
tests:
  - case: 最小金额
    data:
      - step: 最小金额兑换
        input:
          amount: "0.01"
          points: 1

# 异常场景
tests:
  - case: 负数金额
    data:
      - step: 负数金额
        input:
          amount: "-100.00"
          points: -1000
```

## 复杂数据结构

### 嵌套对象

```yaml
tests:
  - case: 用户信息更新
    data:
      - step: 更新用户资料
        input:
          user_id: ${user_id}
          user_info:
            name: "Test User"
            email: ${test_email}
            address:
              city: "Hong Kong"
              district: "Central"
              street: "Test Street 123"
        expected:
          expected_code: "000000"
```

### 列表数据

```yaml
tests:
  - case: 批量查询用户
    data:
      - step: 批量查询
        input:
          customer_nos:
            - ${customer_no_1}
            - ${customer_no_2}
            - ${customer_no_3}
          activity_codes:
            - "ZA_ZONE"
            - "REWARD"
        expected:
          expected_code: "000000"
```

## 多步骤场景 (不推荐)

**注意**: 当前框架推荐1个YAML = 1个case = 1个step,避免参数化问题。

如果确实需要多步骤,使用以下格式:

```yaml
# ⚠️ 不推荐: 多步骤在一个YAML中
tests:
  - case: 完整兑换流程
    data:
      - step: 步骤1-获取验证码
        input:
          email: ${test_email}
        expected:
          expected_code: "000000"

      - step: 步骤2-验证码校验
        input:
          email: ${test_email}
          verify_code: "123456"  # 从步骤1获取
        expected:
          expected_code: "000000"

      - step: 步骤3-完成兑换
        input:
          email: ${test_email}
          token_id: "xxx"  # 从步骤2获取
        expected:
          expected_code: "000000"
```

**推荐做法**: 拆分为3个独立的测试方法,每个方法1个YAML文件。

## 环境变量替换机制

### 框架如何替换变量

```python
# pytest框架在运行时会:
# 1. 读取YAML文件
# 2. 根据 --envId 参数(如 sit/auto_qe/uat) 选择对应的env配置
# 3. 将 ${variable} 替换为实际值

# 示例:
# pytest --envId=sit testcases/test_entry_page.py

# YAML中:
# user_id: ${joined_user_id}

# 替换后:
# user_id: "2328059639100342784"  (sit环境的值)
```

### 测试代码如何获取

```python
# 测试代码中使用 .get() 方法获取数据
step = data[0]
user_id = step.get("user_id", "")  # 已经被框架替换为实际值
customer_no = step.get("customer_no", "")

# 如果YAML中写的是:
# user_id: ${joined_user_id}
#
# 那么step.get("user_id")会得到:
# "2328059639100342784" (sit环境)
# 或 "2358240469768503808" (auto_qe环境)
# 取决于运行时的 --envId 参数
```

## 错误格式对比

### ❌ 错误格式1: 旧格式(不支持多环境)

```yaml
# 问题: 写死了环境,无法在sit/auto_qe/uat之间切换
正常场景:
  user_id: "2367007718494994944"
  customer_no: "8000782594"
  expected_code: "000000"
```

### ❌ 错误格式2: 多个case在一个文件

```yaml
# 问题: 会导致pytest参数化,重复运行所有case
env:
  sit:
    user_id: "xxx"

tests:
  - case: 场景1
    data:
      - step: 步骤1
        input:
          user_id: ${user_id}

  - case: 场景2  # ❌ 不要在一个YAML中写多个case
    data:
      - step: 步骤2
        input:
          user_id: ${user_id}
```

### ❌ 错误格式3: 缺少tests列表

```yaml
# 问题: 缺少tests列表包裹,框架无法解析
env:
  sit:
    user_id: "xxx"

case: 正常场景  # ❌ 缺少tests:
data:
  - step: 查询
    input:
      user_id: ${user_id}
```

## ✅ 正确格式检查清单

生成YAML文件后,检查以下几点:

- [ ] 文件命名符合规范: `{interface}_{number}_{scene}.yaml`
- [ ] 正常/边界场景包含`env`配置
- [ ] 异常场景不包含`env`配置(或env为空)
- [ ] 必须有`tests:`列表包裹
- [ ] 每个YAML只有1个case
- [ ] 使用`${变量名}`语法引用环境变量
- [ ] expected中包含`expected_code`字段
- [ ] 每个字段都有合理的默认值或注释

## 环境切换命令

```bash
# SIT环境
pytest testcases/interface_case/test_za_zone_entry_page.py --envId=sit -v

# AutoQE环境
pytest testcases/interface_case/test_za_zone_entry_page.py --envId=auto_qe -v

# UAT环境
pytest testcases/interface_case/test_za_zone_entry_page.py --envId=uat -v

# 不指定envId时,使用pytest.ini中配置的默认环境
pytest testcases/interface_case/test_za_zone_entry_page.py -v
```

## pytest.ini环境配置

```ini
[pytest]
# 默认环境配置
envId = sit

# 或从命令行传入
# pytest --envId=uat
```
