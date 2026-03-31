#!/usr/bin/env python3
"""
每日基金摘要 - 最终解决方案
极简摘要 + 本地保存，适应微信限制
"""

import subprocess
import os
import sys
from datetime import datetime

class DailyFundReporter:
    def __init__(self):
        self.session_id = 'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat'
        self.workspace = '/Users/carson/.openclaw/workspace'
        
    def run_report_script(self):
        """运行报告脚本"""
        print("📊 生成基金报告...")
        
        try:
            result = subprocess.run(
                [sys.executable, 'daily_fund_report.py'],
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=30  # 30秒超时
            )
            
            if result.returncode != 0:
                print(f"❌ 报告生成失败: {result.stderr[:200]}")
                return None
            
            print(f"✅ 报告生成成功 ({len(result.stdout)} 字符)")
            return result.stdout
            
        except subprocess.TimeoutExpired:
            print("❌ 报告生成超时")
            return None
        except Exception as e:
            print(f"❌ 报告生成异常: {str(e)}")
            return None
    
    def save_full_report(self, content):
        """保存完整报告"""
        report_dir = os.path.join(self.workspace, "fund_reports")
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(report_dir, f"report_{timestamp}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📁 完整报告已保存: {report_file}")
        return report_file
    
    def extract_key_data(self, report_content):
        """从报告中提取关键数据"""
        lines = report_content.split('\n')
        
        # 初始化数据
        data = {
            'personal_up': 0,
            'personal_down': 0,
            'top_funds': [],
            'gold_price': '',
            'gold_change': '',
            'key_funds': []
        }
        
        for line in lines:
            # 统计涨跌 - 处理格式 "📈 上涨: 5只 | 📉 下跌: 2只"
            if '📈 上涨:' in line:
                # 提取上涨数量
                up_part = line.split('📈 上涨:')[1]
                if '只' in up_part:
                    up_num = up_part.split('只')[0].strip()
                    try:
                        data['personal_up'] = int(up_num)
                    except:
                        pass
                
                # 提取下跌数量
                if '📉 下跌:' in line:
                    down_part = line.split('📉 下跌:')[1]
                    if '只' in down_part:
                        down_num = down_part.split('只')[0].strip()
                        try:
                            data['personal_down'] = int(down_num)
                        except:
                            pass
            
            # 提取关键基金（前3个）
            if ('📈' in line or '📉' in line) and '%' in line:
                if len(data['key_funds']) < 3:
                    # 简化格式
                    simplified = line.replace('📈 ', '↑ ').replace('📉 ', '↓ ')
                    data['key_funds'].append(simplified.strip())
            
            # 提取黄金价格
            if '💰 价格:' in line:
                data['gold_price'] = line.replace('💰 价格:', '').strip()
            elif '📊 今日涨跌:' in line:
                data['gold_change'] = line.replace('📊 今日涨跌:', '').strip()
        
        return data
    
    def create_minimal_summary(self, data):
        """创建极简摘要"""
        current_time = datetime.now().strftime('%H:%M:%S')
        
        summary = f"""📈 基金日报 {current_time}
========================"""
        
        # 持仓概况
        total = data['personal_up'] + data['personal_down']
        summary += f"\n👤 持仓: {total}只"
        if data['personal_up'] > 0:
            summary += f" (↑{data['personal_up']} ↓{data['personal_down']})"
        
        # 关键基金
        if data['key_funds']:
            summary += "\n"
            for fund in data['key_funds'][:2]:  # 最多2只
                summary += f"\n{fund}"
        
        # 黄金信息
        if data['gold_price']:
            summary += f"\n\n🏆 黄金: {data['gold_price']}"
            if data['gold_change']:
                summary += f" {data['gold_change']}"
        
        # 结尾
        summary += f"\n\n📁 详报已保存"
        summary += f"\n⏰ 明日 11:00"
        
        # 确保长度合适
        if len(summary) > 300:
            summary = summary[:280] + "..."
        
        print(f"📋 摘要长度: {len(summary)} 字符")
        return summary
    
    def send_summary(self, summary):
        """发送摘要"""
        print("📤 发送极简摘要...")
        
        # 使用正确的命令格式
        send_cmd = [
            'openclaw', 'message', 'send',
            '--channel', 'openclaw-weixin',
            '--target', 'o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
            '--message', summary
        ]
        
        try:
            result = subprocess.run(
                send_cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ 摘要发送成功")
                return True
            else:
                print(f"❌ 摘要发送失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 发送超时")
            return False
        except Exception as e:
            print(f"❌ 发送异常: {str(e)}")
            return False
    
    def log_daily_run(self, success, report_file, summary):
        """记录每日运行日志"""
        log_dir = os.path.join(self.workspace, "fund_logs")
        os.makedirs(log_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f"run_{date_str}.log")
        
        log_content = f"""📅 运行日志 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
状态: {'✅ 成功' if success else '❌ 失败'}

📊 报告信息:
• 生成时间: {datetime.now().strftime('%H:%M:%S')}
• 报告文件: {os.path.basename(report_file) if report_file else '无'}
• 摘要长度: {len(summary)} 字符
• 发送状态: {'成功' if success else '失败'}

📋 摘要内容:
{summary}

🔧 系统信息:
• Python版本: {sys.version.split()[0]}
• 工作目录: {self.workspace}
• 会话ID: {self.session_id[:30]}...
========================================"""
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print(f"📝 运行日志已保存: {log_file}")
    
    def run(self):
        """主运行流程"""
        print(f"🚀 每日基金摘要系统")
        print(f"🕐 启动时间: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # 1. 生成报告
        report_content = self.run_report_script()
        if not report_content:
            print("❌ 无法生成报告，退出")
            return False
        
        print("\n" + "-" * 50)
        
        # 2. 保存完整报告
        report_file = self.save_full_report(report_content)
        
        print("\n" + "-" * 50)
        
        # 3. 提取数据并创建摘要
        data = self.extract_key_data(report_content)
        summary = self.create_minimal_summary(data)
        
        print("\n" + "-" * 50)
        
        # 4. 发送摘要
        send_success = self.send_summary(summary)
        
        print("\n" + "-" * 50)
        
        # 5. 记录日志
        self.log_daily_run(send_success, report_file, summary)
        
        print("\n" + "=" * 60)
        
        if send_success:
            print("🎉 每日摘要任务完成!")
            print(f"✅ 极简摘要已发送")
            print(f"✅ 完整报告已保存")
            print(f"✅ 运行日志已记录")
        else:
            print("⚠️ 摘要发送失败")
            print(f"📁 报告已保存: {report_file}")
            print(f"📝 日志已记录")
        
        print(f"\n🐉 系统时间: {datetime.now().strftime('%H:%M:%S')}")
        return send_success

def main():
    """主函数"""
    reporter = DailyFundReporter()
    success = reporter.run()
    
    # 返回退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()