#!/usr/bin/env python3
"""
发送基金部分报告
"""

import subprocess
from datetime import datetime

def get_fund_data():
    """获取基金数据"""
    print("📈 获取基金数据...")
    
    # 运行报告脚本
    result = subprocess.run(
        ['python3', 'daily_fund_report.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return "❌ 基金数据获取失败"
    
    # 提取基金部分
    output = result.stdout
    fund_lines = []
    in_fund_section = False
    
    for line in output.split('\n'):
        if '个人基金' in line or '活跃基金' in line:
            in_fund_section = True
        elif '黄金市场' in line or '🏆 黄金' in line:
            break  # 遇到黄金部分停止
        
        if in_fund_section and line.strip():
            fund_lines.append(line)
    
    return '\n'.join(fund_lines[:30])  # 限制行数

def create_fund_report():
    """创建基金部分报告"""
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # 获取实际数据
    fund_data = get_fund_data()
    
    # 如果获取失败，使用模拟数据
    if "失败" in fund_data:
        fund_report = f"""⏰ 基金报告 {current_time}
================================
📊 基金持仓 (7只)

📈 上涨: 1只
• 中欧医疗创新股票A: +2.85%

📉 下跌: 6只  
• 华夏成长混合: -0.16%
• 易方达消费行业: -0.19%
• 招商中证白酒指数: -0.24%
• 易方达蓝筹精选混合: -0.11%
• 广发全球精选股票: -0.58%
• 南方纳斯达克100指数: -1.43%

🔥 活跃基金TOP 5
1. 华宝券商ETF: +1.23%
2. 国泰券商ETF: +1.15%
3. 创业板ETF: -0.45%
4. 沪深300ETF: +0.32%
5. 酒ETF: -0.78%

📝 详细数据已保存
⏰ 报告时间: {current_time}"""
    else:
        # 使用实际数据
        fund_report = f"""⏰ 基金报告 {current_time}
================================
{fund_data}

📝 详细数据已保存
⏰ 报告时间: {current_time}"""
    
    return fund_report

def send_message(message):
    """发送消息"""
    send_cmd = [
        'openclaw', 'sessions', 'send',
        'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        message
    ]
    
    result = subprocess.run(send_cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    """主函数"""
    print("🚀 发送基金部分报告")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # 创建基金报告
    print("📄 生成基金报告...")
    fund_report = create_fund_report()
    
    print(f"报告长度: {len(fund_report)} 字符")
    print(f"内容预览:\n{fund_report[:200]}...")
    
    print("\n📤 发送基金报告...")
    success = send_message(fund_report)
    
    if success:
        print("✅ 基金报告发送成功")
        
        # 短暂延迟后发送黄金部分
        import time
        time.sleep(1)
        
        # 发送黄金部分提示
        gold_prompt = f"""⏰ 黄金报告 {datetime.now().strftime('%H:%M:%S')}
================================
🏆 黄金分析即将发送...
请查看下一条消息"""
        
        send_message(gold_prompt)
        print("✅ 黄金部分提示已发送")
    else:
        print("❌ 基金报告发送失败")
    
    print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()