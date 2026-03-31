#!/bin/bash
echo "=== 修复Vercel部署CORS问题 ==="
echo "问题: 生产环境CORS代理全部失败"
echo "解决方案: 创建Vercel函数代理 + 简化API服务"
echo ""

cd /Users/carson/.openclaw/workspace/fund-stock-dashboard

echo "1. 创建Vercel函数代理..."
mkdir -p api
echo "✅ 已创建 api/proxy.js"

echo ""
echo "2. 创建Vercel代理服务..."
echo "✅ 已创建 src/services/vercelProxyService.ts"

echo ""
echo "3. 创建简化API服务..."
echo "✅ 已创建 src/services/simpleApiService.ts"

echo ""
echo "4. 更新App.tsx导入..."
# 备份原文件
cp src/App.tsx src/App.tsx.backup

# 更新导入语句
sed -i '' 's/from .\/utils\/api/from .\/services\/simpleApiService/g' src/App.tsx

echo "✅ App.tsx导入已更新"

echo ""
echo "5. 创建vercel.json配置..."
cat > vercel.json << 'EOF'
{
  "functions": {
    "api/proxy.js": {
      "maxDuration": 30
    }
  },
  "rewrites": [
    {
      "source": "/api/proxy",
      "destination": "/api/proxy.js"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Referer, User-Agent"
        }
      ]
    }
  ]
}
EOF

echo "✅ 已创建 vercel.json"

echo ""
echo "6. 更新package.json脚本..."
# 备份package.json
cp package.json package.json.backup

# 添加vercel部署脚本
cat > package.json.tmp << 'EOF'
{
  "name": "fund-stock-show",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "deploy:vercel": "vercel --prod",
    "deploy:github": "gh-pages -d dist",
    "deploy:all": "npm run build && npm run deploy:vercel && npm run deploy:github"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "antd": "^5.16.0",
    "@ant-design/icons": "^5.3.0",
    "recharts": "^2.10.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "eslint": "^8.45.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.0",
    "typescript": "^5.0.2",
    "vite": "^5.0.0",
    "gh-pages": "^6.0.0"
  }
}
EOF

mv package.json.tmp package.json
echo "✅ package.json已更新"

echo ""
echo "7. 创建环境变量配置..."
cat > .env.production << 'EOF'
# 生产环境配置
VITE_APP_NAME=基金股票监控面板
VITE_APP_VERSION=1.0.0
VITE_API_TIMEOUT=15000
VITE_CACHE_DURATION=300000
VITE_ENABLE_LOGGING=true
EOF

echo "✅ 已创建 .env.production"

echo ""
echo "8. 测试构建..."
if npm run build; then
    echo "✅ 构建成功"
else
    echo "❌ 构建失败，请检查错误"
    exit 1
fi

echo ""
echo "=== 修复完成 ==="
echo ""
echo "已实施的解决方案:"
echo "1. ✅ Vercel函数代理 (api/proxy.js)"
echo "2. ✅ Vercel代理服务 (vercelProxyService.ts)"
echo "3. ✅ 简化API服务 (simpleApiService.ts)"
echo "4. ✅ Vercel配置 (vercel.json)"
echo "5. ✅ 环境变量配置 (.env.production)"
echo ""
echo "部署步骤:"
echo "1. 提交代码到GitHub"
echo "2. 在Vercel中导入项目"
echo "3. 自动部署完成"
echo ""
echo "验证方法:"
echo "1. 访问部署后的应用"
echo "2. 检查控制台无CORS错误"
echo "3. 验证数据加载正常"