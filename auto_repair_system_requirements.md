# 汽修店记账软件需求文档

## 1. 项目概述

### 1.1 项目背景
为小型汽修店（主修火车、挂车）开发一款记账管理软件，用于记录进货、维修账单、配件消耗等业务数据，提高店铺管理效率。

### 1.2 项目目标
- 实现进货记录管理
- 实现维修账单及配件消耗记录
- 提供按客户名、时间等条件的查询索引功能
- 提供基础的财务统计分析功能

### 1.3 技术栈
- **后端语言**: Python 3.8+
- **数据库**: SQLite（轻量级，适合小型店铺）
- **GUI框架**: Tkinter（Python内置）或 PyQt5/PySide2
- **数据处理**: Pandas（数据分析）
- **报表生成**: ReportLab（PDF报表）

## 2. 功能需求

### 2.1 核心功能模块

#### 2.1.1 配件库存管理
**功能描述**: 管理汽修店的配件库存信息

**详细需求**:
- 配件基础信息管理（编号、名称、规格、品牌、类型）
- 配件分类管理（零部件、润滑油、消耗品等）
- 库存数量实时更新
- 库存预警功能（低库存提醒）
- 配件价格管理（进价、售价）

**数据字段**:
```
配件表 (parts)
- part_id: 配件ID（主键）
- part_name: 配件名称
- part_code: 配件编号
- category: 配件类型
- brand: 品牌
- specification: 规格型号
- unit: 单位
- purchase_price: 进价
- selling_price: 售价
- stock_quantity: 库存数量
- min_stock: 最小库存预警值
- supplier: 供应商
- create_time: 创建时间
- update_time: 更新时间
```

#### 2.1.2 进货管理
**功能描述**: 记录配件采购进货信息

**详细需求**:
- 进货单录入（供应商、进货日期、配件清单）
- 进货成本计算
- 自动更新库存数量
- 进货记录查询和统计
- 供应商管理

**数据字段**:
```
进货单表 (purchase_orders)
- order_id: 进货单号（主键）
- supplier_name: 供应商名称
- purchase_date: 进货日期
- total_amount: 进货总金额
- status: 单据状态
- operator: 操作员
- remarks: 备注
- create_time: 创建时间

进货明细表 (purchase_details)
- detail_id: 明细ID（主键）
- order_id: 进货单号（外键）
- part_id: 配件ID（外键）
- quantity: 进货数量
- unit_price: 单价
- subtotal: 小计金额
```

#### 2.1.3 维修账单管理
**功能描述**: 记录每次维修服务的详细账单信息

**详细需求**:
- 维修订单创建和管理
- 客户信息管理
- 维修项目记录
- 配件消耗记录
- 工时费用计算
- 账单打印功能

**数据字段**:
```
客户表 (customers)
- customer_id: 客户ID（主键）
- customer_name: 客户姓名
- phone: 联系电话
- address: 地址
- vehicle_info: 车辆信息
- create_time: 创建时间

维修订单表 (repair_orders)
- order_id: 订单号（主键）
- customer_id: 客户ID（外键）
- vehicle_type: 车辆类型（火车/挂车）
- vehicle_number: 车牌号/车辆编号
- repair_date: 维修日期
- fault_description: 故障描述
- repair_content: 维修内容
- labor_cost: 工时费
- parts_cost: 配件费用
- total_amount: 总金额
- status: 订单状态
- technician: 维修技师
- remarks: 备注
- create_time: 创建时间
- complete_time: 完成时间

维修配件消耗表 (repair_parts_usage)
- usage_id: 使用记录ID（主键）
- order_id: 订单号（外键）
- part_id: 配件ID（外键）
- quantity_used: 使用数量
- unit_price: 单价
- subtotal: 小计金额
```

#### 2.1.4 查询索引功能
**功能描述**: 提供多维度的数据查询和检索功能

**详细需求**:
- 按客户名查询历史维修记录
- 按时间范围查询（日、周、月、年）
- 按车辆类型查询
- 按维修项目类型查询
- 按配件使用情况查询
- 复合条件查询

**查询接口**:
```python
# 查询示例
def query_repairs_by_customer(customer_name, start_date=None, end_date=None)
def query_repairs_by_date_range(start_date, end_date)
def query_parts_usage(part_name, start_date=None, end_date=None)
def query_customer_history(customer_id)
```

### 2.2 辅助功能模块

#### 2.2.1 统计分析
- 日/月/年收入统计
- 配件消耗统计
- 客户维修频次分析
- 库存周转率分析

#### 2.2.2 报表生成
- 维修账单打印
- 进货单打印
- 月度经营报表
- 库存报表

#### 2.2.3 数据备份
- 定期数据备份
- 数据导入/导出功能
- 数据恢复功能

## 3. 非功能性需求

### 3.1 性能要求
- 响应时间: 查询操作 < 2秒
- 数据处理: 支持10万条记录以内的数据量
- 并发性: 支持单用户操作

### 3.2 可靠性要求
- 数据准确性: 99.9%
- 系统稳定性: 连续运行72小时无故障
- 数据安全性: 定期备份，防止数据丢失

### 3.3 可用性要求
- 界面友好，操作简单
- 支持键盘快捷键操作
- 提供操作帮助文档

## 4. 系统架构设计

### 4.1 整体架构
```
┌─────────────────────────────────────┐
│           用户界面层 (GUI)            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │进货管理 │ │维修管理 │ │查询统计 │  │
│  └─────────┘ └─────────┘ └─────────┘  │
├─────────────────────────────────────┤
│           业务逻辑层 (Service)        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │库存服务 │ │订单服务 │ │报表服务 │  │
│  └─────────┘ └─────────┘ └─────────┘  │
├─────────────────────────────────────┤
│           数据访问层 (DAO)           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │配件DAO  │ │订单DAO  │ │客户DAO  │  │
│  └─────────┘ └─────────┘ └─────────┘  │
├─────────────────────────────────────┤
│           数据库层 (SQLite)          │
└─────────────────────────────────────┘
```

### 4.2 目录结构
```
auto_repair_system/
├── main.py                 # 主程序入口
├── config/
│   ├── __init__.py
│   └── settings.py         # 配置文件
├── models/
│   ├── __init__.py
│   ├── database.py         # 数据库连接
│   ├── parts.py           # 配件模型
│   ├── customers.py       # 客户模型
│   └── orders.py          # 订单模型
├── services/
│   ├── __init__.py
│   ├── inventory_service.py # 库存服务
│   ├── order_service.py    # 订单服务
│   └── report_service.py   # 报表服务
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # 主窗口
│   ├── inventory_window.py # 库存管理窗口
│   ├── order_window.py     # 订单管理窗口
│   └── query_window.py     # 查询窗口
├── utils/
│   ├── __init__.py
│   ├── database_utils.py   # 数据库工具
│   └── export_utils.py     # 导出工具
├── data/
│   └── auto_repair.db      # SQLite数据库文件
└── docs/
    └── user_manual.md      # 用户手册
```

## 5. 数据库设计

### 5.1 数据库表关系图
```
customers (客户表)
    ↓ 1:N
repair_orders (维修订单表)
    ↓ 1:N
repair_parts_usage (配件使用表)
    ↓ N:1
parts (配件表)
    ↑ 1:N
purchase_details (进货明细表)
    ↓ N:1
purchase_orders (进货单表)
```

### 5.2 索引设计
```sql
-- 客户名称索引
CREATE INDEX idx_customer_name ON customers(customer_name);

-- 维修日期索引
CREATE INDEX idx_repair_date ON repair_orders(repair_date);

-- 客户维修记录索引
CREATE INDEX idx_customer_repair ON repair_orders(customer_id, repair_date);

-- 配件使用索引
CREATE INDEX idx_parts_usage ON repair_parts_usage(part_id, order_id);
```

## 6. 开发计划

### 6.1 开发阶段划分

**第一阶段 (2周)**: 基础框架搭建
- 数据库设计和创建
- 基本模型类开发
- 主界面框架搭建

**第二阶段 (2周)**: 核心功能开发
- 配件库存管理功能
- 进货管理功能
- 基础的增删改查操作

**第三阶段 (2周)**: 维修管理功能
- 客户管理功能
- 维修订单管理
- 配件消耗记录

**第四阶段 (1周)**: 查询统计功能
- 多维度查询功能
- 基础统计报表
- 数据导出功能

**第五阶段 (1周)**: 测试和优化
- 功能测试
- 性能优化
- 用户界面优化

### 6.2 技术要点

#### 6.2.1 数据库连接管理
```python
# 使用连接池管理数据库连接
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('data/auto_repair.db')
    try:
        yield conn
    finally:
        conn.close()
```

#### 6.2.2 事务处理
```python
# 维修订单创建时的事务处理
def create_repair_order(order_data, parts_usage):
    with get_db_connection() as conn:
        try:
            cursor = conn.cursor()
            # 创建订单
            cursor.execute(insert_order_sql, order_data)
            order_id = cursor.lastrowid
            
            # 记录配件使用并更新库存
            for part_usage in parts_usage:
                cursor.execute(insert_usage_sql, part_usage)
                cursor.execute(update_stock_sql, (part_usage['quantity'], part_usage['part_id']))
            
            conn.commit()
            return order_id
        except Exception as e:
            conn.rollback()
            raise e
```

## 7. 风险评估

### 7.1 技术风险
- **数据丢失风险**: 通过定期备份和数据校验机制降低风险
- **性能风险**: 通过索引优化和查询优化提升性能

### 7.2 业务风险
- **用户接受度**: 通过简化界面和提供培训降低学习成本
- **数据迁移**: 提供数据导入功能支持现有数据迁移

## 8. 交付物清单

### 8.1 软件交付物
- 可执行程序文件
- 数据库文件
- 配置文件
- 安装说明

### 8.2 文档交付物
- 用户操作手册
- 系统管理员手册
- 技术文档
- 数据库设计文档

## 9. 后续维护

### 9.1 版本更新计划
- 根据用户反馈进行功能优化
- 定期安全更新
- 新功能需求评估和开发

### 9.2 技术支持
- 提供远程技术支持
- 定期数据备份检查
- 系统性能监控

---

**文档版本**: v1.0  
**创建日期**: 2025年7月  
**最后更新**: 2025年7月