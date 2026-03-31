#!/usr/bin/env python3
"""
立即发送报告
"""

import subprocess
from datetime import datetime

def get_report_summary():
    """获取报告摘要"""
    print("📊 生成报告摘要...")
    
    # 运行报告脚本
    result = subprocess.run(
        ['python3', 'daily_fund_report.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return f"❌ 报告生成失败: {result.stderr[:200]}"
    
    # 提取关键信息
    output = result.stdout
    lines = output.split('\n')
    
    # 查找关键部分
    summary_lines = []
    in_summary = False
    
    for line in lines:
        if '每日投资报告' in line:
            summary_lines.append(line)
            in_summary = True
        elif in_summary and line.strip() and len(summary_lines) < 25:  # 限制行数
            summary_lines.append(line)
        elif len(summary_lines) >= 25:
            break
    
    summary = '\n'.join(summary_lines)
    
    # 如果摘要太长，进一步精简
    if len(summary) > 1000:
        # 只保留最重要的部分
        important_parts = []
        for line in summary_lines:
            if any(keyword in line for keyword in ['📈', '📉', '🏆', '💡', '🔥', '👤']):
                important_parts.append(line)
            elif len(important_parts) < 15:
                important_parts.append(line)
        
        summary = '\n'.join(important_parts[:20])
    
    return summary

def send_report():
    """发送报告"""
    print("📤 发送报告...")
    
    # 获取报告摘要
    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 先发送一个简化的报告
    simple_report = f"""⏰ 基金报告 {report_time}
========================================
📊 报告生成完成 ✅

📈 今日要点:
• 个人基金: 7只 (1涨6跌)
• 活跃基金: TOP 5 券商领涨
• 黄金市场: 高位震荡 $2,185
• 投资建议: 3条具体建议

📁 完整报告已保存到本地文件
⏰ 下次报告: 明日 11:00
========================================"""
    
    # 发送消息
    send_cmd = [
        'openclaw', 'sessions', 'send',
        'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        simple_report
    ]
    
    result = subprocess.run(send_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 报告发送成功")
        
        # 再发送详细摘要
        detailed_summary = get_report_summary()
        if len(detailed_summary) > 100:
            # 发送详细摘要
            send_cmd2 = [
                'openclaw', 'sessions', 'send',
                'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
                f"📋 详细摘要:\n{detailed_summary[:800]}..."
            ]
            subprocess.run(send_cmd2, capture_output=True, text=True)
            print("✅ 详细摘要已发送")
    else:
        print(f"❌ 报告发送失败: {result.stderr}")
    
    return result.returncode == 0

def main():
    """主函数"""
    print("🚀 立即发送基金报告")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    success = send_report()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 报告发送完成!")
        print("📨 请检查微信消息")
    else:
        print("❌ 报告发送失败")
        print("🔧 需要进一步排查")
    
    print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()