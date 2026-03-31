#!/usr/bin/env python3
"""
使用 AKshare 的基金报告
获取官方净值数据，而不是实时估算数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import json
import sys

def get_fund_data_akshare(fund_code):
    """使用 AKshare 获取基金数据"""
    try:
        # 获取基金信息（官方净值数据）
        fund_info = ak.fund_open_fund_info_em(symbol=fund_code, indicator='单位净值走势')
        
        if not fund_info.empty:
            # 获取最新数据
            latest = fund_info.iloc[-1]
            
            # 解析数据
            data = {
                'code': fund_code,
                '净值日期': latest.get('净值日期', '未知'),
                '单位净值': latest.get('单位净值', 0),
                '日增长率': latest.get('日增长率', '0.00'),
                '累计净值': latest.get('累计净值', 0)
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
            print(f"警告: 未找到基金 {fund_code} 的数据")
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
        # 默认基金列表
        return [
            {"code": "000001", "name": "华夏成长混合"},
            {"code": "110022", "name": "易方达消费行业"},
            {"code": "161725", "name": "招商中证白酒指数"},
            {"code": "021000", "name": "南方纳斯达克100指数"},
            {"code": "005827", "name": "易方达蓝筹精选混合"},
            {"code": "270023", "name": "广发全球精选股票(QDII)"},
            {"code": "006228", "name": "中欧医疗创新股票A"}
        ]

def generate_akshare_report():
    """生成 AKshare 基金报告"""
    now = datetime.now().strftime('%m-%d %H:%M')
    
    # 加载基金配置
    funds = load_fund_config()
    
    # 获取基金数据
    fund_results = []
    up_count = 0
    down_count = 0
    
    print(f"📊 正在使用 AKshare 获取 {len(funds)} 只基金数据...")
    print("注意: AKshare 提供的是官方净值数据，非实时估算")
    print()
    
    for fund in funds:
        code = fund["code"]
        name = fund["name"]
        
        data = get_fund_data_akshare(code)
        
        if data:
            change = data['日增长率']
            nav_date = data['净值日期']
            nav = data['单位净值']
            
            if change > 0:
                emoji = "📈"
                up_count += 1
            elif change < 0:
                emoji = "📉"
                down_count += 1
            else:
                emoji = "➡️"
            
            fund_results.append({
                "name": name,
                "code": code,
                "change": change,
                "emoji": emoji,
                "nav_date": nav_date,
                "nav": nav
            })
            
            print(f"  {emoji} {name} ({code}): {change:+.2f}% | 净值: {nav} | 日期: {nav_date}")
            
        else:
            print(f"  ❌ {name} ({code}): 获取数据失败")
            fund_results.append({
                "name": name,
                "code": code,
                "change": 0.0,
                "emoji": "❓",
                "nav_date": "未知",
                "nav": 0
            })
    
    # 生成报告
    report = []
    report.append(f"📊 AKshare 基金报告 {now}")
    report.append("="*50)
    report.append(f"📈 上涨: {up_count}只 | 📉 下跌: {down_count}只 | ➡️ 平盘: {len(funds)-up_count-down_count}只")
    report.append("")
    
    # 按涨跌幅排序
    sorted_funds = sorted(fund_results, key=lambda x: x["change"], reverse=True)
    
    for fund in sorted_funds:
        if fund["change"] > 0:
            report.append(f"{fund['emoji']} {fund['name']}: +{fund['change']:.2f}% (净值: {fund['nav']}, {fund['nav_date']})")
        elif fund["change"] < 0:
            report.append(f"{fund['emoji']} {fund['name']}: {fund['change']:.2f}% (净值: {fund['nav']}, {fund['nav_date']})")
        else:
            report.append(f"{fund['emoji']} {fund['name']}: {fund['change']:.2f}% (净值: {fund['nav']}, {fund['nav_date']})")
    
    report.append("")
    report.append("📊 数据说明:")
    report.append("  ✅ 数据来源: AKshare (东方财富)")
    report.append("  ✅ 数据类型: 官方净值数据")
    report.append("  ⚠️  更新时间: 上一个交易日收盘后")
    report.append("  ⚠️  非实时: 这是官方确认的净值，非盘中估算")
    
    report.append("")
    report.append("💡 市场概览:")
    if up_count > down_count:
        report.append("  ✅ 上一个交易日整体上涨")
    elif down_count > up_count:
        report.append("  ⚠️ 上一个交易日整体下跌")
    else:
        report.append("  ⚖️ 上一个交易日涨跌互现")
    
    # 找出领涨和领跌
    if sorted_funds:
        top_gainer = sorted_funds[0]
        top_loser = sorted_funds[-1] if sorted_funds[-1]["change"] < 0 else None
        
        report.append("")
        report.append("🏆 上个交易日表现:")
        report.append(f"  领涨: {top_gainer['name']} ({top_gainer['change']:+.2f}%)")
        if top_loser:
            report.append(f"  领跌: {top_loser['name']} ({top_loser['change']:+.2f}%)")
    
    report.append("="*50)
    
    return "\n".join(report)

def main():
    """主函数"""
    print("=== 生成 AKshare 基金报告（官方净值数据） ===")
    
    try:
        report = generate_akshare_report()
        print("\n" + report)
        
        # 保存到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"akshare_fund_report_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 更新最新报告文件
        with open("latest_akshare_report.txt", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📁 报告已保存: {filename}")
        print("📝 最新报告已更新: latest_akshare_report.txt")
        print("✅ AKshare 基金报告生成完成！")
        
        return report
        
    except Exception as e:
        error_msg = f"❌ 生成报告失败: {e}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    main()