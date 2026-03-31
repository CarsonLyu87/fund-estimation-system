#!/usr/bin/env python3
"""
简单格式基金报告 - 按照持仓截图格式
"""

import subprocess
from datetime import datetime

def get_fund_data():
    """获取基金数据"""
    result = subprocess.run(
        ['python3', 'daily_fund_report.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return None
    
    return result.stdout

def parse_fund_data(report_content):
    """解析基金数据"""
    lines = report_content.split('\n')
    
    personal_funds = []
    active_funds = []
    gold_info = ""
    
    current_section = None
    
    for line in lines:
        if '👤 你的基金持仓' in line or '个人基金' in line:
            current_section = 'personal'
        elif '🔥 市场最活跃基金' in line or '活跃基金' in line:
            current_section = 'active'
        elif '🏆 黄金市场' in line or '黄金市场分析' in line:
            current_section = 'gold'
        elif '💰 价格:' in line and current_section == 'gold':
            gold_info = line.replace('💰 价格:', '').strip()
        
        # 收集个人基金
        if current_section == 'personal' and ('📈' in line or '📉' in line) and '%' in line:
            personal_funds.append(line.strip())
        
        # 收集活跃基金
        if current_section == 'active' and ('📈' in line or '📉' in line) and '%' in line:
            active_funds.append(line.strip())
    
    return personal_funds, active_funds, gold_info

def create_simple_report():
    """创建简单格式报告"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 获取数据
    report_content = get_fund_data()
    if not report_content:
        return ["❌ 无法获取基金数据"]
    
    personal_funds, active_funds, gold_info = parse_fund_data(report_content)
    
    # 创建报告部分
    parts = []
    
    # 第1部分: 标题和个人基金前4只
    part1 = f"""📊 基金持仓报告
⏰ {current_time}
=======================

👤 你的持仓 ({len(personal_funds)}只)"""
    
    for i, fund in enumerate(personal_funds[:4], 1):
        # 简化格式
        fund_line = fund.replace('📈 ', '').replace('📉 ', '')
        parts_info = fund_line.split(':')
        if len(parts_info) >= 2:
            name_code = parts_info[0].strip()
            change = parts_info[1].strip()
            
            # 提取名称和代码
            if '(' in name_code and ')' in name_code:
                name = name_code.split('(')[0].strip()
                code = name_code.split('(')[1].replace(')', '').strip()
            else:
                name = name_code
                code = ""
            
            trend = '📈' if '📈' in fund else '📉'
            part1 += f"\n\n{i}. {name}"
            if code:
                part1 += f"\n   代码: {code}"
            part1 += f"\n   涨跌: {change} {trend}"
    
    part1 += "\n\n[1/3] 继续..."
    parts.append(part1)
    
    # 第2部分: 个人基金续和统计
    part2 = f"""📊 基金持仓报告 [2/3]
======================="""
    
    # 继续个人基金
    start_idx = 4
    for i, fund in enumerate(personal_funds[start_idx:], start_idx + 1):
        fund_line = fund.replace('📈 ', '').replace('📉 ', '')
        parts_info = fund_line.split(':')
        if len(parts_info) >= 2:
            name_code = parts_info[0].strip()
            change = parts_info[1].strip()
            
            if '(' in name_code and ')' in name_code:
                name = name_code.split('(')[0].strip()
                code = name_code.split('(')[1].replace(')', '').strip()
            else:
                name = name_code
                code = ""
            
            trend = '📈' if '📈' in fund else '📉'
            part2 += f"\n\n{i}. {name}"
            if code:
                part2 += f"\n   代码: {code}"
            part2 += f"\n   涨跌: {change} {trend}"
    
    # 统计信息
    up_count = sum(1 for f in personal_funds if '📈' in f)
    down_count = sum(1 for f in personal_funds if '📉' in f)
    
    part2 += f"\n\n📈 持仓统计:"
    part2 += f"\n• 总数量: {len(personal_funds)}只"
    part2 += f"\n• 上涨: {up_count}只 ({up_count/len(personal_funds)*100:.1f}%)"
    part2 += f"\n• 下跌: {down_count}只 ({down_count/len(personal_funds)*100:.1f}%)"
    
    # 找出领涨领跌
    if personal_funds:
        changes = []
        for fund in personal_funds:
            if '%' in fund:
                try:
                    change_str = fund.split(':')[1].strip().replace('%', '').replace('+', '').replace('-', '')
                    change_val = float(change_str)
                    if '📉' in fund:
                        change_val = -change_val
                    changes.append((fund, change_val))
                except:
                    pass
        
        if changes:
            changes.sort(key=lambda x: x[1], reverse=True)
            top_gain = changes[0]
            top_loss = changes[-1] if changes[-1][1] < 0 else None
            
            # 提取名称
            top_gain_name = top_gain[0].split(':')[0].replace('📈 ', '').replace('📉 ', '').split('(')[0].strip()
            part2 += f"\n• 领涨: {top_gain_name} {top_gain[1]:+.2f}%"
            
            if top_loss:
                top_loss_name = top_loss[0].split(':')[0].replace('📈 ', '').replace('📉 ', '').split('(')[0].strip()
                part2 += f"\n• 领跌: {top_loss_name} {top_loss[1]:+.2f}%"
    
    part2 += "\n\n[2/3] 继续..."
    parts.append(part2)
    
    # 第3部分: 活跃基金和黄金
    part3 = f"""📊 基金持仓报告 [3/3]
=======================

🔥 市场活跃基金:"""
    
    for i, fund in enumerate(active_funds[:5], 1):
        fund_line = fund.replace('📈 ', '').replace('📉 ', '')
        parts_info = fund_line.split(':')
        if len(parts_info) >= 2:
            name_code = parts_info[0].strip()
            change = parts_info[1].strip()
            
            if '(' in name_code and ')' in name_code:
                name = name_code.split('(')[0].strip()
                code = name_code.split('(')[1].replace(')', '').strip()
            else:
                name = name_code
                code = ""
            
            trend = '📈' if '📈' in fund else '📉'
            part3 += f"\n\n{i}. {name}"
            if code:
                part3 += f"\n   代码: {code}"
            part3 += f"\n   涨跌: {change} {trend}"
    
    # 黄金信息
    if gold_info:
        part3 += f"\n\n🏆 黄金: {gold_info}"
        part3 += f"\n📈 趋势: 高位震荡"
        part3 += f"\n🎯 关键: 阻力$2,200"
    
    part3 += f"\n\n======================="
    part3 += f"\n📝 报告时间: {datetime.now().strftime('%H:%M:%S')}"
    part3 += f"\n🐉 下次报告: 明日 11:00"
    
    parts.append(part3)
    
    return parts

def send_report_parts(parts):
    """发送报告部分"""
    for i, part in enumerate(parts, 1):
        print(f"发送第 {i}/{len(parts)} 部分...")
        
        send_cmd = [
            'openclaw', 'sessions', 'send',
            'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
            part
        ]
        
        result = subprocess.run(send_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ 第 {i} 部分发送失败: {result.stderr}")
            return False
        
        print(f"✅ 第 {i} 部分发送成功")
        
        # 部分之间短暂延迟
        if i < len(parts):
            import time
            time.sleep(0.5)
    
    return True

def main():
    """主函数"""
    print("📊 生成简单格式基金报告")
    print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)
    
    # 创建报告
    parts = create_simple_report()
    
    print(f"生成 {len(parts)} 部分报告")
    for i, part in enumerate(parts, 1):
        print(f"  第 {i} 部分: {len(part)} 字符")
    
    print("\n📤 发送报告...")
    success = send_report_parts(parts)
    
    if success:
        print(f"\n🎉 报告发送完成!")
        print(f"📨 共发送 {len(parts)} 部分")
    else:
        print(f"\n❌ 报告发送失败")
    
    print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()