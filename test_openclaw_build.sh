#!/bin/bash

echo "=== OpenClaw构建环境测试 ==="
echo "测试时间: $(date)"
echo "当前目录: $(pwd)"
echo ""

# 测试1: 检查node和npm
echo "1. 检查Node.js环境:"
node --version
npm --version
echo ""

# 测试2: 检查PATH
echo "2. 检查PATH环境变量:"
echo "PATH: $PATH"
echo ""

# 测试3: 检查vite命令
echo "3. 检查vite命令可用性:"
which vite || echo "vite命令未找到"
echo ""

# 测试4: 测试各种构建方法
echo "4. 测试构建方法:"
cd /Users/carson/.openclaw/workspace/fund-stock-dashboard

echo "方法1: npm run build"
npm run build 2>&1 | tail -5

echo ""
echo "方法2: npx vite build"
npx vite build 2>&1 | tail -5

echo ""
echo "方法3: ./build"
./build 2>&1 | tail -10

echo ""
echo "=== 测试完成 ==="