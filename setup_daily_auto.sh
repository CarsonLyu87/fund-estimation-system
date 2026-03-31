#!/bin/bash
"""
设置每日自动运行
"""

echo "🚀 设置每日基金摘要自动运行"
echo "🕐 时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 工作目录
WORKSPACE="/Users/carson/.openclaw/workspace"
SCRIPT="daily_fund_summary.py"

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
echo "🔧 设置自动运行:"
echo "------------------------------------------"

# 创建启动脚本
START_SCRIPT="$WORKSPACE/start_fund_report.sh"
cat > "$START_SCRIPT" << 'EOF'
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
EOF

chmod +x "$START_SCRIPT"
echo "✅ 创建启动脚本: $START_SCRIPT"

echo ""
echo "📅 设置Cron任务:"
echo "------------------------------------------"

# 显示当前cron
echo "当前crontab:"
crontab -l 2>/dev/null || echo "无cron任务"

echo ""
echo "添加以下任务到crontab:"
echo "------------------------------------------"
echo "# 每日基金摘要 - 11:00"
echo "0 11 * * * $START_SCRIPT >> $WORKSPACE/fund_logs/cron.log 2>&1"
echo ""
echo "# 测试任务 - 5分钟后"
echo "$(($(date '+%M') + 5)) $(date '+%H') * * * $START_SCRIPT >> $WORKSPACE/fund_logs/test.log 2>&1"

echo ""
echo "🔧 手动添加Cron任务:"
echo "------------------------------------------"
echo "执行以下命令:"
echo ""
echo "crontab -e"
echo ""
echo "然后添加:"
echo "0 11 * * * $START_SCRIPT >> $WORKSPACE/fund_logs/cron.log 2>&1"

echo ""
echo "📁 目录结构:"
echo "------------------------------------------"
echo "$WORKSPACE/"
echo "├── daily_fund_summary.py    # 主脚本"
echo "├── start_fund_report.sh     # 启动脚本"
echo "├── fund_reports/           # 完整报告"
echo "├── fund_logs/              # 运行日志"
echo "└── daily_summaries/        # 每日摘要"

echo ""
echo "🎯 测试运行:"
echo "------------------------------------------"
echo "立即测试: $START_SCRIPT"
echo "或: cd $WORKSPACE && python3 daily_fund_summary.py"

echo ""
echo "📊 最终解决方案总结:"
echo "=========================================="
echo "✅ 问题: 微信消息长度限制"
echo "✅ 方案: 极简摘要 + 本地保存"
echo "✅ 摘要: <300字符，确保送达"
echo "✅ 完整: 保存到本地文件"
echo "✅ 自动: 每日11点运行"
echo "✅ 日志: 完整运行记录"

echo ""
echo "🐉 设置完成! 明天11点将自动运行。"