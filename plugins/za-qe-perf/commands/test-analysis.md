# za-qe-perf:test-analysis

基于代码变更生成测试要点报告，结果强制保存到文件。自动分析git diff或指定文件，生成完整的测试点分析报告。

## 使用方式

在Claude Code中直接调用：

```bash
# 分析git diff，保存到默认目录
/za-qe-perf:test-analysis

# 分析指定文件，保存到默认目录
/za-qe-perf:test-analysis src/main/java/group/za/bank/trade/controller/TradeController.java

# 保存到指定目录
/za-qe-perf:test-analysis -o ./reports src/main/java/group/za/bank/trade/
/za-qe-perf:test-analysis --output /tmp/test-points File1.java File2.java

# 分支对比，保存到默认目录
/za-qe-perf:test-analysis --branch main feature/order-refactor
/za-qe-perf:test-analysis -b main
```

## 功能说明

此命令将激活 `smart-interface-spec` 技能，提供以下测试分析功能：

### 自动代码变更分析
- 分析git diff的修改内容
- 支持指定文件或目录分析
- 支持分支对比分析（两个分支对比或当前工作区与分支对比）

### 全面测试点识别
- 识别新增、修改、删除的接口
- 分析Service层、DAO层、Feign调用等变更
- 识别事务、异常处理、配置等变更点

### 测试报告生成
- 生成接口级功能测试点
- 数据层测试点（数据库操作、事务、缓存）
- 异常与边界测试点
- 回归测试影响分析
- 配置与环境测试点

### 输出配置
- 结果强制保存到文件，窗口仅显示摘要
- 默认保存到 `./test-point-analysis-results` 目录
- 支持通过 `-o` 或 `--output` 指定输出目录
- 文件名含时间戳，避免覆盖历史报告

## 适用场景

- 代码提交前的测试覆盖检查
- 代码审查时的测试点补充
- 持续集成中的自动化测试生成
- 回归测试范围确定

## 关键词

test-point-analysis, code-change, testing-scenarios, regression-testing, git-diff, branch-comparison, test-coverage