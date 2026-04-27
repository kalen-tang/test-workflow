---
name: invest-controller-spec
description: INVEST框架Controller层完整开发规范。当编写Controller、处理HTTP请求响应、实现RESTful API、处理分页查询时使用。包含ResponseData规范、分页处理、Swagger注解等核心内容。
---

# INVEST Controller层开发规范

INVEST框架Controller层负责接收HTTP请求、协调业务处理、返回标准化响应。本规范定义了Controller层的开发标准和最佳实践。

## 快速开始

基本Controller实现:
```java
/**
 * 股票订单
 */
@RestController
@RequestMapping(value = "/sbs-trade/normal/order")
@Validated
@Slf4j
public class OrderController {

    @Autowired
    private OrderService orderService;

    @ApiOperation(value = "股票下单")
    @PostMapping(value = "/entrust", 
                 consumes = MediaType.APPLICATION_JSON_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseData<EntrustOrderResp> entrust(@Valid @RequestBody EntrustOrderReq req) {
        log.info("用户申购股票：参数为：{}", JsonUtils.toJsonString(req));
        EntrustOrderResp resp = orderService.entrust(req);
        return ResponseUtil.success(resp);
    }
}
```

## 核心规范

### 1. Controller命名和注解规范

- **类名**: 以Controller结尾，如`OrderController`、`HoldingController`
- **包路径**: 位于`web.controller`包下
- **必须注解**: `@RestController`、`@RequestMapping`、`@Validated`

```java
/**
 * 股票订单
 */
@RestController
@RequestMapping(value = "/sbs-trade/normal/order")
@Validated
@Slf4j
public class OrderController {
    // Controller实现
}
```

### 2. 方法注解配置

- **HTTP方法**: 全部接口必须使用POST方法, 禁止使用GET、PUT、DELETE等方法

Controller方法必须配置以下属性：

```java
@ApiOperation(value = "股票下单")
@PostMapping(value = "/entrust",
             consumes = MediaType.APPLICATION_JSON_VALUE,
             produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseData<EntrustOrderResp> entrust(
        @Valid @RequestBody EntrustOrderReq req) {
    // 实现逻辑
}
```

### 3. 请求参数校验

使用JSR-380校验注解：

```java
public ResponseData<OrderResp> createOrder(
        @Valid @RequestBody OrderCreateReq req) {
    // @Valid 触发参数校验
}
```

## ResponseData响应规范

### 响应结构

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ResponseData<T> implements Serializable {
    /**
     * 响应码 - 以"0000"结尾表示成功
     */
    private String code;
    
    /**
     * 响应信息
     */
    private String msg;
    
    /**
     * 返回的业务数据
     */
    private T value;
    
    /**
     * 服务器当前时间
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date serverTime;
    
    /**
     * 判断是否成功
     */
    @JsonProperty("success")
    public boolean judgeSuccess() {
        return SUCCESS_END_CODE.equals(code) || 
               (code != null && code.endsWith(SUCCESS_END_CODE));
    }
}
```

### 响应工具类 ResponseUtil

```java
// 成功响应
ResponseUtil.success(data);

// 带消息的成功响应
ResponseUtil.success("操作成功", data);

// 错误响应
ResponseUtil.error("错误码", "错误信息");
```

## 分页查询规范

### 分页请求

继承`BasePageReq`：

```java
@Setter
@Getter
@ToString(callSuper = true)
public class OrderQueryReq extends BasePageReq {
    
    /**
     * 订单状态
     */
    private String status;
    
    /**
     * 股票代码
     */
    private String stockCode;
}
```

BasePageReq提供的字段：
```java
public class BasePageReq extends BaseReq {
    @Min(value = 1, message = "页数必须大于0")
    @NotNull(message = "pageNum cant not null")
    protected Integer pageNum = 1;

    @Min(value = 1, message = "页面记录数必须大于0")
    @NotNull(message = "pageSize cant not null")
    protected Integer pageSize = 20;

    @Length(min = 0, max = 50, message = "排序字符串过长")
    protected String orderBy;

    @Pattern(regexp = "desc|asc|DESC|ASC")
    protected String orderName;
}
```

### 分页响应

使用`PageInfoResp`：

```java
@PostMapping("/list")
public ResponseData<PageInfoResp<OrderResp>> queryOrders(
        @Valid @RequestBody OrderQueryReq req) {
    PageInfoResp<OrderResp> pageResp = orderService.queryOrders(req);
    return ResponseUtil.success(pageResp);
}
```

PageInfoResp结构：
```java
public class PageInfoResp<T> {
    private Integer pageNum;     // 页码
    private Integer pageSize;    // 每页条数
    private Long total;          // 总条数
    private List<T> list;        // 数据列表
}
```

## Feign服务实现

### Feign Controller

用于实现服务间调用的接口：

```java
/**
 * 订单Feign接口
 */
@RestController
@RequestMapping("/feign/order")
@Validated
@Slf4j
public class OrderFeignController implements OrderFeignApi {

    @Autowired
    private OrderService orderService;

    @Override
    @PostMapping("/info")
    public ResponseData<OrderInfoResp> getOrderInfo(
            @Valid @RequestBody OrderInfoReq req) {
        OrderInfoResp resp = orderService.getOrderInfo(req);
        return ResponseUtil.success(resp);
    }
}
```

## 日志规范

```java
@PostMapping("/entrust")
public ResponseData<EntrustResp> entrust(@Valid @RequestBody EntrustReq req) {
    // 入参日志
    log.info("用户申购股票：参数为：{}", JsonUtils.toJsonString(req));
    
    EntrustResp resp = orderService.entrust(req);
    
    // 结果日志
    log.info("用户下单成功. userId:{}, orderId:{}", 
             req.getBankUserId(), resp.getOrderNo());
    
    return ResponseUtil.success(resp);
}
```

## 完整Controller示例

```java
/**
 * 股票订单
 */
@RestController
@RequestMapping(value = "/sbs-trade/normal/order")
@Validated
@Slf4j
public class OrderController {

    @Autowired
    private OrderService orderService;

    @ApiOperation(value = "股票下单")
    @PostMapping(value = "/entrust",
                 consumes = MediaType.APPLICATION_JSON_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseData<EntrustOrderResp> entrust(
            @Valid @RequestBody EntrustOrderReq req) {
        log.info("用户申购股票：参数为：{}", JsonUtils.toJsonString(req));
        
        EntrustOrderResp resp = orderService.entrust(req);
        
        log.info("用户下单成功. userId:{}, orderId:{}", 
                 req.getBankUserId(), resp.getOrderNo());
        
        return ResponseUtil.success(resp);
    }

    @ApiOperation(value = "订单分页查询")
    @PostMapping(value = "/list",
                 consumes = MediaType.APPLICATION_JSON_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseData<PageInfoResp<OrderResp>> queryOrders(
            @Valid @RequestBody OrderQueryReq req) {
        log.info("订单分页查询：参数为：{}", JsonUtils.toJsonString(req));
        
        PageInfoResp<OrderResp> pageResp = orderService.queryOrders(req);
        
        return ResponseUtil.success(pageResp);
    }

    @ApiOperation(value = "撤销订单")
    @PostMapping(value = "/cancel",
                 consumes = MediaType.APPLICATION_JSON_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseData<CancelOrderResp> cancelOrder(
            @Valid @RequestBody CancelOrderReq req) {
        log.info("撤销订单：参数为：{}", JsonUtils.toJsonString(req));
        
        CancelOrderResp resp = orderService.cancelOrder(req);
        
        return ResponseUtil.success(resp);
    }
}
```
