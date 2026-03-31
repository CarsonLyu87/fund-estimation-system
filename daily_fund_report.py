#!/usr/bin/env python3
"""
每日投资报告脚本
整合：个人基金 + 活跃基金 + 黄金分析
"""

import json
import os
from datetime import datetime
import urllib.request
import urllib.error

# ==================== 黄金分析部分 ====================

def get_gold_analysis():
    """获取黄金分析数据"""
    try:
        current_time = datetime.now().strftime('%H:%M')
        
        # 模拟黄金数据（实际可接入API）
        gold_data = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "prices": {
                "international": 2185.42,
                "domestic": 522.35,
                "change": "+0.40%",
                "high": 2190.15,
                "low": 2175.30
            },
            "analysis": {
                "trend": "高位震荡",
                "key_resistance": 2200,
                "key_support": 2150,
                "sentiment": "谨慎乐观",
                "position": "历史高点附近"
            },
            "factors": {
                "bullish": ["降息预期", "地缘风险", "央行购金"],
                "bearish": ["美元强势", "获利了结"]
            },
            "scenarios": [
                {"name": "突破上行", "probability": "40%", "target": "2250-2300"},
                {"name": "高位震荡", "probability": "50%", "range": "2100-2200"},
                {"name": "技术回调", "probability": "10%", "target": "2000-2100"}
            ]
        }
        
        return gold_data
    except Exception as e:
        print(f"获取黄金分析失败: {e}")
        return None

def format_gold_section(gold_data):
    """格式化黄金分析部分"""
    if not gold_data:
        return "🏆 黄金分析: 数据暂不可用\n"
    
    section = "🏆 黄金市场分析\n"
    section += "=" * 40 + "\n\n"
    
    # 价格信息
    prices = gold_data["prices"]
    section += f"💰 价格: ${prices['international']:.2f}/oz ({prices['change']})\n"
    section += f"   区间: ${prices['low']:.2f}-${prices['high']:.2f}\n"
    section += f"   国内: {prices['domestic']}元/克\n\n"
    
    # 技术分析
    analysis = gold_data["analysis"]
    section += f"📊 技术面: {analysis['trend']}\n"
    section += f"   阻力: ${analysis['key_resistance']} | 支撑: ${analysis['key_support']}\n"
    section += f"   位置: {analysis['position']}\n"
    section += f"   情绪: {analysis['sentiment']}\n\n"
    
    # 情景分析
    section += "🎯 情景分析:\n"
    for scenario in gold_data["scenarios"]:
        prob = scenario["probability"]
        if "突破" in scenario["name"]:
            emoji = "🚀"
        elif "震荡" in scenario["name"]:
            emoji = "➡️"
        else:
            emoji = "📉"
        
        if "target" in scenario:
            section += f"  {emoji} {scenario['name']} ({prob}): {scenario['target']}\n"
        else:
            section += f"  {emoji} {scenario['name']} ({prob}): {scenario['range']}\n"
    
    # 影响因素
    factors = gold_data["factors"]
    section += "\n📈 看涨因素: " + ", ".join(factors["bullish"][:2]) + "\n"
    section += "📉 看跌因素: " + ", ".join(factors["bearish"][:2]) + "\n"
    
    section += "\n" + "=" * 40 + "\n\n"
    
    return section

# ==================== 个人基金监控部分 ====================

def load_personal_funds():
    """加载个人基金配置"""
    config_file = "fund_config.json"
    default_funds = [
        {"code": "000001", "name": "华夏成长混合"},
        {"code": "110022", "name": "易方达消费行业"},
        {"code": "161725", "name": "招商中证白酒指数"}
    ]
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("funds", default_funds)
    except Exception as e:
        print(f"加载个人基金配置失败: {e}")
    
    return default_funds

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

def check_personal_funds():
    """检查个人基金"""
    print("📊 正在检查个人基金...")
    funds = load_personal_funds()
    
    results = []
    up_count = 0
    down_count = 0
    
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
            except:
                emoji = "❓"
            
            result = f"{emoji} {name}: {gszzl}%"
            results.append(result)
        else:
            result = f"❌ {name}: 数据获取失败"
            results.append(result)
    
    # 生成个人基金报告
    personal_report = f"👤 个人基金 ({len(funds)}只):\n"
    personal_report += f"📈 上涨: {up_count}只 | 📉 下跌: {down_count}只\n\n"
    
    for result in results:
        personal_report += f"  {result}\n"
    
    return personal_report

# ==================== 活跃基金部分 ====================

def get_active_funds():
    """获取活跃基金数据"""
    # 模拟数据 - 实际可替换为真实API
    active_funds = [
        {"code": "512000", "name": "华宝券商ETF", "amount": "5.2亿", "change": "+1.23%", "reason": "政策利好"},
        {"code": "512880", "name": "国泰券商ETF", "amount": "4.8亿", "change": "+1.15%", "reason": "成交量最大"},
        {"code": "159915", "name": "创业板ETF", "amount": "3.5亿", "change": "-0.45%", "reason": "科技股波动"},
        {"code": "510300", "name": "沪深300ETF", "amount": "3.2亿", "change": "+0.32%", "reason": "大盘核心"},
        {"code": "512690", "name": "酒ETF", "amount": "2.8亿", "change": "-0.78%", "reason": "板块调整"}
    ]
    return active_funds

def check_active_funds():
    """检查活跃基金"""
    print("🔥 正在获取活跃基金...")
    active_funds = get_active_funds()
    
    active_report = "🔥 市场最活跃基金TOP 5:\n\n"
    
    for i, fund in enumerate(active_funds[:5], 1):
        change = fund.get("change", "0%")
        if "+" in change:
            emoji = "📈"
        elif "-" in change:
            emoji = "📉"
        else:
            emoji = "➡️"
        
        active_report += f"{i}. {emoji} {fund['name']} ({fund['code']})\n"
        active_report += f"   成交额: {fund['amount']} | 涨跌: {change}\n"
        
        reason = fund.get("reason", "")
        if reason:
            active_report += f"   原因: {reason}\n"
        
        if i < 5:
            active_report += "\n"
    
    return active_report

# ==================== 主报告生成 ====================

def generate_daily_report():
    """生成每日投资报告"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"🐉 生成每日投资报告 {current_time}")
    print("=" * 60)
    
    # 获取各部分报告
    print("1. 检查个人基金...")
    personal_report = check_personal_funds()
    
    print("2. 检查活跃基金...")
    active_report = check_active_funds()
    
    print("3. 分析黄金市场...")
    gold_data = get_gold_analysis()
    gold_section = format_gold_section(gold_data)
    
    # 生成完整报告
    full_report = f"⏰ 每日投资报告 {current_time}\n"
    full_report += "=" * 50 + "\n\n"
    
    # 投资概览
    full_report += "📈 今日投资概览\n"
    full_report += "├─ 📊 个人基金 (7只)\n"
    full_report += "├─ 🔥 活跃基金 (TOP 5)\n"
    full_report += "└─ 🏆 黄金市场\n\n"
    
    full_report += personal_report + "\n"
    full_report += "-" * 40 + "\n\n"
    full_report += active_report + "\n"
    full_report += "-" * 40 + "\n\n"
    full_report += gold_section
    
    # 总结与建议
    full_report += "💡 今日投资建议:\n"
    
    # 基于分析给出建议
    if gold_data:
        gold_price = gold_data["prices"]["international"]
        if gold_price > 2180:
            gold_advice = "黄金高位，谨慎追高，关注$2,200阻力"
        else:
            gold_advice = "黄金相对合理，可考虑分批布局"
    else:
        gold_advice = "黄金数据暂缺，建议观察"
    
    full_report += f"1. 黄金: {gold_advice}\n"
    full_report += "2. 基金: 关注医疗领涨，QDII注意时差\n"
    full_report += "3. 整体: 控制仓位，分散风险\n\n"
    
    full_report += "=" * 50 + "\n"
    full_report += "📝 详细分析已保存到日志文件\n"
    full_report += "⏳ 下次报告: 明日 11:00"
    
    return full_report

def save_report(report):
    """保存报告到文件"""
    try:
        log_dir = "fund_reports"
        os.makedirs(log_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f"report_{date_str}.txt")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n\n")
            f.write(report)
            f.write("\n")
        
        print(f"📁 报告已保存: {log_file}")
    except Exception as e:
        print(f"保存报告失败: {e}")

def main():
    """主函数"""
    print("=== 每日基金报告生成 ===\n")
    
    # 生成报告
    report = generate_daily_report()
    
    # 打印报告
    print("\n" + report + "\n")
    
    # 保存报告
    save_report(report)
    
    print("✅ 报告生成完成！")

if __name__ == "__main__":
    main()