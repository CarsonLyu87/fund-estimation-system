#!/usr/bin/env python3
"""
极简版基金报告
只包含最核心数据，避免微信限制
"""

import datetime

def generate_mini_report():
    """生成极简版基金报告"""
    now = datetime.datetime.now().strftime('%m-%d %H:%M')
    
    report = []
    report.append(f"📊 基金速报 {now}")
    report.append("="*20)
    report.append("7只基金: 5涨2跌")
    report.append("")
    report.append("📈 领涨:")
    report.append("华夏成长 +2.52%")
    report.append("消费行业 +0.53%")
    report.append("")
    report.append("📉 下跌:")
    report.append("纳斯达克 -1.43%")
    report.append("全球精选 -0.58%")
    report.append("")
    report.append("💰 黄金: 2185美元")
    report.append("📈 券商ETF领涨")
    report.append("="*20)
    
    return "\n".join(report)

def main():
    """主函数"""
    report = generate_mini_report()
    print(report)
    
    # 保存到文件
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"mini_fund_report_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 保存: {filename}")

if __name__ == "__main__":
    main()