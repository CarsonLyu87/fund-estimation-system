from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.estimator import TiantianEastmoneyEstimator
    ESTIMATOR_AVAILABLE = True
except ImportError as e:
    print(f"导入错误: {e}")
    ESTIMATOR_AVAILABLE = False

def estimate_fund(fund_code, fund_name):
    """估算单只基金"""
    if not ESTIMATOR_AVAILABLE:
        return {
            'error': '估算器不可用',
            'fund_code': fund_code,
            'fund_name': fund_name,
            'estimated_change': 0.0
        }
    
    try:
        estimator_config = {
            'max_holdings': 10,
            'cash_return_rate': 0.0,
            'request_interval': 0.05,
            'cache_ttl': 300
        }
        
        estimator = TiantianEastmoneyEstimator(estimator_config)
        result = estimator.estimate_fund(fund_code, fund_name)
        
        return {
            'success': True,
            'fund_code': result.fund_code,
            'fund_name': result.fund_name,
            'estimated_change': result.estimated_change,
            'stock_weight': result.stock_weight,
            'cash_weight': result.cash_weight,
            'data_quality': result.data_quality,
            'estimation_time': result.estimation_time,
            'contributions': result.contributions[:3] if result.contributions else []
        }
    except Exception as e:
        return {
            'error': str(e),
            'fund_code': fund_code,
            'fund_name': fund_name,
            'estimated_change': 0.0,
            'success': False
        }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        try:
            # 解析URL
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # 获取参数
            fund_code = query_params.get('fund_code', ['006228'])[0]
            fund_name = query_params.get('fund_name', ['中欧医疗创新股票A'])[0]
            
            # 执行估算
            result = estimate_fund(fund_code, fund_name)
            
            # 构建响应
            response_data = {
                'success': result.get('success', True),
                'timestamp': datetime.now().isoformat(),
                'fund': {
                    'code': fund_code,
                    'name': fund_name
                },
                'estimation': {
                    'change_percent': result.get('estimated_change', 0.0),
                    'stock_weight': result.get('stock_weight', 0.0),
                    'cash_weight': result.get('cash_weight', 0.0),
                    'data_quality': result.get('data_quality', 'N/A'),
                    'estimation_time': result.get('estimation_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                },
                'contributions': result.get('contributions', []),
                'api_info': {
                    'version': '1.0.0',
                    'endpoint': '/api/estimate',
                    'method': 'GET'
                }
            }
            
            if 'error' in result:
                response_data['error'] = result['error']
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_POST(self):
        """处理POST请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 解析JSON
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
            
            # 获取参数
            fund_code = body.get('fund_code', '006228')
            fund_name = body.get('fund_name', '中欧医疗创新股票A')
            
            # 执行估算
            result = estimate_fund(fund_code, fund_name)
            
            # 构建响应
            response_data = {
                'success': result.get('success', True),
                'timestamp': datetime.now().isoformat(),
                'fund': {
                    'code': fund_code,
                    'name': fund_name
                },
                'estimation': {
                    'change_percent': result.get('estimated_change', 0.0),
                    'stock_weight': result.get('stock_weight', 0.0),
                    'cash_weight': result.get('cash_weight', 0.0),
                    'data_quality': result.get('data_quality', 'N/A'),
                    'estimation_time': result.get('estimation_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                },
                'contributions': result.get('contributions', []),
                'api_info': {
                    'version': '1.0.0',
                    'endpoint': '/api/estimate',
                    'method': 'POST'
                }
            }
            
            if 'error' in result:
                response_data['error'] = result['error']
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# 注意: Vercel会自动调用handler类
# 不需要main函数