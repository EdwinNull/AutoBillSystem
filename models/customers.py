#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户模型
"""

from datetime import datetime
from .database import DatabaseManager
from config.settings import DATABASE_PATH

class Customer:
    """客户模型类"""
    
    def __init__(self, customer_id=None, customer_name="", phone="", 
                 address="", vehicle_info="", license_plate="", car_model="",
                 car_color="", engine_number="", vin="", notes=""):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.vehicle_info = vehicle_info
        self.license_plate = license_plate
        self.car_model = car_model
        self.car_color = car_color
        self.engine_number = engine_number
        self.vin = vin
        self.notes = notes
        self.create_time = None
        self.created_at = None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'phone': self.phone,
            'address': self.address,
            'vehicle_info': self.vehicle_info
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        customer = cls()
        for key, value in data.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        
        # 处理日期字段
        if 'create_time' in data and data['create_time']:
            try:
                if isinstance(data['create_time'], str):
                    customer.created_at = datetime.strptime(data['create_time'], '%Y-%m-%d %H:%M:%S')
                else:
                    customer.created_at = data['create_time']
            except (ValueError, TypeError):
                customer.created_at = None
        
        return customer

class CustomerDAO:
    """客户数据访问对象"""
    
    def __init__(self):
        self.db_manager = DatabaseManager(DATABASE_PATH)
    
    def add_customer(self, customer):
        """添加客户"""
        query = '''
            INSERT INTO customers (customer_name, phone, license_plate, car_model, 
                                 car_color, engine_number, vin, address, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            customer.customer_name, customer.phone, customer.license_plate,
            customer.car_model, customer.car_color, customer.engine_number,
            customer.vin, customer.address, customer.notes
        )
        return self.db_manager.execute_insert(query, params)
    
    def update_customer(self, customer):
        """更新客户信息"""
        query = '''
            UPDATE customers SET customer_name=?, phone=?, license_plate=?, car_model=?,
                               car_color=?, engine_number=?, vin=?, address=?, notes=?
            WHERE customer_id=?
        '''
        params = (
            customer.customer_name, customer.phone, customer.license_plate,
            customer.car_model, customer.car_color, customer.engine_number,
            customer.vin, customer.address, customer.notes, customer.customer_id
        )
        return self.db_manager.execute_update(query, params)
    
    def delete_customer(self, customer_id):
        """删除客户"""
        query = "DELETE FROM customers WHERE customer_id=?"
        return self.db_manager.execute_update(query, (customer_id,))
    
    def get_customer_by_id(self, customer_id):
        """根据ID获取客户"""
        query = "SELECT * FROM customers WHERE customer_id=?"
        result = self.db_manager.execute_query(query, (customer_id,))
        if result:
            return Customer.from_dict(dict(result[0]))
        return None
    
    def get_all_customers(self):
        """获取所有客户"""
        query = "SELECT * FROM customers ORDER BY customer_name"
        results = self.db_manager.execute_query(query)
        return [Customer.from_dict(dict(row)) for row in results]
    
    def search_customers(self, keyword=""):
        """搜索客户"""
        if not keyword:
            return self.get_all_customers()
        
        query = '''
            SELECT * FROM customers 
            WHERE customer_name LIKE ? OR phone LIKE ? OR license_plate LIKE ? 
               OR car_model LIKE ? OR notes LIKE ?
            ORDER BY customer_name
        '''
        keyword_param = f"%{keyword}%"
        params = [keyword_param, keyword_param, keyword_param, keyword_param, keyword_param]
        results = self.db_manager.execute_query(query, params)
        return [Customer.from_dict(dict(row)) for row in results]
    
    def get_customer_by_name(self, customer_name):
        """根据姓名获取客户"""
        query = "SELECT * FROM customers WHERE customer_name=?"
        result = self.db_manager.execute_query(query, (customer_name,))
        if result:
            return Customer.from_dict(dict(result[0]))
        return None
    
    def get_customer_by_phone(self, phone):
        """根据电话获取客户"""
        query = "SELECT * FROM customers WHERE phone=?"
        result = self.db_manager.execute_query(query, (phone,))
        if result:
            return Customer.from_dict(dict(result[0]))
        return None