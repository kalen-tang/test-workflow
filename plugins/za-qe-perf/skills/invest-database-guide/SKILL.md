---
name: invest-database-guide
description: INVEST数据库ORM使用指南。用于MyBatis-Plus配置、分页查询、TransactionUtils事务处理等数据持久化场景。当需要配置ORM、编写Mapper层代码、实现分页逻辑、使用TransactionUtils进行事务管理时使用。涉及数据库、ORM、MyBatis-Plus、事务等关键词时使用此skill。
---

# INVEST数据库ORM使用指南

## 🎯 Skill主要内容

- **核心功能**: MyBatis-Plus ORM配置和增强功能使用
- **适用场景**: 数据库操作、实体映射、分页查询
- **关键特性**: MyBatis-Plus增强、自动分页、逻辑删除

---

## 💾 ORM组件 - zainvest-mybatisplus-spring-boot-starter

### 📦 接入方式

引入依赖：
```xml
<dependency>
    <groupId>group.za.invest</groupId>
    <artifactId>zainvest-mybatisplus-spring-boot-starter</artifactId>
    <version>${zainvest.mybatisplus.version}</version>
</dependency>
```

### ⚙️ 配置说明

application.properties配置：
```properties
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://${mysql.host}:${mysql.port}/${mysql.database}?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
spring.datasource.username=${mysql.username}
spring.datasource.password=${mysql.password}
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.idle-timeout=30000
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.max-lifetime=1800000

mybatis-plus.mapper-locations=classpath*:mapper/**/*.xml
mybatis-plus.type-aliases-package=group.za.bank.sbs.trade.model.entity
mybatis-plus.configuration.map-underscore-to-camel-case=true
mybatis-plus.configuration.log-impl=org.apache.ibatis.logging.stdout.StdOutImpl
```

### 🚀 启动类配置

```java
@SpringBootApplication
@MapperScan("group.za.bank.sbs.trade.mapper")
public class TradeApplication {
    public static void main(String[] args) {
        SpringApplication.run(TradeApplication.class, args);
    }
}
```

---

## 📊 实体类设计

### 基础实体示例

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

    @TableField("stock_code")
    private String stockCode;

    @TableField("entrust_price")
    private BigDecimal entrustPrice;

    @TableField("status")
    private String status;

    @TableField("create_time")
    private Date createTime;

    @TableField("update_time")
    private Date updateTime;
}
```

---

## 🔍 查询操作

### LambdaQueryWrapper查询

```java
@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private StkOrderMapper orderMapper;

    // 单条件查询
    public StkOrder getByOrderNo(String orderNo) {
        return orderMapper.selectOne(
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getOrderNo, orderNo)
        );
    }

    // 多条件查询
    public List<StkOrder> getUserOrders(String userId, String status) {
        return orderMapper.selectList(
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getUserId, userId)
                .eq(StringUtils.isNotBlank(status), StkOrder::getStatus, status)
                .orderByDesc(StkOrder::getCreateTime)
        );
    }

    // 条件查询
    public List<StkOrder> queryOrders(OrderQueryReq req) {
        LambdaQueryWrapper<StkOrder> wrapper = new LambdaQueryWrapper<>();
        
        wrapper.eq(StkOrder::getUserId, req.getBankUserId());
        
        if (StringUtils.isNotBlank(req.getStatus())) {
            wrapper.eq(StkOrder::getStatus, req.getStatus());
        }
        if (StringUtils.isNotBlank(req.getStockCode())) {
            wrapper.eq(StkOrder::getStockCode, req.getStockCode());
        }
        if (req.getStartDate() != null) {
            wrapper.ge(StkOrder::getCreateTime, req.getStartDate());
        }
        if (req.getEndDate() != null) {
            wrapper.le(StkOrder::getCreateTime, req.getEndDate());
        }
        
        wrapper.orderByDesc(StkOrder::getCreateTime);
        
        return orderMapper.selectList(wrapper);
    }
}
```

### 分页查询

```java
public PageInfoResp<OrderResp> queryOrdersPage(OrderQueryReq req) {
    // 1. 创建分页对象
    Page<StkOrder> page = new Page<>(req.getPageNum(), req.getPageSize());
    
    // 2. 构建查询条件
    LambdaQueryWrapper<StkOrder> wrapper = new LambdaQueryWrapper<>();
    wrapper.eq(StkOrder::getUserId, req.getBankUserId())
           .orderByDesc(StkOrder::getCreateTime);
    
    // 3. 执行分页查询
    IPage<StkOrder> result = orderMapper.selectPage(page, wrapper);
    
    // 4. 转换为响应对象
    List<OrderResp> respList = result.getRecords().stream()
        .map(this::convertToResp)
        .collect(Collectors.toList());
    
    return new PageInfoResp<OrderResp>()
        .pageNum((int) result.getCurrent())
        .pageSize((int) result.getSize())
        .total(result.getTotal())
        .list(respList);
}
```

### 统计查询

```java
// 查询数量
public long countUserOrders(String userId) {
    return orderMapper.selectCount(
        new LambdaQueryWrapper<StkOrder>()
            .eq(StkOrder::getUserId, userId)
    );
}

// 判断是否存在
public boolean existsOrder(String orderNo) {
    return orderMapper.selectCount(
        new LambdaQueryWrapper<StkOrder>()
            .eq(StkOrder::getOrderNo, orderNo)
    ) > 0;
}
```

---

## ✏️ 更新操作

### LambdaUpdateWrapper更新

```java
// 根据ID更新
public boolean updateOrderStatus(Long id, String status) {
    StkOrder update = new StkOrder();
    update.setId(id);
    update.setStatus(status);
    update.setUpdateTime(new Date());
    return orderMapper.updateById(update) > 0;
}

// 条件更新
public boolean updateOrderStatus(String orderNo, String status) {
    LambdaUpdateWrapper<StkOrder> wrapper = new LambdaUpdateWrapper<>();
    wrapper.eq(StkOrder::getOrderNo, orderNo)
           .set(StkOrder::getStatus, status)
           .set(StkOrder::getUpdateTime, new Date());
    
    return orderMapper.update(null, wrapper) > 0;
}

// 批量更新
public boolean batchUpdateStatus(List<String> orderNos, String status) {
    LambdaUpdateWrapper<StkOrder> wrapper = new LambdaUpdateWrapper<>();
    wrapper.in(StkOrder::getOrderNo, orderNos)
           .set(StkOrder::getStatus, status)
           .set(StkOrder::getUpdateTime, new Date());
    
    return orderMapper.update(null, wrapper) > 0;
}
```

---

## ➕ 插入操作

```java
// 单条插入
public boolean createOrder(StkOrder order) {
    order.setCreateTime(new Date());
    order.setUpdateTime(new Date());
    return orderMapper.insert(order) > 0;
}

// 批量插入（需要IService接口）
public boolean batchCreateOrders(List<StkOrder> orders) {
    orders.forEach(order -> {
        order.setCreateTime(new Date());
        order.setUpdateTime(new Date());
    });
    return saveBatch(orders);
}
```

---

## ❌ 删除操作

```java
// 根据ID删除
public boolean deleteOrder(Long id) {
    return orderMapper.deleteById(id) > 0;
}

// 条件删除
public boolean deleteByOrderNo(String orderNo) {
    return orderMapper.delete(
        new LambdaQueryWrapper<StkOrder>()
            .eq(StkOrder::getOrderNo, orderNo)
    ) > 0;
}

// 批量删除
public boolean batchDelete(List<Long> ids) {
    return orderMapper.deleteBatchIds(ids) > 0;
}
```

---

## 🔄 事务管理

> **⛔ 禁止使用 `@Transactional` 注解和 `PlatformTransactionManager` 等其他事务方式。**
> INVEST项目统一使用 `invest-common` 包中的 `TransactionUtils` 进行事务管理。

### 核心原则

- **事务范围尽可能小**：只将写操作包裹在事务中，读操作和业务逻辑放在事务外
- **禁止整方法事务**：不要把整个方法都包裹在事务中，避免长事务导致数据库连接占用过长
- **提高并发能力**：缩小事务范围可以减少锁持有时间，提升系统性能

### TransactionUtils API

```java
import group.za.bank.invest.common.utils.TransactionUtils;

// 基础用法：默认TransactionTemplate
TransactionUtils.execute(() -> {
    // 写操作代码
});

// 指定TransactionTemplate名称（多数据源场景）
TransactionUtils.execute(TransactionTemplateNameConstants.TRADE, () -> {
    // 写操作代码
});

// 指定传播机制
TransactionUtils.execute(() -> {
    // 写操作代码
}, TransactionDefinition.PROPAGATION_REQUIRES_NEW);

// 指定传播机制和隔离级别
TransactionUtils.execute(() -> {
    // 写操作代码
}, TransactionDefinition.PROPAGATION_REQUIRES_NEW, TransactionDefinition.ISOLATION_READ_COMMITTED);
```

### TransactionTemplateNameConstants

FTC域多数据源场景需要指定模板名称：

```java
import group.za.bank.invest.common.constants.TransactionTemplateNameConstants;

// 可用常量
TransactionTemplateNameConstants.TRADE    // "tradeTransactionTemplate"
TransactionTemplateNameConstants.ACCOUNT  // "accountTransactionTemplate"
TransactionTemplateNameConstants.USER     // "userTransactionTemplate"
TransactionTemplateNameConstants.CASHIO   // "cashioTransactionTemplate"
TransactionTemplateNameConstants.MARKET   // "marketTransactionTemplate"
TransactionTemplateNameConstants.ACTIVITY // "activityTransactionTemplate"
```

### SBS域示例

SBS域通常使用默认TransactionTemplate，只包裹写操作：

```java
@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private StkOrderMapper orderMapper;

    public void updateModifyOrderWithSuccess(OrderDTO orderDto) {
        // ✅ 读操作和业务逻辑在事务外
        log.info("改单成功，开始更新订单记录表");

        // ✅ 只把写操作包裹在事务中
        TransactionUtils.execute(() -> {
            orderManager.updateOrderRecord(
                orderDto.getOriginalStkOrder().getOrderNo(),
                OrderRecordOptStatusEnum.PROCESSING.getValue(),
                OrderRecordOptStatusEnum.SUCCESS.getValue()
            );
            activitySendService.sendAmendActivity(orderDto);
        });

        log.info("改单成功处理完毕");
    }
}
```

### FTC域示例

FTC域需要指定TransactionTemplate名称：

```java
@Service
public class PlaceOrderServiceImpl implements PlaceOrderService {

    @Autowired
    private TdFundOrderMapper tdFundOrderMapper;

    public void submitOrderSuccess(TdFundOrder tdFundOrder) {
        // ✅ 数据准备在事务外
        TdFundOrder target = new TdFundOrder();
        target.setStatus(FundOrderStatusEnum.SUBMIT.getDbValue());
        target.setGmtModified(new Date());

        TdFundOrder condition = new TdFundOrder();
        condition.setOrderNo(tdFundOrder.getOrderNo());

        TdFundOrderRecord record = FundOrderTransformer.initFundOrderRecord(
            tdFundOrder, FundOrderRecordOptTypeEnum.SUBMIT, RequestStatusEnum.SUCCESS
        );

        // ✅ 指定TRADE模板，只包裹写操作
        TransactionUtils.execute(TransactionTemplateNameConstants.TRADE, () -> {
            int count = tdFundOrderMapper.updateByCondition(target, condition);
            if (count < 1) {
                throw new BusinessException(TradeErrorMsgEnum.UPDATE_ORDER_STATUS_FAILED);
            }
            tdFundOrderRecordMapper.insert(record);
        });
    }
}
```

### ❌ 错误用法

```java
// ❌ 禁止使用 @Transactional
@Transactional(rollbackFor = Exception.class)
public void createOrder(OrderCreateReq req) { ... }

// ❌ 禁止使用 PlatformTransactionManager
@Autowired
private PlatformTransactionManager transactionManager;

// ❌ 禁止把整个方法逻辑都放进事务
TransactionUtils.execute(() -> {
    validateOrder(req);      // 读操作不应在事务中
    queryUserInfo(userId);   // 读操作不应在事务中
    orderMapper.insert(order);
    holdingMapper.update(holding);
    sendNotification();      // 非DB操作不应在事务中
});

// ✅ 正确：只包裹写操作
validateOrder(req);
queryUserInfo(userId);
TransactionUtils.execute(() -> {
    orderMapper.insert(order);
    holdingMapper.update(holding);
});
sendNotification();
```

---

## 📝 自定义SQL

> **⛔ 禁止使用 `@Select`、`@Insert`、`@Update`、`@Delete` 等注解方式指定SQL。**
> 查询只允许两种方式：LambdaQueryWrapper（简单查询）或 XML（复杂SQL）。

### 查询方式选择

| 场景 | 推荐方式 | 适用项目 |
|------|---------|----------|
| 单表简单查询 | LambdaQueryWrapper | SBS项目 |
| 单表条件查询 | 实体对象作为条件 | FTC项目 |
| 多表关联/聚合统计 | Mapper XML | SBS/FTC通用 |

> **SBS与FTC的查询差异**: SBS项目使用Mybatis-Plus的LambdaQueryWrapper，FTC项目使用实体对象作为查询条件。详见 `invest-dao-spec` 技能文档。

### SBS项目 - LambdaQueryWrapper（简单查询优先）

```java
// ✅ 简单查询用LambdaQueryWrapper
public List<StkOrder> selectByUserIdAndStatus(String userId, String status) {
    return orderMapper.selectList(
        new LambdaQueryWrapper<StkOrder>()
            .eq(StkOrder::getUserId, userId)
            .eq(StkOrder::getStatus, status)
    );
}
```

### FTC项目 - 实体对象查询

```java
// ✅ FTC使用实体对象作为查询条件
TdFundOrder condition = new TdFundOrder();
condition.setBankUserId(bankUserId);
condition.setStatus(status);
List<TdFundOrder> orders = orderMapper.selectList(condition);
```

### 复杂查询 - Mapper XML

```java
// Mapper接口只声明方法，SQL写在XML中
@Mapper
public interface StkOrderMapper extends BaseMapper<StkOrder> {

    List<OrderStatDTO> queryOrderStatistics(
        @Param("startDate") Date startDate,
        @Param("endDate") Date endDate
    );
}
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="group.za.bank.sbs.trade.mapper.StkOrderMapper">

    <select id="queryOrderStatistics" 
            resultType="group.za.bank.sbs.trade.model.dto.OrderStatDTO">
        SELECT 
            DATE(create_time) as tradeDate,
            COUNT(*) as orderCount,
            SUM(entrust_amount) as totalAmount
        FROM stk_order
        WHERE create_time BETWEEN #{startDate} AND #{endDate}
        GROUP BY DATE(create_time)
        ORDER BY tradeDate DESC
    </select>

</mapper>
```

### ❌ 错误用法

```java
// ❌ 禁止使用注解方式指定SQL
@Select("SELECT * FROM stk_order WHERE user_id = #{userId}")
List<StkOrder> selectByUserId(@Param("userId") String userId);

@Insert("INSERT INTO stk_order ...")
int insertOrder(StkOrder order);
```

---

## ⚠️ 注意事项

1. **事务管理**: 统一使用 `TransactionUtils`，禁止 `@Transactional` 和 `PlatformTransactionManager`
2. **事务范围**: 事务只包裹写操作代码块，读操作和非DB操作放在事务外
3. **SQL定义**: 禁止使用 `@Select` 等注解，简单查询用 LambdaQueryWrapper/实体条件，复杂SQL用 XML
4. **SBS/FTC差异**: SBS用LambdaQueryWrapper，FTC用实体对象条件查询，详见 `invest-dao-spec`
5. **分页插件**: 确保配置了MyBatis-Plus分页插件
6. **SQL注入**: 使用参数化查询，避免SQL注入
7. **慢查询**: 大表查询必须使用索引，避免全表扫描
8. **连接池**: 合理配置连接池参数，避免连接泄漏
