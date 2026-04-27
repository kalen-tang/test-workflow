---
name: invest-feign-guide
description: INVEST Feign服务调用指南。用于OpenFeign服务间调用配置和使用。当需要配置Feign客户端、实现服务间调用、处理Feign接口时使用。涉及Feign、服务调用、远程调用等关键词时使用此skill。
---

# INVEST Feign服务调用指南

## 🎯 Skill主要内容

- **核心功能**: OpenFeign服务间调用配置和最佳实践
- **适用场景**: 微服务间RPC调用、Feign接口定义
- **关键特性**: Feign接口规范、Hystrix熔断、请求上下文传递

---

## 🔧 Feign组件 - zainvest-loadbalancer-spring-boot-starter

### 📦 接入方式

引入依赖：
```xml
<dependency>
    <groupId>group.za.invest</groupId>
    <artifactId>zainvest-loadbalancer-spring-boot-starter</artifactId>
    <version>${zainvest.loadbalancer.starter.version}</version>
</dependency>
```

### 🚀 启用Feign

在启动类添加注解：
```java
@SpringBootApplication
@EnableFeignClients(basePackages = "group.za.bank")
public class TradeApplication {
    public static void main(String[] args) {
        SpringApplication.run(TradeApplication.class, args);
    }
}
```

---

## 📋 Feign接口定义规范

### 接口定义位置

Feign接口定义在Share模块中，供其他服务引用：

```
zabank-sbs-trade-service/
├── zabank-sbs-trade-share/
│   └── src/main/java/group/za/bank/sbs/trade/
│       ├── feign/                    # Feign接口
│       │   ├── StkOrderFeignService.java
│       │   └── StkAssetFeignService.java
│       └── model/
│           ├── req/feign/           # Feign请求对象
│           └── resp/feign/          # Feign响应对象
```

### 接口定义示例

```java
package group.za.bank.sbs.trade.feign;

import group.za.bank.invest.basecommon.entity.resp.ResponseData;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.validation.Valid;

/**
 * 股票订单Feign服务接口
 */
@FeignClient(value = "zabank-sbs-trade-service", contextId = "stkOrderFeignService")
public interface StkOrderFeignService {

    /**
     * 查询订单信息列表
     *
     * @param req 查询请求
     * @return 订单信息列表
     */
    @RequestMapping(value = "/inner/trade/order/queryOrderInfoList", method = RequestMethod.POST)
    ResponseData<List<OrderInfoResp>> queryOrderInfoList(@RequestBody OrderInfoReq req);

    /**
     * 查询成交终态订单
     *
     * @param request 查询请求
     * @return 分页结果
     */
    @RequestMapping(value = "/inner/trade/order/queryDealFinalOrderList", method = RequestMethod.POST)
    ResponseData<PageInfoResp<DealFinalOrderResp>> queryDealFinalOrderList(
        @RequestBody @Valid QueryDealFinalOrderReq request);
}
```

---

## ⚙️ Feign配置

### 基础配置

```properties
feign.hystrix.enabled=true
feign.client.config.default.connectTimeout=5000
feign.client.config.default.readTimeout=30000
feign.client.config.default.loggerLevel=BASIC
feign.compression.request.enabled=true
feign.compression.response.enabled=true
```

### Hystrix熔断配置

```properties
hystrix.command.default.execution.timeout.enabled=true
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=30000
hystrix.command.default.circuitBreaker.enabled=true
hystrix.command.default.circuitBreaker.requestVolumeThreshold=20
hystrix.command.default.circuitBreaker.errorThresholdPercentage=50
hystrix.command.default.circuitBreaker.sleepWindowInMilliseconds=5000
```

---

## 💻 Feign调用使用

### 服务调用示例

```java
@Service
@Slf4j
public class AssetService {

    @Autowired
    private StkAssetFeignService stkAssetFeignService;

    public List<FreezeInfoDTO> queryFreezeInfo(String userId, String stockCode) {
        StockAssetInfoReq req = new StockAssetInfoReq();
        req.setUserId(userId);
        req.setStockCode(stockCode);

        ResponseData<List<FreezeInfoDTO>> response = stkAssetFeignService.stockFreezeInfo(req);
        
        if (!response.isSuccess()) {
            log.error("查询冻结信息失败, code={}, msg={}", 
                response.getCode(), response.getMessage());
            throw new BusinessException(CommonErrorMsgEnum.REMOTE_CALL_ERROR);
        }
        
        return response.getData();
    }
}
```

---

## 🏗️ Feign实现类规范

### Provider模块实现

```java
package group.za.bank.sbs.trade.web.feign;

import group.za.bank.invest.basecommon.entity.resp.ResponseData;
import group.za.bank.sbs.trade.feign.StkOrderFeignService;
import group.za.bank.sbs.trade.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

/**
 * 股票订单Feign服务实现
 */
@RestController
public class StkOrderFeignController implements StkOrderFeignService {

    @Autowired
    private OrderService orderService;

    @Override
    public ResponseData<List<OrderInfoResp>> queryOrderInfoList(@RequestBody OrderInfoReq req) {
        List<OrderInfoResp> result = orderService.queryOrderInfoList(req);
        return ResponseData.success(result);
    }

    @Override
    public ResponseData<PageInfoResp<DealFinalOrderResp>> queryDealFinalOrderList(
            @RequestBody @Valid QueryDealFinalOrderReq request) {
        PageInfoResp<DealFinalOrderResp> result = orderService.queryDealFinalOrderList(request);
        return ResponseData.success(result);
    }
}
```

---

## 📝 URL路径规范

### 内部接口路径

Feign内部接口统一使用`/inner/`前缀：

```java
// 订单相关
/inner/trade/order/queryOrderInfoList
/inner/trade/order/createOrder

// 资产相关
/inner/trade/asset/queryFreezeInfo
/inner/trade/asset/queryBuyingPower
```

### 常量管理

```java
public class FeignTradeProvideUrlConstant {
    
    public static final String QUERY_ORDER_INFO_LIST = "/inner/trade/order/queryOrderInfoList";
    public static final String QUERY_DEAL_FINAL_ORDER_LIST = "/inner/trade/order/queryDealFinalOrderList";
    public static final String JUDGE_USER_ORDER_CLEAR = "/inner/trade/order/judgeUserOrderClear";
}
```

---

## 💡 最佳实践

### ✅ 推荐做法

1. **contextId配置**: 每个FeignClient指定唯一contextId避免冲突
2. **参数校验**: 使用@Valid注解对请求参数进行校验
3. **统一响应处理**: 封装Feign调用结果处理工具方法
4. **日志记录**: 调用前后记录必要日志

### ❌ 避免做法

1. 不要在Feign接口中使用GET请求传递复杂对象
2. 不要忽略Feign调用的异常处理
3. 不要将内部Feign接口暴露给外部

### 🔧 常见问题

**Q: Feign调用超时怎么处理？**
A: 检查Hystrix和Feign超时配置，确保Hystrix超时 > Feign超时

**Q: 多个FeignClient调用同一服务报冲突？**
A: 使用不同的contextId区分
