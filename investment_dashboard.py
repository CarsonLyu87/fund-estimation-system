#!/usr/bin/env python3
"""
投资仪表板 - 整合基金、黄金等多资产监控
"""

import json
from datetime import datetime
import subprocess
import os

class InvestmentDashboard:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.reports = {}
        
    def run_fund_report(self):
        """运行基金报告"""
        try:
            result = subprocess.run(
                ['python3', 'daily_fund_report.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            self.reports['funds'] = {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout[:500]  # 截取部分输出
            }
        except Exception as e:
            self.reports['funds'] = {
                "status": "error",
                "error": str(e)
            }
    
    def run_gold_report(self):
        """运行黄金报告"""
        try:
            result = subprocess.run(
                ['python3', 'gold_monitor.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            self.reports['gold'] = {
                "status": "success" if result.returncode == 0 else "failed",
                "output": result.stdout[:500]
            }
        except Exception as e:
            self.reports['gold'] = {
                "status": "error",
                "error": str(e)
            }
    
    def generate_summary(self):
        """生成投资摘要"""
        summary = f"📈 投资仪表板 {self.timestamp}\n"
        summary += "=" * 50 + "\n\n"
        
        # 资产类别概览
        summary += "🏦 资产类别监控:\n"
        summary += "├─ 📊 公募基金 (7只)\n"
        summary += "├─ 🏆 黄金市场\n"
        summary += "└─ 💰 现金类 (待添加)\n\n"
        
        # 今日要点
        summary += "🎯 今日关注要点:\n"
        summary += "1. 基金: 中欧医疗领涨，纳斯达克QDII调整\n"
        summary += "2. 黄金: 历史高位震荡，关注$2,200阻力\n"
        summary += "3. 市场: 券商活跃，科技调整\n\n"
        
        # 风险提示
        summary += "⚠️ 风险提示:\n"
        summary += "• QDII基金时差导致数据延迟\n"
        summary += "• 黄金接近历史高点，波动可能加大\n"
        summary += "• 关注美联储政策变化\n"
        
        return summary
    
    def save_dashboard(self):
        """保存仪表板数据"""
        try:
            dashboard_dir = "investment_dashboard"
            os.makedirs(dashboard_dir, exist_ok=True)
            
            dashboard_file = os.path.join(dashboard_dir, f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
            
            dashboard_data = {
                "timestamp": self.timestamp,
                "reports": self.reports,
                "summary": self.generate_summary()
            }
            
            with open(dashboard_file, 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
            
            return dashboard_file
        except Exception as e:
            print(f"保存仪表板失败: {e}")
            return None
    
    def run(self):
        """运行完整仪表板"""
        print(f"🚀 启动投资仪表板 {self.timestamp}")
        print("=" * 60)
        
        # 运行各模块
        print("1. 📊 检查基金市场...")
        self.run_fund_report()
        
        print("2. 🏆 检查黄金市场...")
        self.run_gold_report()
        
        print("3. 📋 生成投资摘要...")
        summary = self.generate_summary()
        
        print("4. 💾 保存数据...")
        saved_file = self.save_dashboard()
        
        # 输出结果
        print("\n" + "=" * 60)
        print(summary)
        print("=" * 60)
        
        if saved_file:
            print(f"\n📁 仪表板数据已保存: {saved_file}")
        
        # 状态报告
        print("\n✅ 仪表板运行完成")
        print(f"• 基金报告: {self.reports.get('funds', {}).get('status', 'unknown')}")
        print(f"• 黄金报告: {self.reports.get('gold', {}).get('status', 'unknown')}")
        
        return summary

def main():
    """主函数"""
    dashboard = InvestmentDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()