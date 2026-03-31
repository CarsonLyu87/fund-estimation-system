#!/usr/bin/env python3
"""
改进版专注基金报告
使用真实基金数据，从天天基金网获取
"""

import json
import urllib.request
from datetime import datetime
import sys

def get_fund_data(fund_code):
    """获取基金数据"""
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            text = response.read().decode('utf-8')
            
            if 'jsonpgz(' in text:
                json_str = text[text.find('(')+1:text.rfind(')')]
                return json.loads(json_str)
        return None
    except Exception as e:
        print(f"获取基金{fund_code}数据失败: {e}")
        return None

def load_fund_config():
    """加载基金配置"""
    try:
        with open('fund_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('funds', [])
    except Exception as e:
        print(f"加载基金配置失败: {e}")
        # 默认基金列表
        return [
            {"code": "000001", "name": "华夏成长混合"},
            {"code": "110022", "name": "易方达消费行业"},
            {"code": "161725", "name": "招商中证白酒指数"},
            {"code": "021000", "name": "南方纳斯达克100指数"},
            {"code": "005827", "name": "易方达蓝筹精选混合"},
            {"code": "270023", "name": "广发全球精选股票(QDII)"},
            {"code": "006228", "name": "中欧医疗创新股票A"}
        ]

def generate_focused_report():
    """生成专注基金报告"""
    now = datetime.now().strftime('%m-%d %H:%M')
    
    # 加载基金配置
    funds = load_fund_config()
    
    # 获取基金数据
    fund_results = []
    up_count = 0
    down_count = 0
    
    print(f"📊 正在获取 {len(funds)} 只基金数据...")
    
    for fund in funds:
        code = fund["code"]
        name = fund["name"]
        
        data = get_fund_data(code)
        
        if data:
            gszzl = data.get('gszzl', '0.00')
            gztime = data.get('gztime', '未知时间')
            
            try:
                change = float(gszzl)
                if change > 0:
                    emoji = "📈"
                    up_count += 1
                elif change < 0:
                    emoji = "📉"
                    down_count += 1
                else:
                    emoji = "➡️"
                
                fund_results.append({
                    "name": name,
                    "change": change,
                    "emoji": emoji,
                    "time": gztime
                })
                
                print(f"  {emoji} {name}: {change:+.2f}% ({gztime})")
                
            except ValueError:
                print(f"  ❌ {name}: 数据格式错误 ({gszzl})")
                fund_results.append({
                    "name": name,
                    "change": 0.0,
                    "emoji": "❓",
                    "time": "数据错误"
                })
        else:
            print(f"  ❌ {name}: 获取数据失败")
            fund_results.append({
                "name": name,
                "change": 0.0,
                "emoji": "❌",
                "time": "获取失败"
            })
    
    # 生成报告
    report = []
    report.append(f"📊 专注基金报告 {now}")
    report.append("="*40)
    report.append(f"📈 上涨: {up_count}只 | 📉 下跌: {down_count}只 | ➡️ 平盘: {len(funds)-up_count-down_count}只")
    report.append("")
    
    # 按涨跌幅排序
    sorted_funds = sorted(fund_results, key=lambda x: x["change"], reverse=True)
    
    for fund in sorted_funds:
        if fund["change"] > 0:
            report.append(f"{fund['emoji']} {fund['name']}: +{fund['change']:.2f}%")
        elif fund["change"] < 0:
            report.append(f"{fund['emoji']} {fund['name']}: {fund['change']:.2f}%")
        else:
            report.append(f"{fund['emoji']} {fund['name']}: {fund['change']:.2f}%")
    
    report.append("")
    report.append("📊 市场概览:")
    if up_count > down_count:
        report.append("  ✅ 整体偏强，上涨基金居多")
    elif down_count > up_count:
        report.append("  ⚠️ 整体偏弱，下跌基金居多")
    else:
        report.append("  ⚖️ 多空平衡，涨跌互现")
    
    # 找出领涨和领跌
    if sorted_funds:
        top_gainer = sorted_funds[0]
        top_loser = sorted_funds[-1] if sorted_funds[-1]["change"] < 0 else None
        
        report.append("")
        report.append("🏆 今日表现:")
        report.append(f"  领涨: {top_gainer['name']} ({top_gainer['change']:+.2f}%)")
        if top_loser:
            report.append(f"  领跌: {top_loser['name']} ({top_loser['change']:+.2f}%)")
    
    report.append("")
    report.append("⏰ 数据时间: " + (sorted_funds[0]["time"] if sorted_funds else "未知"))
    report.append("="*40)
    
    return "\n".join(report)

def main():
    """主函数"""
    print("=== 生成专注基金报告（真实数据） ===")
    
    try:
        report = generate_focused_report()
        print("\n" + report)
        
        # 保存到文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"focused_fund_report_real_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 更新最新报告文件
        with open("latest_focused_report.txt", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📁 报告已保存: {filename}")
        print("📝 最新报告已更新: latest_focused_report.txt")
        print("✅ 专注基金报告生成完成！")
        
        return report
        
    except Exception as e:
        error_msg = f"❌ 生成报告失败: {e}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    main()