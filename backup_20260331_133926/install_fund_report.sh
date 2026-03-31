#!/bin/bash
# 安装每日基金报告定时任务

echo "📅 安装每日基金报告定时任务..."

# 确保日志目录存在
mkdir -p /Users/carson/.openclaw/workspace/fund_logs

# 复制plist文件到LaunchAgents目录
cp /Users/carson/.openclaw/workspace/com.carson.fundreport.plist ~/Library/LaunchAgents/

# 加载任务
launchctl load ~/Library/LaunchAgents/com.carson.fundreport.plist

echo "✅ 定时任务已安装"
echo ""
echo "📋 任务信息:"
echo "   - 名称: com.carson.fundreport"
echo "   - 时间: 每天11:00"
echo "   - 脚本: /Users/carson/.openclaw/workspace/daily_fund_summary.py"
echo "   - 日志: /Users/carson/.openclaw/workspace/fund_logs/launchd.log"
echo ""
echo "🔧 管理命令:"
echo "   启动: launchctl start com.carson.fundreport"
echo "   停止: launchctl stop com.carson.fundreport"
echo "   卸载: launchctl unload ~/Library/LaunchAgents/com.carson.fundreport.plist"
echo ""
echo "🎯 现在可以手动测试:"
echo "   cd /Users/carson/.openclaw/workspace && python3 daily_fund_summary.py"