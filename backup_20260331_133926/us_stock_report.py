#!/usr/bin/env python3
"""
美股三大科技股报告
英伟达(NVDA)、谷歌(GOOGL)、苹果(AAPL)前一日股价
"""

import datetime
import random
import json
import os

def get_stock_data():
    """获取美股三大科技股数据"""
    # 股票代码和名称映射
    stocks = {
        "NVDA": "英伟达(NVIDIA)",
        "GOOGL": "谷歌(Alphabet)",
        "AAPL": "苹果(Apple)"
    }
    
    # 获取前一日日期（美股交易日）
    today = datetime.datetime.now()
    # 如果是周一，前一日是上周五
    if today.weekday() == 0:  # 周一
        previous_day = today - datetime.timedelta(days=3)
    else:
        previous_day = today - datetime.timedelta(days=1)
    
    date_str = previous_day.strftime('%Y-%m-%d')
    
    # 模拟股价数据（实际使用时可以接入雅虎财经、Alpha Vantage等API）
    stock_data = []
    for symbol, name in stocks.items():
        # 模拟收盘价和涨跌
        base_prices = {
            "NVDA": 950.0,  # 英伟达
            "GOOGL": 180.0, # 谷歌
            "AAPL": 220.0   # 苹果
        }
        
        base_price = base_prices.get(symbol, 100.0)
        # 模拟涨跌在-5%到+5%之间
        change_percent = round(random.uniform(-5.0, 5.0), 2)
        change_amount = round(base_price * change_percent / 100, 2)
        current_price = round(base_price + change_amount, 2)
        
        stock_data.append({
            "symbol": symbol,
            "name": name,
            "date": date_str,
            "price": current_price,
            "change": change_amount,
            "change_percent": change_percent
        })
    
    return stock_data

def generate_stock_report():
    """生成美股报告"""
    stock_data = get_stock_data()
    
    # 生成报告
    report = []
    report.append("📈 美股三大科技股")
    report.append("=" * 30)
    report.append(f"📅 交易日: {stock_data[0]['date']}")
    report.append("")
    
    for stock in stock_data:
        if stock["change"] > 0:
            emoji = "📈"
        else:
            emoji = "📉"
        
        report.append(f"{emoji} {stock['name']} ({stock['symbol']})")
        report.append(f"   价格: ${stock['price']:.2f}")
        report.append(f"   涨跌: {stock['change']:+.2f} ({stock['change_percent']:+.2f}%)")
        report.append("")
    
    report.append("💡 数据来源: 模拟数据")
    report.append("⏰ 下次报告: 明日 9:00")
    report.append("=" * 30)
    
    return "\n".join(report)

def save_report(report):
    """保存报告到文件"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"us_stock_report_{timestamp}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filename

def main():
    """主函数"""
    print("=== 生成美股三大科技股报告 ===")
    report = generate_stock_report()
    print(report)
    
    # 保存报告
    filename = save_report(report)
    print(f"\n📁 报告已保存: {filename}")
    print("✅ 美股报告生成完成！")
    
    return report

if __name__ == "__main__":
    main()