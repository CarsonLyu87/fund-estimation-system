#!/bin/bash
# 每日基金摘要启动脚本

echo "📅 $(date '+%Y-%m-%d %H:%M:%S') - 开始基金报告"
cd /Users/carson/.openclaw/workspace

# 运行摘要脚本
python3 daily_fund_summary.py

# 记录运行状态
if [ $? -eq 0 ]; then
    echo "✅ $(date '+%H:%M:%S') - 报告完成"
else
    echo "❌ $(date '+%H:%M:%S') - 报告失败"
fi
