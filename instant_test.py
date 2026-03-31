#!/usr/bin/env python3
"""
即时测试脚本
"""

import subprocess
from datetime import datetime

def test_direct_message():
    """直接发送测试消息"""
    print(f"🕐 测试时间: {datetime.now().strftime('%H:%M:%S')}")
    
    # 测试消息
    test_msg = f"""📊 即时测试报告 {datetime.now().strftime('%H:%M:%S')}
========================================
✅ 系统功能测试

1. 消息发送测试
2. 报告生成测试  
3. 微信通道测试

📋 测试项目:
• 直接消息发送 ✓
• 会话路由验证 ✓
• 内容格式测试 ✓

⏰ 时间戳: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================"""
    
    print("📤 发送测试消息...")
    
    # 使用正确的会话ID格式
    send_cmd = [
        'openclaw', 'sessions', 'send',
        'openclaw-weixin:o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        test_msg
    ]
    
    print(f"执行命令: {' '.join(send_cmd[:3])} [消息内容...]")
    
    result = subprocess.run(send_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 消息发送命令执行成功")
        print(f"输出: {result.stdout}")
    else:
        print(f"❌ 消息发送失败")
        print(f"错误: {result.stderr}")
    
    return result.returncode == 0

def test_report_generation():
    """测试报告生成"""
    print("\n📄 测试报告生成...")
    
    result = subprocess.run(['python3', 'daily_fund_report.py'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 报告生成成功")
        # 提取报告摘要
        lines = result.stdout.split('\n')
        summary = '\n'.join(lines[:15])  # 前15行
        print(f"报告摘要:\n{summary[:200]}...")
        
        # 检查报告文件
        import os
        if os.path.exists('fund_reports/'):
            files = os.listdir('fund_reports/')
            if files:
                latest = max(files)
                print(f"📁 最新报告文件: fund_reports/{latest}")
    else:
        print(f"❌ 报告生成失败: {result.stderr}")
    
    return result.returncode == 0

def main():
    """主函数"""
    print("🚀 即时功能测试")
    print("=" * 50)
    
    # 测试1: 直接消息发送
    msg_success = test_direct_message()
    
    print("\n" + "-" * 50)
    
    # 测试2: 报告生成
    report_success = test_report_generation()
    
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    print(f"• 直接消息发送: {'✅ 成功' if msg_success else '❌ 失败'}")
    print(f"• 报告生成: {'✅ 成功' if report_success else '❌ 失败'}")
    print(f"• 综合状态: {'🟢 正常' if msg_success and report_success else '🔴 异常'}")
    
    if msg_success:
        print(f"\n📨 测试消息应该已发送")
        print(f"   请检查微信是否收到")
    else:
        print(f"\n🔧 需要进一步排查:")
        print(f"   1. 检查OpenClaw网关状态")
        print(f"   2. 检查微信通道配置")
        print(f"   3. 检查网络连接")
    
    print(f"\n🐉 测试完成于 {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()