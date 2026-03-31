#!/bin/bash
# 手动运行每日美股报告

cd /Users/carson/.openclaw/workspace
node us_stock_daily_report.js

# 如果微信通知已配置，可以添加发送逻辑
# openclaw send --channel weixin --message "美股报告已生成"
