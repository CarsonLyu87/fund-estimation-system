#!/usr/bin/env python3
"""
易方达蓝筹精选混合 (005827) 数据对比分析
对比天天基金网实时估算 vs AKshare官方净值
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import json
import urllib.request
import time

def get_tiantian_fund_data(fund_code):
    """获取天天基金网实时估算数据"""
    try:
        url = f'http://fundgz.1234567.com.cn/js/{fund_code}.js'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            text = response.read().decode('utf-8')
            
            if 'jsonpgz(' in text:
                json_str = text[text.find('(')+1:text.rfind(')')]
                data = json.loads(json_str)
                
                return {
                    'source': '天天基金网',
                    'fund_code': data.get('fundcode', ''),
                    'fund_name': data.get('name', ''),
                    'dwjz': float(data.get('dwjz', 0)),  # 单位净值
                    'gsz': float(data.get('gsz', 0)),    # 估算净值
                    'gszzl': float(data.get('gszzl', 0)), # 估算涨跌
                    'gztime': data.get('gztime', ''),
                    'data_type': '实时估算',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
        return None
    except Exception as e:
        return {'error': f'天天基金网数据获取失败: {e}'}

def get_akshare_fund_data(fund_code):
    """获取AKshare官方净值数据"""
    try:
        # 获取基金信息（官方净值数据）
        fund_info = ak.fund_open_fund_info_em(symbol=fund_code, indicator='单位净值走势')
        
        if not fund_info.empty:
            # 获取最新数据
            latest = fund_info.iloc[-1]
            
            # 解析数据
            nav_date = latest.get('净值日期', '未知')
            nav = latest.get('单位净值', 0)
            change_str = latest.get('日增长率', '0.00')
            
            # 转换日增长率为浮点数
            try:
                if isinstance(change_str, str):
                    change = float(change_str.replace('%', ''))
                else:
                    change = float(change_str)
            except:
                change = 0.0
            
            return {
                'source': 'AKshare (东方财富)',
                'fund_code': fund_code,
                'fund_name': '易方达蓝筹精选混合',
                'nav_date': nav_date,
                'nav': float(nav),
                'change': change,
                'data_type': '官方净值',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_lag': '上一个交易日收盘后'
            }
        else:
            return {'error': '未找到基金数据'}
            
    except Exception as e:
        return {'error': f'AKshare数据获取失败: {e}'}

def get_akshare_estimation(fund_code):
    """尝试获取AKshare的实时估算数据"""
    try:
        # 获取所有基金的估值数据
        fund_estimation = ak.fund_value_estimation_em(symbol='全部')
        if not fund_estimation.empty:
            # 查找特定基金
            fund_data = fund_estimation[fund_estimation['代码'] == fund_code]
            if not fund_data.empty:
                latest = fund_data.iloc[-1]
                return {
                    'source': 'AKshare实时估算',
                    'fund_name': latest.get('名称', ''),
                    'est_nav': float(latest.get('估算净值', 0)),
                    'est_change': float(latest.get('估算涨跌幅', 0)),
                    'update_time_est': latest.get('更新时间', ''),
                    'data_type': '实时估算'
                }
        return None
    except Exception as e:
        return {'error': f'AKshare实时估算获取失败: {e}'}

def analyze_fund_composition(fund_code):
    """分析基金持仓构成（模拟）"""
    # 易方达蓝筹精选混合的主要持仓（根据公开信息）
    holdings = [
        {'stock': '贵州茅台', 'weight': 9.8, 'sector': '白酒'},
        {'stock': '腾讯控股', 'weight': 9.5, 'sector': '互联网'},
        {'stock': '招商银行', 'weight': 9.2, 'sector': '银行'},
        {'stock': '五粮液', 'weight': 8.7, 'sector': '白酒'},
        {'stock': '香港交易所', 'weight': 8.3, 'sector': '金融'},
        {'stock': '美团-W', 'weight': 7.9, 'sector': '互联网'},
        {'stock': '中国平安', 'weight': 7.5, 'sector': '保险'},
        {'stock': '药明康德', 'weight': 6.8, 'sector': '医药'},
        {'stock': '洋河股份', 'weight': 6.2, 'sector': '白酒'},
        {'stock': '其他', 'weight': 26.1, 'sector': '分散'}
    ]
    
    return holdings

def get_market_status():
    """获取当前市场状态"""
    current_time = datetime.now()
    market_open = current_time.hour >= 9 and current_time.hour < 15
    market_closed = current_time.hour >= 15 or current_time.hour < 9
    
    status = {
        'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'market_open': market_open,
        'market_closed': market_closed,
        'trading_hours': '09:30-11:30, 13:00-15:00',
        'next_trading_day': '2026-03-31' if current_time.hour >= 15 else '今日'
    }
    
    return status

def main():
    """主函数"""
    print("="*70)
    print("易方达蓝筹精选混合 (005827) 数据对比分析")
    print("="*70)
    
    fund_code = '005827'
    
    # 获取市场状态
    market = get_market_status()
    print(f"\n📅 当前时间: {market['current_time']}")
    print(f"🏦 市场状态: {'交易中' if market['market_open'] else '已收盘' if market['market_closed'] else '未开市'}")
    print(f"⏰ 交易时间: {market['trading_hours']}")
    print(f"📈 下一个交易日: {market['next_trading_day']}")
    
    print("\n" + "="*70)
    print("1. 数据源对比分析")
    print("="*70)
    
    # 获取天天基金网数据
    print("\n🔍 天天基金网实时估算数据:")
    tiantian_data = get_tiantian_fund_data(fund_code)
    if 'error' not in tiantian_data:
        print(f"   基金名称: {tiantian_data['fund_name']}")
        print(f"   单位净值: {tiantian_data['dwjz']:.4f} (前一日收盘)")
        print(f"   估算净值: {tiantian_data['gsz']:.4f}")
        print(f"   估算涨跌: {tiantian_data['gszzl']:+.4f}%")
        print(f"   更新时间: {tiantian_data['gztime']}")
        print(f"   数据类型: {tiantian_data['data_type']}")
    else:
        print(f"   ❌ {tiantian_data['error']}")
    
    # 获取AKshare官方净值数据
    print("\n🔍 AKshare官方净值数据:")
    akshare_data = get_akshare_fund_data(fund_code)
    if 'error' not in akshare_data:
        print(f"   基金名称: {akshare_data['fund_name']}")
        print(f"   净值日期: {akshare_data['nav_date']}")
        print(f"   单位净值: {akshare_data['nav']:.4f}")
        print(f"   日增长率: {akshare_data['change']:+.4f}%")
        print(f"   数据来源: {akshare_data['source']}")
        print(f"   数据类型: {akshare_data['data_type']}")
        print(f"   数据延迟: {akshare_data['data_lag']}")
    else:
        print(f"   ❌ {akshare_data['error']}")
    
    # 尝试获取AKshare实时估算
    print("\n🔍 AKshare实时估算数据:")
    akshare_est = get_akshare_estimation(fund_code)
    if akshare_est and 'error' not in akshare_est:
        print(f"   基金名称: {akshare_est['fund_name']}")
        print(f"   估算净值: {akshare_est['est_nav']:.4f}")
        print(f"   估算涨跌: {akshare_est['est_change']:+.4f}%")
        print(f"   更新时间: {akshare_est['update_time_est']}")
        print(f"   数据来源: {akshare_est['source']}")
    elif akshare_est and 'error' in akshare_est:
        print(f"   ⚠️  {akshare_est['error']}")
    else:
        print("   ℹ️  AKshare未提供实时估算数据")
    
    print("\n" + "="*70)
    print("2. 数据差异分析")
    print("="*70)
    
    if 'error' not in tiantian_data and 'error' not in akshare_data:
        tiantian_change = tiantian_data['gszzl']
        akshare_change = akshare_data['change']
        
        print(f"\n📊 涨跌幅对比:")
        print(f"   天天基金网实时估算: {tiantian_change:+.4f}%")
        print(f"   AKshare官方净值: {akshare_change:+.4f}%")
        print(f"   差异: {abs(tiantian_change - akshare_change):.4f}%")
        
        print(f"\n💰 净值对比:")
        print(f"   天天基金网估算净值: {tiantian_data['gsz']:.4f}")
        print(f"   AKshare单位净值: {akshare_data['nav']:.4f}")
        print(f"   前一日单位净值: {tiantian_data['dwjz']:.4f}")
        
        print(f"\n⏰ 时间对比:")
        print(f"   天天基金网数据时间: {tiantian_data['gztime']}")
        print(f"   AKshare净值日期: {akshare_data['nav_date']}")
        
        # 分析差异原因
        print(f"\n🔍 差异原因分析:")
        if tiantian_change < 0 and akshare_change > 0:
            print("   ❗ 严重分歧: 实时估算显示下跌，但官方净值显示上涨")
            print("   可能原因:")
            print("     1. 实时估算算法不准确")
            print("     2. 持仓股票实时价格与收盘价差异大")
            print("     3. 基金调仓未在估算中反映")
        elif abs(tiantian_change - akshare_change) > 1.0:
            print("   ⚠️  显著差异: 涨跌幅差异超过1%")
            print("   可能原因:")
            print("     1. 市场波动较大")
            print("     2. 估算模型误差")
            print("     3. 数据源不同导致的计算差异")
        else:
            print("   ✅ 差异较小: 在正常误差范围内")
    
    print("\n" + "="*70)
    print("3. 基金持仓分析（影响估算的因素）")
    print("="*70)
    
    holdings = analyze_fund_composition(fund_code)
    print(f"\n📈 易方达蓝筹精选混合主要持仓（模拟）:")
    total_weight = 0
    for i, holding in enumerate(holdings[:5], 1):
        print(f"   {i}. {holding['stock']}: {holding['weight']:.1f}% ({holding['sector']})")
        total_weight += holding['weight']
    
    print(f"   前5大持仓占比: {total_weight:.1f}%")
    print(f"   其他持仓: {holdings[-1]['weight']:.1f}%")
    
    print(f"\n🔍 实时估算影响因素:")
    print("   1. 持仓股票实时价格变动")
    print("   2. 基金仓位调整（估算可能滞后）")
    print("   3. 现金仓位影响（通常10-20%）")
    print("   4. 汇率波动（港股持仓）")
    print("   5. 分红除权影响")
    
    print("\n" + "="*70)
    print("4. 结论与建议")
    print("="*70)
    
    print(f"\n🎯 数据可靠性评估:")
    print("   ✅ AKshare官方净值:")
    print("      - 基金公司确认的官方数据")
    print("      - 准确性最高")
    print("      - 缺点是T+1延迟")
    
    print("\n   ⚠️  天天基金网实时估算:")
    print("      - 实时性较好")
    print("      - 但估算误差可能较大")
    print("      - 适合盘中参考，不可作为交易依据")
    
    print(f"\n💡 投资建议:")
    print("   1. 以官方净值为准，实时估算仅作参考")
    print("   2. 关注基金持仓变化和经理操作")
    print("   3. 长期投资应关注基本面而非短期波动")
    print("   4. 定期查看基金季报了解最新持仓")
    
    print(f"\n📝 最终结论:")
    if 'error' not in akshare_data:
        print(f"   易方达蓝筹精选混合官方净值: {akshare_data['nav']:.4f}")
        print(f"   上一个交易日涨跌: {akshare_data['change']:+.4f}%")
        print(f"   数据日期: {akshare_data['nav_date']}")
    else:
        print("   ❌ 无法获取准确数据，建议直接查看基金公司官网")
    
    print("\n" + "="*70)
    print("分析完成！")
    print("="*70)

if __name__ == "__main__":
    main()