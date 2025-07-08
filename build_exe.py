#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将汽车维修管理系统打包为exe文件
使用PyInstaller进行打包
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")
    
    # 清理.spec文件
    spec_files = list(Path('.').glob('*.spec'))
    for spec_file in spec_files:
        spec_file.unlink()
        print(f"已删除文件: {spec_file}")

def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print("PyInstaller安装完成")

def create_build_script():
    """创建打包脚本"""
    # PyInstaller命令参数
    cmd = [
        'pyinstaller',
        '--onefile',  # 打包成单个exe文件
        '--windowed',  # 不显示控制台窗口
        '--name=汽车维修管理系统',  # 指定exe文件名
        '--icon=icon.ico',  # 图标文件（如果存在）
        '--add-data=data;data',  # 包含数据目录
        '--add-data=config;config',  # 包含配置目录
        '--hidden-import=tkinter',
        '--hidden-import=sqlite3',
        '--hidden-import=datetime',
        '--hidden-import=decimal',
        '--collect-all=tkinter',
        'main.py'
    ]
    
    return cmd

def build_exe():
    """执行打包"""
    print("开始打包...")
    
    # 检查图标文件是否存在，如果不存在则从命令中移除
    cmd = create_build_script()
    if not os.path.exists('icon.ico'):
        cmd = [arg for arg in cmd if not arg.startswith('--icon')]
        print("未找到icon.ico文件，跳过图标设置")
    
    try:
        subprocess.check_call(cmd)
        print("\n打包完成！")
        print("可执行文件位置: dist/汽车维修管理系统.exe")
        
        # 复制必要的文件到dist目录
        copy_additional_files()
        
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False
    
    return True

def copy_additional_files():
    """复制额外的文件到dist目录"""
    dist_dir = Path('dist')
    
    # 创建必要的目录结构
    (dist_dir / 'data').mkdir(exist_ok=True)
    (dist_dir / 'config').mkdir(exist_ok=True)
    (dist_dir / 'reports').mkdir(exist_ok=True)
    (dist_dir / 'backups').mkdir(exist_ok=True)
    
    # 复制配置文件
    if os.path.exists('config/settings.py'):
        shutil.copy2('config/settings.py', dist_dir / 'config')
    
    # 复制README文件
    if os.path.exists('README.md'):
        shutil.copy2('README.md', dist_dir)
    
    # 创建启动说明文件
    readme_content = """
汽车维修管理系统 - 使用说明

1. 双击"汽车维修管理系统.exe"启动程序
2. 首次运行会自动创建数据库文件
3. 数据文件保存在data目录下
4. 报表文件保存在reports目录下
5. 备份文件保存在backups目录下

注意事项：
- 请确保有足够的磁盘空间
- 建议定期备份data目录
- 如遇问题，请检查是否有杀毒软件拦截

技术支持：请联系开发团队
"""
    
    with open(dist_dir / '使用说明.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("已复制必要文件到dist目录")

def create_installer_script():
    """创建安装包脚本（可选）"""
    installer_script = """
; 汽车维修管理系统安装脚本
; 使用Inno Setup编译

[Setup]
AppName=汽车维修管理系统
AppVersion=1.0
DefaultDirName={pf}\汽车维修管理系统
DefaultGroupName=汽车维修管理系统
OutputDir=installer
OutputBaseFilename=汽车维修管理系统_安装包
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\汽车维修管理系统.exe"; DestDir: "{app}"
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\汽车维修管理系统"; Filename: "{app}\汽车维修管理系统.exe"
Name: "{commondesktop}\汽车维修管理系统"; Filename: "{app}\汽车维修管理系统.exe"

[Run]
Filename: "{app}\汽车维修管理系统.exe"; Description: "启动汽车维修管理系统"; Flags: nowait postinstall skipifsilent
"""
    
    with open('installer_script.iss', 'w', encoding='utf-8') as f:
        f.write(installer_script)
    
    print("已创建安装包脚本: installer_script.iss")
    print("可使用Inno Setup编译生成安装包")

def main():
    """主函数"""
    print("=" * 50)
    print("汽车维修管理系统 - 打包工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('main.py'):
        print("错误: 请在项目根目录下运行此脚本")
        return
    
    # 清理之前的构建
    clean_build_dirs()
    
    # 安装PyInstaller
    install_pyinstaller()
    
    # 执行打包
    if build_exe():
        print("\n打包成功！")
        print("\n可选步骤:")
        print("1. 测试dist目录下的exe文件")
        print("2. 使用installer_script.iss创建安装包")
        
        # 创建安装包脚本
        create_installer_script()
    else:
        print("\n打包失败，请检查错误信息")

if __name__ == '__main__':
    main()