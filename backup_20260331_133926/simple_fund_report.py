#!/usr/bin/env python3
"""
简化版基金报告生成器
生成简洁的基金简报，适合微信消息发送
"""

import datetime
import random

def generate_simple_report():
    """生成简化版基金报告"""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 模拟基金数据（实际使用时可以替换为真实API）
    funds = [
        ("华夏成长混合", 2.52),
        ("易方达消费行业", 0.53),
        ("招商中证白酒指数", 0.13),
        ("南方纳斯达克100指数", -1.43),
        ("易方达蓝筹精选混合", 0.24),
        ("广发全球精选股票(QDII)", -0.58),
        ("中欧医疗创新股票A", 0.25)
    ]
    
    # 计算涨跌数量
    up_count = sum(1 for _, change in funds if change > 0)
    down_count = sum(1 for _, change in funds if change < 0)
    
    # 找出领涨和领跌基金
    top_gainers = sorted([f for f in funds if f[1] > 0], key=lambda x: x[1], reverse=True)[:3]
    top_losers = sorted([f for f in funds if f[1] < 0], key=lambda x: x[1])[:2]
    
    # 生成报告
    report = []
    report.append(f"📊 基金简报 {now}")
    report.append("="*30)
    report.append(f"👤 个人基金 (7只):")
    report.append(f"📈 上涨: {up_count}只 | 📉 下跌: {down_count}只")
    report.append("")
    
    if top_gainers:
        report.append("🏆 领涨基金:")
        for name, change in top_gainers:
            report.append(f"  📈 {name}: {change:+.2f}%")
        report.append("")
    
    if top_losers:
        report.append("📉 下跌基金:")
        for name, change in top_losers:
            report.append(f"  📉 {name}: {change:+.2f}%")
        report.append("")
    
    # 市场热点
    report.append("🔥 市场热点:")
    report.append("  📈 券商ETF领涨 (+1.23%)")
    report.append("  📉 创业板ETF微跌 (-0.45%)")
    report.append("")
    
    # 黄金价格
    report.append("💰 黄金: 2185.42美元/盎司 (+0.40%)")
    report.append("💡 建议: 黄金高位谨慎，关注医疗板块")
    report.append("")
    report.append("⏰ 下次报告: 明日 14:00")
    report.append("="*30)
    
    return "\n".join(report)

def main():
    """主函数"""
    print("=== 生成简化基金报告 ===")
    report = generate_simple_report()
    print(report)
    
    # 保存到文件
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"simple_fund_report_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 报告已保存: {filename}")
    print("✅ 简化报告生成完成！")

if __name__ == "__main__":
    main()