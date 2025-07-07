#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存查询窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from services.inventory_service import InventoryService

class InventoryQueryWindow:
    """库存查询窗口类"""
    
    def __init__(self, parent):
        self.parent = parent
        self.inventory_service = InventoryService()
        self.setup_window()
        self.setup_widgets()
        self.load_data()
    
    def setup_window(self):
        """设置窗口属性"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("库存查询")
        self.window.geometry("1000x600")
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
        
        # 关键字搜索
        ttk.Label(search_frame, text="关键字:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.keyword_var = tk.StringVar()
        keyword_entry = ttk.Entry(search_frame, textvariable=self.keyword_var, width=20)
        keyword_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 类别筛选
        ttk.Label(search_frame, text="类别:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, width=15, state="readonly")
        self.category_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # 库存状态筛选
        ttk.Label(search_frame, text="库存状态:").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
        self.stock_status_var = tk.StringVar(value="全部")
        stock_status_combo = ttk.Combobox(search_frame, textvariable=self.stock_status_var, 
                                        values=["全部", "正常", "库存不足", "零库存"], 
                                        width=10, state="readonly")
        stock_status_combo.grid(row=0, column=5, sticky=tk.W, padx=(0, 20))
        
        # 查询按钮
        search_btn = ttk.Button(search_frame, text="查询", command=self.search_inventory)
        search_btn.grid(row=0, column=6, padx=(10, 0))
        
        reset_btn = ttk.Button(search_frame, text="重置", command=self.reset_search)
        reset_btn.grid(row=0, column=7, padx=(5, 0))
        
        # 库存列表区域
        list_frame = ttk.LabelFrame(main_frame, text="库存列表", padding="10")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('part_code', 'part_name', 'category', 'stock_quantity', 'min_stock', 
                  'purchase_price', 'selling_price', 'stock_value', 'status')
        self.inventory_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题
        self.inventory_tree.heading('part_code', text='配件编号')
        self.inventory_tree.heading('part_name', text='配件名称')
        self.inventory_tree.heading('category', text='类别')
        self.inventory_tree.heading('stock_quantity', text='库存数量')
        self.inventory_tree.heading('min_stock', text='最低库存')
        self.inventory_tree.heading('purchase_price', text='进货价')
        self.inventory_tree.heading('selling_price', text='销售价')
        self.inventory_tree.heading('stock_value', text='库存价值')
        self.inventory_tree.heading('status', text='状态')
        
        # 设置列宽
        self.inventory_tree.column('part_code', width=100)
        self.inventory_tree.column('part_name', width=150)
        self.inventory_tree.column('category', width=100)
        self.inventory_tree.column('stock_quantity', width=80)
        self.inventory_tree.column('min_stock', width=80)
        self.inventory_tree.column('purchase_price', width=80)
        self.inventory_tree.column('selling_price', width=80)
        self.inventory_tree.column('stock_value', width=80)
        self.inventory_tree.column('status', width=80)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inventory_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
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
        
        export_btn = ttk.Button(bottom_frame, text="导出Excel", command=self.export_to_excel)
        export_btn.grid(row=0, column=0, padx=(0, 10))
        
        refresh_btn = ttk.Button(bottom_frame, text="刷新", command=self.load_data)
        refresh_btn.grid(row=0, column=1, padx=(0, 10))
        
        close_btn = ttk.Button(bottom_frame, text="关闭", command=self.window.destroy)
        close_btn.grid(row=0, column=2)
        
        # 绑定双击事件
        self.inventory_tree.bind('<Double-1>', self.on_item_double_click)
    
    def load_data(self):
        """加载数据"""
        self.load_categories()
        self.load_inventory()
    
    def load_categories(self):
        """加载配件类别"""
        try:
            categories = self.inventory_service.get_part_categories()
            category_list = ["全部"] + categories
            self.category_combo['values'] = category_list
            self.category_var.set("全部")
        except Exception as e:
            messagebox.showerror("错误", f"加载类别失败: {e}")
    
    def load_inventory(self, parts=None):
        """加载库存数据"""
        try:
            # 清空现有记录
            for item in self.inventory_tree.get_children():
                self.inventory_tree.delete(item)
            
            # 获取库存数据
            if parts is None:
                parts = self.inventory_service.get_all_parts()
            
            total_parts = 0
            total_value = 0
            low_stock_count = 0
            zero_stock_count = 0
            
            for part in parts:
                # 计算库存价值
                stock_value = part.stock_quantity * part.purchase_price
                total_value += stock_value
                total_parts += 1
                
                # 判断库存状态
                if part.stock_quantity == 0:
                    status = "零库存"
                    zero_stock_count += 1
                elif part.stock_quantity <= part.min_stock:
                    status = "库存不足"
                    low_stock_count += 1
                else:
                    status = "正常"
                
                # 设置行颜色
                tags = ()
                if status == "零库存":
                    tags = ('zero_stock',)
                elif status == "库存不足":
                    tags = ('low_stock',)
                
                # 插入数据
                self.inventory_tree.insert('', 'end', values=(
                    part.part_code,
                    part.part_name,
                    part.category,
                    part.stock_quantity,
                    part.min_stock,
                    f"¥{part.purchase_price:.2f}",
                    f"¥{part.selling_price:.2f}",
                    f"¥{stock_value:.2f}",
                    status
                ), tags=tags)
            
            # 设置行颜色
            self.inventory_tree.tag_configure('zero_stock', background='#ffcccc')
            self.inventory_tree.tag_configure('low_stock', background='#fff2cc')
            
            # 更新统计信息
            normal_count = total_parts - low_stock_count - zero_stock_count
            stats_text = (f"配件总数: {total_parts} | "
                         f"正常: {normal_count} | "
                         f"库存不足: {low_stock_count} | "
                         f"零库存: {zero_stock_count} | "
                         f"总价值: ¥{total_value:.2f}")
            self.stats_var.set(stats_text)
            
        except Exception as e:
            messagebox.showerror("错误", f"加载库存数据失败: {e}")
    
    def search_inventory(self):
        """搜索库存"""
        try:
            keyword = self.keyword_var.get().strip()
            category = self.category_var.get() if self.category_var.get() != "全部" else ""
            stock_status = self.stock_status_var.get()
            
            # 搜索配件
            parts = self.inventory_service.search_parts(keyword, category)
            
            # 根据库存状态筛选
            if stock_status != "全部":
                filtered_parts = []
                for part in parts:
                    if stock_status == "零库存" and part.stock_quantity == 0:
                        filtered_parts.append(part)
                    elif stock_status == "库存不足" and 0 < part.stock_quantity <= part.min_stock:
                        filtered_parts.append(part)
                    elif stock_status == "正常" and part.stock_quantity > part.min_stock:
                        filtered_parts.append(part)
                parts = filtered_parts
            
            # 加载搜索结果
            self.load_inventory(parts)
            
        except Exception as e:
            messagebox.showerror("错误", f"搜索失败: {e}")
    
    def reset_search(self):
        """重置搜索条件"""
        self.keyword_var.set('')
        self.category_var.set('全部')
        self.stock_status_var.set('全部')
        self.load_inventory()
    
    def on_item_double_click(self, event):
        """双击事件处理"""
        selection = self.inventory_tree.selection()
        if selection:
            item = self.inventory_tree.item(selection[0])
            values = item['values']
            
            # 显示详细信息
            detail_text = f"""配件详细信息

配件编号: {values[0]}
配件名称: {values[1]}
类别: {values[2]}
库存数量: {values[3]}
最低库存: {values[4]}
进货价: {values[5]}
销售价: {values[6]}
库存价值: {values[7]}
状态: {values[8]}"""
            
            messagebox.showinfo("配件详情", detail_text)
    
    def export_to_excel(self):
        """导出到Excel"""
        try:
            from tkinter import filedialog
            from utils.export_utils import ExportUtils
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                title="导出库存报表",
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
            )
            
            if file_path:
                # 获取当前显示的数据
                data = []
                for item in self.inventory_tree.get_children():
                    values = self.inventory_tree.item(item)['values']
                    data.append(values)
                
                # 导出数据
                headers = ['配件编号', '配件名称', '类别', '库存数量', '最低库存', 
                          '进货价', '销售价', '库存价值', '状态']
                
                ExportUtils.export_to_excel(data, headers, file_path, "库存报表")
                messagebox.showinfo("成功", f"库存报表已导出到: {file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {e}")