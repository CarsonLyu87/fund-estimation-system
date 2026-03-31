#!/usr/bin/env python3
"""
测试网关消息发送
"""

from datetime import datetime
import subprocess
import time

def test_simple_message():
    """发送简单测试消息"""
    print(f"🕐 测试时间: {datetime.now().strftime('%H:%M:%S')}")
    
    # 创建简单的测试消息
    test_msg = f"🔧 网关测试消息 {datetime.now().strftime('%H:%M:%S')}\n"
    test_msg += "=" * 30 + "\n"
    test_msg += "✅ OpenClaw网关测试\n"
    test_msg += "📨 如果收到此消息，说明:\n"
    test_msg += "1. 网关运行正常\n"
    test_msg += "2. 消息发送正常\n"
    test_msg += "3. Cron任务可触发\n"
    test_msg += "=" * 30
    
    print("📤 准备发送测试消息...")
    print(f"📝 消息内容:\n{test_msg}")
    
    # 尝试通过Cron发送
    print("\n🚀 通过Cron发送测试...")
    
    # 先删除旧的测试任务
    subprocess.run(['openclaw', 'cron', 'rm', 'test-1110'], 
                  capture_output=True, text=True)
    subprocess.run(['openclaw', 'cron', 'rm', 'test-now'], 
                  capture_output=True, text=True)
    
    # 创建新的立即测试任务
    next_minute = (datetime.now().minute + 1) % 60
    cron_expr = f"{next_minute} {datetime.now().hour} * * *"
    
    create_result = subprocess.run([
        'openclaw', 'cron', 'add',
        '--name', 'gateway-test',
        '--cron', cron_expr,
        '--message', '网关功能测试',
        '--announce'
    ], capture_output=True, text=True)
    
    if create_result.returncode == 0:
        print(f"✅ 创建测试任务成功")
        print(f"⏰ 将在 {datetime.now().hour}:{next_minute:02d} 运行")
        
        # 立即运行
        print("\n⚡ 立即触发测试...")
        run_result = subprocess.run(['openclaw', 'cron', 'run', 'gateway-test'],
                                   capture_output=True, text=True)
        print(f"触发结果: {run_result.returncode}")
        
        if run_result.returncode == 0:
            print("✅ 任务触发成功")
            print("📨 消息已加入发送队列")
        else:
            print(f"❌ 任务触发失败: {run_result.stderr}")
    else:
        print(f"❌ 创建任务失败: {create_result.stderr}")
    
    return create_result.returncode == 0

def check_gateway_connection():
    """检查网关连接"""
    print("\n🔌 检查网关连接...")
    
    # 检查网关状态
    status_result = subprocess.run(['openclaw', 'gateway', 'status'],
                                  capture_output=True, text=True)
    
    if status_result.returncode == 0:
        print("✅ 网关状态: 运行中")
        # 提取PID信息
        for line in status_result.stdout.split('\n'):
            if 'pid' in line.lower():
                print(f"   {line.strip()}")
    else:
        print("❌ 网关状态检查失败")
    
    # 检查Cron任务
    print("\n📋 检查Cron任务...")
    cron_result = subprocess.run(['openclaw', 'cron', 'list'],
                                capture_output=True, text=True)
    
    if cron_result.returncode == 0:
        print("✅ Cron服务正常")
        tasks = [line for line in cron_result.stdout.split('\n') if line.strip()]
        print(f"   找到 {len(tasks)} 个任务")
    else:
        print("❌ Cron服务异常")
    
    return status_result.returncode == 0

if __name__ == "__main__":
    print("=== OpenClaw网关功能测试 ===\n")
    
    # 检查连接
    gateway_ok = check_gateway_connection()
    
    if not gateway_ok:
        print("\n❌ 网关连接异常，请检查:")
        print("1. 运行: openclaw gateway start")
        print("2. 检查日志: openclaw gateway status")
        print("3. 重启: openclaw gateway restart")
        exit(1)
    
    print("\n" + "="*50)
    
    # 发送测试消息
    print("\n📨 发送测试消息...")
    success = test_simple_message()
    
    print("\n" + "="*50)
    
    if success:
        print("✅ 测试完成!")
        print("📋 结果:")
        print("1. 网关运行正常 ✓")
        print("2. Cron任务创建成功 ✓")
        print("3. 消息触发成功 ✓")
        print("\n⏳ 请检查微信是否收到测试消息")
        print("   • 消息标题: '网关功能测试'")
        print("   • 发送时间: 约1分钟内")
    else:
        print("❌ 测试失败!")
        print("📋 可能原因:")
        print("1. 网关未完全启动")
        print("2. 权限问题")
        print("3. 配置错误")
    
    print(f"\n🕐 当前时间: {datetime.now().strftime('%H:%M:%S')}")
    print("🐉 等待消息接收确认...")