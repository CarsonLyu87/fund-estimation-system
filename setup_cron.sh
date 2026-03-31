#!/bin/bash
# 设置每日基金报告cron任务

echo "正在设置每日基金报告定时任务..."

# 创建cron任务
CRON_JOB="0 11 * * * cd /Users/carson/.openclaw/workspace && /usr/bin/python3 daily_fund_summary.py"

# 添加到crontab
echo "$CRON_JOB" | crontab -

# 验证设置
echo "✅ 定时任务已设置:"
crontab -l

echo ""
echo "📅 任务将在每天11:00执行"
echo "📁 报告将保存在: /Users/carson/.openclaw/workspace/fund_reports/"
echo "📝 日志将保存在: /Users/carson/.openclaw/workspace/fund_logs/"