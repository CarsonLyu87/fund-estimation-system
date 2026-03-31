#!/usr/bin/env python3
import subprocess
from datetime import datetime

# 运行报告脚本
print("生成报告...")
report_result = subprocess.run(['python3', 'daily_fund_report.py'], 
                             capture_output=True, text=True)

if report_result.returncode == 0:
    # 提取报告内容（简化版）
    report_content = f"⏰ 每日投资报告 {datetime.now().strftime('%H:%M:%S')}\n"
    report_content += "="*40 + "\n"
    report_content += "📊 报告生成成功！\n"
    report_content += "详细内容已保存到日志文件。\n"
    
    # 发送消息
    send_cmd = [
        'openclaw', 'sessions', 'send',
        '--session', 'o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        report_content
    ]
    
    send_result = subprocess.run(send_cmd, capture_output=True, text=True)
    print(f"消息发送结果: {send_result.returncode}")
else:
    print(f"报告生成失败: {report_result.stderr}")
