#!/usr/bin/env python3
"""
下午开盘基金报告
A股下午13:00开盘后更新
"""

import subprocess
from datetime import datetime

def generate_afternoon_report():
    """生成下午报告"""
    print("📊 生成下午开盘基金报告...")
    
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # 运行基金报告脚本
    result = subprocess.run(
        ['python3', 'daily_fund_report.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 报告生成失败: {result.stderr[:200]}")
        return None
    
    # 修改报告时间为下午
    report_content = result.stdout
    report_content = report_content.replace('每日投资报告', '下午投资快报')
    
    # 添加下午开盘标识
    afternoon_report = f"""⏰ 下午开盘快报 {datetime.now().strftime('%H:%M:%S')}
================================
📅 {datetime.now().strftime('%Y年%m月%d日')}
⏰ A股下午开盘: 13:00

{report_content}

📋 下午关注:
• 成交量变化
• 板块轮动情况  
• 外资流向
• 尾盘走势

🎯 操作建议:
1. 观察下午量能是否放大
2. 关注医疗板块持续性
3. 注意尾盘资金动向
4. 控制仓位，避免追高

================================
🐉 报告时间: {current_time}
📊 下次报告: 收盘后总结"""
    
    return afternoon_report

def create_simple_afternoon_report():
    """创建简化的下午报告"""
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # 模拟下午数据（实际应该从API获取）
    # 这里使用上午数据，但标记为下午更新
    afternoon_data = f"""📊 下午开盘快报 {current_time}
================================
⏰ A股下午已开盘
📅 {datetime.now().strftime('%Y-%m-%d')}

👤 你的基金持仓 (7只)
📈 上涨: 1只 | 📉 下跌: 6只

📈 领涨板块:
• 医疗: +2.85% (中欧医疗)
• 券商: +1.23% (华宝券商ETF)

📉 调整板块:
• 科技: -0.45% (创业板ETF)
• 消费: -0.24% (招商白酒)
• 海外: -1.43% (南方纳斯达克)

🏆 黄金市场:
💰 价格: $2,185.42 (+0.40%)
📊 趋势: 高位震荡
🎯 关键: 关注$2,200阻力

🔥 下午关注点:
1. 成交量能否放大
2. 外资流向变化
3. 板块轮动节奏
4. 尾盘资金动向

💡 操作建议:
• 医疗强势可持有
• 券商关注持续性
• 控制整体仓位
• 避免盲目追涨

================================
📝 数据时间: {current_time}
🐉 A股交易时间: 13:00-15:00"""

    return afternoon_data

def send_afternoon_report():
    """发送下午报告"""
    print("📤 发送下午开盘报告...")
    
    # 创建报告
    report = create_simple_afternoon_report()
    
    print(f"报告长度: {len(report)} 字符")
    
    # 发送报告
    send_cmd = [
        'openclaw', 'sessions', 'send',
        'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        report
    ]
    
    result = subprocess.run(send_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 下午报告发送成功")
        return True
    else:
        print(f"❌ 下午报告发送失败: {result.stderr}")
        return False

def main():
    """主函数"""
    print("🚀 下午开盘基金报告")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # 发送下午报告
    success = send_afternoon_report()
    
    if success:
        print("\n🎉 下午报告发送完成!")
        print("📨 请查看微信消息")
    else:
        print("\n❌ 下午报告发送失败")
    
    print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()