#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示数据生成脚本
用于为汽修店记账软件添加示例数据
"""

import sys
import os
from datetime import datetime, date, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.inventory_service import InventoryService
from services.order_service import OrderService

def create_demo_parts():
    """创建演示配件数据"""
    inventory_service = InventoryService()
    
    demo_parts = [
        {
            'part_name': '机油滤清器',
            'part_code': 'OF001',
            'category': '滤清器',
            'brand': '博世',
            'specification': '适用于大众/奥迪',
            'unit': '个',
            'purchase_price': 25.00,
            'selling_price': 45.00,
            'stock_quantity': 50,
            'min_stock': 10,
            'supplier': '博世汽配'
        },
        {
            'part_name': '空气滤清器',
            'part_code': 'AF001',
            'category': '滤清器',
            'brand': '曼牌',
            'specification': '适用于宝马',
            'unit': '个',
            'purchase_price': 35.00,
            'selling_price': 65.00,
            'stock_quantity': 30,
            'min_stock': 8,
            'supplier': '曼牌汽配'
        },
        {
            'part_name': '刹车片',
            'part_code': 'BP001',
            'category': '制动系统',
            'brand': '布雷博',
            'specification': '前轮刹车片',
            'unit': '套',
            'purchase_price': 120.00,
            'selling_price': 200.00,
            'stock_quantity': 25,
            'min_stock': 5,
            'supplier': '布雷博中国'
        },
        {
            'part_name': '火花塞',
            'part_code': 'SP001',
            'category': '点火系统',
            'brand': 'NGK',
            'specification': '铱金火花塞',
            'unit': '个',
            'purchase_price': 45.00,
            'selling_price': 80.00,
            'stock_quantity': 40,
            'min_stock': 12,
            'supplier': 'NGK官方'
        },
        {
            'part_name': '机油',
            'part_code': 'OIL001',
            'category': '润滑油',
            'brand': '美孚',
            'specification': '5W-30全合成机油',
            'unit': '升',
            'purchase_price': 35.00,
            'selling_price': 60.00,
            'stock_quantity': 100,
            'min_stock': 20,
            'supplier': '美孚润滑油'
        },
        {
            'part_name': '轮胎',
            'part_code': 'TIRE001',
            'category': '轮胎',
            'brand': '米其林',
            'specification': '225/60R16',
            'unit': '条',
            'purchase_price': 450.00,
            'selling_price': 650.00,
            'stock_quantity': 16,
            'min_stock': 4,
            'supplier': '米其林轮胎'
        },
        {
            'part_name': '雨刷片',
            'part_code': 'WB001',
            'category': '车身配件',
            'brand': '博世',
            'specification': '24寸无骨雨刷',
            'unit': '对',
            'purchase_price': 25.00,
            'selling_price': 45.00,
            'stock_quantity': 20,
            'min_stock': 6,
            'supplier': '博世汽配'
        },
        {
            'part_name': '蓄电池',
            'part_code': 'BAT001',
            'category': '电气系统',
            'brand': '瓦尔塔',
            'specification': '12V 60Ah',
            'unit': '个',
            'purchase_price': 280.00,
            'selling_price': 450.00,
            'stock_quantity': 8,
            'min_stock': 3,
            'supplier': '瓦尔塔电池'
        }
    ]
    
    print("正在创建演示配件数据...")
    for part_data in demo_parts:
        try:
            inventory_service.add_part(part_data)
            print(f"✓ 已添加配件: {part_data['part_name']}")
        except Exception as e:
            print(f"✗ 添加配件失败 {part_data['part_name']}: {e}")

def create_demo_customers():
    """创建演示客户数据"""
    order_service = OrderService()
    
    demo_customers = [
        {
            'customer_name': '张三',
            'phone': '13800138001',
            'license_plate': '京A12345',
            'car_model': '大众帕萨特',
            'car_color': '白色',
            'engine_number': 'VW123456',
            'vin': 'WVWZZZ3CZDE123456',
            'address': '北京市朝阳区建国路88号',
            'notes': 'VIP客户，定期保养'
        },
        {
            'customer_name': '李四',
            'phone': '13900139002',
            'license_plate': '京B67890',
            'car_model': '宝马320i',
            'car_color': '黑色',
            'engine_number': 'BMW789012',
            'vin': 'WBAVA31070F123456',
            'address': '北京市海淀区中关村大街1号',
            'notes': '喜欢原厂配件'
        },
        {
            'customer_name': '王五',
            'phone': '13700137003',
            'license_plate': '京C11111',
            'car_model': '奥迪A4L',
            'car_color': '银色',
            'engine_number': 'AUDI345678',
            'vin': 'WAUZZZ8E2DA123456',
            'address': '北京市西城区金融街15号',
            'notes': '商务用车，要求快速维修'
        },
        {
            'customer_name': '赵六',
            'phone': '13600136004',
            'license_plate': '京D22222',
            'car_model': '丰田凯美瑞',
            'car_color': '红色',
            'engine_number': 'TOYOTA901234',
            'vin': 'JTNBE46K403123456',
            'address': '北京市东城区王府井大街100号',
            'notes': '家庭用车，注重性价比'
        },
        {
            'customer_name': '钱七',
            'phone': '13500135005',
            'license_plate': '京E33333',
            'car_model': '本田雅阁',
            'car_color': '蓝色',
            'engine_number': 'HONDA567890',
            'vin': 'JHMCG56457C123456',
            'address': '北京市丰台区南三环西路88号',
            'notes': '新客户，首次维修'
        }
    ]
    
    print("\n正在创建演示客户数据...")
    for customer_data in demo_customers:
        try:
            order_service.add_customer(customer_data)
            print(f"✓ 已添加客户: {customer_data['customer_name']} ({customer_data['license_plate']})")
        except Exception as e:
            print(f"✗ 添加客户失败 {customer_data['customer_name']}: {e}")

def create_demo_orders():
    """创建演示订单数据"""
    order_service = OrderService()
    
    # 获取客户列表
    customers = order_service.get_all_customers()
    if not customers:
        print("没有客户数据，无法创建订单")
        return
    
    # 创建一些演示订单
    demo_orders = [
        {
            'customer_id': customers[0].customer_id,
            'repair_date': date.today() - timedelta(days=5),
            'fault_description': '发动机异响，怠速不稳',
            'repair_content': '更换机油滤清器，清洗节气门，调整怠速',
            'labor_cost': 150.00,
            'parts_used': [
                {'part_id': 1, 'quantity': 1, 'unit_price': 45.00},  # 机油滤清器
                {'part_id': 5, 'quantity': 4, 'unit_price': 60.00}   # 机油
            ]
        },
        {
            'customer_id': customers[1].customer_id,
            'repair_date': date.today() - timedelta(days=3),
            'fault_description': '刹车异响，制动距离变长',
            'repair_content': '更换前轮刹车片，检查刹车盘',
            'labor_cost': 200.00,
            'parts_used': [
                {'part_id': 3, 'quantity': 1, 'unit_price': 200.00}  # 刹车片
            ]
        },
        {
            'customer_id': customers[2].customer_id,
            'repair_date': date.today() - timedelta(days=1),
            'fault_description': '定期保养',
            'repair_content': '更换机油、机滤、空滤、火花塞',
            'labor_cost': 120.00,
            'parts_used': [
                {'part_id': 1, 'quantity': 1, 'unit_price': 45.00},  # 机油滤清器
                {'part_id': 2, 'quantity': 1, 'unit_price': 65.00},  # 空气滤清器
                {'part_id': 4, 'quantity': 4, 'unit_price': 80.00},  # 火花塞
                {'part_id': 5, 'quantity': 4, 'unit_price': 60.00}   # 机油
            ]
        }
    ]
    
    print("\n正在创建演示订单数据...")
    for i, order_data in enumerate(demo_orders):
        try:
            order_id = order_service.create_repair_order(order_data)
            print(f"✓ 已创建订单: {order_id}")
            
            # 完成前两个订单
            if i < 2:
                order_service.complete_order(order_id)
                print(f"  └─ 订单 {order_id} 已完成")
        except Exception as e:
            print(f"✗ 创建订单失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("汽修店记账软件 - 演示数据生成器")
    print("=" * 50)
    
    try:
        # 创建演示数据
        create_demo_parts()
        create_demo_customers()
        create_demo_orders()
        
        print("\n" + "=" * 50)
        print("✓ 演示数据创建完成！")
        print("\n现在您可以：")
        print("1. 运行 python main.py 启动主程序")
        print("2. 在配件管理中查看和管理配件")
        print("3. 在客户管理中查看客户信息")
        print("4. 在订单管理中查看维修订单")
        print("5. 查看各种统计报表")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ 创建演示数据时出错: {e}")
        print("请检查数据库连接和配置")

if __name__ == "__main__":
    main()