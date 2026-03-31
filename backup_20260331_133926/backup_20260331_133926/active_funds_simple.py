#!/usr/bin/env python3
"""
简化版活跃基金获取
"""

import json
from datetime import datetime

def get_active_funds():
    """
    获取今日最活跃的5只基金
    由于API限制，这里使用模拟数据
    实际使用时可以替换为真实API
    """
    # 模拟数据 - 这些通常是市场上交易最活跃的ETF和基金
    active_funds = [
        {
            "code": "512000",
            "name": "华宝中证全指证券公司ETF",
            "amount": "5.2亿元",
            "change": "+1.23%",
            "reason": "券商板块今日活跃，政策利好预期"
        },
        {
            "code": "512880",
            "name": "国泰中证全指证券公司ETF", 
            "amount": "4.8亿元",
            "change": "+1.15%",
            "reason": "成交量最大的券商ETF"
        },
        {
            "code": "159915",
            "name": "易方达创业板ETF",
            "amount": "3.5亿元", 
            "change": "-0.45%",
            "reason": "创业板代表，科技股波动"
        },
        {
            "code": "510300",
            "name": "华泰柏瑞沪深300ETF",
            "amount": "3.2亿元",
            "change": "+0.32%",
            "reason": "大盘核心，机构资金关注"
        },
        {
            "code": "512690",
            "name": "酒ETF",
            "amount": "2.8亿元",
            "change": "-0.78%",
            "reason": "白酒板块调整，资金分歧"
        }
    ]
    
    # 按成交额排序（模拟）
    active_funds.sort(key=lambda x: float(x["amount"].replace("亿元", "")), reverse=True)
    
    return active_funds

def format_active_funds_message(funds):
    """格式化活跃基金消息"""
    if not funds:
        return ""
    
    message = "🔥 今日最活跃基金TOP 5:\n"
    message += "=" * 40 + "\n"
    
    for i, fund in enumerate(funds[:5], 1):
        # 判断涨跌表情
        change = fund.get("change", "0%")
        if "+" in change:
            emoji = "📈"
        elif "-" in change:
            emoji = "📉"
        else:
            emoji = "➡️"
        
        message += f"{i}. {emoji} {fund['name']} ({fund['code']})\n"
        message += f"   成交额: {fund['amount']} | 涨跌: {change}\n"
        
        reason = fund.get("reason", "")
        if reason:
            message += f"   原因: {reason}\n"
        
        if i < 5:
            message += "\n"
    
    return message

def main():
    """测试函数"""
    print("=== 活跃基金测试 ===\n")
    
    active_funds = get_active_funds()
    message = format_active_funds_message(active_funds)
    
    print(message)
    
    # 保存缓存
    cache_file = "active_funds_cache.json"
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M:%S"),
                "funds": active_funds,
                "source": "模拟数据"
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📁 活跃基金数据已缓存到: {cache_file}")
    except Exception as e:
        print(f"保存缓存失败: {e}")

if __name__ == "__main__":
    main()