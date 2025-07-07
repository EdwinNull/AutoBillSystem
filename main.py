#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汽修店记账软件主程序
作者: AI Assistant
版本: 1.0
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.main_window import MainWindow
from models.database import DatabaseManager
from config.settings import DATABASE_PATH

def main():
    """主程序入口"""
    try:
        # 初始化数据库
        db_manager = DatabaseManager(DATABASE_PATH)
        db_manager.init_database()
        
        # 启动GUI应用
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()