#!/usr/bin/env python3
"""
专注基金报告
只显示指定基金的涨跌情况，保持名称完整
"""

import datetime
import random

def generate_focused_report():
    """生成专注基金报告"""
    now = datetime.datetime.now().strftime('%m-%d %H:%M')
    
    # 7只关注的基金（名称保留完整）
    focused_funds = [
        "华夏成长混合",
        "易方达消费行业", 
        "招商中证白酒指数",
        "南方纳斯达克100指数",
        "易方达蓝筹精选混合",
        "广发全球精选股票(QDII)",
        "中欧医疗创新股票A"
    ]
    
    # 生成模拟涨跌数据（实际使用时替换为真实API）
    fund_data = []
    for fund in focused_funds:
        # 模拟涨跌在-2%到+3%之间
        change = round(random.uniform(-2.0, 3.0), 2)
        fund_data.append((fund, change))
    
    # 生成报告
    report = []
    report.append(f"📊 基金关注 {now}")
    report.append("="*30)
    
    for fund, change in fund_data:
        if change > 0:
            report.append(f"📈 {fund}: +{change}%")
        else:
            report.append(f"📉 {fund}: {change}%")
    
    report.append("="*30)
    
    return "\n".join(report)

def main():
    """主函数"""
    print("=== 生成专注基金报告 ===")
    report = generate_focused_report()
    print(report)
    
    # 保存到文件
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"focused_fund_report_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 报告已保存: {filename}")
    print("✅ 专注基金报告生成完成！")

if __name__ == "__main__":
    main()