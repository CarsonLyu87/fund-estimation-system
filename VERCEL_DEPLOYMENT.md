# 🚀 Vercel 部署指南

## 📋 部署准备

### 1. 项目结构要求
```
fund-estimation-system/
├── api/                    # Vercel Serverless函数
│   ├── estimate.py        # 单基金估算API
│   └── batch.py           # 批量估算API
├── vercel.json            # Vercel配置文件
├── requirements.txt       # Python依赖
├── src/                   # 源代码
└── index.html            # 前端页面
```

### 2. 环境要求
- **Python版本**: 3.10+
- **Node.js**: 18+ (Vercel CLI需要)
- **Vercel账户**: 免费账户即可

## 🚀 部署步骤

### 方法一：使用Vercel CLI（推荐）

#### 1. 安装Vercel CLI
```bash
npm install -g vercel
```

#### 2. 登录Vercel
```bash
vercel login
```

#### 3. 部署项目
```bash
cd fund-estimation-system
vercel
```

#### 4. 部署到生产环境
```bash
vercel --prod
```

### 方法二：通过GitHub集成

#### 1. 连接GitHub仓库
1. 访问 [vercel.com](https://vercel.com)
2. 点击 "New Project"
3. 选择 "Import Git Repository"
4. 选择 `CarsonLyu87/fund-estimation-system`
5. 点击 "Import"

#### 2. 配置项目
- **Framework Preset**: Other
- **Build Command**: (留空，Vercel自动检测)
- **Output Directory**: (留空)
- **Install Command**: `pip install -r requirements.txt`

#### 3. 部署
点击 "Deploy" 按钮

### 方法三：通过Vercel Dashboard

#### 1. 手动上传
1. 访问 [vercel.com/new](https://vercel.com/new)
2. 选择 "Deploy from GitHub"
3. 搜索并选择仓库
4. 点击 "Deploy"

## 🔧 Vercel配置说明

### `vercel.json` 配置文件
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    },
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/",
      "dest": "/index.html"
    },
    {
      "src": "/api/estimate",
      "dest": "/api/estimate.py"
    },
    {
      "src": "/api/batch",
      "dest": "/api/batch.py"
    }
  ]
}
```

### 环境变量配置（可选）
在Vercel Dashboard中设置：
```
PYTHON_VERSION=3.10
CACHE_TTL=300
MAX_HOLDINGS=10
```

## 🌐 API端点说明

### 1. 单基金估算 API
**端点**: `GET|POST /api/estimate`

**请求参数**:
```json
{
  "fund_code": "006228",
  "fund_name": "中欧医疗创新股票A"
}
```

**或URL参数**:
```
GET /api/estimate?fund_code=006228&fund_name=中欧医疗创新股票A
```

**响应示例**:
```json
{
  "success": true,
  "timestamp": "2026-03-30T18:15:00",
  "fund": {
    "code": "006228",
    "name": "中欧医疗创新股票A"
  },
  "estimation": {
    "change_percent": 0.2633,
    "stock_weight": 34.7,
    "cash_weight": 65.3,
    "data_quality": "5/5",
    "estimation_time": "2026-03-30 16:05:19"
  },
  "contributions": [
    {
      "stock": "泰格医药(300347)",
      "weight": 6.8,
      "stock_change": 3.614,
      "contribution": 0.2457
    }
  ]
}
```

### 2. 批量基金估算 API
**端点**: `GET|POST /api/batch`

**请求参数**:
```json
{
  "funds": [
    {"code": "006228", "name": "中欧医疗创新股票A"},
    {"code": "005827", "name": "易方达蓝筹精选混合"},
    {"code": "161725", "name": "招商中证白酒指数"}
  ]
}
```

**响应示例**:
```json
{
  "success": true,
  "timestamp": "2026-03-30T18:15:00",
  "summary": {
    "total_funds": 3,
    "successful": 3,
    "failed": 0,
    "up_count": 2,
    "down_count": 0,
    "flat_count": 1
  },
  "results": [
    {
      "fund_code": "006228",
      "fund_name": "中欧医疗创新股票A",
      "estimated_change": 0.2633,
      "stock_weight": 34.7,
      "cash_weight": 65.3,
      "data_quality": "5/5"
    }
  ]
}
```

## 🎨 前端页面

### 访问地址
部署成功后，可以通过以下地址访问：
- **主页面**: `https://your-project.vercel.app/`
- **API文档**: `https://your-project.vercel.app/api/estimate`
- **批量API**: `https://your-project.vercel.app/api/batch`

### 页面功能
1. **基金估算表单**: 输入基金代码进行估算
2. **实时结果展示**: 显示估算结果和贡献分析
3. **批量估算**: 同时估算多只基金
4. **历史记录**: 查看最近的估算记录

## ⚡ 性能优化

### 1. 冷启动优化
- **保持函数活跃**: 设置合适的memory和maxDuration
- **使用缓存**: 实现数据缓存减少API调用
- **预加载**: 在函数初始化时预加载必要资源

### 2. 资源配置
```json
{
  "functions": {
    "api/estimate.py": {
      "maxDuration": 10,
      "memory": 1024
    },
    "api/batch.py": {
      "maxDuration": 30,
      "memory": 2048
    }
  }
}
```

### 3. 缓存策略
- **客户端缓存**: 设置Cache-Control头
- **CDN缓存**: 利用Vercel的全球CDN
- **数据缓存**: 实现内存或Redis缓存

## 🔒 安全考虑

### 1. CORS配置
```python
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
}
```

### 2. 速率限制
建议在Vercel Dashboard中配置：
- **最大请求数**: 1000次/小时
- **突发限制**: 100次/分钟

### 3. 输入验证
所有API都包含输入验证和错误处理。

## 📊 监控和日志

### 1. Vercel Analytics
- 访问Vercel Dashboard查看访问统计
- 监控API调用次数和响应时间
- 查看错误率和性能指标

### 2. 自定义日志
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### 3. 错误追踪
- 使用try-catch捕获所有异常
- 返回详细的错误信息
- 记录错误日志供调试

## 🚨 故障排除

### 常见问题

#### 1. 导入错误
**问题**: `ModuleNotFoundError: No module named 'src'`
**解决**: 确保Python路径正确设置
```python
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
```

#### 2. 内存不足
**问题**: `MemoryError` 或超时
**解决**: 增加内存配置
```json
"memory": 2048
```

#### 3. 冷启动慢
**解决**:
- 减少依赖包大小
- 使用更轻量的库
- 实现延迟加载

#### 4. API响应慢
**解决**:
- 实现数据缓存
- 优化网络请求
- 使用并发处理

### 调试步骤
1. **本地测试**: 使用Vercel CLI本地开发
2. **查看日志**: 在Vercel Dashboard查看部署日志
3. **检查配置**: 确认vercel.json配置正确
4. **测试API**: 使用curl或Postman测试API端点

## 🔄 持续部署

### 1. 自动部署
连接GitHub仓库后，每次push都会自动部署。

### 2. 预览部署
每次Pull Request都会创建预览部署。

### 3. 生产部署
合并到main分支后自动部署到生产环境。

### 4. 回滚
在Vercel Dashboard中可以轻松回滚到之前的版本。

## 💰 成本估算

### 免费套餐限制
- **带宽**: 100GB/月
- **函数执行**: 100小时/月
- **构建时间**: 100小时/月
- **并发函数**: 12个

### 典型用量
- **单次API调用**: ~2-5秒
- **内存使用**: ~100-200MB
- **每月估算**: 可支持约10,000次API调用

### 升级建议
如果超过免费限制，考虑：
1. **优化代码**: 减少执行时间和内存使用
2. **实现缓存**: 减少重复计算
3. **升级套餐**: Hobby套餐($20/月)提供更多资源

## 📞 支持资源

### 官方文档
- [Vercel Documentation](https://vercel.com/docs)
- [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Serverless Functions](https://vercel.com/docs/concepts/functions/serverless-functions)

### 社区支持
- [Vercel Community](https://vercel.com/community)
- [GitHub Issues](https://github.com/CarsonLyu87/fund-estimation-system/issues)
- [Discord](https://vercel.com/discord)

### 示例项目
- [Python API Example](https://github.com/vercel/examples/tree/main/python)
- [Serverless Functions Examples](https://github.com/vercel/examples/tree/main/solutions)

## 🎉 部署完成

### 验证部署
1. **访问主页**: `https://your-project.vercel.app/`
2. **测试API**: `curl https://your-project.vercel.app/api/estimate`
3. **检查日志**: 在Vercel Dashboard查看部署日志
4. **功能测试**: 使用前端页面进行完整测试

### 成功标志
- ✅ 主页正常显示
- ✅ API返回正确数据
- ✅ 无错误日志
- ✅ 响应时间合理(<5秒)

### 后续步骤
1. **配置域名**: 绑定自定义域名
2. **设置监控**: 配置告警和监控
3. **优化性能**: 根据使用情况优化配置
4. **扩展功能**: 添加更多API端点

---

**部署状态**: 🟢 准备就绪  
**最后更新**: 2026-03-30 18:15  
**维护团队**: 基金估算系统开发团队