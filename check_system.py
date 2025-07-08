#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统兼容性检查脚本
在打包前检查系统环境和依赖
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        return False
    else:
        print("✅ Python版本符合要求")
        return True

def check_system_info():
    """检查系统信息"""
    print("\n检查系统信息...")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    print(f"处理器: {platform.processor()}")
    
    if platform.system() != 'Windows':
        print("⚠️  警告: 本打包脚本主要针对Windows系统优化")
    else:
        print("✅ Windows系统，适合打包")
    
    return True

def check_required_modules():
    """检查必需的模块"""
    print("\n检查必需模块...")
    required_modules = [
        'tkinter',
        'sqlite3',
        'datetime',
        'decimal',
        'pathlib',
        'json',
        'csv',
        'os',
        'sys'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - 缺失")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ 缺失模块: {', '.join(missing_modules)}")
        return False
    else:
        print("\n✅ 所有必需模块都已安装")
        return True

def check_pyinstaller():
    """检查PyInstaller"""
    print("\n检查PyInstaller...")
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        print("请运行: pip install pyinstaller")
        return False

def check_project_structure():
    """检查项目结构"""
    print("\n检查项目结构...")
    required_files = [
        'main.py',
        'models/__init__.py',
        'gui/__init__.py',
        'services/__init__.py',
        'config/__init__.py'
    ]
    
    optional_files = [
        'data/',
        'config/settings.py',
        'README.md',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} - 缺失")
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    for file_path in optional_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} (可选)")
        else:
            print(f"⚠️  {file_path} (可选) - 不存在")
    
    if missing_files:
        print(f"\n❌ 缺失必需文件: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ 项目结构完整")
        return True

def check_disk_space():
    """检查磁盘空间"""
    print("\n检查磁盘空间...")
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free // (1024**3)
        print(f"可用磁盘空间: {free_gb} GB")
        
        if free_gb < 2:
            print("⚠️  警告: 可用磁盘空间不足2GB，可能影响打包")
            return False
        else:
            print("✅ 磁盘空间充足")
            return True
    except Exception as e:
        print(f"⚠️  无法检查磁盘空间: {e}")
        return True

def check_dependencies():
    """检查项目依赖"""
    print("\n检查项目依赖...")
    
    # 尝试导入项目模块
    try:
        sys.path.insert(0, '.')
        
        # 检查主要模块
        from models import database, orders, customers, parts
        from services import order_service, inventory_service
        from gui import main_window
        
        print("✅ 所有项目模块导入成功")
        return True
        
    except ImportError as e:
        print(f"❌ 项目模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"⚠️  检查项目依赖时出错: {e}")
        return True

def suggest_optimizations():
    """建议优化措施"""
    print("\n=== 优化建议 ===")
    
    suggestions = [
        "1. 创建应用图标文件 (assets/icon.ico) 以美化exe文件",
        "2. 添加版本信息文件以显示程序详细信息",
        "3. 考虑使用 --onedir 模式以提高启动速度",
        "4. 排除不必要的模块以减小文件大小",
        "5. 测试打包后的程序在不同Windows版本上的兼容性",
        "6. 考虑创建安装程序以提供更好的用户体验",
        "7. 添加数字签名以避免杀毒软件误报"
    ]
    
    for suggestion in suggestions:
        print(f"💡 {suggestion}")

def create_assets_directory():
    """创建资源目录"""
    assets_dir = Path('assets')
    if not assets_dir.exists():
        assets_dir.mkdir()
        print(f"\n📁 已创建资源目录: {assets_dir}")
        
        # 创建图标说明文件
        icon_readme = assets_dir / 'README.txt'
        with open(icon_readme, 'w', encoding='utf-8') as f:
            f.write("资源文件目录\n\n")
            f.write("请将以下文件放置在此目录中：\n")
            f.write("- icon.ico: 应用程序图标文件 (推荐尺寸: 256x256)\n")
            f.write("- splash.png: 启动画面图片 (可选)\n")
            f.write("- logo.png: 应用程序标志 (可选)\n")
        
        print(f"📄 已创建说明文件: {icon_readme}")

def main():
    """主检查函数"""
    print("=" * 60)
    print("汽车维修管理系统 - 打包前系统检查")
    print("=" * 60)
    
    checks = [
        check_python_version,
        check_system_info,
        check_required_modules,
        check_pyinstaller,
        check_project_structure,
        check_disk_space,
        check_dependencies
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ 检查过程中出错: {e}")
            results.append(False)
    
    # 创建资源目录
    create_assets_directory()
    
    # 显示总结
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有检查通过 ({passed}/{total})")
        print("\n🎉 系统已准备好进行打包！")
        print("\n下一步：")
        print("1. 运行 package.bat 进行快速打包")
        print("2. 或运行 python build_exe.py 进行高级打包")
    else:
        print(f"⚠️  部分检查未通过 ({passed}/{total})")
        print("\n请解决上述问题后再进行打包")
    
    # 显示优化建议
    suggest_optimizations()
    
    print("\n" + "=" * 60)
    return passed == total

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)