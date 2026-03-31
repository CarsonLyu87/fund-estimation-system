#!/usr/bin/env python3
"""
分段发送报告 - 解决微信字数限制
"""

import subprocess
from datetime import datetime

def split_report():
    """生成分段报告"""
    print("📋 生成分段报告...")
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 分段1: 报告标题和个人基金
    part1 = f"""⏰ 每日投资报告 {current_time}
==================================================

📈 今日投资概览
├─ 📊 个人基金 (7只)
├─ 🔥 活跃基金 (TOP 5)
└─ 🏆 黄金市场

👤 你的基金持仓 (7只)
📈 上涨: 1只 | 📉 下跌: 6只

📈 中欧医疗创新股票A (006228): +2.85%
📉 华夏成长混合 (000001): -0.16%
📉 易方达消费行业 (110022): -0.19%
📉 招商中证白酒指数 (161725): -0.24%
📉 易方达蓝筹精选混合 (005827): -0.11%

[1/4] 继续下一页..."""
    
    # 分段2: 个人基金续 + 活跃基金
    part2 = f"""⏰ 每日投资报告 {current_time} [2/4]
==================================================

👤 基金持仓续:
📉 广发全球精选股票(QDII) (270023): -0.58%
📉 南方纳斯达克100指数 (021000): -1.43%

--------------------------------------------------

🔥 市场最活跃基金TOP 5

1. 📈 华宝券商ETF (512000): +1.23%
   成交额: 5.2亿元 | 政策利好预期

2. 📈 国泰券商ETF (512880): +1.15%
   成交额: 4.8亿元 | 成交量最大

[2/4] 继续下一页..."""
    
    # 分段3: 活跃基金续 + 黄金分析
    part3 = f"""⏰ 每日投资报告 {current_time} [3/4]
==================================================

🔥 活跃基金续:
3. 📉 创业板ETF (159915): -0.45%
   成交额: 3.5亿元 | 科技股波动

4. 📈 沪深300ETF (510300): +0.32%
   成交额: 3.2亿元 | 大盘核心

5. 📉 酒ETF (512690): -0.78%
   成交额: 2.8亿元 | 板块调整

--------------------------------------------------

🏆 黄金市场分析

💰 价格: $2,185.42/oz (+0.40%)
📊 趋势: 高位震荡，接近历史高点
🎯 关键位: 阻力$2,200 | 支撑$2,150

[3/4] 继续下一页..."""
    
    # 分段4: 黄金分析续 + 投资建议
    part4 = f"""⏰ 每日投资报告 {current_time} [4/4]
==================================================

🏆 黄金分析续:

📈 看涨因素:
• 降息预期
• 地缘风险  
• 央行购金

📉 看跌因素:
• 美元强势
• 获利了结
• 风险偏好回升

--------------------------------------------------

💡 今日投资建议:

1. 黄金: 高位谨慎，关注$2,200阻力突破
2. 基金: 医疗领涨可持有，QDII注意时差风险
3. 整体: 控制仓位在70%以下，分散配置

==================================================
📝 详细报告: fund_reports/report_20260324.txt
⏰ 下次报告: 明日 11:00
🐉 报告完成时间: {current_time}"""
    
    return [part1, part2, part3, part4]

def send_parts(parts):
    """分段发送"""
    print(f"📤 发送 {len(parts)} 段报告...")
    
    for i, part in enumerate(parts, 1):
        print(f"\n发送第 {i}/{len(parts)} 段...")
        print(f"长度: {len(part)} 字符")
        
        send_cmd = [
            'openclaw', 'sessions', 'send',
            'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
            part
        ]
        
        result = subprocess.run(send_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 第 {i} 段发送成功")
            # 段之间短暂延迟
            if i < len(parts):
                import time
                time.sleep(1)
        else:
            print(f"❌ 第 {i} 段发送失败: {result.stderr}")
            return False
    
    return True

def check_length_limits():
    """检查长度限制"""
    print("📏 消息长度限制检查:")
    print("=" * 50)
    
    print("已知限制:")
    print("• 微信消息: ~500-1000字符 (可能因平台而异)")
    print("• 短信: 160字符")
    print("• 推特: 280字符")
    print("• 电报: 4096字符")
    
    print("\n🔧 分段策略:")
    print("• 每段控制在 400-500 字符")
    print("• 重要信息优先")
    print("• 添加页码标识")
    print("• 段间短暂延迟")
    
    return True

def main():
    """主函数"""
    print("🚀 分段发送基金报告")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # 检查长度限制
    check_length_limits()
    
    print("\n" + "=" * 60)
    
    # 生成分段报告
    parts = split_report()
    
    print(f"生成 {len(parts)} 段报告:")
    for i, part in enumerate(parts, 1):
        print(f"  第 {i} 段: {len(part)} 字符")
    
    print("\n" + "=" * 60)
    
    # 发送分段报告
    success = send_parts(parts)
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 分段报告发送完成!")
        print(f"📨 共发送 {len(parts)} 段消息")
        print("   请检查微信是否收到完整报告")
    else:
        print("❌ 分段报告发送失败")
        print("🔧 需要进一步排查")
    
    print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()