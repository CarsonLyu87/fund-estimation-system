#!/usr/bin/env python3
"""
基金实时涨跌幅估算 - 主运行脚本
"""

import sys
import os
import json
from datetime import datetime

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from estimator import TiantianEastmoneyEstimator

def load_config():
    """加载配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'funds.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  配置文件不存在: {config_path}")
        print("使用默认配置...")
        return {
            "funds": [
                {
                    "code": "006228",
                    "name": "中欧医疗创新股票A",
                    "type": "医疗",
                    "priority": 1
                },
                {
                    "code": "005827",
                    "name": "易方达蓝筹精选混合",
                    "type": "蓝筹",
                    "priority": 2
                },
                {
                    "code": "161725",
                    "name": "招商中证白酒指数",
                    "type": "白酒",
                    "priority": 3
                }
            ]
        }

def generate_report(results, config):
    """生成报告"""
    report = []
    report.append("="*70)
    report.append("📊 基金实时涨跌幅估算报告")
    report.append(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*70)
    report.append("")
    
    # 总体概览
    total_funds = len(results)
    up_count = sum(1 for r in results if r.estimated_change > 0)
    down_count = sum(1 for r in results if r.estimated_change < 0)
    
    report.append("📈 总体概览:")
    report.append(f"   监控基金: {total_funds} 只")
    report.append(f"   预计上涨: {up_count} 只")
    report.append(f"   预计下跌: {down_count} 只")
    report.append(f"   预计平盘: {total_funds - up_count - down_count} 只")
    report.append("")
    
    # 各基金详情
    report.append("🏆 各基金估算结果:")
    report.append("-"*50)
    
    # 按涨跌幅绝对值排序
    sorted_results = sorted(results, key=lambda x: abs(x.estimated_change), reverse=True)
    
    for result in sorted_results:
        change = result.estimated_change
        emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        
        report.append(f"{emoji} {result.fund_name} ({result.fund_code})")
        report.append(f"   估算涨跌: {change:+.4f}%")
        report.append(f"   股票仓位: {result.stock_weight:.1f}%")
        report.append(f"   现金仓位: {result.cash_weight:.1f}%")
        report.append(f"   数据质量: {result.data_quality}")
        report.append(f"   估算时间: {result.estimation_time}")
        
        # 显示主要贡献
        if result.contributions:
            report.append("   主要贡献股票:")
            for i, contrib in enumerate(result.contributions[:3], 1):
                sign = "+" if contrib['contribution'] > 0 else ""
                report.append(f"     {i}. {contrib['stock']}: {sign}{contrib['contribution']:.4f}%")
        
        report.append("")
    
    # 数据源说明
    report.append("📝 数据源说明:")
    report.append("   • 基金持仓: 天天基金网 (最新季报数据)")
    report.append("   • 股票数据: 东方财富网/新浪财经 (实时行情)")
    report.append("   • 估算方法: ∑(持仓权重 × 股票实时涨跌)")
    report.append("")
    
    # 注意事项
    report.append("⚠️  注意事项:")
    report.append("   1. 持仓数据基于最新季报，可能已调仓")
    report.append("   2. 实时估算存在误差，仅供参考")
    report.append("   3. 现金仓位假设收益为0")
    report.append("   4. 最终以基金公司官方净值为准")
    report.append("")
    
    # 投资建议
    report.append("💡 投资建议:")
    if up_count > down_count:
        report.append("   市场情绪偏积极，可关注上涨基金")
    elif down_count > up_count:
        report.append("   市场情绪偏谨慎，注意风险控制")
    else:
        report.append("   市场分化明显，精选个股更重要")
    
    report.append("="*70)
    
    return "\n".join(report)

def save_report(report_text):
    """保存报告到文件"""
    # 创建reports目录
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # 保存带时间戳的报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"fund_estimation_{timestamp}.txt"
    filepath = os.path.join(reports_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    # 保存为最新报告
    latest_path = os.path.join(reports_dir, "latest_fund_estimation.txt")
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return filepath, latest_path

def main():
    """主函数"""
    print("🚀 基金实时涨跌幅估算系统")
    print("="*70)
    
    # 加载配置
    config = load_config()
    funds = config.get('funds', [])
    
    print(f"📋 监控基金: {len(funds)} 只")
    for fund in funds:
        print(f"   • {fund['name']} ({fund['code']})")
    print()
    
    # 创建估算器
    estimator_config = {
        'max_holdings': 10,
        'cash_return_rate': 0.0,
        'request_interval': 0.05,
        'cache_ttl': 300
    }
    
    estimator = TiantianEastmoneyEstimator(estimator_config)
    
    # 估算所有基金
    results = []
    for fund in funds:
        try:
            print(f"📊 估算 {fund['name']} ({fund['code']})...")
            result = estimator.estimate_fund(fund['code'], fund['name'])
            results.append(result)
            print(f"   ✅ 完成: {result.estimated_change:+.4f}%")
        except Exception as e:
            print(f"   ❌ 失败: {e}")
            continue
    
    if not results:
        print("❌ 所有基金估算都失败了")
        return 1
    
    # 生成报告
    print("\n📝 生成报告...")
    report = generate_report(results, config)
    print(report)
    
    # 保存报告
    filepath, latest_path = save_report(report)
    print(f"\n📁 报告已保存:")
    print(f"   • 详细报告: {filepath}")
    print(f"   • 最新报告: {latest_path}")
    
    print("\n✅ 估算完成!")
    print("="*70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())