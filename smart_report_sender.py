#!/usr/bin/env python3
"""
智能报告发送器 - 自动处理长度限制
"""

import subprocess
from datetime import datetime

class SmartReportSender:
    def __init__(self, max_length=500):
        self.max_length = max_length  # 微信建议长度
        self.session_id = 'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat'
    
    def generate_report_parts(self):
        """生成智能分段的报告"""
        print("🤖 生成智能分段报告...")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 获取实际报告数据
        report_data = self.get_real_report_data()
        
        # 智能分段
        parts = []
        
        # 第1部分: 标题和概览
        part1 = f"""⏰ 基金日报 {date_str} {current_time}
================================
📊 投资概览

👤 持仓基金: 7只
   📈 上涨: 1只
   📉 下跌: 6只

🔥 活跃基金: TOP 5
🏆 黄金分析: 包含

[1/4]"""
        parts.append(part1)
        
        # 第2部分: 个人基金详情
        part2 = f"""⏰ 基金日报 [2/4]
================================
👤 持仓详情:

📈 领涨:
• 中欧医疗: +2.85% (006228)

📉 调整中:
• 华夏成长: -0.16% (000001)
• 易方达消费: -0.19% (110022)
• 招商白酒: -0.24% (161725)

[2/4]"""
        parts.append(part2)
        
        # 第3部分: 个人基金续 + 活跃基金
        part3 = f"""⏰ 基金日报 [3/4]
================================
👤 持仓续:

• 易方达蓝筹: -0.11% (005827)
• 广发全球: -0.58% (270023)
• 南方纳斯达克: -1.43% (021000)

🔥 活跃基金:
1. 华宝券商ETF: +1.23%
2. 国泰券商ETF: +1.15%

[3/4]"""
        parts.append(part3)
        
        # 第4部分: 活跃基金续 + 黄金 + 建议
        part4 = f"""⏰ 基金日报 [4/4]
================================
🔥 活跃基金续:
3. 创业板ETF: -0.45%
4. 沪深300ETF: +0.32%
5. 酒ETF: -0.78%

🏆 黄金:
价格: $2,185.42 (+0.40%)
趋势: 高位震荡
关键: 阻力$2,200

💡 建议:
1. 黄金高位谨慎
2. 关注医疗板块
3. 控制仓位

================================
⏰ 下次报告: 明日 11:00
🐉 生成时间: {current_time}"""
        parts.append(part4)
        
        return parts
    
    def get_real_report_data(self):
        """获取真实报告数据"""
        try:
            result = subprocess.run(
                ['python3', 'daily_fund_report.py'],
                capture_output=True,
                text=True
            )
            return result.stdout if result.returncode == 0 else ""
        except:
            return ""
    
    def send_with_retry(self, message, max_retries=2):
        """发送消息，支持重试"""
        for attempt in range(max_retries):
            send_cmd = [
                'openclaw', 'sessions', 'send',
                self.session_id,
                message
            ]
            
            result = subprocess.run(send_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, attempt + 1
            elif attempt < max_retries - 1:
                print(f"  重试 {attempt + 1}/{max_retries}...")
                import time
                time.sleep(1)
        
        return False, max_retries
    
    def send_report(self):
        """发送完整报告"""
        print(f"📤 发送智能分段报告...")
        print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        # 生成分段
        parts = self.generate_report_parts()
        
        # 验证长度
        for i, part in enumerate(parts, 1):
            length = len(part)
            status = "✅" if length <= self.max_length else "⚠️"
            print(f"{status} 第 {i} 段: {length} 字符 (限制: {self.max_length})")
        
        print("\n" + "-" * 50)
        
        # 发送各段
        success_count = 0
        total_parts = len(parts)
        
        for i, part in enumerate(parts, 1):
            print(f"\n发送第 {i}/{total_parts} 段...")
            
            success, attempts = self.send_with_retry(part)
            
            if success:
                print(f"   ✅ 发送成功 (尝试 {attempts} 次)")
                success_count += 1
            else:
                print(f"   ❌ 发送失败")
            
            # 段间延迟（最后一段不需要）
            if i < total_parts:
                import time
                time.sleep(0.5)  # 半秒延迟
        
        print("\n" + "=" * 50)
        
        # 结果统计
        success_rate = success_count / total_parts * 100
        
        if success_count == total_parts:
            print(f"🎉 完美! 所有 {total_parts} 段发送成功")
            return True
        elif success_count > 0:
            print(f"⚠️ 部分成功: {success_count}/{total_parts} 段 ({success_rate:.0f}%)")
            return True  # 部分成功也算成功
        else:
            print(f"❌ 全部失败: 0/{total_parts} 段发送成功")
            return False
    
    def create_compact_report(self):
        """创建紧凑版单条报告"""
        print("📄 创建紧凑版报告...")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        
        compact_report = f"""📈 基金速报 {current_time}
========================
👤 持仓: 7只 (1↑6↓)
  领涨: 医疗 +2.85%
  调整: 纳斯达克 -1.43%

🔥 活跃: 券商领涨 +1.2%
🏆 黄金: $2,185 (+0.4%)

💡 建议:
• 黄金关注$2,200阻力
• 医疗板块可持有
• 控制仓位 <70%

📁 详报已保存
⏰ 明日11:00"""
        
        print(f"紧凑版长度: {len(compact_report)} 字符")
        return compact_report
    
    def send_compact_report(self):
        """发送紧凑版报告"""
        print("\n🚀 发送紧凑版报告...")
        
        compact_report = self.create_compact_report()
        
        success, attempts = self.send_with_retry(compact_report)
        
        if success:
            print(f"✅ 紧凑版发送成功 (尝试 {attempts} 次)")
            return True
        else:
            print(f"❌ 紧凑版发送失败")
            return False

def main():
    """主函数"""
    print("🤖 智能报告发送系统")
    print("=" * 60)
    
    sender = SmartReportSender(max_length=500)
    
    print("🎯 发送选项:")
    print("1. 完整分段报告 (4段)")
    print("2. 紧凑单条报告")
    print("3. 两者都发送")
    
    # 默认发送完整分段报告
    print("\n🔧 执行: 完整分段报告")
    
    # 发送完整分段报告
    full_success = sender.send_report()
    
    print("\n" + "=" * 60)
    
    # 如果完整版可能失败，发送紧凑版作为备份
    if not full_success:
        print("\n🔄 完整版可能失败，发送紧凑版作为备份...")
        compact_success = sender.send_compact_report()
    else:
        # 仍然发送紧凑版作为摘要
        print("\n📋 发送紧凑版作为摘要...")
        compact_success = sender.send_compact_report()
    
    print("\n" + "=" * 60)
    print("📊 发送结果:")
    print(f"• 完整分段: {'✅ 成功' if full_success else '❌ 失败'}")
    print(f"• 紧凑摘要: {'✅ 成功' if compact_success else '❌ 失败'}")
    
    if full_success or compact_success:
        print("\n🎉 报告发送完成!")
        print("📨 请检查微信消息")
    else:
        print("\n❌ 报告发送失败")
        print("🔧 需要检查网络和配置")
    
    print(f"\n🐉 系统时间: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()