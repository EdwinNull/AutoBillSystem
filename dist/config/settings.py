#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据库配置
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DATABASE_PATH = DATA_DIR / "auto_repair.db"

# 应用配置
APP_NAME = "汽修店记账软件"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# 数据库配置
DB_TIMEOUT = 30  # 数据库连接超时时间（秒）

# 库存预警配置
DEFAULT_MIN_STOCK = 10  # 默认最小库存预警值

# 日期格式
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 报表配置
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

# 备份配置
BACKUP_DIR = PROJECT_ROOT / "backups"
BACKUP_DIR.mkdir(exist_ok=True)