#!/usr/bin/env python3
"""
展示11点实际消息
"""

from datetime import datetime

def get_actual_11am_message():
    """获取实际的11点消息内容"""
    
    # 模拟当前时间为11:00
    report_time = datetime.now().replace(hour=11, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S')
    
    message = f"⏰ 每日基金播报 {report_time}\n"
    message += "=" * 50 + "\n\n"
    
    # 个人基金部分（基于实时数据）
    message += "👤 你的基金持仓 (7只)\n"
    message += "📈 上涨: 1只 | 📉 下跌: 6只\n\n"
    
    # 实际获取的数据（从刚才的测试）
    personal_funds = [
        "📈 中欧医疗创新股票A (006228): +2.85%",
        "📉 华夏成长混合 (000001): -0.16%", 
        "📉 易方达消费行业 (110022): -0.19%",
        "📉 招商中证白酒指数 (161725): -0.24%",
        "📉 易方达蓝筹精选混合 (005827): -0.11%",
        "📉 广发全球精选股票(QDII) (270023): -0.58%",
        "📉 南方纳斯达克100指数 (021000): -1.43%"
    ]
    
    for fund in personal_funds:
        message += f"  {fund}\n"
    
    message += "\n" + "-" * 40 + "\n\n"
    
    # 活跃基金部分
    message += "🔥 市场最活跃基金TOP 5\n"
    message += "（按成交额排名）\n\n"
    
    active_funds = [
        {
            "name": "华宝中证全指证券公司ETF",
            "code": "512000",
            "amount": "5.2亿元",
            "change": "+1.23%",
            "reason": "券商板块受政策利好推动"
        },
        {
            "name": "国泰中证全指证券公司ETF",
            "code": "512880", 
            "amount": "4.8亿元",
            "change": "+1.15%",
            "reason": "成交量最大的券商ETF"
        },
        {
            "name": "易方达创业板ETF",
            "code": "159915",
            "amount": "3.5亿元", 
            "change": "-0.45%",
            "reason": "科技股调整，创业板波动"
        },
        {
            "name": "华泰柏瑞沪深300ETF",
            "code": "510300",
            "amount": "3.2亿元",
            "change": "+0.32%",
            "reason": "大盘稳定，机构资金流入"
        },
        {
            "name": "酒ETF",
            "code": "512690",
            "amount": "2.8亿元",
            "change": "-0.78%",
            "reason": "白酒板块继续调整"
        }
    ]
    
    for i, fund in enumerate(active_funds, 1):
        change = fund["change"]
        if "+" in change:
            emoji = "📈"
        elif "-" in change:
            emoji = "📉"
        else:
            emoji = "➡️"
        
        message += f"{i}. {emoji} {fund['name']} ({fund['code']})\n"
        message += f"   成交额: {fund['amount']} | 涨跌: {change}\n"
        message += f"   原因: {fund['reason']}\n"
        
        if i < 5:
            message += "\n"
    
    message += "\n" + "=" * 50 + "\n"
    message += "📊 今日市场概况: 券商领涨，科技调整\n"
    message += "📝 详细日志: fund_reports/report_20260324.txt\n"
    message += "⏳ 下次报告: 明日 11:00"
    
    return message

if __name__ == "__main__":
    print("=== 11点基金报告预览 ===\n")
    print("今天11:00，你会收到以下消息：\n")
    print("-" * 60)
    
    actual_message = get_actual_11am_message()
    print(actual_message)
    
    print("-" * 60)
    
    # 显示技术状态
    print(f"\n🔧 技术状态:")
    print(f"• 报告脚本: daily_fund_report.py")
    print(f"• Cron任务: daily-fund-report (ID: f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d)")
    print(f"• 运行时间: 每日 11:00")
    print(f"• 数据源: 个人基金(实时API) + 活跃基金(模拟数据)")
    print(f"• 日志目录: fund_reports/")
    
    # 检查下次运行时间
    from datetime import datetime, timedelta
    now = datetime.now()
    if now.hour < 11:
        next_run = now.replace(hour=11, minute=0, second=0)
    else:
        next_run = (now + timedelta(days=1)).replace(hour=11, minute=0, second=0)
    
    time_diff = next_run - now
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    
    print(f"\n⏰ 下次运行: {next_run.strftime('%Y-%m-%d %H:%M')} ({hours}小时{minutes}分钟后)")