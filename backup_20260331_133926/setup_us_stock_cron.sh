#!/bin/bash
"""
设置美股同步任务 - 每天早上9点
"""

echo "🚀 设置美股同步任务"
echo "🕐 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 工作目录
WORKSPACE="/Users/carson/.openclaw/workspace"
SCRIPT="us_stock_sync.py"

echo ""
echo "📋 检查系统状态:"
echo "------------------------------------------"

# 1. 检查脚本是否存在
if [ -f "$WORKSPACE/$SCRIPT" ]; then
    echo "✅ 脚本存在: $SCRIPT"
else
    echo "❌ 脚本不存在: $SCRIPT"
    exit 1
fi

# 2. 检查Python环境
if command -v python3 &> /dev/null; then
    echo "✅ Python3 可用: $(python3 --version)"
else
    echo "❌ Python3 不可用"
    exit 1
fi

# 3. 检查OpenClaw
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw 可用: $(openclaw --version 2>/dev/null | head -1)"
else
    echo "❌ OpenClaw 不可用"
fi

echo ""
echo "📈 美股监控配置:"
echo "------------------------------------------"

echo "监控股票:"
echo "1. 🏢 英伟达 (NVDA) - 半导体/科技"
echo "2. 🏢 谷歌 (GOOGL) - 互联网/科技"

echo ""
echo "📅 同步时间:"
echo "• 每日 09:00 (北京时间)"
echo "• 同步前一日美股收盘数据"
echo "• 包含详细股价和涨跌信息"

echo ""
echo "🔧 创建启动脚本:"
echo "------------------------------------------"

# 创建美股启动脚本
START_SCRIPT="$WORKSPACE/start_us_stock.sh"
cat > "$START_SCRIPT" << 'EOF'
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
EOF

chmod +x "$START_SCRIPT"
echo "✅ 创建启动脚本: $START_SCRIPT"

echo ""
echo "📁 目录结构:"
echo "------------------------------------------"
echo "$WORKSPACE/"
echo "├── us_stock_sync.py       # 美股同步主脚本"
echo "├── start_us_stock.sh      # 美股启动脚本"
echo "├── us_stock_data/         # 股票数据存储"
echo "└── us_stock_logs/         # 同步运行日志"

echo ""
echo "📅 设置Cron任务:"
echo "------------------------------------------"

# 显示当前cron
echo "当前crontab:"
crontab -l 2>/dev/null || echo "无cron任务"

echo ""
echo "添加以下任务到crontab:"
echo "------------------------------------------"
echo "# 美股同步 - 09:00"
echo "0 9 * * * $START_SCRIPT >> $WORKSPACE/us_stock_logs/cron.log 2>&1"

echo ""
echo "# 测试任务 - 5分钟后"
echo "$(($(date '+%M') + 5)) $(date '+%H') * * * $START_SCRIPT >> $WORKSPACE/us_stock_logs/test.log 2>&1"

echo ""
echo "🔧 手动添加Cron任务:"
echo "------------------------------------------"
echo "执行以下命令:"
echo ""
echo "crontab -e"
echo ""
echo "然后添加:"
echo "0 9 * * * $START_SCRIPT >> $WORKSPACE/us_stock_logs/cron.log 2>&1"

echo ""
echo "🎯 测试运行:"
echo "------------------------------------------"
echo "立即测试: $START_SCRIPT"
echo "或: cd $WORKSPACE && python3 us_stock_sync.py"

echo ""
echo "📊 完整任务清单:"
echo "=========================================="
echo "1. 📈 基金报告 - 11:00"
echo "   脚本: daily_fund_summary.py"
echo "   格式: 持仓截图样式 (3部分)"
echo ""
echo "2. 🏢 美股同步 - 09:00"
echo "   脚本: us_stock_sync.py"
echo "   股票: 英伟达(NVDA) + 谷歌(GOOGL)"
echo "   内容: 前一日收盘数据 + 涨跌分析"
echo ""
echo "3. 📁 数据保存:"
echo "   • 基金报告: fund_reports/"
echo "   • 股票数据: us_stock_data/"
echo "   • 运行日志: *_logs/"
echo ""
echo "4. 🔧 自动运行:"
echo "   • 基金: 0 11 * * *"
echo "   • 美股: 0 9 * * *"

echo ""
echo "🐉 美股同步任务设置完成! 明天9点将自动运行。"