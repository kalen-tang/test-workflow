---
name: qe-workflow
description: 执行测试左移工作流，从开发方案自动生成API自动化测试用例
arguments:
  - name: doc_path
    description: KM开发方案文档路径或URL
    required: true
---

# 测试左移工作流

自动执行测试左移流程，从 KM 开发方案直接生成 API 自动化测试用例，适合接口测试场景。

## 🎯 工作流概览

```
📄 KM 开发方案文档
        ↓
📊 devplan-analyzer (步骤1)
   - 提取接口信息
   - 生成单接口测试用例建议
   - 识别业务流程场景用例
        ↓
📋 测试左移分析报告
        ↓
🧪 api-generator (步骤2)
   - 生成 Python 测试代码
   - 生成多环境测试数据 (sit/auto_qe/uat)
   - 生成执行脚本
        ↓
🎯 API 自动化测试用例集
```

## 📝 使用方式

```bash
# 从本地文档生成
/za-qe:qe-workflow ./docs/za-zone-development.md

# 从网页URL生成（需要Playwright MCP）
/za-qe:qe-workflow https://km.yourcompany.com/doc/12345

# 等价于手动执行以下命令：
# /devplan-analyzer ./docs/za-zone-development.md
# /api-generator ./result/za_zone_测试左移分析报告.md
```

## 🔄 执行步骤

### 步骤 1: 测试左移分析

调用 `devplan-analyzer` 分析 KM 开发方案：

**输入**: KM 开发方案文档
**输出**: `./result/{项目名}_测试左移分析报告.md`

**分析内容**:
- 🔍 提取接口信息（路径、参数、响应）
- 📋 生成单接口测试用例（正常/异常/边界）
- 🔗 识别接口依赖关系
- 📊 生成业务流程场景用例
- ⚠️ 标注测试重点和风险点

**执行命令**: `/devplan-analyzer {doc_path}`

---

### 步骤 2: API 用例生成

自动检测分析报告路径并生成测试用例：

**自动检测逻辑**:
1. 优先查找: `./result/{项目名}_测试左移分析报告.md`
2. 备选查找: `./result/` 下最新的 `*测试左移分析报告.md`
3. 如未找到: 提示用户手动指定路径

**输出**:
- `./testcases/interface_case/test_{service}_{interface}.py` - 测试代码
- `./data/{service}/` - 测试数据（YAML格式）
- `./scripts/run_{module}_tests.sh` - 执行脚本

**执行命令**: `/api-generator {分析报告路径}`

---

## ✅ 执行成功输出

```
🚀 测试左移工作流执行完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 步骤1: 测试左移分析 ✅
   输入: ./docs/za-zone-development.md
   输出: ./result/za_zone_测试左移分析报告.md

   📋 分析结果:
   - 识别接口: 11个
   - 单接口用例: 33个 (正常11 + 异常11 + 边界11)
   - 场景用例: 5个业务流程
   - 优先级分布: P0(3) P1(5) P2(3)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 步骤2: API 用例生成 ✅
   输入: ./result/za_zone_测试左移分析报告.md

   📁 生成文件:
   • 测试代码: testcases/interface_case/test_za_zone_*.py (11个)
   • 测试数据: data/za_zone/*.yaml (33个)
   • 执行脚本: scripts/run_za_zone_tests.sh

   🌍 环境配置: sit, auto_qe, uat

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 下一步操作:

1. 查看分析报告:
   cat ./result/za_zone_测试左移分析报告.md

2. 执行测试用例:
   cd zabank_imc_case
   bash scripts/run_za_zone_tests.sh

3. 切换测试环境:
   pytest --envId sit   # SIT环境
   pytest --envId uat   # UAT环境

4. 查看测试报告:
   allure serve ./allure-report
```

## ⚠️ 错误处理

### 错误 1: 文档未找到

```
❌ 错误: 文档文件不存在
   路径: ./docs/za-zone-development.md

建议:
- 检查文件路径是否正确
- 确认文件是否存在
- 使用绝对路径或相对路径
```

**处理**: 停止执行，提示用户修正路径

---

### 错误 2: 分析报告生成失败

```
❌ 步骤1失败: 测试左移分析未完成

建议:
- 检查文档格式是否符合要求
- 确认文档包含接口信息
- 查看错误日志了解详情
```

**处理**: 停止执行，不进入步骤2

---

### 错误 3: 分析报告未找到

```
⚠️ 警告: 未找到测试左移分析报告

自动查找路径:
- ./result/{项目名}_测试左移分析报告.md ❌
- ./result/*测试左移分析报告.md ❌

建议:
- 手动指定报告路径: /api-generator <报告路径>
- 或重新执行步骤1: /devplan-analyzer ./docs/plan.md
```

**处理**: 提示用户手动执行步骤2

---

### 错误 4: 用例生成失败

```
❌ 步骤2失败: API 用例生成未完成

可能原因:
- 分析报告格式不符合要求
- 缺少必要的接口信息
- Service 映射未找到

建议:
- 检查分析报告内容
- 查看 api-generator 错误日志
- 参考 references/ 文档修正问题
```

**处理**: 工作流终止，保留步骤1的输出

---

## 💡 使用场景

### 场景 1: 新接口开发

```bash
# 开发团队提供 KM 文档后立即生成测试
/za-qe:qe-workflow ./docs/new-feature-plan.md
```

### 场景 2: 接口变更

```bash
# 接口修改后快速更新测试用例
/za-qe:qe-workflow ./docs/api-update-plan.md
```

### 场景 3: 快速验证

```bash
# 从线上 KM 系统直接生成测试
/za-qe:qe-workflow https://km.company.com/doc/feature-123
```

## 🎯 适用场景

✅ **适合**:
- 接口测试为主的项目
- 需要快速迭代的场景
- 开发文档相对完整
- 仅有 KM 开发方案

❌ **不适合**:
- 需要手工测试用例（使用 `/za-qe:qe-gencase`）
- 需要需求验证（先运行 `/doc-reviewer`）

## 📊 性能预估

| 接口数量 | 步骤1耗时 | 步骤2耗时 | 总耗时 |
|---------|---------|---------|--------|
| 5-10个  | 2-3分钟  | 3-5分钟  | 5-8分钟 |
| 10-20个 | 3-5分钟  | 5-8分钟  | 8-13分钟 |
| 20+个   | 5-8分钟  | 8-12分钟 | 13-20分钟 |

## 📚 相关命令

- `/za-qe:qe-gencase` - 生成场景测试案例（PlantUML流程图+MindMap）
- `/za-qe:qe-help` - 查看详细帮助
- `/devplan-analyzer` - 独立执行步骤1
- `/api-generator` - 独立执行步骤2

## 📖 详细文档

- [devplan-analyzer 文档](../skills/devplan-analyzer/SKILL.md)
- [api-generator 文档](../skills/api-generator/SKILL.md)
- [插件 README](../README.md)

---

**版本**: v1.4.0 | **状态**: ✅ 可用
