**企业福利（ZA Zone）设计方案**

|  |  |
| --- | --- |
| 需求id | [BANK-77222](https://jira.in.za/browse/BANK-77222?src=confmacro) - |
| 需求概要 | PRD:[ZA Zone 产品需求文档 0630.docx| [https://zagroup-my.sharepoint.com/:w:/g/personal/xing\_fan\_za\_group/EaX8kkEXZPNLh\_WG8G1JSOMBpk8HIF4pgXNSTaSoowSpMQ?e=0EuoYj](https://zagroup-my.sharepoint.com/%3Aw%3A/g/personal/xing_fan_za_group/EaX8kkEXZPNLh_WG8G1JSOMBpk8HIF4pgXNSTaSoowSpMQ?e=0EuoYj) ] |
| UE | [企业员工福利 – Figma|  <https://www.figma.com/embed?embed_host=confluence&url=https%3A%2F%2Fwww.figma.com%2Fdesign%2FuLG2zhzeec3XH1miHnThHJ%2F%E4%BC%81%E4%B8%9A%E5%91%98%E5%B7%A5%E7%A6%8F%E5%88%A9%3Fnode-id%3D0-1%26p%3Df%26t%3DHIQNpUbuXf9okpzq-0>  ] |
| 文档编写时间 | 2025/07/29 |
| 文档撰写人 |  |
| 设计概要复核人 |  |
| 设计概要复核时间 |  |
| 需求进度 | 概要设计-概要评审-编码阶段-代码评审-测试阶段-发布阶段-生产验证阶段-已投产 |

**【目录】**

**1.需求背景描述**

**1.1背景**

针对etb用户，可通过"组队解锁"机制，让用户通过邀请同事动态升级专属权益，提升企业/校园用户规模

**1.2功能简介&业务效果**

企业福利的权益：根据团体参与人数解锁不同档位福利
Lv.1 星云：20人认证，每月高达1000港币奖赏
Lv.2 星球：100人认证，每月高达2000港币奖赏
未来可扩展更多等级（Lv.3星座，Lv.4）

预计发放的权益：

* **存款** ：1%至1.5%活期年利率
* **基金** ：0认购费
* **股票** ：低至0美元交易费
* **ZA Card** ：回赠券
* **货币兑换** ：差价外汇优惠（2张/5张）
* **海外汇款** ：免便利费
* **ZA Insure** ：首年保费5-6折（仅HKID客户可见）

参与方式：通过企业/校园邮箱验证（OTP）即可完成登记

**1.3 分工**

主活动：兆增，退团&activity 本辉；

组团：展亮；

会员权益：杨威；

**2.整体设计概要**

**2.1 活动主会场**

**a. 数据模型**

|  |
| --- |
| Java 活动配置 projectId ：“zoneProjectId” mainActivityId：“zoneMainActivityId” subActivityId：“zoneSubActivityId”  新增节点： {  "projectId": "zoneProjectId",  "nodeTemplateName": "企业福利ZaZone",  "subActivityId": "zoneSubActivityId",  "nodeStructureType": 1,  "nodeBizType": 1,  "nodePageType": 2,  "nodeDesc": "企业福利ZaZone",  "pageConfig": "{\"component\":\"ZoneWelfare\"}",  "childNode": null }  eg: {  "zoneConfig": {  "levelsConfig": [{  "level": 1, --等级  "peopleNum": 20 --人数,禁用不允许编辑  ? ? ? ... --对应奖赏信息  }]  }, "teamUpConfig":{"teamUpLimit":"人数限制，不限人数 -1"} }  CREATE TABLE `user\_verify\_mgm` (  `id` bigint(20) NOT NULL AUTO\_INCREMENT COMMENT '业务主键',  `cuberAlias` varchar(64) NOT NULL COMMENT '主活动ID',  `user\_id` bigint(20) NOT NULL COMMENT '用户ID',  `join\_time` datetime NOT NULL COMMENT '参与时间',  `redeem\_code` varchar(20) NOT NULL COMMENT '邀请码',  `inviter\_user\_id` bigint(20) NOT NULL COMMENT '邀请人用户ID',   `email` varchar(64) NOT NULL COMMENT '团队标识',   `team\_tag` varchar(64) NOT NULL COMMENT '团队标识',  `is\_deleted` char(1) NULL DEFAULT 'N' COMMENT '是否删除 N-否 Y-是',  `create\_time` datetime NULL DEFAULT CURRENT\_TIMESTAMP COMMENT '创建时间',  `creator` varchar(64) NULL DEFAULT 'system' COMMENT '创建人',  `modify\_time` datetime NULL DEFAULT CURRENT\_TIMESTAMP ON UPDATE CURRENT\_TIMESTAMP COMMENT '更新时间',  `modifier` varchar(64) NULL DEFAULT 'system' COMMENT '更新人',  PRIMARY KEY (`id`),  KEY `idx\_inviter\_user\_id` (`inviter\_user\_id`) ) COMMENT='用户邀请关系表'; |

b.涉及接口

参与模块

![](data:image/png;base64...)

团解散任务：

1.通知组团组件

2.通知会员权益模块

|  |  |  |  |
| --- | --- | --- | --- |
| 接口说明 | 接口 路径 | 请求参数 | 响应 |
| 获取验证码  1.增加员工福利校验 | /dmb/nok9iy/activity/zazone/getVerifyCode | {  "revIdType ": "EMAIL", ##邮箱=EMAIL "revId ": "xxx@xxx", ##邮箱  "redeemCode ": "xxxx" ##邀请码 } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS", "value": {  " tokenId ": "XXX"  }, "messageItems": null, "msg": "SUCCESS", "serverTime": "2025-07-29 18:32:05", "sysTransTime": "183205", "success": true } |
| 企业认证接口  1.参与成功且当前团队组团中，当前用户发activity  2.参与成功且当前团队已成团1、2、3，由rcs企业会员模块触发activity发放流程（权益发放后，针对所有团员发act）  3.用户获得试用权益时发通知：push/email/activity  4.新增用户参与记录user\_verify\_mgm，后续增加校验专属邀请码只能使用一次 | /dmb/npo9iy/activity/zazone/verify | { "customerNo": "XXX", " tokenId ": "XXX",  "revIdType ": "EMAIL",? ##邮箱=EMAIL "revId ": "xxx@xxx",? ?##邮箱 "verifyCode": "XXX", ##验证码  "redeemCode ": "xxx"? ?##邀请码 } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS",  "value": {  ?"revId ": "xxx@xxx",? ?##邮箱  "currentLevel": 1, ## 未成团=0  "currentTeamCount": 50, #已成团人数  "levelChange": true, #等级是否变化  "advCodeUseSuccessFlag": true, #专属邀请码是否核销成功:true是 false否  "levelsConfig": [{  "level": 1,  "peopleNum": 20,  ?...  }]  },  "messageItems": null, "msg": "SUCCESS", "serverTime": "2025-07-29 18:32:05", "sysTransTime": "183205", "success": true } |
| 活动状态接口 | /dmb/nqe3iy/activity/zazone/entryPage | { "customerNo": "XXX" } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS",  "value": {  "employeeFlag": false, ?##是否员工: true=是, false=否  "employeeRelativesFlag": true,? ?##是否亲友: true=是, false=否  "joinFlag": true, ## true=参与 false=未参与  "currentLevel": 1, ## 未成团=0  "currentTeamCount": 50, #已成团人数  "rewardNum": 7, #当前等级奖励数量  "levelsConfig": [{  "level": 1,  "peopleNum": 20  }]  },  "messageItems": null, "msg": "SUCCESS", "serverTime": "2025-07-29 18:32:05", "sysTransTime": "183205", "success": true } |
| 活动首页接口 | /dmb/nwe5iy/activity/zazone/homePage  响应体中权益类型的映射关系  懒人钱罐权益：interestType=27,subInterestType=1  股票佣金权益：interestType=28,subInterestType=1  优惠券-咖啡消费回赠：interestType=16,subInterestType=65  优惠券-保险折扣：interestType=16,subInterestType=32  优惠券-海外汇款返现：interestType=16,subInterestType=54  优惠券-货币兑换立减：interestType=16,subInterestType=76 | {  "customerNo": "XXX" } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS",  "value": {  ~~"employeeFlag": false, ?##是否员工: true=是, false=否~~  ~~"employeeRelativesFlag": true,? ?##是否亲友: true=是, false=否~~  "joinFlag": true, ## true=参与 false=未参与  "redeemCode": “xxx”, ## 邀请码  ~~" advCodeUseSuccessFlag ": true, #专属邀请码是否核销成功:true是 false否~~  " advCodeExpireTime ": 123L, #专属邀请码对应权益过期时间  " advRightExpireFlag ": false, #专属邀请码对应权益是否过期:true是 false否  "nickName": "昵称",  "inviteSuccessCount": 4, ## 邀请成功人数  ?"teamTag ": "@xxx",? ?##团队标识  "currentLevel": 1, ## 0=未成团  ?"preLevel": 1, ## 前一个月等级（null表示上月未参与，0表示上月未成团）  "currentTeamCount": 50, #已成团人数  "levelsConfig": [{  "level": 1,  "peopleNum": 20,  "rewards": [{  //权益类型 private String interestType; //子权益类型 private String subInterestType; //权益号，全局唯一 private String interestNo; //券号，全局唯一，权益券有值 private String couponNo; //权益产品名 private String interestName; //权益产品描述，支持国际化 private String interestDesc; /跳转链接 private String interestJumpUrl;  //权益发放状态 PENDING("0", "处理中，待发放") OPERATIONAL("1", "正常发放,已可使用") private String interestSendState;  //券的状态0-待生效 1-正常 2-锁定 3-已核销 4-过期 private String couponState; //图标 private String interestIconUrl; //标签:zone\_consume=消费,zone\_invest=投资,zone\_deposit=存款,zone\_other=其他 private String interestTag;  ?}]  ?...  }]  }, "success": true }  枚举详见： [卡券模板元数据字段梳理](https://zaglobal.feishu.cn/wiki/N534w3vCTijCJTksxkoc4KhInWh) |
| 推荐记录接口 | /dmb/ngui7y/activity/zazone/queryInviteRecord | {  "startKey": " 分页查询 Key, 首次查询不需送 , 仅用于 app 接口场景 ",  "pageSize": " 每页查询返回数 "  } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS",  "value": {  ?"details":[{  "nickName": "昵称",  "inviteTime": XXX # long类型时间戳  ?}] ,  ?"pageInfo":{  "nextKey": " 输出下一页键值 , 该栏位返回为空代表查询完毕，仅用于 app 接口场景 "  }  ?}  "messageItems": null,? ? "msg": "SUCCESS",? ? "serverTime": "2025-07-29 18:32:05", "sysTransTime": "183205", "success": true } |
| 退出活动接口  1.退出成功，当前用户发activity、push、email  2.人数不足 下月 将会 降级/退团时（ 当月首次才 触发），异步：全员发push、email  3.销户增加退出处理（监听销户MQ） | /dmb/npo9iy/activity/zazone/quitActivity | { "customerNo": "XXX" } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS",  "value": null ,  "messageItems": null,? ? "msg": "SUCCESS", "serverTime": "2025-07-29 18:32:05", "sysTransTime": "183205", "success": true } |
| 每月1日0点通知activity、email | 每月1日0点任务：  1.退团(1→0)，所有团员发activity、email  2.降级(n→m)，所有团员发activity、email |  |  |
| 当月月底的倒数 第2日 早上1 0 : 00通知 P ush、Email | 当月月底的倒数 第2日 早上1 0 : 00任务：  1.退团(1→0)，所有团员发 P ush 、email  2.降级(n→m)，所有团员发 P ush 、email |  |  |
| 后管 | 活动工厂配置页  ~~运营-认证企业 (客服查组团)~~  ~~运营-名单管理~~  ~~运营-权益发放记录 (rcs后管)~~ |  |  |
| 参与内部员工福利活动 | 1.ticket增加亲友，增加校验，如果参与内部员工，报错  2.大数据推送内部员工名单，如果该员工参与zazone，自动触发退团 |  |  |
| 1.用户如在30天内未成团，则展示在到期日的倒数第3天,提示用户试用的权益将到期。  2.当月首次触发的即将降级通知取消，增加每月15号10点发送。  ZaZoneNextMonthsDowngradeReminderJob  ZA Zone下月降级提醒任务  0 0 10 15,28 \* ? | 每天10点执行： 发push/邮件通知提醒  查询userMemberShip |  |  |
| 福利详情权益列表查询 | /dmb/n5kliy/activity/zazone/queryInterest | { "customerNo": "XXX"  } | { "code": "000000", "responseCode": "UMP000000",  "value": {  ?"currentLevel": 1, ## 0=未成团  " advCodeExpireTime ": 123L, #专属邀请码对应权益过期时间  " advRightExpireFlag ": false, #专属邀请码对应权益是否过期:true是 false否  " interestList ": [{  //权益类型 private String interestType; //子权益类型 private String subInterestType; //权益产品名 private String interestName; //权益产品描述，支持国际化 private String interestDesc; //权益Icon private String interestIconUrl; //跳转链接 private String interestJumpUrl; //标签 private String interestTag;  "levelInterestConfigList":[{  "level": 2, //权益产品描述，支持国际化 private String interestDesc; }...]  ?}]  }, "success": true } |
| 员工福利与 ZA Zone的规则更新 | 企业认证校验放开；  加入众安自动退团处理逻辑移除； |  |  |

**2.2 RCS权益模块**

![](data:image/png;base64...)

![](data:image/png;base64...)

![](data:image/png;base64...)

**用户等级维护**

功能1：用户升级，入参用户等级，团队标识，团队等级否变动（0不变，1增加，2 降低），用户标识，事件发生的时间，事件编号
功能2：用户降级，当团队人员减少时，用户级别也跟着变动，团队等级否变动（0不变，1增加，2 降低），需要用户标识，变更后的等级，团队标识，事件发生的时间，事件编号

当团队等级 发生变更时，需要同时处理，该团队下的所有用户的权益,用户一个月用同一个等级仅发一次权益，

团队升级时：已经发放的权益不回收（加息券特殊需要替换），直接发新级别的权益，同步发放当前用户的权益，异步发放团内其他用户的权益,先写发放计划表，再发放

团队降级时：退出的用户以及整个团体的等级都更新，次月按照新等级发放权益

默认是等级是长期的，

新增用户等级变更表：t\_user\_membership\_log， 记录用户的等级变更的流水记录

|  |
| --- |
| SQL CREATE TABLE zabank\_rcs\_core.`t\_user\_membership\_log` (  `id` bigint(20) NOT NULL AUTO\_INCREMENT COMMENT '物理主键',  `serial\_no` varchar(64) NOT NULL COMMENT '流水号',  `user\_id` bigint(20) NOT NULL COMMENT '用户ID',  `member\_type` char(2) NOT NULL DEFAULT '4' COMMENT '会员类型:4=企业专区',  `operation\_type` tinyint(1) NOT NULL COMMENT '用户操作类型 1-增加，2-减少',  `business\_id` varchar(64) NOT NULL COMMENT '团队标识',  `team\_level\_change` tinyint(1) NOT NULL DEFAULT 0 COMMENT '团队等级变动 0-不变，1-增加，2-降低',  `event\_time` datetime(3) NOT NULL COMMENT '事件发生时间',  `log\_status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '处理状态 1-待处理，2-处理中，3-已完成，9-失败',  `process\_time` datetime(3) NULL COMMENT '处理时间',  `remark` varchar(255) NULL COMMENT '备注',  `is\_deleted` char(1) NOT NULL DEFAULT 'N' COMMENT '逻辑删除，N:正常，Y:删除',  `create\_time` datetime DEFAULT CURRENT\_TIMESTAMP COMMENT '创建时间',  `creator` varchar(45) DEFAULT 'system' COMMENT '创建人',  `modify\_time` datetime DEFAULT CURRENT\_TIMESTAMP ON UPDATE CURRENT\_TIMESTAMP COMMENT '修改时间',  `modifier` varchar(45) DEFAULT 'system' COMMENT '更新人',  PRIMARY KEY (`id`),  UNIQUE KEY `uk\_serial\_no` (`serial\_no`),  KEY `idx\_user\_id` (`user\_id`),  KEY `idx\_business\_id` (`business\_id`),  KEY `idx\_event\_time` (`event\_time`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户等级变更流水表';   CREATE TABLE zabank\_rcs\_core.`t\_user\_membership\_rights\_order` (  `id` bigint(20) NOT NULL AUTO\_INCREMENT COMMENT '物理主键',  `order\_no` varchar(64) NOT NULL COMMENT '订单号（对应 t\_rights\_send\_plan.order\_no）',  `serial\_no` varchar(64) NOT NULL COMMENT '关联流水号',  `user\_id` bigint(20) NOT NULL COMMENT '用户ID',  `business\_id` varchar(64) NOT NULL COMMENT '团队标识',  `team\_level` int(11) NOT NULL COMMENT '团队等级',  `benefit\_type` tinyint(4) NOT NULL COMMENT '权益类型：1-当月，2-预发',  `effective\_time` datetime(3) NOT NULL COMMENT '权益生效时间',  `order\_status` tinyint(4) NOT NULL DEFAULT 0 COMMENT '订单状态：0-待处理，1-处理中，2-已完成，3-已取消，4-处理失败',  `process\_time` datetime(3) DEFAULT NULL COMMENT '开始处理时间',  `complete\_time` datetime(3) DEFAULT NULL COMMENT '完成时间',  `total\_count` int(11) NOT NULL DEFAULT 0 COMMENT '权益总数',  `success\_count` int(11) NOT NULL DEFAULT 0 COMMENT '成功发放数',  `failed\_count` int(11) NOT NULL DEFAULT 0 COMMENT '失败数',  `retry\_count` int(11) NOT NULL DEFAULT 0 COMMENT '重试次数',  `max\_retry\_count` int(11) NOT NULL DEFAULT 3 COMMENT '最大重试次数',  `error\_msg` varchar(500) DEFAULT NULL COMMENT '错误信息',  `is\_deleted` char(1) NOT NULL DEFAULT 'N' COMMENT '逻辑删除，N:正常，Y:删除',  `create\_time` datetime DEFAULT CURRENT\_TIMESTAMP COMMENT '创建时间',  `creator` varchar(45) DEFAULT 'system' COMMENT '创建人',  `modify\_time` datetime DEFAULT CURRENT\_TIMESTAMP ON UPDATE CURRENT\_TIMESTAMP COMMENT '修改时间',  `modifier` varchar(45) DEFAULT 'system' COMMENT '更新人',  PRIMARY KEY (`id`),  UNIQUE KEY `uk\_order\_no` (`order\_no`),  KEY `idx\_serial\_no` (`serial\_no`),  KEY `idx\_user\_effective` (`user\_id`, `effective\_time`),  KEY `idx\_status\_effective` (`order\_status`, `effective\_time`),  KEY `idx\_status\_retry` (`order\_status`, `retry\_count`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户会员权益订单表'; |

|  |  |  |  |
| --- | --- | --- | --- |
| 接口说明 | 接口 路径 | 请求参数 | 响应 |
| 用户升级接口 | /rc/groupMembership/user/updategrade | {  "serialNo":"/流水id,幂等" "memberType“:"4" "userId": 123456789, //userid "teamLevel": "T1", ##用户的团队等级 "operationType":"1",##用户参与标识（1参加，2退出） "businessId": "TEAM\_001", ##团队标识，必填，字符串类型 "teamLevelChange": false, ?##团队等级变动，必填，false-不变，true-变动 "eventTime": "2025-07-29 18:32:05", ##事件发生时间 } | { "code": "000000", "responseCode": "UMP000000", "status": "SUCCESS", "messageVars": null, "messageItems": null, "msg": "SUCCESS", "serverTime": "2025-07-29 18:32:05", "sysTransTime": "183205", "success": true } |
|  |  |  |  |

**用户权益的发放**

基础原则

* **权益发放时机** ：升级立即发放，降级，次月发新等级权益
* **团队处理** ：团队等级变动时需要处理团队内所有用户
* **幂等性保证** ：通过发放记录表确保同一用户同一等级同一月份仅发放一次
* **异步处理** ：团队升级时，触发用户同步处理，其他用户可异步处理

1.新增券的发放渠道，@兆增分配

2.升级的用户立即发放当期权益，涉及团队升级，其他用户异步发放权益

t\_user\_membership，增加字段

|  |
| --- |
| Ruby -- 给 t\_user\_membership 表增加字段（ ALTER TABLE `t\_user\_membership`  ADD COLUMN `current\_level` int(11) NOT NULL DEFAULT 0 COMMENT '当前用户等级0,1 2 ', ADD COLUMN `next\_level` int(11) NOT NULL DEFAULT 0 COMMENT '待生效等级', ADD COLUMN `next\_level\_effict\_month` varchar(64) DEFAULT NULL COMMENT '待生效月份'; |

3.退出团的用户，权益不处理，涉及团队降级，需要变动其他用户的权益等级，

4.用户A退出A某个团队时，如果不参加其他团队，权益到当月底，第二月不再发放权益
5.用户不在团队中，参加团队，根据级别来， 回收原有的权益，发放新的权益（替换）， 原来级别时3级别，现在参加1级团，新加团需要发 1级
已有会员体系表，是否可以兼容

6.在跨月的节点时，当月最后一天凌晨，预发下月的权益，根据t\_user\_membership，中member\_type=4 来过滤，

7.如果在最后一天，用户等级提升，需要将预发的数据回收，重新发最新的权益，含当月，以及下个月的；月底出现团等级下降，需要回收预发的权益，重新发新的权益

8.同一用户的权益做到幂等，发放的biz生成了逻辑为， custmerNo+年月+权益模板id，发放前查询是否已经发放，已发放不处理，打印日志

权益包： 复用 r\_rights\_product加类型隔离，新类型ZAZone, level来做不同级别使用不通的产品, 同等级只配置一条产品信息

|  |
| --- |
| Java ALTER TABLE `zabank\_rcs\_core`.`t\_rights\_product` ADD COLUMN `product\_level` tinyint NOT NULL DEFAULT 0 COMMENT '产品适用等级默认0级别，1为一级的权益 2为二级权益' after order\_no; |

权益包配置表,：可直接复用，t\_rights\_relation需要增加字段，权益是否替换（升级时权益需要原子性更换）

|  |
| --- |
| SQL ALTER TABLE `t\_rights\_relation` ADD COLUMN `upgrade\_replace\_interest` varchar(32) NOT NULL COMMENT '升级后替换的权益id' after send\_period ； |

每月定时任务，提前批量发放权益，通过表t\_user\_membership，中member\_type=4 来过滤，先批量生成发放计划，然后异步发放+定时任务扫描

发放计划表修改：

|  |
| --- |
| SQL -- 字段添加 ALTER TABLE zabank\_rcs\_core.t\_rights\_send\_plan ADD COLUMN `rights\_level` char(4) NOT NULL DEFAULT 0 COMMENT '用户权益等级 0-基础级别 1-一级， 2二级', ADD COLUMN `benefit\_type` tinyint(4) NOT NULL DEFAULT 1 COMMENT '权益类型：1-当月生效，2-预发权益', ADD COLUMN `parent\_biz\_no` varchar(64) DEFAULT NULL COMMENT '被替换的权益业务编号', ADD COLUMN `replace\_reason` varchar(100) DEFAULT NULL COMMENT '替换原因', ADD COLUMN `replace\_rights\_id`varchar(20) DEFAULT NULL COMMENT '需要替换掉的权益id';  ALTER TABLE zabank\_rcs\_core.t\_rights\_send\_plan ADD COLUMN `product\_type` int(11) DEFAULT 2 COMMENT '计划所属UserProductTypeEnum的code，历史默认值是2 ';    -- 修改现有字段注释，明确 order\_no 的双重作用 ALTER TABLE zabank\_rcs\_core.`t\_rights\_send\_plan` MODIFY COLUMN `order\_no` varchar(64) NOT NULL COMMENT '订单号/权益组ID（同组权益共享相同订单号）', MODIFY COLUMN `send\_status` char(1) NOT NULL COMMENT'发放状态：0-待发放，1-发放中，2-已发放，3-发放失败，4-已取消，5-已失效，6-预发待生效';  -- 添加对应索引 ALTER TABLE zabank\_rcs\_core.`t\_rights\_send\_plan` ADD KEY `idx\_order\_no` (`order\_no`); -- 给 t\_user\_membership 表增加字段（ ALTER TABLE zabank\_rcs\_core.`t\_user\_membership` ADD COLUMN `current\_level` int(11) NOT NULL DEFAULT 0 COMMENT '当前用户等级0,1 2 ', ADD COLUMN `next\_level` int(11) NOT NULL DEFAULT 0 COMMENT '待生效等级', ADD COLUMN `next\_level\_effect\_month` varchar(64) DEFAULT NULL COMMENT '待生效月份';  ALTER TABLE zabank\_rcs\_core.`t\_rights\_relation` ADD COLUMN `upgrade\_replace\_interest` varchar(32) DEFAULT NULL COMMENT '升级需要替换的权益id' after send\_period;  ALTER TABLE `zabank\_rcs\_core`.`t\_rights\_product` ADD COLUMN `product\_level` tinyint NOT NULL DEFAULT 0 COMMENT '产品适用等级默认0级别，1为一级的权益 2为二级权益' after order\_no;   ALTER TABLE `zabank\_rcs\_core`.`t\_rights\_product` modify COLUMN `rights\_pool\_id` varchar(8) DEFAULT NULL COMMENT '权益包ID';   -- 删除现有的唯一索引 ALTER TABLE zabank\_rcs\_core.t\_rights\_product DROP INDEX uniq\_product\_id; |

权益记录查询，直接调用权益系统查。

|  |  |  |  |
| --- | --- | --- | --- |
| 接口说明 | 接口 路径 | 请求参数 | 响应 |
| 查询用户的权益信息 | /rc/rights/interest/list | { "userId": 123456789, //userid "customerNo":"", ?"productType":"ZAZone" } | { "interestList": [ { "interestName": "权益产品名称1", "interestDesc": "权益产品描述1，支持国际化", "interestInstruction": "权益说明1", "productId": "PROD001", "interestId": "INT001", "interestType": "DISCOUNT", "subInterestType": "4", "interestIconUrl": " <https://example.com/icon1.png>", "interestSmallIconUrl": " <https://example.com/small_icon1.png>", "interestBackgroundUrl": " <https://example.com/bg1.png>", "interestBoughtBackgroundUrl": " <https://example.com/bought_bg1.png>", "interestJumpUrl": " <https://example.com/jump1>", "orderNo": 1, "periodType": "MONTH", "period": "1个月" }, { "interestName": "权益产品名称2", "interestDesc": "权益产品描述2，支持国际化", "interestInstruction": "权益说明2", "productId": "PROD002", "interestId": "INT002", "interestType": "CASHBACK", "subInterestType": "DINING", "interestIconUrl": " <https://example.com/icon2.png>", "interestSmallIconUrl": " <https://example.com/small_icon2.png>", "interestBackgroundUrl": " <https://example.com/bg2.png>", "interestBoughtBackgroundUrl": " <https://example.com/bought_bg2.png>", "interestJumpUrl": " <https://example.com/jump2>", "orderNo": 2, "periodType": "DAY", "period": "每日" } ] } |
| 用户等级查询 | rc/groupship/user/level | { "userId": 123456789, //userid "customerNo":"", ?"productType":"ZAZone" } | { "productType":"ZAZone" "userLevel": "T1", ##用户的等级 } |
| 用户当前等级已发放的权益 | rc/groupship/user/interest/list | { "userId": 123456789, //userid "customerNo":"", ?"productType":"ZAZone" } | { "currentMonthInterstList":"ZAZone" "userLevel": "T1", ##用户的等级 } |

**2.3 后管**

**2.4 组团**

[14 组团组件设计概要 - ZA BANK DEV - ZA Knowledge Management](https://zaglobal.feishu.cn/wiki/NGOcwBqlfiyo1tkLiumcGSsenyd)

**2.5 卡券**

**3.架构变更及评审**

不涉及

**4.需求模块拆解**

已在整体设计概要中描述，这里不做赘述。

**5.分模块概要设计**

**6.整体兼容性分析**

**6.1?上游调用方分析**

**6.2下游被调用方分析**

**6.3app兼容性分析**

**6.3.1老版本app新代码**

不涉及

**6.3.2老版本app新数据**

不涉及

**6.3.3新版本app老数据**

不涉及

**6.4数据兼容性分析**

**6.4.1新数据老代码**

详见6.3

**6.4.2新代码老数据**

详见6.3

**6.5后管兼容性分析**

不涉及

**6.6发布机房兼容性分析**

前后向都兼容，发布顺序无影响

**6.6.1新老机房流量兼容分析**

前后向都兼容，发布顺序无影响

**6.6.2发布切流兼容性分析**

前后向都兼容，发布顺序无影响

**6.6.3发布时序顺序分析**

前后向都兼容，发布顺序无影响

**7.兼容性方案**

不涉及

**8.业务降级和数据一致性梳理**

此处缺图：上下游调用关系全览图

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 序号 | 功能点 | 调用下游 | 是否启用熔断/降级 | 不启用的原因 | 业务降级方案简述 | 是否存在多发数据一致性场景 | 数据一致性方案 |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

**9.多线程安全梳理**

不涉及

**10.发布物料**

**10.1发布系统**

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 序号 | 系统名称 | 发布方式 | db | tag |
| 1 | zabank-rcs-core-service |  |  |  |
|  | zabank-rcs-batch-service |  |  |  |
|  | zabank-imc-cubercore-service |  |  |  |
|  | zabank-imc-interestcore-service | panda, BANK-80512\_zabank-imc-batch-service\_468 | 已上传 |  |
|  | zabank-imc-batch-service | panda, BANK-80512\_zabank-imc-batch-service\_468 |  |  |
|  | zabank-imc-activity-service | panda, BANK-80512\_zabank-imc-batch-service\_468 | 已上传 |  |
|  | zabank-imc-mbs-web | panda, BANK-80512\_zabank-imc-batch-service\_468 |  |  |
|  | za-mks-marketing-service |  |  |  |
|  | zabank-mbs-statistics-service |  |  |  |
|  | zaip-cuber-manager-web | moray，new-rcs |  |  |
|  | zaip-cuber-render-web | moray，  feature/BANK-77222 |  |  |
|  | zaip-sales-coupon-service | moray，  feature/BANK-77222 | 已上传 |  |
|  | zaip-sales-batch-service | moray，  feature/BANK-77222 |  |  |

**10.2 sql物料**

|  |
| --- |
| SQL 参考xcode  1125新增： INSERT INTO `zabank\_imc\_interestcore`.`t\_sub\_interest\_type`( `sub\_interest\_type`, `parent\_interest\_type`, `remark`, `sub\_interest\_type\_name`, `sub\_interest\_type\_name\_ca`, `sub\_interest\_type\_name\_en`, `jump\_url`, `jump\_url\_ca`, `jump\_url\_en`, `is\_deleted`, `create\_time`, `creator`, `modify\_time`, `modifier`) VALUES ( '76', '16', '', '货币兑换立减券', '貨幣兌換即減券', 'Currency Exchange Saver Coupon', NULL, NULL, NULL, 'N', now(), 'system', now(), 'system'); INSERT INTO `zabank\_imc\_interestcore`.`t\_sub\_interest\_type`( `sub\_interest\_type`, `parent\_interest\_type`, `remark`, `sub\_interest\_type\_name`, `sub\_interest\_type\_name\_ca`, `sub\_interest\_type\_name\_en`, `jump\_url`, `jump\_url\_ca`, `jump\_url\_en`, `is\_deleted`, `create\_time`, `creator`, `modify\_time`, `modifier`) VALUES ( '65', '16', '', '消费回赠券', '消費回贈券', 'Spending Rebate Coupon', NULL, NULL, NULL, 'N', now(), 'system', now(), 'system'); INSERT INTO `zabank\_imc\_interestcore`.`t\_sub\_interest\_type`( `sub\_interest\_type`, `parent\_interest\_type`, `remark`, `sub\_interest\_type\_name`, `sub\_interest\_type\_name\_ca`, `sub\_interest\_type\_name\_en`, `jump\_url`, `jump\_url\_ca`, `jump\_url\_en`, `is\_deleted`, `create\_time`, `creator`, `modify\_time`, `modifier`) VALUES ( '54', '16', '', '海外汇款现金回赠券', '海外匯款現金回贈券', 'Global Transfer Cashback Coupon', NULL, NULL, NULL, 'N', now(), 'system', now(), 'system'); INSERT INTO `zabank\_imc\_interestcore`.`t\_sub\_interest\_type`( `sub\_interest\_type`, `parent\_interest\_type`, `remark`, `sub\_interest\_type\_name`, `sub\_interest\_type\_name\_ca`, `sub\_interest\_type\_name\_en`, `jump\_url`, `jump\_url\_ca`, `jump\_url\_en`, `is\_deleted`, `create\_time`, `creator`, `modify\_time`, `modifier`) VALUES ( '32', '16', '', '保费优惠券', '保費優惠券', 'Insurance Discount Coupon', NULL, NULL, NULL, 'N', now(), 'system', now(), 'system');  INSERT INTO `zabank\_imc\_cubercore`.`t\_common\_tag\_type`( `tag\_type`, `description`, `is\_deleted`, `create\_time`, `creator`, `modify\_time`, `modifier`) VALUES ( 3, '权益', 'N', '2025-11-12 17:06:20', 'admin', '2025-11-13 10:32:07', 'admin'); |

**10.3定时任务物料**

rcs-batch

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 序号 | 任务名称 | 描述 | 执行计划 | 上线状态 |  |
| 1 | {"job":"com.zatech.bank.rights.job.MemberOrderUpdateJob"} | zazone权益订单重试job | CRON 0 0/10 \* \* \* ? | 开启 |  |
| 2 | {"job":"com.zatech.bank.rights.job.MemberShipLevelUpdateJob"} | zazone月初会员等级更新任务 | CRON 0 0 0 1 \* \* | 开启 |  |
| 3 | {"job":"com.zatech.bank.rights.job.MonthlyBenefitPreGrantJob"} | zazone月底预发权益 | CRON 0 0 10 L \* ? | 开启 |  |
| 4 | {"job":"com.zatech.bank.rights.job.ZaZoneNextMonthsDowngradeReminderJob"} | ZA Zone下月降级提醒任务 | CRON 0 0 10 L-1 \* ?  1125迭代修改 ：CRON 0 0 10 15,28 \* ? | 开启 |  |
| ~~5~~ | ~~{"job":"com.zatech.bank.rights.job.ZaZoneMonthlyDowngradeReminderJob"}~~ | ~~ZA Zone月度降级提醒任务~~ | ~~CRON 0 0 0 1 \* ?~~ |  |  |
| 6 | {\"job\":\"com.zatech.bank.rights.job.ZaZonePreExpireReminderJob\"} | Zone专属权益即将到期提醒任务,  1125迭代新增 | CRON 0 0 10 10 \* ? | 开启 | {"id":null,"jobName":"Zone专属权益即将到期提醒任务","jobDescription":"Zone专属权益即将到期提醒任务","appId":91,"jobParams":"{\"job\":\"com.zatech.bank.rights.job.ZaZonePreExpireReminderJob\"}","timeExpressionType":"CRON","timeExpression":"0 0 10 \* \* ?","executeType":"STANDALONE","processorType":"BUILT\_IN","processorInfo":"com.zabank.magicbox.powerjob.adapter.processor.JobDispatcher","maxInstanceNum":0,"concurrency":5,"instanceTimeLimit":0,"instanceRetryNum":0,"taskRetryNum":1,"minCpuCores":0,"minMemorySpace":0,"minDiskSpace":0,"enable":true,"designatedWorkers":"","maxWorkerCount":0,"notifyUserIds":null,"alarmLevel":3,"extra":null,"dispatchStrategy":"RANDOM","lifeCycle":{"start":null,"end":null},"alarmConfig":{"alertThreshold":0,"statisticWindowLen":0,"silenceWindowLen":0},"tag":null,"logConfig":{"type":1,"level":null,"loggerName":null}} |

imc-batch

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 序号 | 任务名称 | 描述 | 执行计划 | 上线状态 |
| 1 | {"job":"com.zabank.imc.batch.job.ZoneTeamDisbandJob"} | 会员团队解散任务JOB:上线关闭，运维手动触发执行  参数运行：{"teamTag":"@ [999.com](http://999.com) ","cuberAlias":"zoneProjectId#zoneActivity"} | CRON 0 0 0 1 1 ? 2099 | 关闭 |
| 2 |  |  |  |  |

**10.4 actvitiy配置**

[众安\_Activity参数配置清单\_zazone-.xlsx](https://zagroup-my.sharepoint.com/%3Ax%3A/g/personal/zhaozeng_he_za_group/EbQp-TjVqgtNoM4Oqi5wm2cBnliy_F1D9TAiacQr-RL6EA?e=LdkZzL)

ump模板 [ZA Zone 文案.xlsx](https://zagroup-my.sharepoint.com/%3Ax%3A/g/personal/xing_fan_za_group/EWZS5mn3lYBKhQuXJYTJD3IBCwVl6PMEs_iZbsKOhxP3mw?e=SJdROb)

**10.5dbff接口**

|  |  |  |  |
| --- | --- | --- | --- |
| 序号 | url | 标题 | json附件 |
|  |  |  | **[ZAZone企业认证-4.json]**  **[ZAZone活动状态查询-1.json]**  **[ZAZone获取验证码-2.json]**  **[ZAZone活动首页查询-1.json]**  **[ZAZone查询邀请记录-1.json]**  **[ZAZone企业认证退出组团-2.json]**  **[ZAZone福利详情权益列表查询-1.json]** |
|  |  |  |  |

**10.6 apollo**

【系统1】

新增：

修改：

删除

**10.7错误码国际化物料**

|  |  |  |
| --- | --- | --- |
| 序号 | 错误码 | 错误信息 |
|  | // email组件 EMAIL\_SEND\_FAILED("IA2701", "验证码发送失败"), EMAIL\_FORMAT\_ERROR("IA2702", "邮箱格式不合法"), EMAIL\_CONFIG\_NOT\_EXIST("IA2703", "配置不存在"), EMAIL\_SUFFIX\_NOT\_ALLOWED("IA2704", "邮箱不允许参加活动"), EMAIL\_AUTH\_EXPIRE("IA2705","邮箱认证码过期"), EMAIL\_AUTH\_EXIST("IA2706", "邮箱已经认证了"), EMAIL\_NOT\_ACTIVITY\_TIME("IA2707", "非活动时间"), EMAIL\_AUTH\_ERROR("IA2708", "邮箱认证失败"), EMAIL\_AUTH\_CODE\_ERROR("IA2709", "邮箱认证验证码错误"), EMAIL\_AUTH\_CODE\_ERROR\_TOO\_MANY("IA2710", "邮箱认证验证码错误次数过多"), EMAIL\_AUTH\_NOT\_EXIST("IA2711", "邮箱认证记录不存在"), CANCEL\_EMAIL\_AUTH\_FAILED("IA2712", "取消邮箱认证失败"), EMAIL\_LIMIT\_ERROR("IA2716", "邮箱认证超出上限"), EMAIL\_AUTH\_MONTHLY\_LIMIT\_EXCEEDED("IA2713", "用户本月已达到邮箱认证上限"), EMAIL\_AUTH\_YEARLY\_LIMIT\_EXCEEDED("IA2714", "用户本年已达到邮箱认证上限"), EMAIL\_YEARLY\_LIMIT\_EXCEEDED("IA2715", "该邮箱本年已达到认证上限"), // 组团组件错误码 TEAM\_IS\_FULL("IA2901", "团队已满员"), USER\_ALREADY\_IN\_TEAM("IA2902", "用户已在团队中"), TEAM\_NOT\_EXIST("IA2903", "团队不存在"), TEAM\_CONFIG\_NOT\_EXIST("IA2904", "团队配置不存在"), JOIN\_TEAM\_FAILED("IA2905", "加入团队失败"), USER\_NOT\_IN\_TEAM("IA2906", "用户不在团队中"), QUIT\_TEAM\_FAILED("IA2907", "退出团队失败"), //企业专区 EMAIL\_NOT\_STANDARD("IA2801", "邮箱不符合规范"), EMAIL\_SEND\_FAIL("IA2802", "邮件验证码发送失败,请重试"), EMPLOYEE\_NOT\_ALLOW("IA2803", "内部员工不允许Zone活动"), EMPLOYEE\_RELATIVES\_NOT\_ALLOW("IA2804", "员工亲友不允许Zone活动"), ZONE\_MGM\_CODE\_ERROR("IA2805", "邀请码错误,请重新输入"), ZONE\_MGM\_CODE\_UNVERIFY\_ERROR("IA2806", "该邀请码所属客户还未认证"), ZONE\_MGM\_CODE\_UNMATCH\_ERROR("IA2807", "该邀请码所属客户必须和你是同一个公司有效域名"),  ZONE\_RESTRICT\_TIME\_ERROR("IA2808", "当前时间在限制时间段内(23:50:00-24:00:00),不允许操作"),  ZONE\_JOIN\_ADV\_VALID\_ERROR("IA2809", "曾经使用过专属邀请码,不能再次使用"), |  |
|  |  |  |

**10.8 前端海鸥文案**

[https://zagroup-my.sharepoint.com/:x:/g/personal/bx-chenqiaolong001\_zagroup\_onmicrosoft\_com/EU8zoHQDQnZEtZsjTHm\_psUBmOK2EEpp8vX0pUnYmYsKcg?e=Rbbrxk](https://zagroup-my.sharepoint.com/%3Ax%3A/g/personal/bx-chenqiaolong001_zagroup_onmicrosoft_com/EU8zoHQDQnZEtZsjTHm_psUBmOK2EEpp8vX0pUnYmYsKcg?e=Rbbrxk)

**11.测试重点关注要点列举**

1、

**12.发布后生产配置清单**

1、dbff新接口

**13. 下线配置清单**

不涉及，无需单独下线

**Original Confluence page attachments**

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Name | Size | Created by | Created on | Labels | Comments |
| **[image-2025-11-24\_10-50-39.png]** | 3.69 KB | 贺 兆增 | 2025-11-24T10:50:39.562+08:00 |  |  |
| **[ZAZone福利详情权益列表查询-1.json]** | 1.64 KB | 贺 兆增 | 2025-11-24T10:46:15.845+08:00 |  |  |
| **[ZAZone获取验证码-2.json]** | 1.56 KB | 贺 兆增 | 2025-10-14T11:30:20.960+08:00 |  |  |
| **[ZAZone企业认证退出组团-2.json]** | 1.54 KB | 贺 兆增 | 2025-10-14T11:28:38.838+08:00 |  |  |
| **[ZAZone查询邀请记录-1.json]** | 1.33 KB | 贺 兆增 | 2025-10-14T11:28:25.751+08:00 |  |  |
| **[ZAZone活动首页查询-1.json]** | 1.53 KB | 贺 兆增 | 2025-10-14T11:26:12.695+08:00 |  |  |
| **[ZAZone企业认证退出组团-1.json]** | 1.32 KB | 贺 兆增 | 2025-10-14T11:26:12.125+08:00 |  |  |
| **[ZAZone获取验证码-1.json]** | 1.33 KB | 贺 兆增 | 2025-10-14T11:26:11.412+08:00 |  |  |
| **[ZAZone活动状态查询-1.json]** | 1.53 KB | 贺 兆增 | 2025-10-14T11:26:10.818+08:00 |  |  |
| **[ZAZone企业认证-4.json]** | 1.53 KB | 贺 兆增 | 2025-10-14T11:25:22.670+08:00 |  |  |
| **[image-2025-9-8\_19-58-43.png]** | 97.76 KB | 贺 兆增 | 2025-09-08T19:58:43.775+08:00 |  |  |
| **[image-2025-9-8\_10-33-23.png]** | 74.16 KB | 杨 威 | 2025-09-08T10:33:23.681+08:00 |  |  |
| **[image-2025-9-8\_10-28-33.png]** | 41.47 KB | 杨 威 | 2025-09-08T10:28:33.201+08:00 |  |  |
| **[image-2025-8-1\_15-48-20.png]** | 57.63 KB | 贺 兆增 | 2025-08-01T15:48:20.683+08:00 |  |  |
| **[image-2025-7-31\_11-2-18.png]** | 57.65 KB | 杨 威 | 2025-07-31T11:02:18.200+08:00 |  |  |
| **[image-2025-7-31\_9-49-26.png]** | 80.77 KB | 贺 兆增 | 2025-07-31T09:49:26.478+08:00 |  |  |
| **[image-2025-7-29\_21-57-37.png]** | 18.71 KB | 杨 威 | 2025-07-29T21:57:37.962+08:00 |  |  |
| **[权益发放流程.jpg]** | 132.47 KB | 杨 威 | 2025-07-29T21:12:00.942+08:00 |  |  |
| **[用户等级变更及权益下发流程图.svg]** | 20.94 KB | 杨 威 | 2025-07-29T21:07:40.905+08:00 |  |  |
