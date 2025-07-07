#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库工具模块
"""

import sqlite3
import shutil
import os
from datetime import datetime
from pathlib import Path
from config.settings import DATABASE_PATH, BACKUP_DIR

class DatabaseUtils:
    """数据库工具类"""
    
    @staticmethod
    def backup_database(backup_name=None):
        """备份数据库"""
        try:
            if not backup_name:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"auto_repair_backup_{timestamp}.db"
            
            backup_path = BACKUP_DIR / backup_name
            
            # 确保备份目录存在
            BACKUP_DIR.mkdir(exist_ok=True)
            
            # 复制数据库文件
            shutil.copy2(DATABASE_PATH, backup_path)
            
            return str(backup_path)
        except Exception as e:
            raise Exception(f"数据库备份失败: {e}")
    
    @staticmethod
    def restore_database(backup_path):
        """恢复数据库"""
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"备份文件不存在: {backup_path}")
            
            # 验证备份文件是否为有效的SQLite数据库
            conn = sqlite3.connect(backup_path)
            conn.execute('SELECT 1')
            conn.close()
            
            # 备份当前数据库
            current_backup = DatabaseUtils.backup_database("current_backup_before_restore.db")
            
            # 恢复数据库
            shutil.copy2(backup_path, DATABASE_PATH)
            
            return current_backup
        except Exception as e:
            raise Exception(f"数据库恢复失败: {e}")
    
    @staticmethod
    def get_backup_list():
        """获取备份文件列表"""
        try:
            if not BACKUP_DIR.exists():
                return []
            
            backup_files = []
            for file_path in BACKUP_DIR.glob('*.db'):
                stat = file_path.stat()
                backup_files.append({
                    'name': file_path.name,
                    'path': str(file_path),
                    'size': stat.st_size,
                    'create_time': datetime.fromtimestamp(stat.st_ctime),
                    'modify_time': datetime.fromtimestamp(stat.st_mtime)
                })
            
            # 按修改时间倒序排列
            backup_files.sort(key=lambda x: x['modify_time'], reverse=True)
            return backup_files
        except Exception as e:
            raise Exception(f"获取备份列表失败: {e}")
    
    @staticmethod
    def delete_backup(backup_path):
        """删除备份文件"""
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
                return True
            return False
        except Exception as e:
            raise Exception(f"删除备份文件失败: {e}")
    
    @staticmethod
    def vacuum_database():
        """压缩数据库"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.execute('VACUUM')
            conn.close()
            return True
        except Exception as e:
            raise Exception(f"数据库压缩失败: {e}")
    
    @staticmethod
    def check_database_integrity():
        """检查数据库完整性"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('PRAGMA integrity_check')
            result = cursor.fetchone()
            conn.close()
            
            return result[0] == 'ok'
        except Exception as e:
            raise Exception(f"数据库完整性检查失败: {e}")
    
    @staticmethod
    def get_database_info():
        """获取数据库信息"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # 获取数据库大小
            cursor.execute('PRAGMA page_count')
            page_count = cursor.fetchone()[0]
            cursor.execute('PRAGMA page_size')
            page_size = cursor.fetchone()[0]
            db_size = page_count * page_size
            
            # 获取表信息
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # 获取每个表的记录数
            table_counts = {}
            for table in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                table_counts[table] = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'size': db_size,
                'page_count': page_count,
                'page_size': page_size,
                'tables': tables,
                'table_counts': table_counts
            }
        except Exception as e:
            raise Exception(f"获取数据库信息失败: {e}")