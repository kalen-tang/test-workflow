# YAML 测试数据格式参考（v2.0）

**版本**: 2.0（基于银行标准测试框架）
**更新日期**: 2026-03-19
**适用框架**: pytest_zabank 系列插件（pytest_zabank_wholesale、pytest_zati_base 等）
**重大变更**: 使用 `variables` 替代 `env` 多环境配置

---

## 🏦 银行标准测试框架说明

本格式规范基于 **pytest_zabank 系列插件**，这是专为银行业务测试定制的标准化框架：

### 核心插件

- **pytest_zabank_wholesale**: 批发银行业务测试插件（BBM、Ticket、Zero 等）
- **pytest_zati_base**: 基础测试工具插件（Data、MySQL、XxlJob 等）
- **pytest_zabank_lns**: 贷款系统测试插件
- **pytest_zabank_momo**: 移动银行测试插件

### 框架特性

- ✅ **数据驱动**: 使用 `@pytest.mark.data()` 装饰器自动加载 YAML
- ✅ **变量替换**: 支持 `${变量名}` 语法，自动替换环境变量
- ✅ **Scenario 模式**: 封装业务逻辑，自动处理认证、断言、日志
- ✅ **多环境支持**: 通过 `env` fixture 切换 sit/qe/uat/prod 环境

---

## 📋 标准 YAML 文件结构

### 核心原则

- ✅ **1个接口 = 1个 YAML 文件 = 多个 step**
- ✅ **正常场景和异常场景分离为不同文件**
- ✅ **使用 `variables` 定义全局变量**
- ✅ **input 中包含方法名和 `json.reqBody` 结构**
- ✅ **移除 `expected` 字段（由 Scenario 处理断言）**

### 基础结构

```yaml
# data/{module}/{interface_group}.yaml

# ===== 全局变量（必须） =====
variables:
  username: ${ENV_USERNAME}
  password: ${ENV_PASSWORD}
  resource_id: 'RES_001'
  account_no: 'ACC_123456'

# ===== 测试用例（必须） =====
tests:
  - case: {功能模块描述}
    data:
      - step: 0{步骤名称}
        input:
          {method_name}:  # 关键：方法名作为 key
            json:
              reqBody:  # 关键：对应 Model 的 json_data 结构
                {param1}: ${variable1}
                {param2}: "fixed_value"
```

---

## 🔧 Variables 配置规则

### 变量命名规范

**推荐命名**：使用业务语义，避免环境前缀

```yaml
variables:
  # ✅ 推荐：业务语义命名
  username: TestUser
  password: TestPass123
  account_id: 'ACC_123456'
  resource_id: 'RES_001'

  # ✅ 可选：环境变量引用（由框架替换）
  test_user_id: ${TEST_USER_ID}
  test_account_no: ${TEST_ACCOUNT_NO}
```

**避免命名**：

```yaml
# ❌ 不推荐：过于复杂的环境前缀
sit_normal_user_id: "xxx"
qe_normal_user_id: "yyy"
prod_normal_user_id: "zzz"
```

### 变量引用语法

使用 `${变量名}` 引用变量：

```yaml
variables:
  account_id: 'ACC_123456'
  user_id: 'USER_001'

tests:
  - case: 账户查询接口测试
    data:
      - step: 0查询账户信息
        input:
          query_account_info:
            json:
              reqBody:
                accountId: ${account_id}  # 引用变量
                userId: ${user_id}
                pageSize: '10'
                currPage: '1'
```

---

## 📝 Tests 结构规则

### Input 结构（关键）

**重要**：`input` 中必须包含**方法名作为 key**，方便 Scenario 识别：

```yaml
- step: 0查询账户信息
  input:
    query_account_info:  # ✅ 方法名作为 key
      json:
        reqBody:  # ✅ 对应 Model 的 json_data 结构
          accountId: ${account_id}
          pageSize: '10'
```

**错误示例**：

```yaml
# ❌ 缺少方法名
- step: 0查询账户信息
  input:
    json:  # ❌ 错误：缺少方法名
      reqBody:
        accountId: ${account_id}
```

### Step 编号规则

使用数字前缀标识执行顺序：

```yaml
tests:
  - case: 完整业务流程测试
    data:
      - step: 0创建资源      # 第1步
      - step: 1查询资源      # 第2步
      - step: 2更新资源      # 第3步
      - step: 3删除资源      # 第4步
```

---

## 📚 正常场景示例

### 示例 1: 单接口查询

```yaml
# data/account/query_account.yaml

variables:
  username: TestUser
  password: TestPass123
  account_id: 'ACC_123456'
  user_id: 'USER_001'

tests:
  - case: 账户信息查询
    data:
      # ===== 步骤0: 查询账户基本信息 =====
      - step: 0查询账户信息
        input:
          query_account_info:
            json:
              reqBody:
                accountId: ${account_id}
                userId: ${user_id}
                pageSize: '10'
                currPage: '1'

      # ===== 步骤1: 查询账户明细 =====
      - step: 1查询账户明细
        input:
          query_account_details:
            json:
              reqBody:
                accountId: ${account_id}

      # ===== 步骤2: 查询账户历史 =====
      - step: 2查询账户历史
        input:
          query_account_history:
            json:
              reqBody:
                accountId: ${account_id}
                startDate: '2026-01-01'
                endDate: '2026-03-19'
```

### 示例 2: 包含数据准备步骤

```yaml
# data/resource/create_resource.yaml

variables:
  username: TestUser
  password: TestPass123
  resource_name: 'TestResource'

tests:
  - case: 资源创建流程
    data:
      - step: 登录系统
        input:
          login:
            username: ${username}
            password: ${password}

      - step: 获取数据
        input:
          env: "test"
          data_type: "resource_template"
          created_date: ${created_date}

      - step: 0创建资源
        input:
          create_resource:
            json:
              reqBody:
                resourceName: ${resource_name}
                resourceType: 'TYPE_A'
                status: 'active'
```

---

## ⚠️ 异常场景示例

### 特点

- ❌ **不使用 `variables`**（或使用固定无效值）
- ✅ **所有异常场景合并在一个 `_fail.yaml` 文件**
- ✅ **使用键值对访问（不是索引）**

### 示例: 异常测试文件

```yaml
# data/account/query_account_fail.yaml

variables:
  invalid_account_id: 'INVALID_ACC_999'
  invalid_user_id: 'INVALID_USER_999'

tests:
  - case: 账户查询异常场景
    data:
      # ===== 异常1: 参数有误 =====
      - step: 查询参数错误
        input:
          query_account_info:
            json:
              reqBody:
                wrongParam: ${invalid_account_id}  # ✅ 错误的参数名

      # ===== 异常2: 账户不存在 =====
      - step: 账户不存在
        input:
          query_account_info:
            json:
              reqBody:
                accountId: ${invalid_account_id}  # ✅ 无效的账户ID

      # ===== 异常3: 用户无权限 =====
      - step: 用户无权限
        input:
          query_account_info:
            json:
              reqBody:
                accountId: 'ACC_123456'
                userId: ${invalid_user_id}  # ✅ 无效的用户ID

      # ===== 异常4: 请求体为空 =====
      - step: 请求体为空
        input:
          query_account_info:
            json:
              reqBody: null  # ✅ 空请求体
```

---

## 🔄 正常场景 vs 异常场景对比

| 维度 | 正常场景 | 异常场景 |
|-----|---------|---------|
| **文件命名** | `query_account.yaml` | `query_account_fail.yaml` |
| **variables** | 使用有效变量 | 使用无效变量或固定值 |
| **step 访问** | `data[0]`, `data[1]` | `data["步骤名称"]` |
| **测试方法** | 每个场景一个方法 | 所有异常合并一个方法 |

---

## 📂 文件组织结构

```
data/
├── account/                          # 按模块分目录
│   ├── query_account.yaml            # 正常场景
│   ├── query_account_fail.yaml       # 异常场景
│   ├── create_account.yaml
│   └── create_account_fail.yaml
├── resource/
│   ├── create_resource.yaml
│   └── create_resource_fail.yaml
└── payment/
    ├── process_payment.yaml
    └── process_payment_fail.yaml
```

---

## 🎯 特殊字段处理

### 日期时间字段

```yaml
variables:
  start_date: '2026-01-01'
  end_date: '2026-03-19'
  created_date: '2026-03-19'

tests:
  - case: 日期范围查询
    data:
      - step: 查询指定日期范围
        input:
          query_by_date_range:
            json:
              reqBody:
                startDate: ${start_date}
                endDate: ${end_date}
                dateFormat: 'YYYY-MM-DD'
```

### 列表参数

```yaml
tests:
  - case: 批量操作
    data:
      - step: 批量创建资源
        input:
          batch_create_resources:
            json:
              reqBody:
                resourceNames:  # ✅ 列表参数
                  - 'Resource_A'
                  - 'Resource_B'
                  - 'Resource_C'
                approvers:
                  - 'User_001'
                  - 'User_002'
```

### 嵌套对象

```yaml
tests:
  - case: 复杂对象创建
    data:
      - step: 创建带详细信息的资源
        input:
          create_resource_with_details:
            json:
              reqBody:
                resourceName: 'ComplexResource'
                details:  # ✅ 嵌套对象
                  description: 'Resource description'
                  owner: 'TestUser'
                  metadata:
                    category: 'TypeA'
                    priority: 'high'
```

---

## ✅ 正确格式检查清单

生成 YAML 文件后，检查以下几点：

- [ ] 文件命名符合规范：`{module}/{interface_group}.yaml`
- [ ] 包含 `variables` 配置
- [ ] 必须有 `tests:` 列表包裹
- [ ] 每个 `step` 的 `input` 包含方法名
- [ ] `input.{method_name}.json.reqBody` 结构正确
- [ ] 使用 `${变量名}` 语法引用变量
- [ ] 异常场景分离到 `_fail.yaml` 文件
- [ ] Step 使用数字前缀（0、1、2...）

---

## 🚫 常见错误对比

### ❌ 错误格式 1: 旧版 env 配置

```yaml
# ❌ 旧格式（不推荐）
env:
  sit:
    user_id: "xxx"
  qe:
    user_id: "yyy"
  prod:
    user_id: "zzz"
```

### ✅ 正确格式 1: 使用 variables

```yaml
# ✅ 新格式（推荐）
variables:
  username: TestUser
  account_id: 'ACC_123456'
```

---

### ❌ 错误格式 2: 缺少方法名

```yaml
# ❌ input 中缺少方法名
- step: 0查询
  input:
    json:
      reqBody:
        accountId: ${account_id}
```

### ✅ 正确格式 2: 包含方法名

```yaml
# ✅ input 中包含方法名
- step: 0查询
  input:
    query_account_info:  # ✅ 方法名
      json:
        reqBody:
          accountId: ${account_id}
```

---

### ❌ 错误格式 3: 包含 expected 字段

```yaml
# ❌ 旧格式（包含 expected）
- step: 0查询
  input:
    query_account_info:
      json:
        reqBody:
          accountId: ${account_id}
  expected:  # ❌ 不需要
    expected_code: "000000"
```

### ✅ 正确格式 3: 移除 expected

```yaml
# ✅ 新格式（移除 expected）
- step: 0查询
  input:
    query_account_info:
      json:
        reqBody:
          accountId: ${account_id}
  # ✅ expected 由 Scenario 处理，不在 YAML 中定义
```

---

## 🔄 环境变量替换机制

### 框架如何替换变量

```python
# pytest框架在运行时会：
# 1. 读取YAML文件
# 2. 识别 ${变量名} 语法
# 3. 从环境变量或配置文件中获取值
# 4. 替换为实际值

# 示例:
# YAML中:
# account_id: ${ACCOUNT_ID}

# 替换后:
# account_id: "ACC_123456"
```

### 测试代码如何获取

```python
# 测试代码中通过 data fixture 获取数据
step = data[0]  # 获取第一个步骤

# 访问方法名和参数
method_input = step["query_account_info"]
req_body = method_input["json"]["reqBody"]

# 或使用字典访问（异常场景）
step = data["查询参数错误"]
```

---

## 📖 通用化命名建议

### 推荐的变量命名

```yaml
# ✅ 通用化命名
variables:
  username: TestUser
  password: TestPass123
  user_id: 'USER_001'
  account_id: 'ACC_123456'
  resource_id: 'RES_001'
  transaction_id: 'TXN_001'
  order_id: 'ORD_001'

# ❌ 避免项目特定命名
variables:
  eln_username: TestUser        # ❌ 包含项目前缀
  imc_customer_no: '8000123'    # ❌ 包含组织前缀
  zabank_loan_no: '88001234'    # ❌ 包含公司前缀
```

### 推荐的方法命名

```yaml
# ✅ 通用化方法名
query_account_info
create_resource
update_user_profile
delete_transaction

# ❌ 避免项目特定方法名
web_bank_query_by_loan_account_no  # ❌ 包含项目特征
imc_activity_za_zone_homepage      # ❌ 包含组织和项目特征
```

---

**版本历史**:
- **v1.0** (2026-02-25): 初始版本，使用 `env` 多环境配置
- **v2.0** (2026-03-19): 重大重构，使用 `variables` 替代 `env`，移除 `expected` 字段，完全通用化

---

**注意**: 这是基于**银行标准测试框架**（pytest_zabank 系列插件）的 YAML 格式规范，适用于所有遵循银行测试架构规范的项目。
