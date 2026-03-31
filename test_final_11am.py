#!/usr/bin/env python3
"""
最终11点提醒测试
展示实际会收到的消息
"""

from datetime import datetime

def test_final_11am_message():
    """生成最终11点消息"""
    current_time = datetime.now().strftime('%H:%M:%S')
    
    message = f"⏰ 每日基金播报 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += "=" * 50 + "\n\n"
    
    # 个人基金部分
    message += "👤 个人基金 (7只):\n"
    message += "📈 上涨: 2只 | 📉 下跌: 5只\n\n"
    
    personal_funds = [
        "📈 中欧医疗创新股票A: +2.85%",
        "📈 华夏成长混合: +0.30%", 
        "📉 易方达消费行业: -0.19%",
        "📉 招商中证白酒指数: -0.24%",
        "📉 易方达蓝筹精选混合: -0.11%",
        "📉 广发全球精选股票(QDII): -0.58%",
        "📉 南方纳斯达克100指数: -1.43%"
    ]
    
    for fund in personal_funds:
        message += f"  {fund}\n"
    
    message += "\n" + "-" * 40 + "\n\n"
    
    # 活跃基金部分
    message += "🔥 市场最活跃基金TOP 5:\n\n"
    
    active_funds = [
        ("📈 华宝券商ETF (512000)", "成交额: 5.2亿 | 涨跌: +1.23%", "政策利好预期"),
        ("📈 国泰券商ETF (512880)", "成交额: 4.8亿 | 涨跌: +1.15%", "成交量最大"),
        ("📉 创业板ETF (159915)", "成交额: 3.5亿 | 涨跌: -0.45%", "科技股波动"),
        ("📈 沪深300ETF (510300)", "成交额: 3.2亿 | 涨跌: +0.32%", "大盘核心"),
        ("📉 酒ETF (512690)", "成交额: 2.8亿 | 涨跌: -0.78%", "板块调整")
    ]
    
    for i, (name, stats, reason) in enumerate(active_funds, 1):
        message += f"{i}. {name}\n"
        message += f"   {stats}\n"
        message += f"   原因: {reason}\n"
        if i < 5:
            message += "\n"
    
    message += "\n" + "=" * 50 + "\n"
    message += "📝 详细数据已保存到日志文件\n"
    message += "⏳ 下次报告: 明日 11:00"
    
    return message

if __name__ == "__main__":
    print("=== 最终11点提醒测试 ===\n")
    print("当cron任务在11点触发时，你会收到以下格式的消息：\n")
    print("-" * 60)
    final_message = test_final_11am_message()
    print(final_message)
    print("-" * 60)
    
    print(f"\n✅ 测试完成！")
    print(f"实际11点运行时会获取实时数据")
    print(f"包含: 7只个人基金 + 5只市场活跃基金")
    print(f"下次自动运行: 今天 11:00 (约55分钟后)")