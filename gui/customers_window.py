#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户管理窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from services.order_service import OrderService
from models.customers import Customer

class CustomersWindow:
    """客户管理窗口"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.order_service = OrderService()
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.setup_window()
        self.setup_widgets()
        self.load_customers()
    
    def setup_window(self):
        """设置窗口属性"""
        self.window.title("客户管理")
        self.window.geometry("900x600")
        self.window.resizable(True, True)
        
        # 居中显示
        self.window.transient(self.parent)
        self.window.grab_set()
    
    def setup_widgets(self):
        """设置界面控件"""
        # 主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 搜索框架
        search_frame = ttk.LabelFrame(main_frame, text="搜索客户", padding="5")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="关键词:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(search_frame, text="搜索", command=self.search_customers).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(search_frame, text="重置", command=self.reset_search).grid(row=0, column=3)
        
        # 左侧：客户列表
        list_frame = ttk.LabelFrame(main_frame, text="客户列表", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 客户列表
        columns = ('ID', '姓名', '电话', '车牌号', '车型', '注册日期')
        self.customers_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题和宽度
        column_widths = {'ID': 50, '姓名': 100, '电话': 120, '车牌号': 100, '车型': 120, '注册日期': 100}
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=column_widths.get(col, 100))
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.customers_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.customers_tree.xview)
        self.customers_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.customers_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 绑定选择事件
        self.customers_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # 右侧：客户详情和操作
        detail_frame = ttk.LabelFrame(main_frame, text="客户详情", padding="10")
        detail_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 客户信息输入框
        self.setup_detail_form(detail_frame)
        
        # 底部按钮
        button_frame = ttk.Frame(detail_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="新增", command=self.add_customer).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="修改", command=self.update_customer).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="删除", command=self.delete_customer).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_form).grid(row=0, column=3, padx=(0, 5))
        ttk.Button(button_frame, text="维修历史", command=self.view_repair_history).grid(row=1, column=0, columnspan=2, pady=(5, 0))
    
    def setup_detail_form(self, parent):
        """设置详情表单"""
        # 客户姓名
        ttk.Label(parent, text="客户姓名:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.name_var, width=25).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 联系电话
        ttk.Label(parent, text="联系电话:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.phone_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.phone_var, width=25).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 车牌号
        ttk.Label(parent, text="车牌号:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.license_plate_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.license_plate_var, width=25).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 车型
        ttk.Label(parent, text="车型:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.car_model_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.car_model_var, width=25).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 车辆颜色
        ttk.Label(parent, text="车辆颜色:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.car_color_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.car_color_var, width=25).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 发动机号
        ttk.Label(parent, text="发动机号:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.engine_number_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.engine_number_var, width=25).grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 车架号
        ttk.Label(parent, text="车架号:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.vin_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.vin_var, width=25).grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 地址
        ttk.Label(parent, text="地址:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.address_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.address_var, width=25).grid(row=7, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 备注
        ttk.Label(parent, text="备注:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.notes_var = tk.StringVar()
        notes_text = tk.Text(parent, width=25, height=3)
        notes_text.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=2)
        self.notes_text = notes_text
        
        # 配置列权重
        parent.columnconfigure(1, weight=1)
        
        # 当前选中的客户ID
        self.current_customer_id = None
    
    def load_customers(self):
        """加载客户列表"""
        try:
            # 清空现有数据
            for item in self.customers_tree.get_children():
                self.customers_tree.delete(item)
            
            # 获取客户数据
            customers = self.order_service.get_all_customers()
            
            # 插入数据到树形控件
            for customer in customers:
                values = (
                    customer.customer_id,
                    customer.customer_name,
                    customer.phone,
                    customer.license_plate or '',
                    customer.car_model or '',
                    customer.created_at.strftime('%Y-%m-%d') if customer.created_at else ''
                )
                self.customers_tree.insert('', tk.END, values=values)
            
        except Exception as e:
            messagebox.showerror("错误", f"加载客户列表失败: {e}")
    
    def search_customers(self):
        """搜索客户"""
        try:
            keyword = self.search_var.get().strip()
            
            # 清空现有数据
            for item in self.customers_tree.get_children():
                self.customers_tree.delete(item)
            
            # 搜索客户
            customers = self.order_service.search_customers(keyword)
            
            # 插入搜索结果
            for customer in customers:
                values = (
                    customer.customer_id,
                    customer.customer_name,
                    customer.phone,
                    customer.license_plate or '',
                    customer.car_model or '',
                    customer.created_at.strftime('%Y-%m-%d') if customer.created_at else ''
                )
                self.customers_tree.insert('', tk.END, values=values)
            
        except Exception as e:
            messagebox.showerror("错误", f"搜索客户失败: {e}")
    
    def reset_search(self):
        """重置搜索"""
        self.search_var.set("")
        self.load_customers()
    
    def on_customer_select(self, event):
        """客户选择事件"""
        selection = self.customers_tree.selection()
        if selection:
            item = self.customers_tree.item(selection[0])
            values = item['values']
            
            # 获取完整的客户信息
            customer_id = values[0]
            try:
                customer = self.order_service.customer_dao.get_customer_by_id(customer_id)
                if customer:
                    self.load_customer_to_form(customer)
            except Exception as e:
                messagebox.showerror("错误", f"加载客户详情失败: {e}")
    
    def load_customer_to_form(self, customer):
        """将客户信息加载到表单"""
        self.current_customer_id = customer.customer_id
        self.name_var.set(customer.customer_name)
        self.phone_var.set(customer.phone)
        self.license_plate_var.set(customer.license_plate or '')
        self.car_model_var.set(customer.car_model or '')
        self.car_color_var.set(customer.car_color or '')
        self.engine_number_var.set(customer.engine_number or '')
        self.vin_var.set(customer.vin or '')
        self.address_var.set(customer.address or '')
        
        # 设置备注文本
        self.notes_text.delete('1.0', tk.END)
        if customer.notes:
            self.notes_text.insert('1.0', customer.notes)
    
    def clear_form(self):
        """清空表单"""
        self.current_customer_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.license_plate_var.set("")
        self.car_model_var.set("")
        self.car_color_var.set("")
        self.engine_number_var.set("")
        self.vin_var.set("")
        self.address_var.set("")
        self.notes_text.delete('1.0', tk.END)
    
    def validate_form(self):
        """验证表单数据"""
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入客户姓名")
            return False
        
        if not self.phone_var.get().strip():
            messagebox.showerror("错误", "请输入联系电话")
            return False
        
        return True
    
    def get_form_data(self):
        """获取表单数据"""
        return {
            'customer_name': self.name_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'license_plate': self.license_plate_var.get().strip(),
            'car_model': self.car_model_var.get().strip(),
            'car_color': self.car_color_var.get().strip(),
            'engine_number': self.engine_number_var.get().strip(),
            'vin': self.vin_var.get().strip(),
            'address': self.address_var.get().strip(),
            'notes': self.notes_text.get('1.0', tk.END).strip()
        }
    
    def add_customer(self):
        """添加客户"""
        if not self.validate_form():
            return
        
        try:
            customer_data = self.get_form_data()
            self.order_service.add_customer(customer_data)
            messagebox.showinfo("成功", "客户添加成功")
            self.load_customers()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("错误", f"添加客户失败: {e}")
    
    def update_customer(self):
        """修改客户"""
        if not self.current_customer_id:
            messagebox.showerror("错误", "请先选择要修改的客户")
            return
        
        if not self.validate_form():
            return
        
        try:
            customer_data = self.get_form_data()
            customer_data['customer_id'] = self.current_customer_id
            self.order_service.update_customer(customer_data)
            messagebox.showinfo("成功", "客户修改成功")
            self.load_customers()
        except Exception as e:
            messagebox.showerror("错误", f"修改客户失败: {e}")
    
    def delete_customer(self):
        """删除客户"""
        if not self.current_customer_id:
            messagebox.showerror("错误", "请先选择要删除的客户")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的客户吗？\n注意：删除客户将同时删除其所有维修记录！"):
            try:
                self.order_service.delete_customer(self.current_customer_id)
                messagebox.showinfo("成功", "客户删除成功")
                self.load_customers()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("错误", f"删除客户失败: {e}")
    
    def view_repair_history(self):
        """查看维修历史"""
        if not self.current_customer_id:
            messagebox.showerror("错误", "请先选择客户")
            return
        
        try:
            # 获取客户维修历史
            history = self.order_service.get_customer_repair_history(self.current_customer_id)
            
            # 创建历史窗口
            history_window = tk.Toplevel(self.window)
            history_window.title(f"维修历史 - {self.name_var.get()}")
            history_window.geometry("800x400")
            history_window.transient(self.window)
            history_window.grab_set()
            
            # 创建树形控件显示历史记录
            frame = ttk.Frame(history_window, padding="10")
            frame.pack(fill=tk.BOTH, expand=True)
            
            columns = ('订单号', '维修日期', '故障描述', '维修内容', '总费用', '状态')
            history_tree = ttk.Treeview(frame, columns=columns, show='headings')
            
            # 设置列标题和宽度
            column_widths = {'订单号': 80, '维修日期': 100, '故障描述': 150, '维修内容': 150, '总费用': 80, '状态': 80}
            for col in columns:
                history_tree.heading(col, text=col)
                history_tree.column(col, width=column_widths.get(col, 100))
            
            # 添加滚动条
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=history_tree.yview)
            history_tree.configure(yscrollcommand=scrollbar.set)
            
            history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 插入历史数据
            for order in history:
                values = (
                    order.order_number,
                    order.repair_date.strftime('%Y-%m-%d') if order.repair_date else '',
                    order.fault_description or '',
                    order.repair_content or '',
                    f"{order.total_amount:.2f}",
                    order.status
                )
                history_tree.insert('', tk.END, values=values)
            
            if not history:
                ttk.Label(frame, text="该客户暂无维修记录").pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取维修历史失败: {e}")

# 测试代码
if __name__ == "__main__":
    app = CustomersWindow()
    app.window.mainloop()