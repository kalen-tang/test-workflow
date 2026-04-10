---
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Skill
description: 已优化测试脚本的增量更新专家。无需重新录制或重新生成，通过自然语言描述直接对testcase-optimized目录下的测试脚本、组件YAML和数据YAML进行精准的增量修改。
---

## Context
- 改动描述或目标文件: $ARGUMENTS

## Your task

{% if ARGUMENTS %}

激活 `qe-ui-update` SKILL，基于用户的改动描述对已有测试脚本进行增量更新。

### 执行流程

1. **解析改动需求**: 理解 `$ARGUMENTS` 描述的改动意图，识别改动类型和目标

2. **定位目标文件**:
   - 若 `$ARGUMENTS` 包含文件路径，直接读取该文件
   - 否则，根据上下文推断或询问用户

3. **读取相关文件**: 在修改前，必须完整读取：
   - 目标测试脚本 (`testcase-optimized/.../*.test.ts`)
   - 对应测试数据 (`data/.../*.yaml`)
   - 涉及的组件定义文件 (`component/.../*.yaml`)

4. **确认改动范围**: 展示计划改动列表，等待确认（若改动明确则直接执行）

5. **执行增量修改**: 按照 `qe-ui-update` SKILL 规范进行精准修改

6. **输出变更摘要**: 完成后展示清晰的变更内容

---

### 激活 SKILL 规范

```
Skill: qe-ui-update
```

按照 SKILL 中定义的规则执行：
- 命名规范：`{Module}-{FileName}-{componentName}`
- index 连续性保证
- 最小化改动原则
- 先读后改约束

{% else %}

请描述需要对已有测试脚本进行的改动。

## 使用示例

```bash
# 在登录后新增弹窗关闭步骤
/za-qe-ui:ui-update 在登录按钮点击后，新增关闭"我知道了"弹窗的步骤

# 指定文件并描述改动
/za-qe-ui:ui-update testcase-optimized/bib/withdrawal/cross-border-ecommerce-revolving.test.ts 新增填写备注字段

# 修改测试数据
/za-qe-ui:ui-update 将提款金额从 13000 改为 20000

# 新增断言
/za-qe-ui:ui-update 在提交按钮点击后，验证页面出现"申請成功"文字

# 更新组件选择器
/za-qe-ui:ui-update 登录按钮文字从"登入"改成了"登錄"，需要更新选择器

# 删除过时步骤
/za-qe-ui:ui-update 删除 Auth-otp-obsoletePopup 的点击步骤
```

## 适用场景

- 新增操作步骤（点击、输入、勾选）
- 修改步骤的目标组件或操作值
- 删除不再需要的步骤
- 更新组件的 Playwright 选择器
- 修改测试数据（账号、金额、URL等）
- 在流程中插入断言验证
- 处理新出现的弹窗或条件性UI元素

## 不适用场景

如需全新生成测试脚本，请使用：
```bash
/playwright-to-optimized testcase-native/your-test.test.ts
```

{% endif %}
