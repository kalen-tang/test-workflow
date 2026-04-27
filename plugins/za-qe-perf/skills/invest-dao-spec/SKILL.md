---
name: invest-dao-spec
description: INVEST框架数据访问层完整开发规范。当设计DAO/Mapper层、使用Mybatis-Plus或自研Mybatis框架、编写数据库访问代码时使用。包含SBS项目BaseMapper规范和FTC项目CrudMapper规范。涉及数据访问、Mapper、DAO等关键词时使用此skill。
---

# INVEST DAO层开发规范

INVEST框架数据访问层负责封装数据库操作。根据项目类型有两种实现方式：
- **SBS项目**: 基于Mybatis-Plus的BaseMapper
- **FTC项目**: 基于自研zainvest-mybatis-spring-boot-starter的CrudMapper

## 快速开始

### SBS项目（Mybatis-Plus）

```java
@Mapper
public interface StkOrderMapper extends BaseMapper<StkOrder> {

    BigDecimal getTotalBusinessAmount(
        @Param("tradeDate") Date tradeDate, 
        @Param("entrustType") String entrustType
    );
}
```

### FTC项目（自研Mybatis框架）

```java
@Repository
public interface TdFundOrderMapper extends CrudMapper<TdFundOrder> {

    List<TdFundOrder> fundOrderList(
        @Param("startDate") Date startDate, 
        @Param("endDate") Date endDate
    );
}
```

---

## 一、SBS项目 - Mybatis-Plus规范

### 1.1 依赖配置

```xml
<dependency>
    <groupId>group.za.invest</groupId>
    <artifactId>zainvest-mybatisplus-spring-boot-starter</artifactId>
    <version>${zainvest.mybatisplus.starter.version}</version>
</dependency>
```

### 1.2 Mapper接口规范

```java
@Mapper
public interface StkOrderMapper extends BaseMapper<StkOrder> {

    /**
     * 获取某个交易日所有成交单的总额
     */
    BigDecimal getTotalBusinessAmount(
        @Param("tradeDate") Date tradeDate, 
        @Param("entrustType") String entrustType
    );

    /**
     * 查询某支股票在某个交易日的成交数量
     */
    List<BusinessShareDTO> queryBusinessShare(
        @Param("tradeDate") Date tradeDate,
        @Param("stockCode") String stockCode
    );
}
```

### 1.3 BaseMapper基础方法

```java
// 插入操作
int insert(T entity);

// 删除操作
int deleteById(Serializable id);
int deleteBatchIds(Collection<? extends Serializable> idList);
int delete(Wrapper<T> queryWrapper);

// 更新操作
int updateById(T entity);
int update(T entity, Wrapper<T> updateWrapper);

// 查询操作
T selectById(Serializable id);
List<T> selectBatchIds(Collection<? extends Serializable> idList);
T selectOne(Wrapper<T> queryWrapper);
List<T> selectList(Wrapper<T> queryWrapper);
IPage<T> selectPage(IPage<T> page, Wrapper<T> queryWrapper);
Integer selectCount(Wrapper<T> queryWrapper);
```

### 1.4 LambdaQueryWrapper使用

```java
// 多条件查询
LambdaQueryWrapper<StkOrder> wrapper = new LambdaQueryWrapper<>();
wrapper.eq(StkOrder::getUserId, userId)
       .eq(StkOrder::getStatus, status)
       .ge(StkOrder::getCreateTime, startDate)
       .le(StkOrder::getCreateTime, endDate);
List<StkOrder> orders = orderMapper.selectList(wrapper);

// 分页查询
Page<StkOrder> page = new Page<>(pageNum, pageSize);
IPage<StkOrder> result = orderMapper.selectPage(page, wrapper);
```

### 1.5 LambdaUpdateWrapper使用

```java
LambdaUpdateWrapper<StkOrder> wrapper = new LambdaUpdateWrapper<>();
wrapper.eq(StkOrder::getOrderNo, orderNo)
       .set(StkOrder::getStatus, newStatus)
       .set(StkOrder::getUpdateTime, new Date());

orderMapper.update(null, wrapper);
```

---

## 二、FTC项目 - 自研Mybatis框架规范

### 2.1 依赖配置

```xml
<dependency>
    <groupId>group.za.invest</groupId>
    <artifactId>zainvest-mybatis-spring-boot-starter</artifactId>
    <version>${zainvest.mybatis.starter.version}</version>
</dependency>
```

### 2.2 Mapper接口规范

```java
@Repository
public interface TdFundOrderMapper extends CrudMapper<TdFundOrder> {

    /**
     * 根据实际确认时间查询订单列表
     */
    List<TdFundOrder> fundOrderList(
        @Param("startDate") Date startDate, 
        @Param("endDate") Date endDate
    );

    /**
     * 查询用户的基金订单列表
     */
    List<TdFundOrder> selectUserOrderRecordList(
        @Param("bankUserId") String bankUserId,
        @Param("bankAccountId") String bankAccountId,
        @Param("startDate") Date startDate, 
        @Param("endDate") Date endDate,
        @Param("productId") String productId,
        @Param("businessType") String businessType
    );
}
```

**注解差异**：
- SBS项目使用 `@Mapper`
- FTC项目使用 `@Repository`

### 2.3 CrudMapper基础方法

CrudMapper继承自多个接口，提供完整的CRUD操作：

```java
// CrudMapper组成
public interface CrudMapper<T> extends 
    CreateMapper<T>,      // 插入操作
    RetrieveMapper<T>,    // 查询操作
    UpdateMapper<T>,      // 更新操作
    DeleteMapper<T> {}    // 删除操作
```

**插入操作 (CreateMapper)**：
```java
int insert(T record);                    // 插入记录（null字段不插入）
int insertAllColumn(T record);           // 插入记录（所有字段）
int insertBatch(List<T> recordList);     // 批量插入
int insertOnDuplicateUpdate(T record);   // 插入或更新（存在则更新）
```

**查询操作 (RetrieveMapper)**：
```java
T selectOne(T condition);                           // 单条件查询
T selectByPrimaryKey(Object key);                   // 主键查询
List<T> selectList(T condition);                    // 条件查询列表
List<T> selectListWithSort(T condition, List<Order> orders);  // 带排序查询
int selectCount(T condition);                       // 条件统计
PageInfo<T> selectPage(T condition, int pageNum, int pageSize);  // 分页查询
```

**更新操作 (UpdateMapper)**：
```java
int updateByPrimaryKey(T record);            // 主键更新（null字段不更新）
int updateByPrimaryKeyAllColumn(T record);   // 主键更新（所有字段）
int updateByCondition(T record, T condition);// 条件更新
int updateUseMapByCondition(Map<String, Object> params, T condition); // Map方式更新
```

**删除操作 (DeleteMapper)**：
```java
int deleteByPrimaryKey(Object key);      // 主键删除
int deleteByCondition(T condition);      // 条件删除
```

### 2.4 条件查询示例

```java
// 使用实体作为查询条件
TdFundOrder condition = new TdFundOrder();
condition.setBankUserId("123456");
condition.setStatus("COMPLETED");
List<TdFundOrder> orders = orderMapper.selectList(condition);

// 单条件查询
TdFundOrder oneCondition = new TdFundOrder();
oneCondition.setOrderNo("ORD001");
TdFundOrder order = orderMapper.selectOne(oneCondition);

// 主键查询
TdFundOrder order = orderMapper.selectByPrimaryKey(orderId);
```

### 2.5 分页查询示例

```java
TdFundOrder condition = new TdFundOrder();
condition.setBankUserId(userId);

PageInfo<TdFundOrder> pageInfo = orderMapper.selectPage(condition, pageNum, pageSize);

// 获取结果
List<TdFundOrder> records = pageInfo.getList();
long total = pageInfo.getTotal();
int pages = pageInfo.getPages();
```

### 2.6 带排序查询

```java
TdFundOrder condition = new TdFundOrder();
condition.setBankUserId(userId);

List<Order> orders = new ArrayList<>();
orders.add(new Order("create_time", Order.Direction.DESC));

List<TdFundOrder> result = orderMapper.selectListWithSort(condition, orders);
```

---

## 三、Mapper.xml配置规范

### 3.1 文件命名和位置

- **文件名**: `{Mapper接口名}.xml`
- **位置**: `src/main/resources/mapper/`目录下

### 3.2 基本XML结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="group.za.bank.fund.domain.trade.mapper.TdFundOrderMapper">

    <select id="fundOrderList" resultType="group.za.bank.fund.domain.trade.entity.TdFundOrder">
        SELECT * FROM td_fund_order
        WHERE actual_confirm_date BETWEEN #{startDate} AND #{endDate}
    </select>

</mapper>
```

### 3.3 动态SQL

```xml
<select id="queryOrders" resultType="...">
    SELECT * FROM td_fund_order
    <where>
        <if test="bankUserId != null and bankUserId != ''">
            AND bank_user_id = #{bankUserId}
        </if>
        <if test="status != null and status != ''">
            AND status = #{status}
        </if>
        <if test="startDate != null">
            AND create_time >= #{startDate}
        </if>
        <if test="endDate != null">
            AND create_time &lt;= #{endDate}
        </if>
    </where>
    ORDER BY create_time DESC
</select>
```

### 3.4 IN查询

```xml
<select id="queryByStatusList" resultType="...">
    SELECT * FROM td_fund_order
    WHERE bank_user_id = #{bankUserId}
    <if test="statusList != null and statusList.size() > 0">
        AND status IN
        <foreach collection="statusList" item="status" 
                 open="(" separator="," close=")">
            #{status}
        </foreach>
    </if>
</select>
```

---

## 四、对比总结

| 特性 | SBS项目 (Mybatis-Plus) | FTC项目 (自研框架) |
|-----|------------------------|-------------------|
| 依赖 | zainvest-mybatisplus-starter | zainvest-mybatis-starter |
| 基类 | BaseMapper | CrudMapper |
| 注解 | @Mapper | @Repository |
| 查询构造器 | LambdaQueryWrapper | 实体对象作为条件 |
| 分页 | IPage + Page | PageInfo |
| 批量插入 | insertBatchSomeColumn | insertBatch |

---

## 五、使用规范总结

1. **选择正确的基类**: SBS项目使用BaseMapper，FTC项目使用CrudMapper
   1. 对于SBS项目, **优先使用** LambdaQueryWrapper, 涉及多表关联或聚合查询时使用再使用XML
2. **优先使用内置方法**: 简单CRUD操作使用框架提供的方法
3. **复杂SQL使用XML**: 多表关联、复杂统计等使用XML定义
4. **参数使用@Param注解**: 多参数方法必须使用`@Param`注解
5. **避免全表扫描**: 查询条件必须包含索引字段
6. **分页查询**: 大数据量查询必须使用分页
