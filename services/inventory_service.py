#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存服务
"""

from models.parts import PartDAO, Part
from models.orders import PurchaseOrderDAO, PurchaseOrder, PurchaseDetail
from datetime import date

class InventoryService:
    """库存管理服务"""
    
    def __init__(self):
        self.part_dao = PartDAO()
        self.purchase_dao = PurchaseOrderDAO()
    
    def add_part(self, part_data):
        """添加配件"""
        # 验证配件编号唯一性
        if part_data.get('part_code'):
            existing_part = self.part_dao.get_part_by_code(part_data['part_code'])
            if existing_part:
                raise ValueError(f"配件编号 {part_data['part_code']} 已存在")
        
        part = Part.from_dict(part_data)
        return self.part_dao.add_part(part)
    
    def update_part(self, part_data):
        """更新配件信息"""
        part = Part.from_dict(part_data)
        return self.part_dao.update_part(part)
    
    def delete_part(self, part_id):
        """删除配件"""
        # 检查是否有相关的使用记录
        # 这里可以添加更多的业务逻辑验证
        return self.part_dao.delete_part(part_id)
    
    def get_all_parts(self):
        """获取所有配件"""
        return self.part_dao.get_all_parts()
    
    def search_parts(self, keyword="", category=""):
        """搜索配件"""
        return self.part_dao.search_parts(keyword, category)
    
    def get_low_stock_parts(self):
        """获取库存不足的配件"""
        return self.part_dao.get_low_stock_parts()
    
    def get_part_categories(self):
        """获取配件类别"""
        return self.part_dao.get_categories()
    
    def create_purchase_order(self, supplier_name, operator, parts_list, remarks=""):
        """创建进货订单"""
        # 计算总金额
        total_amount = sum(item['quantity'] * item['unit_price'] for item in parts_list)
        
        # 创建进货订单
        order = PurchaseOrder(
            supplier_name=supplier_name,
            purchase_date=date.today(),
            total_amount=total_amount,
            operator=operator,
            remarks=remarks
        )
        
        # 创建进货明细
        purchase_details = []
        for item in parts_list:
            detail = PurchaseDetail(
                part_id=item['part_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                subtotal=item['quantity'] * item['unit_price']
            )
            purchase_details.append(detail)
        
        # 保存订单和明细
        return self.purchase_dao.add_purchase_order(order, purchase_details)
    
    def get_purchase_orders(self):
        """获取进货订单列表"""
        return self.purchase_dao.get_all_purchase_orders()
    
    def get_purchase_order_details(self, order_id):
        """获取进货订单明细"""
        return self.purchase_dao.get_purchase_details(order_id)
    
    def get_inventory_statistics(self):
        """获取库存统计信息"""
        all_parts = self.get_all_parts()
        low_stock_parts = self.get_low_stock_parts()
        
        total_parts = len(all_parts)
        total_value = sum(part.stock_quantity * part.purchase_price for part in all_parts)
        low_stock_count = len(low_stock_parts)
        
        return {
            'total_parts': total_parts,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'low_stock_parts': low_stock_parts
        }