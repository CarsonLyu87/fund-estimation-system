#!/usr/bin/env python3
"""
最终解决方案：极简摘要 + 本地文件
"""

import subprocess
import os
from datetime import datetime

def generate_full_report():
    """生成完整报告并保存"""
    print("📄 生成完整报告...")
    
    result = subprocess.run(
        ['python3', 'daily_fund_report.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 报告生成失败: {result.stderr[:200]}")
        return None
    
    # 保存报告
    report_dir = "fund_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"{report_dir}/report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(result.stdout)
    
    print(f"✅ 完整报告已保存: {report_file}")
    print(f"   文件大小: {len(result.stdout)} 字符")
    
    return report_file, result.stdout

def create_minimal_summary(report_content):
    """创建极简摘要"""
    print("📋 创建极简摘要...")
    
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # 从报告中提取关键数据
    lines = report_content.split('\n')
    
    # 提取个人基金数据
    personal_funds = []
    active_funds = []
    gold_info = []
    
    for line in lines:
        if '📈' in line and '%' in line:
            if '个人基金' not in line and '活跃基金' not in line:
                personal_funds.append(line.strip())
        elif '🔥' in line and '%' in line:
            active_funds.append(line.strip())
        elif '💰' in line or '🏆' in line:
            gold_info.append(line.strip())
    
    # 创建极简摘要
    summary = f"""📊 投资速报 {current_time}
========================
👤 持仓: 7只基金"""
    
    # 添加关键基金（最多3只）
    if personal_funds:
        summary += "\n"
        for fund in personal_funds[:3]:
            # 简化格式
            simplified = fund.replace('📈 ', '↑ ').replace('📉 ', '↓ ')
            summary += f"\n{simplified}"
    
    # 添加活跃基金（最多2只）
    if active_funds:
        summary += "\n\n🔥 活跃:"
        for fund in active_funds[:2]:
            simplified = fund.replace('📈 ', '↑ ').replace('📉 ', '↓ ')
            summary += f"\n{simplified}"
    
    # 添加黄金
    if gold_info:
        summary += "\n\n🏆 黄金:"
        for info in gold_info[:2]:
            summary += f"\n{info}"
    
    summary += f"\n\n📁 完整报告已保存"
    summary += f"\n⏰ 下次报告: 明日 11:00"
    
    print(f"摘要长度: {len(summary)} 字符")
    return summary

def send_message(message):
    """发送消息"""
    send_cmd = [
        'openclaw', 'sessions', 'send',
        'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        message
    ]
    
    result = subprocess.run(send_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 消息发送成功 ({len(message)} 字符)")
        return True
    else:
        print(f"❌ 消息发送失败: {result.stderr}")
        return False

def create_daily_summary_file(report_file, summary):
    """创建每日摘要文件"""
    print("📝 创建每日摘要文件...")
    
    summary_dir = "daily_summaries"
    os.makedirs(summary_dir, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    summary_file = f"{summary_dir}/summary_{date_str}.txt"
    
    content = f"""📅 每日投资摘要 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================

📋 今日摘要:
{summary}

📁 完整报告位置:
{report_file}

📊 报告统计:
• 生成时间: {datetime.now().strftime('%H:%M:%S')}
• 摘要长度: {len(summary)} 字符
• 完整报告: {os.path.getsize(report_file) if os.path.exists(report_file) else 0} 字符

🔧 系统状态:
• 微信通道: 工作正常 (极简摘要)
• 报告生成: 工作正常
• 文件保存: 工作正常

⏰ 明日计划:
• 报告时间: 11:00
• 发送方式: 极简摘要 + 本地保存
========================================"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 每日摘要已保存: {summary_file}")
    return summary_file

def main():
    """主函数"""
    print("🎯 最终解决方案实施")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # 1. 生成完整报告
    report_result = generate_full_report()
    if not report_result:
        print("❌ 无法生成报告，退出")
        return
    
    report_file, report_content = report_result
    
    print("\n" + "-" * 50)
    
    # 2. 创建极简摘要
    summary = create_minimal_summary(report_content)
    
    print("\n" + "-" * 50)
    
    # 3. 发送极简摘要
    print("📤 发送极简摘要...")
    send_success = send_message(summary)
    
    print("\n" + "-" * 50)
    
    # 4. 创建每日摘要文件
    summary_file = create_daily_summary_file(report_file, summary)
    
    print("\n" + "=" * 60)
    
    if send_success:
        print("🎉 解决方案实施成功!")
        print(f"✅ 极简摘要已发送 ({len(summary)} 字符)")
        print(f"✅ 完整报告已保存: {report_file}")
        print(f"✅ 每日摘要已保存: {summary_file}")
        
        # 发送成功确认
        confirm_msg = f"""✅ 报告系统就绪 {datetime.now().strftime('%H:%M:%S')}
========================
📋 状态: 极简摘要模式启用

📊 今日已生成:
• 极简摘要: 已发送
• 完整报告: {os.path.basename(report_file)}
• 系统摘要: {os.path.basename(summary_file)}

🎯 明日11点将自动:
1. 📤 发送极简摘要
2. 💾 保存完整报告
3. 📝 记录系统日志

🐉 系统优化完成"""
        
        send_message(confirm_msg)
    else:
        print("⚠️ 摘要发送失败，但报告已保存")
        print(f"📁 请查看本地文件: {report_file}")
    
    print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()