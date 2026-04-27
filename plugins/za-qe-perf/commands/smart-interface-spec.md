# smart-interface-spec

测试点分析 - 基于代码变更生成测试要点报告，结果强制保存到文件 $ARGUMENTS

## 使用方式

在Claude Code中直接调用：

```bash
# 分析git diff，保存到默认目录
/smart-interface-spec

# 分析指定文件，保存到默认目录
/smart-interface-spec src/main/java/group/za/bank/trade/controller/TradeController.java

# 保存到指定目录
/smart-interface-spec -o ./reports src/main/java/group/za/bank/trade/
/smart-interface-spec --output /tmp/test-points File1.java File2.java

# 分支对比，保存到默认目录
/smart-interface-spec --branch main feature/order-refactor
/smart-interface-spec -b main
```

## 适用场景

- 分析git diff或指定文件，生成完整的测试点分析报告
- 基于代码变更自动生成测试要点
- 强制保存测试报告到文件

## 关键词

test-point-analysis, code-change, testing-scenarios, regression-testing