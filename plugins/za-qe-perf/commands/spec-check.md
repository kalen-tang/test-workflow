# za-qe-perf:spec-check

INVEST框架各层级开发规范检查。整合Controller层、Service层、DAO层、DTO设计、实体类、异常处理等完整开发规范。

## 使用方式

在Claude Code中直接调用：

```bash
/za-qe-perf:spec-check
```

## 功能说明

此命令将依次激活以下技能，提供完整的开发规范检查：

### 1. Controller层规范（invest-controller-spec）
- ResponseData统一响应结构规范
- 分页查询处理规范
- Swagger API文档注解规范
- HTTP请求响应处理规范

### 2. Service层规范（invest-service-spec）
- Service接口和ServiceImpl实现规范
- TransactionUtils编程式事务管理（禁止使用@Transactional）
- Manager层使用规范
- 业务逻辑编写规范

### 3. DAO层规范（invest-dao-spec）
- SBS项目BaseMapper规范
- FTC项目CrudMapper规范
- Mapper XML配置规范
- 数据库访问代码规范

### 4. DTO设计规范（invest-dto-spec）
- BaseReq继承规范
- 分页DTO设计规范
- 请求响应DTO结构规范
- DTO映射转换规范

### 5. 实体类规范（invest-entity-spec）
- 数据库实体类设计规范
- MyBatis-Plus注解配置规范
- 字段映射和命名规范
- 持久化对象设计规范

### 6. 异常处理规范（invest-exception-spec）
- BusinessException使用规范
- 错误码枚举设计规范
- ResourceHandler国际化接口规范
- 统一异常响应处理规范

## 适用场景

- 新功能开发时的规范参考
- 代码审查时的规范检查
- 团队统一开发标准制定
- 技术债务清理和重构

## 关键词

invest-spec, controller-spec, service-spec, dao-spec, dto-spec, entity-spec, exception-spec, development-standard, code-review