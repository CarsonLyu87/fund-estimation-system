#!/usr/bin/env python3
"""
模拟11点基金通知
展示实际cron触发时会发送的消息格式
"""

from datetime import datetime
import json

def simulate_11am_notification():
    """模拟11点通知"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 模拟基金数据（实际运行时会获取实时数据）
    funds_data = [
        {"name": "华夏成长混合", "code": "000001", "change": "-0.16%", "trend": "📉"},
        {"name": "易方达消费行业", "code": "110022", "change": "-0.19%", "trend": "📉"},
        {"name": "招商中证白酒指数", "code": "161725", "change": "-0.05%", "trend": "📉"},
        {"name": "南方纳斯达克100指数", "code": "021000", "change": "-1.43%", "trend": "📉"},
        {"name": "易方达蓝筹精选混合", "code": "005827", "change": "-0.11%", "trend": "📉"},
        {"name": "广发全球精选股票(QDII)", "code": "270023", "change": "-0.58%", "trend": "📉"},
        {"name": "中欧医疗创新股票A", "code": "006228", "change": "+2.53%", "trend": "📈"}
    ]
    
    # 生成通知消息
    message = f"⏰ 每日基金播报 {current_time}\n"
    message += "=" * 35 + "\n\n"
    
    # 今日涨跌统计
    up_count = sum(1 for f in funds_data if f["trend"] == "📈")
    down_count = sum(1 for f in funds_data if f["trend"] == "📉")
    
    message += f"📊 监控基金: {len(funds_data)} 只\n"
    message += f"📈 上涨: {up_count} 只 | 📉 下跌: {down_count} 只\n\n"
    
    # 基金列表
    message += "🔍 各基金表现:\n"
    for i, fund in enumerate(funds_data, 1):
        message += f"{i}. {fund['trend']} {fund['name']}: {fund['change']}\n"
    
    # 突出表现
    message += "\n⭐ 今日亮点:\n"
    
    # 找涨幅最大的
    max_up = max([f for f in funds_data if "+" in f["change"]], 
                 key=lambda x: float(x["change"].replace('+', '').replace('%', '')), 
                 default=None)
    if max_up:
        message += f"  涨幅最高: {max_up['name']} {max_up['change']}\n"
    
    # 找跌幅最大的
    max_down = min([f for f in funds_data if "-" in f["change"]], 
                   key=lambda x: float(x["change"].replace('-', '').replace('%', '')), 
                   default=None)
    if max_down:
        message += f"  跌幅最大: {max_down['name']} {max_down['change']}\n"
    
    message += "\n📝 详细数据已保存到日志文件"
    message += "\n⏳ 下次检查: 明日 11:00"
    
    return message

if __name__ == "__main__":
    print("=== 模拟11点基金通知测试 ===\n")
    print("当cron任务在11点触发时，你会收到类似以下格式的消息：\n")
    print("-" * 50)
    notification = simulate_11am_notification()
    print(notification)
    print("-" * 50)
    
    print("\n✅ 测试完成！")
    print(f"实际11点运行时，会获取实时数据并发送通知。")
    print(f"下次自动运行: 今天 11:00 (约1小时后)")