# Vercel Python函数 - 基金持仓数据API

这是一个标准的Vercel Python函数项目，演示如何正确配置Vercel Serverless Functions。

## ✅ 正确的Vercel Python函数结构

```
fund-estimation-system/
├── api/
│   └── index.py          # Vercel官方Python函数入口
├── requirements.txt      # Python依赖
├── index.html           # 前端测试页面
└── README.md            # 项目说明
```

## 🚀 部署到Vercel

### 方法1: Vercel Dashboard
1. 访问 [vercel.com](https://vercel.com)
2. 点击"New Project"
3. 导入这个GitHub仓库
4. Vercel会自动检测并部署

### 方法2: Vercel CLI
```bash
# 安装Vercel CLI
npm i -g vercel

# 部署
vercel

# 生产环境部署
vercel --prod
```

## 🔧 技术细节

### API函数 (`api/index.py`)
- **位置**: 必须放在 `api/` 目录下
- **文件名**: 必须是 `index.py`
- **函数签名**: 必须包含 `handler(request)` 函数
- **返回格式**: 返回 `(data, status_code, headers)`

### 依赖管理 (`requirements.txt`)
- 必须包含所有Python依赖
- Vercel会自动安装这些依赖
- 支持 `akshare`, `pandas`, `requests` 等

### 前端页面 (`index.html`)
- 纯静态HTML/JavaScript页面
- 演示如何调用Python函数API
- 可以替换为任何前端框架

## 📊 API使用示例

### 查询基金持仓
```
GET /api/index.py?code=005827
```

### 响应示例
```json
{
  "fund": "005827",
  "name": "基金005827持仓数据",
  "holdings": [
    {
      "symbol": "000858",
      "name": "五粮液",
      "proportion": "9.87"
    }
  ],
  "count": 10,
  "timestamp": "2026-03-31T13:36:00.000000"
}
```

## 🐛 常见问题解决

### 1. "Function Runtimes must have a valid version"
**原因**: Vercel没有找到正确的Python函数入口
**解决**: 确保 `api/index.py` 存在且格式正确

### 2. "ModuleNotFoundError: No module named 'akshare'"
**原因**: 依赖未安装
**解决**: 确保 `requirements.txt` 包含 `akshare`

### 3. 函数返回404
**原因**: 文件位置或名称错误
**解决**: 必须是 `api/index.py`，不能是其他名称

### 4. CORS错误
**原因**: 前端跨域请求被阻止
**解决**: API函数返回正确的CORS头

## 📁 文件说明

### 必须保留的文件
- `api/index.py` - Python函数入口
- `requirements.txt` - Python依赖
- `index.html` - 前端测试页面

### 必须删除的文件
- `vercel.json` - Vercel会自动检测配置
- `pyproject.toml` - 不需要的Python配置
- 其他多余的Python文件

## 🔍 验证部署

1. 访问部署的网站
2. 点击"查询持仓数据"按钮
3. 检查数据是否正确返回
4. 查看浏览器控制台是否有错误

## 📞 技术支持

如果部署仍有问题：
1. 检查Vercel部署日志
2. 确保文件结构完全匹配
3. 验证Python代码语法
4. 检查依赖版本兼容性

---

**重要**: 这是Vercel Python函数的官方标准结构，遵循这个结构可以避免大多数部署问题。