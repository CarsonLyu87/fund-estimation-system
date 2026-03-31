#!/usr/bin/env node
/**
 * 测试真实基金数据功能
 */

import { getRealFundHoldings, getSinaStockPrice, estimateFundValuation, getCompleteFundData, testServiceConnection } from './fund-stock-dashboard/src/services/realFundHoldingsService.js'

async function testRealData() {
  console.log('🧪 开始测试真实基金数据功能')
  console.log('='.repeat(50))
  
  // 1. 测试服务连接
  console.log('\n1. 测试服务连接...')
  const connection = await testServiceConnection()
  console.log('✅ 天天基金API:', connection.tiantianApi ? '可用' : '不可用')
  console.log('✅ 新浪股票API:', connection.sinaApi ? '可用' : '不可用')
  console.log('✅ 代理状态:', connection.proxyStatus ? '正常' : '异常')
  
  if (!connection.proxyStatus) {
    console.log('❌ 服务连接测试失败，请检查网络和代理配置')
    return
  }
  
  // 2. 测试基金持仓数据
  console.log('\n2. 测试基金持仓数据...')
  const testFund = { code: '003095', name: '中欧医疗健康混合A' }
  
  try {
    const holdings = await getRealFundHoldings(testFund.code, testFund.name)
    
    if (holdings) {
      console.log(`✅ 成功获取基金 ${testFund.code} 持仓数据`)
      console.log(`   基金名称: ${holdings.fundName}`)
      console.log(`   报告日期: ${holdings.reportDate}`)
      console.log(`   持仓股票数: ${holdings.totalStocks}`)
      console.log(`   股票总权重: ${holdings.totalWeight.toFixed(2)}%`)
      console.log(`   现金比例: ${holdings.cashWeight.toFixed(2)}%`)
      console.log(`   其他资产: ${holdings.otherWeight.toFixed(2)}%`)
      
      // 显示前5只重仓股
      console.log('\n   前5只重仓股:')
      holdings.stockList.slice(0, 5).forEach((stock, index) => {
        console.log(`   ${index + 1}. ${stock.name} (${stock.code}): ${stock.weight.toFixed(2)}%`)
      })
    } else {
      console.log(`❌ 获取基金 ${testFund.code} 持仓数据失败`)
    }
  } catch (error) {
    console.log(`❌ 测试基金持仓数据时出错:`, error.message)
  }
  
  // 3. 测试新浪股票数据
  console.log('\n3. 测试新浪股票数据...')
  const testStock = '600519' // 贵州茅台
  
  try {
    const stockData = await getSinaStockPrice(testStock)
    
    if (stockData) {
      console.log(`✅ 成功获取股票 ${testStock} 实时数据`)
      console.log(`   股票名称: ${stockData.name}`)
      console.log(`   当前价格: ¥${stockData.price}`)
      console.log(`   涨跌幅: ${stockData.changePercent.toFixed(2)}%`)
      console.log(`   涨跌额: ¥${stockData.change}`)
      console.log(`   成交量: ${(stockData.volume / 10000).toFixed(2)} 万手`)
      console.log(`   成交额: ${(stockData.amount / 10000).toFixed(2)} 亿元`)
    } else {
      console.log(`❌ 获取股票 ${testStock} 数据失败`)
    }
  } catch (error) {
    console.log(`❌ 测试股票数据时出错:`, error.message)
  }
  
  // 4. 测试基金估值估算
  console.log('\n4. 测试基金估值估算...')
  
  try {
    const completeData = await getCompleteFundData(testFund.code, testFund.name)
    
    if (completeData.success && completeData.holdings && completeData.valuation) {
      console.log(`✅ 成功估算基金 ${testFund.code} 估值`)
      console.log(`   估算涨跌幅: ${completeData.valuation.estimatedChange.toFixed(2)}%`)
      console.log(`   股票贡献: ${completeData.valuation.weightedChange.toFixed(2)}%`)
      console.log(`   现金贡献: ${completeData.valuation.cashContribution.toFixed(2)}%`)
      console.log(`   其他贡献: ${completeData.valuation.otherContribution.toFixed(2)}%`)
      
      // 显示主要贡献股票
      console.log('\n   主要贡献股票:')
      completeData.valuation.stockContributions
        .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution))
        .slice(0, 3)
        .forEach((sc, index) => {
          const direction = sc.contribution > 0 ? '📈' : '📉'
          console.log(`   ${index + 1}. ${sc.name} (${sc.code}): ${direction} ${sc.contribution.toFixed(3)}% (权重: ${sc.weight.toFixed(2)}%, 涨跌: ${sc.changePercent.toFixed(2)}%)`)
        })
    } else {
      console.log(`❌ 估算基金 ${testFund.code} 估值失败:`, completeData.error)
    }
  } catch (error) {
    console.log(`❌ 测试基金估值估算时出错:`, error.message)
  }
  
  console.log('\n' + '='.repeat(50))
  console.log('🧪 测试完成')
  
  // 总结
  console.log('\n📊 测试总结:')
  console.log(`   服务连接: ${connection.proxyStatus ? '✅ 正常' : '❌ 异常'}`)
  console.log(`   持仓数据: ${holdings ? '✅ 成功' : '❌ 失败'}`)
  console.log(`   股票数据: ${stockData ? '✅ 成功' : '❌ 失败'}`)
  console.log(`   估值估算: ${completeData?.success ? '✅ 成功' : '❌ 失败'}`)
  
  if (connection.proxyStatus && holdings && stockData && completeData?.success) {
    console.log('\n🎉 所有测试通过！真实数据功能正常工作。')
  } else {
    console.log('\n⚠️  部分测试失败，请检查配置和网络连接。')
  }
}

// 运行测试
testRealData().catch(console.error)