#!/usr/bin/env python3
"""
微信通道配置向导
"""

import os
import json
from datetime import datetime

def check_prerequisites():
    """检查前提条件"""
    print("🔍 检查微信通道配置前提条件:")
    print("=" * 50)
    
    checks = []
    
    # 1. 检查OpenClaw版本
    print("\n1. OpenClaw版本检查...")
    import subprocess
    result = subprocess.run(['openclaw', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ {result.stdout.strip()}")
        checks.append(True)
    else:
        print("   ❌ 无法获取版本信息")
        checks.append(False)
    
    # 2. 检查网关状态
    print("\n2. 网关状态检查...")
    result = subprocess.run(['openclaw', 'gateway', 'status'], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ 网关运行正常")
        checks.append(True)
    else:
        print("   ❌ 网关未运行")
        checks.append(False)
    
    # 3. 检查配置目录
    print("\n3. 配置目录检查...")
    config_dir = os.path.expanduser("~/.openclaw/channels")
    if os.path.exists(config_dir):
        print(f"   ✅ 配置目录存在: {config_dir}")
        checks.append(True)
    else:
        print(f"   ⚠️  配置目录不存在，将创建")
        checks.append(True)
    
    return all(checks)

def get_weixin_config():
    """获取微信配置信息"""
    print("\n📱 微信通道配置信息")
    print("=" * 50)
    
    print("\n你需要准备以下信息:")
    print("\n🔑 必需信息:")
    print("1. 微信账号ID (accountId)")
    print("   • 你的微信唯一标识")
    print("   • 格式如: wxid_xxxxxxxxxxxxxx")
    
    print("\n2. 访问令牌 (token)")
    print("   • 微信开放平台的访问令牌")
    print("   • 或第三方服务的API密钥")
    
    print("\n3. 消息端点 (endpoint)")
    print("   • 消息接收的URL地址")
    print("   • 通常为: https://api.openclaw.ai/v1/weixin")
    
    print("\n📝 可选信息:")
    print("• 通道名称 (name) - 默认: '微信个人号'")
    print("• 描述 (description) - 通道说明")
    print("• 启用状态 (enabled) - 默认: true")
    
    print("\n💡 如何获取这些信息:")
    print("1. 如果你使用OpenClaw官方微信服务:")
    print("   • 访问: https://app.openclaw.ai")
    print("   • 在控制台获取配置信息")
    
    print("\n2. 如果你使用第三方微信机器人:")
    print("   • 查看对应服务的文档")
    print("   • 获取API密钥和端点")
    
    print("\n3. 如果你自建微信服务:")
    print("   • 需要部署微信消息服务器")
    print("   • 配置公网可访问的URL")
    
    return {}

def generate_config_template():
    """生成配置模板"""
    print("\n📄 微信通道配置模板")
    print("=" * 50)
    
    template = {
        "type": "weixin",
        "name": "微信个人号",
        "description": "个人微信消息通道",
        "enabled": True,
        "config": {
            "accountId": "YOUR_WECHAT_ACCOUNT_ID",
            "token": "YOUR_ACCESS_TOKEN",
            "endpoint": "https://api.openclaw.ai/v1/weixin",
            "webhook": {
                "url": "YOUR_WEBHOOK_URL",
                "secret": "YOUR_WEBHOOK_SECRET"
            }
        }
    }
    
    print("\nJSON配置格式:")
    print(json.dumps(template, indent=2, ensure_ascii=False))
    
    # 保存模板文件
    template_file = "weixin_config_template.json"
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 模板已保存: {template_file}")
    
    return template_file

def setup_instructions():
    """提供设置说明"""
    print("\n🔧 微信通道设置步骤")
    print("=" * 50)
    
    print("\n方法A: 使用命令行配置")
    print("1. 准备配置信息")
    print("2. 运行配置命令:")
    print("""
   openclaw channels add weixin \\
     --name "微信个人号" \\
     --account-id "你的微信ID" \\
     --token "你的访问令牌" \\
     --endpoint "https://api.openclaw.ai/v1/weixin"
    """)
    
    print("\n方法B: 手动创建配置文件")
    print("1. 编辑模板文件:")
    print("   nano weixin_config_template.json")
    print("\n2. 填写你的配置信息")
    print("\n3. 复制到配置目录:")
    print("   cp weixin_config_template.json ~/.openclaw/channels/openclaw-weixin.json")
    
    print("\n方法C: 使用OpenClaw官方服务")
    print("1. 访问 https://app.openclaw.ai")
    print("2. 注册并登录")
    print("3. 在控制台配置微信通道")
    print("4. 获取自动生成的配置")
    
    print("\n🔄 配置完成后:")
    print("1. 重启网关:")
    print("   openclaw gateway restart")
    print("\n2. 测试消息发送:")
    print("   openclaw message send '测试消息'")
    print("\n3. 测试Cron任务:")
    print("   openclaw cron run f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d")

def quick_test_option():
    """快速测试选项"""
    print("\n🚀 快速测试方案")
    print("=" * 50)
    
    print("\n如果微信通道配置复杂，可先测试其他通道:")
    
    print("\n1. 测试本地文件输出 (当前使用)")
    print("   ✅ 已实现: generate_report_only.py")
    print("   📁 报告保存到: local_reports/")
    
    print("\n2. 测试控制台输出")
    print("""
   # 修改daily_fund_report.py
   # 添加: print(report_content)
   # 然后直接运行查看输出
    """)
    
    print("\n3. 测试其他简单通道")
    print("""
   # 测试文件通道
   openclaw channels add file --path ./messages.txt
   
   # 测试HTTP通道
   openclaw channels add http --url http://localhost:8080/webhook
    """)

def main():
    """主函数"""
    print("🚀 微信通道配置向导")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查前提条件
    if not check_prerequisites():
        print("\n❌ 前提条件检查失败，请先解决问题")
        return
    
    # 获取配置信息说明
    get_weixin_config()
    
    # 生成配置模板
    template_file = generate_config_template()
    
    # 设置说明
    setup_instructions()
    
    # 快速测试选项
    quick_test_option()
    
    print("\n" + "=" * 60)
    print("🎯 总结:")
    print("1. 微信通道需要特定配置信息")
    print("2. 已生成配置模板: weixin_config_template.json")
    print("3. 按照步骤填写信息并配置")
    print("4. 或先使用本地报告系统")
    
    print(f"\n🐉 请提供微信通道的配置信息，或选择其他方案")

if __name__ == "__main__":
    main()