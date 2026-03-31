#!/bin/bash

# 设置每日美股报告自动化脚本
# 运行: bash setup_daily_report.sh

echo "📊 设置每日美股报告系统"
echo "="============================

# 1. 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js"
    exit 1
fi

echo "✅ Node.js版本: $(node --version)"

# 2. 创建报告目录
REPORT_DIR="/Users/carson/.openclaw/workspace/reports"
MEMORY_DIR="/Users/carson/.openclaw/workspace/memory"

mkdir -p "$REPORT_DIR"
mkdir -p "$MEMORY_DIR"

echo "✅ 创建目录:"
echo "   - 报告目录: $REPORT_DIR"
echo "   - 记忆目录: $MEMORY_DIR"

# 3. 测试报告生成
echo ""
echo "🧪 测试报告生成..."
cd /Users/carson/.openclaw/workspace
node us_stock_daily_report.js

if [ $? -eq 0 ]; then
    echo "✅ 报告生成测试成功"
else
    echo "❌ 报告生成测试失败"
    exit 1
fi

# 4. 创建OpenClaw定时任务配置
echo ""
echo "⏰ 创建OpenClaw定时任务..."

# 检查OpenClaw配置目录
OPENCLAW_CONFIG_DIR="/Users/carson/.openclaw"
if [ ! -d "$OPENCLAW_CONFIG_DIR" ]; then
    echo "❌ OpenClaw配置目录不存在: $OPENCLAW_CONFIG_DIR"
    exit 1
fi

# 创建cron任务配置
CRON_CONFIG="$OPENCLAW_CONFIG_DIR/cron.json"
if [ ! -f "$CRON_CONFIG" ]; then
    cat > "$CRON_CONFIG" << EOF
{
  "jobs": [
    {
      "id": "us-stock-daily-report",
      "name": "每日美股报告",
      "schedule": "0 9 * * *",
      "timezone": "Asia/Shanghai",
      "command": "node /Users/carson/.openclaw/workspace/us_stock_daily_report.js",
      "cwd": "/Users/carson/.openclaw/workspace",
      "output": "file:/Users/carson/.openclaw/workspace/reports/cron_log.txt",
      "enabled": true,
      "description": "每日9点生成美股科技股报告"
    }
  ]
}
EOF
    echo "✅ 创建cron配置: $CRON_CONFIG"
else
    echo "⚠️ cron配置已存在: $CRON_CONFIG"
    echo "   请手动添加美股报告任务"
fi

# 5. 创建手动运行脚本
cat > /Users/carson/.openclaw/workspace/run_daily_report.sh << 'EOF'
#!/bin/bash
# 手动运行每日美股报告

cd /Users/carson/.openclaw/workspace
node us_stock_daily_report.js

# 如果微信通知已配置，可以添加发送逻辑
# openclaw send --channel weixin --message "美股报告已生成"
EOF

chmod +x /Users/carson/.openclaw/workspace/run_daily_report.sh

echo "✅ 创建手动运行脚本: run_daily_report.sh"

# 6. 创建今日报告快捷方式
cat > /Users/carson/.openclaw/workspace/today_report.sh << 'EOF'
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
EOF

chmod +x /Users/carson/.openclaw/workspace/today_report.sh

echo "✅ 创建今日报告查看脚本: today_report.sh"

# 7. 创建配置说明
cat > /Users/carson/.openclaw/workspace/REPORT_SYSTEM_README.md << 'EOF'
# 每日美股报告系统

## 功能
每日9点自动生成美股科技股报告，包含：
- 市场概况
- 涨幅榜/跌幅榜
- 板块分析
- 特别关注
- 今日展望

## 文件结构
```
workspace/
├── us_stock_report_config.json    # 配置文件
├── us_stock_daily_report.js       # 主程序
├── run_daily_report.sh            # 手动运行脚本
├── today_report.sh                # 查看今日报告
├── reports/                       # 报告保存目录
└── memory/                        # 记忆文件目录
```

## 使用方法

### 1. 手动生成报告
```bash
./run_daily_report.sh
```

### 2. 查看今日报告
```bash
./today_report.sh
```

### 3. 查看历史报告
```bash
ls -la reports/
cat reports/us_stock_report_2026-03-26.md
```

### 4. 配置OpenClaw定时任务
系统已自动配置每日9点运行。如需修改：
```bash
openclaw cron list
openclaw cron edit
```

## 监控股票列表
在 `us_stock_report_config.json` 中配置，包含：
- 苹果(AAPL)、微软(MSFT)、谷歌(GOOGL)
- 亚马逊(AMZN)、Meta(META)、特斯拉(TSLA)
- 英伟达(NVDA)、AMD、英特尔(INTC)
- 奈飞(NFLX)、博通(AVGO)、Salesforce(CRM)

## 数据源
- 主要: 腾讯财经API (免费、无限制)
- 备用: 新浪财经

## 报告示例
报告保存为Markdown格式，便于阅读和分享。
EOF

echo "✅ 创建系统说明文档: REPORT_SYSTEM_README.md"

# 8. 总结
echo ""
echo "="============================
echo "🎉 每日美股报告系统设置完成！"
echo "="============================
echo ""
echo "📋 可用命令:"
echo "  ./run_daily_report.sh    # 手动生成报告"
echo "  ./today_report.sh        # 查看今日报告"
echo "  openclaw cron list       # 查看定时任务"
echo ""
echo "📅 报告时间: 每日 09:00 (北京时间)"
echo "📊 监控股票: 12只科技股"
echo "💾 报告保存: workspace/reports/"
echo ""
echo "💡 提示: 系统将在明日9点自动运行"
echo "       如需立即测试，请运行: ./run_daily_report.sh"