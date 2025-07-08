#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维修订单管理窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from services.order_service import OrderService
from services.inventory_service import InventoryService
from models.orders import RepairOrder

class OrdersWindow:
    """维修订单管理窗口"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.order_service = OrderService()
        self.inventory_service = InventoryService()
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.setup_window()
        self.setup_widgets()
        self.load_orders()
    
    def setup_window(self):
        """设置窗口属性"""
        self.window.title("维修订单管理")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        
        # 居中显示
        if self.parent:
            self.window.transient(self.parent)
            self.window.grab_set()
    
    def setup_widgets(self):
        """设置界面控件"""
        # 创建笔记本控件（标签页）
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 订单列表标签页
        self.list_frame = ttk.Frame(notebook)
        notebook.add(self.list_frame, text="订单列表")
        self.setup_list_tab()
        
        # 新建订单标签页
        self.new_frame = ttk.Frame(notebook)
        notebook.add(self.new_frame, text="新建订单")
        self.setup_new_order_tab()
    
    def setup_list_tab(self):
        """设置订单列表标签页"""
        # 搜索框架
        search_frame = ttk.LabelFrame(self.list_frame, text="搜索订单", padding="5")
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        ttk.Label(search_frame, text="订单号:").grid(row=0, column=0, padx=(0, 5))
        self.search_order_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_order_var, width=15).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(search_frame, text="客户:").grid(row=0, column=2, padx=(0, 5))
        self.search_customer_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_customer_var, width=15).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(search_frame, text="状态:").grid(row=0, column=4, padx=(0, 5))
        self.search_status_var = tk.StringVar()
        status_combo = ttk.Combobox(search_frame, textvariable=self.search_status_var, 
                                   values=["", "待维修", "维修中", "已完成", "已取消"], width=12)
        status_combo.grid(row=0, column=5, padx=(0, 10))
        
        ttk.Button(search_frame, text="搜索", command=self.search_orders).grid(row=0, column=6, padx=(0, 5))
        ttk.Button(search_frame, text="重置", command=self.reset_search).grid(row=0, column=7)
        
        # 订单列表框架
        list_container = ttk.Frame(self.list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 订单列表
        columns = ('订单号', '客户', '车牌号', '维修日期', '故障描述', '总费用', '状态')
        self.orders_tree = ttk.Treeview(list_container, columns=columns, show='headings', height=15)
        
        # 设置列标题和宽度
        column_widths = {'订单号': 100, '客户': 100, '车牌号': 100, '维修日期': 100, 
                        '故障描述': 200, '总费用': 80, '状态': 80}
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=column_widths.get(col, 100))
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.orders_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_container, orient=tk.HORIZONTAL, command=self.orders_tree.xview)
        self.orders_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定双击事件
        self.orders_tree.bind('<Double-1>', self.view_order_detail)
        
        # 操作按钮框架
        button_frame = ttk.Frame(self.list_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="查看详情", command=self.view_order_detail).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="完成订单", command=self.complete_order).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="取消订单", command=self.cancel_order).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="刷新", command=self.load_orders).pack(side=tk.RIGHT)
    
    def setup_new_order_tab(self):
        """设置新建订单标签页"""
        # 主框架
        main_frame = ttk.Frame(self.new_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：客户信息
        customer_frame = ttk.LabelFrame(main_frame, text="客户信息", padding="10")
        customer_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 客户选择
        ttk.Label(customer_frame, text="选择客户:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_frame, textvariable=self.customer_var, width=25)
        self.customer_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        self.customer_combo.bind('<<ComboboxSelected>>', self.on_customer_select)
        
        ttk.Button(customer_frame, text="新建客户", command=self.new_customer).grid(row=0, column=2, padx=(5, 0))
        
        # 客户详情显示
        ttk.Label(customer_frame, text="联系电话:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.customer_phone_var = tk.StringVar()
        ttk.Label(customer_frame, textvariable=self.customer_phone_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(customer_frame, text="车牌号:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.customer_plate_var = tk.StringVar()
        ttk.Label(customer_frame, textvariable=self.customer_plate_var).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(customer_frame, text="车型:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.customer_car_var = tk.StringVar()
        ttk.Label(customer_frame, textvariable=self.customer_car_var).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # 右侧：订单信息
        order_frame = ttk.LabelFrame(main_frame, text="订单信息", padding="10")
        order_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 维修日期
        ttk.Label(order_frame, text="维修日期:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.repair_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        ttk.Entry(order_frame, textvariable=self.repair_date_var, width=25).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 故障描述
        ttk.Label(order_frame, text="故障描述:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.fault_text = tk.Text(order_frame, width=25, height=3)
        self.fault_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 维修内容
        ttk.Label(order_frame, text="维修内容:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.repair_text = tk.Text(order_frame, width=25, height=3)
        self.repair_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 工时费
        ttk.Label(order_frame, text="工时费:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.labor_cost_var = tk.StringVar(value="0.00")
        ttk.Entry(order_frame, textvariable=self.labor_cost_var, width=25).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 配件使用框架
        parts_frame = ttk.LabelFrame(main_frame, text="使用配件", padding="10")
        parts_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # 配件选择
        parts_select_frame = ttk.Frame(parts_frame)
        parts_select_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行：配件来源选择
        source_frame = ttk.Frame(parts_select_frame)
        source_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(source_frame, text="配件来源:").pack(side=tk.LEFT, padx=(0, 5))
        self.part_source_var = tk.StringVar(value="库存配件")
        source_combo = ttk.Combobox(source_frame, textvariable=self.part_source_var, 
                                   values=["库存配件", "客户自带"], width=12, state="readonly")
        source_combo.pack(side=tk.LEFT, padx=(0, 10))
        source_combo.bind('<<ComboboxSelected>>', self.on_part_source_change)
        
        # 第二行：配件选择/输入
        part_frame = ttk.Frame(parts_select_frame)
        part_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(part_frame, text="配件名称:").pack(side=tk.LEFT, padx=(0, 5))
        self.part_var = tk.StringVar()
        self.part_combo = ttk.Combobox(part_frame, textvariable=self.part_var, width=20)
        self.part_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # 客户自带配件名称输入框（初始隐藏）
        self.custom_part_var = tk.StringVar()
        self.custom_part_entry = ttk.Entry(part_frame, textvariable=self.custom_part_var, width=22)
        
        ttk.Label(part_frame, text="数量:").pack(side=tk.LEFT, padx=(0, 5))
        self.part_quantity_var = tk.StringVar(value="1")
        ttk.Entry(part_frame, textvariable=self.part_quantity_var, width=8).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(part_frame, text="单价:").pack(side=tk.LEFT, padx=(0, 5))
        self.part_price_var = tk.StringVar(value="0.00")
        ttk.Entry(part_frame, textvariable=self.part_price_var, width=10).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(part_frame, text="添加配件", command=self.add_part_to_order).pack(side=tk.LEFT)
        
        # 配件列表
        parts_list_frame = ttk.Frame(parts_frame)
        parts_list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('配件名称', '来源', '数量', '单价', '小计')
        self.parts_tree = ttk.Treeview(parts_list_frame, columns=columns, show='headings', height=6)
        
        column_widths = {'配件名称': 150, '来源': 80, '数量': 60, '单价': 80, '小计': 80}
        for col in columns:
            self.parts_tree.heading(col, text=col)
            self.parts_tree.column(col, width=column_widths.get(col, 100))
        
        scrollbar_parts = ttk.Scrollbar(parts_list_frame, orient=tk.VERTICAL, command=self.parts_tree.yview)
        self.parts_tree.configure(yscrollcommand=scrollbar_parts.set)
        
        self.parts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_parts.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定删除事件
        self.parts_tree.bind('<Delete>', self.remove_part_from_order)
        
        # 总计框架
        total_frame = ttk.Frame(parts_frame)
        total_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(total_frame, text="配件总计:").pack(side=tk.LEFT)
        self.parts_total_var = tk.StringVar(value="0.00")
        ttk.Label(total_frame, textvariable=self.parts_total_var, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(total_frame, text="订单总计:").pack(side=tk.LEFT)
        self.order_total_var = tk.StringVar(value="0.00")
        ttk.Label(total_frame, textvariable=self.order_total_var, font=('Arial', 12, 'bold'), foreground='red').pack(side=tk.LEFT, padx=(5, 0))
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="创建订单", command=self.create_order).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空表单", command=self.clear_new_order_form).pack(side=tk.LEFT)
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        customer_frame.columnconfigure(1, weight=1)
        order_frame.columnconfigure(1, weight=1)
        
        # 初始化数据
        self.selected_parts = []  # 存储选中的配件
        self.load_customers_for_combo()
        self.load_parts_for_combo()
    
    def load_customers_for_combo(self):
        """加载客户到下拉框"""
        try:
            customers = self.order_service.get_all_customers()
            customer_list = [f"{c.customer_name} ({c.phone})" for c in customers]
            self.customer_combo['values'] = customer_list
            self.customers_data = customers  # 保存客户数据
        except Exception as e:
            messagebox.showerror("错误", f"加载客户列表失败: {e}")
    
    def load_parts_for_combo(self):
        """加载配件到下拉框"""
        try:
            parts = self.inventory_service.get_all_parts()
            part_list = [f"{p.part_name} (库存:{p.stock_quantity})" for p in parts if p.stock_quantity > 0]
            self.part_combo['values'] = part_list
            self.parts_data = parts  # 保存配件数据
        except Exception as e:
            messagebox.showerror("错误", f"加载配件列表失败: {e}")
    
    def on_customer_select(self, event):
        """客户选择事件"""
        selection = self.customer_var.get()
        if selection:
            # 从选择中提取客户信息
            for customer in self.customers_data:
                if f"{customer.customer_name} ({customer.phone})" == selection:
                    self.customer_phone_var.set(customer.phone)
                    self.customer_plate_var.set(customer.license_plate or '')
                    self.customer_car_var.set(customer.car_model or '')
                    self.selected_customer = customer
                    break
    
    def new_customer(self):
        """新建客户"""
        # 这里可以打开客户管理窗口或简单的客户添加对话框
        messagebox.showinfo("提示", "请使用客户管理功能添加新客户")
    
    def on_part_source_change(self, event):
        """配件来源切换事件"""
        source = self.part_source_var.get()
        if source == "库存配件":
            # 显示配件下拉框，隐藏自定义输入框
            self.part_combo.pack(side=tk.LEFT, padx=(0, 10))
            self.custom_part_entry.pack_forget()
            self.part_var.set("")
            # 启用配件选择，禁用单价输入（从库存获取）
            self.part_combo.configure(state="readonly")
        else:  # 客户自带
            # 隐藏配件下拉框，显示自定义输入框
            self.part_combo.pack_forget()
            self.custom_part_entry.pack(side=tk.LEFT, padx=(0, 10))
            self.custom_part_var.set("")
            # 启用自定义输入
            self.custom_part_entry.configure(state="normal")
    
    def add_part_to_order(self):
        """添加配件到订单"""
        source = self.part_source_var.get()
        
        try:
            quantity = int(self.part_quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("错误", "数量必须大于0")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数量")
            return
        
        try:
            unit_price = float(self.part_price_var.get())
            if unit_price < 0:
                messagebox.showerror("错误", "单价不能为负数")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的单价")
            return
        
        if source == "库存配件":
            part_selection = self.part_var.get()
            if not part_selection:
                messagebox.showerror("错误", "请选择配件")
                return
            
            # 查找选中的配件
            selected_part = None
            for part in self.parts_data:
                if f"{part.part_name} (库存:{part.stock_quantity})" == part_selection:
                    selected_part = part
                    break
            
            if not selected_part:
                messagebox.showerror("错误", "配件不存在")
                return
            
            # 检查库存
            if quantity > selected_part.stock_quantity:
                messagebox.showerror("错误", f"库存不足，当前库存：{selected_part.stock_quantity}")
                return
            
            # 检查是否已添加
            for existing_part in self.selected_parts:
                if existing_part.get('part_id') == selected_part.part_id:
                    messagebox.showerror("错误", "该配件已添加，请修改数量或删除后重新添加")
                    return
            
            # 使用库存配件的价格
            unit_price = selected_part.selling_price
            self.part_price_var.set(f"{unit_price:.2f}")
            
            # 添加到选中配件列表
            part_info = {
                'part_id': selected_part.part_id,
                'part_name': selected_part.part_name,
                'part_source': '库存配件',
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': quantity * unit_price
            }
            
        else:  # 客户自带
            part_name = self.custom_part_var.get().strip()
            if not part_name:
                messagebox.showerror("错误", "请输入配件名称")
                return
            
            # 检查是否已添加同名配件
            for existing_part in self.selected_parts:
                if (existing_part['part_name'] == part_name and 
                    existing_part['part_source'] == '客户自带'):
                    messagebox.showerror("错误", "该客户自带配件已添加，请修改数量或删除后重新添加")
                    return
            
            # 添加到选中配件列表
            part_info = {
                'part_id': None,
                'part_name': part_name,
                'part_source': '客户自带',
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': quantity * unit_price
            }
        
        self.selected_parts.append(part_info)
        
        # 更新配件列表显示
        self.update_parts_display()
        
        # 清空选择
        if source == "库存配件":
            self.part_var.set("")
        else:
            self.custom_part_var.set("")
        self.part_quantity_var.set("1")
        self.part_price_var.set("0.00")
    
    def remove_part_from_order(self, event=None):
        """从订单中移除配件"""
        selection = self.parts_tree.selection()
        if selection:
            item = self.parts_tree.item(selection[0])
            part_name = item['values'][0]
            
            # 从选中配件列表中移除
            self.selected_parts = [p for p in self.selected_parts if p['part_name'] != part_name]
            
            # 更新显示
            self.update_parts_display()
    
    def update_parts_display(self):
        """更新配件显示和总计"""
        # 清空配件列表
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        # 添加配件到列表
        parts_total = 0
        for part in self.selected_parts:
            values = (
                part['part_name'],
                part['part_source'],
                part['quantity'],
                f"{part['unit_price']:.2f}",
                f"{part['subtotal']:.2f}"
            )
            self.parts_tree.insert('', tk.END, values=values)
            parts_total += part['subtotal']
        
        # 更新总计
        self.parts_total_var.set(f"{parts_total:.2f}")
        
        # 计算订单总计
        try:
            labor_cost = float(self.labor_cost_var.get())
        except ValueError:
            labor_cost = 0
        
        order_total = parts_total + labor_cost
        self.order_total_var.set(f"{order_total:.2f}")
    
    def create_order(self):
        """创建订单"""
        # 验证必填字段
        if not hasattr(self, 'selected_customer'):
            messagebox.showerror("错误", "请选择客户")
            return
        
        fault_description = self.fault_text.get('1.0', tk.END).strip()
        if not fault_description:
            messagebox.showerror("错误", "请输入故障描述")
            return
        
        try:
            labor_cost = float(self.labor_cost_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的工时费")
            return
        
        try:
            # 准备配件使用数据
            parts_usage_list = []
            for part in self.selected_parts:
                usage_data = {
                    'part_id': part.get('part_id'),
                    'part_name': part['part_name'],
                    'part_source': part['part_source'],
                    'quantity_used': part['quantity'],
                    'unit_price': part['unit_price'],
                    'remarks': ''
                }
                parts_usage_list.append(usage_data)
            
            # 准备订单数据
            order_data = {
                'customer_id': self.selected_customer.customer_id,
                'repair_date': datetime.strptime(self.repair_date_var.get(), '%Y-%m-%d').date(),
                'fault_description': fault_description,
                'repair_content': self.repair_text.get('1.0', tk.END).strip(),
                'labor_cost': labor_cost
            }
            
            # 创建订单
            order_id = self.order_service.create_repair_order(order_data, parts_usage_list)
            messagebox.showinfo("成功", f"订单创建成功！订单号：{order_id}")
            
            # 清空表单
            self.clear_new_order_form()
            
            # 刷新订单列表
            self.load_orders()
            
        except Exception as e:
            messagebox.showerror("错误", f"创建订单失败: {e}")
    
    def clear_new_order_form(self):
        """清空新建订单表单"""
        self.customer_var.set("")
        self.customer_phone_var.set("")
        self.customer_plate_var.set("")
        self.customer_car_var.set("")
        self.repair_date_var.set(date.today().strftime('%Y-%m-%d'))
        self.fault_text.delete('1.0', tk.END)
        self.repair_text.delete('1.0', tk.END)
        self.labor_cost_var.set("0.00")
        self.part_source_var.set("库存配件")
        self.part_var.set("")
        self.custom_part_var.set("")
        self.part_quantity_var.set("1")
        self.part_price_var.set("0.00")
        self.selected_parts = []
        self.update_parts_display()
        # 重置配件选择界面
        self.on_part_source_change(None)
        if hasattr(self, 'selected_customer'):
            delattr(self, 'selected_customer')
    
    def load_orders(self):
        """加载订单列表"""
        try:
            # 清空现有数据
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)
            
            # 获取订单数据
            orders = self.order_service.get_all_orders()
            
            # 插入数据到树形控件
            for order in orders:
                # 获取客户信息
                customer = self.order_service.customer_dao.get_customer_by_id(order.customer_id)
                customer_name = customer.customer_name if customer else '未知客户'
                license_plate = customer.license_plate if customer else ''
                
                values = (
                    order.order_number,
                    customer_name,
                    license_plate,
                    order.repair_date.strftime('%Y-%m-%d') if order.repair_date else '',
                    order.fault_description or '',
                    f"{order.total_amount:.2f}",
                    order.status
                )
                
                # 根据状态设置不同颜色
                tags = ()
                if order.status == '已完成':
                    tags = ('completed',)
                elif order.status == '已取消':
                    tags = ('cancelled',)
                elif order.status == '维修中':
                    tags = ('in_progress',)
                
                self.orders_tree.insert('', tk.END, values=values, tags=tags)
            
            # 设置标签样式
            self.orders_tree.tag_configure('completed', background='#ccffcc')
            self.orders_tree.tag_configure('cancelled', background='#ffcccc')
            self.orders_tree.tag_configure('in_progress', background='#ffffcc')
            
        except Exception as e:
            messagebox.showerror("错误", f"加载订单列表失败: {e}")
    
    def search_orders(self):
        """搜索订单"""
        try:
            order_number = self.search_order_var.get().strip()
            customer_keyword = self.search_customer_var.get().strip()
            status = self.search_status_var.get().strip()
            
            # 清空现有数据
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)
            
            # 获取所有订单并过滤
            orders = self.order_service.get_all_orders()
            
            for order in orders:
                # 获取客户信息
                customer = self.order_service.customer_dao.get_customer_by_id(order.customer_id)
                customer_name = customer.customer_name if customer else '未知客户'
                license_plate = customer.license_plate if customer else ''
                
                # 应用过滤条件
                if order_number and order_number not in order.order_number:
                    continue
                if customer_keyword and customer_keyword not in customer_name and customer_keyword not in license_plate:
                    continue
                if status and status != order.status:
                    continue
                
                values = (
                    order.order_number,
                    customer_name,
                    license_plate,
                    order.repair_date.strftime('%Y-%m-%d') if order.repair_date else '',
                    order.fault_description or '',
                    f"{order.total_amount:.2f}",
                    order.status
                )
                
                tags = ()
                if order.status == '已完成':
                    tags = ('completed',)
                elif order.status == '已取消':
                    tags = ('cancelled',)
                elif order.status == '维修中':
                    tags = ('in_progress',)
                
                self.orders_tree.insert('', tk.END, values=values, tags=tags)
            
        except Exception as e:
            messagebox.showerror("错误", f"搜索订单失败: {e}")
    
    def reset_search(self):
        """重置搜索"""
        self.search_order_var.set("")
        self.search_customer_var.set("")
        self.search_status_var.set("")
        self.load_orders()
    
    def view_order_detail(self, event=None):
        """查看订单详情"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要查看的订单")
            return
        
        item = self.orders_tree.item(selection[0])
        order_number = item['values'][0]
        
        try:
            # 获取订单详情
            order_detail = self.order_service.get_order_details(order_number)
            if not order_detail:
                messagebox.showerror("错误", "订单不存在")
                return
            
            # 创建详情窗口
            detail_window = tk.Toplevel(self.window)
            detail_window.title(f"订单详情 - {order_number}")
            detail_window.geometry("600x500")
            detail_window.transient(self.window)
            detail_window.grab_set()
            
            # 显示订单详情
            self.show_order_detail(detail_window, order_detail)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取订单详情失败: {e}")
    
    def show_order_detail(self, parent, order_detail):
        """显示订单详情"""
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 基本信息
        info_frame = ttk.LabelFrame(frame, text="基本信息", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text=f"订单号: {order_detail['order'].order_number}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"客户: {order_detail['customer'].customer_name}").grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Label(info_frame, text=f"电话: {order_detail['customer'].phone}").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"车牌: {order_detail['customer'].license_plate or ''}").grid(row=1, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Label(info_frame, text=f"维修日期: {order_detail['order'].repair_date}").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"状态: {order_detail['order'].status}").grid(row=2, column=1, sticky=tk.W, padx=(20, 0))
        
        # 故障描述
        fault_frame = ttk.LabelFrame(frame, text="故障描述", padding="10")
        fault_frame.pack(fill=tk.X, pady=(0, 10))
        
        fault_text = tk.Text(fault_frame, height=3, wrap=tk.WORD)
        fault_text.pack(fill=tk.X)
        fault_text.insert('1.0', order_detail['order'].fault_description or '')
        fault_text.config(state=tk.DISABLED)
        
        # 维修内容
        repair_frame = ttk.LabelFrame(frame, text="维修内容", padding="10")
        repair_frame.pack(fill=tk.X, pady=(0, 10))
        
        repair_text = tk.Text(repair_frame, height=3, wrap=tk.WORD)
        repair_text.pack(fill=tk.X)
        repair_text.insert('1.0', order_detail['order'].repair_content or '')
        repair_text.config(state=tk.DISABLED)
        
        # 使用配件
        parts_frame = ttk.LabelFrame(frame, text="使用配件", padding="10")
        parts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        if order_detail['parts_used']:
            columns = ('配件名称', '来源', '数量', '单价', '小计')
            parts_tree = ttk.Treeview(parts_frame, columns=columns, show='headings', height=6)
            
            for col in columns:
                parts_tree.heading(col, text=col)
                if col == '配件名称':
                    parts_tree.column(col, width=150)
                elif col == '来源':
                    parts_tree.column(col, width=80)
                else:
                    parts_tree.column(col, width=80)
            
            for part in order_detail['parts_used']:
                values = (
                    part.part_name,
                    part.part_source or '库存配件',
                    part.quantity,
                    f"{part.unit_price:.2f}",
                    f"{part.subtotal:.2f}"
                )
                parts_tree.insert('', tk.END, values=values)
            
            parts_tree.pack(fill=tk.BOTH, expand=True)
        else:
            ttk.Label(parts_frame, text="未使用配件").pack()
        
        # 费用信息
        cost_frame = ttk.LabelFrame(frame, text="费用信息", padding="10")
        cost_frame.pack(fill=tk.X)
        
        ttk.Label(cost_frame, text=f"工时费: ¥{order_detail['order'].labor_cost:.2f}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(cost_frame, text=f"配件费: ¥{order_detail['order'].parts_cost:.2f}").grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Label(cost_frame, text=f"总计: ¥{order_detail['order'].total_amount:.2f}", 
                 font=('Arial', 12, 'bold'), foreground='red').grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
    
    def complete_order(self):
        """完成订单"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要完成的订单")
            return
        
        item = self.orders_tree.item(selection[0])
        order_number = item['values'][0]
        current_status = item['values'][6]
        
        if current_status == '已完成':
            messagebox.showinfo("提示", "订单已经完成")
            return
        
        if current_status == '已取消':
            messagebox.showwarning("提示", "已取消的订单无法完成")
            return
        
        if messagebox.askyesno("确认", f"确定要完成订单 {order_number} 吗？"):
            try:
                self.order_service.complete_order(order_number)
                messagebox.showinfo("成功", "订单已完成")
                self.load_orders()
            except Exception as e:
                messagebox.showerror("错误", f"完成订单失败: {e}")
    
    def cancel_order(self):
        """取消订单"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要取消的订单")
            return
        
        item = self.orders_tree.item(selection[0])
        order_number = item['values'][0]
        current_status = item['values'][6]
        
        if current_status == '已取消':
            messagebox.showinfo("提示", "订单已经取消")
            return
        
        if current_status == '已完成':
            messagebox.showwarning("提示", "已完成的订单无法取消")
            return
        
        if messagebox.askyesno("确认", f"确定要取消订单 {order_number} 吗？\n取消后配件库存将恢复。"):
            try:
                # 这里需要实现取消订单的逻辑，包括恢复库存
                messagebox.showinfo("提示", "取消订单功能待实现")
                # self.order_service.cancel_order(order_number)
                # messagebox.showinfo("成功", "订单已取消")
                # self.load_orders()
            except Exception as e:
                messagebox.showerror("错误", f"取消订单失败: {e}")

# 测试代码
if __name__ == "__main__":
    app = OrdersWindow()
    app.window.mainloop()