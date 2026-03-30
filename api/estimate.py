from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.estimator import TiantianEastmoneyEstimator

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        try:
            # 解析URL参数
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # 获取基金代码参数
            fund_code = query_params.get('fund_code', ['006228'])[0]
            fund_name = query_params.get('fund_name', ['中欧医疗创新股票A'])[0]
            
            # 创建估算器
            estimator_config = {
                'max_holdings': 10,
                'cash_return_rate': 0.0,
                'request_interval': 0.05,
                'cache_ttl': 300
            }
            
            estimator = TiantianEastmoneyEstimator(estimator_config)
            
            # 执行估算
            result = estimator.estimate_fund(fund_code, fund_name)
            
            # 准备响应数据
            response_data = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'fund': {
                    'code': result.fund_code,
                    'name': result.fund_name
                },
                'estimation': {
                    'change_percent': result.estimated_change,
                    'stock_weight': result.stock_weight,
                    'cash_weight': result.cash_weight,
                    'data_quality': result.data_quality,
                    'estimation_time': result.estimation_time
                },
                'contributions': result.contributions[:3] if result.contributions else [],
                'api_info': {
                    'version': '1.0.0',
                    'endpoint': '/api/estimate',
                    'method': 'GET'
                }
            }
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))
            
        except Exception as e:
            # 错误响应
            error_response = {
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'api_info': {
                    'version': '1.0.0',
                    'endpoint': '/api/estimate',
                    'method': 'GET'
                }
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False, indent=2).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # 解析JSON数据
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
            
            # 获取基金代码参数
            fund_code = body.get('fund_code', '006228')
            fund_name = body.get('fund_name', '中欧医疗创新股票A')
            
            # 创建估算器
            estimator_config = {
                'max_holdings': 10,
                'cash_return_rate': 0.0,
                'request_interval': 0.05,
                'cache_ttl': 300
            }
            
            estimator = TiantianEastmoneyEstimator(estimator_config)
            
            # 执行估算
            result = estimator.estimate_fund(fund_code, fund_name)
            
            # 准备响应数据
            response_data = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'fund': {
                    'code': result.fund_code,
                    'name': result.fund_name
                },
                'estimation': {
                    'change_percent': result.estimated_change,
                    'stock_weight': result.stock_weight,
                    'cash_weight': result.cash_weight,
                    'data_quality': result.data_quality,
                    'estimation_time': result.estimation_time
                },
                'contributions': result.contributions[:3] if result.contributions else [],
                'api_info': {
                    'version': '1.0.0',
                    'endpoint': '/api/estimate',
                    'method': 'POST'
                }
            }
            
            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode('utf-8'))
            
        except Exception as e:
            # 错误响应
            error_response = {
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'api_info': {
                    'version': '1.0.0',
                    'endpoint': '/api/estimate',
                    'method': 'POST'
                }
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False, indent=2).encode('utf-8'))