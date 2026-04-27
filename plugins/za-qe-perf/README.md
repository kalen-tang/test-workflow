# za-qe-perf - INVEST微服务框架性能测试与规范检查工具集

## 📋 插件概述

`za-qe-perf` 是专门为众安银行 INVEST 微服务框架设计的性能测试与代码规范检查工具集。该插件提供了一套完整的开发规范指南，帮助开发人员遵循 INVEST 框架的最佳实践，确保代码质量和系统性能。

### 核心价值

- **规范化开发**: 提供 INVEST 框架各层级的完整开发规范
- **性能优化**: 包含性能测试点和最佳实践指导
- **代码质量**: 统一的异常处理、事务管理、数据访问规范
- **团队协作**: 标准化的开发流程和代码风格

## 🚀 快速开始

### 安装配置

该插件作为 Claude Code 插件系统的一部分，需要配置到项目的 `.claude-plugin/marketplace.json` 中：

```json
{
  "plugins": {
    "core": [
      {
        "name": "za-qe-perf",
        "description": "INVEST微服务框架性能测试与规范检查工具集",
        "path": "plugins/za-qe-perf"
      }
    ]
  }
}
```

### 基本使用

在 Claude Code 中直接调用相关技能：

```bash
# 查看框架概览
/invest-framework-overview

# 检查Controller层规范
/invest-controller-spec

# 分析Service层代码
/invest-service-spec

# 生成测试点分析报告
/smart-interface-spec
```

## 🛠️ 技能列表

### 1. invest-framework-overview
**框架概览** - INVEST微服务框架技术栈和分层架构概览

- **用途**: 了解INVEST框架Spring Boot + MyBatis-Plus技术栈、理解Controller-Service-DAO分层架构
- **关键词**: `invest-framework`, `spring-boot`, `mybatis-plus`, `microservice-overview`
- **适用场景**: 项目初期架构理解、新人onboarding

### 2. invest-controller-spec
**Controller层规范** - INVEST框架Controller层完整开发规范

- **用途**: 创建Controller层RESTful API接口、配置ResponseData统一响应结构、处理分页查询请求
- **关键词**: `invest-controller`, `restful-api`, `response-data`, `pagination-controller`
- **核心内容**: ResponseData规范、分页处理、Swagger注解

### 3. invest-service-spec
**Service层规范** - INVEST框架Service层完整开发规范

- **用途**: 设计Service接口和ServiceImpl实现类、编写业务逻辑代码、使用TransactionUtils编程式事务管理
- **关键词**: `invest-service`, `service-impl`, `transaction-utils`, `business-logic`
- **重要约束**: 禁止使用 `@Transactional` 注解，统一使用 `TransactionUtils`

### 4. invest-dao-spec
**DAO层规范** - INVEST框架数据访问层完整开发规范

- **用途**: 创建DAO层Mapper接口、SBS项目继承BaseMapper、FTC项目继承CrudMapper
- **关键词**: `invest-dao`, `base-mapper`, `crud-mapper`, `mybatis-plus`
- **项目差异**: SBS项目使用BaseMapper，FTC项目使用CrudMapper

### 5. invest-dto-spec
**DTO设计规范** - INVEST框架DTO设计完整规范

- **用途**: 设计请求响应DTO结构、继承BaseReq分页基类、配置分页传输对象
- **关键词**: `invest-dto`, `base-req`, `page-req-dto`, `page-rsp-dto`
- **核心内容**: BaseReq继承、分页DTO、请求响应DTO设计

### 6. invest-entity-spec
**实体类规范** - INVEST框架实体类完整开发规范

- **用途**: 设计数据库实体类、配置MyBatis-Plus注解、处理持久化对象映射
- **关键词**: `invest-entity`, `table-name`, `table-field`, `mybatis-plus-entity`
- **核心内容**: 实体类设计、字段注解、命名规范

### 7. invest-exception-spec
**异常处理规范** - INVEST框架异常处理完整规范

- **用途**: 抛出BusinessException业务异常、设计错误码枚举类、实现ResourceHandler国际化接口
- **关键词**: `invest-exception`, `business-exception`, `error-code`, `resource-handler`
- **核心内容**: BusinessException使用、错误码枚举设计、统一异常响应

### 8. invest-database-guide
**数据库ORM指南** - INVEST数据库ORM使用指南

- **用途**: 配置MyBatis-Plus ORM增强功能、实现IPage分页查询、使用TransactionUtils编程式事务管理
- **关键词**: `invest-database`, `mybatis-plus-config`, `ipage-pagination`, `transaction-utils`
- **核心内容**: MyBatis-Plus配置、分页查询、事务处理

### 9. invest-feign-guide
**Feign调用指南** - INVEST Feign服务调用指南

- **用途**: 配置OpenFeign客户端接口、实现微服务间远程调用、处理Feign降级和超时配置
- **关键词**: `invest-feign`, `open-feign`, `feign-client`, `remote-call`
- **核心内容**: Feign接口规范、Hystrix熔断、请求上下文传递

### 10. smart-interface-spec
**测试点分析** - 基于代码变更生成测试要点报告

- **用途**: 分析git diff或指定文件，生成完整的测试点分析报告
- **关键词**: `test-point-analysis`, `code-change`, `testing-scenarios`, `regression-testing`
- **核心功能**: 自动识别代码变更点，生成功能测试、接口测试、数据层测试等完整测试方案

## 📊 技能分类

| 分类 | 技能 | 用途 |
|------|------|------|
| **框架概览** | invest-framework-overview | 整体架构理解 |
| **开发规范** | invest-controller-spec<br>invest-service-spec<br>invest-dao-spec<br>invest-dto-spec<br>invest-entity-spec<br>invest-exception-spec | 各层级开发规范 |
| **技术指南** | invest-database-guide<br>invest-feign-guide | 具体技术使用指南 |
| **测试分析** | smart-interface-spec | 代码变更测试分析 |

## 🔧 使用示例

### 新项目开发指导

```bash
# 1. 了解框架整体架构
/invest-framework-overview

# 2. 设计实体类和DTO
/invest-entity-spec
/invest-dto-spec

# 3. 实现数据访问层
/invest-dao-spec
/invest-database-guide

# 4. 编写业务逻辑层
/invest-service-spec

# 5. 实现Controller接口
/invest-controller-spec

# 6. 配置服务间调用
/invest-feign-guide

# 7. 异常处理设计
/invest-exception-spec
```

### 代码审查与测试分析

```bash
# 分析当前git变更的测试点
/smart-interface-spec

# 分析指定文件的测试点
/smart-interface-spec src/main/java/group/za/bank/trade/controller/TradeController.java

# 对比分支差异的测试点
/smart-interface-spec --branch main feature/order-refactor
```

## ⚠️ 重要规范

### 事务管理规范
- **禁止使用** `@Transactional` 注解
- **统一使用** `TransactionUtils.execute()` 进行编程式事务管理
- **事务范围** 只包裹写操作，读操作和非DB操作放在事务外

### 异常处理规范
- **统一使用** `BusinessException` 抛出业务异常
- **错误码设计** 遵循模块前缀 + 编号格式（如 ORD001）
- **国际化支持** 通过 `ResourceHandler` 接口实现

### 代码分层规范
- **Controller层** 负责HTTP请求响应和参数校验
- **Service层** 实现核心业务逻辑，协调Manager层
- **Manager层** 封装可复用的业务逻辑单元
- **DAO层** 负责数据持久化操作

## 📈 性能优化建议

### 数据库操作
- 使用LambdaQueryWrapper进行条件查询
- 大数据量查询必须使用分页
- 避免全表扫描，查询条件必须包含索引字段

### 缓存使用
- 使用RedissonClient进行缓存操作
- 缓存Key通过RedisCacheKeyBuilder枚举管理
- 合理设置缓存过期时间

### 事务优化
- 事务范围尽可能小，只包裹写操作
- 避免长事务导致数据库连接占用过长
- 提高并发能力，减少锁持有时间

## 🔍 故障排查

### 常见问题

**Q: Feign调用超时怎么处理？**
A: 检查Hystrix和Feign超时配置，确保Hystrix超时 > Feign超时

**Q: 事务不生效怎么办？**
A: 确认使用TransactionUtils而非@Transactional，检查事务传播机制配置

**Q: 分页查询性能差怎么办？**
A: 检查是否使用了正确的索引，避免全表扫描，合理设置pageSize

## 📚 相关资源

- **INVEST框架文档**: 参考各技能的SKILL.md文件
- **开发规范**: 每个技能都包含完整的代码示例和最佳实践
- **测试分析**: smart-interface-spec提供自动化测试点生成

## 🎯 版本信息

- **插件版本**: 1.0.0
- **适用框架**: INVEST微服务框架
- **支持技术**: Spring Boot 2.1.6, MyBatis-Plus 3.4.0, OpenFeign
- **更新日期**: 2026-04-27

---

**注意**: 本插件适用于众安银行INVEST微服务框架开发团队，确保代码质量和开发效率的统一标准。