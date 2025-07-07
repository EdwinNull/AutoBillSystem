#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, Menu
from datetime import date, datetime
from services.inventory_service import InventoryService
from services.order_service import OrderService
from services.report_service import ReportService
from config.settings import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_services()
        self.setup_menu()
        self.setup_widgets()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        
        # 居中显示
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    def setup_services(self):
        """初始化服务"""
        self.inventory_service = InventoryService()
        self.order_service = OrderService()
        self.report_service = ReportService()
    
    def setup_menu(self):
        """设置菜单栏"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="数据备份", command=self.backup_data)
        file_menu.add_command(label="数据恢复", command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 库存菜单
        inventory_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="库存管理", menu=inventory_menu)
        inventory_menu.add_command(label="配件管理", command=self.open_parts_window)
        inventory_menu.add_command(label="进货管理", command=self.open_purchase_management)
        inventory_menu.add_command(label="库存查询", command=self.open_inventory_query)
        
        # 订单菜单
        order_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="订单管理", menu=order_menu)
        order_menu.add_command(label="客户管理", command=self.open_customers_window)
        order_menu.add_command(label="维修订单", command=self.open_orders_window)
        order_menu.add_command(label="订单查询", command=self.open_order_query)
        
        # 报表菜单
        report_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="报表统计", menu=report_menu)
        report_menu.add_command(label="销售报表", command=self.show_sales_report)
        report_menu.add_command(label="库存报表", command=self.show_inventory_report)
        report_menu.add_command(label="客户分析", command=self.show_customer_analysis)
        
        # 帮助菜单
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def setup_widgets(self):
        """设置主界面控件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text=APP_NAME, font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 左侧功能按钮区域
        button_frame = ttk.LabelFrame(main_frame, text="功能菜单", padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 功能按钮
        buttons = [
            ("配件管理", self.open_parts_window),
            ("进货管理", self.open_purchase_management),
            ("客户管理", self.open_customers_window),
            ("维修订单", self.open_orders_window),
            ("库存查询", self.open_inventory_query),
            ("订单查询", self.open_order_query),
            ("销售报表", self.show_sales_report),
            ("库存报表", self.show_inventory_report)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, width=15)
            btn.grid(row=i, column=0, pady=5, sticky=tk.W+tk.E)
        
        # 右侧信息显示区域
        info_frame = ttk.LabelFrame(main_frame, text="系统信息", padding="10")
        info_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # 创建信息显示文本框
        self.info_text = tk.Text(info_frame, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 加载系统信息
        self.load_system_info()
    
    def load_system_info(self):
        """加载系统信息"""
        try:
            # 获取库存统计
            inventory_stats = self.inventory_service.get_inventory_statistics()
            
            # 获取今日订单统计
            today_stats = self.order_service.get_order_statistics(
                start_date=date.today(),
                end_date=date.today()
            )
            
            # 构建信息文本
            info_text = f"""系统概览 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== 库存信息 ===
配件总数: {inventory_stats['total_parts']} 种
库存总值: ¥{inventory_stats['total_value']:.2f}
库存不足: {inventory_stats['low_stock_count']} 种

=== 今日业务 ===
维修订单: {today_stats['total_orders']} 单
已完成: {today_stats['completed_orders']} 单
今日收入: ¥{today_stats['total_revenue']:.2f}

=== 库存预警 ===
"""
            
            # 添加库存不足的配件信息
            if inventory_stats['low_stock_parts']:
                for part in inventory_stats['low_stock_parts'][:5]:  # 只显示前5个
                    info_text += f"• {part.part_name} (库存: {part.stock_quantity})\n"
                if len(inventory_stats['low_stock_parts']) > 5:
                    info_text += f"... 还有 {len(inventory_stats['low_stock_parts']) - 5} 种配件库存不足\n"
            else:
                info_text += "暂无库存不足的配件\n"
            
            # 更新信息显示
            self.info_text.config(state=tk.NORMAL)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)
            self.info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("错误", f"加载系统信息失败: {e}")
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    # 功能窗口打开方法
    def open_parts_window(self):
        """打开配件管理窗口"""
        try:
            from gui.parts_window import PartsWindow
            PartsWindow(self.root)
        except Exception as e:
            messagebox.showerror("错误", f"打开配件管理窗口失败: {e}")
    
    def open_customers_window(self):
        """打开客户管理窗口"""
        try:
            from gui.customers_window import CustomersWindow
            CustomersWindow(self.root)
        except Exception as e:
            messagebox.showerror("错误", f"打开客户管理窗口失败: {e}")
    
    def open_orders_window(self):
        """打开订单管理窗口"""
        try:
            from gui.orders_window import OrdersWindow
            OrdersWindow(self.root)
        except Exception as e:
            messagebox.showerror("错误", f"打开订单管理窗口失败: {e}")
    
    def open_purchase_management(self):
        """打开进货管理窗口"""
        try:
            from gui.purchase_window import PurchaseWindow
            PurchaseWindow(self.root)
        except Exception as e:
            messagebox.showerror("错误", f"打开进货管理窗口失败: {e}")
    
    def open_inventory_query(self):
        """打开库存查询窗口"""
        try:
            from gui.inventory_query_window import InventoryQueryWindow
            InventoryQueryWindow(self.root)
        except Exception as e:
            messagebox.showerror("错误", f"打开库存查询窗口失败: {e}")
    
    def open_order_query(self):
        """打开订单查询窗口"""
        try:
            from gui.order_query_window import OrderQueryWindow
            OrderQueryWindow(self.root)
        except Exception as e:
            messagebox.showerror("错误", f"打开订单查询窗口失败: {e}")
    
    def show_sales_report(self):
        """显示销售报表"""
        try:
            # 获取本月销售数据
            from datetime import datetime, date
            current_date = date.today()
            monthly_report = self.report_service.get_monthly_revenue_report(
                current_date.year, current_date.month
            )
            
            # 计算平均订单金额
            avg_order_amount = (monthly_report['total_revenue'] / monthly_report['total_orders']) if monthly_report['total_orders'] > 0 else 0
            
            report_text = f"""本月销售报表 ({current_date.year}年{current_date.month}月)

订单数量: {monthly_report['total_orders']} 单
总收入: ¥{monthly_report['total_revenue']:.2f}
工时费: ¥{monthly_report['total_labor']:.2f}
配件费: ¥{monthly_report['total_parts']:.2f}
平均订单金额: ¥{avg_order_amount:.2f}"""
            messagebox.showinfo("销售报表", report_text)
        except Exception as e:
            messagebox.showerror("错误", f"生成销售报表失败: {e}")
    
    def show_inventory_report(self):
        """显示库存报表"""
        try:
            inventory_data = self.report_service.get_inventory_report()
            
            # 统计库存信息
            total_parts = len(inventory_data)
            total_value = sum(item['inventory_value'] or 0 for item in inventory_data)
            low_stock_count = sum(1 for item in inventory_data if item['stock_status'] == '库存不足')
            zero_stock_count = sum(1 for item in inventory_data if item['stock_quantity'] == 0)
            
            report_text = f"""库存报表

配件总数: {total_parts} 种
库存总值: ¥{total_value:.2f}
低库存配件: {low_stock_count} 种
零库存配件: {zero_stock_count} 种"""
            messagebox.showinfo("库存报表", report_text)
        except Exception as e:
            messagebox.showerror("错误", f"生成库存报表失败: {e}")
    
    def show_customer_analysis(self):
        """显示客户分析"""
        try:
            customer_data = self.report_service.get_customer_analysis_report()
            
            # 统计客户信息
            total_customers = len(customer_data)
            active_customers = sum(1 for customer in customer_data if customer['order_count'] > 0)
            total_spent = sum(customer['total_spent'] or 0 for customer in customer_data)
            avg_spending = total_spent / active_customers if active_customers > 0 else 0
            
            # 计算新增客户（最近30天有订单的客户）
            from datetime import date, timedelta
            recent_date = date.today() - timedelta(days=30)
            new_customers = sum(1 for customer in customer_data 
                              if customer['last_visit_date'] and 
                              customer['last_visit_date'] >= recent_date.strftime('%Y-%m-%d'))
            
            report_text = f"""客户分析报表

客户总数: {total_customers} 人
活跃客户: {active_customers} 人
新增客户: {new_customers} 人
平均消费: ¥{avg_spending:.2f}"""
            messagebox.showinfo("客户分析", report_text)
        except Exception as e:
            messagebox.showerror("错误", f"生成客户分析失败: {e}")
    
    def backup_data(self):
        """备份数据"""
        try:
            from utils.database_utils import DatabaseUtils
            backup_file = DatabaseUtils.backup_database()
            messagebox.showinfo("成功", f"数据备份成功！\n备份文件：{backup_file}")
        except Exception as e:
            messagebox.showerror("错误", f"数据备份失败: {e}")
    
    def restore_data(self):
        """恢复数据"""
        try:
            from tkinter import filedialog
            from utils.database_utils import DatabaseUtils
            
            backup_file = filedialog.askopenfilename(
                title="选择备份文件",
                filetypes=[("数据库文件", "*.db"), ("所有文件", "*.*")]
            )
            
            if backup_file:
                if messagebox.askyesno("确认", "恢复数据将覆盖当前数据，确定继续吗？"):
                    DatabaseUtils.restore_database(backup_file)
                    messagebox.showinfo("成功", "数据恢复成功！请重启应用程序。")
        except Exception as e:
            messagebox.showerror("错误", f"数据恢复失败: {e}")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = f"""{APP_NAME} v{APP_VERSION}

专为汽修店设计的记账管理软件

功能特点:
• 配件库存管理
• 进货记录管理
• 维修订单管理
• 客户信息管理
• 财务统计分析

技术支持: AI Assistant
"""
        messagebox.showinfo("关于", about_text)
    
    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()
        except Exception as e:
            messagebox.showerror("错误", f"程序运行出错: {e}")
            self.root.quit()