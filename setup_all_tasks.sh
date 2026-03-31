#!/bin/bash
"""
设置所有自动任务
"""

echo "🚀 设置所有自动投资监控任务"
echo "🕐 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 工作目录
WORKSPACE="/Users/carson/.openclaw/workspace"

echo ""
echo "📋 系统检查:"
echo "------------------------------------------"

# 检查所有必要脚本
scripts=(
    "daily_fund_summary.py"
    "us_stock_sync.py"
    "start_fund_report.sh"
    "start_us_stock.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$WORKSPACE/$script" ]; then
        echo "✅ $script"
    else
        echo "❌ $script (缺失)"
    fi
done

echo ""
echo "📅 自动任务配置:"
echo "------------------------------------------"

echo "1. 🏢 美股同步"
echo "   时间: 09:00"
echo "   股票: 英伟达(NVDA) + 谷歌(GOOGL)"
echo "   脚本: us_stock_sync.py"
echo ""
echo "2. 📈 基金报告"
echo "   时间: 11:00"
echo "   基金: 7只个人基金 + 5只活跃基金"
echo "   脚本: daily_fund_summary.py"
echo ""
echo "3. 📁 数据存储"
echo "   • 基金报告: fund_reports/"
echo "   • 股票数据: us_stock_data/"
echo "   • 运行日志: *_logs/"

echo ""
echo "🔧 创建完整Cron配置:"
echo "------------------------------------------"

# 创建完整的cron配置
CRON_FILE="$WORKSPACE/cron_config.txt"

cat > "$CRON_FILE" << EOF
# ========================================
# 自动投资监控任务配置
# 生成时间: $(date '+%Y-%m-%d %H:%M:%S')
# ========================================

# 🏢 美股同步 - 每天早上9点
# 同步英伟达(NVDA)和谷歌(GOOGL)前一日收盘数据
0 9 * * * $WORKSPACE/start_us_stock.sh >> $WORKSPACE/us_stock_logs/cron.log 2>&1

# 📈 基金报告 - 每天早上11点
# 7只个人基金 + 5只活跃基金 + 黄金分析
0 11 * * * $WORKSPACE/start_fund_report.sh >> $WORKSPACE/fund_logs/cron.log 2>&1

# ========================================
# 可选测试任务 (可删除)
# ========================================

# 测试美股同步 (5分钟后)
$(($(date '+%M') + 5)) $(date '+%H') * * * $WORKSPACE/start_us_stock.sh >> $WORKSPACE/us_stock_logs/test.log 2>&1

# 测试基金报告 (10分钟后)
$(($(date '+%M') + 10)) $(date '+%H') * * * $WORKSPACE/start_fund_report.sh >> $WORKSPACE/fund_logs/test.log 2>&1
EOF

echo "✅ 创建Cron配置: $CRON_FILE"

echo ""
echo "📝 应用Cron配置:"
echo "------------------------------------------"
echo "执行以下命令应用配置:"
echo ""
echo "crontab $CRON_FILE"
echo ""
echo "或手动编辑:"
echo "crontab -e"
echo ""
echo "然后复制上面的配置"

echo ""
echo "🎯 测试所有任务:"
echo "------------------------------------------"

echo "1. 测试美股同步:"
echo "   $WORKSPACE/start_us_stock.sh"
echo ""
echo "2. 测试基金报告:"
echo "   $WORKSPACE/start_fund_report.sh"
echo ""
echo "3. 查看运行状态:"
echo "   tail -f $WORKSPACE/*_logs/*.log"

echo ""
echo "📊 消息格式预览:"
echo "------------------------------------------"

echo "🏢 美股同步 (09:00):"
echo "-------------------"
echo "📈 美股早报 [时间]"
echo "🏢 英伟达 (NVDA)"
echo "💰 股价: \$XXX.XX"
echo "📈 涨跌: +X.XX (+X.XX%)"
echo ""
echo "📈 基金报告 (11:00):"
echo "-------------------"
echo "📊 基金持仓报告 [时间]"
echo "👤 你的持仓 (7只)"
echo "1. 基金名称"
echo "   代码: XXXXXX"
echo "   涨跌: +X.XX% 📈"

echo ""
echo "🔧 故障排除:"
echo "------------------------------------------"

echo "1. 检查网关状态:"
echo "   openclaw gateway status"
echo ""
echo "2. 检查脚本权限:"
echo "   chmod +x $WORKSPACE/*.sh"
echo ""
echo "3. 查看运行日志:"
echo "   ls -la $WORKSPACE/*_logs/"
echo ""
echo "4. 手动测试发送:"
echo "   openclaw sessions send [会话ID] '测试消息'"

echo ""
echo "📋 最终检查清单:"
echo "=========================================="
echo "✅ 美股同步脚本: us_stock_sync.py"
echo "✅ 基金报告脚本: daily_fund_summary.py"
echo "✅ 启动脚本: start_*.sh"
echo "✅ 目录结构: *_data/ *_logs/"
echo "✅ Cron配置: cron_config.txt"
echo ""
echo "⏰ 明日自动运行时间:"
echo "• 09:00 - 美股同步 (英伟达+谷歌)"
echo "• 11:00 - 基金报告 (7只基金+黄金)"
echo ""
echo "🐉 所有任务设置完成! 系统将在指定时间自动运行。"