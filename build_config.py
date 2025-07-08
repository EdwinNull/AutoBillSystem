#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包配置文件
包含PyInstaller的详细配置选项
"""

import os
import sys
from pathlib import Path

# 项目基本信息
APP_NAME = "汽车维修管理系统"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "专业的汽车维修管理系统"
APP_AUTHOR = "开发团队"

# 打包配置
BUILD_CONFIG = {
    # 基本选项
    'onefile': True,  # 打包成单个exe文件
    'windowed': True,  # 不显示控制台窗口
    'name': APP_NAME,
    
    # 图标和版本信息
    'icon': 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    
    # 包含的数据文件和目录
    'datas': [
        ('data', 'data'),
        ('config', 'config'),
    ],
    
    # 隐藏导入的模块
    'hidden_imports': [
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'sqlite3',
        'datetime',
        'decimal',
        'pathlib',
        'json',
        'csv',
        'os',
        'sys',
        'threading',
    ],
    
    # 收集所有子模块
    'collect_all': [
        'tkinter',
    ],
    
    # 排除的模块（减小文件大小）
    'excludes': [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'IPython',
    ],
    
    # 优化选项
    'optimize': 2,  # 字节码优化级别
    'strip': True,  # 去除调试信息
    'upx': False,  # 不使用UPX压缩（可能导致杀毒软件误报）
}

# 版本信息文件内容
VERSION_INFO = f"""
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'080404B0',
        [StringStruct(u'CompanyName', u'{APP_AUTHOR}'),
        StringStruct(u'FileDescription', u'{APP_DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{APP_VERSION}'),
        StringStruct(u'InternalName', u'{APP_NAME}'),
        StringStruct(u'LegalCopyright', u'Copyright © 2024 {APP_AUTHOR}'),
        StringStruct(u'OriginalFilename', u'{APP_NAME}.exe'),
        StringStruct(u'ProductName', u'{APP_NAME}'),
        StringStruct(u'ProductVersion', u'{APP_VERSION}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
"""

def get_pyinstaller_args():
    """生成PyInstaller命令行参数"""
    args = ['pyinstaller']
    
    # 基本选项
    if BUILD_CONFIG['onefile']:
        args.append('--onefile')
    
    if BUILD_CONFIG['windowed']:
        args.append('--windowed')
    
    # 应用名称
    args.extend(['--name', BUILD_CONFIG['name']])
    
    # 图标
    if BUILD_CONFIG['icon'] and os.path.exists(BUILD_CONFIG['icon']):
        args.extend(['--icon', BUILD_CONFIG['icon']])
    
    # 数据文件
    for src, dst in BUILD_CONFIG['datas']:
        if os.path.exists(src):
            args.extend(['--add-data', f'{src};{dst}'])
    
    # 隐藏导入
    for module in BUILD_CONFIG['hidden_imports']:
        args.extend(['--hidden-import', module])
    
    # 收集所有子模块
    for module in BUILD_CONFIG['collect_all']:
        args.extend(['--collect-all', module])
    
    # 排除模块
    for module in BUILD_CONFIG['excludes']:
        args.extend(['--exclude-module', module])
    
    # 优化选项
    if BUILD_CONFIG['strip']:
        args.append('--strip')
    
    if not BUILD_CONFIG['upx']:
        args.append('--noupx')
    
    # 主文件
    args.append('main.py')
    
    return args

def create_version_file():
    """创建版本信息文件"""
    version_content = VERSION_INFO.format(
        APP_NAME=APP_NAME,
        APP_VERSION=APP_VERSION,
        APP_DESCRIPTION=APP_DESCRIPTION,
        APP_AUTHOR=APP_AUTHOR
    )
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    return 'version_info.txt'

def create_spec_file():
    """创建.spec文件用于高级配置"""
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('config', 'config'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'sqlite3',
        'datetime',
        'decimal',
        'pathlib',
        'json',
        'csv',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
"""
    
    with open(f'{APP_NAME}.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    return f'{APP_NAME}.spec'

if __name__ == '__main__':
    print("打包配置信息:")
    print(f"应用名称: {APP_NAME}")
    print(f"版本: {APP_VERSION}")
    print(f"描述: {APP_DESCRIPTION}")
    print("\nPyInstaller参数:")
    args = get_pyinstaller_args()
    print(' '.join(args))