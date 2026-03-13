---
name: api-case-generator
description: 此技能应在用户询问"生成API测试用例"、"生成接口测试代码"、"根据接口文档生成自动化测试"、"生成API自动化测试"、"创建接口测试用例"或"为API端点生成测试数据"时使用。适用于ZA Bank测试框架中的所有微服务接口测试生成。
---

# ZA Bank API测试用例生成器

## 技能用途

从接口文档生成完整的API自动化测试套件,支持ZA Bank所有微服务,包含标准化测试代码、多环境测试数据(sit/auto_qe/uat)和执行脚本。适用于**快速模式**(直接从KM文档)和**完整模式第四阶段**(从手工测试用例)两种测试左移工作流。

## 核心特性

- ✅ **服务无关**: 支持所有微服务(zabank-imc-activity、zabank-imc-cubercore、zabank-act-core等)
- ✅ **格式统一**: 基于标准化接口文档生成测试
- ✅ **智能适配**: 自动检测服务类型,选择正确的service/scenario层
- ✅ **完整生成**: 一次性生成测试代码+测试数据+执行脚本
- ✅ **多环境支持**: 支持sit/auto_qe/uat配置,变量自动替换

## 使用场景

在用户需要以下操作时应用此技能:

1. 为任何微服务API端点生成自动化测试
2. 快速从接口文档创建测试套件
3. 生成标准化的多环境测试数据文件
4. 验证和测试特定API端点

**输入来源**:
- 快速模式: KM开发方案 → shift-left-analyzer报告 → 本技能
- 完整模式: 手工测试用例 + 规范化产出物 → 本技能

## 输入格式要求

### 标准接口文档格式

期望包含以下结构的Markdown文件:

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
"请根据skill/ZA_Zone.md生成接口自动化测试"

# 方式2: 为指定服务生成
"为reward服务的积分兑换接口生成测试用例"

# 方式3: 快速测试端点
"测试activity服务的entryPage接口"

# 方式4: 仅生成测试数据
"为cubercore服务的配置查询接口生成测试数据"
```

## 实施工作流

### 步骤1: 分析输入并识别服务

当用户提供文档或接口信息时:

1. **解析文档**
   - 提取所有接口信息(路径、方法、参数、响应)
   - 提取所有测试用例场景
   - 识别优先级(P0/P1/P2)

2. **识别目标服务**
   - 从API路径前缀自动检测服务类型
   - 定位对应的service目录
   - 查找匹配的scenario类

**服务识别规则**:
```python
# 路径前缀 → 服务映射
"/activity/*" → zabank_imc_activity_service
"/rc/*" → zabank_rcs_core (RCS权益服务)
"/cuber/*" → zabank_imc_cubercore_service
"/reward/*" → zabank_imc_reward_service
"/act/*" → zabank_act_core_service
"/batch/*" → zabank_bms_batch_service
```

完整服务列表参见 `references/service-mapping.md`。

### 步骤2: 获取服务信息

基于识别的服务,自动获取:

1. **Service层信息**
   - 读取 `service/{service_name}/__init__.py` 获取接口映射
   - 解析mapping字典获取可用方法和Model类
   - ⚠️ 如Service层缺失: 自动创建或提示用户(参见 `references/edge-cases.md`)

2. **Scenario层信息**
   - 根据服务映射定位scenario文件
   - 示例: `zabank_imc_activity_service` → `scenario/imc/activity_scenario.py`

3. **配置信息**
   - 从 `config/{env}.yaml` 获取服务host配置

### 步骤3: 确保Scenario Fixture

**关键**: 必须在 `conftest.py` 中添加对应的scenario fixture,否则测试会失败!

```python
# conftest.py
from scenario.imc.activity_scenario import ActivityScenario

@pytest.fixture(scope="session")
def activity_sc(config):
    return ActivityScenario(config)
```

**Fixture命名规则**: `{service_domain}_sc`
- zabank_imc_activity_service → activity_sc
- zabank_imc_cubercore_service → cuber_core_sc
- zabank_imc_reward_service → reward_sc

### 步骤4: 生成测试代码

**关键原则**:
- ✅ **1个测试方法 = 1个YAML文件** (避免参数化问题)
- ✅ **使用 `data[0]` 获取测试数据** (tests列表的第一个case)
- ✅ **不在测试文件中定义fixture** (统一在conftest.py管理)

**测试代码模板结构**:

完整模板参见 `references/test-code-template.md`。

**Model类实例化** (关键规范):

```python
# ✅ 正确: 使用静态导入via model模块
from service.zabank_imc_activity_service import model
params = model.ActivityZaZoneGetVerifyCode()

# ❌ 错误: 通过method_to_model动态查找
params = activity_sc.controller.method_to_model("activity_za_zone_get_verify_code")()
```

详细原理参见 `references/model-instantiation.md`。

### 步骤5: 生成测试数据YAML

**核心原则**:
- ✅ **1个测试方法 = 1个YAML文件 = 1个case** (避免参数化)
- ✅ **文件命名**: `{interface_name}_{scene_number}_{scene_name}.yaml`
- ✅ **必须使用tests列表格式** (框架要求)

**YAML结构**:

```yaml
# data/{service_module}/{interface_name}_{scene_number}_{scene_name}.yaml

# ===== 环境配置 (可选,正常/边界场景需要) =====
env:
  sit:
    user_id: "{sit_user_id}"
    customer_no: "{sit_customer_no}"
  auto_qe:
    user_id: "{autoqe_user_id}"
    customer_no: "{autoqe_customer_no}"
  uat:
    user_id: "{uat_user_id}"
    customer_no: "{uat_customer_no}"

# ===== 测试用例 (必须,且只包含1个case) =====
tests:
  - case: {场景描述}
    data:
      - step: {步骤名称}
        input:
          user_id: ${user_id}         # 引用环境变量
          customer_no: ${customer_no}
          {param1}: "{value1}"
        expected:
          expected_code: "{期望响应码}"
```

**关键点**:
- ✅ 正常/边界场景: 包含 `env` 配置,多环境数据
- ✅ 异常场景: 使用固定无效值,不需要 `env`
- ✅ 使用 `${变量}` 语法引用环境变量
- ✅ 测试代码使用 `data[0]` 获取唯一case

详细示例参见 `references/yaml-format.md`。

### 步骤6: 生成执行脚本

生成便捷的按优先级执行的测试脚本:

```bash
#!/bin/bash
# run_{service_name}_{interface_name}.sh

echo "开始 {Interface Name} API测试..."

# P0级别测试 (核心业务流程)
pytest testcases/interface_case/test_{service_name}_{interface_name}.py -m P0 -v

# P1级别测试 (重要功能)
pytest testcases/interface_case/test_{service_name}_{interface_name}.py -m P1 -v

# P2级别测试 (辅助功能)
pytest testcases/interface_case/test_{service_name}_{interface_name}.py -m P2 -v

# 生成Allure报告
allure generate ./allure-results -o ./allure-report --clean

echo "测试执行完成!"
```

## 智能特性

### 1. Controller方法名推断

从API路径自动生成controller方法名:

```python
# /dmb/nok9iy/activity/zazone/getVerifyCode
# → activity_za_zone_get_verify_code
```

### 2. Model类名推断

将snake_case方法名转换为PascalCase类名:

```python
# activity_za_zone_get_verify_code → ActivityZaZoneGetVerifyCode
# 转换: 按下划线分割 → 每个单词首字母大写 → 拼接
```

### 3. 智能测试数据生成

根据参数类型和场景生成多环境测试数据:

- **正常/边界**: 使用环境变量 (`${user_id}`, `${customer_no}`)
- **异常**: 使用固定无效值 (`"INVALID_CUSTOMER_9999999"`)
- **特殊字段**: 自动检测email、mobile、userId、customerNo模式

### 4. 断言自动生成

**重要**: 为简洁高效,仅验证 `code` 字段:

```python
expected_code = step.get("expected_code", "000000")
Assertion.str_assert(resp.json()["code"], expected_code)
logging.info(f"响应码验证通过: {resp.json()['code']}")
```

**设计原则**: 专注响应码验证,除非明确要求,否则避免复杂的业务字段断言。

## 文件组织

```
zabank_imc_case/
├── testcases/
│   └── interface_case/
│       └── test_{service}_{interface}.py
├── data/
│   └── {service_module}/
│       └── {interface}_{scene_number}_{scene_name}.yaml
├── scenario/
│   └── imc/
│       ├── activity_scenario.py
│       └── reward_scenario.py
├── service/
│   ├── zabank_imc_activity_service/
│   └── zabank_imc_reward_service/
├── scripts/
│   └── run_{module}_tests.sh
└── conftest.py
```

## 常见错误处理

### 1. 服务未找到

```
❌ 错误: 未找到服务 'zabank_xxx_service'

建议:
- 检查service/目录下是否存在该服务
- 确认接口路径是否正确
- 可用服务列表: [列出所有服务]
```

### 2. Scenario类缺失

```
⚠️  警告: 未找到对应的Scenario类

建议:
- 直接使用Controller层调用(无scenario封装)
- 或在 scenario/{module}/{service}_scenario.py 创建Scenario类
```

### 3. 接口映射缺失

参见 `references/edge-cases.md` 的自动生成解决方案。

### 4. 测试数据缺失

参见 `references/edge-cases.md` 的占位符和数据准备策略。

## 最佳实践

1. **文档先行**: 确保接口文档完整准确
2. **增量生成**: 先生成一个接口测试验证,再批量生成
3. **及时Review**: 生成后检查代码并进行必要调整
4. **持续维护**: 接口变更时同步更新测试代码
5. **多环境数据管理**:
   - 为每个环境(sit/auto_qe/uat)配置独立测试账号
   - 使用 `${变量}` 语法引用环境配置
   - 正常/边界场景使用环境变量,异常场景使用固定无效值
   - 定期更新各环境的测试数据
6. **环境切换**:
   - 使用 `--envId` 参数切换测试环境
   - 在pytest.ini中配置默认环境
   - CI/CD中使用参数化环境配置

## 工作流示例

### 示例1: 生成ZA Zone接口测试

**输入**: "请根据skill/ZA_Zone.md生成接口自动化测试"

**执行步骤**:
1. 读取 `skill/ZA_Zone.md`
2. 识别11个接口,属于 `zabank_imc_activity_service`
3. 扫描 `service/zabank_imc_activity_service/__init__.py` 获取接口映射
4. 为每个接口生成:
   - `testcases/interface_case/test_za_zone_{interface}.py`
   - `data/za_zone/{interface}_{scene_number}_{scene_name}.yaml`
5. 生成执行脚本 `scripts/run_za_zone_tests.sh`

### 示例2: 为其他服务生成测试

**输入**: "请根据skill/Reward_System.md为reward服务生成接口测试"

**执行步骤**:
1. 读取 `skill/Reward_System.md`
2. 识别接口属于 `zabank_imc_reward_service`
3. 定位 `scenario/imc/reward_scenario.py`
4. 扫描 `service/zabank_imc_reward_service/__init__.py`
5. 生成对应的测试代码和数据
6. 适配RewardScenario和reward service特定配置

### 示例3: 快速测试单个接口

**输入**: "快速测试activity服务的homepage接口,使用customerNo=8000782594"

**执行步骤**:
1. 识别服务: `zabank_imc_activity_service`
2. 识别接口: `activity_za_zone_homepage`
3. 构造测试请求
4. 执行并展示结果
5. 提供进一步测试建议

## 附加资源

### 参考文件

详细实施指导:
- **`references/service-mapping.md`** - 完整服务映射表和自动扩展策略
- **`references/test-code-template.md`** - 完整测试代码模板,包含所有章节和动态参数填充
- **`references/yaml-format.md`** - YAML文件格式详情、多环境示例和最佳实践
- **`references/model-instantiation.md`** - Model类实例化规则、命名转换算法和原理
- **`references/edge-cases.md`** - 边界情况处理(Service层缺失、测试数据缺失)
- **`references/advanced-features.md`** - 批量生成、增量更新、覆盖率分析

### 示例文件

`examples/` 中的工作示例:
- **`example-test-code.py`** - 完整测试类示例,包含多场景测试
- **`example-yaml-normal.yaml`** - 正常场景YAML,带env配置
- **`example-yaml-exception.yaml`** - 异常场景YAML,使用固定无效值

### 实用脚本

`scripts/` 中的可用工具(如需要):
- 生成测试代码的验证脚本
- YAML格式检查器
- 服务映射发现工具

## 版本历史

- **v1.0** (2026-02-25): 初始版本,支持通用接口测试生成
- **v1.1** (2026-02-25): 新增多环境YAML格式支持(sit/auto_qe/uat)
- **v1.2** (2026-02-25): 简化断言逻辑,仅验证code字段
- **v1.3** (2026-02-25): 新增边界情况处理(Service层缺失、测试数据缺失)
- **v1.4** (2026-02-25): 优化YAML生成策略(1方法=1文件,使用data[0])
- **v1.5** (2026-03-11): 修正Model类实例化(使用静态导入,非动态查找)
- **v1.6** (2026-03-13): **[重大重构]** 应用渐进式披露设计
  - ✅ 压缩SKILL.md至~2000词(仅核心工作流)
  - ✅ 将详细内容移至references/(6个参考文件)
  - ✅ 添加工作示例至examples/
  - ✅ 修正description为第三人称格式
  - ✅ 转换为命令式写作风格
  - ✅ 对齐README架构(快速模式+完整模式第四阶段)

---

**注意**: 这是一个通用技能,适用于所有符合ZA Bank测试框架标准的微服务。
