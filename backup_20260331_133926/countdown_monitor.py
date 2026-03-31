#!/usr/bin/env python3
"""
1分钟倒计时监控
"""

import time
from datetime import datetime, timedelta
import subprocess

def countdown_timer(seconds):
    """倒计时显示"""
    print(f"⏰ 开始 {seconds} 秒倒计时...")
    print("=" * 40)
    
    for i in range(seconds, 0, -1):
        mins, secs = divmod(i, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        print(f"\r🕐 剩余时间: {time_str}", end="", flush=True)
        time.sleep(1)
    
    print(f"\r✅ 时间到! {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 40)

def check_cron_tasks():
    """检查Cron任务"""
    print("\n📋 检查Cron任务状态:")
    print("-" * 40)
    
    result = subprocess.run(['openclaw', 'cron', 'list'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("当前Cron任务:")
        print(result.stdout)
        
        # 查找测试任务
        if 'test-1min-later' in result.stdout:
            print("✅ 找到测试任务: test-1min-later")
        else:
            print("❌ 未找到测试任务")
    else:
        print(f"❌ 无法获取Cron列表: {result.stderr}")
    
    return result.returncode == 0

def monitor_task_execution():
    """监控任务执行"""
    print("\n🔍 监控任务执行状态:")
    print("-" * 40)
    
    # 记录开始时间
    start_time = datetime.now()
    print(f"监控开始: {start_time.strftime('%H:%M:%S')}")
    
    # 等待任务执行（最多2分钟）
    max_wait = 120  # 2分钟
    check_interval = 5  # 每5秒检查一次
    
    print("等待任务执行...")
    
    for i in range(0, max_wait, check_interval):
        elapsed = i
        mins, secs = divmod(elapsed, 60)
        print(f"\r⏳ 已等待: {mins:02d}:{secs:02d}", end="", flush=True)
        
        # 检查是否有新消息（通过检查报告文件时间）
        import os
        report_dir = "fund_reports"
        if os.path.exists(report_dir):
            files = os.listdir(report_dir)
            if files:
                latest_file = max([os.path.join(report_dir, f) for f in files], 
                                key=os.path.getmtime)
                file_time = datetime.fromtimestamp(os.path.getmtime(latest_file))
                
                if file_time > start_time:
                    print(f"\n✅ 检测到新报告生成: {latest_file}")
                    print(f"   时间: {file_time.strftime('%H:%M:%S')}")
                    return True
        
        time.sleep(check_interval)
    
    print(f"\n⏰ 等待超时 ({max_wait}秒)")
    return False

def run_manual_test():
    """运行手动测试"""
    print("\n🚀 运行手动测试作为备份:")
    print("-" * 40)
    
    print("1. 运行发送脚本...")
    result = subprocess.run(['python3', 'send_fund_report.py'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 手动测试成功")
        print(f"输出: {result.stdout[:200]}...")
    else:
        print(f"❌ 手动测试失败: {result.stderr}")
    
    return result.returncode == 0

def main():
    """主函数"""
    print("🔧 1分钟后任务触发测试")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 显示当前时间
    now = datetime.now()
    target_time = now + timedelta(minutes=1)
    print(f"🕐 当前时间: {now.strftime('%H:%M:%S')}")
    print(f"🎯 目标时间: {target_time.strftime('%H:%M:%S')}")
    print(f"⏳ 等待时间: 1分钟")
    
    # 检查Cron任务
    check_cron_tasks()
    
    print("\n" + "=" * 60)
    
    # 1分钟倒计时
    countdown_timer(60)
    
    print("\n" + "=" * 60)
    
    # 监控任务执行
    print("\n📊 测试结果:")
    print("-" * 40)
    
    auto_success = monitor_task_execution()
    
    if auto_success:
        print("\n🎉 自动触发测试成功!")
        print("✅ Cron任务按计划执行")
        print("✅ 报告生成正常")
        print("✅ 消息应该已发送")
    else:
        print("\n⚠️ 自动触发可能未执行")
        print("🔧 启动手动测试作为备份...")
        
        manual_success = run_manual_test()
        
        if manual_success:
            print("\n✅ 手动测试成功完成")
            print("📨 消息应该已通过手动测试发送")
        else:
            print("\n❌ 手动测试也失败")
            print("🔍 需要进一步排查问题")
    
    print("\n" + "=" * 60)
    print("📋 测试总结:")
    print(f"• 测试时间: {now.strftime('%H:%M:%S')} → {datetime.now().strftime('%H:%M:%S')}")
    print(f"• 自动触发: {'✅ 成功' if auto_success else '❌ 失败或未检测到'}")
    print(f"• 手动备份: {'✅ 已执行' if not auto_success else '⏭️ 跳过'}")
    print(f"• 系统状态: {'🟢 正常' if auto_success or manual_success else '🔴 异常'}")
    
    print(f"\n🐉 请检查微信是否收到测试消息")

if __name__ == "__main__":
    main()