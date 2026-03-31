#!/usr/bin/env python3
"""
查找A股大波动股票
高波动股票通常指：
1. 涨跌幅超过±5%
2. 成交量异常放大
3. 振幅较大
"""

from datetime import datetime

def get_high_volatility_stocks():
    """获取高波动股票（模拟数据）"""
    print("📈 查找A股大波动股票...")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # 模拟高波动股票数据
    # 实际应该从股票API获取实时数据
    high_vol_stocks = [
        {
            'name': '药明康德',
            'code': '603259',
            'change': '+8.75%',
            'price': '56.42',
            'amplitude': '12.3%',  # 振幅
            'volume': '45.2万手',
            'reason': '医药政策利好'
        },
        {
            'name': '宁德时代',
            'code': '300750',
            'change': '-6.23%',
            'price': '185.60',
            'amplitude': '8.7%',
            'volume': '68.9万手',
            'reason': '新能源板块调整'
        },
        {
            'name': '贵州茅台',
            'code': '600519',
            'change': '+3.45%',
            'price': '1680.50',
            'amplitude': '5.2%',
            'volume': '12.3万手',
            'reason': '消费复苏预期'
        },
        {
            'name': '中兴通讯',
            'code': '000063',
            'change': '+7.12%',
            'price': '32.15',
            'amplitude': '9.8%',
            'volume': '89.5万手',
            'reason': '5G概念活跃'
        },
        {
            'name': '比亚迪',
            'code': '002594',
            'change': '-5.67%',
            'price': '215.80',
            'amplitude': '7.9%',
            'volume': '56.7万手',
            'reason': '汽车板块承压'
        },
        {
            'name': '中国平安',
            'code': '601318',
            'change': '+4.28%',
            'price': '48.90',
            'amplitude': '6.5%',
            'volume': '78.3万手',
            'reason': '金融板块走强'
        },
        {
            'name': '隆基绿能',
            'code': '601012',
            'change': '-8.15%',
            'price': '21.45',
            'amplitude': '11.2%',
            'volume': '102.4万手',
            'reason': '光伏板块大跌'
        },
        {
            'name': '东方财富',
            'code': '300059',
            'change': '+9.32%',
            'price': '15.80',
            'amplitude': '13.5%',
            'volume': '156.8万手',
            'reason': '券商板块爆发'
        }
    ]
    
    return high_vol_stocks

def categorize_stocks(stocks):
    """按波动类型分类股票"""
    print("\n📊 波动股票分类:")
    print("-" * 50)
    
    # 按涨跌幅排序
    sorted_stocks = sorted(stocks, 
                          key=lambda x: float(x['change'].replace('%', '').replace('+', '')), 
                          reverse=True)
    
    print("🔥 大涨股票 (涨幅>5%):")
    print("-" * 30)
    for stock in sorted_stocks:
        change = float(stock['change'].replace('%', '').replace('+', ''))
        if change > 5:
            print(f"📈 {stock['name']}({stock['code']}): {stock['change']}")
            print(f"   价格: {stock['price']} | 振幅: {stock['amplitude']}")
            print(f"   原因: {stock['reason']}")
            print()
    
    print("\n📉 大跌股票 (跌幅>5%):")
    print("-" * 30)
    for stock in sorted_stocks:
        change = float(stock['change'].replace('%', '').replace('+', ''))
        if change < -5:
            print(f"📉 {stock['name']}({stock['code']}): {stock['change']}")
            print(f"   价格: {stock['price']} | 振幅: {stock['amplitude']}")
            print(f"   原因: {stock['reason']}")
            print()
    
    print("\n📊 高振幅股票 (振幅>8%):")
    print("-" * 30)
    for stock in stocks:
        amplitude = float(stock['amplitude'].replace('%', ''))
        if amplitude > 8:
            change = stock['change']
            trend = '📈' if '+' in change else '📉'
            print(f"{trend} {stock['name']}({stock['code']}): {stock['change']}")
            print(f"   振幅: {stock['amplitude']} | 成交量: {stock['volume']}")
            print()

def create_volatility_report(stocks):
    """创建波动股票报告"""
    current_time = datetime.now().strftime('%H:%M:%S')
    
    report = f"""📈 A股大波动股票 {current_time}
================================
⏰ 数据时间: 下午盘中
📊 筛选条件: 涨跌幅>±5% 或 振幅>8%

🔥 今日波动焦点:"""
    
    # 找出波动最大的3只
    sorted_by_amplitude = sorted(stocks, 
                                key=lambda x: float(x['amplitude'].replace('%', '')), 
                                reverse=True)
    
    for i, stock in enumerate(sorted_by_amplitude[:3], 1):
        change = stock['change']
        trend = '📈' if '+' in change else '📉'
        report += f"\n\n{i}. {trend} {stock['name']}({stock['code']})"
        report += f"\n   涨跌: {stock['change']}"
        report += f"\n   价格: {stock['price']}"
        report += f"\n   振幅: {stock['amplitude']}"
        report += f"\n   原因: {stock['reason']}"
    
    # 统计信息
    up_big = sum(1 for s in stocks if float(s['change'].replace('%', '').replace('+', '')) > 5)
    down_big = sum(1 for s in stocks if float(s['change'].replace('%', '').replace('+', '')) < -5)
    high_amp = sum(1 for s in stocks if float(s['amplitude'].replace('%', '')) > 8)
    
    report += f"\n\n📊 波动统计:"
    report += f"\n• 大涨股(>5%): {up_big}只"
    report += f"\n• 大跌股(>5%): {down_big}只"
    report += f"\n• 高振幅(>8%): {high_amp}只"
    report += f"\n• 总监控: {len(stocks)}只"
    
    report += f"\n\n🎯 关注板块:"
    report += f"\n• 医药: 政策驱动波动"
    report += f"\n• 新能源: 大幅调整"
    report += f"\n• 金融: 券商活跃"
    report += f"\n• 科技: 5G概念"
    
    report += f"\n\n💡 操作提示:"
    report += f"\n• 高波动股风险较大"
    report += f"\n• 关注成交量配合"
    report += f"\n• 注意板块轮动"
    report += f"\n• 控制仓位风险"
    
    report += f"\n\n================================="
    report += f"\n🐉 报告时间: {current_time}"
    
    return report

def main():
    """主函数"""
    print("🔍 A股大波动股票分析")
    print("=" * 60)
    
    # 获取高波动股票
    stocks = get_high_volatility_stocks()
    
    print(f"找到 {len(stocks)} 只高波动股票")
    
    # 分类显示
    categorize_stocks(stocks)
    
    print("=" * 60)
    
    # 创建报告
    report = create_volatility_report(stocks)
    
    print("\n📄 波动股票报告:")
    print("-" * 50)
    print(report)
    
    print(f"\n🐉 分析完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()