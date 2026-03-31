#!/usr/bin/env python3
"""
OpenClaw全面诊断
"""

import subprocess
import json
import os
from datetime import datetime

def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n🔍 {description}:")
    print(f"   $ {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ 成功")
            if result.stdout.strip():
                output = result.stdout.strip()
                if len(output) > 200:
                    print(f"     输出: {output[:200]}...")
                else:
                    print(f"     输出: {output}")
        else:
            print(f"   ❌ 失败 (code: {result.returncode})")
            if result.stderr:
                print(f"     错误: {result.stderr[:200]}")
        return result
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  超时")
        return None
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return None

def diagnose_openclaw():
    """全面诊断OpenClaw"""
    print("=== OpenClaw 系统诊断 ===")
    print(f"诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 基本安装检查
    print("\n1. 📦 基本安装检查")
    run_command("which openclaw", "查找openclaw命令")
    run_command("openclaw --version", "版本信息")
    run_command("ls -la ~/.openclaw/", "配置文件目录")
    
    # 2. 网关状态
    print("\n2. 🔌 网关状态检查")
    run_command("openclaw gateway status", "网关状态")
    run_command("ps aux | grep openclaw | grep -v grep", "进程检查")
    
    # 3. 通道配置
    print("\n3. 📡 通道配置检查")
    run_command("openclaw channels list", "通道列表")
    run_command("ls -la ~/.openclaw/channels/ 2>/dev/null || echo '无通道目录'", "通道目录")
    
    # 4. Cron服务
    print("\n4. ⏰ Cron服务检查")
    run_command("openclaw cron list", "Cron任务列表")
    
    # 5. 配置检查
    print("\n5. ⚙️ 配置检查")
    run_command("openclaw config get", "配置获取")
    run_command("cat ~/.openclaw/config.json 2>/dev/null | head -50", "配置文件内容")
    
    # 6. 网络连接
    print("\n6. 🌐 网络连接检查")
    run_command("curl -s http://localhost:3000/health 2>/dev/null || echo '本地服务未响应'", "本地服务健康检查")
    
    # 7. 权限检查
    print("\n7. 🔐 权限检查")
    run_command("ls -la ~/.openclaw/", "目录权限")
    run_command("id", "用户信息")
    
    return True

def check_weixin_config():
    """检查微信配置"""
    print("\n" + "=" * 60)
    print("8. 💬 微信通道专项检查")
    
    # 检查微信配置文件
    weixin_config = os.path.expanduser("~/.openclaw/channels/openclaw-weixin.json")
    if os.path.exists(weixin_config):
        print(f"✅ 找到微信配置文件: {weixin_config}")
        try:
            with open(weixin_config, 'r') as f:
                config = json.load(f)
            print(f"   配置摘要:")
            print(f"   • 类型: {config.get('type', '未知')}")
            print(f"   • 名称: {config.get('name', '未知')}")
            print(f"   • 状态: {config.get('enabled', '未知')}")
            
            # 检查关键字段
            required = ['accountId', 'token', 'endpoint']
            missing = [field for field in required if not config.get(field)]
            if missing:
                print(f"   ⚠️  缺少必要字段: {missing}")
            else:
                print(f"   ✅ 必要字段完整")
                
        except Exception as e:
            print(f"   ❌ 读取配置文件失败: {e}")
    else:
        print(f"❌ 未找到微信配置文件")
        print(f"   预期位置: {weixin_config}")
    
    # 检查微信是否在通道列表中
    result = run_command("openclaw channels list --json 2>/dev/null", "通道JSON列表")
    if result and result.returncode == 0:
        try:
            channels = json.loads(result.stdout)
            weixin_channels = [c for c in channels if 'weixin' in c.get('name', '').lower()]
            if weixin_channels:
                print(f"✅ 微信通道在列表中: {len(weixin_channels)} 个")
                for channel in weixin_channels[:2]:
                    print(f"   • {channel.get('name')} - {channel.get('status', '未知')}")
            else:
                print("❌ 微信通道不在列表中")
        except:
            print("   无法解析通道列表")

def generate_fix_plan():
    """生成修复计划"""
    print("\n" + "=" * 60)
    print("🔧 修复建议")
    
    print("\n📋 可能的问题:")
    print("1. ❌ 微信通道未配置或未启用")
    print("2. ❌ 网关与通道连接失败")
    print("3. ❌ 微信账号授权过期")
    print("4. ❌ 网络连接问题")
    
    print("\n🎯 修复步骤:")
    print("1. 检查微信通道配置")
    print("   $ openclaw channels list")
    print("   $ cat ~/.openclaw/channels/openclaw-weixin.json")
    
    print("\n2. 重新配置微信通道")
    print("   # 可能需要重新扫描二维码登录")
    print("   $ openclaw channels add weixin")
    
    print("\n3. 重启网关服务")
    print("   $ openclaw gateway restart")
    
    print("\n4. 测试消息发送")
    print("   $ openclaw message send '测试消息'")
    
    print("\n5. 验证Cron任务")
    print("   $ openclaw cron run f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d")

if __name__ == "__main__":
    print("🚀 开始OpenClaw系统诊断...\n")
    
    diagnose_openclaw()
    check_weixin_config()
    generate_fix_plan()
    
    print("\n" + "=" * 60)
    print(f"✅ 诊断完成于 {datetime.now().strftime('%H:%M:%S')}")
    print("\n📝 总结:")
    print("• 网关运行正常，但微信通道可能未正确配置")
    print("• 需要检查微信通道的配置和连接状态")
    print("• 建议重新配置微信通道或检查授权状态")
    print("\n🐉 请按照修复建议逐步排查")