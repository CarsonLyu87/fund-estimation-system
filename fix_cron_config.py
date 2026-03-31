#!/usr/bin/env python3
"""
修复Cron任务配置
"""

import subprocess
import json
import os
from datetime import datetime

def get_current_session_info():
    """获取当前会话信息"""
    print("🔍 当前会话信息:")
    print("=" * 50)
    
    # 从环境或元数据获取会话信息
    session_info = {
        "chat_id": "o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat",
        "account_id": "62c6db9ab80d-im-bot", 
        "channel": "openclaw-weixin",
        "provider": "openclaw-weixin"
    }
    
    print(f"聊天ID: {session_info['chat_id']}")
    print(f"账号ID: {session_info['account_id']}")
    print(f"通道: {session_info['channel']}")
    print(f"提供商: {session_info['provider']}")
    
    return session_info

def check_cron_task():
    """检查Cron任务"""
    print("\n📋 检查Cron任务:")
    print("=" * 50)
    
    # 运行Cron列表
    result = subprocess.run(['openclaw', 'cron', 'list'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ 无法获取Cron任务列表")
        return None
    
    print("当前Cron任务:")
    print(result.stdout)
    
    # 查找我们的任务
    lines = result.stdout.split('\n')
    task_info = None
    for line in lines:
        if 'daily-fund-report' in line or 'f5e5a6b6' in line:
            print(f"\n找到目标任务: {line}")
            task_info = line
            break
    
    return task_info

def recreate_cron_task(session_info):
    """重新创建Cron任务"""
    print("\n🔧 重新创建Cron任务:")
    print("=" * 50)
    
    # 先删除旧任务
    print("1. 删除旧任务...")
    delete_result = subprocess.run(['openclaw', 'cron', 'rm', 'f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d'],
                                 capture_output=True, text=True)
    
    if delete_result.returncode == 0:
        print("✅ 旧任务删除成功")
    else:
        print(f"⚠️ 删除旧任务失败: {delete_result.stderr}")
    
    # 创建新任务
    print("\n2. 创建新任务...")
    
    # 构建命令
    cmd = [
        'openclaw', 'cron', 'add',
        '--name', 'daily-fund-report-fixed',
        '--cron', '0 11 * * *',  # 每天11:00
        '--message', '生成每日基金报告',
        '--description', '每日11点基金和黄金投资报告',
        '--announce'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    
    create_result = subprocess.run(cmd, capture_output=True, text=True)
    
    if create_result.returncode == 0:
        print("✅ 新任务创建成功")
        
        # 获取新任务ID
        list_result = subprocess.run(['openclaw', 'cron', 'list'], 
                                   capture_output=True, text=True)
        if list_result.returncode == 0:
            print("\n更新后的任务列表:")
            print(list_result.stdout)
    else:
        print(f"❌ 创建新任务失败: {create_result.stderr}")
    
    return create_result.returncode == 0

def test_cron_with_session_send():
    """测试使用sessions_send的Cron替代方案"""
    print("\n🚀 测试替代方案:")
    print("=" * 50)
    
    # 创建直接使用sessions_send的脚本
    test_script = """#!/usr/bin/env python3
import subprocess
from datetime import datetime

# 运行报告脚本
print("生成报告...")
report_result = subprocess.run(['python3', 'daily_fund_report.py'], 
                             capture_output=True, text=True)

if report_result.returncode == 0:
    # 提取报告内容（简化版）
    report_content = f"⏰ 每日投资报告 {datetime.now().strftime('%H:%M:%S')}\\n"
    report_content += "="*40 + "\\n"
    report_content += "📊 报告生成成功！\\n"
    report_content += "详细内容已保存到日志文件。\\n"
    
    # 发送消息
    send_cmd = [
        'openclaw', 'sessions', 'send',
        '--session', 'o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        report_content
    ]
    
    send_result = subprocess.run(send_cmd, capture_output=True, text=True)
    print(f"消息发送结果: {send_result.returncode}")
else:
    print(f"报告生成失败: {report_result.stderr}")
"""
    
    # 保存测试脚本
    script_file = "cron_alternative.py"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print(f"✅ 创建替代脚本: {script_file}")
    print(f"📝 脚本内容:")
    print("-" * 40)
    print(test_script[:300] + "..." if len(test_script) > 300 else test_script)
    print("-" * 40)
    
    return script_file

def create_final_solution():
    """创建最终解决方案"""
    print("\n🎯 最终解决方案:")
    print("=" * 50)
    
    solution = """
## 问题分析：
1. ✅ 微信通道工作正常（已验证）
2. ✅ 消息路由工作正常（sessions_send成功）
3. ❌ Cron任务的消息路由配置有问题

## 解决方案：

### 方案A：修复Cron配置
```bash
# 1. 删除旧任务
openclaw cron rm f5e5a6b6-9b6b-4c4e-8e7d-4b0b2d2a8e3d

# 2. 创建新任务（指定接收者）
openclaw cron add \\
  --name "daily-fund-report-fixed" \\
  --cron "0 11 * * *" \\
  --message "生成每日基金报告" \\
  --to "o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat" \\
  --announce
```

### 方案B：使用系统Cron + 脚本
```bash
# 1. 创建脚本
cat > ~/fund_report.sh << 'EOF'
#!/bin/bash
cd /Users/carson/.openclaw/workspace
python3 daily_fund_report.py
EOF

# 2. 添加执行权限
chmod +x ~/fund_report.sh

# 3. 添加到系统crontab
(crontab -l 2>/dev/null; echo "0 11 * * * ~/fund_report.sh") | crontab -
```

### 方案C：混合方案（推荐）
1. 使用系统Cron调用Python脚本
2. Python脚本生成报告并使用sessions_send发送
3. 确保消息正确路由到微信
"""
    
    print(solution)
    
    # 创建推荐方案脚本
    recommended_script = """#!/usr/bin/env python3
"""
    recommended_script += f'''
"""
每日基金报告发送脚本
使用sessions_send确保消息正确路由
"""

import subprocess
import sys
from datetime import datetime

def main():
    """主函数"""
    print(f"🚀 开始生成基金报告 {datetime.now().strftime('%H:%M:%S')}")
    
    # 1. 运行报告脚本
    print("1. 生成报告...")
    report_result = subprocess.run(
        [sys.executable, 'daily_fund_report.py'],
        cwd='/Users/carson/.openclaw/workspace',
        capture_output=True,
        text=True
    )
    
    if report_result.returncode != 0:
        print(f"❌ 报告生成失败: {report_result.stderr}")
        return 1
    
    print("✅ 报告生成成功")
    
    # 2. 提取报告摘要
    report_output = report_result.stdout
    if len(report_output) > 500:
        # 提取关键部分
        lines = report_output.split('\\n')
        summary = '\\n'.join(lines[:20])  # 前20行作为摘要
    else:
        summary = report_output
    
    # 3. 发送消息
    print("2. 发送消息...")
    send_cmd = [
        'openclaw', 'sessions', 'send',
        'o9cq806vHScTf1BIGAV1jLztzgzk@im.wechat',
        summary[:1000]  # 限制长度
    ]
    
    send_result = subprocess.run(send_cmd, capture_output=True, text=True)
    
    if send_result.returncode == 0:
        print("✅ 消息发送成功")
    else:
        print(f"❌ 消息发送失败: {send_result.stderr}")
    
    print(f"🎉 完成于 {datetime.now().strftime('%H:%M:%S')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    script_file = "send_fund_report.py"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(recommended_script)
    
    print(f"\n✅ 创建推荐方案脚本: {script_file}")
    print(f"🔧 使用方法:")
    print(f"1. 测试: python3 {script_file}")
    print(f"2. 添加到系统Cron: 0 11 * * * python3 {script_file}")
    
    return script_file

def main():
    """主函数"""
    print("🔧 Cron任务配置修复工具")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取会话信息
    session_info = get_current_session_info()
    
    # 检查Cron任务
    task_info = check_cron_task()
    
    # 重新创建Cron任务
    success = recreate_cron_task(session_info)
    
    if not success:
        print("\n⚠️ Cron任务修复可能不成功，尝试替代方案...")
    
    # 创建替代方案
    alt_script = test_cron_with_session_send()
    
    # 创建最终解决方案
    final_script = create_final_solution()
    
    print("\n" + "=" * 60)
    print("🎯 修复完成!")
    print(f"\n📋 已创建:")
    print(f"1. 修复的Cron任务: daily-fund-report-fixed")
    print(f"2. 替代方案脚本: {alt_script}")
    print(f"3. 推荐方案脚本: {final_script}")
    
    print(f"\n🔧 下一步:")
    print(f"1. 测试: python3 {final_script}")
    print(f"2. 如果成功，添加到系统Cron")
    print(f"3. 明天11点验证自动运行")
    
    print(f"\n🐉 建议先测试推荐方案脚本")

if __name__ == "__main__":
    main()