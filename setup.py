#!/usr/bin/env python3
"""
基金估算系统安装脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ 找不到依赖文件: {requirements_file}")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def create_directories():
    """创建必要的目录"""
    directories = [
        "reports",
        "logs",
        "cache",
        "data",
        "config"
    ]
    
    print("📁 创建目录结构...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ 创建: {directory}/")
    
    return True

def copy_config_files():
    """复制配置文件"""
    print("⚙️  设置配置文件...")
    
    # 检查配置文件是否存在
    config_files = ["config/funds.json"]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"   ✅ 配置文件已存在: {config_file}")
        else:
            print(f"   ⚠️  配置文件不存在: {config_file}")
            # 可以在这里创建默认配置文件
    
    return True

def setup_environment():
    """设置环境变量"""
    print("🌍 设置环境变量...")
    
    env_example = """# 基金估算系统环境变量
# 数据源API密钥（如果需要）
TIANTIAN_API_KEY=your_tiantian_api_key
EASTMONEY_API_KEY=your_eastmoney_api_key

# 邮件通知设置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_password

# 缓存设置
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL=300

# 日志设置
LOG_LEVEL=INFO
LOG_FILE=logs/fund_estimation.log
"""
    
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_example)
        print(f"   ✅ 创建环境变量文件: {env_file}")
        print("   ⚠️  请编辑 .env 文件设置您的配置")
    else:
        print(f"   ✅ 环境变量文件已存在: {env_file}")
    
    return True

def create_startup_scripts():
    """创建启动脚本"""
    print("🚀 创建启动脚本...")
    
    scripts = {
        "start.sh": """#!/bin/bash
# 启动基金估算系统

echo "🚀 启动基金估算系统..."

# 激活虚拟环境（如果有）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行估算
python scripts/run_estimation.py

echo "✅ 估算完成!"
""",
        
        "daily_report.sh": """#!/bin/bash
# 每日自动报告脚本

echo "📅 生成每日基金报告..."

# 激活虚拟环境（如果有）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行估算并保存报告
timestamp=$(date +"%Y%m%d_%H%M%S")
python scripts/run_estimation.py > "reports/daily_${timestamp}.log" 2>&1

echo "✅ 每日报告生成完成!"
""",
        
        "setup_cron.sh": """#!/bin/bash
# 设置定时任务

echo "⏰ 设置定时任务..."

# 添加每日9:30和14:30的估算任务
(crontab -l 2>/dev/null; echo "30 9,14 * * * cd $(pwd) && ./daily_report.sh") | crontab -

# 添加每周一9:00的周报任务
(crontab -l 2>/dev/null; echo "0 9 * * 1 cd $(pwd) && python scripts/weekly_report.py") | crontab -

echo "✅ 定时任务设置完成!"
echo "当前crontab:"
crontab -l
"""
    }
    
    for script_name, script_content in scripts.items():
        script_path = Path(script_name)
        if not script_path.exists():
            script_path.write_text(script_content, encoding="utf-8")
            script_path.chmod(0o755)  # 添加执行权限
            print(f"   ✅ 创建: {script_name}")
        else:
            print(f"   ✅ 已存在: {script_name}")
    
    return True

def test_installation():
    """测试安装"""
    print("🧪 测试安装...")
    
    try:
        # 测试Python导入
        import sys
        sys.path.insert(0, "src")
        
        import estimator
        print("   ✅ estimator模块导入成功")
        
        # 测试配置加载
        import json
        with open("config/funds.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            print(f"   ✅ 配置文件加载成功: {len(config.get('funds', []))} 只基金")
        
        print("✅ 安装测试通过!")
        return True
        
    except Exception as e:
        print(f"❌ 安装测试失败: {e}")
        return False

def main():
    """主安装函数"""
    print("="*60)
    print("基金估算系统安装程序")
    print("="*60)
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"安装目录: {current_dir}")
    print()
    
    # 执行安装步骤
    steps = [
        ("检查Python版本", check_python_version),
        ("创建目录结构", create_directories),
        ("安装依赖包", install_dependencies),
        ("设置配置文件", copy_config_files),
        ("设置环境变量", setup_environment),
        ("创建启动脚本", create_startup_scripts),
        ("测试安装", test_installation)
    ]
    
    success = True
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            if not step_func():
                success = False
                print(f"❌ {step_name}失败")
                break
        except Exception as e:
            print(f"❌ {step_name}出错: {e}")
            success = False
            break
    
    print("\n" + "="*60)
    if success:
        print("🎉 基金估算系统安装完成!")
        print()
        print("📋 下一步:")
        print("   1. 编辑 .env 文件设置您的配置")
        print("   2. 运行 ./start.sh 测试系统")
        print("   3. 运行 ./setup_cron.sh 设置定时任务")
        print("   4. 查看 reports/ 目录获取估算结果")
    else:
        print("❌ 安装失败，请检查错误信息")
    
    print("="*60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())