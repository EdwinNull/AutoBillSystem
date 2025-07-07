#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配件模型
"""

from datetime import datetime
from .database import DatabaseManager
from config.settings import DATABASE_PATH

class Part:
    """配件模型类"""
    
    def __init__(self, part_id=None, part_name="", part_code="", category="", 
                 brand="", specification="", unit="个", purchase_price=0.0, 
                 selling_price=0.0, stock_quantity=0, min_stock=10, supplier=""):
        self.part_id = part_id
        self.part_name = part_name
        self.part_code = part_code
        self.category = category
        self.brand = brand
        self.specification = specification
        self.unit = unit
        self.purchase_price = purchase_price
        self.selling_price = selling_price
        self.stock_quantity = stock_quantity
        self.min_stock = min_stock
        self.supplier = supplier
        self.create_time = None
        self.update_time = None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'part_id': self.part_id,
            'part_name': self.part_name,
            'part_code': self.part_code,
            'category': self.category,
            'brand': self.brand,
            'specification': self.specification,
            'unit': self.unit,
            'purchase_price': self.purchase_price,
            'selling_price': self.selling_price,
            'stock_quantity': self.stock_quantity,
            'min_stock': self.min_stock,
            'supplier': self.supplier
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        part = cls()
        for key, value in data.items():
            if hasattr(part, key):
                setattr(part, key, value)
        return part

class PartDAO:
    """配件数据访问对象"""
    
    def __init__(self):
        self.db_manager = DatabaseManager(DATABASE_PATH)
    
    def add_part(self, part):
        """添加配件"""
        query = '''
            INSERT INTO parts (part_name, part_code, category, brand, specification, 
                             unit, purchase_price, selling_price, stock_quantity, 
                             min_stock, supplier, update_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        '''
        params = (
            part.part_name, part.part_code, part.category, part.brand,
            part.specification, part.unit, part.purchase_price, part.selling_price,
            part.stock_quantity, part.min_stock, part.supplier
        )
        return self.db_manager.execute_insert(query, params)
    
    def update_part(self, part):
        """更新配件信息"""
        query = '''
            UPDATE parts SET part_name=?, part_code=?, category=?, brand=?, 
                           specification=?, unit=?, purchase_price=?, selling_price=?, 
                           stock_quantity=?, min_stock=?, supplier=?, 
                           update_time=CURRENT_TIMESTAMP
            WHERE part_id=?
        '''
        params = (
            part.part_name, part.part_code, part.category, part.brand,
            part.specification, part.unit, part.purchase_price, part.selling_price,
            part.stock_quantity, part.min_stock, part.supplier, part.part_id
        )
        return self.db_manager.execute_update(query, params)
    
    def delete_part(self, part_id):
        """删除配件"""
        query = "DELETE FROM parts WHERE part_id=?"
        return self.db_manager.execute_update(query, (part_id,))
    
    def get_part_by_id(self, part_id):
        """根据ID获取配件"""
        query = "SELECT * FROM parts WHERE part_id=?"
        result = self.db_manager.execute_query(query, (part_id,))
        if result:
            return Part.from_dict(dict(result[0]))
        return None
    
    def get_part_by_code(self, part_code):
        """根据编号获取配件"""
        query = "SELECT * FROM parts WHERE part_code=?"
        result = self.db_manager.execute_query(query, (part_code,))
        if result:
            return Part.from_dict(dict(result[0]))
        return None
    
    def get_all_parts(self):
        """获取所有配件"""
        query = "SELECT * FROM parts ORDER BY part_name"
        results = self.db_manager.execute_query(query)
        return [Part.from_dict(dict(row)) for row in results]
    
    def search_parts(self, keyword="", category=""):
        """搜索配件"""
        query = "SELECT * FROM parts WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (part_name LIKE ? OR part_code LIKE ? OR brand LIKE ?)"
            keyword_param = f"%{keyword}%"
            params.extend([keyword_param, keyword_param, keyword_param])
        
        if category:
            query += " AND category=?"
            params.append(category)
        
        query += " ORDER BY part_name"
        results = self.db_manager.execute_query(query, params)
        return [Part.from_dict(dict(row)) for row in results]
    
    def get_low_stock_parts(self):
        """获取库存不足的配件"""
        query = "SELECT * FROM parts WHERE stock_quantity <= min_stock ORDER BY stock_quantity"
        results = self.db_manager.execute_query(query)
        return [Part.from_dict(dict(row)) for row in results]
    
    def update_stock(self, part_id, quantity_change):
        """更新库存数量"""
        query = '''
            UPDATE parts SET stock_quantity = stock_quantity + ?, 
                           update_time = CURRENT_TIMESTAMP
            WHERE part_id = ?
        '''
        return self.db_manager.execute_update(query, (quantity_change, part_id))
    
    def get_categories(self):
        """获取所有配件类别"""
        query = "SELECT DISTINCT category FROM parts WHERE category IS NOT NULL AND category != '' ORDER BY category"
        results = self.db_manager.execute_query(query)
        return [row[0] for row in results]