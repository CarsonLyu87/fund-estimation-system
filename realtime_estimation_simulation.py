#!/usr/bin/env python3
"""
实时估算过程模拟分析
展示天天基金网如何计算基金实时估算净值
"""

import json
import random
from datetime import datetime, timedelta

def simulate_fund_holdings():
    """模拟基金持仓结构"""
    # 易方达蓝筹精选混合的典型持仓（根据公开季报数据模拟）
    holdings = {
        'A股': [
            {'code': '600519', 'name': '贵州茅台', 'weight': 9.8, 'sector': '白酒', 'price_change': -0.5},
            {'code': '000858', 'name': '五粮液', 'weight': 8.7, 'sector': '白酒', 'price_change': -0.3},
            {'code': '600036', 'name': '招商银行', 'weight': 9.2, 'sector': '银行', 'price_change': -0.8},
            {'code': '601318', 'name': '中国平安', 'weight': 7.5, 'sector': '保险', 'price_change': -0.6},
            {'code': '002415', 'name': '海康威视', 'weight': 4.2, 'sector': '科技', 'price_change': -1.2},
        ],
        '港股': [
            {'code': '00700', 'name': '腾讯控股', 'weight': 9.5, 'sector': '互联网', 'price_change': -1.5, 'hkd_cny': 0.92},
            {'code': '00388', 'name': '香港交易所', 'weight': 8.3, 'sector': '金融', 'price_change': -0.9, 'hkd_cny': 0.92},
            {'code': '03690', 'name': '美团-W', 'weight': 7.9, 'sector': '互联网', 'price_change': -2.1, 'hkd_cny': 0.92},
        ],
        '现金': [
            {'type': '现金及等价物', 'weight': 15.0, 'return': 0.0},
        ],
        '其他': [
            {'type': '债券及其他', 'weight': 19.9, 'return': 0.0},
        ]
    }
    
    return holdings

def calculate_real_time_estimation(holdings, previous_nav=1.7866):
    """计算实时估算净值"""
    
    print("📊 实时估算计算过程")
    print("="*60)
    
    # 1. 计算股票部分贡献
    print("\n1. 股票持仓实时变动计算:")
    print("-"*40)
    
    total_stock_impact = 0
    stock_details = []
    
    # A股部分
    for stock in holdings['A股']:
        impact = stock['weight'] * stock['price_change'] / 100
        total_stock_impact += impact
        stock_details.append({
            'name': stock['name'],
            'weight': stock['weight'],
            'price_change': stock['price_change'],
            'impact': impact
        })
        print(f"   {stock['name']}: {stock['weight']:.1f}% × {stock['price_change']:+.1f}% = {impact:+.4f}%")
    
    # 港股部分（考虑汇率）
    for stock in holdings['港股']:
        # 港股价格变动 + 汇率变动影响
        hk_impact = stock['weight'] * stock['price_change'] / 100
        # 假设汇率今日变动 -0.2%
        fx_impact = stock['weight'] * -0.2 / 100
        total_impact = hk_impact + fx_impact
        total_stock_impact += total_impact
        stock_details.append({
            'name': stock['name'] + '(H)',
            'weight': stock['weight'],
            'price_change': stock['price_change'],
            'fx_change': -0.2,
            'impact': total_impact
        })
        print(f"   {stock['name']}(H): {stock['weight']:.1f}% × ({stock['price_change']:+.1f}% -0.2%汇率) = {total_impact:+.4f}%")
    
    print(f"\n   股票部分总影响: {total_stock_impact:+.4f}%")
    
    # 2. 现金和其他资产贡献（假设为0）
    print("\n2. 现金及其他资产贡献:")
    print("-"*40)
    cash_impact = 0
    for cash in holdings['现金']:
        print(f"   现金({cash['type']}): {cash['weight']:.1f}% × {cash['return']:.1f}% = 0.000%")
    
    other_impact = 0
    for other in holdings['其他']:
        print(f"   其他({other['type']}): {other['weight']:.1f}% × {other['return']:.1f}% = 0.000%")
    
    # 3. 总影响计算
    print("\n3. 总影响计算:")
    print("-"*40)
    total_impact = total_stock_impact + cash_impact + other_impact
    print(f"   股票影响: {total_stock_impact:+.4f}%")
    print(f"   现金影响: {cash_impact:+.4f}%")
    print(f"   其他影响: {other_impact:+.4f}%")
    print(f"   总影响: {total_impact:+.4f}%")
    
    # 4. 估算净值计算
    print("\n4. 估算净值计算:")
    print("-"*40)
    estimated_nav = previous_nav * (1 + total_impact / 100)
    print(f"   前一日净值: {previous_nav:.4f}")
    print(f"   估算涨跌: {total_impact:+.4f}%")
    print(f"   估算净值: {estimated_nav:.4f}")
    
    return {
        'previous_nav': previous_nav,
        'estimated_change': total_impact,
        'estimated_nav': estimated_nav,
        'stock_details': stock_details,
        'total_stock_impact': total_stock_impact
    }

def analyze_estimation_errors(estimation_result, actual_data=None):
    """分析估算误差"""
    print("\n" + "="*60)
    print("🔍 估算误差分析")
    print("="*60)
    
    # 估算误差来源
    print("\n1. 主要误差来源:")
    print("-"*40)
    error_sources = [
        ("持仓数据滞后", "季报数据 vs 实际持仓", "高", "基金可能已调仓但估算仍用旧数据"),
        ("现金仓位变化", "估算假设固定 vs 实际变动", "中", "基金经理可能调整现金比例"),
        ("汇率波动", "估算汇率 vs 实际汇率", "中", "港股部分受汇率影响"),
        ("大宗交易影响", "估算未考虑 vs 实际发生", "低", "基金可能有大宗交易"),
        ("分红除权", "估算未及时调整", "中", "持仓股票可能分红除权"),
        ("停牌股票", "估算用前收 vs 实际价值", "低", "持仓股票可能停牌"),
    ]
    
    for source, description, impact, reason in error_sources:
        print(f"   • {source}: {description} ({impact}影响) - {reason}")
    
    # 与实际情况对比
    if actual_data:
        print(f"\n2. 与实际数据对比:")
        print("-"*40)
        print(f"   估算涨跌: {estimation_result['estimated_change']:+.4f}%")
        print(f"   实际涨跌: {actual_data['actual_change']:+.4f}%")
        print(f"   误差: {abs(estimation_result['estimated_change'] - actual_data['actual_change']):.4f}%")
        
        if abs(estimation_result['estimated_change'] - actual_data['actual_change']) > 0.5:
            print(f"\n   ⚠️  显著误差警告: 误差超过0.5%")
            print("   可能原因:")
            print("     - 基金已大幅调仓")
            print("     - 现金仓位变化较大")
            print("     - 汇率波动超预期")
            print("     - 估算模型缺陷")
    
    # 估算可靠性评估
    print(f"\n3. 估算可靠性评估:")
    print("-"*40)
    reliability_factors = [
        ("数据时效性", "季报数据，可能滞后1-3个月", "低"),
        ("模型准确性", "基于公开算法，有一定误差", "中"),
        ("市场波动", "正常交易日误差较小", "中"),
        ("特殊日期", "分红季、调仓期误差大", "高"),
    ]
    
    for factor, description, error in reliability_factors:
        print(f"   • {factor}: {description} (误差风险: {error})")
    
    print(f"\n💡 估算使用建议:")
    print("   1. 仅作盘中参考，不可作为交易依据")
    print("   2. 关注基金公司官方公告")
    print("   3. 季报发布后重新评估估算准确性")
    print("   4. 大额交易前以官方净值为准")

def simulate_market_scenarios():
    """模拟不同市场情景下的估算"""
    print("\n" + "="*60)
    print("📈 不同市场情景模拟")
    print("="*60)
    
    scenarios = [
        {"name": "正常波动", "a股_change": -0.5, "港股_change": -1.0, "fx_change": -0.2},
        {"name": "大幅下跌", "a股_change": -2.0, "港股_change": -3.0, "fx_change": -0.5},
        {"name": "小幅上涨", "a股_change": 0.5, "港股_change": 1.0, "fx_change": 0.1},
        {"name": "分化行情", "a股_change": -1.0, "港股_change": 1.5, "fx_change": 0.3},
    ]
    
    previous_nav = 1.7866
    
    for scenario in scenarios:
        print(f"\n情景: {scenario['name']}")
        print("-"*30)
        
        # 简化计算
        a股_weight = 45.0  # 假设A股总权重45%
        港股_weight = 30.0  # 假设港股总权重30%
        现金其他_weight = 25.0  # 现金和其他25%
        
        a股_impact = a股_weight * scenario['a股_change'] / 100
        港股_price_impact = 港股_weight * scenario['港股_change'] / 100
        港股_fx_impact = 港股_weight * scenario['fx_change'] / 100
        港股_total_impact = 港股_price_impact + 港股_fx_impact
        
        total_impact = a股_impact + 港股_total_impact
        estimated_nav = previous_nav * (1 + total_impact / 100)
        
        print(f"  A股: {a股_weight:.1f}% × {scenario['a股_change']:+.1f}% = {a股_impact:+.4f}%")
        print(f"  港股: {港股_weight:.1f}% × ({scenario['港股_change']:+.1f}% {scenario['fx_change']:+.1f}%汇率) = {港股_total_impact:+.4f}%")
        print(f"  现金其他: {现金其他_weight:.1f}% × 0% = 0.000%")
        print(f"  总影响: {total_impact:+.4f}%")
        print(f"  估算净值: {estimated_nav:.4f}")

def main():
    """主函数"""
    print("="*70)
    print("易方达蓝筹精选混合 (005827) 实时估算过程分析")
    print("="*70)
    
    print(f"\n📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏦 基金代码: 005827")
    print(f"📈 前一日净值: 1.7866 (2026-03-27)")
    
    # 模拟持仓
    holdings = simulate_fund_holdings()
    
    # 计算实时估算
    estimation = calculate_real_time_estimation(holdings)
    
    # 与实际数据对比（使用天天基金网数据）
    actual_data = {
        'actual_change': -0.04,  # 天天基金网显示-0.04%
        'source': '天天基金网 2026-03-30 14:47'
    }
    
    # 分析误差
    analyze_estimation_errors(estimation, actual_data)
    
    # 模拟不同市场情景
    simulate_market_scenarios()
    
    print("\n" + "="*70)
    print("🎯 关键结论")
    print("="*70)
    
    print(f"\n1. 当前估算结果:")
    print(f"   估算涨跌: {estimation['estimated_change']:+.4f}%")
    print(f"   估算净值: {estimation['estimated_nav']:.4f}")
    
    print(f"\n2. 与实际对比:")
    print(f"   天天基金网显示: {actual_data['actual_change']:+.4f}%")
    print(f"   估算误差: {abs(estimation['estimated_change'] - actual_data['actual_change']):.4f}%")
    
    print(f"\n3. 估算过程总结:")
    print("   • 基于季报持仓数据计算")
    print("   • 考虑A股、港股实时价格")
    print("   • 包含汇率影响")
    print("   • 现金部分假设无收益")
    
    print(f"\n4. 可靠性评估:")
    print("   ✅ 优点: 实时性较好，反映市场情绪")
    print("   ⚠️  缺点: 基于滞后数据，误差可能较大")
    print("   ⚠️  注意: 不可作为交易依据，以官方净值为准")
    
    print(f"\n💡 最终建议:")
    print("   使用AKshare的官方净值数据 ({akshare_nav:.4f}, +{akshare_change:.2f}%)".format(
        akshare_nav=1.7866, akshare_change=0.74))
    print("   天天基金网实时估算仅作盘中参考")
    
    print("\n" + "="*70)
    print("分析完成！")
    print("="*70)

if __name__ == "__main__":
    main()