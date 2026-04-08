---
name: qe-config
description: 配置 qe-toolkit 工具集的行为和参数
arguments:
  - name: setting
    description: 配置项名称（可选，不提供则显示当前配置）
    required: false
  - name: value
    description: 配置项的值（可选）
    required: false
---

管理 qe-toolkit 测试自动化工具集的配置项。

## 🔧 可配置项

### 1. 输出目录配置
```bash
/qe-config output_dir ./result
```
设置测试报告和用例的输出目录（默认：`./result/`）

### 2. 工作模式配置
```bash
/qe-config mode quick     # 快速模式
/qe-config mode full      # 完整模式
```

### 3. 代码生成配置
```bash
/qe-config code_style pep8          # 代码风格（pep8/google/numpy）
/qe-config max_line_length 180      # 最大行长度
```

### 4. 测试环境配置
```bash
/qe-config environments sit,auto_qe,uat   # 测试环境列表
```

### 5. 日志级别配置
```bash
/qe-config log_level info   # 日志级别（debug/info/warning/error）
```

## 📋 查看当前配置

不带参数执行命令，显示所有当前配置：

```bash
/qe-config
```

输出示例：
```
🔧 qe-toolkit 当前配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 输出目录: ./result/
⚡ 工作模式: quick (快速模式)
📝 代码风格: pep8
📏 最大行长度: 180
🌍 测试环境: sit, auto_qe, uat
📊 日志级别: info
```

## 💾 配置存储

配置项存储在：
- 项目级：`.claude/qe-toolkit.local.md` (YAML frontmatter)
- 全局级：`~/.claude/qe-toolkit.config.yaml`

项目级配置优先级高于全局配置。

## 🎯 使用示例

```bash
# 查看当前配置
/qe-config

# 设置输出目录
/qe-config output_dir ./test-output

# 切换到快速模式
/qe-config mode quick

# 设置多个测试环境
/qe-config environments sit,uat,prod
```
