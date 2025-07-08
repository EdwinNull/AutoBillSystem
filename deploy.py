#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的部署工作流程脚本
集成系统检查、打包、测试和发布功能
"""

import os
import sys
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

# 导入其他模块
try:
    from check_system import main as check_system
    from build_config import get_pyinstaller_args, create_version_file, create_spec_file
except ImportError:
    print("警告: 无法导入某些模块，将使用基本功能")
    check_system = None

class DeploymentManager:
    """部署管理器"""
    
    def __init__(self):
        self.project_root = Path('.')
        self.build_dir = self.project_root / 'build'
        self.dist_dir = self.project_root / 'dist'
        self.release_dir = self.project_root / 'releases'
        self.app_name = "汽车维修管理系统"
        self.version = "1.0.0"
        
    def print_header(self, title):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f" {title} ")
        print("=" * 60)
    
    def print_step(self, step, description):
        """打印步骤"""
        print(f"\n[步骤 {step}] {description}")
        print("-" * 40)
    
    def clean_build_directories(self):
        """清理构建目录"""
        self.print_step(1, "清理构建目录")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✅ 已清理: {dir_path}")
        
        # 清理spec文件
        spec_files = list(self.project_root.glob('*.spec'))
        for spec_file in spec_files:
            spec_file.unlink()
            print(f"✅ 已删除: {spec_file}")
        
        print("✅ 构建目录清理完成")
    
    def run_system_check(self):
        """运行系统检查"""
        self.print_step(2, "系统环境检查")
        
        if check_system:
            try:
                result = check_system()
                if not result:
                    print("❌ 系统检查未通过，请解决问题后重试")
                    return False
                print("✅ 系统检查通过")
                return True
            except Exception as e:
                print(f"⚠️  系统检查出错: {e}")
                return True  # 继续执行
        else:
            print("⚠️  跳过系统检查（模块未找到）")
            return True
    
    def install_dependencies(self):
        """安装依赖"""
        self.print_step(3, "安装打包依赖")
        
        try:
            # 检查PyInstaller
            import PyInstaller
            print(f"✅ PyInstaller已安装: {PyInstaller.__version__}")
        except ImportError:
            print("📦 正在安装PyInstaller...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller安装完成")
        
        return True
    
    def create_version_info(self):
        """创建版本信息"""
        self.print_step(4, "创建版本信息")
        
        try:
            version_file = create_version_file()
            print(f"✅ 版本信息文件已创建: {version_file}")
            return True
        except Exception as e:
            print(f"⚠️  创建版本信息失败: {e}")
            return True  # 不是致命错误
    
    def build_executable(self):
        """构建可执行文件"""
        self.print_step(5, "构建可执行文件")
        
        try:
            # 使用配置文件的参数
            args = get_pyinstaller_args()
            print(f"执行命令: {' '.join(args)}")
            
            # 执行打包
            result = subprocess.run(args, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 可执行文件构建成功")
                return True
            else:
                print(f"❌ 构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 构建过程出错: {e}")
            return False
    
    def copy_additional_files(self):
        """复制额外文件"""
        self.print_step(6, "复制必要文件")
        
        # 创建必要目录
        directories = ['data', 'config', 'reports', 'backups']
        for dir_name in directories:
            dir_path = self.dist_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"✅ 创建目录: {dir_name}")
        
        # 复制文件
        files_to_copy = [
            ('README.md', 'README.md'),
            ('部署指南.md', '部署指南.md'),
            ('config/settings.py', 'config/settings.py'),
        ]
        
        for src, dst in files_to_copy:
            src_path = self.project_root / src
            dst_path = self.dist_dir / dst
            
            if src_path.exists():
                # 确保目标目录存在
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                print(f"✅ 复制文件: {src} -> {dst}")
        
        # 创建使用说明
        self.create_user_manual()
        
        print("✅ 文件复制完成")
        return True
    
    def create_user_manual(self):
        """创建用户手册"""
        manual_content = f"""
{self.app_name} - 用户手册

版本: {self.version}
构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== 快速开始 ===

1. 启动程序
   双击 "{self.app_name}.exe" 启动程序

2. 首次使用
   - 程序会自动创建数据库文件
   - 建议先添加一些基础数据（客户、配件等）

3. 主要功能
   - 客户管理：添加、编辑、查询客户信息
   - 配件管理：管理配件库存和价格
   - 订单管理：创建维修订单，支持库存配件和客户自带配件
   - 进货管理：记录配件采购信息
   - 报表查询：查看各种统计报表

=== 目录结构 ===

{self.app_name}.exe    - 主程序文件
data/                  - 数据库文件目录
config/                - 配置文件目录
reports/               - 报表输出目录
backups/               - 数据备份目录

=== 注意事项 ===

1. 数据安全
   - 定期备份 data 目录
   - 避免直接删除数据库文件
   - 建议在重要操作前创建备份

2. 系统要求
   - Windows 7/8/10/11
   - 至少 100MB 可用磁盘空间
   - 建议分辨率 1024x768 或更高

3. 常见问题
   - 如果程序无法启动，请检查是否被杀毒软件拦截
   - 如果数据丢失，请从 backups 目录恢复
   - 如果界面显示异常，请检查系统DPI设置

=== 技术支持 ===

如需技术支持，请联系开发团队。

构建信息:
- Python版本: {sys.version}
- 构建平台: {sys.platform}
- 构建时间: {datetime.now().isoformat()}
"""
        
        manual_path = self.dist_dir / '用户手册.txt'
        with open(manual_path, 'w', encoding='utf-8') as f:
            f.write(manual_content)
        
        print(f"✅ 用户手册已创建: {manual_path}")
    
    def test_executable(self):
        """测试可执行文件"""
        self.print_step(7, "测试可执行文件")
        
        exe_path = self.dist_dir / f"{self.app_name}.exe"
        
        if not exe_path.exists():
            print(f"❌ 可执行文件不存在: {exe_path}")
            return False
        
        print(f"✅ 可执行文件存在: {exe_path}")
        print(f"文件大小: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # 可以添加更多测试，如启动测试等
        print("⚠️  建议手动测试程序功能")
        
        return True
    
    def create_release_package(self):
        """创建发布包"""
        self.print_step(8, "创建发布包")
        
        # 创建releases目录
        self.release_dir.mkdir(exist_ok=True)
        
        # 创建发布包文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        release_name = f"{self.app_name}_v{self.version}_{timestamp}"
        zip_path = self.release_dir / f"{release_name}.zip"
        
        # 创建ZIP文件
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.dist_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.dist_dir)
                    zipf.write(file_path, arc_path)
        
        print(f"✅ 发布包已创建: {zip_path}")
        print(f"包大小: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        return True
    
    def generate_deployment_report(self):
        """生成部署报告"""
        self.print_step(9, "生成部署报告")
        
        report_content = f"""
{self.app_name} - 部署报告

构建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
版本: {self.version}

=== 构建环境 ===
Python版本: {sys.version}
操作系统: {sys.platform}
工作目录: {os.getcwd()}

=== 文件清单 ===
"""
        
        # 添加文件清单
        if self.dist_dir.exists():
            for root, dirs, files in os.walk(self.dist_dir):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.dist_dir)
                    size = file_path.stat().st_size
                    report_content += f"{rel_path} ({size} bytes)\n"
        
        report_content += f"""

=== 部署说明 ===
1. 将整个dist目录复制到目标计算机
2. 双击{self.app_name}.exe启动程序
3. 首次运行会自动创建必要的数据文件

=== 系统要求 ===
- Windows 7/8/10/11
- 至少100MB可用磁盘空间
- 无需安装Python或其他依赖

报告生成时间: {datetime.now().isoformat()}
"""
        
        report_path = self.release_dir / f"部署报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ 部署报告已生成: {report_path}")
        return True
    
    def deploy(self):
        """执行完整部署流程"""
        self.print_header(f"{self.app_name} - 自动化部署")
        
        steps = [
            self.clean_build_directories,
            self.run_system_check,
            self.install_dependencies,
            self.create_version_info,
            self.build_executable,
            self.copy_additional_files,
            self.test_executable,
            self.create_release_package,
            self.generate_deployment_report
        ]
        
        for i, step in enumerate(steps, 1):
            try:
                if not step():
                    print(f"\n❌ 步骤 {i} 失败，部署中止")
                    return False
            except Exception as e:
                print(f"\n❌ 步骤 {i} 出错: {e}")
                return False
        
        self.print_header("部署完成")
        print("🎉 恭喜！应用程序已成功打包")
        print(f"\n📁 可执行文件位置: {self.dist_dir}")
        print(f"📦 发布包位置: {self.release_dir}")
        print("\n下一步:")
        print("1. 测试dist目录中的程序")
        print("2. 将发布包分发给用户")
        print("3. 提供技术支持文档")
        
        return True

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("""
汽车维修管理系统 - 部署工具

用法:
  python deploy.py          # 执行完整部署流程
  python deploy.py --help   # 显示帮助信息

功能:
  - 自动检查系统环境
  - 安装必要的依赖
  - 构建可执行文件
  - 创建发布包
  - 生成部署报告

输出:
  - dist/: 可执行程序目录
  - releases/: 发布包目录
        """)
        return
    
    # 检查是否在项目根目录
    if not Path('main.py').exists():
        print("❌ 错误: 请在项目根目录下运行此脚本")
        sys.exit(1)
    
    # 执行部署
    deployer = DeploymentManager()
    success = deployer.deploy()
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()