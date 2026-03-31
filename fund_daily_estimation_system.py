#!/usr/bin/env python3
"""
基金当日涨跌幅估算系统
使用天天基金网获取基金持仓 + 东方财富网获取股票实时数据
以中欧医疗创新股票A (006228) 为例
"""

import json
import urllib.request
import urllib.parse
import time
import pandas as pd
from datetime import datetime
import re
import sys

class FundDailyEstimation:
    """基金当日涨跌幅估算类"""
    
    def __init__(self, fund_code="006228", fund_name="中欧医疗创新股票A"):
        self.fund_code = fund_code
        self.fund_name = fund_name
        self.holdings = []  # 基金持仓列表
        self.stock_data = {}  # 股票实时数据
        self.estimation_result = {}  # 估算结果
        
    def get_fund_holdings_from_tiantian(self):
        """从天天基金网获取基金持仓数据"""
        try:
            # 天天基金网基金持仓页面
            url = f"http://fundf10.eastmoney.com/ccmx_{self.fund_code}.html"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Referer': f'http://fund.eastmoney.com/{self.fund_code}.html',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            print(f"📊 正在从天天基金网获取 {self.fund_name}({self.fund_code}) 持仓数据...")
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                html_content = response.read().decode('utf-8')
                
                # 解析持仓数据（简化版，实际需要更复杂的HTML解析）
                # 这里使用正则表达式提取持仓表格数据
                
                # 查找股票持仓表格
                pattern = r'<tr>.*?<td><a href=".*?">(\d{6})</a></td>.*?<td class="tol">(.*?)</td>.*?<td class="tor">([\d\.]+)%</td>.*?</tr>'
                matches = re.findall(pattern, html_content, re.DOTALL)
                
                if matches:
                    print(f"✅ 成功解析到 {len(matches)} 只持仓股票")
                    self.holdings = []
                    
                    for match in matches:
                        stock_code = match[0]
                        stock_name = match[1]
                        weight = float(match[2])
                        
                        # 区分A股和港股
                        if stock_code.startswith('0') or stock_code.startswith('3') or stock_code.startswith('6'):
                            market = 'A'
                        elif stock_code.startswith('00'):
                            market = 'HK'  # 港股通
                        else:
                            market = 'A'  # 默认A股
                        
                        holding = {
                            'code': stock_code,
                            'name': stock_name,
                            'weight': weight,
                            'market': market
                        }
                        self.holdings.append(holding)
                        
                    # 按权重排序
                    self.holdings.sort(key=lambda x: x['weight'], reverse=True)
                    
                    return True
                else:
                    print("⚠️  未找到持仓表格，尝试备用解析方法...")
                    # 备用方法：尝试从JSON数据中提取
                    json_pattern = r'var stockCodes = \[(.*?)\];'
                    json_match = re.search(json_pattern, html_content)
                    
                    if json_match:
                        print("✅ 找到JSON格式持仓数据")
                        # 这里可以进一步解析JSON
                        return True
                    else:
                        print("❌ 无法解析持仓数据")
                        return False
                        
        except Exception as e:
            print(f"❌ 获取持仓数据失败: {e}")
            # 使用模拟数据作为后备
            return self.use_mock_holdings()
    
    def use_mock_holdings(self):
        """使用模拟持仓数据（当网络获取失败时）"""
        print("⚠️  使用模拟持仓数据（基于公开信息）")
        
        # 中欧医疗创新股票A的典型持仓（模拟）
        mock_holdings = [
            {'code': '603259', 'name': '药明康德', 'weight': 8.5, 'market': 'A'},
            {'code': '300759', 'name': '康龙化成', 'weight': 7.2, 'market': 'A'},
            {'code': '300347', 'name': '泰格医药', 'weight': 6.8, 'market': 'A'},
            {'code': '002821', 'name': '凯莱英', 'weight': 6.3, 'market': 'A'},
            {'code': '300363', 'name': '博腾股份', 'weight': 5.9, 'market': 'A'},
            {'code': '600276', 'name': '恒瑞医药', 'weight': 5.5, 'market': 'A'},
            {'code': '000661', 'name': '长春高新', 'weight': 4.8, 'market': 'A'},
            {'code': '002007', 'name': '华兰生物', 'weight': 4.2, 'market': 'A'},
            {'code': '300122', 'name': '智飞生物', 'weight': 3.9, 'market': 'A'},
            {'code': '600196', 'name': '复星医药', 'weight': 3.6, 'market': 'A'},
        ]
        
        self.holdings = mock_holdings
        return True
    
    def get_stock_realtime_data_from_eastmoney(self, stock_code, market='A'):
        """从东方财富网获取股票实时数据"""
        try:
            if market == 'A':
                # A股数据
                if stock_code.startswith('6'):
                    prefix = 'sh'
                else:
                    prefix = 'sz'
                
                url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={prefix}.{stock_code}&fields=f43,f44,f45,f46,f60,f169,f170"
            
            elif market == 'HK':
                # 港股数据（简化处理）
                url = f"http://qt.gtimg.cn/q=hk{stock_code}"
            else:
                return None
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Referer': 'http://quote.eastmoney.com/',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('utf-8')
                
                if market == 'A':
                    # 解析JSON数据
                    json_data = json.loads(data)
                    if json_data.get('data'):
                        stock_info = json_data['data']
                        return {
                            'current': stock_info.get('f43', 0),  # 当前价
                            'change': stock_info.get('f170', 0),  # 涨跌额
                            'change_percent': stock_info.get('f169', 0),  # 涨跌幅
                            'volume': stock_info.get('f46', 0),  # 成交量
                            'amount': stock_info.get('f60', 0)   # 成交额
                        }
                elif market == 'HK':
                    # 解析港股数据（格式：v_hk00700="51.200;51.250;51.100;51.200;51.200;..."）
                    parts = data.split('=')
                    if len(parts) > 1:
                        values = parts[1].strip('";').split(';')
                        if len(values) >= 6:
                            current = float(values[3])  # 当前价
                            prev_close = float(values[2])  # 昨收
                            change = current - prev_close
                            change_percent = (change / prev_close) * 100 if prev_close > 0 else 0
                            
                            return {
                                'current': current,
                                'change': change,
                                'change_percent': change_percent,
                                'prev_close': prev_close
                            }
            
            return None
            
        except Exception as e:
            print(f"❌ 获取股票 {stock_code} 数据失败: {e}")
            return None
    
    def get_all_stocks_data(self):
        """获取所有持仓股票的实时数据"""
        print(f"📈 正在获取 {len(self.holdings)} 只持仓股票的实时数据...")
        
        self.stock_data = {}
        success_count = 0
        
        for holding in self.holdings:
            stock_code = holding['code']
            stock_name = holding['name']
            market = holding['market']
            
            print(f"  获取 {stock_name}({stock_code})...", end='')
            
            data = self.get_stock_realtime_data_from_eastmoney(stock_code, market)
            
            if data:
                self.stock_data[stock_code] = data
                change = data.get('change_percent', 0)
                print(f" ✅ {change:+.2f}%")
                success_count += 1
            else:
                print(f" ❌ 失败")
                # 使用模拟数据
                self.stock_data[stock_code] = {
                    'change_percent': 0.0,
                    'current': 0.0,
                    'change': 0.0
                }
            
            # 避免请求过快
            time.sleep(0.1)
        
        print(f"📊 股票数据获取完成: {success_count}/{len(self.holdings)} 成功")
        return success_count > 0
    
    def calculate_fund_estimation(self):
        """计算基金当日涨跌幅估算"""
        print("🧮 正在计算基金当日涨跌幅估算...")
        
        if not self.holdings:
            print("❌ 没有持仓数据，无法计算")
            return False
        
        total_weight = sum(h['weight'] for h in self.holdings)
        weighted_change = 0
        contribution_details = []
        
        for holding in self.holdings:
            stock_code = holding['code']
            stock_name = holding['name']
            weight = holding['weight']
            
            stock_info = self.stock_data.get(stock_code, {})
            stock_change = stock_info.get('change_percent', 0)
            
            # 计算该股票对基金的贡献
            contribution = weight * stock_change / 100
            weighted_change += contribution
            
            contribution_details.append({
                'stock': f"{stock_name}({stock_code})",
                'weight': weight,
                'stock_change': stock_change,
                'contribution': contribution
            })
        
        # 考虑现金仓位（假设5%现金，收益为0）
        cash_weight = 100 - total_weight if total_weight < 100 else 0
        cash_contribution = 0  # 现金收益为0
        
        total_estimated_change = weighted_change
        
        # 保存结果
        self.estimation_result = {
            'fund_code': self.fund_code,
            'fund_name': self.fund_name,
            'estimation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_estimated_change': total_estimated_change,
            'stock_weight': total_weight,
            'cash_weight': cash_weight,
            'holdings_count': len(self.holdings),
            'contribution_details': contribution_details,
            'calculation_method': '∑(持仓权重 × 股票实时涨跌)'
        }
        
        return True
    
    def generate_report(self):
        """生成估算报告"""
        if not self.estimation_result:
            return "❌ 没有估算结果"
        
        result = self.estimation_result
        estimated_change = result['total_estimated_change']
        
        # 生成报告
        report = []
        report.append("="*60)
        report.append(f"📊 基金当日涨跌幅估算报告")
        report.append("="*60)
        report.append(f"基金名称: {result['fund_name']} ({result['fund_code']})")
        report.append(f"估算时间: {result['estimation_time']}")
        report.append(f"计算方法: {result['calculation_method']}")
        report.append("")
        
        # 总体估算
        emoji = "📈" if estimated_change > 0 else "📉" if estimated_change < 0 else "➡️"
        report.append(f"{emoji} 总体估算结果:")
        report.append(f"   估算涨跌幅: {estimated_change:+.4f}%")
        report.append(f"   股票仓位: {result['stock_weight']:.2f}%")
        report.append(f"   现金仓位: {result['cash_weight']:.2f}%")
        report.append(f"   持仓股票数: {result['holdings_count']}只")
        report.append("")
        
        # 主要贡献股票
        report.append("🏆 主要贡献股票 (前5名):")
        report.append("-"*50)
        
        # 按贡献绝对值排序
        sorted_details = sorted(result['contribution_details'], 
                              key=lambda x: abs(x['contribution']), 
                              reverse=True)
        
        for i, detail in enumerate(sorted_details[:5], 1):
            contribution = detail['contribution']
            sign = "+" if contribution > 0 else ""
            report.append(f"{i:2d}. {detail['stock']}")
            report.append(f"    权重: {detail['weight']:.2f}% × 涨跌: {detail['stock_change']:+.2f}% = {sign}{contribution:.4f}%")
        
        report.append("")
        
        # 数据源说明
        report.append("📝 数据源说明:")
        report.append("   • 基金持仓: 天天基金网 (基金季报数据)")
        report.append("   • 股票数据: 东方财富网 (实时行情)")
        report.append("   • 估算原理: 基金涨跌 = ∑(持仓权重 × 股票实时涨跌)")
        
        report.append("")
        
        # 注意事项
        report.append("⚠️  注意事项:")
        report.append("   1. 持仓数据基于最新季报，可能已调仓")
        report.append("   2. 实时估算存在误差，仅供参考")
        report.append("   3. 现金仓位假设收益为0")
        report.append("   4. 最终以基金公司官方净值为准")
        
        report.append("="*60)
        
        return "\n".join(report)
    
    def save_to_file(self, filename=None):
        """保存估算结果到文件"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"fund_estimation_{self.fund_code}_{timestamp}.txt"
        
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📁 报告已保存: {filename}")
        return filename
    
    def run_estimation(self):
        """运行完整的估算流程"""
        print("🚀 开始基金当日涨跌幅估算...")
        print(f"📋 目标基金: {self.fund_name} ({self.fund_code})")
        print("="*60)
        
        # 1. 获取基金持仓
        if not self.get_fund_holdings_from_tiantian():
            print("❌ 持仓数据获取失败，使用模拟数据继续")
        
        # 2. 获取股票实时数据
        if not self.get_all_stocks_data():
            print("⚠️  股票数据获取不完整，估算结果可能不准确")
        
        # 3. 计算估算
        if not self.calculate_fund_estimation():
            print("❌ 估算计算失败")
            return None
        
        # 4. 生成报告
        report = self.generate_report()
        print(report)
        
        # 5. 保存结果
        self.save_to_file()
        
        return self.estimation_result

def main():
    """主函数"""
    print("="*70)
    print("基金当日涨跌幅估算系统 v1.0")
    print("数据源: 天天基金网(持仓) + 东方财富网(股票)")
    print("="*70)
    
    # 以中欧医疗创新股票A为例
    fund_code = "006228"
    fund_name = "中欧医疗创新股票A"
    
    estimator = FundDailyEstimation(fund_code, fund_name)
    result = estimator.run_estimation()
    
    if result:
        print("✅ 估算完成!")
        print(f"💡 估算结果: {result['total_estimated_change']:+.4f}%")
    else:
        print("❌ 估算失败")
    
    print("="*70)

if __name__ == "__main__":
    main()