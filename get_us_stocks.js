// 获取美股科技股数据的简单脚本
// 使用腾讯财经API

const stocks = [
  { symbol: 'AAPL', name: '苹果' },
  { symbol: 'MSFT', name: '微软' },
  { symbol: 'GOOGL', name: '谷歌' },
  { symbol: 'AMZN', name: '亚马逊' },
  { symbol: 'META', name: 'Meta' },
  { symbol: 'TSLA', name: '特斯拉' },
  { symbol: 'NVDA', name: '英伟达' },
  { symbol: 'AMD', name: 'AMD' },
  { symbol: 'INTC', name: '英特尔' },
  { symbol: 'NFLX', name: '奈飞' }
];

// 腾讯财经API格式：美股代码前加"us"
const stockCodes = stocks.map(s => `us${s.symbol}`).join(',');

console.log('正在获取美股科技股数据...');
console.log(`API URL: http://qt.gtimg.cn/q=${stockCodes}`);
console.log('\n');

// 使用curl获取数据
const { execSync } = require('child_process');

try {
  const result = execSync(`curl -s "http://qt.gtimg.cn/q=${stockCodes}"`, { encoding: 'utf8' });
  
  // 解析腾讯财经API返回的数据格式
  const lines = result.split(';').filter(line => line.trim());
  
  console.log('昨晚美股科技股涨跌情况 (北京时间 2026年3月26日 早上):');
  console.log('='.repeat(60));
  
  lines.forEach((line, index) => {
    if (index < stocks.length) {
      const parts = line.split('~');
      if (parts.length > 40) {
        const stock = stocks[index];
        const name = parts[1] || stock.name;
        const currentPrice = parseFloat(parts[3]) || 0;
        const prevClose = parseFloat(parts[4]) || 0;
        const change = currentPrice - prevClose;
        const changePercent = prevClose > 0 ? (change / prevClose * 100).toFixed(2) : 0;
        
        console.log(`${stock.symbol} (${name}):`);
        console.log(`  当前价格: $${currentPrice.toFixed(2)}`);
        console.log(`  昨收: $${prevClose.toFixed(2)}`);
        console.log(`  涨跌: ${change >= 0 ? '+' : ''}$${change.toFixed(2)} (${changePercent}%)`);
        console.log(`  涨跌幅: ${changePercent >= 0 ? '📈' : '📉'} ${Math.abs(changePercent)}%`);
        console.log('');
      }
    }
  });
  
  console.log('数据来源: 腾讯财经API');
  console.log('更新时间: 北京时间早上 (美股收盘后)');
  
} catch (error) {
  console.error('获取数据失败:', error.message);
  console.log('\n备用方案: 尝试手动查询以下网站:');
  console.log('1. 新浪财经美股: https://finance.sina.com.cn/stock/usstock/');
  console.log('2. 东方财富美股: https://quote.eastmoney.com/center/gridlist.html#us_stocks');
  console.log('3. 雪球美股: https://xueqiu.com/hq#exchange=US');
}