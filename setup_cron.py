#!/usr/bin/env python3
"""
设置基金报告cron任务
"""

import os
import subprocess
import sys

def setup_cron():
    """设置cron任务"""
    
    cron_job = "0 11 * * * cd /Users/carson/.openclaw/workspace && /usr/bin/python3 daily_fund_summary.py"
    
    print("📅 正在设置每日基金报告定时任务...")
    
    try:
        # 使用subprocess设置cron
        result = subprocess.run(
            ['crontab', '-l'],
            capture_output=True,
            text=True
        )
        
        current_cron = result.stdout if result.returncode == 0 else ""
        
        # 检查是否已存在相同任务
        if cron_job in current_cron:
            print("✅ 定时任务已存在")
        else:
            # 添加新任务
            new_cron = current_cron.strip() + "\n" + cron_job + "\n"
            
            # 写入crontab
            process = subprocess.Popen(
                ['crontab', '-'],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(input=new_cron)
            
            print("✅ 定时任务已设置")
        
        # 验证设置
        result = subprocess.run(
            ['crontab', '-l'],
            capture_output=True,
            text=True
        )
        
        print("\n📋 当前cron任务:")
        print(result.stdout)
        
        print("🎯 任务将在每天11:00执行")
        print("📁 报告将保存在: /Users/carson/.openclaw/workspace/fund_reports/")
        print("📝 日志将保存在: /Users/carson/.openclaw/workspace/fund_logs/")
        
        return True
        
    except Exception as e:
        print(f"❌ 设置失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_cron()
    sys.exit(0 if success else 1)