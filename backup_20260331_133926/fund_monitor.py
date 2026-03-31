#!/usr/bin/env python3
"""
基金涨跌监控脚本
每日11点运行，检查指定基金的涨跌情况
"""

import requests
import json
from datetime import datetime
import os

# 基金代码列表（示例，请根据实际需要修改）
FUND_CODES = [
    "000001",  # 华夏成长混合
    "110022",  # 易方达消费行业
    "161725",  # 招商中证白酒指数
    # 添加更多基金代码...
]

def get_fund_data(fund_code):
    """
    获取基金实时数据
    这里使用天天基金网的API示例
    """
    try:
        url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # 解析JSONP格式的数据
            text = response.text
            # 去除jsonp回调函数
            json_str = text[text.find('{'):text.rfind('}')+1]
            data = json.loads(json_str)
            return data
        else:
            return None
    except Exception as e:
        print(f"获取基金{fund_code}数据失败: {e}")
        return None

def format_fund_message(fund_data):
    """格式化基金信息"""
    if not fund_data:
        return "数据获取失败"
    
    name = fund_data.get('name', '未知基金')
    code = fund_data.get('fundcode', '未知代码')
    dwjz = fund_data.get('dwjz', '0.0000')  # 单位净值
    gsz = fund_data.get('gsz', '0.0000')    # 估算净值
    gszzl = fund_data.get('gszzl', '0.00')  # 估算涨跌幅
    gztime = fund_data.get('gztime', '未知时间')
    
    # 判断涨跌
    change = float(gszzl)
    if change > 0:
        trend = "📈 上涨"
    elif change < 0:
        trend = "📉 下跌"
    else:
        trend = "➡️ 持平"
    
    return f"{name} ({code})\n" \
           f"净值: {dwjz} | 估算: {gsz}\n" \
           f"涨跌: {trend} {gszzl}%\n" \
           f"时间: {gztime}\n"

def main():
    print(f"=== 基金监控报告 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    
    all_results = []
    for fund_code in FUND_CODES:
        print(f"正在查询基金 {fund_code}...")
        data = get_fund_data(fund_code)
        if data:
            message = format_fund_message(data)
            all_results.append(message)
            print(message)
        else:
            error_msg = f"基金 {fund_code} 数据获取失败\n"
            all_results.append(error_msg)
            print(error_msg)
    
    # 保存结果到文件（可选）
    result_file = "fund_report.txt"
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f"基金监控报告 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for result in all_results:
            f.write(result + "\n")
    
    print(f"报告已保存到: {result_file}")
    return all_results

if __name__ == "__main__":
    main()