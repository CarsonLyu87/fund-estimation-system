# 基金实时涨跌幅估算系统

## 📊 项目简介

一个基于Python的基金实时涨跌幅估算系统，使用：
- **基金持仓数据**: 天天基金网
- **股票实时数据**: 东方财富网/新浪财经
- **估算方法**: ∑(持仓权重 × 股票实时涨跌)

## 🎯 核心功能

1. **实时估算**: 基于持仓和股票实时价格估算基金涨跌
2. **多基金支持**: 可同时监控多只基金
3. **数据可视化**: 生成详细的估算报告
4. **错误处理**: 完善的异常处理和备用数据源
5. **自动化运行**: 支持定时任务和自动化部署

## 🏗️ 系统架构

```
fund-estimation-system/
├── src/                    # 源代码
│   ├── estimator.py       # 核心估算类
│   ├── data_fetcher.py    # 数据获取模块
│   ├── report_generator.py # 报告生成模块
│   └── config.py          # 配置文件
├── config/                # 配置文件
│   ├── funds.json        # 基金配置
│   └── settings.py       # 系统设置
├── scripts/              # 运行脚本
│   ├── run_estimation.py # 主运行脚本
│   ├── daily_report.sh   # 每日报告脚本
│   └── setup.py          # 安装脚本
├── tests/                # 测试文件
│   ├── test_estimator.py
│   └── test_data_fetcher.py
├── docs/                 # 文档
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── EXAMPLES.md
├── requirements.txt      # Python依赖
├── Dockerfile           # Docker配置
└── README.md           # 项目说明
```

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- pip 包管理器

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置基金
编辑 `config/funds.json`:
```json
{
  "funds": [
    {
      "code": "006228",
      "name": "中欧医疗创新股票A",
      "type": "医疗",
      "priority": 1
    },
    {
      "code": "005827",
      "name": "易方达蓝筹精选混合",
      "type": "蓝筹",
      "priority": 2
    }
  ]
}
```

### 4. 运行估算
```bash
python scripts/run_estimation.py
```

### 5. 查看结果
报告将保存为 `reports/fund_estimation_YYYYMMDD_HHMMSS.txt`

## 📈 估算原理

### 计算公式
```
基金估算涨跌 = ∑(持仓权重_i × 股票实时涨跌_i) + 现金收益
```

### 数据流程
1. **获取基金持仓**: 从天天基金网获取最新季报持仓
2. **获取股票数据**: 从东方财富网/新浪财经获取实时行情
3. **计算贡献**: 每只股票对基金的贡献 = 权重 × 涨跌
4. **汇总估算**: 所有股票贡献之和 + 现金收益
5. **生成报告**: 详细的分析报告和可视化

## 🔧 配置说明

### 基金配置 (`config/funds.json`)
```json
{
  "funds": [
    {
      "code": "基金代码",
      "name": "基金名称",
      "type": "基金类型",
      "priority": "优先级(1-10)",
      "max_holdings": "最大持仓数(默认10)"
    }
  ]
}
```

### 系统配置 (`config/settings.py`)
```python
# 数据源配置
DATA_SOURCES = {
    'fund_holdings': 'tiantian',  # 天天基金网
    'stock_realtime': 'eastmoney', # 东方财富网
    'fallback': 'sina'            # 备用数据源
}

# 估算参数
ESTIMATION_SETTINGS = {
    'cash_return_rate': 0.0,      # 现金收益率
    'max_holdings': 10,           # 最大持仓数
    'timeout': 10,                # 请求超时(秒)
    'retry_times': 3              # 重试次数
}

# 报告配置
REPORT_SETTINGS = {
    'format': 'text',             # 报告格式(text/markdown/html)
    'save_to_file': True,         # 保存到文件
    'show_details': True,         # 显示详细贡献
    'include_charts': False       # 包含图表
}
```

## 📊 输出示例

```
📊 基金实时涨跌幅估算汇总报告
报告时间: 2026-03-30 15:30:00
======================================================================

📈 总体概览:
   监控基金: 3 只
   预计上涨: 2 只
   预计下跌: 1 只
   预计平盘: 0 只

🏆 各基金估算结果:
--------------------------------------------------
📈 中欧医疗创新股票A (006228)
   估算涨跌: +0.85%
   股票仓位: 94.2%
   数据质量: 8/10
   估算时间: 15:28:32

📉 易方达蓝筹精选混合 (005827)
   估算涨跌: -0.42%
   股票仓位: 92.8%
   数据质量: 9/10
   估算时间: 15:29:15
```

## 🔍 数据源说明

### 1. 基金持仓数据
- **主要来源**: 天天基金网API
- **数据格式**: JSON/HTML解析
- **更新频率**: 季报更新后
- **备用方案**: 模拟数据 + 本地缓存

### 2. 股票实时数据
- **主要来源**: 东方财富网API
- **备用来源**: 新浪财经API
- **数据频率**: 实时(3-5秒延迟)
- **支持市场**: A股、港股

### 3. 数据质量保障
- **多源验证**: 多个数据源交叉验证
- **缓存机制**: 减少重复请求
- **错误重试**: 自动重试失败请求
- **降级策略**: 主源失败时使用备用源

## 🛠️ 高级功能

### 1. 定时任务
```bash
# 每日9:30和14:30运行估算
crontab -e
30 9,14 * * * cd /path/to/fund-estimation-system && python scripts/run_estimation.py
```

### 2. 邮件通知
```python
# 配置邮件发送
EMAIL_SETTINGS = {
    'enabled': True,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'your_email@gmail.com',
    'password': 'your_password',
    'recipients': ['user1@example.com', 'user2@example.com']
}
```

### 3. Web API
```python
# 启动Web服务
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/estimate/<fund_code>')
def estimate_fund(fund_code):
    estimator = FundEstimator(fund_code)
    result = estimator.estimate()
    return jsonify(result)
```

### 4. 数据可视化
```python
# 生成图表
import matplotlib.pyplot as plt

def generate_chart(results):
    funds = [r['fund_name'] for r in results]
    changes = [r['estimated_change'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.bar(funds, changes, color=['green' if c > 0 else 'red' for c in changes])
    plt.title('基金估算涨跌幅')
    plt.xlabel('基金名称')
    plt.ylabel('涨跌幅(%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('fund_estimation_chart.png')
```

## 📈 性能优化

### 1. 并发请求
```python
import concurrent.futures

def fetch_multiple_stocks(stock_codes):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_stock_data, code): code for code in stock_codes}
        results = {}
        for future in concurrent.futures.as_completed(futures):
            code = futures[future]
            try:
                results[code] = future.result()
            except Exception as e:
                print(f"股票 {code} 获取失败: {e}")
        return results
```

### 2. 数据缓存
```python
import redis
import pickle

class DataCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
    
    def get(self, key):
        data = self.redis.get(key)
        return pickle.loads(data) if data else None
    
    def set(self, key, value, expire=300):
        self.redis.setex(key, expire, pickle.dumps(value))
```

### 3. 请求限流
```python
import time
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=1)  # 每秒最多10次请求
def call_api(url):
    # API调用代码
    pass
```

## 🔒 安全考虑

### 1. API密钥管理
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = {
    'tiantian': os.getenv('TIANTIAN_API_KEY'),
    'eastmoney': os.getenv('EASTMONEY_API_KEY')
}
```

### 2. 请求头伪装
```python
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
```

### 3. 错误处理
```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"请求失败: {e}")
    return fallback_data()
except json.JSONDecodeError as e:
    logger.error(f"JSON解析失败: {e}")
    return None
```

## 📚 扩展开发

### 1. 添加新数据源
```python
class NewDataSource:
    def get_fund_holdings(self, fund_code):
        # 实现新数据源的持仓获取
        pass
    
    def get_stock_data(self, stock_code):
        # 实现新数据源的股票数据获取
        pass
```

### 2. 自定义估算算法
```python
class CustomEstimator(FundEstimator):
    def calculate_estimation(self, holdings, stock_data):
        # 实现自定义估算算法
        # 例如: 考虑行业权重、市场情绪等
        pass
```

### 3. 集成机器学习
```python
from sklearn.linear_model import LinearRegression

class MLEstimator:
    def __init__(self):
        self.model = LinearRegression()
    
    def train(self, historical_data):
        # 使用历史数据训练模型
        X = historical_data[['market_return', 'sector_return', 'fund_size']]
        y = historical_data['fund_return']
        self.model.fit(X, y)
    
    def predict(self, current_features):
        # 预测基金表现
        return self.model.predict([current_features])
```

## 🤝 贡献指南

### 1. 开发流程
1. Fork项目
2. 创建功能分支
3. 提交代码变更
4. 创建Pull Request

### 2. 代码规范
- 遵循PEP 8编码规范
- 添加适当的注释
- 编写单元测试
- 更新相关文档

### 3. 测试要求
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_estimator.py

# 生成测试覆盖率报告
pytest --cov=src tests/
```

## 📞 支持与联系

### 问题反馈
- GitHub Issues: [项目Issues页面](https://github.com/yourusername/fund-estimation-system/issues)
- 邮件支持: support@example.com

### 社区交流
- Discord频道: [加入链接]
- 微信群: [二维码]

### 文档资源
- API文档: [API.md](docs/API.md)
- 部署指南: [DEPLOYMENT.md](docs/DEPLOYMENT.md)
- 示例代码: [EXAMPLES.md](docs/EXAMPLES.md)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢天天基金网提供基金数据
- 感谢东方财富网提供股票数据
- 感谢所有贡献者和用户的支持

---

**最后更新**: 2026-03-30  
**版本**: v1.0.0  
**作者**: 基金估算系统开发团队  
**状态**: 🟢 生产就绪