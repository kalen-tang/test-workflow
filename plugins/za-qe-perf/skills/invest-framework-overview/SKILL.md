---
name: invest-framework-overview
description: INVEST微服务框架技术栈和分层架构概览。当需要了解INVEST框架整体架构、技术选型、目录结构时使用。支持银行投资业务系统开发，适用于项目初期架构理解和新人onboarding。
---

# INVEST框架概览

INVEST是众安银行投资业务后端开发团队所使用的微服务框架，基于Spring Boot构建，为股票、基金等投资业务系统提供标准化的开发规范和架构指导。

## 核心技术栈

### 基础框架
- **Java 8** - 开发语言
- **Spring Boot 2.1.6.RELEASE** - 核心应用框架
- **Spring Cloud Greenwich.SR2** - 微服务治理
- **Maven** - 构建系统，标准Maven目录结构

### 数据处理
- **Mybatis-Plus 3.4.0** - 数据库ORM框架
- **Redis** - 缓存中间件
- **HikariCP** - 数据库连接池

### 服务治理
- **Apollo** - 配置中心
- **Eureka** - 服务注册与发现
- **OpenFeign** - 服务间调用

### 消息队列
- **RabbitMQ** - 消息队列

### 测试框架
- **JUnit 5** - 单元测试
- 如果是 SBS 项目还会使用 **Spock** 进行单元测试

## 核心组件说明

### 父工程
- **zabank-invest-spring-boot-parent**: 每个微服务项目的父工程，作为依赖管理

### 公共组件库
- **zainvest-all-plugins**: INVEST团队开发的各种Spring Boot Starter和公共组件集合
  - `zainvest-cache-spring-boot-starter` - Redis缓存
  - `zainvest-mybatisplus-spring-boot-starter` - MyBatis Plus增强
  - `zainvest-rabbitmq-spring-boot-starter` - RabbitMQ消息队列
  - `zainvest-web-spring-boot-starter` - Web相关组件
  - `zainvest-apollo-spring-boot-starter` - Apollo配置中心
  - 其他starter...

### 基础类库
- **zabank-invest-basecommon**: 定义了Controller层的公共入参父类、返回值父类、业务异常父类等基础组件
- **zabank-invest-common**: 定义了大量的公共工具类

## 分层架构设计

INVEST采用经典的多模块微服务架构，每个服务按以下模块划分：

以 `zabank-sbs-trade-service` 为例：

### 1. Share模块 (zabank-sbs-trade-share)
```
zabank-sbs-trade-share/
├── pom.xml
└── src/main/java/
    └── group/za/bank/sbs/trade/
        ├── dto/           # 对外暴露的DTO
        ├── req/           # 请求对象
        ├── resp/          # 响应对象
        ├── enums/         # 枚举类
        └── feign/           # Feign接口定义
```

**职责：**
- 定义服务对外暴露的接口契约
- 提供给其他服务调用的DTO和API定义
- 作为服务间调用的二方包

### 2. Domain模块 (zabank-sbs-trade-domain)
```
zabank-sbs-trade-domain/
├── pom.xml
└── src/main/java/
    └── group/za/bank/sbs/trade/
        ├── mapper/        # MyBatis Mapper接口
        └── model/
            ├── entity/    # 数据库实体类
            └── dto/       # 内部DTO
```

**职责：**
- 数据持久层实现
- 实体类和Mapper定义
- 数据库操作封装

### 3. Provider模块 (zabank-sbs-trade-provider)
```
zabank-sbs-trade-provider/
├── pom.xml
└── src/main/java/
    └── group/za/bank/sbs/trade/
        ├── web/
        │   ├── controller/    # Controller层
        │   └── feign/         # Share模块的Feign接口实现
        ├── service/           # 业务逻辑接口
        │   └── impl/          # 业务逻辑实现
        ├── manager/           # 管理层（复杂业务编排）
        │   └── impl/
        ├── model/
        │   ├── req/           # 请求对象
        │   ├── resp/          # 响应对象
        │   ├── dto/           # 数据传输对象
        │   ├── bo/            # 业务对象
        │   └── convert/       # 对象转换器
        └── common/
            ├── aop/           # 切面
            ├── config/        # 配置类
            ├── constant/      # 常量
            └── utils/         # 工具类
```

**职责：**
- 接收外部请求并协调业务处理
- 实现核心业务逻辑
- 调用其他微服务
- 处理定时任务和消息监听

## 包名规范

INVEST项目统一使用以下包名前缀：
- 基础公共包: `group.za.bank.invest.basecommon`
- 公共工具包: `group.za.bank.invest.common`
- 业务服务包: `group.za.bank.{service}` (如`sbs.trade`、`ftc.trade`等)

## 示例项目

`zabank-sbs-trade-service` 是一个典型的INVEST微服务项目示例，包含了完整的分层架构实现。
