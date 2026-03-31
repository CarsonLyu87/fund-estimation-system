#!/usr/bin/env node
/**
 * 每日美股报告生成器
 * 运行时间: 每日09:00 (北京时间)
 * 功能: 获取昨晚美股收盘数据，生成格式化报告
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 加载配置
const configPath = path.join(__dirname, 'us_stock_report_config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// 获取当前日期
const now = new Date();
const beijingTime = new Date(now.getTime() + (8 * 60 * 60 * 1000)); // UTC+8
const reportDate = beijingTime.toISOString().split('T')[0];
const reportTime = beijingTime.toLocaleTimeString('zh-CN', { 
  hour12: false,
  hour: '2-digit',
  minute: '2-digit'
});

console.log(`📅 报告生成时间: ${reportDate} ${reportTime} (北京时间)`);
console.log(`📊 报告名称: ${config.report_name}`);
console.log('='.repeat(70));

// 准备股票代码
const stockCodes = config.stocks_to_monitor.map(s => `us${s.symbol}`).join(',');

// 获取股票数据
function fetchStockData() {
  try {
    console.log('📡 正在获取美股数据...');
    const result = execSync(`curl -s "http://qt.gtimg.cn/q=${stockCodes}"`, { 
      encoding: 'utf8',
      timeout: 10000 
    });
    
    return parseStockData(result);
  } catch (error) {
    console.error('❌ 数据获取失败:', error.message);
    return null;
  }
}

// 解析股票数据
function parseStockData(rawData) {
  const lines = rawData.split(';').filter(line => line.trim());
  const stockData = [];
  
  lines.forEach((line, index) => {
    if (index < config.stocks_to_monitor.length) {
      const parts = line.split('~');
      if (parts.length > 40) {
        const stockConfig = config.stocks_to_monitor[index];
        const currentPrice = parseFloat(parts[3]) || 0;
        const prevClose = parseFloat(parts[4]) || 0;
        const change = currentPrice - prevClose;
        const changePercent = prevClose > 0 ? (change / prevClose * 100) : 0;
        const volume = parseFloat(parts[6]) || 0;
        const turnover = parseFloat(parts[37]) || 0; // 成交额
        
        stockData.push({
          symbol: stockConfig.symbol,
          name: stockConfig.name,
          category: stockConfig.category,
          currentPrice,
          prevClose,
          change,
          changePercent,
          volume,
          turnover,
          timestamp: new Date().toISOString()
        });
      }
    }
  });
  
  return stockData;
}

// 生成报告 - 专注于前10大科技股涨跌值
function generateReport(stockData) {
  if (!stockData || stockData.length === 0) {
    console.log('❌ 无有效数据，报告生成失败');
    return;
  }
  
  // 按涨跌值排序（绝对值）
  const sortedByChangeValue = [...stockData].sort((a, b) => Math.abs(b.change) - Math.abs(a.change));
  const sortedByGain = [...stockData].filter(s => s.change > 0).sort((a, b) => b.change - a.change);
  const sortedByLoss = [...stockData].filter(s => s.change < 0).sort((a, b) => a.change - b.change);
  
  // 按板块分组
  const byCategory = {};
  stockData.forEach(stock => {
    if (!byCategory[stock.category]) {
      byCategory[stock.category] = [];
    }
    byCategory[stock.category].push(stock);
  });
  
  // 生成报告内容
  const report = [];
  
  // 1. 报告标题
  report.push(`# 📈 美股前10大科技股报告 - ${reportDate}`);
  report.push(`**报告时间**: ${reportTime} (北京时间)`);
  report.push(`**数据来源**: 腾讯财经API (美股前一交易日收盘数据)`);
  report.push('');
  
  // 2. 核心涨跌值概览
  report.push('## 💰 核心涨跌值概览');
  
  // 计算总涨跌值
  const totalChangeValue = stockData.reduce((sum, s) => sum + s.change, 0);
  const avgChangeValue = totalChangeValue / stockData.length;
  
  report.push(`- **监控股票**: ${stockData.length} 只前10大科技股`);
  report.push(`- **总涨跌值**: ${totalChangeValue >= 0 ? '+' : ''}$${totalChangeValue.toFixed(2)}`);
  report.push(`- **平均涨跌值**: ${avgChangeValue >= 0 ? '+' : ''}$${avgChangeValue.toFixed(2)}`);
  report.push('');
  
  // 3. 涨跌值排行榜
  report.push('## 🏆 涨跌值排行榜');
  
  // 涨跌值最大（正）
  report.push('### 📈 涨跌值最大 (Top 3)');
  sortedByGain.slice(0, 3).forEach((stock, i) => {
    const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : '🔸';
    report.push(`${medal} **${stock.symbol}** (${stock.name})`);
    report.push(`   - **涨跌值**: ${stock.change >= 0 ? '+' : ''}$${stock.change.toFixed(2)}`);
    report.push(`   - **涨跌幅**: ${stock.changePercent >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%`);
    report.push(`   - **当前价**: $${stock.currentPrice.toFixed(2)}`);
  });
  report.push('');
  
  // 涨跌值最大（负）
  const topLosers = sortedByLoss.filter(s => s.change < 0).slice(0, 3);
  if (topLosers.length > 0) {
    report.push('### 📉 跌值最大 (Top 3)');
    topLosers.forEach((stock, i) => {
      const icon = i === 0 ? '🔻' : i === 1 ? '🔻' : '🔻';
      report.push(`${icon} **${stock.symbol}** (${stock.name})`);
      report.push(`   - **涨跌值**: -$${Math.abs(stock.change).toFixed(2)}`);
      report.push(`   - **涨跌幅**: ${stock.changePercent.toFixed(2)}%`);
      report.push(`   - **当前价**: $${stock.currentPrice.toFixed(2)}`);
    });
  }
  report.push('');
  
  // 4. 绝对值涨跌值排名
  report.push('## 💪 绝对值涨跌值排名');
  report.push('*(按涨跌值绝对值排序，反映对指数影响大小)*');
  
  sortedByChangeValue.slice(0, 5).forEach((stock, i) => {
    const rank = i + 1;
    const trend = stock.change >= 0 ? '📈' : '📉';
    report.push(`${rank}. **${stock.symbol}** (${stock.name}) ${trend}`);
    report.push(`   - **涨跌值**: ${stock.change >= 0 ? '+' : ''}$${stock.change.toFixed(2)}`);
    report.push(`   - **涨跌幅**: ${stock.changePercent >= 0 ? '+' : ''}${stock.changePercent.toFixed(2)}%`);
    report.push(`   - **对指数影响**: ${Math.abs(stock.change) >= 10 ? '大' : Math.abs(stock.change) >= 5 ? '中' : '小'}`);
  });
  report.push('');
  // 5. 板块涨跌值分析
  report.push('## 🏢 板块涨跌值分析');
  
  // 计算各板块总涨跌值
  const categoryChangeValues = {};
  Object.keys(byCategory).forEach(category => {
    const stocks = byCategory[category];
    const totalChange = stocks.reduce((sum, s) => sum + s.change, 0);
    const avgChange = totalChange / stocks.length;
    const gainers = stocks.filter(s => s.change > 0).length;
    categoryChangeValues[category] = { totalChange, avgChange, total: stocks.length, gainers };
  });
  
  // 按板块总涨跌值排序
  const sortedCategories = Object.keys(categoryChangeValues).sort((a, b) => 
    categoryChangeValues[b].totalChange - categoryChangeValues[a].totalChange
  );
  
  sortedCategories.forEach(category => {
    const stats = categoryChangeValues[category];
    const trend = stats.totalChange >= 0 ? '📈' : '📉';
    report.push(`### ${category} ${trend}`);
    report.push(`- **板块总涨跌值**: ${stats.totalChange >= 0 ? '+' : ''}$${stats.totalChange.toFixed(2)}`);
    report.push(`- **平均涨跌值**: ${stats.avgChange >= 0 ? '+' : ''}$${stats.avgChange.toFixed(2)}`);
    report.push(`- **上涨股票**: ${stats.gainers}/${stats.total} 只`);
    
    // 显示该板块涨跌值最大的股票
    const topStock = byCategory[category].sort((a, b) => b.change - a.change)[0];
    if (topStock) {
      report.push(`- **最大贡献**: ${topStock.symbol} (${topStock.change >= 0 ? '+' : ''}$${topStock.change.toFixed(2)})`);
    }
    report.push('');
  });
  
  // 6. 特别关注 - 基于涨跌值
  report.push('## 🔍 特别关注 (涨跌值视角)');
  
  // 大额涨跌股票
  const bigChangeStocks = sortedByChangeValue.filter(s => Math.abs(s.change) >= 5);
  if (bigChangeStocks.length > 0) {
    report.push('### 💰 大额涨跌股票 (|涨跌值| ≥ $5)');
    bigChangeStocks.forEach(stock => {
      const trend = stock.change >= 0 ? '📈' : '📉';
      report.push(`${trend} **${stock.symbol}** (${stock.name}): ${stock.change >= 0 ? '+' : ''}$${stock.change.toFixed(2)}`);
    });
  }
  
  // 高成交额股票
  const highTurnover = [...stockData].sort((a, b) => b.turnover - a.turnover).slice(0, 3);
  report.push('### 💸 高成交额股票');
  highTurnover.forEach(stock => {
    const turnoverStr = stock.turnover >= 1e9 
      ? `$${(stock.turnover/1e9).toFixed(1)}B` 
      : stock.turnover >= 1e6 
        ? `$${(stock.turnover/1e6).toFixed(1)}M` 
        : `$${(stock.turnover/1e3).toFixed(0)}K`;
    report.push(`- **${stock.symbol}**: ${turnoverStr}`);
  });
  report.push('');
  
  // 7. 今日投资视角
  report.push('## 💡 今日投资视角 (基于涨跌值)');
  report.push('1. **涨跌值分析**: 关注涨跌值绝对值大的股票，对指数影响显著');
  report.push('2. **板块轮动**: 观察各板块总涨跌值，判断资金流向');
  report.push('3. **大额变动**: 关注涨跌值≥$5的股票，可能反映重大消息');
  report.push('4. **成交活跃**: 高成交额股票反映市场关注度');
  report.push('');
  
  // 8. 数据说明
  report.push('## 📋 数据说明');
  report.push(`- **数据时间**: 北京时间 ${reportTime} (美股前一交易日收盘后)`);
  report.push(`- **数据来源**: ${config.data_sources.join(', ')}`);
  report.push(`- **美股交易时间**: 北京时间 21:30-04:00 (次日)`);
  report.push(`- **监控范围**: 美股前10大科技股 (按市值)`);
  report.push(`- **报告重点**: 涨跌值分析 (美元变动) 而非仅百分比`);
  report.push(`- **下次报告**: 明日 ${config.schedule_time}`);
  
  return report.join('\n');
}

// 保存报告到文件
function saveReportToFile(reportContent) {
  const reportDir = path.join(__dirname, 'reports');
  if (!fs.existsSync(reportDir)) {
    fs.mkdirSync(reportDir, { recursive: true });
  }
  
  const filename = `us_stock_report_${reportDate}.md`;
  const filepath = path.join(reportDir, filename);
  
  fs.writeFileSync(filepath, reportContent, 'utf8');
  console.log(`💾 报告已保存: ${filepath}`);
  
  // 同时保存到今日记忆文件
  const memoryDir = path.join(__dirname, 'memory');
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
  }
  
  const memoryFile = path.join(memoryDir, `${reportDate}.md`);
  const memoryContent = `# ${reportDate} 记忆记录\n\n## 美股报告\n\n${reportContent}`;
  
  if (fs.existsSync(memoryFile)) {
    const existing = fs.readFileSync(memoryFile, 'utf8');
    fs.writeFileSync(memoryFile, `${existing}\n\n${reportContent}`, 'utf8');
  } else {
    fs.writeFileSync(memoryFile, memoryContent, 'utf8');
  }
  
  console.log(`📝 记录已保存到记忆文件: ${memoryFile}`);
  
  return filepath;
}

// 主函数
async function main() {
  console.log('🚀 开始生成每日美股报告...\n');
  
  // 获取数据
  const stockData = fetchStockData();
  
  if (stockData) {
    // 生成报告
    const report = generateReport(stockData);
    
    if (report) {
      // 保存报告
      const savedPath = saveReportToFile(report);
      
      // 输出报告摘要
      console.log('\n' + '='.repeat(70));
      console.log('✅ 报告生成完成！');
      console.log('='.repeat(70));
      console.log(report.substring(0, 1000) + '...'); // 显示前1000字符
      console.log('\n📄 完整报告请查看保存的文件');
      
      return {
        success: true,
        reportPath: savedPath,
        stockCount: stockData.length,
        reportDate
      };
    }
  }
  
  return {
    success: false,
    error: '报告生成失败'
  };
}

// 执行
if (require.main === module) {
  main().then(result => {
    if (result.success) {
      console.log(`\n🎯 监控股票数量: ${result.stockCount} 只`);
      console.log(`📅 报告日期: ${result.reportDate}`);
      process.exit(0);
    } else {
      console.error('❌ 报告生成失败');
      process.exit(1);
    }
  }).catch(error => {
    console.error('❌ 程序执行错误:', error);
    process.exit(1);
  });
}

module.exports = { main, fetchStockData, generateReport };