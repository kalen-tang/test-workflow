---
name: invest-exception-spec
description: INVEST框架异常处理完整规范。当处理业务异常、设计错误码、实现异常处理机制、统一异常响应时使用。包含BusinessException使用、ResourceHandler接口、错误码枚举设计等内容。
---

# INVEST异常处理规范

INVEST框架提供了完整的异常处理机制，包括业务异常类、错误码规范和国际化支持。本规范定义了异常处理的标准和最佳实践。

## 异常基类

### BusinessException - 业务异常

```java
@Getter
public class BusinessException extends RuntimeException {
    private static final long serialVersionUID = 4471873950276682007L;

    private String code;

    /**
     * 使用错误码和消息构造异常
     * 注意：msg需要国际化
     */
    public BusinessException(String code, String msg) {
        super(msg);
        this.code = code;
    }

    /**
     * 使用ResourceHandler枚举构造异常
     * 自动获取国际化消息
     */
    public BusinessException(ResourceHandler resourceHandler) {
        super(resourceHandler.getMsg(UserUtil.getLanguage()));
        this.code = resourceHandler.getCode();
    }

    /**
     * 使用ResourceHandler枚举和参数构造异常
     * 支持消息模板参数替换
     */
    public BusinessException(ResourceHandler resourceHandler, String... param) {
        super(MessageFormat.format(
            resourceHandler.getMsg(UserUtil.getLanguage()), 
            param
        ));
        this.code = resourceHandler.getCode();
    }
}
```

## 抛出异常的方式

### 1. 直接使用错误码和消息

```java
// 简单的业务异常
if (order == null) {
    throw new BusinessException("ORD001", "订单不存在");
}

if (balance.compareTo(amount) < 0) {
    throw new BusinessException("ACC001", "账户余额不足");
}
```

### 2. 使用ResourceHandler枚举（推荐）

```java
// 使用枚举定义的错误
if (order == null) {
    throw new BusinessException(OrderErrorMsgEnum.ORDER_NOT_FOUND);
}

// 带参数的错误消息
if (isExceedLimit(order)) {
    throw new BusinessException(
        OrderErrorMsgEnum.EXCEED_LIMIT, 
        order.getStockCode()
    );
}
```

### 3. 使用通用错误枚举

```java
// 系统错误
throw new BusinessException(CommonErrorMsgEnum.SYSTEM_ERROR);

// 参数错误
throw new BusinessException(CommonErrorMsgEnum.PARAM_ERROR);

// 不在交易时间
throw new BusinessException(CommonErrorMsgEnum.NOT_TRADING_TIME);
```

## 错误码枚举设计

### ResourceHandler接口

```java
public interface ResourceHandler {
    /**
     * 获取错误码
     */
    String getCode();
    
    /**
     * 获取国际化消息
     */
    String getMsg(String language);
}
```

### 错误码枚举示例

```java
@Getter
@AllArgsConstructor
public enum OrderErrorMsgEnum implements ResourceHandler {
    
    ORDER_NOT_FOUND("ORD001", "订单不存在", "Order not found"),
    ORDER_STATUS_ERROR("ORD002", "订单状态异常", "Order status error"),
    EXCEED_LIMIT("ORD003", "股票{0}超出限额", "Stock {0} exceeds limit"),
    INSUFFICIENT_QTY("ORD004", "可用数量不足", "Insufficient quantity"),
    ORDER_EXPIRED("ORD005", "订单已过期", "Order expired"),
    DUPLICATE_ORDER("ORD006", "重复下单", "Duplicate order"),
    ;

    private final String code;
    private final String msgCn;
    private final String msgEn;

    @Override
    public String getMsg(String language) {
        if ("en".equalsIgnoreCase(language)) {
            return msgEn;
        }
        return msgCn;
    }
}
```

### 通用错误码枚举

```java
@Getter
@AllArgsConstructor
public enum CommonErrorMsgEnum implements ResourceHandler {
    
    SUCCESS("0000", "成功", "Success"),
    SYSTEM_ERROR("9999", "系统繁忙，请稍后重试", "System busy, please try again"),
    PARAM_ERROR("9001", "参数错误", "Parameter error"),
    DATA_NOT_FOUND("9002", "数据不存在", "Data not found"),
    PERMISSION_DENIED("9003", "权限不足", "Permission denied"),
    NOT_TRADING_TIME("9004", "非交易时间", "Not trading time"),
    REPEAT_REQUEST("9005", "重复请求", "Repeat request"),
    ;

    private final String code;
    private final String msgCn;
    private final String msgEn;

    @Override
    public String getMsg(String language) {
        if ("en".equalsIgnoreCase(language)) {
            return msgEn;
        }
        return msgCn;
    }
}
```

## 异常处理最佳实践

### Service层异常处理

```java
@Slf4j
@Service
public class OrderServiceImpl implements OrderService {

    @Override
    public OrderResp getOrderDetail(String orderNo) {
        // 1. 参数校验
        if (StringUtils.isBlank(orderNo)) {
            throw new BusinessException(CommonErrorMsgEnum.PARAM_ERROR);
        }

        // 2. 查询数据
        StkOrder order = orderMapper.selectOne(
            new LambdaQueryWrapper<StkOrder>()
                .eq(StkOrder::getOrderNo, orderNo)
        );

        // 3. 数据校验
        if (order == null) {
            throw new BusinessException(OrderErrorMsgEnum.ORDER_NOT_FOUND);
        }

        // 4. 权限校验
        if (!hasPermission(order)) {
            throw new BusinessException(CommonErrorMsgEnum.PERMISSION_DENIED);
        }

        return convertToResp(order);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public OrderResp createOrder(OrderCreateReq req) {
        try {
            // 业务处理...
            return doCreateOrder(req);
            
        } catch (BusinessException e) {
            // 业务异常直接抛出
            log.warn("创建订单失败: {}", e.getMessage());
            throw e;
            
        } catch (Exception e) {
            // 系统异常转换为业务异常
            log.error("创建订单异常", e);
            throw new BusinessException(CommonErrorMsgEnum.SYSTEM_ERROR);
        }
    }
}
```

### 调用远程服务的异常处理

```java
public AccountInfo getAccountInfo(String userId) {
    try {
        ResponseData<AccountInfo> response = accountFeignClient.getAccount(userId);
        
        if (!response.judgeSuccess()) {
            log.warn("获取账户信息失败: code={}, msg={}", 
                     response.getCode(), response.getMsg());
            throw new BusinessException(response.getCode(), response.getMsg());
        }
        
        return response.getValue();
        
    } catch (FeignException e) {
        log.error("调用账户服务异常", e);
        throw new BusinessException("ACC999", "账户服务暂时不可用");
    }
}
```

## 错误码规范

### 错误码格式

| 类型 | 格式 | 示例 | 说明 |
|------|------|------|------|
| 成功 | 0000 | 0000 | 所有成功响应 |
| 系统错误 | 9xxx | 9999, 9001 | 通用系统级错误 |
| 业务错误 | XXXnnn | ORD001, ACC002 | 业务模块错误 |

### 业务模块前缀

| 前缀 | 模块 | 示例 |
|------|------|------|
| ORD | 订单 | ORD001 |
| ACC | 账户 | ACC001 |
| HLD | 持仓 | HLD001 |
| TRD | 交易 | TRD001 |
| USR | 用户 | USR001 |

## 异常日志规范

```java
// 业务异常 - 使用warn级别
catch (BusinessException e) {
    log.warn("业务处理失败: userId={}, code={}, msg={}", 
             userId, e.getCode(), e.getMessage());
    throw e;
}

// 系统异常 - 使用error级别
catch (Exception e) {
    log.error("系统异常: userId={}", userId, e);
    throw new BusinessException(CommonErrorMsgEnum.SYSTEM_ERROR);
}
```

## 全局异常处理器

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    /**
     * 处理业务异常
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseData<Void> handleBusinessException(BusinessException e) {
        log.warn("业务异常: code={}, msg={}", e.getCode(), e.getMessage());
        return ResponseData.builder()
            .code(e.getCode())
            .msg(e.getMessage())
            .build();
    }

    /**
     * 处理参数校验异常
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseData<Void> handleValidationException(
            MethodArgumentNotValidException e) {
        String message = e.getBindingResult().getFieldErrors().stream()
            .map(FieldError::getDefaultMessage)
            .collect(Collectors.joining(", "));
        
        log.warn("参数校验失败: {}", message);
        return ResponseData.builder()
            .code(CommonErrorMsgEnum.PARAM_ERROR.getCode())
            .msg(message)
            .build();
    }

    /**
     * 处理其他异常
     */
    @ExceptionHandler(Exception.class)
    public ResponseData<Void> handleException(Exception e) {
        log.error("系统异常", e);
        return ResponseData.builder()
            .code(CommonErrorMsgEnum.SYSTEM_ERROR.getCode())
            .msg(CommonErrorMsgEnum.SYSTEM_ERROR.getMsgCn())
            .build();
    }
}
```
