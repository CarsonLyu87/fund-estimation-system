#!/bin/bash

# 修复基金项目中的HTTP头问题
# 将所有硬编码的HTTP头替换为使用httpHeaders工具

echo "开始修复HTTP头问题..."

# 1. 修复 accurateFundService.ts
echo "修复 accurateFundService.ts..."
sed -i '' "s/headers: {.*'Referer': 'https:\/\/fund.eastmoney.com\/'.*}/headers: getFundApiHeaders()/g" src/services/accurateFundService.ts
sed -i '' "s/headers: REQUEST_HEADERS/headers: getFundApiHeaders()/g" src/services/accurateFundService.ts

# 2. 修复 fundSearchService.ts
echo "修复 fundSearchService.ts..."
sed -i '' "s/headers: {.*'Referer': 'https:\/\/fund.eastmoney.com\/'.*}/headers: getFundApiHeaders()/g" src/services/fundSearchService.ts

# 3. 修复 realDataService.ts
echo "修复 realDataService.ts..."
sed -i '' "s/headers: {.*'Referer': 'https:\/\/fund.eastmoney.com\/'.*}/headers: getFundApiHeaders()/g" src/services/realDataService.ts
sed -i '' "s/headers: {.*'Referer': 'https:\/\/finance.sina.com.cn\/'.*}/headers: getStockApiHeaders()/g" src/services/realDataService.ts

# 4. 修复 fundPortfolioService.ts
echo "修复 fundPortfolioService.ts..."
sed -i '' "s/headers: {.*'Referer': 'https:\/\/fund.eastmoney.com\/'.*}/headers: getFundApiHeaders()/g" src/services/fundPortfolioService.ts

# 5. 确保导入httpHeaders工具
echo "检查导入语句..."
for file in src/services/*.ts; do
    if grep -q "getFundApiHeaders\|getStockApiHeaders" "$file" && ! grep -q "import.*httpHeaders" "$file"; then
        echo "在 $file 中添加导入语句..."
        sed -i '' "1s/^/import { getFundApiHeaders, getStockApiHeaders } from '..\/utils\/httpHeaders'\n/" "$file"
    fi
done

echo "修复完成！"