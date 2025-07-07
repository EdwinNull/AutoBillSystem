#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进货管理窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from services.inventory_service import InventoryService

class PurchaseWindow:
    """进货管理窗口类"""
    
    def __init__(self, parent):
        self.parent = parent
        self.inventory_service = InventoryService()
        self.setup_window()
        self.setup_widgets()
        self.load_data()
    
    def setup_window(self):
        """设置窗口属性"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("进货管理")
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # 居中显示
        self.window.transient(self.parent)
        self.window.grab_set()
    
    def setup_widgets(self):
        """设置界面控件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 左侧进货录入区域
        input_frame = ttk.LabelFrame(main_frame, text="进货录入", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 供应商信息
        ttk.Label(input_frame, text="供应商:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.supplier_var = tk.StringVar()
        supplier_entry = ttk.Entry(input_frame, textvariable=self.supplier_var, width=20)
        supplier_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(input_frame, text="操作员:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.operator_var = tk.StringVar(value="管理员")
        operator_entry = ttk.Entry(input_frame, textvariable=self.operator_var, width=15)
        operator_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(input_frame, text="备注:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.remarks_var = tk.StringVar()
        remarks_entry = ttk.Entry(input_frame, textvariable=self.remarks_var, width=20)
        remarks_entry.grid(row=0, column=5, sticky=tk.W)
        
        # 配件选择区域
        parts_frame = ttk.LabelFrame(input_frame, text="配件选择", padding="5")
        parts_frame.grid(row=1, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(parts_frame, text="配件:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.part_var = tk.StringVar()
        self.part_combo = ttk.Combobox(parts_frame, textvariable=self.part_var, width=25, state="readonly")
        self.part_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(parts_frame, text="数量:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.quantity_var = tk.StringVar()
        quantity_entry = ttk.Entry(parts_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(parts_frame, text="单价:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.unit_price_var = tk.StringVar()
        unit_price_entry = ttk.Entry(parts_frame, textvariable=self.unit_price_var, width=10)
        unit_price_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 10))
        
        # 按钮
        add_btn = ttk.Button(parts_frame, text="添加配件", command=self.add_part_to_list)
        add_btn.grid(row=0, column=6, padx=(10, 0))
        
        # 进货明细列表
        list_frame = ttk.LabelFrame(main_frame, text="进货明细", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('part_name', 'quantity', 'unit_price', 'subtotal')
        self.parts_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # 设置列标题
        self.parts_tree.heading('part_name', text='配件名称')
        self.parts_tree.heading('quantity', text='数量')
        self.parts_tree.heading('unit_price', text='单价')
        self.parts_tree.heading('subtotal', text='小计')
        
        # 设置列宽
        self.parts_tree.column('part_name', width=200)
        self.parts_tree.column('quantity', width=80)
        self.parts_tree.column('unit_price', width=80)
        self.parts_tree.column('subtotal', width=80)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.parts_tree.yview)
        self.parts_tree.configure(yscrollcommand=scrollbar.set)
        
        self.parts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 操作按钮
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        remove_btn = ttk.Button(btn_frame, text="删除选中", command=self.remove_selected_part)
        remove_btn.grid(row=0, column=0, padx=(0, 10))
        
        clear_btn = ttk.Button(btn_frame, text="清空列表", command=self.clear_parts_list)
        clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        # 总金额显示
        total_frame = ttk.Frame(list_frame)
        total_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=tk.E)
        
        ttk.Label(total_frame, text="总金额:", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=(0, 5))
        self.total_var = tk.StringVar(value="¥0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=('Arial', 12, 'bold'), foreground='red').grid(row=0, column=1)
        
        # 右侧进货记录区域
        history_frame = ttk.LabelFrame(main_frame, text="进货记录", padding="10")
        history_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # 进货记录列表
        history_columns = ('order_id', 'supplier', 'date', 'total_amount', 'operator')
        self.history_tree = ttk.Treeview(history_frame, columns=history_columns, show='headings', height=15)
        
        # 设置列标题
        self.history_tree.heading('order_id', text='订单号')
        self.history_tree.heading('supplier', text='供应商')
        self.history_tree.heading('date', text='进货日期')
        self.history_tree.heading('total_amount', text='总金额')
        self.history_tree.heading('operator', text='操作员')
        
        # 设置列宽
        self.history_tree.column('order_id', width=80)
        self.history_tree.column('supplier', width=120)
        self.history_tree.column('date', width=100)
        self.history_tree.column('total_amount', width=80)
        self.history_tree.column('operator', width=80)
        
        # 添加滚动条
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        save_btn = ttk.Button(bottom_frame, text="保存进货单", command=self.save_purchase_order)
        save_btn.grid(row=0, column=0, padx=(0, 10))
        
        refresh_btn = ttk.Button(bottom_frame, text="刷新记录", command=self.load_purchase_history)
        refresh_btn.grid(row=0, column=1, padx=(0, 10))
        
        close_btn = ttk.Button(bottom_frame, text="关闭", command=self.window.destroy)
        close_btn.grid(row=0, column=2)
        
        # 初始化进货明细列表
        self.parts_list = []
    
    def load_data(self):
        """加载数据"""
        self.load_parts_combo()
        self.load_purchase_history()
    
    def load_parts_combo(self):
        """加载配件下拉列表"""
        try:
            parts = self.inventory_service.get_all_parts()
            part_names = [f"{part.part_name} ({part.part_code})" for part in parts]
            self.part_combo['values'] = part_names
            self.parts_data = {f"{part.part_name} ({part.part_code})": part for part in parts}
        except Exception as e:
            messagebox.showerror("错误", f"加载配件列表失败: {e}")
    
    def load_purchase_history(self):
        """加载进货记录"""
        try:
            # 清空现有记录
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # 加载进货记录
            orders = self.inventory_service.get_purchase_orders()
            for order in orders:
                self.history_tree.insert('', 'end', values=(
                    order.order_id,
                    order.supplier_name,
                    order.purchase_date.strftime('%Y-%m-%d'),
                    f"¥{order.total_amount:.2f}",
                    order.operator
                ))
        except Exception as e:
            messagebox.showerror("错误", f"加载进货记录失败: {e}")
    
    def add_part_to_list(self):
        """添加配件到进货列表"""
        try:
            # 验证输入
            if not self.part_var.get():
                messagebox.showwarning("警告", "请选择配件")
                return
            
            if not self.quantity_var.get() or not self.quantity_var.get().isdigit():
                messagebox.showwarning("警告", "请输入有效的数量")
                return
            
            try:
                unit_price = float(self.unit_price_var.get())
                if unit_price <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showwarning("警告", "请输入有效的单价")
                return
            
            # 获取选中的配件
            selected_part = self.parts_data[self.part_var.get()]
            quantity = int(self.quantity_var.get())
            subtotal = quantity * unit_price
            
            # 检查是否已存在
            for item in self.parts_list:
                if item['part_id'] == selected_part.part_id:
                    messagebox.showwarning("警告", "该配件已在列表中，请先删除后重新添加")
                    return
            
            # 添加到列表
            part_item = {
                'part_id': selected_part.part_id,
                'part_name': selected_part.part_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal
            }
            self.parts_list.append(part_item)
            
            # 更新界面
            self.update_parts_tree()
            self.update_total_amount()
            
            # 清空输入
            self.part_var.set('')
            self.quantity_var.set('')
            self.unit_price_var.set('')
            
        except Exception as e:
            messagebox.showerror("错误", f"添加配件失败: {e}")
    
    def remove_selected_part(self):
        """删除选中的配件"""
        selection = self.parts_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的配件")
            return
        
        # 获取选中项的索引
        item = selection[0]
        index = self.parts_tree.index(item)
        
        # 从列表中删除
        del self.parts_list[index]
        
        # 更新界面
        self.update_parts_tree()
        self.update_total_amount()
    
    def clear_parts_list(self):
        """清空配件列表"""
        if messagebox.askyesno("确认", "确定要清空配件列表吗？"):
            self.parts_list.clear()
            self.update_parts_tree()
            self.update_total_amount()
    
    def update_parts_tree(self):
        """更新配件列表显示"""
        # 清空现有项
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        # 添加新项
        for part in self.parts_list:
            self.parts_tree.insert('', 'end', values=(
                part['part_name'],
                part['quantity'],
                f"¥{part['unit_price']:.2f}",
                f"¥{part['subtotal']:.2f}"
            ))
    
    def update_total_amount(self):
        """更新总金额"""
        total = sum(part['subtotal'] for part in self.parts_list)
        self.total_var.set(f"¥{total:.2f}")
    
    def save_purchase_order(self):
        """保存进货单"""
        try:
            # 验证输入
            if not self.supplier_var.get().strip():
                messagebox.showwarning("警告", "请输入供应商名称")
                return
            
            if not self.operator_var.get().strip():
                messagebox.showwarning("警告", "请输入操作员")
                return
            
            if not self.parts_list:
                messagebox.showwarning("警告", "请添加进货配件")
                return
            
            # 创建进货订单
            order_id = self.inventory_service.create_purchase_order(
                supplier_name=self.supplier_var.get().strip(),
                operator=self.operator_var.get().strip(),
                parts_list=self.parts_list,
                remarks=self.remarks_var.get().strip()
            )
            
            messagebox.showinfo("成功", f"进货单保存成功！订单号: {order_id}")
            
            # 清空输入
            self.supplier_var.set('')
            self.remarks_var.set('')
            self.parts_list.clear()
            self.update_parts_tree()
            self.update_total_amount()
            
            # 刷新进货记录
            self.load_purchase_history()
            
        except Exception as e:
            messagebox.showerror("错误", f"保存进货单失败: {e}")