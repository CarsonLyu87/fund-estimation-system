#!/bin/bash
# 查看今日报告

TODAY=$(date +%Y-%m-%d)
REPORT_FILE="/Users/carson/.openclaw/workspace/reports/us_stock_report_${TODAY}.md"

if [ -f "$REPORT_FILE" ]; then
    echo "📄 今日美股报告 ($TODAY):"
    echo "="============================
    head -100 "$REPORT_FILE"
else
    echo "❌ 今日报告尚未生成"
    echo "运行: ./run_daily_report.sh 生成报告"
fi
