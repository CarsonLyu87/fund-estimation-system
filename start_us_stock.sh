#!/bin/bash
# 美股同步启动脚本

echo "📅 $(date '+%Y-%m-%d %H:%M:%S') - 开始美股同步"
cd /Users/carson/.openclaw/workspace

# 运行美股同步脚本
python3 us_stock_sync.py

# 记录运行状态
if [ $? -eq 0 ]; then
    echo "✅ $(date '+%H:%M:%S') - 美股同步完成"
else
    echo "❌ $(date '+%H:%M:%S') - 美股同步失败"
fi
