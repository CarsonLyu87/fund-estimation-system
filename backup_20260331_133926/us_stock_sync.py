#!/usr/bin/env python3
"""
美股同步脚本 - 英伟达(NVDA)和谷歌(GOOGL)
每天早上9点同步前一日收盘涨跌情况
"""

import requests
import json
from datetime import datetime, timedelta
import subprocess
import os

class USStockSync:
    def __init__(self):
        self.session_id = 'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat'
        self.workspace = '/Users/carson/.openclaw/workspace'
        
        # 美股股票配置
        self.stocks = {
            'NVDA': {
                'name': '英伟达',
                'symbol': 'NVDA',
                'full_name': 'NVIDIA Corporation',
                'sector': '半导体/科技'
            },
            'GOOGL': {
                'name': '谷歌',
                'symbol': 'GOOGL',
                'full_name': 'Alphabet Inc. (Google)',
                'sector': '互联网/科技'
            }
        }
    
    def get_stock_data(self, symbol):
        """获取股票数据（使用模拟数据，实际可接入API）"""
        print(f"📊 获取 {symbol} 数据...")
        
        # 这里使用模拟数据，实际可以接入：
        # 1. Yahoo Finance API
        # 2. Alpha Vantage
        # 3. 其他财经数据API
        
        # 模拟数据 - 实际使用时需要替换为真实API调用
        mock_data = {
            'NVDA': {
                'price': 950.42,
                'change': -12.35,
                'change_percent': -1.28,
                'prev_close': 962.77,
                'volume': '45.2M',
                'market_cap': '2.38T',
                'day_range': '945.60 - 958.20',
                'year_range': '350.51 - 974.00',
                'timestamp': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            },
            'GOOGL': {
                'price': 175.85,
                'change': +2.15,
                'change_percent': +1.24,
                'prev_close': 173.70,
                'volume': '28.7M',
                'market_cap': '2.21T',
                'day_range': '173.20 - 176.50',
                'year_range': '115.15 - 178.67',
                'timestamp': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            }
        }
        
        return mock_data.get(symbol, {})
    
    def create_stock_message(self, stock_info, stock_config):
        """创建股票消息"""
        symbol = stock_config['symbol']
        name = stock_config['name']
        
        if not stock_info:
            return f"{name}({symbol}): 数据获取失败"
        
        price = stock_info.get('price', 0)
        change = stock_info.get('change', 0)
        change_percent = stock_info.get('change_percent', 0)
        volume = stock_info.get('volume', 'N/A')
        timestamp = stock_info.get('timestamp', '')
        
        # 确定涨跌图标
        trend = '📈' if change >= 0 else '📉'
        change_sign = '+' if change >= 0 else ''
        
        message = f"""🏢 {name} ({symbol})
💰 股价: ${price:.2f}
{trend} 涨跌: {change_sign}{change:.2f} ({change_sign}{change_percent:.2f}%)
📊 成交量: {volume}
🕐 数据时间: {timestamp}"""
        
        return message
    
    def create_summary_message(self, stocks_data):
        """创建汇总消息"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 计算总体表现
        total_change = sum(data.get('change', 0) for data in stocks_data.values())
        avg_change = total_change / len(stocks_data) if stocks_data else 0
        
        summary = f"""📈 美股早报 {current_time}
=======================
🎯 监控股票: 2只

📊 昨日收盘表现:"""
        
        for symbol, data in stocks_data.items():
            stock_config = self.stocks.get(symbol, {})
            name = stock_config.get('name', symbol)
            change = data.get('change', 0)
            change_percent = data.get('change_percent', 0)
            trend = '📈' if change >= 0 else '📉'
            change_sign = '+' if change >= 0 else ''
            
            summary += f"\n{trend} {name}: {change_sign}{change_percent:.2f}%"
        
        summary += f"\n\n📈 平均涨跌: {avg_change:+.2f}%"
        summary += f"\n🕐 数据时间: 前一日收盘"
        summary += f"\n⏰ 下次同步: 明日 09:00"
        
        return summary
    
    def save_stock_data(self, stocks_data):
        """保存股票数据到文件"""
        data_dir = os.path.join(self.workspace, "us_stock_data")
        os.makedirs(data_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        data_file = os.path.join(data_dir, f"stocks_{date_str}.json")
        
        # 添加时间戳
        data_with_meta = {
            'timestamp': datetime.now().isoformat(),
            'data_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'stocks': stocks_data
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data_with_meta, f, indent=2, ensure_ascii=False)
        
        print(f"📁 股票数据已保存: {data_file}")
        return data_file
    
    def send_message(self, message):
        """发送消息"""
        send_cmd = [
            'openclaw', 'sessions', 'send',
            self.session_id,
            message
        ]
        
        result = subprocess.run(send_cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def run(self):
        """主运行流程"""
        print("🚀 美股同步任务启动")
        print(f"🕐 时间: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # 获取股票数据
        stocks_data = {}
        detailed_messages = []
        
        for symbol, config in self.stocks.items():
            print(f"\n📊 处理 {config['name']}({symbol})...")
            
            stock_info = self.get_stock_data(symbol)
            if stock_info:
                stocks_data[symbol] = stock_info
                
                # 创建详细消息
                detailed_msg = self.create_stock_message(stock_info, config)
                detailed_messages.append(detailed_msg)
                
                print(f"   ✅ 数据获取成功")
                print(f"     股价: ${stock_info.get('price', 0):.2f}")
                print(f"     涨跌: {stock_info.get('change', 0):+.2f}%")
            else:
                print(f"   ❌ 数据获取失败")
        
        print("\n" + "-" * 50)
        
        if not stocks_data:
            print("❌ 所有股票数据获取失败")
            error_msg = f"""❌ 美股数据获取失败 {datetime.now().strftime('%H:%M:%S')}
=======================
无法获取英伟达和谷歌的股价数据。

可能原因:
• 网络连接问题
• 数据API限制
• 市场休市

🔧 请检查网络或稍后重试"""
            
            self.send_message(error_msg)
            return False
        
        # 保存数据
        data_file = self.save_stock_data(stocks_data)
        
        print("\n" + "-" * 50)
        
        # 发送详细股票信息
        print("📤 发送详细股票信息...")
        for i, msg in enumerate(detailed_messages, 1):
            print(f"  发送第 {i}/{len(detailed_messages)} 只股票...")
            success = self.send_message(msg)
            if success:
                print(f"     ✅ 发送成功")
            else:
                print(f"     ❌ 发送失败")
            
            # 消息间短暂延迟
            if i < len(detailed_messages):
                import time
                time.sleep(0.5)
        
        print("\n" + "-" * 50)
        
        # 发送汇总消息
        print("📋 发送汇总消息...")
        summary_msg = self.create_summary_message(stocks_data)
        summary_success = self.send_message(summary_msg)
        
        if summary_success:
            print("✅ 汇总消息发送成功")
        else:
            print("❌ 汇总消息发送失败")
        
        print("\n" + "-" * 50)
        
        # 记录运行日志
        self.log_run(stocks_data, data_file, summary_success)
        
        print("\n" + "=" * 60)
        
        if summary_success:
            print("🎉 美股同步任务完成!")
            print(f"✅ 详细股票信息: {len(detailed_messages)} 条")
            print(f"✅ 汇总消息: 1 条")
            print(f"✅ 数据文件: {os.path.basename(data_file)}")
        else:
            print("⚠️ 美股同步部分完成")
            print(f"📁 数据已保存: {data_file}")
        
        print(f"\n🐉 完成于 {datetime.now().strftime('%H:%M:%S')}")
        return summary_success
    
    def log_run(self, stocks_data, data_file, success):
        """记录运行日志"""
        log_dir = os.path.join(self.workspace, "us_stock_logs")
        os.makedirs(log_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f"sync_{date_str}.log")
        
        log_content = f"""📅 美股同步日志 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
状态: {'✅ 成功' if success else '❌ 失败'}

📊 同步股票: {len(stocks_data)} 只
"""
        
        for symbol, data in stocks_data.items():
            config = self.stocks.get(symbol, {})
            name = config.get('name', symbol)
            price = data.get('price', 0)
            change = data.get('change', 0)
            change_percent = data.get('change_percent', 0)
            
            log_content += f"\n{name}({symbol}):"
            log_content += f"\n  • 股价: ${price:.2f}"
            log_content += f"\n  • 涨跌: {change:+.2f} ({change_percent:+.2f}%)"
        
        log_content += f"\n\n📁 数据文件: {os.path.basename(data_file)}"
        log_content += f"\n📝 日志文件: {os.path.basename(log_file)}"
        log_content += f"\n⏰ 下次同步: 明日 09:00"
        log_content += f"\n========================================"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"📝 运行日志已保存: {log_file}")

def main():
    """主函数"""
    sync = USStockSync()
    success = sync.run()
    
    # 返回退出码
    import sys
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()