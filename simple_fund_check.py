#!/usr/bin/env python3
"""
简化版基金检查脚本
使用内置库，无需外部依赖
"""

import json
import os
from datetime import datetime
import urllib.request
import urllib.error

def simple_get_fund_data(fund_code):
    """
    使用urllib获取基金数据
    """
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            text = response.read().decode('utf-8')
            
            # 解析JSONP
            if 'jsonpgz(' in text:
                json_str = text[text.find('(')+1:text.rfind(')')]
                return json.loads(json_str)
        return None
    except Exception as e:
        print(f"获取基金{fund_code}数据失败: {e}")
        return None

def load_config():
    """加载基金配置"""
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
        print(f"加载配置失败: {e}")
    
    return default_funds

def main():
    print(f"🐉 小龙基金监控 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 加载基金配置
    funds = load_config()
    print(f"📊 监控 {len(funds)} 只基金")
    
    results = []
    
    for fund in funds:
        code = fund["code"]
        name = fund["name"]
        
        print(f"查询: {name} ({code})...")
        data = simple_get_fund_data(code)
        
        if data:
            gszzl = data.get('gszzl', '0.00')
            gztime = data.get('gztime', '未知时间')
            
            try:
                change = float(gszzl)
                if change > 0:
                    emoji = "📈"
                elif change < 0:
                    emoji = "📉"
                else:
                    emoji = "➡️"
            except:
                emoji = "❓"
            
            result = f"{emoji} {name}: {gszzl}% ({gztime})"
            results.append(result)
            print(f"  {result}")
        else:
            result = f"❌ {name}: 数据获取失败"
            results.append(result)
            print(f"  {result}")
        
        print("-" * 40)
    
    # 总结
    print(f"\n📋 今日基金概览:")
    for result in results:
        print(f"  {result}")
    
    # 保存日志
    try:
        log_dir = "fund_logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.txt")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            for result in results:
                f.write(result + "\n")
            f.write("\n")
        
        print(f"\n📝 日志已保存: {log_file}")
    except Exception as e:
        print(f"保存日志失败: {e}")

if __name__ == "__main__":
    main()