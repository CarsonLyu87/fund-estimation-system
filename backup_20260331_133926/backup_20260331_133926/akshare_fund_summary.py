#!/usr/bin/env python3
"""
AKshare 基金简报 - 简洁版
适合微信消息发送
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import json

def get_fund_data_akshare(fund_code):
    """使用 AKshare 获取基金数据"""
    try:
        fund_info = ak.fund_open_fund_info_em(symbol=fund_code, indicator='单位净值走势')
        
        if not fund_info.empty:
            latest = fund_info.iloc[-1]
            
            data = {
                'code': fund_code,
                '净值日期': latest.get('净值日期', '未知'),
                '单位净值': latest.get('单位净值', 0),
                '日增长率': latest.get('日增长率', '0.00'),
            }
            
            # 转换日增长率为浮点数
            try:
                if isinstance(data['日增长率'], str):
                    data['日增长率'] = float(data['日增长率'].replace('%', ''))
                else:
                    data['日增长率'] = float(data['日增长率'])
            except:
                data['日增长率'] = 0.0
                
            return data
        else:
            return None
            
    except Exception as e:
        print(f"获取基金 {fund_code} 数据失败: {e}")
        return None

def load_fund_config():
    """加载基金配置"""
    try:
        with open('fund_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('funds', [])
    except Exception as e:
        print(f"加载基金配置失败: {e}")
        return [
            {"code": "000001", "name": "华夏成长混合"},
            {"code": "110022", "name": "易方达消费行业"},
            {"code": "161725", "name": "招商中证白酒指数"},
            {"code": "021000", "name": "南方纳斯达克100指数"},
            {"code": "005827", "name": "易方达蓝筹精选混合"},
            {"code": "270023", "name": "广发全球精选股票(QDII)"},
            {"code": "006228", "name": "中欧医疗创新股票A"}
        ]

def generate_akshare_summary():
    """生成 AKshare 基金简报"""
    now = datetime.now().strftime('%m-%d %H:%M')
    
    # 加载基金配置
    funds = load_fund_config()
    
    # 获取基金数据
    fund_results = []
    
    for fund in funds:
        code = fund["code"]
        name = fund["name"]
        
        data = get_fund_data_akshare(code)
        
        if data:
            change = data['日增长率']
            nav_date = data['净值日期']
            
            if change > 0:
                emoji = "📈"
            elif change < 0:
                emoji = "📉"
            else:
                emoji = "➡️"
            
            fund_results.append({
                "name": name,
                "change": change,
                "emoji": emoji,
                "nav_date": nav_date
            })
        else:
            fund_results.append({
                "name": name,
                "change": 0.0,
                "emoji": "❓",
                "nav_date": "未知"
            })
    
    # 计算涨跌数量
    up_count = sum(1 for f in fund_results if f["change"] > 0)
    down_count = sum(1 for f in fund_results if f["change"] < 0)
    
    # 找出领涨和领跌
    sorted_funds = sorted(fund_results, key=lambda x: x["change"], reverse=True)
    top_gainers = [f for f in sorted_funds if f["change"] > 0][:2]
    top_losers = [f for f in sorted_funds if f["change"] < 0][:2]
    
    # 生成简报
    summary = []
    summary.append(f"📊 基金简报 {now}")
    summary.append("="*30)
    summary.append(f"👤 持仓: {len(funds)}只 (↑{up_count} ↓{down_count})")
    summary.append("")
    
    if top_gainers:
        summary.append("🏆 领涨:")
        for fund in top_gainers:
            summary.append(f"  {fund['emoji']} {fund['name']}: {fund['change']:+.2f}%")
        summary.append("")
    
    if top_losers:
        summary.append("📉 领跌:")
        for fund in top_losers:
            summary.append(f"  {fund['emoji']} {fund['name']}: {fund['change']:+.2f}%")
        summary.append("")
    
    # 数据说明
    summary.append("📝 数据说明:")
    summary.append("  ✅ AKshare官方净值")
    summary.append(f"  📅 最新数据: {sorted_funds[0]['nav_date'] if sorted_funds else '未知'}")
    summary.append("")
    
    summary.append("⏰ 下次报告: 明日 14:00")
    summary.append("="*30)
    
    return "\n".join(summary)

def main():
    """主函数"""
    print("=== 生成 AKshare 基金简报（简洁版） ===")
    
    try:
        summary = generate_akshare_summary()
        print("\n" + summary)
        
        # 保存到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"akshare_fund_summary_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n📁 简报已保存: {filename}")
        print("✅ AKshare 基金简报生成完成！")
        
        return summary
        
    except Exception as e:
        error_msg = f"❌ 生成简报失败: {e}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    main()