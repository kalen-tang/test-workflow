# 分析报告与测试策略输出模板

## 文件 1：代码变更分析报告模板

文件名：`<需求ID>_代码变更分析.md`

---

```markdown
# <需求ID> 代码变更分析报告

## 1. 需求概览

| 字段 | 内容 |
|------|------|
| 需求编号 | BANK-XXXXX |
| 需求标题 | <summary> |
| 需求类型 | Story / Bug / 优化 |
| 版本 | <fixVersion> |
| 分析时间 | YYYY-MM-DD HH:mm |
| 涉及服务数 | N 个 |

> ⚠️ **优化需求标记**：本次变更为优化需求，已开启"优化影响分析"模块。
（仅在判断为优化需求时显示此提示）

---

## 2. 变更概览

| 服务名称 | 分支 | 新增行数 | 删除行数 | 变更文件数 | 风险等级 |
|----------|------|---------|---------|-----------|---------|
| activity-service | feature/BANK-89156-xxx | +120 | -30 | 8 | P0 |
| push-service | feature/BANK-89156-xxx | +45 | -10 | 3 | P1 |

---

## 3. 各服务变更详情

### 3.1 <service-name>

**分支**：`feature/BANK-89156-xxx`
**最后提交**：`abc123d` - feat: add game activity logic（2024-04-10）

#### 变更文件清单

| 状态 | 文件路径 | 变更类型 | 风险等级 |
|------|---------|---------|---------|
| M | src/main/java/.../ActivityController.java | 接口层 | P1 |
| M | src/main/java/.../ActivityService.java | 业务逻辑 | P0 |
| A | src/main/resources/db/migration/V1.2.3__add_activity_table.sql | DB变更 | P0 |
| M | src/main/resources/application.yml | 配置变更 | P1 |

> 状态说明：A=新增，M=修改，D=删除，R=重命名

#### 关键变更说明

**[P0] 数据库变更 - V1.2.3__add_activity_table.sql**
```sql
-- 新增活动参与记录表
CREATE TABLE activity_record (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  activity_id VARCHAR(64) NOT NULL,
  score INT DEFAULT 0,
  created_at DATETIME NOT NULL
);
```
- 风险：新增表，需确认索引是否满足查询需求
- 注意：`user_id` 无索引，活动结束后查询用户记录可能慢查询

**[P0] 业务逻辑变更 - ActivityService.java**
- `calculateScore()` 方法修改了积分计算规则：由"每题+10分"改为"按时间衰减计算"
- 影响：存量进行中的活动用户得分计算方式变更

**[P1] 接口变更 - ActivityController.java**
- 新增接口：`POST /activity/submit` - 提交活动答案
- 修改接口：`GET /activity/result` 响应新增字段 `timeBonus`（时间奖励积分）

---

## 4. 业务流程 & 数据库信息

> 本节从代码变更中还原核心业务流程，并梳理各流程涉及的数据库操作，供测试用例设计和风险评估参考。

### 4.1 <流程名称>（如：审批流程）

**流程描述**：

1. 入口：`POST /xxx/approval`（Controller）
2. 状态校验：approvalStatus != 2 才允许审批
3. 更新审批状态：UPDATE t_xxx SET approval_status = 2
4. 触发后续逻辑：同步下载文件 → EasyExcel 解析 → 逐行上报 Kafka

**数据库操作**：

| 表名 | 操作 | 关键字段 / 条件 | 索引 | 备注 |
|------|------|--------------|------|------|
| t_dc_report_manage | SELECT | WHERE task_id = ? AND is_deleted = 'N' | uk_task_id | 唯一索引，快速定位 |
| t_dc_report_manage | UPDATE | SET approval_status = 2 WHERE id = ? | PRIMARY KEY | 审批通过 |
| t_dc_report_manage | UPDATE | SET status = 3 WHERE id = ? | PRIMARY KEY | 执行失败时更新 |
| t_statistics_user | SELECT | WHERE ma_game_id = ? | 无索引（⚠️） | 每行 Excel 都触发一次全表扫描 |

### 4.2 <流程名称>（如：开户 MA 游戏 ID 生成流程）

**流程描述**：

1. 入口：MQ 消费 `OpenAccountListener`（开户成功事件）
2. 开关判断：`mbs.statis.hkma.gameid.generate.switch=true` 才执行
3. 生成 ID：随机 9 位数字（387 前缀），DB 查重，冲突则重试
4. 写入：UPDATE t_statistics_user SET ma_game_id = ? WHERE user_id = ?

**数据库操作**：

| 表名 | 操作 | 关键字段 / 条件 | 索引 | 备注 |
|------|------|--------------|------|------|
| t_statistics_user | SELECT | WHERE ma_game_id = ? | 无索引（⚠️） | 唯一性查重，高并发下性能风险 |
| t_statistics_user | UPDATE | SET ma_game_id = ? WHERE user_id = ? | uk_user_id | 写入生成的 ID |

**SQL 变更（DDL）**：

| 变更 | SQL | 风险 |
|------|-----|------|
| user_id 改 NOT NULL | `ALTER TABLE t_statistics_user MODIFY COLUMN user_id bigint(20) NOT NULL` | 存量 NULL 数据会导致执行失败 |
| 新增 ma_game_id 字段 | `ALTER TABLE t_statistics_user ADD COLUMN ma_game_id varchar(16)` | 无唯一索引，通过 maGameId 查询会全表扫描 |
| 新建 t_dc_report_manage | `CREATE TABLE t_dc_report_manage (...)` | 设计合理，含 uk_task_id 唯一索引 |

---

## 5. 质量风险汇总

### P0 高风险

| 风险编号 | 服务 | 风险描述 | 受影响场景 |
|---------|------|---------|-----------|
| R001 | activity-service | 新建 activity_record 表缺少 user_id 索引，大数据量下查询超时 | 活动结束后查看个人得分 |
| R002 | activity-service | 积分计算规则变更，进行中的活动用户预期收益可能与实际不符 | 活动过程中的积分展示 |

### P1 中风险

| 风险编号 | 服务 | 风险描述 | 受影响场景 |
|---------|------|---------|-----------|
| R003 | activity-service | 新增响应字段 `timeBonus` 未做 null 处理，旧版客户端可能解析异常 | 客户端展示活动结果 |
| R004 | push-service | 活动结果推送 TTL 配置由 60s 改为 30s，网络差环境可能丢失通知 | 弱网环境下的推送触达率 |

### P2 低风险

| 风险编号 | 服务 | 风险描述 |
|---------|------|---------|
| R005 | activity-service | 日志新增用户设备信息，注意脱敏（已检查无敏感字段） |

---

## 6. 优化影响分析（仅优化需求显示）

### 6.1 性能预期影响

| 场景 | 优化前 | 优化后（预期） | 验证方式 |
|------|-------|---------------|---------|
| 活动列表查询（100并发） | P99 > 2000ms | P99 < 500ms | 压测 |
| 积分计算接口 | CPU 峰值 80% | CPU 峰值 < 40% | 压测 + 监控 |

### 6.2 兼容性风险

- 计算公式变更影响**已进行中的活动**：建议发布时间选在活动间歇期
- `timeBonus` 字段客户端需适配：确认 iOS/Android 均已更新解析逻辑

### 6.3 回归风险

- 重构范围：`ActivityService`（核心业务逻辑）
- 建议：执行完整回归测试，包含历史活动场景

---

*报告生成时间：YYYY-MM-DD HH:mm | za-qe code-diff-analysis*
```

---

## 文件 2：测试策略模板

文件名：`<需求ID>_测试策略.md`

---

```markdown
# <需求ID> 测试策略

## 1. 测试范围与目标

**需求**：<需求标题>
**测试目标**：验证本次变更的功能正确性，确保无回归，覆盖所有识别的质量风险点。

**测试范围**：
- activity-service：活动参与、积分计算、结果查询
- push-service：活动结果推送

**不在范围**：
- 未变更服务的全量回归（仅执行冒烟）
- 性能压测（另行计划）

---

## 2. P0 必测用例

> 以下用例**必须全部通过**，否则阻塞发布。

### 用例组 1：数据库变更验证（R001）

| 编号 | 场景 | 前置条件 | 操作 | 预期结果 |
|------|------|---------|------|---------|
| TC001 | 新表写入正常 | 数据库已执行迁移脚本 | 提交活动答案 | activity_record 表新增一条记录 |
| TC002 | 查询活动记录 | activity_record 有 1000+ 条用户数据 | 调用 GET /activity/result | 响应时间 < 1s |
| TC003 | 迁移脚本幂等 | 已执行过迁移脚本 | 再次执行迁移脚本 | 无报错，数据无重复 |

### 用例组 2：积分计算变更（R002）

| 编号 | 场景 | 前置条件 | 操作 | 预期结果 |
|------|------|---------|------|---------|
| TC004 | 快速答题时间奖励 | 用户在 10s 内答题 | 提交答案 | timeBonus > 0，总分 = 基础分 + timeBonus |
| TC005 | 超时答题无奖励 | 用户在 60s 后答题 | 提交答案 | timeBonus = 0，总分 = 基础分 |
| TC006 | 答错无积分 | 答错题目 | 提交错误答案 | 积分不变，timeBonus = 0 |
| TC007 | 积分上限校验 | 用户积分接近上限 | 答对所有题目 | 积分不超过系统上限（如 9999） |

---

## 3. P1 建议用例

> 以下用例建议在发布前覆盖，存在风险但非阻塞。

### 用例组 3：新字段兼容性（R003）

| 编号 | 场景 | 操作 | 预期结果 |
|------|------|------|---------|
| TC008 | 旧版客户端请求活动结果 | 使用未升级的 App 版本调用 GET /activity/result | 忽略未知字段 timeBonus，正常展示结果 |
| TC009 | timeBonus 为 null 时处理 | 查询未设置时间奖励的活动结果 | 响应中 timeBonus 为 0 或不返回该字段 |

### 用例组 4：推送 TTL 验证（R004）

| 编号 | 场景 | 操作 | 预期结果 |
|------|------|------|---------|
| TC010 | 正常网络下推送触达 | 提交活动答案后等待推送 | 30s 内收到推送通知 |
| TC011 | 推送失败重试 | Mock push-service 异常 | 3 次重试后记录推送失败日志 |

---

## 4. P2 可选用例

| 编号 | 场景 | 说明 |
|------|------|------|
| TC012 | 日志脱敏检查 | 检查新增日志不含敏感信息（身份证、手机号） |
| TC013 | 活动入口曝光埋点 | 验证新增埋点数据上报正确 |

---

## 5. 回归测试建议

以下已有功能需执行回归：

| 功能 | 回归方式 | 说明 |
|------|---------|------|
| 活动列表展示 | 自动化冒烟 | 确认现有活动不受影响 |
| 历史活动积分查询 | 手动验证 | 确认历史数据展示正常 |
| 用户推送偏好设置 | 自动化冒烟 | push-service 变更影响范围 |

---

## 6. 测试数据准备

| 数据项 | 说明 | 准备方式 |
|--------|------|---------|
| 测试活动 ID | 需在 SIT 创建测试活动 | 调用活动创建接口或直接插库 |
| 参与活动的用户 | 至少 3 类：新用户、老用户、积分上限用户 | 测试账号管理系统 |
| 1000+ 条活动记录 | 验证查询性能 | 执行数据初始化脚本 |

---

## 7. 测试环境依赖

| 依赖项 | 状态 | 负责人 |
|--------|------|-------|
| SIT 数据库迁移脚本执行 | 待确认 | DBA |
| push-service SIT 部署 | 待部署 | 开发 |
| iOS/Android 新版本打包 | 待确认 | 客户端开发 |

---

*测试策略生成时间：YYYY-MM-DD HH:mm | za-qe code-diff-analysis*
```
