#!/bin/bash

# 基金估算系统 - Vercel部署脚本

set -e  # 遇到错误退出

echo "🚀 开始部署基金估算系统到Vercel..."
echo "="*60

# 检查是否已安装Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI未安装"
    echo ""
    echo "📦 安装Vercel CLI:"
    echo "   npm install -g vercel"
    echo ""
    echo "或者使用以下方法部署:"
    echo "   1. 访问 https://vercel.com/new"
    echo "   2. 选择 'Import Git Repository'"
    echo "   3. 选择 CarsonLyu87/fund-estimation-system"
    echo "   4. 点击 'Deploy'"
    exit 1
fi

# 检查当前目录
PROJECT_DIR=$(pwd)
PROJECT_NAME="fund-estimation-system"
echo "项目目录: $PROJECT_DIR"
echo "项目名称: $PROJECT_NAME"

# 1. 检查Vercel配置
echo ""
echo "1. 检查Vercel配置..."
if [ ! -f "vercel.json" ]; then
    echo "❌ 找不到vercel.json配置文件"
    exit 1
fi

if [ ! -d "api" ]; then
    echo "❌ 找不到api目录"
    exit 1
fi

echo "✅ Vercel配置检查通过"

# 2. 检查Python依赖
echo ""
echo "2. 检查Python依赖..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ 找不到requirements.txt"
    exit 1
fi

echo "✅ Python依赖文件存在"

# 3. 登录Vercel（如果需要）
echo ""
echo "3. 检查Vercel登录状态..."
if ! vercel whoami &> /dev/null; then
    echo "⚠️  未登录Vercel，正在登录..."
    vercel login
else
    echo "✅ 已登录Vercel"
fi

# 4. 部署到Vercel
echo ""
echo "4. 部署到Vercel..."
echo "   部署选项:"
echo "   - 环境: 生产环境 (--prod)"
echo "   - 自动确认: 是 (--yes)"
echo "   - 强制部署: 是 (--force)"

# 执行部署
vercel --prod --yes --force

# 5. 获取部署信息
echo ""
echo "5. 获取部署信息..."
DEPLOYMENT_URL=$(vercel ls $PROJECT_NAME 2>/dev/null | grep -o 'https://[^ ]*' | head -1 || echo "")

if [ -n "$DEPLOYMENT_URL" ]; then
    echo "✅ 部署成功!"
    echo "   部署地址: $DEPLOYMENT_URL"
else
    echo "⚠️  无法获取部署地址，请手动检查"
    echo "   访问 https://vercel.com/dashboard 查看部署状态"
fi

# 6. 显示API端点
echo ""
echo "6. API端点信息:"
if [ -n "$DEPLOYMENT_URL" ]; then
    echo "   📍 主页: $DEPLOYMENT_URL"
    echo "   📊 单基金估算: $DEPLOYMENT_URL/api/estimate"
    echo "   📈 批量估算: $DEPLOYMENT_URL/api/batch"
    echo ""
    echo "   🔧 测试API:"
    echo "   curl '$DEPLOYMENT_URL/api/estimate?fund_code=006228'"
    echo "   curl -X POST '$DEPLOYMENT_URL/api/batch' -H 'Content-Type: application/json' -d '{\"funds\":[{\"code\":\"006228\",\"name\":\"中欧医疗\"}]}'"
else
    echo "   📍 主页: https://[your-project].vercel.app"
    echo "   📊 单基金估算: /api/estimate"
    echo "   📈 批量估算: /api/batch"
fi

# 7. 显示部署指南
echo ""
echo "7. 部署完成! 下一步操作:"
echo ""
echo "📋 手动部署方法 (如果没有使用CLI):"
echo "   1. 访问 https://vercel.com/new"
echo "   2. 点击 'Import Git Repository'"
echo "   3. 输入: CarsonLyu87/fund-estimation-system"
echo "   4. 点击 'Import'"
echo "   5. 项目名称: fund-estimation-system (或自定义)"
echo "   6. Framework Preset: Other"
echo "   7. Root Directory: ./"
echo "   8. Build Command: (留空)"
echo "   9. Output Directory: (留空)"
echo "   10. Install Command: pip install -r requirements.txt"
echo "   11. 点击 'Deploy'"
echo ""
echo "🔧 环境配置 (可选):"
echo "   在Vercel Dashboard → Project Settings → Environment Variables:"
echo "   - PYTHON_VERSION: 3.10"
echo "   - CACHE_TTL: 300"
echo "   - MAX_HOLDINGS: 10"
echo ""
echo "📊 监控部署:"
echo "   1. 访问 Vercel Dashboard"
echo "   2. 选择 fund-estimation-system 项目"
echo "   3. 查看 'Deployments' 标签页"
echo "   4. 检查构建日志和运行状态"
echo ""
echo "🚨 故障排除:"
echo "   如果部署失败，检查:"
echo "   1. vercel.json 配置是否正确"
echo "   2. requirements.txt 依赖是否兼容"
echo "   3. API函数是否有语法错误"
echo "   4. 查看Vercel构建日志"
echo ""
echo "📞 支持资源:"
echo "   - Vercel文档: https://vercel.com/docs"
echo "   - Python运行时: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python"
echo "   - 项目Issues: https://github.com/CarsonLyu87/fund-estimation-system/issues"

echo ""
echo "="*60
echo "🎉 Vercel部署准备完成!"
echo ""
echo "📋 总结:"
echo "   项目已准备好部署到Vercel"
echo "   包含:"
echo "   ✅ Vercel配置文件 (vercel.json)"
echo "   ✅ Serverless API端点 (api/estimate.py, api/batch.py)"
echo "   ✅ 优化依赖 (requirements.txt)"
echo "   ✅ 部署脚本 (本脚本)"
echo "   ✅ 完整文档 (VERCEL_DEPLOYMENT.md)"
echo ""
echo "🚀 立即部署:"
echo "   运行: vercel --prod"
echo "   或使用上述手动部署方法"
echo "="*60