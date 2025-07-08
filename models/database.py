#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理模块
"""

import sqlite3
import logging
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        
    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        conn = None
        try:
            conn = sqlite3.connect(str(self.db_path), timeout=30)
            conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"数据库操作错误: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建配件表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parts (
                    part_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    part_name TEXT NOT NULL,
                    part_code TEXT UNIQUE,
                    category TEXT,
                    brand TEXT,
                    specification TEXT,
                    unit TEXT DEFAULT '个',
                    purchase_price REAL DEFAULT 0,
                    selling_price REAL DEFAULT 0,
                    stock_quantity INTEGER DEFAULT 0,
                    min_stock INTEGER DEFAULT 10,
                    supplier TEXT,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建客户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    phone TEXT,
                    address TEXT,
                    vehicle_info TEXT,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建进货单表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchase_orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_name TEXT NOT NULL,
                    purchase_date DATE NOT NULL,
                    total_amount REAL DEFAULT 0,
                    status TEXT DEFAULT '已完成',
                    operator TEXT,
                    remarks TEXT,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建进货明细表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchase_details (
                    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    part_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES purchase_orders (order_id),
                    FOREIGN KEY (part_id) REFERENCES parts (part_id)
                )
            ''')
            
            # 创建维修订单表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS repair_orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    vehicle_type TEXT,
                    vehicle_number TEXT,
                    repair_date DATE NOT NULL,
                    fault_description TEXT,
                    repair_content TEXT,
                    labor_cost REAL DEFAULT 0,
                    parts_cost REAL DEFAULT 0,
                    total_amount REAL DEFAULT 0,
                    status TEXT DEFAULT '进行中',
                    technician TEXT,
                    remarks TEXT,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    complete_time TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                )
            ''')
            
            # 创建维修配件消耗表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS repair_parts_usage (
                    usage_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    part_id INTEGER,
                    part_name TEXT NOT NULL,
                    part_source TEXT DEFAULT '库存配件',
                    quantity_used INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    remarks TEXT,
                    FOREIGN KEY (order_id) REFERENCES repair_orders (order_id),
                    FOREIGN KEY (part_id) REFERENCES parts (part_id)
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_name ON customers(customer_name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_repair_date ON repair_orders(repair_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_repair ON repair_orders(customer_id, repair_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_parts_usage ON repair_parts_usage(part_id, order_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_part_code ON parts(part_code)')
            
            conn.commit()
            logging.info("数据库初始化完成")
    
    def execute_query(self, query, params=None):
        """执行查询语句"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """执行更新语句"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    def execute_insert(self, query, params=None):
        """执行插入语句并返回新记录ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid