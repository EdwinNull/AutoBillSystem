#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单服务
"""

from models.orders import RepairOrderDAO, RepairOrder, RepairPartsUsage
from models.customers import CustomerDAO, Customer
from models.parts import PartDAO
from datetime import date, datetime

class OrderService:
    """订单管理服务"""
    
    def __init__(self):
        self.repair_dao = RepairOrderDAO()
        self.customer_dao = CustomerDAO()
        self.part_dao = PartDAO()
    
    def add_customer(self, customer_data):
        """添加客户"""
        customer = Customer.from_dict(customer_data)
        return self.customer_dao.add_customer(customer)
    
    def update_customer(self, customer_data):
        """更新客户信息"""
        customer = Customer.from_dict(customer_data)
        return self.customer_dao.update_customer(customer)
    
    def get_all_customers(self):
        """获取所有客户"""
        return self.customer_dao.get_all_customers()
    
    def search_customers(self, keyword=""):
        """搜索客户"""
        return self.customer_dao.search_customers(keyword)
    
    def get_customer_by_id(self, customer_id):
        """根据ID获取客户"""
        return self.customer_dao.get_customer_by_id(customer_id)
    
    def delete_customer(self, customer_id):
        """删除客户"""
        return self.customer_dao.delete_customer(customer_id)
    
    def create_repair_order(self, order_data, parts_usage_list=None):
        """创建维修订单"""
        # 验证客户是否存在
        customer = self.customer_dao.get_customer_by_id(order_data['customer_id'])
        if not customer:
            raise ValueError("客户不存在")
        
        # 计算配件费用
        parts_cost = 0
        parts_usage = []
        
        if parts_usage_list:
            for usage_data in parts_usage_list:
                # 验证配件是否存在和库存是否充足
                part = self.part_dao.get_part_by_id(usage_data['part_id'])
                if not part:
                    raise ValueError(f"配件ID {usage_data['part_id']} 不存在")
                
                if part.stock_quantity < usage_data['quantity_used']:
                    raise ValueError(f"配件 {part.part_name} 库存不足")
                
                subtotal = usage_data['quantity_used'] * usage_data['unit_price']
                parts_cost += subtotal
                
                usage = RepairPartsUsage(
                    part_id=usage_data['part_id'],
                    quantity_used=usage_data['quantity_used'],
                    unit_price=usage_data['unit_price'],
                    subtotal=subtotal
                )
                parts_usage.append(usage)
        
        # 计算总金额
        labor_cost = order_data.get('labor_cost', 0)
        total_amount = labor_cost + parts_cost
        
        # 创建维修订单
        order = RepairOrder(
            customer_id=order_data['customer_id'],
            vehicle_type=order_data.get('vehicle_type', ''),
            vehicle_number=order_data.get('vehicle_number', ''),
            repair_date=order_data.get('repair_date', date.today()),
            fault_description=order_data.get('fault_description', ''),
            repair_content=order_data.get('repair_content', ''),
            labor_cost=labor_cost,
            parts_cost=parts_cost,
            total_amount=total_amount,
            status=order_data.get('status', '进行中'),
            technician=order_data.get('technician', ''),
            remarks=order_data.get('remarks', '')
        )
        
        return self.repair_dao.add_repair_order(order, parts_usage)
    
    def update_repair_order(self, order_data):
        """更新维修订单"""
        order = RepairOrder.from_dict(order_data)
        return self.repair_dao.update_repair_order(order)
    
    def get_repair_order_by_id(self, order_id):
        """根据ID获取维修订单"""
        return self.repair_dao.get_repair_order_by_id(order_id)
    
    def get_all_repair_orders(self, limit=100):
        """获取所有维修订单"""
        return self.repair_dao.get_all_repair_orders(limit)
    
    def get_all_orders(self, limit=100):
        """获取所有订单（别名方法）"""
        return self.get_all_repair_orders(limit)
    
    def get_order_details(self, order_number):
        """获取订单详情（通过订单号）"""
        order = self.repair_dao.get_repair_order_by_number(order_number)
        if not order:
            return None
        
        # 获取客户信息
        customer = self.customer_dao.get_customer_by_id(order.customer_id)
        
        # 获取配件使用记录
        parts_usage = self.repair_dao.get_repair_parts_usage(order.order_id)
        
        return {
            'order': order,
            'customer': customer,
            'parts_usage': parts_usage
        }
    
    def complete_order(self, order_number):
        """完成订单（通过订单号）"""
        order = self.repair_dao.get_repair_order_by_number(order_number)
        if not order:
            raise ValueError("订单不存在")
        
        order.status = "已完成"
        order.complete_time = datetime.now()
        return self.repair_dao.update_repair_order(order)
    
    def search_repair_orders(self, customer_name="", start_date=None, end_date=None, status=""):
        """搜索维修订单"""
        return self.repair_dao.search_repair_orders(customer_name, start_date, end_date, status)
    
    def get_repair_order_details(self, order_id):
        """获取维修订单详细信息（包含配件使用记录）"""
        order = self.repair_dao.get_repair_order_by_id(order_id)
        if not order:
            return None
        
        # 获取客户信息
        customer = self.customer_dao.get_customer_by_id(order.customer_id)
        
        # 获取配件使用记录
        parts_usage = self.repair_dao.get_repair_parts_usage(order_id)
        
        return {
            'order': order,
            'customer': customer,
            'parts_usage': parts_usage
        }
    
    def complete_repair_order(self, order_id):
        """完成维修订单"""
        order = self.repair_dao.get_repair_order_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")
        
        order.status = "已完成"
        order.complete_time = datetime.now()
        return self.repair_dao.update_repair_order(order)
    
    def get_customer_repair_history(self, customer_id):
        """获取客户维修历史"""
        return self.repair_dao.search_repair_orders(
            customer_name="", 
            start_date=None, 
            end_date=None, 
            status=""
        )
    
    def get_order_statistics(self, start_date=None, end_date=None):
        """获取订单统计信息"""
        orders = self.repair_dao.search_repair_orders(
            customer_name="",
            start_date=start_date,
            end_date=end_date,
            status=""
        )
        
        total_orders = len(orders)
        completed_orders = len([o for o in orders if o.status == "已完成"])
        total_revenue = sum(o.total_amount for o in orders if o.status == "已完成")
        total_labor_cost = sum(o.labor_cost for o in orders if o.status == "已完成")
        total_parts_cost = sum(o.parts_cost for o in orders if o.status == "已完成")
        
        return {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': total_orders - completed_orders,
            'total_revenue': total_revenue,
            'total_labor_cost': total_labor_cost,
            'total_parts_cost': total_parts_cost
        }