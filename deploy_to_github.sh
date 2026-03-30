#!/bin/bash

# 基金估算系统 - GitHub部署脚本

set -e  # 遇到错误退出

echo "🚀 开始部署基金估算系统到GitHub..."
echo "="*60

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

# 检查当前目录
PROJECT_DIR=$(pwd)
PROJECT_NAME="fund-estimation-system"
echo "项目目录: $PROJECT_DIR"
echo "项目名称: $PROJECT_NAME"

# 1. 初始化Git仓库
echo ""
echo "1. 初始化Git仓库..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

# 2. 添加文件到暂存区
echo ""
echo "2. 添加文件到暂存区..."
git add .
echo "✅ 文件已添加到暂存区"

# 3. 提交更改
echo ""
echo "3. 提交更改..."
COMMIT_MESSAGE="基金估算系统 v1.0 - 实时涨跌幅估算"
git commit -m "$COMMIT_MESSAGE" || {
    echo "⚠️  没有新的更改需要提交"
}

# 4. 检查远程仓库
echo ""
echo "4. 检查远程仓库..."
if git remote | grep -q "origin"; then
    echo "✅ 远程仓库已配置"
    REMOTE_URL=$(git remote get-url origin)
    echo "   远程地址: $REMOTE_URL"
else
    echo "⚠️  未配置远程仓库"
    echo "   请先创建GitHub仓库，然后运行:"
    echo "   git remote add origin https://github.com/你的用户名/$PROJECT_NAME.git"
    echo "   或使用SSH: git remote add origin git@github.com:你的用户名/$PROJECT_NAME.git"
    echo ""
    echo "📋 创建GitHub仓库步骤:"
    echo "   1. 访问 https://github.com/new"
    echo "   2. 仓库名称: $PROJECT_NAME"
    echo "   3. 描述: 基金实时涨跌幅估算系统"
    echo "   4. 选择公开或私有"
    echo "   5. 不要初始化README、.gitignore等"
    echo "   6. 点击创建仓库"
    echo "   7. 复制仓库URL"
    exit 0
fi

# 5. 推送到GitHub
echo ""
echo "5. 推送到GitHub..."
echo "   分支: main"
echo "   远程: origin"

# 检查是否有未推送的提交
if git status | grep -q "Your branch is ahead"; then
    echo "📤 有未推送的提交，正在推送..."
    git push origin main
    echo "✅ 推送完成"
else
    echo "📤 强制推送最新代码..."
    git push -u origin main --force
    echo "✅ 推送完成"
fi

# 6. 创建GitHub Pages（可选）
echo ""
echo "6. 设置GitHub Pages（可选）..."
echo "   如果要启用GitHub Pages展示报告:"
echo "   1. 访问 https://github.com/你的用户名/$PROJECT_NAME/settings/pages"
echo "   2. Source选择: GitHub Actions"
echo "   3. 保存设置"

# 7. 创建GitHub Actions工作流（可选）
echo ""
echo "7. 创建GitHub Actions工作流（可选）..."
WORKFLOW_DIR=".github/workflows"
WORKFLOW_FILE="$WORKFLOW_DIR/daily-estimation.yml"

if [ ! -f "$WORKFLOW_FILE" ]; then
    mkdir -p "$WORKFLOW_DIR"
    
    cat > "$WORKFLOW_FILE" << 'EOF'
name: 每日基金估算

on:
  schedule:
    # 每天北京时间9:30和14:30运行（UTC时间1:30和6:30）
    - cron: '30 1,6 * * *'
  workflow_dispatch:  # 手动触发

jobs:
  estimate:
    runs-on: ubuntu-latest
    
    steps:
    - name: 检出代码
      uses: actions/checkout@v3
    
    - name: 设置Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: 运行基金估算
      run: |
        python scripts/run_estimation.py
      
    - name: 上传报告
      uses: actions/upload-artifact@v3
      with:
        name: fund-estimation-reports
        path: reports/
        
    - name: 提交报告到仓库
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add reports/
        git commit -m "自动更新: 基金估算报告 $(date +'%Y-%m-%d %H:%M')" || echo "没有新的报告"
        git push
EOF
    
    echo "✅ 创建GitHub Actions工作流: $WORKFLOW_FILE"
    echo "   工作流将在每天9:30和14:30自动运行"
else
    echo "✅ GitHub Actions工作流已存在"
fi

# 8. 创建README徽章
echo ""
echo "8. 项目状态徽章..."
echo ""
echo "📊 可以添加到README.md的徽章:"
echo ""
echo "[![GitHub](https://img.shields.io/github/license/你的用户名/$PROJECT_NAME)](https://github.com/你的用户名/$PROJECT_NAME)"
echo "[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)"
echo "[![GitHub Actions](https://github.com/你的用户名/$PROJECT_NAME/actions/workflows/daily-estimation.yml/badge.svg)](https://github.com/你的用户名/$PROJECT_NAME/actions)"
echo "[![GitHub last commit](https://img.shields.io/github/last-commit/你的用户名/$PROJECT_NAME)](https://github.com/你的用户名/$PROJECT_NAME)"
echo ""

# 9. 总结
echo "="*60
echo "🎉 基金估算系统部署完成!"
echo ""
echo "📋 项目信息:"
echo "   仓库地址: $REMOTE_URL"
echo "   本地目录: $PROJECT_DIR"
echo ""
echo "🚀 下一步操作:"
echo "   1. 测试系统运行: ./start.sh"
echo "   2. 设置定时任务: ./setup_cron.sh"
echo "   3. 查看估算报告: cat reports/latest_fund_estimation.txt"
echo "   4. 访问GitHub仓库查看代码"
echo ""
echo "🔧 开发工作流:"
echo "   1. 修改代码"
echo "   2. git add ."
echo "   3. git commit -m '描述更改'"
echo "   4. git push origin main"
echo ""
echo "📞 问题反馈:"
echo "   在GitHub Issues中提交问题:"
echo "   ${REMOTE_URL%.git}/issues"
echo "="*60