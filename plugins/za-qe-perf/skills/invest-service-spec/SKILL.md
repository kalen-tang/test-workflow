---
name: invest-service-spec
description: INVEST框架Service层完整开发规范。当编写业务逻辑、设计服务接口、实现业务方法、处理事务时使用。包含Service接口设计、ServiceImpl实现、Manager层使用、TransactionUtils事务管理等内容。禁止使用@Transactional注解。
---

# INVEST Service层开发规范

INVEST框架Service层是业务逻辑的核心，负责实现具体的业务规则和流程。本规范定义了Service层的设计原则和开发标准。

## 核心规范

### 1. Service命名和组织规范

- **接口名**: 以Service结尾，如`OrderService`、`HoldingService`
- **实现类名**: 以ServiceImpl结尾，如`OrderServiceImpl`
- **包路径**: 接口位于`service`包，实现类位于`service.impl`包

```java
// Service接口
public interface OrderService {
    OrderDTO entrust(OrderDTO orderDto);
    PageInfoResp<OrderResp> queryOrders(OrderQueryReq req);
}

// Service实现类
@Slf4j
@Service
public class OrderServiceImpl implements OrderService {
    // 业务逻辑实现
}
```

### 2. Service与Manager的职责划分

INVEST框架采用Service + Manager的双层业务逻辑设计：

**Service层**:
- 面向Controller的业务接口
- 处理简单的业务逻辑
- 协调多个Manager完成复杂业务

**Manager层**:
- 可复用的业务逻辑单元
- 封装特定领域的业务操作
- 被多个Service共享调用

```java
// Manager层
@Component
@Slf4j
public class OrderManager {
    
    @Autowired
    private StkOrderMapper orderMapper;
    
    public StkOrder getOrderByOrderNo(String orderNo) {
        return orderMapper.selectOne(
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getOrderNo, orderNo)
        );
    }
}

// Service层调用Manager
@Service
public class OrderServiceImpl implements OrderService {
    
    @Autowired
    private OrderManager orderManager;
    
    @Override
    public OrderResp getOrderDetail(String orderNo) {
        StkOrder order = orderManager.getOrderByOrderNo(orderNo);
        return convertToResp(order);
    }
}
```

## Service层设计模式

### 1. 标准Service实现

```java
@Slf4j
@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private StkOrderMapper orderMapper;

    @Autowired
    private OrderManager orderManager;

    @Autowired
    private HoldingService holdingService;

    @Override
    public OrderDTO entrust(OrderDTO orderDto) {
        log.info("委托下单开始: userId={}, stockCode={}", 
                 orderDto.getUserId(), orderDto.getStockCode());

        // 1. 参数校验（事务外）
        validateEntrustRequest(orderDto);

        // 2. 业务规则校验（事务外）
        checkTradingTime(orderDto.getMarketCode());
        checkUserPermission(orderDto.getUserId());

        // 3. 构建订单实体（事务外）
        StkOrder stkOrder = buildStkOrder(orderDto);

        // 4. 只把写操作包裹在事务中
        TransactionUtils.execute(() -> {
            orderMapper.insert(stkOrder);
        });

        // 5. 后置处理（事务外）
        sendOrderNotification(stkOrder);

        // 6. 返回结果
        orderDto.setOrderNo(stkOrder.getOrderNo());
        log.info("委托下单成功: orderNo={}", stkOrder.getOrderNo());

        return orderDto;
    }

    @Override
    public PageInfoResp<OrderResp> queryOrders(OrderQueryReq req) {
        log.info("分页查询订单: {}", req);

        // 构建分页对象
        Page<StkOrder> page = new Page<>(req.getPageNum(), req.getPageSize());

        // 构建查询条件
        LambdaQueryWrapper<StkOrder> queryWrapper = buildQueryWrapper(req);

        // 执行分页查询（纯读操作无需事务）
        IPage<StkOrder> poPage = orderMapper.selectPage(page, queryWrapper);

        // 转换为响应DTO
        return buildPageResp(poPage);
    }
}
```

### 2. 事务管理

> **⛔ 禁止使用 `@Transactional` 注解、`PlatformTransactionManager` 等其他事务方式。**
> INVEST项目统一使用 `invest-common` 包中的 `TransactionUtils` 进行编程式事务管理。

#### 核心原则

- **事务范围尽可能小**：只将写操作包裹在事务中，读操作和业务逻辑放在事务外
- **禁止整方法事务**：不要把整个方法都包裹在事务中，避免长事务导致数据库连接占用过长
- **提高并发能力**：缩小事务范围可以减少锁持有时间，提升系统性能

#### TransactionUtils API

```java
import group.za.bank.invest.common.utils.TransactionUtils;

// 基础用法：默认TransactionTemplate（SBS域常用）
TransactionUtils.execute(() -> {
    // 写操作代码
});

// 指定TransactionTemplate名称（FTC域多数据源场景）
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

#### SBS域示例

SBS域通常使用默认TransactionTemplate，只包裹写操作：

```java
@Service
public class OrderServiceImpl implements OrderService {

    @Autowired
    private OrderManager orderManager;

    private void updateModifyOrderWithSuccess(OrderDTO orderDto) {
        // ✅ 日志和读操作在事务外
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

#### FTC域示例

FTC域需要指定TransactionTemplate名称：

```java
import group.za.bank.invest.common.constants.TransactionTemplateNameConstants;

@Service
public class FundClearServiceImpl implements FundClearService {

    private HandleCapitalResp handleBuyFailRefund(TdFundOrder tdFundOrder) {
        // ✅ 指定TRADE模板，只包裹写操作
        TransactionUtils.execute(TransactionTemplateNameConstants.TRADE, () -> {
            this.rollBackOrderRefund(tdFundOrder.getOrderNo());
            this.rollBackCoinBusiness(tdFundOrder);
        });

        // ✅ 非DB操作放在事务外
        HandleCapitalResp resp = new HandleCapitalResp();
        resp.setResult(RespResultEnum.SUCCESS.getValue());
        return resp;
    }
}
```

#### ❌ 错误用法

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

### 3. 异常处理

使用`BusinessException`抛出业务异常：

```java
@Override
public OrderDTO entrust(OrderDTO orderDto) {
    // 使用错误码和消息
    if (orderDto.getEntrustQty() <= 0) {
        throw new BusinessException("ORD001", "委托数量必须大于0");
    }

    // 使用ResourceHandler枚举
    if (!isTradingTime()) {
        throw new BusinessException(CommonErrorMsgEnum.NOT_TRADING_TIME);
    }

    // 带参数的异常消息
    if (isExceedLimit(orderDto)) {
        throw new BusinessException(
            OrderErrorMsgEnum.EXCEED_LIMIT, 
            orderDto.getStockCode()
        );
    }
}
```

## Manager层规范

### Manager命名和职责

```java
@Component
@Slf4j
public class OrderManager {

    @Autowired
    private StkOrderMapper orderMapper;

    /**
     * 根据订单号获取订单
     */
    public StkOrder getOrderByOrderNo(String orderNo) {
        return orderMapper.selectOne(
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getOrderNo, orderNo)
        );
    }

    /**
     * 获取用户今日订单
     */
    public List<StkOrder> getUserTodayOrders(String userId) {
        Date today = DateUtils.getToday();
        return orderMapper.selectList(
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getUserId, userId)
                .ge(StkOrder::getCreateTime, today)
        );
    }

    /**
     * 更新订单状态
     */
    public boolean updateOrderStatus(String orderNo, String status) {
        StkOrder update = new StkOrder();
        update.setStatus(status);
        update.setUpdateTime(new Date());
        
        int rows = orderMapper.update(update,
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getOrderNo, orderNo)
        );
        return rows > 0;
    }
}
```

### 缓存管理

> **缓存完整规范请参考 `invest-cache-guide` skill**，包含 RedissonClient 操作、Key 枚举设计、分布式锁、缓存模式等详细内容。

INVEST 项目使用 **RedissonClient**（非 CacheService）进行缓存操作，Key 统一通过 `RedisCacheKeyBuilder` 枚举管理：

```java
import org.redisson.api.RedissonClient;
import java.util.concurrent.TimeUnit;

@Component
@Slf4j
public class OrderCacheManager {

    @Resource
    private RedissonClient redissonClient;

    public StkOrder getOrderFromCache(String orderNo) {
        String key = RedisCacheKeyEnum.TODAY_ORDER.key(orderNo);
        return redissonClient.<StkOrder>getBucket(key).get();
    }

    public void setOrderToCache(StkOrder order) {
        String key = RedisCacheKeyEnum.TODAY_ORDER.key(order.getOrderNo());
        redissonClient.<StkOrder>getBucket(key).set(order, 3600, TimeUnit.SECONDS);
    }

    public void removeOrderFromCache(String orderNo) {
        String key = RedisCacheKeyEnum.TODAY_ORDER.key(orderNo);
        redissonClient.getBucket(key).delete();
    }
}
```

## 远程服务调用

### Feign客户端调用

```java
@Service
@Slf4j
public class OrderServiceImpl implements OrderService {

    @Autowired
    private AccountFeignClient accountFeignClient;

    @Override
    public OrderDTO entrust(OrderDTO orderDto) {
        // 调用账户服务检查余额
        ResponseData<AccountBalanceResp> balanceResp = 
            accountFeignClient.getBalance(
                new AccountBalanceReq(orderDto.getUserId())
            );
        
        if (!balanceResp.judgeSuccess()) {
            throw new BusinessException("ACC001", "获取账户余额失败");
        }
        
        if (balanceResp.getValue().getAvailableBalance()
                .compareTo(orderDto.getAmount()) < 0) {
            throw new BusinessException("ACC002", "账户余额不足");
        }
        
        // 继续订单处理...
    }
}
```

## 分页查询实现

```java
@Override
public PageInfoResp<OrderResp> queryOrders(OrderQueryReq req) {
    // 1. 构建分页对象
    Page<StkOrder> page = new Page<>(req.getPageNum(), req.getPageSize());

    // 2. 构建查询条件
    LambdaQueryWrapper<StkOrder> wrapper = new LambdaQueryWrapper<>();
    wrapper.eq(StkOrder::getUserId, req.getBankUserId());
    
    if (StringUtils.isNotBlank(req.getStatus())) {
        wrapper.eq(StkOrder::getStatus, req.getStatus());
    }
    if (StringUtils.isNotBlank(req.getStockCode())) {
        wrapper.eq(StkOrder::getStockCode, req.getStockCode());
    }
    
    // 排序
    wrapper.orderByDesc(StkOrder::getCreateTime);

    // 3. 执行查询
    IPage<StkOrder> poPage = orderMapper.selectPage(page, wrapper);

    // 4. 转换响应
    List<OrderResp> respList = poPage.getRecords().stream()
        .map(this::convertToResp)
        .collect(Collectors.toList());

    return new PageInfoResp<OrderResp>()
        .pageNum(req.getPageNum())
        .pageSize(req.getPageSize())
        .total(poPage.getTotal())
        .list(respList);
}
```

## 日志规范

```java
@Slf4j
@Service
public class OrderServiceImpl implements OrderService {

    @Override
    public OrderDTO entrust(OrderDTO orderDto) {
        // 方法入口日志
        log.info("委托下单开始: userId={}, stockCode={}, qty={}", 
                 orderDto.getUserId(), 
                 orderDto.getStockCode(),
                 orderDto.getEntrustQty());
        
        try {
            // 业务处理...
            
            // 成功日志
            log.info("委托下单成功: orderNo={}", orderDto.getOrderNo());
            return orderDto;
            
        } catch (BusinessException e) {
            // 业务异常日志
            log.warn("委托下单失败: userId={}, reason={}", 
                     orderDto.getUserId(), e.getMessage());
            throw e;
            
        } catch (Exception e) {
            // 系统异常日志
            log.error("委托下单异常: userId={}", orderDto.getUserId(), e);
            throw new BusinessException("SYS001", "系统繁忙，请稍后重试");
        }
    }
}
```
