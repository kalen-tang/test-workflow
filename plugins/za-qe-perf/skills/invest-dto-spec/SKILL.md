---
name: invest-dto-spec
description: INVEST框架DTO设计完整规范。当设计数据传输对象、处理分页查询、定义API参数、进行数据转换等DTO时使用。包含BaseReq继承、分页DTO、请求响应DTO设计、DTO映射等核心内容。
---

# INVEST DTO设计规范

INVEST框架DTO（Data Transfer Object）负责在不同层之间传输数据，提供标准化的数据传输对象设计。本规范定义了DTO的设计原则和开发标准。

## 核心规范

### 1. DTO命名和继承规范

- **类名**: 以Req/Resp结尾，如`OrderCreateReq`、`OrderResp`
- **包路径**: 位于`model.req`和`model.resp`包下
- **继承关系**: 请求DTO继承`BaseReq`或`BasePageReq`
- **分类**: 按用途分为Request、Response、Page等类型

```java
// 普通请求DTO - 继承BaseReq
public class OrderCreateReq extends BaseReq {
    // 请求参数
}

// 分页请求DTO - 继承BasePageReq
public class OrderQueryReq extends BasePageReq {
    // 查询条件 + 分页参数
}

// 响应DTO - 继承BaseResp或直接定义
public class OrderResp extends BaseResp {
    // 响应数据
}
```

## BaseReq基础规范

### BaseReq结构

```java
@Getter
@Setter
@ToString
public class BaseReq implements Serializable {
    private static final long serialVersionUID = 3725515402781229512L;

    /**
     * 银行用户userId
     */
    public String bankUserId;

    /**
     * userId类型
     */
    public String fromType;

    /**
     * 账户类型
     */
    private String accountType;
}
```

### BasePageReq分页请求

```java
@Setter
@Getter
@NoArgsConstructor
@ToString(callSuper = true)
public class BasePageReq extends BaseReq {
    
    /**
     * 页码
     **/
    @Min(value = 1, message = "页数必须大于0")
    @NotNull(message = "pageNum cant not null")
    protected Integer pageNum = 1;

    /**
     * 每页条数
     **/
    @Min(value = 1, message = "页面记录数必须大于0")
    @NotNull(message = "pageSize cant not null")
    protected Integer pageSize = 20;

    /**
     * 排序字段
     **/
    @Length(min = 0, max = 50, message = "排序字符串过长")
    protected String orderBy;

    /**
     * 排序方向
     **/
    @Pattern(regexp = "desc|asc|DESC|ASC")
    protected String orderName;
}
```

## DTO分类设计

### 1. 请求DTO (Request)

用于接收客户端请求参数：

```java
@Data
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public class OrderCreateReq extends BaseReq {

    @NotBlank(message = "股票代码不能为空")
    private String stockCode;

    @NotNull(message = "委托价格不能为空")
    @DecimalMin(value = "0.01", message = "委托价格必须大于0")
    private BigDecimal entrustPrice;

    @NotNull(message = "委托数量不能为空")
    @Min(value = 1, message = "委托数量必须大于0")
    private Integer entrustQty;

    @NotBlank(message = "市场代码不能为空")
    @Pattern(regexp = "HK|US", message = "市场代码只能是HK或US")
    private String marketCode;

    @NotBlank(message = "委托类型不能为空")
    private String entrustType;

    private String orderProp;
}
```

### 2. 分页查询请求DTO

```java
@Data
@EqualsAndHashCode(callSuper = true)
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

    /**
     * 市场代码
     */
    private String marketCode;

    /**
     * 开始日期
     */
    @JsonFormat(pattern = "yyyy-MM-dd")
    private Date startDate;

    /**
     * 结束日期
     */
    @JsonFormat(pattern = "yyyy-MM-dd")
    private Date endDate;
}
```

### 3. 响应DTO (Response)

用于返回业务数据给客户端：

```java
@Data
public class OrderResp implements Serializable {
    private static final long serialVersionUID = 1L;

    /**
     * 订单号
     */
    private String orderNo;

    /**
     * 股票代码
     */
    private String stockCode;

    /**
     * 股票名称
     */
    private String stockName;

    /**
     * 委托价格
     */
    private BigDecimal entrustPrice;

    /**
     * 委托数量
     */
    private BigDecimal entrustQty;

    /**
     * 委托金额
     */
    private BigDecimal entrustAmount;

    /**
     * 订单状态
     */
    private String status;

    /**
     * 状态描述
     */
    private String statusDesc;

    /**
     * 创建时间
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;
}
```

## 分页响应规范

### PageInfoResp结构

```java
@NoArgsConstructor
@AllArgsConstructor
public class PageInfoResp<T> {
    
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Integer pageNum;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Integer pageSize;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING)
    private Long total;
    
    private List<T> list;

    // 链式调用方法
    public PageInfoResp<T> pageNum(Integer pageNum) {
        this.pageNum = pageNum;
        return this;
    }

    public PageInfoResp<T> pageSize(Integer pageSize) {
        this.pageSize = pageSize;
        return this;
    }

    public PageInfoResp<T> total(Long total) {
        this.total = total;
        return this;
    }

    public PageInfoResp<T> list(List<T> list) {
        this.list = list;
        return this;
    }

    // 空分页响应
    public static <E> PageInfoResp<E> emptyPageResponse(BasePageReq page) {
        return new PageInfoResp<>(
            page.getPageNum(), 
            page.getPageSize(), 
            0L, 
            Collections.emptyList()
        );
    }
}
```

### 分页响应构建

```java
// 从MyBatis-Plus IPage构建
public PageInfoResp<OrderResp> buildPageResp(IPage<StkOrder> poPage) {
    List<OrderResp> respList = poPage.getRecords().stream()
        .map(this::convertToResp)
        .collect(Collectors.toList());

    return new PageInfoResp<OrderResp>()
        .pageNum((int) poPage.getCurrent())
        .pageSize((int) poPage.getSize())
        .total(poPage.getTotal())
        .list(respList);
}

// 空数据返回
if (CollectionUtils.isEmpty(orders)) {
    return PageInfoResp.emptyPageResponse(req);
}
```

## 参数校验注解

### 常用校验注解

```java
// 非空校验
@NotNull(message = "字段不能为null")
@NotBlank(message = "字符串不能为空")  // 字符串专用
@NotEmpty(message = "集合不能为空")    // 集合专用

// 长度校验
@Size(min = 1, max = 50, message = "长度必须在1-50之间")
@Length(min = 1, max = 50, message = "长度必须在1-50之间")

// 数值校验
@Min(value = 1, message = "必须大于等于1")
@Max(value = 100, message = "必须小于等于100")
@DecimalMin(value = "0.01", message = "必须大于0")
@DecimalMax(value = "999999.99", message = "超出最大值")

// 格式校验
@Pattern(regexp = "^[A-Z]{2}$", message = "格式不正确")
@Email(message = "邮箱格式不正确")

// 范围校验
@Range(min = 1, max = 100, message = "必须在1-100之间")
```

### 校验示例

```java
@Data
@EqualsAndHashCode(callSuper = true)
public class OrderCreateReq extends BaseReq {

    @NotBlank(message = "股票代码不能为空")
    @Size(max = 20, message = "股票代码长度不能超过20")
    private String stockCode;

    @NotNull(message = "委托价格不能为空")
    @DecimalMin(value = "0.001", message = "委托价格必须大于0")
    @Digits(integer = 10, fraction = 4, message = "价格格式不正确")
    private BigDecimal entrustPrice;

    @NotNull(message = "委托数量不能为空")
    @Min(value = 1, message = "委托数量必须大于0")
    private Integer entrustQty;

    @NotBlank(message = "市场代码不能为空")
    @Pattern(regexp = "HK|US|SH|SZ", message = "不支持的市场代码")
    private String marketCode;
}
```

## DTO转换规范

### 使用MapStruct

```java
@Mapper(componentModel = "spring")
public interface OrderConverter {

    OrderResp toResp(StkOrder entity);

    List<OrderResp> toRespList(List<StkOrder> entityList);

    StkOrder toEntity(OrderCreateReq req);
}
```

### 手动转换

```java
private OrderResp convertToResp(StkOrder order) {
    OrderResp resp = new OrderResp();
    resp.setOrderNo(order.getOrderNo());
    resp.setStockCode(order.getStockCode());
    resp.setStockName(order.getStockName());
    resp.setEntrustPrice(order.getEntrustPrice());
    resp.setEntrustQty(order.getEntrustQty());
    resp.setStatus(order.getStatus());
    resp.setStatusDesc(OrderStatusEnum.getDesc(order.getStatus()));
    resp.setCreateTime(order.getCreateTime());
    return resp;
}
```

## JSON格式化

```java
// 日期格式化
@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
private Date createTime;

// 只有日期
@JsonFormat(pattern = "yyyy-MM-dd")
private Date tradeDate;

// 数值格式化为字符串
@JsonFormat(shape = JsonFormat.Shape.STRING)
private Long total;

// 忽略null值
@JsonInclude(JsonInclude.Include.NON_NULL)
private String optionalField;
```

## 命名规范总结

| DTO类型 | 命名规范 | 示例 |
|---------|---------|------|
| 普通请求 | XxxReq | OrderCreateReq |
| 分页请求 | XxxQueryReq | OrderQueryReq |
| 响应 | XxxResp | OrderResp |
| 分页响应 | PageInfoResp<Xxx> | PageInfoResp<OrderResp> |
| 内部DTO | XxxDTO | OrderDTO |
| 业务对象 | XxxBO | OrderBO |
