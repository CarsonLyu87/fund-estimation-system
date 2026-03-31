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
