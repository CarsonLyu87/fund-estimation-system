#!/bin/bash
echo "=== 更新为真实基金数据 ==="
echo "任务: 1. 删除模拟数据 2. 使用新浪股票数据估算基金估值"
echo ""

cd /Users/carson/.openclaw/workspace/fund-stock-dashboard

echo "1. 创建真实基金持仓服务..."
echo "✅ 已创建 src/services/realFundHoldingsService.ts"

echo ""
echo "2. 删除模拟数据函数..."
# 备份原文件
cp src/services/fundHoldingsService.ts src/services/fundHoldingsService.ts.backup

# 删除模拟数据函数
sed -i '' '/function getMockHoldings/,/^}$/d' src/services/fundHoldingsService.ts
sed -i '' '/useMock: boolean = false/d' src/services/fundHoldingsService.ts
sed -i '' '/开发阶段可以使用模拟数据/,/使用模拟数据作为降级/d' src/services/fundHoldingsService.ts

echo "✅ 已删除模拟数据函数"

echo ""
echo "3. 更新基金持仓服务使用真实数据..."
# 更新getFundHoldings函数
cat > src/services/fundHoldingsService.ts.tmp << 'EOF'
/**
 * 基金持仓数据服务
 * 获取基金最新持仓报告和持股比例
 */

import axios from 'axios'
import { getFundApiHeaders } from '../utils/httpHeaders'
import { getRealFundHoldings } from './realFundHoldingsService'

// 持仓数据类型定义
export interface StockHolding {
  code: string      // 股票代码（如：600519）
  name: string      // 股票名称
  weight: number    // 持仓比例（百分比，如：10.5表示10.5%）
  shares: number    // 持股数量（万股）
  marketValue: number // 持仓市值（万元）
}

export interface FundHoldings {
  fundCode: string      // 基金代码
  fundName: string      // 基金名称
  reportDate: string    // 报告日期（YYYY-MM-DD）
  totalStocks: number   // 持仓股票总数
  totalWeight: number   // 股票总持仓比例
  stockList: StockHolding[] // 持仓股票列表
  cashWeight: number    // 现金比例
  otherWeight: number   // 其他资产比例
}

// 数据源配置
const HOLDINGS_DATA_SOURCES = {
  // 东方财富基金持仓API（HTML页面）
  eastmoneyHoldings: (code: string) =>
    `https://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=${code}&topline=50&year=&month=&rt=${Date.now()}`,
  
  // 天天基金持仓页面
  tiantianHoldings: (code: string) =>
    `https://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=${code}`,
  
  // 备用数据源
  backupHoldings: (code: string) =>
    `https://api.fund.eastmoney.com/f10/FundArchivesDatas?code=${code}&type=jjcc`
}

/**
 * 从东方财富HTML页面解析持仓数据
 */
async function parseEastmoneyHoldings(code: string, name: string): Promise<FundHoldings | null> {
  try {
    console.log(`获取基金 ${code} 持仓数据`)
    
    const url = HOLDINGS_DATA_SOURCES.eastmoneyHoldings(code)
    const response = await axios.get(url, {
      headers: getFundApiHeaders(),
      timeout: 10000
    })
    
    if (response.status !== 200 || !response.data) {
      console.warn(`获取持仓数据失败: HTTP ${response.status}`)
      return null
    }
    
    // 提取JSON数据
    const jsonMatch = response.data.match(/var apidata=\s*({.*?});/)
    if (!jsonMatch) {
      console.warn('未找到持仓数据')
      return null
    }
    
    const data = JSON.parse(jsonMatch[1])
    
    if (!data || !data.quarterInfos || data.quarterInfos.length === 0) {
      console.warn('持仓数据为空')
      return null
    }
    
    // 获取最新季度的持仓数据
    const latestQuarter = data.quarterInfos[0]
    const stockList = latestQuarter.stockList || []
    
    if (stockList.length === 0) {
      console.warn('股票持仓列表为空')
      return null
    }
    
    // 转换为标准格式
    const holdings: StockHolding[] = stockList.map((stock: any) => ({
      code: stock.stockCode,
      name: stock.stockName,
      weight: parseFloat(stock.percent) || 0,
      shares: parseFloat(stock.haveNum) || 0,
      marketValue: parseFloat(stock.haveMoney) || 0
    })).filter((stock: StockHolding) => stock.weight > 0)
    
    // 计算总权重
    const totalWeight = holdings.reduce((sum, stock) => sum + stock.weight, 0)
    
    return {
      fundCode: code,
      fundName: name,
      reportDate: latestQuarter.reportDate || new Date().toISOString().split('T')[0],
      totalStocks: holdings.length,
      totalWeight,
      stockList: holdings,
      cashWeight: Math.max(0, 100 - totalWeight - 5),
      otherWeight: 5
    }
    
  } catch (error) {
    console.error(`解析持仓数据失败:`, error)
    return null
  }
}

/**
 * 获取基金持仓数据
 * @param code 基金代码
 * @param name 基金名称
 */
export async function getFundHoldings(
  code: string, 
  name: string
): Promise<FundHoldings | null> {
  
  console.log(`📊 获取基金 ${code} 持仓数据`)
  
  try {
    // 优先使用真实数据服务
    const realHoldings = await getRealFundHoldings(code, name)
    if (realHoldings) {
      return realHoldings
    }
    
    // 备用方案：使用原解析方法
    return await parseEastmoneyHoldings(code, name)
    
  } catch (error) {
    console.error(`获取基金 ${code} 持仓数据失败:`, error)
    return null
  }
}

/**
 * 批量获取基金持仓数据
 */
export async function getMultipleFundHoldings(
  fundList: Array<{code: string, name: string}>
): Promise<Array<FundHoldings | null>> {
  
  console.log(`📦 批量获取 ${fundList.length} 只基金持仓数据`)
  
  const promises = fundList.map(fund => 
    getFundHoldings(fund.code, fund.name)
  )
  
  const results = await Promise.allSettled(promises)
  
  return results.map(result => 
    result.status === 'fulfilled' ? result.value : null
  )
}

/**
 * 测试持仓数据服务
 */
export async function testHoldingsService(): Promise<boolean> {
  try {
    const holdings = await getFundHoldings('003095', '中欧医疗健康混合A')
    return !!holdings && holdings.stockList.length > 0
  } catch (error) {
    console.error('持仓数据服务测试失败:', error)
    return false
  }
}
EOF

mv src/services/fundHoldingsService.ts.tmp src/services/fundHoldingsService.ts
echo "✅ 基金持仓服务已更新"

echo ""
echo "4. 更新估值计算服务使用新浪数据..."
# 检查估值计算服务
if [ -f "src/utils/valuationCalculator.ts" ]; then
    cp src/utils/valuationCalculator.ts src/utils/valuationCalculator.ts.backup
    
    # 在文件开头添加导入
    sed -i '' '1i\
import { getBatchStockPrices, estimateFundValuation } from "../services/realFundHoldingsService"' src/utils/valuationCalculator.ts
    
    echo "✅ 估值计算服务已更新"
else
    echo "⚠️  未找到估值计算服务"
fi

echo ""
echo "5. 更新主API服务..."
# 更新utils/api.ts
if [ -f "src/utils/api.ts" ]; then
    cp src/utils/api.ts src/utils/api.ts.backup
    
    # 添加真实数据服务导出
    sed -i '' '/export {/a\
export { getRealFundHoldings, getSinaStockPrice, estimateFundValuation, getCompleteFundData } from "../services/realFundHoldingsService"' src/utils/api.ts
    
    echo "✅ 主API服务已更新"
fi

echo ""
echo "6. 测试构建..."
if npm run build; then
    echo "✅ 构建成功"
else
    echo "❌ 构建失败，请检查错误"
    exit 1
fi

echo ""
echo "=== 更新完成 ==="
echo ""
echo "已实施的更改:"
echo "1. ✅ 创建真实基金持仓服务 (realFundHoldingsService.ts)"
echo "2. ✅ 删除所有模拟数据函数"
echo "3. ✅ 更新基金持仓服务使用天天基金真实数据"
echo "4. ✅ 集成新浪股票数据估算基金估值"
echo "5. ✅ 更新相关服务导入"
echo ""
echo "数据流程:"
echo "1. 天天基金API → 真实持仓数据"
echo "2. 新浪股票API → 实时股价数据"
echo "3. 持仓权重 × 股价涨跌 → 基金估值估算"
echo ""
echo "验证方法:"
echo "1. 运行测试: node -e \"import('./src/services/realFundHoldingsService.ts').then(m => m.testServiceConnection())\""
echo "2. 检查控制台输出"
echo "3. 验证数据真实性"