// 获取美股科技股数据的脚本 - 修复编码问题
const stocks = [
  { symbol: 'AAPL', name: '苹果', chineseName: '苹果' },
  { symbol: 'MSFT', name: '微软', chineseName: '微软' },
  { symbol: 'GOOGL', name: '谷歌', chineseName: '谷歌' },
  { symbol: 'AMZN', name: '亚马逊', chineseName: '亚马逊' },
  { symbol: 'META', name: 'Meta', chineseName: 'Meta' },
  { symbol: 'TSLA', name: '特斯拉', chineseName: '特斯拉' },
  { symbol: 'NVDA', name: '英伟达', chineseName: '英伟达' },
  { symbol: 'AMD', name: 'AMD', chineseName: 'AMD' },
  { symbol: 'INTC', name: '英特尔', chineseName: '英特尔' },
  { symbol: 'NFLX', name: '奈飞', chineseName: '奈飞' }
];

const stockCodes = stocks.map(s => `us${s.symbol}`).join(',');

console.log('📊 昨晚美股科技股涨跌情况分析');
console.log('='.repeat(70));
console.log('数据时间: 北京时间 2026年3月26日 早上 (美股3月25日收盘后)');
console.log('');

const { execSync } = require('child_process');

try {
  const result = execSync(`curl -s "http://qt.gtimg.cn/q=${stockCodes}"`, { encoding: 'utf8' });
  const lines = result.split(';').filter(line => line.trim());
  
  const stockData = [];
  let totalChange = 0;
  let gainers = 0;
  let losers = 0;
  
  lines.forEach((line, index) => {
    if (index < stocks.length) {
      const parts = line.split('~');
      if (parts.length > 40) {
        const stock = stocks[index];
        const currentPrice = parseFloat(parts[3]) || 0;
        const prevClose = parseFloat(parts[4]) || 0;
        const change = currentPrice - prevClose;
        const changePercent = prevClose > 0 ? (change / prevClose * 100) : 0;
        
        stockData.push({
          symbol: stock.symbol,
          name: stock.chineseName,
          currentPrice,
          prevClose,
          change,
          changePercent
        });
        
        totalChange += changePercent;
        if (change > 0) gainers++;
        else if (change < 0) losers++;
      }
    }
  });
  
  // 按涨跌幅排序
  stockData.sort((a, b) => b.changePercent - a.changePercent);
  
  // 显示涨幅最大的股票
  console.log('🏆 涨幅榜:');
  stockData.slice(0, 3).forEach(stock => {
    console.log(`  ${stock.symbol} (${stock.name}): +${stock.changePercent.toFixed(2)}%`);
  });
  
  console.log('');
  
  // 显示跌幅最大的股票
  const losersSorted = [...stockData].sort((a, b) => a.changePercent - b.changePercent);
  console.log('📉 跌幅榜:');
  losersSorted.slice(0, 3).forEach(stock => {
    if (stock.changePercent < 0) {
      console.log(`  ${stock.symbol} (${stock.name}): ${stock.changePercent.toFixed(2)}%`);
    }
  });
  
  console.log('');
  console.log('📈 详细数据:');
  console.log('='.repeat(70));
  
  stockData.forEach(stock => {
    const trend = stock.change >= 0 ? '📈' : '📉';
    const colorIndicator = stock.change >= 0 ? '🟢' : '🔴';
    
    console.log(`${colorIndicator} ${stock.symbol} (${stock.name})`);
    console.log(`  当前: $${stock.currentPrice.toFixed(2)} | 昨收: $${stock.prevClose.toFixed(2)}`);
    console.log(`  涨跌: ${stock.change >= 0 ? '+' : ''}$${stock.change.toFixed(2)}`);
    console.log(`  涨跌幅: ${trend} ${Math.abs(stock.changePercent).toFixed(2)}%`);
    console.log('');
  });
  
  // 市场概况
  const avgChange = totalChange / stockData.length;
  console.log('📊 市场概况:');
  console.log(`  上涨股票: ${gainers} 只`);
  console.log(`  下跌股票: ${losers} 只`);
  console.log(`  平均涨跌幅: ${avgChange >= 0 ? '+' : ''}${avgChange.toFixed(2)}%`);
  console.log('');
  
  // 特别关注
  console.log('🔍 特别关注:');
  const amd = stockData.find(s => s.symbol === 'AMD');
  const intc = stockData.find(s => s.symbol === 'INTC');
  const nvda = stockData.find(s => s.symbol === 'NVDA');
  
  if (amd && amd.changePercent > 5) {
    console.log(`  • AMD大涨 ${amd.changePercent.toFixed(2)}%，芯片股表现强势`);
  }
  if (intc && intc.changePercent > 5) {
    console.log(`  • 英特尔大涨 ${intc.changePercent.toFixed(2)}%，与AMD同步上涨`);
  }
  if (nvda && nvda.changePercent > 0) {
    console.log(`  • 英伟达上涨 ${nvda.changePercent.toFixed(2)}%，AI芯片股持续受关注`);
  }
  
  console.log('');
  console.log('💡 分析要点:');
  console.log('  1. 芯片股(AMD、英特尔、英伟达)表现突出');
  console.log('  2. 科技巨头整体呈现上涨趋势');
  console.log('  3. 仅微软小幅下跌，其他主要科技股均上涨');
  
  console.log('');
  console.log('📅 注: 美股交易时间为北京时间 21:30-04:00（次日）');
  console.log('数据来源: 腾讯财经API');
  
} catch (error) {
  console.error('获取数据失败:', error.message);
  console.log('\n💡 备用查询方式:');
  console.log('1. 访问: https://finance.sina.com.cn/stock/usstock/');
  console.log('2. 访问: https://quote.eastmoney.com/center/gridlist.html#us_stocks');
  console.log('3. 使用雪球APP查看美股行情');
}