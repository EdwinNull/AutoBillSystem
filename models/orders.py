#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单模型
"""

from datetime import datetime, date
from .database import DatabaseManager
from config.settings import DATABASE_PATH

class RepairOrder:
    """维修订单模型类"""
    
    def __init__(self, order_id=None, customer_id=None, vehicle_type="", 
                 vehicle_number="", repair_date=None, fault_description="", 
                 repair_content="", labor_cost=0.0, parts_cost=0.0, 
                 total_amount=0.0, status="进行中", technician="", remarks=""):
        self.order_id = order_id
        self.customer_id = customer_id
        self.vehicle_type = vehicle_type
        self.vehicle_number = vehicle_number
        self.repair_date = repair_date or date.today()
        self.fault_description = fault_description
        self.repair_content = repair_content
        self.labor_cost = labor_cost
        self.parts_cost = parts_cost
        self.total_amount = total_amount
        self.status = status
        self.technician = technician
        self.remarks = remarks
        self.create_time = None
        self.complete_time = None
        # 生成订单号（如果是新订单则生成新号码，如果是从数据库加载则使用ID生成）
        self.order_number = f"RO{order_id:06d}" if order_id else self._generate_order_number()
    
    def _generate_order_number(self):
        """生成订单号"""
        from datetime import datetime
        now = datetime.now()
        return f"RO{now.strftime('%Y%m%d%H%M%S')}"
    
    def to_dict(self):
        """转换为字典"""
        return {
            'order_id': self.order_id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'vehicle_type': self.vehicle_type,
            'vehicle_number': self.vehicle_number,
            'repair_date': self.repair_date,
            'fault_description': self.fault_description,
            'repair_content': self.repair_content,
            'labor_cost': self.labor_cost,
            'parts_cost': self.parts_cost,
            'total_amount': self.total_amount,
            'status': self.status,
            'technician': self.technician,
            'remarks': self.remarks
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        order = cls()
        for key, value in data.items():
            if hasattr(order, key):
                setattr(order, key, value)
        
        # 处理日期字段
        if 'repair_date' in data and data['repair_date']:
            try:
                if isinstance(data['repair_date'], str):
                    # 尝试解析不同的日期格式
                    try:
                        order.repair_date = datetime.strptime(data['repair_date'], '%Y-%m-%d').date()
                    except ValueError:
                        order.repair_date = datetime.strptime(data['repair_date'], '%Y-%m-%d %H:%M:%S').date()
                elif hasattr(data['repair_date'], 'date'):
                    order.repair_date = data['repair_date'].date()
                else:
                    order.repair_date = data['repair_date']
            except (ValueError, TypeError, AttributeError):
                order.repair_date = date.today()
        
        return order

class PurchaseOrder:
    """进货订单模型类"""
    
    def __init__(self, order_id=None, supplier_name="", purchase_date=None, 
                 total_amount=0.0, status="已完成", operator="", remarks=""):
        self.order_id = order_id
        self.supplier_name = supplier_name
        self.purchase_date = purchase_date or date.today()
        self.total_amount = total_amount
        self.status = status
        self.operator = operator
        self.remarks = remarks
        self.create_time = None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'order_id': self.order_id,
            'supplier_name': self.supplier_name,
            'purchase_date': self.purchase_date,
            'total_amount': self.total_amount,
            'status': self.status,
            'operator': self.operator,
            'remarks': self.remarks
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        order = cls()
        for key, value in data.items():
            if hasattr(order, key):
                setattr(order, key, value)
        return order

class RepairPartsUsage:
    """维修配件使用记录"""
    
    def __init__(self, usage_id=None, order_id=None, part_id=None, part_name="",
                 part_source="库存配件", quantity_used=0, unit_price=0.0, subtotal=0.0, remarks=""):
        self.usage_id = usage_id
        self.order_id = order_id
        self.part_id = part_id
        self.part_name = part_name
        self.part_source = part_source  # '库存配件' 或 '客户自带'
        self.quantity_used = quantity_used
        self.unit_price = unit_price
        self.subtotal = subtotal
        self.remarks = remarks

class PurchaseDetail:
    """进货明细记录"""
    
    def __init__(self, detail_id=None, order_id=None, part_id=None, 
                 quantity=0, unit_price=0.0, subtotal=0.0):
        self.detail_id = detail_id
        self.order_id = order_id
        self.part_id = part_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal

class RepairOrderDAO:
    """维修订单数据访问对象"""
    
    def __init__(self):
        self.db_manager = DatabaseManager(DATABASE_PATH)
    
    def add_repair_order(self, order, parts_usage=None):
        """添加维修订单（包含配件使用记录）"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # 插入维修订单
                query = '''
                    INSERT INTO repair_orders (customer_id, vehicle_type, vehicle_number, 
                                             repair_date, fault_description, repair_content, 
                                             labor_cost, parts_cost, total_amount, status, 
                                             technician, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (
                    order.customer_id, order.vehicle_type, order.vehicle_number,
                    order.repair_date, order.fault_description, order.repair_content,
                    order.labor_cost, order.parts_cost, order.total_amount,
                    order.status, order.technician, order.remarks
                )
                cursor.execute(query, params)
                order_id = cursor.lastrowid
                
                # 插入配件使用记录并更新库存
                if parts_usage:
                    for usage in parts_usage:
                        # 插入使用记录
                        usage_query = '''
                            INSERT INTO repair_parts_usage (order_id, part_id, part_name, part_source, 
                                                           quantity_used, unit_price, subtotal, remarks)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        '''
                        cursor.execute(usage_query, (
                            order_id, usage.part_id, usage.part_name, usage.part_source,
                            usage.quantity_used, usage.unit_price, usage.subtotal, usage.remarks
                        ))
                        
                        # 只有库存配件才需要更新库存
                        if usage.part_source == '库存配件' and usage.part_id:
                            stock_query = '''
                                UPDATE parts SET stock_quantity = stock_quantity - ?, 
                                               update_time = CURRENT_TIMESTAMP
                                WHERE part_id = ?
                            '''
                            cursor.execute(stock_query, (usage.quantity_used, usage.part_id))
                
                conn.commit()
                return order_id
            except Exception as e:
                conn.rollback()
                raise e
    
    def update_repair_order(self, order):
        """更新维修订单"""
        query = '''
            UPDATE repair_orders SET customer_id=?, vehicle_type=?, vehicle_number=?, 
                                   repair_date=?, fault_description=?, repair_content=?, 
                                   labor_cost=?, parts_cost=?, total_amount=?, status=?, 
                                   technician=?, remarks=?
            WHERE order_id=?
        '''
        params = (
            order.customer_id, order.vehicle_type, order.vehicle_number,
            order.repair_date, order.fault_description, order.repair_content,
            order.labor_cost, order.parts_cost, order.total_amount,
            order.status, order.technician, order.remarks, order.order_id
        )
        return self.db_manager.execute_update(query, params)
    
    def get_repair_order_by_id(self, order_id):
        """根据ID获取维修订单"""
        query = "SELECT * FROM repair_orders WHERE order_id=?"
        result = self.db_manager.execute_query(query, (order_id,))
        if result:
            return RepairOrder.from_dict(dict(result[0]))
        return None
    
    def get_repair_order_by_number(self, order_number):
        """根据订单号获取维修订单"""
        # 从订单号中提取ID（格式：RO000001）
        try:
            order_id = int(order_number[2:])  # 去掉"RO"前缀
            return self.get_repair_order_by_id(order_id)
        except (ValueError, IndexError):
            return None
    
    def get_all_repair_orders(self, limit=100):
        """获取所有维修订单"""
        query = "SELECT * FROM repair_orders ORDER BY repair_date DESC, order_id DESC LIMIT ?"
        results = self.db_manager.execute_query(query, (limit,))
        return [RepairOrder.from_dict(dict(row)) for row in results]
    
    def search_repair_orders(self, customer_name="", start_date=None, end_date=None, status=""):
        """搜索维修订单"""
        query = '''
            SELECT ro.*, c.customer_name 
            FROM repair_orders ro 
            LEFT JOIN customers c ON ro.customer_id = c.customer_id 
            WHERE 1=1
        '''
        params = []
        
        if customer_name:
            query += " AND c.customer_name LIKE ?"
            params.append(f"%{customer_name}%")
        
        if start_date:
            query += " AND ro.repair_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND ro.repair_date <= ?"
            params.append(end_date)
        
        if status:
            query += " AND ro.status = ?"
            params.append(status)
        
        query += " ORDER BY ro.repair_date DESC, ro.order_id DESC"
        results = self.db_manager.execute_query(query, params)
        return [RepairOrder.from_dict(dict(row)) for row in results]
    
    def get_repair_parts_usage(self, order_id):
        """获取维修订单的配件使用记录"""
        query = '''
            SELECT rpu.*, p.part_code, p.unit
            FROM repair_parts_usage rpu
            LEFT JOIN parts p ON rpu.part_id = p.part_id
            WHERE rpu.order_id = ?
        '''
        results = self.db_manager.execute_query(query, (order_id,))
        return [dict(row) for row in results]

class PurchaseOrderDAO:
    """进货订单数据访问对象"""
    
    def __init__(self):
        self.db_manager = DatabaseManager(DATABASE_PATH)
    
    def add_purchase_order(self, order, purchase_details=None):
        """添加进货订单（包含进货明细）"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # 插入进货订单
                query = '''
                    INSERT INTO purchase_orders (supplier_name, purchase_date, total_amount, 
                                                status, operator, remarks)
                    VALUES (?, ?, ?, ?, ?, ?)
                '''
                params = (
                    order.supplier_name, order.purchase_date, order.total_amount,
                    order.status, order.operator, order.remarks
                )
                cursor.execute(query, params)
                order_id = cursor.lastrowid
                
                # 插入进货明细并更新库存
                if purchase_details:
                    for detail in purchase_details:
                        # 插入明细记录
                        detail_query = '''
                            INSERT INTO purchase_details (order_id, part_id, quantity, unit_price, subtotal)
                            VALUES (?, ?, ?, ?, ?)
                        '''
                        cursor.execute(detail_query, (
                            order_id, detail.part_id, detail.quantity, 
                            detail.unit_price, detail.subtotal
                        ))
                        
                        # 更新库存
                        stock_query = '''
                            UPDATE parts SET stock_quantity = stock_quantity + ?, 
                                           update_time = CURRENT_TIMESTAMP
                            WHERE part_id = ?
                        '''
                        cursor.execute(stock_query, (detail.quantity, detail.part_id))
                
                conn.commit()
                return order_id
            except Exception as e:
                conn.rollback()
                raise e
    
    def get_all_purchase_orders(self, limit=100):
        """获取所有进货订单"""
        query = "SELECT * FROM purchase_orders ORDER BY purchase_date DESC, order_id DESC LIMIT ?"
        results = self.db_manager.execute_query(query, (limit,))
        return [PurchaseOrder.from_dict(dict(row)) for row in results]
    
    def get_purchase_details(self, order_id):
        """获取进货订单明细"""
        query = '''
            SELECT pd.*, p.part_name, p.part_code, p.unit
            FROM purchase_details pd
            LEFT JOIN parts p ON pd.part_id = p.part_id
            WHERE pd.order_id = ?
        '''
        results = self.db_manager.execute_query(query, (order_id,))
        return [dict(row) for row in results]