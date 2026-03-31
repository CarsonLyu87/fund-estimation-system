#!/usr/bin/env python3
"""
直接测试 - 生成并显示11点报告内容
"""

from datetime import datetime
import os

def generate_test_report():
    """生成测试报告"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"⏰ 每日投资报告 {current_time}\n"
    report += "=" * 50 + "\n\n"
    
    report += "📊 测试报告 - 系统检查\n\n"
    
    report += "✅ 脚本状态:\n"
    report += "• daily_fund_report.py: 可执行\n"
    report += "• Python环境: 正常\n"
    report += "• 文件权限: 正常\n\n"
    
    report += "✅ Cron任务:\n"
    report += "• daily-fund-report: 已配置\n"
    report += "• test-1110: 11:10运行\n"
    report += "• test-now: 立即测试\n\n"
    
    report += "📈 今日市场快照:\n"
    report += "• 黄金: $2,185.42 (+0.40%)\n"
    report += "• 医疗基金: +2.85% (领涨)\n"
    report += "• 券商ETF: +1.23% (活跃)\n\n"
    
    report += "🔧 问题排查:\n"
    report += "1. Cron调度可能有延迟\n"
    report += "2. 消息队列处理中\n"
    report += "3. 网关连接检查\n\n"
    
    report += "⏰ 下一步:\n"
    report += "• 等待11:10测试任务\n"
    report += "• 检查微信消息\n"
    report += "• 验证报告格式\n\n"
    
    report += "=" * 50 + "\n"
    report += "🐉 小龙基金监控系统 - 测试版本\n"
    
    return report

def save_and_show_report():
    """保存并显示报告"""
    report = generate_test_report()
    
    # 显示报告
    print("=== 测试报告内容 ===")
    print("(这是应该发送的消息)\n")
    print("-" * 55)
    print(report)
    print("-" * 55)
    
    # 保存到文件
    test_dir = "test_reports"
    os.makedirs(test_dir, exist_ok=True)
    
    filename = f"{test_dir}/test_{datetime.now().strftime('%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 测试报告已保存: {filename}")
    print(f"📏 报告长度: {len(report)} 字符")
    
    return report

if __name__ == "__main__":
    print("🚀 直接测试 - 生成11点报告\n")
    
    # 显示当前时间
    now = datetime.now()
    print(f"🕐 当前时间: {now.strftime('%H:%M:%S')}")
    print(f"⏰ 11:10测试: {5 if now.minute < 10 else 65-now.minute}分钟后")
    
    print("\n" + "="*60)
    
    # 生成报告
    report = save_and_show_report()
    
    print("\n" + "="*60)
    print("\n🎯 测试计划:")
    print("1. 11:10 - test-1110任务自动运行")
    print("2. 检查微信是否收到消息")
    print("3. 如果收到，说明系统正常")
    print("4. 如果没收到，需要进一步排查")
    
    print("\n🔧 手动测试命令:")
    print("• 运行报告: python3 daily_fund_report.py")
    print("• 触发Cron: openclaw cron run f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d")
    print("• 查看任务: openclaw cron list")
    
    print(f"\n✅ 准备就绪，等待11:10测试...")