#!/bin/bash
# 修复React渲染错误：添加防御性检查防止undefined值调用toFixed方法

echo "=== 开始修复React渲染错误 ==="
echo "目标仓库: fund-stock-dashboard"
echo "修复内容: 添加防御性检查防止undefined值调用toFixed方法"

cd /Users/carson/.openclaw/workspace/fund-stock-dashboard

echo ""
echo "1. 检查当前状态..."
git status

echo ""
echo "2. 应用修复到FundDetail.tsx..."
sed -i '' 's/{weight.toFixed(2)}%/{weight !== undefined ? weight.toFixed(2) + "%" : "N/A"}/g' ./src/components/FundDetail/FundDetail.tsx

echo "3. 应用修复到HoldingsTable.tsx..."
sed -i '' 's/{weight.toFixed(2)}%/{weight !== undefined ? weight.toFixed(2) + "%" : "N/A"}/g' ./src/components/FundDetail/HoldingsTable.tsx

echo "4. 应用修复到ValuationChart.tsx..."
# 修复第70行
sed -i '' 's/{payload\[0\].value.toFixed(3)}%/{payload[0].value !== undefined ? payload[0].value.toFixed(3) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第91行
sed -i '' 's/\${(percent \* 100).toFixed(1)}%/\${percent !== undefined ? (percent * 100).toFixed(1) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第101行
sed -i '' 's/\${value.toFixed(3)}%/\${value !== undefined ? value.toFixed(3) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第120行
sed -i '' 's/{valuation.estimatedChangePercent.toFixed(2)}%/{valuation.estimatedChangePercent !== undefined ? valuation.estimatedChangePercent.toFixed(2) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第159行
sed -i '' 's/value.toFixed(2)/value !== undefined ? value.toFixed(2) : "N/A"/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第201行
sed -i '' 's/{valuation.weightedChange.toFixed(3)}%/{valuation.weightedChange !== undefined ? valuation.weightedChange.toFixed(3) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第205行
sed -i '' 's/{valuation.estimatedChangePercent} \* 100).toFixed(1)/valuation.estimatedChangePercent !== undefined ? (Math.abs(valuation.weightedChange) \/ Math.abs(valuation.estimatedChangePercent) \* 100).toFixed(1) : "N/A"/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第221行
sed -i '' 's/{valuation.cashContribution.toFixed(3)}%/{valuation.cashContribution !== undefined ? valuation.cashContribution.toFixed(3) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第225行
sed -i '' 's/{valuation.estimatedChangePercent} \* 100).toFixed(1)/valuation.estimatedChangePercent !== undefined ? (Math.abs(valuation.cashContribution) \/ Math.abs(valuation.estimatedChangePercent) \* 100).toFixed(1) : "N/A"/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第241行
sed -i '' 's/{valuation.otherContribution.toFixed(3)}%/{valuation.otherContribution !== undefined ? valuation.otherContribution.toFixed(3) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第245行
sed -i '' 's/{valuation.estimatedChangePercent} \* 100).toFixed(1)/valuation.estimatedChangePercent !== undefined ? (Math.abs(valuation.otherContribution) \/ Math.abs(valuation.estimatedChangePercent) \* 100).toFixed(1) : "N/A"/g' ./src/components/FundDetail/ValuationChart.tsx

# 修复第262行
sed -i '' 's/{valuation.estimatedChangePercent.toFixed(3)}%/{valuation.estimatedChangePercent !== undefined ? valuation.estimatedChangePercent.toFixed(3) + "%" : "N/A"}/g' ./src/components/FundDetail/ValuationChart.tsx

echo "5. 应用修复到App.tsx..."
# 检查App.tsx中的toFixed调用
if grep -q "toFixed" ./src/App.tsx; then
    echo "  找到App.tsx中的toFixed调用，进行修复..."
    sed -i '' 's/(\((risingFunds \/ totalFunds) \* 100\).toFixed(1)}%)/(totalFunds > 0 ? ((risingFunds \/ totalFunds) \* 100).toFixed(1) + "%" : "0%")}/g' ./src/App.tsx
    sed -i '' 's/(\((risingStocks \/ totalStocks) \* 100\).toFixed(1)}%)/(totalStocks > 0 ? ((risingStocks \/ totalStocks) \* 100).toFixed(1) + "%" : "0%")}/g' ./src/App.tsx
fi

echo ""
echo "6. 验证修复..."
echo "  检查FundDetail.tsx:"
grep -n "toFixed" ./src/components/FundDetail/FundDetail.tsx

echo ""
echo "  检查HoldingsTable.tsx:"
grep -n "toFixed" ./src/components/FundDetail/HoldingsTable.tsx | head -5

echo ""
echo "7. 构建测试..."
if [ -f "./build" ]; then
    ./build
elif [ -f "package.json" ]; then
    npm run build
else
    echo "  未找到构建脚本"
fi

echo ""
echo "=== 修复完成 ==="
echo "下一步: git add . && git commit -m '修复React渲染错误' && git push"