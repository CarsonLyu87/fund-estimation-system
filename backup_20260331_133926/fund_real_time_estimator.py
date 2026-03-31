#!/usr/bin/env python3
"""
基金实时涨跌幅估算器 - 实用版
使用天天基金网持仓 + 东方财富网股票数据
支持多基金、错误处理、备用数据源
"""

import json
import urllib.request
import urllib.parse
import time
import pandas as pd
from datetime import datetime
import re
import sys
import os

class FundRealTimeEstimator:
    """基金实时涨跌幅估算器"""
    
    def __init__(self):
        self.funds_config = self.load_funds_config()
        self.results = {}
        
    def load_funds_config(self):
        """加载基金配置"""
        config = [
            {
                'code': '006228',
                'name': '中欧医疗创新股票A',
                'type': '医疗',
                'priority': 1
            },
            {
                'code': '005827',
                'name': '易方达蓝筹精选混合',
                'type': '蓝筹',
                'priority': 2
            },
            {
                'code': '161725',
                'name': '招商中证白酒指数',
                'type': '白酒',
                'priority': 3
            }
        ]
        return config
    
    def get_fund_holdings_simple(self, fund_code):
        """简化版获取基金持仓（使用公开API）"""
        try:
            # 使用天天基金网的API接口
            url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Referer': f'http://fund.eastmoney.com/{fund_code}.html',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
                
                # 解析持仓数据
                holdings = []
                
                # 查找股票持仓
                stock_pattern = r'var stockCodes = \[(.*?)\];'
                stock_match = re.search(stock_pattern, content)
                
                if stock_match:
                    stock_codes = stock_match.group(1).replace('"', '').split(',')
                    
                    # 查找股票名称
                    name_pattern = r'var stockNames = \[(.*?)\];'
                    name_match = re.search(name_pattern, content)
                    stock_names = []
                    if name_match:
                        stock_names = name_match.group(1).replace('"', '').split(',')
                    
                    # 查找持仓比例
                    weight_pattern = r'var stockPercents = \[(.*?)\];'
                    weight_match = re.search(weight_pattern, content)
                    stock_weights = []
                    if weight_match:
                        stock_weights = weight_match.group(1).split(',')
                    
                    # 组合数据
                    for i in range(min(len(stock_codes), 10)):  # 只取前10大持仓
                        if i < len(stock_names) and i < len(stock_weights):
                            try:
                                weight = float(stock_weights[i])
                                if weight > 0:  # 只保留有持仓的
                                    holdings.append({
                                        'code': stock_codes[i],
                                        'name': stock_names[i] if i < len(stock_names) else f"股票{stock_codes[i]}",
                                        'weight': weight,
                                        'market': 'A' if stock_codes[i].startswith(('0', '3', '6')) else 'HK'
                                    })
                            except:
                                continue
                
                if holdings:
                    print(f"✅ 成功获取 {len(holdings)} 只持仓股票")
                    return holdings
                else:
                    print("⚠️  未找到持仓数据，使用模拟数据")
                    return self.get_mock_holdings(fund_code)
                    
        except Exception as e:
            print(f"❌ 获取持仓数据失败: {e}")
            return self.get_mock_holdings(fund_code)
    
    def get_mock_holdings(self, fund_code):
        """获取模拟持仓数据"""
        mock_data = {
            '006228': [  # 中欧医疗
                {'code': '603259', 'name': '药明康德', 'weight': 8.5, 'market': 'A'},
                {'code': '300759', 'name': '康龙化成', 'weight': 7.2, 'market': 'A'},
                {'code': '300347', 'name': '泰格医药', 'weight': 6.8, 'market': 'A'},
                {'code': '002821', 'name': '凯莱英', 'weight': 6.3, 'market': 'A'},
                {'code': '300363', 'name': '博腾股份', 'weight': 5.9, 'market': 'A'},
            ],
            '005827': [  # 易方达蓝筹
                {'code': '600519', 'name': '贵州茅台', 'weight': 9.8, 'market': 'A'},
                {'code': '00700', 'name': '腾讯控股', 'weight': 9.5, 'market': 'HK'},
                {'code': '600036', 'name': '招商银行', 'weight': 9.2, 'market': 'A'},
                {'code': '000858', 'name': '五粮液', 'weight': 8.7, 'market': 'A'},
                {'code': '00388', 'name': '香港交易所', 'weight': 8.3, 'market': 'HK'},
            ],
            '161725': [  # 招商白酒
                {'code': '600519', 'name': '贵州茅台', 'weight': 15.2, 'market': 'A'},
                {'code': '000858', 'name': '五粮液', 'weight': 14.8, 'market': 'A'},
                {'code': '002304', 'name': '洋河股份', 'weight': 12.5, 'market': 'A'},
                {'code': '000568', 'name': '泸州老窖', 'weight': 11.9, 'market': 'A'},
                {'code': '600809', 'name': '山西汾酒', 'weight': 9.7, 'market': 'A'},
            ]
        }
        
        return mock_data.get(fund_code, [])
    
    def get_stock_realtime_simple(self, stock_code, market='A'):
        """简化版获取股票实时数据"""
        try:
            if market == 'A':
                # 使用新浪财经API（更稳定）
                if stock_code.startswith('6'):
                    symbol = f"sh{stock_code}"
                else:
                    symbol = f"sz{stock_code}"
                
                url = f"http://hq.sinajs.cn/list={symbol}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Referer': 'http://finance.sina.com.cn',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate'
                }
                
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as response:
                    data = response.read().decode('gbk')
                    
                    # 解析数据格式：var hq_str_sh600519="贵州茅台,1825.000,1820.000,1822.500,..."
                    if '="' in data:
                        content = data.split('="')[1].strip('";')
                        parts = content.split(',')
                        
                        if len(parts) >= 4:
                            name = parts[0]
                            open_price = float(parts[1]) if parts[1] else 0
                            prev_close = float(parts[2]) if parts[2] else 0
                            current = float(parts[3]) if parts[3] else 0
                            
                            if prev_close > 0:
                                change = current - prev_close
                                change_percent = (change / prev_close) * 100
                            else:
                                change = 0
                                change_percent = 0
                            
                            return {
                                'name': name,
                                'current': current,
                                'change': change,
                                'change_percent': change_percent,
                                'prev_close': prev_close,
                                'open': open_price
                            }
            
            elif market == 'HK':
                # 港股使用腾讯财经API
                url = f"http://qt.gtimg.cn/q=hk{stock_code}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Referer': 'http://quote.eastmoney.com',
                    'Accept': '*/*'
                }
                
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as response:
                    data = response.read().decode('gbk')
                    
                    # 解析数据格式：v_hk00700="51.200;51.250;51.100;51.200;51.200;..."
                    if '="' in data:
                        content = data.split('="')[1].strip('";')
                        parts = content.split(';')
                        
                        if len(parts) >= 6:
                            current = float(parts[3]) if parts[3] else 0
                            prev_close = float(parts[2]) if parts[2] else 0
                            
                            if prev_close > 0:
                                change = current - prev_close
                                change_percent = (change / prev_close) * 100
                            else:
                                change = 0
                                change_percent = 0
                            
                            return {
                                'current': current,
                                'change': change,
                                'change_percent': change_percent,
                                'prev_close': prev_close
                            }
            
            return None
            
        except Exception as e:
            # print(f"调试: 获取股票 {stock_code} 失败: {e}")
            return None
    
    def estimate_fund_performance(self, fund_code, fund_name):
        """估算单只基金表现"""
        print(f"\n📊 开始估算: {fund_name} ({fund_code})")
        print("-"*40)
        
        # 1. 获取持仓
        holdings = self.get_fund_holdings_simple(fund_code)
        if not holdings:
            print("❌ 无法获取持仓数据，跳过该基金")
            return None
        
        # 2. 获取股票数据
        stock_data = {}
        success_count = 0
        
        print(f"获取 {len(holdings)} 只持仓股票实时数据...")
        for holding in holdings[:10]:  # 只处理前10大持仓
            stock_code = holding['code']
            stock_name = holding['name']
            market = holding['market']
            
            data = self.get_stock_realtime_simple(stock_code, market)
            
            if data:
                stock_data[stock_code] = data
                success_count += 1
            else:
                # 使用默认数据
                stock_data[stock_code] = {'change_percent': 0.0}
            
            time.sleep(0.05)  # 避免请求过快
        
        print(f"股票数据获取: {success_count}/{len(holdings)} 成功")
        
        # 3. 计算估算
        total_weight = sum(h['weight'] for h in holdings)
        weighted_change = 0
        contributions = []
        
        for holding in holdings:
            stock_code = holding['code']
            weight = holding['weight']
            
            stock_info = stock_data.get(stock_code, {})
            stock_change = stock_info.get('change_percent', 0)
            
            contribution = weight * stock_change / 100
            weighted_change += contribution
            
            contributions.append({
                'stock': f"{holding['name']}({stock_code})",
                'weight': weight,
                'stock_change': stock_change,
                'contribution': contribution
            })
        
        # 考虑现金仓位
        cash_weight = max(0, 100 - total_weight)
        total_estimated_change = weighted_change
        
        # 4. 保存结果
        result = {
            'fund_code': fund_code,
            'fund_name': fund_name,
            'estimation_time': datetime.now().strftime('%H:%M:%S'),
            'estimated_change': total_estimated_change,
            'stock_weight': total_weight,
            'cash_weight': cash_weight,
            'holdings_count': len(holdings),
            'contributions': contributions[:5],  # 只保留前5大贡献
            'data_quality': f"{success_count}/{len(holdings)}"
        }
        
        # 显示结果
        emoji = "📈" if total_estimated_change > 0 else "📉" if total_estimated_change < 0 else "➡️"
        print(f"{emoji} 估算结果: {total_estimated_change:+.4f}%")
        
        return result
    
    def generate_summary_report(self):
        """生成汇总报告"""
        if not self.results:
            return "❌ 没有估算结果"
        
        report = []
        report.append("="*70)
        report.append("📊 基金实时涨跌幅估算汇总报告")
        report.append(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*70)
        report.append("")
        
        # 总体概览
        total_funds = len(self.results)
        up_count = sum(1 for r in self.results.values() if r['estimated_change'] > 0)
        down_count = sum(1 for r in self.results.values() if r['estimated_change'] < 0)
        flat_count = total_funds - up_count - down_count
        
        report.append("📈 总体概览:")
        report.append(f"   监控基金: {total_funds} 只")
        report.append(f"   预计上涨: {up_count} 只")
        report.append(f"   预计下跌: {down_count} 只")
        report.append(f"   预计平盘: {flat_count} 只")
        report.append("")
        
        # 各基金详情
        report.append("🏆 各基金估算结果:")
        report.append("-"*50)
        
        sorted_results = sorted(self.results.items(), 
                              key=lambda x: abs(x[1]['estimated_change']), 
                              reverse=True)
        
        for fund_code, result in sorted_results:
            change = result['estimated_change']
            emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            
            report.append(f"{emoji} {result['fund_name']} ({fund_code})")
            report.append(f"   估算涨跌: {change:+.4f}%")
            report.append(f"   股票仓位: {result['stock_weight']:.1f}%")
            report.append(f"   数据质量: {result['data_quality']}")
            report.append(f"   估算时间: {result['estimation_time']}")
            report.append("")
        
        # 数据源说明
        report.append("📝 数据源说明:")
        report.append("   • 基金持仓: 天天基金网API")
        report.append("   • 股票数据: 新浪财经/腾讯财经API")
        report.append("   • 估算方法: ∑(持仓权重 × 股票实时涨跌)")
        report.append("")
        
        # 注意事项
        report.append("⚠️  重要提示:")
        report.append("   1. 此为实时估算，存在误差")
        report.append("   2. 持仓数据基于最新季报")
        report.append("   3. 现金仓位假设收益为0")
        report.append("   4. 最终以基金公司官方净值为准")
        report.append("")
        
        # 建议
        report.append("💡 投资建议:")
        if up_count > down_count:
            report.append("   市场情绪偏积极，可关注上涨基金")
        elif down_count > up_count:
            report.append("   市场情绪偏谨慎，注意风险控制")
        else:
            report.append("   市场分化明显，精选个股更重要")
        
        report.append("="*70)
        
        return "\n".join(report)
    
    def run_all_funds(self):
        """运行所有基金的估算"""
        print("🚀 开始基金实时涨跌幅估算")
        print("="*70)
        
        self.results = {}
        
        for fund in self.funds_config:
            fund_code = fund['code']
            fund_name = fund['name']
            
            result = self.estimate_fund_performance(fund_code, fund_name)
            if result:
                self.results[fund_code] = result
        
        # 生成报告
        report = self.generate_summary_report()
        print("\n" + report)
        
        # 保存报告
        self.save_report(report)
        
        return self.results
    
    def save_report(self, report):
        """保存报告到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fund_real_time_estimation_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 同时保存为最新报告
        with open("latest_fund_estimation.txt", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📁 报告已保存: {filename}")
        print(f"📝 最新报告: latest_fund_estimation.txt")
        
        return filename

def main():
    """主函数"""
    print("="*70)
    print("基金实时涨跌幅估算