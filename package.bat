@echo off
chcp 65001 >nul
echo ========================================
echo 汽车维修管理系统 - 一键打包工具
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

:: 检查是否在正确的目录
if not exist "main.py" (
    echo 错误: 请在项目根目录下运行此脚本
    pause
    exit /b 1
)

echo 正在检查并安装依赖...
python -m pip install pyinstaller
if errorlevel 1 (
    echo 错误: 安装PyInstaller失败
    pause
    exit /b 1
)

echo.
echo 正在清理之前的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo.
echo 开始打包，请稍候...
pyinstaller --onefile --windowed --name="汽车维修管理系统" --add-data="data;data" --add-data="config;config" --hidden-import=tkinter --hidden-import=sqlite3 --collect-all=tkinter main.py

if errorlevel 1 (
    echo.
    echo 打包失败！请检查错误信息。
    pause
    exit /b 1
)

echo.
echo 正在复制必要文件...
if not exist "dist\data" mkdir "dist\data"
if not exist "dist\config" mkdir "dist\config"
if not exist "dist\reports" mkdir "dist\reports"
if not exist "dist\backups" mkdir "dist\backups"

if exist "config\settings.py" copy "config\settings.py" "dist\config\"
if exist "README.md" copy "README.md" "dist\"

:: 创建使用说明
echo 汽车维修管理系统 - 使用说明 > "dist\使用说明.txt"
echo. >> "dist\使用说明.txt"
echo 1. 双击"汽车维修管理系统.exe"启动程序 >> "dist\使用说明.txt"
echo 2. 首次运行会自动创建数据库文件 >> "dist\使用说明.txt"
echo 3. 数据文件保存在data目录下 >> "dist\使用说明.txt"
echo 4. 报表文件保存在reports目录下 >> "dist\使用说明.txt"
echo 5. 备份文件保存在backups目录下 >> "dist\使用说明.txt"
echo. >> "dist\使用说明.txt"
echo 注意事项： >> "dist\使用说明.txt"
echo - 请确保有足够的磁盘空间 >> "dist\使用说明.txt"
echo - 建议定期备份data目录 >> "dist\使用说明.txt"
echo - 如遇问题，请检查是否有杀毒软件拦截 >> "dist\使用说明.txt"

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo 可执行文件位置: dist\汽车维修管理系统.exe
echo 完整程序包位置: dist 目录
echo.
echo 您可以将整个 dist 目录复制到其他电脑上使用
echo ========================================
echo.
pause