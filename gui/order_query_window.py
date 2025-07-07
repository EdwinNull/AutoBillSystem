#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单查询窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta
from services.order_service import OrderService

class OrderQueryWindow:
    """订单查询窗口类"""
    
    def __init__(self, parent):
        self.parent = parent
        self.order_service = OrderService()
        self.setup_window()
        self.setup_widgets()
        self.load_data()
    
    def setup_window(self):
        """设置窗口属性"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("订单查询")
        self.window.geometry("1200x700")
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
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 查询条件区域
        search_frame = ttk.LabelFrame(main_frame, text="查询条件", padding="10")
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 第一行查询条件
        # 客户姓名
        ttk.Label(search_frame, text="客户姓名:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.customer_var = tk.StringVar()
        customer_entry = ttk.Entry(search_frame, textvariable=self.customer_var, width=15)
        customer_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 订单状态
        ttk.Label(search_frame, text="订单状态:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.status_var = tk.StringVar(value="全部")
        status_combo = ttk.Combobox(search_frame, textvariable=self.status_var, 
                                  values=["全部", "进行中", "已完成", "已取消"], 
                                  width=10, state="readonly")
        status_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # 车牌号
        ttk.Label(search_frame, text="车牌号:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.vehicle_var = tk.StringVar()
        vehicle_entry = ttk.Entry(search_frame, textvariable=self.vehicle_var, width=15)
        vehicle_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 20))
        
        # 技师
        ttk.Label(search_frame, text="技师:").grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
        self.technician_var = tk.StringVar()
        technician_entry = ttk.Entry(search_frame, textvariable=self.technician_var, width=10)
        technician_entry.grid(row=0, column=7, sticky=tk.W)
        
        # 第二行查询条件
        # 开始日期
        ttk.Label(search_frame, text="开始日期:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.start_date_var = tk.StringVar()
        start_date_entry = ttk.Entry(search_frame, textvariable=self.start_date_var, width=12)
        start_date_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        
        # 结束日期
        ttk.Label(search_frame, text="结束日期:").grid(row=1, column=2, sticky=tk.W, padx=(15, 5), pady=(10, 0))
        self.end_date_var = tk.StringVar()
        end_date_entry = ttk.Entry(search_frame, textvariable=self.end_date_var, width=12)
        end_date_entry.grid(row=1, column=3, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        # 快速日期选择
        quick_date_frame = ttk.Frame(search_frame)
        quick_date_frame.grid(row=1, column=4, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(quick_date_frame, text="今天", command=lambda: self.set_date_range(0), width=6).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(quick_date_frame, text="本周", command=lambda: self.set_date_range(7), width=6).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(quick_date_frame, text="本月", command=lambda: self.set_date_range(30), width=6).grid(row=0, column=2, padx=(0, 5))
        
        # 查询按钮
        button_frame = ttk.Frame(search_frame)
        button_frame.grid(row=1, column=6, columnspan=2, sticky=tk.E, pady=(10, 0))
        
        search_btn = ttk.Button(button_frame, text="查询", command=self.search_orders)
        search_btn.grid(row=0, column=0, padx=(0, 5))
        
        reset_btn = ttk.Button(button_frame, text="重置", command=self.reset_search)
        reset_btn.grid(row=0, column=1)
        
        # 订单列表区域
        list_frame = ttk.LabelFrame(main_frame, text="订单列表", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('order_number', 'customer_name', 'vehicle_number', 'repair_date', 
                  'fault_description', 'total_amount', 'status', 'technician')
        self.orders_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题
        self.orders_tree.heading('order_number', text='订单号')
        self.orders_tree.heading('customer_name', text='客户姓名')
        self.orders_tree.heading('vehicle_number', text='车牌号')
        self.orders_tree.heading('repair_date', text='维修日期')
        self.orders_tree.heading('fault_description', text='故障描述')
        self.orders_tree.heading('total_amount', text='总金额')
        self.orders_tree.heading('status', text='状态')
        self.orders_tree.heading('technician', text='技师')
        
        # 设置列宽
        self.orders_tree.column('order_number', width=120)
        self.orders_tree.column('customer_name', width=100)
        self.orders_tree.column('vehicle_number', width=100)
        self.orders_tree.column('repair_date', width=100)
        self.orders_tree.column('fault_description', width=200)
        self.orders_tree.column('total_amount', width=80)
        self.orders_tree.column('status', width=80)
        self.orders_tree.column('technician', width=80)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 统计信息区域
        stats_frame = ttk.LabelFrame(list_frame, text="统计信息", padding="10")
        stats_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 统计标签
        self.stats_var = tk.StringVar()
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_var, font=('Arial', 10))
        stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, pady=(20, 0))
        
        detail_btn = ttk.Button(bottom_frame, text="查看详情", command=self.show_order_detail)
        detail_btn.grid(row=0, column=0, padx=(0, 10))
        
        export_btn = ttk.Button(bottom_frame, text="导出Excel", command=self.export_to_excel)
        export_btn.grid(row=0, column=1, padx=(0, 10))
        
        refresh_btn = ttk.Button(bottom_frame, text="刷新", command=self.load_data)
        refresh_btn.grid(row=0, column=2, padx=(0, 10))
        
        close_btn = ttk.Button(bottom_frame, text="关闭", command=self.window.destroy)
        close_btn.grid(row=0, column=3)
        
        # 绑定双击事件
        self.orders_tree.bind('<Double-1>', self.on_item_double_click)
        
        # 设置默认日期范围（本月）
        self.set_date_range(30)
    
    def load_data(self):
        """加载数据"""
        self.search_orders()
    
    def set_date_range(self, days):
        """设置日期范围"""
        end_date = date.today()
        if days == 0:
            start_date = end_date
        else:
            start_date = end_date - timedelta(days=days-1)
        
        self.start_date_var.set(start_date.strftime('%Y-%m-%d'))
        self.end_date_var.set(end_date.strftime('%Y-%m-%d'))
    
    def search_orders(self):
        """搜索订单"""
        try:
            # 获取查询条件
            customer_name = self.customer_var.get().strip()
            status = self.status_var.get() if self.status_var.get() != "全部" else ""
            vehicle_number = self.vehicle_var.get().strip()
            technician = self.technician_var.get().strip()
            
            # 解析日期
            start_date = None
            end_date = None
            
            if self.start_date_var.get():
                try:
                    start_date = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d').date()
                except ValueError:
                    messagebox.showwarning("警告", "开始日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
            
            if self.end_date_var.get():
                try:
                    end_date = datetime.strptime(self.end_date_var.get(), '%Y-%m-%d').date()
                except ValueError:
                    messagebox.showwarning("警告", "结束日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
            
            # 搜索订单
            orders = self.order_service.search_repair_orders(
                customer_name=customer_name,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            
            # 根据车牌号和技师进一步筛选
            if vehicle_number or technician:
                filtered_orders = []
                for order in orders:
                    if vehicle_number and vehicle_number.lower() not in order.vehicle_number.lower():
                        continue
                    if technician and technician.lower() not in order.technician.lower():
                        continue
                    filtered_orders.append(order)
                orders = filtered_orders
            
            # 加载搜索结果
            self.load_orders(orders)
            
        except Exception as e:
            messagebox.showerror("错误", f"搜索失败: {e}")
    
    def load_orders(self, orders):
        """加载订单数据"""
        try:
            # 清空现有记录
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)
            
            # 获取客户信息映射
            customers = self.order_service.get_all_customers()
            customer_map = {customer.customer_id: customer.customer_name for customer in customers}
            
            total_orders = 0
            completed_orders = 0
            total_amount = 0
            total_labor_cost = 0
            total_parts_cost = 0
            
            for order in orders:
                # 获取客户姓名
                customer_name = customer_map.get(order.customer_id, "未知客户")
                
                # 设置行颜色
                tags = ()
                if order.status == "已完成":
                    tags = ('completed',)
                    completed_orders += 1
                    total_amount += order.total_amount
                    total_labor_cost += order.labor_cost
                    total_parts_cost += order.parts_cost
                elif order.status == "已取消":
                    tags = ('cancelled',)
                else:
                    tags = ('in_progress',)
                
                total_orders += 1
                
                # 插入数据
                self.orders_tree.insert('', 'end', values=(
                    order.order_number,
                    customer_name,
                    order.vehicle_number,
                    order.repair_date.strftime('%Y-%m-%d'),
                    order.fault_description[:30] + "..." if len(order.fault_description) > 30 else order.fault_description,
                    f"¥{order.total_amount:.2f}",
                    order.status,
                    order.technician
                ), tags=tags)
            
            # 设置行颜色
            self.orders_tree.tag_configure('completed', background='#e8f5e8')
            self.orders_tree.tag_configure('cancelled', background='#ffeeee')
            self.orders_tree.tag_configure('in_progress', background='#fff8dc')
            
            # 更新统计信息
            in_progress_orders = total_orders - completed_orders - len([o for o in orders if o.status == "已取消"])
            cancelled_orders = len([o for o in orders if o.status == "已取消"])
            
            stats_text = (f"订单总数: {total_orders} | "
                         f"进行中: {in_progress_orders} | "
                         f"已完成: {completed_orders} | "
                         f"已取消: {cancelled_orders} | "
                         f"总收入: ¥{total_amount:.2f} | "
                         f"工时费: ¥{total_labor_cost:.2f} | "
                         f"配件费: ¥{total_parts_cost:.2f}")
            self.stats_var.set(stats_text)
            
        except Exception as e:
            messagebox.showerror("错误", f"加载订单数据失败: {e}")
    
    def reset_search(self):
        """重置搜索条件"""
        self.customer_var.set('')
        self.status_var.set('全部')
        self.vehicle_var.set('')
        self.technician_var.set('')
        self.set_date_range(30)  # 默认本月
        self.search_orders()
    
    def on_item_double_click(self, event):
        """双击事件处理"""
        self.show_order_detail()
    
    def show_order_detail(self):
        """显示订单详情"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要查看的订单")
            return
        
        try:
            item = self.orders_tree.item(selection[0])
            order_number = item['values'][0]
            
            # 获取订单详情
            order_details = self.order_service.get_order_details(order_number)
            if not order_details:
                messagebox.showerror("错误", "订单不存在")
                return
            
            order = order_details['order']
            customer = order_details['customer']
            parts_usage = order_details['parts_usage']
            
            # 创建详情窗口
            detail_window = tk.Toplevel(self.window)
            detail_window.title(f"订单详情 - {order_number}")
            detail_window.geometry("600x500")
            detail_window.resizable(False, False)
            detail_window.transient(self.window)
            detail_window.grab_set()
            
            # 创建详情内容
            detail_frame = ttk.Frame(detail_window, padding="20")
            detail_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # 基本信息
            basic_frame = ttk.LabelFrame(detail_frame, text="基本信息", padding="10")
            basic_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            basic_info = f"""订单号: {order.order_number}
客户姓名: {customer.customer_name if customer else '未知客户'}
联系电话: {customer.phone if customer else '无'}
车辆类型: {order.vehicle_type}
车牌号: {order.vehicle_number}
维修日期: {order.repair_date.strftime('%Y-%m-%d')}
技师: {order.technician}
状态: {order.status}"""
            
            ttk.Label(basic_frame, text=basic_info, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
            
            # 故障描述
            fault_frame = ttk.LabelFrame(detail_frame, text="故障描述", padding="10")
            fault_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            fault_text = tk.Text(fault_frame, height=3, width=60, wrap=tk.WORD)
            fault_text.insert(1.0, order.fault_description)
            fault_text.config(state=tk.DISABLED)
            fault_text.grid(row=0, column=0)
            
            # 维修内容
            repair_frame = ttk.LabelFrame(detail_frame, text="维修内容", padding="10")
            repair_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            repair_text = tk.Text(repair_frame, height=3, width=60, wrap=tk.WORD)
            repair_text.insert(1.0, order.repair_content)
            repair_text.config(state=tk.DISABLED)
            repair_text.grid(row=0, column=0)
            
            # 配件使用
            if parts_usage:
                parts_frame = ttk.LabelFrame(detail_frame, text="配件使用", padding="10")
                parts_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                
                parts_tree = ttk.Treeview(parts_frame, columns=('part_name', 'quantity', 'unit_price', 'subtotal'), 
                                        show='headings', height=4)
                
                parts_tree.heading('part_name', text='配件名称')
                parts_tree.heading('quantity', text='数量')
                parts_tree.heading('unit_price', text='单价')
                parts_tree.heading('subtotal', text='小计')
                
                parts_tree.column('part_name', width=200)
                parts_tree.column('quantity', width=80)
                parts_tree.column('unit_price', width=80)
                parts_tree.column('subtotal', width=80)
                
                for usage in parts_usage:
                    parts_tree.insert('', 'end', values=(
                        usage.part_name if hasattr(usage, 'part_name') else '未知配件',
                        usage.quantity_used,
                        f"¥{usage.unit_price:.2f}",
                        f"¥{usage.subtotal:.2f}"
                    ))
                
                parts_tree.grid(row=0, column=0)
            
            # 费用信息
            cost_frame = ttk.LabelFrame(detail_frame, text="费用信息", padding="10")
            cost_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            
            cost_info = f"""工时费: ¥{order.labor_cost:.2f}
配件费: ¥{order.parts_cost:.2f}
总金额: ¥{order.total_amount:.2f}"""
            
            ttk.Label(cost_frame, text=cost_info, justify=tk.LEFT, font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
            
            # 备注
            if order.remarks:
                remarks_frame = ttk.LabelFrame(detail_frame, text="备注", padding="10")
                remarks_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                
                ttk.Label(remarks_frame, text=order.remarks, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
            
            # 关闭按钮
            ttk.Button(detail_frame, text="关闭", command=detail_window.destroy).grid(row=6, column=0, pady=(10, 0))
            
        except Exception as e:
            messagebox.showerror("错误", f"显示订单详情失败: {e}")
    
    def export_to_excel(self):
        """导出到Excel"""
        try:
            from tkinter import filedialog
            from utils.export_utils import ExportUtils
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                title="导出订单报表",
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
            )
            
            if file_path:
                # 获取当前显示的数据
                data = []
                for item in self.orders_tree.get_children():
                    values = self.orders_tree.item(item)['values']
                    data.append(values)
                
                # 导出数据
                headers = ['订单号', '客户姓名', '车牌号', '维修日期', '故障描述', '总金额', '状态', '技师']
                
                ExportUtils.export_to_excel(data, headers, file_path, "订单报表")
                messagebox.showinfo("成功", f"订单报表已导出到: {file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")