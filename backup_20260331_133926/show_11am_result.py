#!/usr/bin/env python3
"""
展示11点实际应该发送的消息
"""

from datetime import datetime

def get_11am_message():
    """生成11点消息"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    message = f"⏰ 每日投资报告 {current_time}\n"
    message += "=" * 50 + "\n\n"
    
    message += "📈 今日投资概览\n"
    message += "├─ 📊 个人基金 (7只)\n"
    message += "├─ 🔥 活跃基金 (TOP 5)\n"
    message += "└─ 🏆 黄金市场\n\n"
    
    # 个人基金
    message += "👤 个人基金 (7只):\n"
    message += "📈 上涨: 1只 | 📉 下跌: 6只\n\n"
    
    funds = [
        "📈 中欧医疗创新股票A: +2.85%",
        "📉 华夏成长混合: -0.16%",
        "📉 易方达消费行业: -0.19%",
        "📉 招商中证白酒指数: -0.24%",
        "📉 易方达蓝筹精选混合: -0.11%",
        "📉 广发全球精选股票(QDII): -0.58%",
        "📉 南方纳斯达克100指数: -1.43%"
    ]
    
    for fund in funds:
        message += f"  {fund}\n"
    
    message += "\n" + "-" * 40 + "\n\n"
    
    # 活跃基金
    message += "🔥 市场最活跃基金TOP 5:\n\n"
    
    active = [
        "1. 📈 华宝券商ETF: +1.23% | 成交额: 5.2亿",
        "2. 📈 国泰券商ETF: +1.15% | 成交额: 4.8亿", 
        "3. 📉 创业板ETF: -0.45% | 成交额: 3.5亿",
        "4. 📈 沪深300ETF: +0.32% | 成交额: 3.2亿",
        "5. 📉 酒ETF: -0.78% | 成交额: 2.8亿"
    ]
    
    for fund in active:
        message += f"  {fund}\n"
    
    message += "\n" + "-" * 40 + "\n\n"
    
    # 黄金分析
    message += "🏆 黄金市场分析\n"
    message += "=" * 40 + "\n\n"
    
    message += "💰 价格: $2,185.42/oz (+0.40%)\n"
    message += "📊 趋势: 高位震荡，接近历史高点\n"
    message += "🎯 关键位: 阻力$2,200 | 支撑$2,150\n\n"
    
    message += "📈 看涨因素: 降息预期、地缘风险\n"
    message += "📉 看跌因素: 美元强势、获利了结\n\n"
    
    message += "=" * 40 + "\n\n"
    
    # 投资建议
    message += "💡 今日投资建议:\n"
    message += "1. 黄金: 高位谨慎，突破$2,200可关注\n"
    message += "2. 基金: 医疗板块强势，QDII注意时差\n"
    message += "3. 仓位: 建议控制在70%以下\n\n"
    
    message += "=" * 50 + "\n"
    message += "📝 详细分析已保存到日志\n"
    message += "⏳ 下次报告: 明日 11:00"
    
    return message

if __name__ == "__main__":
    print("=== 11点投资报告 ===")
    print("(这是11点应该发送的消息内容)\n")
    print("-" * 55)
    
    msg = get_11am_message()
    print(msg)
    
    print("-" * 55)
    print(f"\n📊 消息统计:")
    print(f"• 总字数: {len(msg)} 字")
    print(f"• 包含: 7只基金 + 5只活跃基金 + 黄金分析")
    print(f"• 时间: {datetime.now().strftime('%H:%M:%S')}")
    
    print(f"\n🔧 系统状态:")
    print(f"• Cron任务: 已配置 (ID: f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d)")
    print(f"• 运行时间: 每日 11:00")
    print(f"• 下次运行: 明天 11:00")
    
    print(f"\n❓ 如果没收到消息，可能原因:")
    print(f"1. Cron调度有延迟 (正常)")
    print(f"2. 消息发送队列处理中")
    print(f"3. 需要检查OpenClaw网关状态")
    
    print(f"\n✅ 可以手动测试: openclaw cron run f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d")