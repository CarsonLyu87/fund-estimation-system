#!/bin/bash
echo "=== GitHub状态检查 ==="
echo "检查时间: $(date)"
echo ""

# 检查fund-stock-dashboard仓库
echo "📦 检查 fund-stock-dashboard 仓库:"
cd /Users/carson/.openclaw/workspace/fund-stock-dashboard

echo "1. 本地提交记录:"
git log --oneline -3

echo ""
echo "2. 远程仓库状态:"
git remote -v

echo ""
echo "3. 分支状态:"
git branch -vv

echo ""
echo "4. 与远程同步状态:"
git fetch origin
git status

echo ""
echo "=== GitHub链接 ==="
echo "🔗 仓库主页: https://github.com/CarsonLyu87/fund-stock-dashboard"
echo "🔗 提交列表: https://github.com/CarsonLyu87/fund-stock-dashboard/commits/main"
echo "🔗 最新提交: https://github.com/CarsonLyu87/fund-stock-dashboard/commit/ebd6a6da"
echo "🔗 React修复提交: https://github.com/CarsonLyu87/fund-stock-dashboard/commit/24b0771e"

echo ""
echo "=== 重要提交说明 ==="
echo ""
echo "✅ 最新提交: ebd6a6da"
echo "   消息: 添加OpenClaw构建配置指南和更新说明"
echo "   内容: 创建OPENCLAW_BUILD_CONFIG.md和UPDATE_OPENCLAW_CONFIG.md"
echo ""
echo "✅ React修复提交: 24b0771e"
echo "   消息: 修复React渲染错误：添加防御性检查防止undefined值调用toFixed方法"
echo "   内容: 修复5个文件中的.toFixed()调用，添加undefined检查"
echo "   修复文件:"
echo "   - src/components/FundDetail/FundDetail.tsx"
echo "   - src/components/FundDetail/HoldingsTable.tsx"
echo "   - src/components/FundDetail/ValuationChart.tsx"
echo "   - src/App.tsx"
echo ""
echo "=== 验证方法 ==="
echo "1. 打开浏览器访问: https://github.com/CarsonLyu87/fund-stock-dashboard"
echo "2. 点击 'Commits' 标签"
echo "3. 查看最新提交记录"
echo "4. 点击提交哈希查看详细修改"