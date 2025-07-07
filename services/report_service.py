#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报表服务
"""

from models.database import DatabaseManager
from config.settings import DATABASE_PATH
from datetime import datetime, date, timedelta
import json

class ReportService:
    """报表服务"""
    
    def __init__(self):
        self.db_manager = DatabaseManager(DATABASE_PATH)
    
    def get_daily_revenue_report(self, target_date=None):
        """获取日收入报表"""
        if not target_date:
            target_date = date.today()
        
        query = '''
            SELECT 
                COUNT(*) as order_count,
                SUM(total_amount) as total_revenue,
                SUM(labor_cost) as total_labor,
                SUM(parts_cost) as total_parts
            FROM repair_orders 
            WHERE repair_date = ? AND status = '已完成'
        '''
        
        result = self.db_manager.execute_query(query, (target_date,))
        if result:
            row = dict(result[0])
            return {
                'date': target_date,
                'order_count': row['order_count'] or 0,
                'total_revenue': row['total_revenue'] or 0,
                'total_labor': row['total_labor'] or 0,
                'total_parts': row['total_parts'] or 0
            }
        return None
    
    def get_monthly_revenue_report(self, year=None, month=None):
        """获取月收入报表"""
        if not year:
            year = date.today().year
        if not month:
            month = date.today().month
        
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        query = '''
            SELECT 
                repair_date,
                COUNT(*) as order_count,
                SUM(total_amount) as daily_revenue,
                SUM(labor_cost) as daily_labor,
                SUM(parts_cost) as daily_parts
            FROM repair_orders 
            WHERE repair_date BETWEEN ? AND ? AND status = '已完成'
            GROUP BY repair_date
            ORDER BY repair_date
        '''
        
        results = self.db_manager.execute_query(query, (start_date, end_date))
        daily_data = [dict(row) for row in results]
        
        # 计算月度汇总
        total_orders = sum(row['order_count'] for row in daily_data)
        total_revenue = sum(row['daily_revenue'] for row in daily_data)
        total_labor = sum(row['daily_labor'] for row in daily_data)
        total_parts = sum(row['daily_parts'] for row in daily_data)
        
        return {
            'year': year,
            'month': month,
            'start_date': start_date,
            'end_date': end_date,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_labor': total_labor,
            'total_parts': total_parts,
            'daily_data': daily_data
        }
    
    def get_parts_usage_report(self, start_date=None, end_date=None):
        """获取配件使用报表"""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        query = '''
            SELECT 
                p.part_name,
                p.part_code,
                p.category,
                p.unit,
                SUM(rpu.quantity_used) as total_used,
                SUM(rpu.subtotal) as total_amount,
                AVG(rpu.unit_price) as avg_price
            FROM repair_parts_usage rpu
            JOIN parts p ON rpu.part_id = p.part_id
            JOIN repair_orders ro ON rpu.order_id = ro.order_id
            WHERE ro.repair_date BETWEEN ? AND ?
            GROUP BY p.part_id, p.part_name, p.part_code, p.category, p.unit
            ORDER BY total_used DESC
        '''
        
        results = self.db_manager.execute_query(query, (start_date, end_date))
        return [dict(row) for row in results]
    
    def get_customer_analysis_report(self, start_date=None, end_date=None):
        """获取客户分析报表"""
        if not start_date:
            start_date = date.today() - timedelta(days=365)
        if not end_date:
            end_date = date.today()
        
        query = '''
            SELECT 
                c.customer_name,
                c.phone,
                c.vehicle_info,
                COUNT(ro.order_id) as order_count,
                SUM(ro.total_amount) as total_spent,
                AVG(ro.total_amount) as avg_order_value,
                MAX(ro.repair_date) as last_visit_date
            FROM customers c
            LEFT JOIN repair_orders ro ON c.customer_id = ro.customer_id
            WHERE ro.repair_date BETWEEN ? AND ? OR ro.repair_date IS NULL
            GROUP BY c.customer_id, c.customer_name, c.phone, c.vehicle_info
            ORDER BY total_spent DESC
        '''
        
        results = self.db_manager.execute_query(query, (start_date, end_date))
        return [dict(row) for row in results]
    
    def get_inventory_report(self):
        """获取库存报表"""
        query = '''
            SELECT 
                part_name,
                part_code,
                category,
                brand,
                unit,
                stock_quantity,
                min_stock,
                purchase_price,
                selling_price,
                (stock_quantity * purchase_price) as inventory_value,
                CASE 
                    WHEN stock_quantity <= min_stock THEN '库存不足'
                    WHEN stock_quantity <= min_stock * 2 THEN '库存偏低'
                    ELSE '库存正常'
                END as stock_status
            FROM parts
            ORDER BY stock_status, stock_quantity
        '''
        
        results = self.db_manager.execute_query(query)
        return [dict(row) for row in results]
    
    def get_supplier_analysis_report(self, start_date=None, end_date=None):
        """获取供应商分析报表"""
        if not start_date:
            start_date = date.today() - timedelta(days=365)
        if not end_date:
            end_date = date.today()
        
        query = '''
            SELECT 
                supplier_name,
                COUNT(*) as order_count,
                SUM(total_amount) as total_purchase,
                AVG(total_amount) as avg_order_value,
                MAX(purchase_date) as last_purchase_date
            FROM purchase_orders
            WHERE purchase_date BETWEEN ? AND ?
            GROUP BY supplier_name
            ORDER BY total_purchase DESC
        '''
        
        results = self.db_manager.execute_query(query, (start_date, end_date))
        return [dict(row) for row in results]
    
    def get_profit_analysis_report(self, start_date=None, end_date=None):
        """获取利润分析报表"""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # 获取维修收入
        repair_query = '''
            SELECT 
                SUM(total_amount) as total_revenue,
                SUM(labor_cost) as total_labor,
                SUM(parts_cost) as total_parts_revenue
            FROM repair_orders
            WHERE repair_date BETWEEN ? AND ? AND status = '已完成'
        '''
        
        repair_result = self.db_manager.execute_query(repair_query, (start_date, end_date))
        repair_data = dict(repair_result[0]) if repair_result else {}
        
        # 获取配件成本
        parts_cost_query = '''
            SELECT 
                SUM(rpu.quantity_used * p.purchase_price) as total_parts_cost
            FROM repair_parts_usage rpu
            JOIN parts p ON rpu.part_id = p.part_id
            JOIN repair_orders ro ON rpu.order_id = ro.order_id
            WHERE ro.repair_date BETWEEN ? AND ? AND ro.status = '已完成'
        '''
        
        parts_cost_result = self.db_manager.execute_query(parts_cost_query, (start_date, end_date))
        parts_cost_data = dict(parts_cost_result[0]) if parts_cost_result else {}
        
        total_revenue = repair_data.get('total_revenue', 0) or 0
        total_labor = repair_data.get('total_labor', 0) or 0
        total_parts_revenue = repair_data.get('total_parts_revenue', 0) or 0
        total_parts_cost = parts_cost_data.get('total_parts_cost', 0) or 0
        
        parts_profit = total_parts_revenue - total_parts_cost
        total_profit = total_labor + parts_profit
        profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_revenue': total_revenue,
            'total_labor': total_labor,
            'total_parts_revenue': total_parts_revenue,
            'total_parts_cost': total_parts_cost,
            'parts_profit': parts_profit,
            'total_profit': total_profit,
            'profit_margin': round(profit_margin, 2)
        }
    
    def export_report_to_json(self, report_data, filename):
        """导出报表为JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
            return True
        except Exception as e:
            print(f"导出报表失败: {e}")
            return False