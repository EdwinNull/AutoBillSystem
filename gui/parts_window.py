#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配件管理窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
from services.inventory_service import InventoryService
from models.parts import Part

class PartsWindow:
    """配件管理窗口"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.inventory_service = InventoryService()
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.setup_window()
        self.setup_widgets()
        self.load_parts()
    
    def setup_window(self):
        """设置窗口属性"""
        self.window.title("配件管理")
        self.window.geometry("1000x600")
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
        search_frame = ttk.LabelFrame(main_frame, text="搜索配件", padding="5")
        search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="关键词:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(search_frame, text="类别:").grid(row=0, column=2, padx=(0, 5))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, width=15)
        self.category_combo.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(search_frame, text="搜索", command=self.search_parts).grid(row=0, column=4, padx=(0, 5))
        ttk.Button(search_frame, text="重置", command=self.reset_search).grid(row=0, column=5)
        
        # 左侧：配件列表
        list_frame = ttk.LabelFrame(main_frame, text="配件列表", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 配件列表
        columns = ('ID', '名称', '编号', '类别', '库存', '单位', '进价', '售价')
        self.parts_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题和宽度
        column_widths = {'ID': 50, '名称': 120, '编号': 100, '类别': 80, '库存': 60, '单位': 50, '进价': 70, '售价': 70}
        for col in columns:
            self.parts_tree.heading(col, text=col)
            self.parts_tree.column(col, width=column_widths.get(col, 100))
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.parts_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.parts_tree.xview)
        self.parts_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.parts_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 绑定选择事件
        self.parts_tree.bind('<<TreeviewSelect>>', self.on_part_select)
        
        # 右侧：配件详情和操作
        detail_frame = ttk.LabelFrame(main_frame, text="配件详情", padding="10")
        detail_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配件信息输入框
        self.setup_detail_form(detail_frame)
        
        # 底部按钮
        button_frame = ttk.Frame(detail_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="新增", command=self.add_part).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="修改", command=self.update_part).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="删除", command=self.delete_part).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(button_frame, text="清空", command=self.clear_form).grid(row=0, column=3)
        
        # 加载类别数据
        self.load_categories()
    
    def setup_detail_form(self, parent):
        """设置详情表单"""
        # 配件名称
        ttk.Label(parent, text="配件名称:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.name_var, width=25).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 配件编号
        ttk.Label(parent, text="配件编号:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.code_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.code_var, width=25).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 类别
        ttk.Label(parent, text="类别:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.detail_category_var = tk.StringVar()
        self.detail_category_combo = ttk.Combobox(parent, textvariable=self.detail_category_var, width=23)
        self.detail_category_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 品牌
        ttk.Label(parent, text="品牌:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.brand_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.brand_var, width=25).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 规格
        ttk.Label(parent, text="规格:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.spec_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.spec_var, width=25).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 单位
        ttk.Label(parent, text="单位:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.unit_var = tk.StringVar(value="个")
        unit_combo = ttk.Combobox(parent, textvariable=self.unit_var, values=["个", "套", "米", "升", "公斤"], width=23)
        unit_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 进价
        ttk.Label(parent, text="进价:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.purchase_price_var = tk.StringVar(value="0.00")
        ttk.Entry(parent, textvariable=self.purchase_price_var, width=25).grid(row=6, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 售价
        ttk.Label(parent, text="售价:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.selling_price_var = tk.StringVar(value="0.00")
        ttk.Entry(parent, textvariable=self.selling_price_var, width=25).grid(row=7, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 库存数量
        ttk.Label(parent, text="库存数量:").grid(row=8, column=0, sticky=tk.W, pady=2)
        self.stock_var = tk.StringVar(value="0")
        ttk.Entry(parent, textvariable=self.stock_var, width=25).grid(row=8, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 最小库存
        ttk.Label(parent, text="最小库存:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.min_stock_var = tk.StringVar(value="10")
        ttk.Entry(parent, textvariable=self.min_stock_var, width=25).grid(row=9, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 供应商
        ttk.Label(parent, text="供应商:").grid(row=10, column=0, sticky=tk.W, pady=2)
        self.supplier_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.supplier_var, width=25).grid(row=10, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # 配置列权重
        parent.columnconfigure(1, weight=1)
        
        # 当前选中的配件ID
        self.current_part_id = None
    
    def load_categories(self):
        """加载配件类别"""
        try:
            categories = self.inventory_service.get_part_categories()
            categories.insert(0, "")  # 添加空选项
            self.category_combo['values'] = categories
            self.detail_category_combo['values'] = categories
        except Exception as e:
            messagebox.showerror("错误", f"加载类别失败: {e}")
    
    def load_parts(self):
        """加载配件列表"""
        try:
            # 清空现有数据
            for item in self.parts_tree.get_children():
                self.parts_tree.delete(item)
            
            # 获取配件数据
            parts = self.inventory_service.get_all_parts()
            
            # 插入数据到树形控件
            for part in parts:
                values = (
                    part.part_id,
                    part.part_name,
                    part.part_code or '',
                    part.category or '',
                    part.stock_quantity,
                    part.unit,
                    f"{part.purchase_price:.2f}",
                    f"{part.selling_price:.2f}"
                )
                
                # 库存不足的行用红色标记
                tags = ('low_stock',) if part.stock_quantity <= part.min_stock else ()
                self.parts_tree.insert('', tk.END, values=values, tags=tags)
            
            # 设置标签样式
            self.parts_tree.tag_configure('low_stock', background='#ffcccc')
            
        except Exception as e:
            messagebox.showerror("错误", f"加载配件列表失败: {e}")
    
    def search_parts(self):
        """搜索配件"""
        try:
            keyword = self.search_var.get().strip()
            category = self.category_var.get().strip()
            
            # 清空现有数据
            for item in self.parts_tree.get_children():
                self.parts_tree.delete(item)
            
            # 搜索配件
            parts = self.inventory_service.search_parts(keyword, category)
            
            # 插入搜索结果
            for part in parts:
                values = (
                    part.part_id,
                    part.part_name,
                    part.part_code or '',
                    part.category or '',
                    part.stock_quantity,
                    part.unit,
                    f"{part.purchase_price:.2f}",
                    f"{part.selling_price:.2f}"
                )
                
                tags = ('low_stock',) if part.stock_quantity <= part.min_stock else ()
                self.parts_tree.insert('', tk.END, values=values, tags=tags)
            
        except Exception as e:
            messagebox.showerror("错误", f"搜索配件失败: {e}")
    
    def reset_search(self):
        """重置搜索"""
        self.search_var.set("")
        self.category_var.set("")
        self.load_parts()
    
    def on_part_select(self, event):
        """配件选择事件"""
        selection = self.parts_tree.selection()
        if selection:
            item = self.parts_tree.item(selection[0])
            values = item['values']
            
            # 获取完整的配件信息
            part_id = values[0]
            try:
                part = self.inventory_service.part_dao.get_part_by_id(part_id)
                if part:
                    self.load_part_to_form(part)
            except Exception as e:
                messagebox.showerror("错误", f"加载配件详情失败: {e}")
    
    def load_part_to_form(self, part):
        """将配件信息加载到表单"""
        self.current_part_id = part.part_id
        self.name_var.set(part.part_name)
        self.code_var.set(part.part_code or '')
        self.detail_category_var.set(part.category or '')
        self.brand_var.set(part.brand or '')
        self.spec_var.set(part.specification or '')
        self.unit_var.set(part.unit)
        self.purchase_price_var.set(f"{part.purchase_price:.2f}")
        self.selling_price_var.set(f"{part.selling_price:.2f}")
        self.stock_var.set(str(part.stock_quantity))
        self.min_stock_var.set(str(part.min_stock))
        self.supplier_var.set(part.supplier or '')
    
    def clear_form(self):
        """清空表单"""
        self.current_part_id = None
        self.name_var.set("")
        self.code_var.set("")
        self.detail_category_var.set("")
        self.brand_var.set("")
        self.spec_var.set("")
        self.unit_var.set("个")
        self.purchase_price_var.set("0.00")
        self.selling_price_var.set("0.00")
        self.stock_var.set("0")
        self.min_stock_var.set("10")
        self.supplier_var.set("")
    
    def validate_form(self):
        """验证表单数据"""
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入配件名称")
            return False
        
        try:
            float(self.purchase_price_var.get())
            float(self.selling_price_var.get())
            int(self.stock_var.get())
            int(self.min_stock_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return False
        
        return True
    
    def get_form_data(self):
        """获取表单数据"""
        return {
            'part_name': self.name_var.get().strip(),
            'part_code': self.code_var.get().strip(),
            'category': self.detail_category_var.get().strip(),
            'brand': self.brand_var.get().strip(),
            'specification': self.spec_var.get().strip(),
            'unit': self.unit_var.get(),
            'purchase_price': float(self.purchase_price_var.get()),
            'selling_price': float(self.selling_price_var.get()),
            'stock_quantity': int(self.stock_var.get()),
            'min_stock': int(self.min_stock_var.get()),
            'supplier': self.supplier_var.get().strip()
        }
    
    def add_part(self):
        """添加配件"""
        if not self.validate_form():
            return
        
        try:
            part_data = self.get_form_data()
            self.inventory_service.add_part(part_data)
            messagebox.showinfo("成功", "配件添加成功")
            self.load_parts()
            self.load_categories()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("错误", f"添加配件失败: {e}")
    
    def update_part(self):
        """修改配件"""
        if not self.current_part_id:
            messagebox.showerror("错误", "请先选择要修改的配件")
            return
        
        if not self.validate_form():
            return
        
        try:
            part_data = self.get_form_data()
            part_data['part_id'] = self.current_part_id
            self.inventory_service.update_part(part_data)
            messagebox.showinfo("成功", "配件修改成功")
            self.load_parts()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("错误", f"修改配件失败: {e}")
    
    def delete_part(self):
        """删除配件"""
        if not self.current_part_id:
            messagebox.showerror("错误", "请先选择要删除的配件")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的配件吗？"):
            try:
                self.inventory_service.delete_part(self.current_part_id)
                messagebox.showinfo("成功", "配件删除成功")
                self.load_parts()
                self.load_categories()
                self.clear_form()
            except Exception as e:
                messagebox.showerror("错误", f"删除配件失败: {e}")

# 测试代码
if __name__ == "__main__":
    app = PartsWindow()
    app.window.mainloop()