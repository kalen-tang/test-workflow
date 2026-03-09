# ZA Bank 接口自动化测试生成器 - 使用指南

## 🎯 Skill概述

这是一个**ZA Bank通用接口自动化测试生成器**,可以根据接口文档自动生成完整的测试代码、测试数据和执行脚本。

### 核心特性

- ✅ **服务无关**: 支持所有ZA Bank微服务(zabank-imc-activity、zabank-act-core、zabank-bms-batch等)
- ✅ **多环境支持**: 自动生成支持sit/auto_qe/uat三环境的测试数据
- ✅ **格式统一**: 基于标准接口文档格式生成
- ✅ **智能适配**: 自动识别服务类型和接口映射
- ✅ **完整生成**: 一次性生成测试代码、数据、文档、脚本
- ✅ **边界处理**: 自动处理Service层缺失和测试数据缺失情况

---

## 📁 Skill文件

### 主要文件

| 文件 | 说明 |
|------|------|
| `skill/api-test-generator.skill.md` | Skill配置文件(包含完整使用说明) |
| `skill/ZA_Zone.md` | ZA Zone接口文档示例 |

### 已生成的示例文件

| 文件 | 说明 |
|------|------|
| `testcases/interface_case/test_za_zone_entry_page.py` | 测试代码(5个测试方法) |
| `data/za_zone/entry_page_01_joined.yaml` | 测试数据1(已参与用户) |
| `data/za_zone/entry_page_02_not_joined.yaml` | 测试数据2(未参与用户) |
| `data/za_zone/entry_page_03_relative.yaml` | 测试数据3(员工亲友) |
| `data/za_zone/entry_page_04_invalid.yaml` | 测试数据4(客户不存在) |
| `data/za_zone/entry_page_05_missing.yaml` | 测试数据5(参数缺失) |
| `conftest.py` | 添加了activity_sc fixture |

### ⚠️ 重要说明

**v1.4版本关键变更**:
- ✅ **1个测试方法 = 1个YAML文件** (避免参数化导致重复运行)
- ✅ **测试代码使用`data[0]`** (获取tests列表的第一个case)
- ✅ **必须在conftest.py添加fixture** (如activity_sc)
- ✅ **YAML命名**: `{interface}_{scene_number}_{scene_name}.yaml`

---

## 🚀 快速开始

### 步骤1: 准备接口文档

创建符合格式的接口文档Markdown文件(参考`skill/ZA_Zone.md`):

```markdown
## 接口X: 接口名称

### 接口信息
- **接口路径**: `/path/to/api`
- **请求方法**: POST
- **功能描述**: 接口功能说明

### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|

### 响应参数
| 字段名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|

### 接口X测试用例
#### 功能测试
##### 1. 正常场景测试
- **用例描述**: ...
- **请求参数**: ```json {...} ```
- **预期结果**: ```json {...} ```
```

### 步骤2: 使用Skill生成测试

调用Skill生成测试代码:

```
"请根据skill/ZA_Zone.md的接口3生成测试用例"
```

### 步骤3: 更新测试数据

编辑生成的YAML文件,填入各环境的真实测试账号:

```yaml
env:
  sit:
    joined_user_id: "你的sit环境user_id"
    joined_customer_no: "你的sit环境customer_no"
  auto_qe:
    joined_user_id: "你的autoqe环境user_id"
    joined_customer_no: "你的autoqe环境customer_no"
  uat:
    joined_user_id: "你的uat环境user_id"
    joined_customer_no: "你的uat环境customer_no"
```

### 步骤4: 运行测试

```bash
# 在UAT环境运行(默认)
pytest testcases/interface_case/test_za_zone_entry_page.py -v -s

# 在SIT环境运行
pytest testcases/interface_case/test_za_zone_entry_page.py -v -s --envId=sit

# 在AutoQE环境运行
pytest testcases/interface_case/test_za_zone_entry_page.py -v -s --envId=auto_qe
```

---

## 💡 使用示例

### 示例1: 为单个接口生成测试

```
"请根据ZA_Zone.md的接口1生成测试用例"
```

**生成内容**:
- ✅ 测试代码: `testcases/interface_case/test_za_zone_get_verify_code.py`
- ✅ 测试数据: `data/za_zone/get_verify_code.yaml` (支持3环境)
- ✅ 测试文档: `docs/za_zone_get_verify_code_test_guide.md`

### 示例2: 批量生成测试套件

```
"请根据ZA_Zone.md生成所有接口的测试套件"
```

**生成内容**:
- ✅ 11个测试代码文件
- ✅ 11个测试数据文件(全部支持多环境)
- ✅ 测试计划文档
- ✅ 批量执行脚本

### 示例3: 为其他服务生成测试

```
"请根据skill/Reward_System.md为reward服务生成接口测试"
```

Skill会自动识别服务类型并生成对应的测试代码。

---

## 🎨 多环境测试数据格式⭐

### 标准格式

**必须使用以下格式**:

```yaml
# ===== 环境配置 =====
env:
  sit:
    scenario1_user_id: "sit环境的user_id"
    scenario1_customer_no: "sit环境的customer_no"

  auto_qe:
    scenario1_user_id: "autoqe环境的user_id"
    scenario1_customer_no: "autoqe环境的customer_no"

  uat:
    scenario1_user_id: "uat环境的user_id"
    scenario1_customer_no: "uat环境的customer_no"

# ===== 测试用例 =====
tests:
  - case: 测试场景描述
    data:
      - step: 步骤名称
        input:
          user_id: ${scenario1_user_id}  # 使用${}引用环境变量
          customer_no: ${scenario1_customer_no}
          param1: "value1"
        expected:
          expected_code: "000000"
        description: "场景说明"
```

### 关键点说明

1. **环境配置(`env`部分)**:
   - 必须包含`sit`、`auto_qe`、`uat`三个环境
   - 每个环境配置独立的测试账号

2. **变量引用**:
   - 使用`${变量名}`语法引用环境配置
   - 测试框架根据`--envId`参数自动替换

3. **场景区分**:
   - 正常/边界场景: 使用环境变量
   - 异常场景: 使用固定无效值

4. **测试代码适配**:
   ```python
   step = data["步骤名称"]
   user_id = step.get("user_id", "")  # 自动替换${变量}
   customer_no = step.get("customer_no", "")
   ```

---

## 📊 生成的文件结构

```
zabank_imc_case/
├── testcases/interface_case/
│   └── test_{service}_{interface}.py       # 测试代码
├── data/{service}/
│   └── {interface}.yaml                    # 测试数据(多环境)
├── docs/
│   └── {service}_{interface}_test_guide.md # 测试文档
└── scripts/
    └── run_{service}_{interface}_test.sh   # 执行脚本
```

---

## 📝 示例对比

### ❌ 旧格式(不支持多环境)

```yaml
正常场景:
  user_id: "2367007718494994944"
  customer_no: "8000782594"
  expected_code: "000000"

异常场景:
  user_id: "2367007718494994945"
  customer_no: "8000782595"
  expected_code: "400001"
```

**问题**:
- 不支持多环境
- 切换环境需要手动修改数据
- 容易出错

### ✅ 新格式(支持多环境)

```yaml
env:
  sit:
    normal_user_id: "sit_user_id"
    normal_customer_no: "sit_customer_no"
  auto_qe:
    normal_user_id: "autoqe_user_id"
    normal_customer_no: "autoqe_customer_no"
  uat:
    normal_user_id: "uat_user_id"
    normal_customer_no: "uat_customer_no"

tests:
  - case: 正常场景测试
    data:
      - step: 正常场景
        input:
          user_id: ${normal_user_id}
          customer_no: ${normal_customer_no}
        expected:
          expected_code: "000000"

  - case: 异常场景测试
    data:
      - step: 异常场景
        input:
          customer_no: "INVALID_CUSTOMER"  # 异常场景用固定值
        expected:
          expected_code: "400001"
```

**优势**:
- ✅ 支持多环境
- ✅ 切换环境只需改`--envId`参数
- ✅ 数据集中管理,不易出错

---

## 🎯 最佳实践

### 1. 数据准备

每个环境准备以下类型的测试账号:

| 账号类型 | 用途 | 变量命名 |
|---------|------|---------|
| 已参与用户 | 测试正常场景 | `joined_user_id` |
| 未参与用户 | 测试未参与场景 | `not_joined_user_id` |
| 特殊身份用户 | 测试边界场景 | `special_user_id` |

### 2. 环境切换

```bash
# 方式1: 命令行参数
pytest test_file.py --envId=sit

# 方式2: 修改pytest.ini
[pytest]
addopts = --envId=uat

# 方式3: CI/CD环境变量
export TEST_ENV=auto_qe
pytest test_file.py --envId=${TEST_ENV}
```

### 3. 数据维护

- ✅ 定期验证测试账号状态
- ✅ 统一管理环境配置
- ✅ 异常场景使用明显无效值
- ✅ 添加详细的数据说明注释

### 4. 代码规范

- ✅ 使用`.get()`方法获取数据,支持默认值
- ✅ 添加详细的测试场景描述
- ✅ 每个关键步骤添加日志
- ✅ **只验证code字段**,简化断言逻辑
- ✅ 记录完整响应数据供调试使用

---

## 🔧 故障排查与边界情况处理

### 问题1: Service层没有对应的接口方法

**现象**: 生成测试用例时提示`service/{service_name}/__init__.py`中没有对应的接口映射

**解决方案**:

#### 方案A: 自动生成(推荐)
Skill会自动生成Service层代码:
1. 在`service/{service_name}/model.py`中添加Model类
2. 在`service/{service_name}/__init__.py`的mapping中添加接口映射
3. 提示用户检查生成的代码是否符合接口规范

#### 方案B: 手动添加
按照Skill提示的格式,手动添加Service层代码后重新生成

**示例**: 参考skill文档中的"边界情况处理 > 情况1"

### 问题2: 测试数据(用户信息)项目中没有

**现象**: 生成测试用例时缺少测试账号数据(user_id, customer_no等)

**解决方案**:

#### 方案A: 使用占位符(推荐)
Skill会生成:
1. 带`TODO_REPLACE_*`占位符的YAML文件
2. 数据准备指南`docs/{interface_name}_data_preparation.md`

按照指南获取测试账号后,替换占位符即可

#### 方案B: 从现有数据复用
Skill会扫描现有YAML文件,提示用户选择是否复用

**示例**: 参考skill文档中的"边界情况处理 > 情况2"

### 问题3: 变量未替换

**现象**: 测试中user_id显示为`${user_id}`字符串

**原因**: 测试框架未正确解析环境变量

**解决**:
1. 检查pytest.ini中的`--envId`配置
2. 确认YAML格式正确(env部分结构)
3. 使用`.get()`方法获取数据

### 问题4: 测试数据不存在

**现象**: 提示customerNo对应的用户不存在

**原因**: 环境配置中的测试账号无效或使用了占位符

**解决**:
1. 检查`data/{service}/{interface}.yaml`中是否有`TODO_REPLACE`占位符
2. 如果有占位符,查看对应的数据准备指南
3. 在目标环境验证账号是否存在
4. 更新为有效的测试账号ID

### 问题5: 切换环境无效

**现象**: 修改--envId后仍使用旧环境数据

**原因**: 缓存或配置问题

**解决**:
1. 清除pytest缓存: `pytest --cache-clear`
2. 检查pytest.ini中的默认envId配置
3. 确认命令行参数优先级

---

## 📞 获取帮助

### 查看Skill详细说明

```bash
cat skill/api-test-generator.skill.md
```

### 查看示例测试指南

```bash
cat docs/za_zone_entry_page_test_guide.md
```

### 查看示例接口文档

```bash
cat skill/ZA_Zone.md
```

---

## 🔄 版本信息

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2026-02-25 | 初始版本,支持通用接口测试生成 |
| v1.1 | 2026-02-25 | 新增多环境YAML格式支持 |
| v1.2 | 2026-02-25 | 简化断言逻辑,只验证code字段 |
| v1.3 | 2026-02-25 | 新增边界情况处理(Service层缺失、测试数据缺失) |
| v1.4 | 2026-02-25 | **优化YAML生成策略**(1测试=1YAML,避免参数化) |

---

## 📚 相关文档

- [API Test Generator Skill](skill/api-test-generator.skill.md) - 完整的Skill使用说明
- [ZA Zone接口文档](skill/ZA_Zone.md) - 接口文档示例
- [测试指南示例](docs/za_zone_entry_page_test_guide.md) - 生成的测试指南示例

---

**生成工具**: API Test Generator Skill
**更新时间**: 2026-02-25
**文档版本**: v1.4
