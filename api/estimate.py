"""
Vercel Serverless API for Fund Estimation
"""

import json
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.estimator import TiantianEastmoneyEstimator

def handler(request):
    """Vercel Serverless函数处理程序"""
    
    # 设置CORS头
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # 处理OPTIONS请求（CORS预检）
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # 解析请求参数
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
            except:
                body = {}
        else:
            body = {}
        
        # 获取基金代码参数
        fund_code = body.get('fund_code') or request.args.get('fund_code', '006228')
        fund_name = body.get('fund_name') or request.args.get('fund_name', '中欧医疗创新股票A')
        
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
                'method': request.method
            }
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_data, ensure_ascii=False, indent=2)
        }
        
    except Exception as e:
        # 错误响应
        error_response = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'api_info': {
                'version': '1.0.0',
                'endpoint': '/api/estimate',
                'method': request.method
            }
        }
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_response, ensure_ascii=False, indent=2)
        }

# Vercel Serverless函数入口
def main(request):
    return handler(request)