#!/usr/bin/env python3
"""
基金监控技能
用于获取和报告基金涨跌情况
"""

import requests
import json
from datetime import datetime
import os
import sys

class FundMonitor:
    def __init__(self, config_file="fund_config.json"):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """加载基金配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # 默认配置
                self.config = {
                    "funds": [
                        {"code": "000001", "name": "华夏成长混合"},
                        {"code": "110022", "name": "易方达消费行业"},
                        {"code": "161725", "name": "招商中证白酒指数"}
                    ],
                    "data_source": "天天基金网",
                    "notification_format": "简洁"
                }
                # 保存默认配置
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.config = {"funds": []}
    
    def get_fund_data(self, fund_code):
        """
        从天天基金网获取基金数据
        注意：这是一个示例API，实际使用时可能需要调整
        """
        try:
            # 天天基金网API
            url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # 解析JSONP
                text = response.text
                if 'jsonpgz(' in text:
                    json_str = text[text.find('(')+1:text.rfind(')')]
                    data = json.loads(json_str)
                    return data
            return None
        except Exception as e:
            print(f"获取基金{fund_code}数据失败: {e}")
            return None
    
    def format_fund_info(self, fund_data, fund_config):
        """格式化基金信息"""
        if not fund_data:
            return f"{fund_config.get('name', '未知基金')} ({fund_config.get('code', '未知')}): 数据获取失败"
        
        name = fund_data.get('name', fund_config.get('name', '未知基金'))
        code = fund_data.get('fundcode', fund_config.get('code', '未知'))
        dwjz = fund_data.get('dwjz', '0.0000')  # 单位净值
        gsz = fund_data.get('gsz', '0.0000')    # 估算净值
        gszzl = fund_data.get('gszzl', '0.00')  # 估算涨跌幅
        gztime = fund_data.get('gztime', '未知时间')
        
        # 转换涨跌幅为浮点数
        try:
            change = float(gszzl)
        except:
            change = 0.0
        
        # 选择表情符号
        if change > 0.5:
            emoji = "🚀"
        elif change > 0:
            emoji = "📈"
        elif change < -0.5:
            emoji = "💥"
        elif change < 0:
            emoji = "📉"
        else:
            emoji = "➡️"
        
        # 根据配置选择格式
        if self.config.get("notification_format") == "详细":
            return f"{emoji} {name} ({code})\n" \
                   f"  单位净值: {dwjz}\n" \
                   f"  估算净值: {gsz}\n" \
                   f"  涨跌幅: {gszzl}%\n" \
                   f"  更新时间: {gztime}\n"
        else:
            # 简洁格式
            return f"{emoji} {name}: {gszzl}%"
    
    def generate_report(self):
        """生成基金报告"""
        print(f"📊 基金监控报告 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 40)
        
        results = []
        total_funds = len(self.config.get("funds", []))
        success_count = 0
        
        for fund in self.config.get("funds", []):
            fund_code = fund.get("code")
            fund_name = fund.get("name", f"基金{fund_code}")
            
            print(f"正在查询: {fund_name} ({fund_code})...")
            data = self.get_fund_data(fund_code)
            
            if data:
                success_count += 1
                formatted = self.format_fund_info(data, fund)
                results.append(formatted)
                print(formatted)
            else:
                error_msg = f"❌ {fund_name}: 数据获取失败"
                results.append(error_msg)
                print(error_msg)
            
            print("-" * 30)
        
        # 总结
        print(f"\n📋 总结: 成功获取 {success_count}/{total_funds} 只基金数据")
        
        # 保存日志
        self.save_log(results)
        
        return results
    
    def save_log(self, results):
        """保存日志文件"""
        try:
            log_dir = "fund_logs"
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, f"fund_{datetime.now().strftime('%Y%m%d')}.txt")
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                for result in results:
                    f.write(result + "\n")
                f.write("\n")
            
            print(f"📝 日志已保存: {log_file}")
        except Exception as e:
            print(f"保存日志失败: {e}")
    
    def update_config(self, new_funds):
        """更新基金配置"""
        try:
            self.config["funds"] = new_funds
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print("✅ 配置已更新")
            return True
        except Exception as e:
            print(f"更新配置失败: {e}")
            return False

def main():
    """主函数"""
    monitor = FundMonitor()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            print("🧪 测试模式: 使用模拟数据")
            # 这里可以添加测试数据
            pass
        elif sys.argv[1] == "config":
            print("⚙️ 显示当前配置:")
            print(json.dumps(monitor.config, ensure_ascii=False, indent=2))
            return
    
    # 生成报告
    monitor.generate_report()

if __name__ == "__main__":
    main()