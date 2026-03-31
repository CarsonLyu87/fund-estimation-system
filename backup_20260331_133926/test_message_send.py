#!/usr/bin/env python3
"""
测试消息发送
"""

import subprocess
import time
from datetime import datetime

def test_cron_message():
    """测试Cron消息发送"""
    print(f"🕐 测试时间: {datetime.now().strftime('%H:%M:%S')}")
    print("正在测试消息发送...")
    
    # 方法1: 直接运行脚本
    print("\n1. 直接运行报告脚本:")
    result = subprocess.run(['python3', 'daily_fund_report.py'], 
                          capture_output=True, text=True)
    print(f"   退出码: {result.returncode}")
    print(f"   输出长度: {len(result.stdout)} 字符")
    
    # 方法2: 检查日志文件
    print("\n2. 检查日志文件:")
    import os
    if os.path.exists('fund_reports/'):
        files = os.listdir('fund_reports/')
        print(f"   日志文件数: {len(files)}")
        for f in files[-3:]:
            print(f"   - {f}")
    else:
        print("   日志目录不存在")
    
    # 方法3: 模拟Cron触发
    print("\n3. 模拟Cron触发:")
    cron_result = subprocess.run(['openclaw', 'cron', 'run', 'f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d'],
                               capture_output=True, text=True)
    print(f"   Cron触发结果: {cron_result.returncode}")
    
    return result.returncode == 0

def check_system_status():
    """检查系统状态"""
    print("\n🔧 系统状态检查:")
    
    # 检查OpenClaw状态
    print("1. OpenClaw状态:")
    status_result = subprocess.run(['openclaw', 'gateway', 'status'], 
                                 capture_output=True, text=True)
    if status_result.returncode == 0:
        print("   ✅ 网关运行正常")
    else:
        print(f"   ❌ 网关状态异常: {status_result.stderr[:100]}")
    
    # 检查Python环境
    print("\n2. Python环境:")
    py_result = subprocess.run(['python3', '--version'], 
                             capture_output=True, text=True)
    print(f"   {py_result.stdout.strip()}")
    
    # 检查文件权限
    print("\n3. 文件权限:")
    import os, stat
    script_stat = os.stat('daily_fund_report.py')
    print(f"   脚本权限: {oct(script_stat.st_mode)[-3:]}")
    print(f"   可执行: {'✅' if script_stat.st_mode & stat.S_IXUSR else '❌'}")

if __name__ == "__main__":
    print("=== 消息发送测试 ===\n")
    
    check_system_status()
    
    print("\n" + "="*50 + "\n")
    
    success = test_cron_message()
    
    print("\n" + "="*50)
    if success:
        print("✅ 测试完成 - 脚本运行正常")
        print("📨 消息应该在处理队列中")
    else:
        print("❌ 测试完成 - 发现问题")
    
    print(f"\n⏰ 下次测试: 11:10 (约5分钟后)")
    print("📋 已创建测试任务: test-1110")