---
name: invest-entity-spec
description: INVEST框架实体类完整开发规范。当设计数据库实体、配置MyBatis-Plus注解、处理持久化对象时使用。包含实体类设计、字段注解、命名规范等内容。
---

# INVEST 实体类开发规范

INVEST框架实体类负责映射数据库表结构，提供标准化的持久化对象设计。本规范定义了实体类的设计原则和开发标准。

## 快速开始

基本实体类实现:
```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("stk_order")
public class StkOrder implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    @TableField("order_no")
    private String orderNo;

    @TableField("user_id")
    private String userId;

    @TableField("create_time")
    private Date createTime;
}
```

## 核心规范

### 1. 实体类命名规范

- **类名**: 直接使用业务名称，如`StkOrder`、`StkHolding`
- **包路径**: 位于`model.entity`包下（domain模块）
- **表映射**: 使用`@TableName`注解映射数据库表

```java
@TableName("stk_order")
public class StkOrder implements Serializable {
    // 实体字段定义
}
```

### 2. 基本注解要求

所有实体类必须：
- 实现`Serializable`接口
- 使用`@Data`注解（Lombok）
- 使用`@TableName`指定表名
- 使用`@TableId`指定主键

```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("stk_order")
public class StkOrder implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    
    // 其他字段...
}
```

## 字段注解规范

### 1. 主键注解 @TableId

```java
// 自增主键
@TableId(value = "id", type = IdType.AUTO)
private Long id;

// 输入主键（手动设置）
@TableId(value = "id", type = IdType.INPUT)
private Long id;

// 雪花算法ID
@TableId(value = "id", type = IdType.ASSIGN_ID)
private Long id;
```

### 2. 字段映射 @TableField

```java
// 基本字段映射
@TableField("order_no")
private String orderNo;

@TableField("user_id")
private String userId;

@TableField("create_time")
private Date createTime;

// 数值字段
@TableField("entrust_price")
private BigDecimal entrustPrice;

@TableField("entrust_qty")
private BigDecimal entrustQty;
```

### 3. 非数据库字段

```java
// 该字段不映射到数据库
@TableField(exist = false)
private String tempData;

// 查询时不返回该字段
@TableField(select = false)
private String sensitiveData;
```

## 完整实体类示例

```java
package group.za.bank.sbs.trade.model.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

/**
 * 股票订单表
 *
 * @author developer
 * @since 2022-05-27
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("stk_order")
public class StkOrder implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 主键
     */
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    /**
     * 订单号
     */
    @TableField("order_no")
    private String orderNo;

    /**
     * 用户ID
     */
    @TableField("user_id")
    private String userId;

    /**
     * 客户交易账号
     */
    @TableField("account_id")
    private String accountId;

    /**
     * 货币单位HKD,USD,CNY
     */
    @TableField("currency")
    private String currency;

    /**
     * 市场类型(US,HK)
     */
    @TableField("market_code")
    private String marketCode;

    /**
     * 股票代码
     */
    @TableField("stock_code")
    private String stockCode;

    /**
     * 股票名称
     */
    @TableField("stock_name")
    private String stockName;

    /**
     * 委托价格
     */
    @TableField("entrust_price")
    private BigDecimal entrustPrice;

    /**
     * 委托数量
     */
    @TableField("entrust_qty")
    private BigDecimal entrustQty;

    /**
     * 委托金额
     */
    @TableField("entrust_amount")
    private BigDecimal entrustAmount;

    /**
     * 订单状态
     */
    @TableField("status")
    private String status;

    /**
     * 创建时间
     */
    @TableField("create_time")
    private Date createTime;

    /**
     * 更新时间
     */
    @TableField("update_time")
    private Date updateTime;

    /**
     * 创建人
     */
    @TableField("creator")
    private String creator;

    /**
     * 更新人
     */
    @TableField("modifier")
    private String modifier;

    /**
     * 非数据库字段 - 临时计算数据
     */
    @TableField(exist = false)
    private BigDecimal totalFee;
}
```

## 字段类型映射

| Java类型 | 数据库类型 | 说明 |
|----------|-----------|------|
| Long | BIGINT | 主键、ID类字段 |
| Integer | INT | 整数字段 |
| String | VARCHAR | 字符串字段 |
| BigDecimal | DECIMAL | 金额、价格、数量 |
| Date | DATETIME/TIMESTAMP | 日期时间 |
| Boolean | TINYINT(1) | 布尔标志 |

## 金额和数量字段规范

```java
// 金额字段使用BigDecimal，不要使用Double
@TableField("entrust_price")
private BigDecimal entrustPrice;

@TableField("entrust_amount")
private BigDecimal entrustAmount;

// 数量字段也使用BigDecimal（支持小数股）
@TableField("entrust_qty")
private BigDecimal entrustQty;
```

## 时间字段规范

```java
// 创建时间
@TableField("create_time")
private Date createTime;

// 更新时间
@TableField("update_time")
private Date updateTime;

// 交易日期（只有日期）
@TableField("trade_date")
private Date tradeDate;
```

## 枚举字段处理

```java
// 方式一：存储枚举的值
@TableField("status")
private String status;  // 存储枚举的code值

// 方式二：使用MyBatis-Plus枚举处理器
@TableField("order_type")
private OrderTypeEnum orderType;  // 需要配置枚举处理器
```

## 命名规范总结

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | 业务名称 | StkOrder, StkHolding |
| 表名 | 小写下划线 | stk_order, stk_holding |
| 字段名 | 驼峰命名 | orderNo, userId |
| 列名 | 小写下划线 | order_no, user_id |
| 主键 | id | id |
| 创建时间 | createTime | create_time |
| 更新时间 | updateTime | update_time |
