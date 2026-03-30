"""
Vercel Serverless API for Batch Fund Estimation
"""

import json
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.estimator import TiantianEastmoneyEstimator

def handler(request):
    """批量基金估算API"""
    
    # 设置CORS头
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # 处理OPTIONS请求
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # 默认基金列表
        default_funds = [
            {'code': '006228', 'name': '中欧医疗创新股票A'},
            {'code': '005827', 'name': '易方达蓝筹精选混合'},
            {'code': '161725', 'name': '招商中证白酒指数'}
        ]
        
        # 解析请求参数
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                funds = body.get('funds', default_funds)
            except:
                funds = default_funds
        else:
            funds = default_funds
        
        # 创建估算器
        estimator_config = {
            'max_holdings': 10,
            'cash_return_rate': 0.0,
            'request_interval': 0.05,
            'cache_ttl': 300
        }
        
        estimator = TiantianEastmoneyEstimator(estimator_config)
        
        # 批量估算
        results = []
        for fund in funds:
            try:
                result = estimator.estimate_fund(fund['code'], fund['name'])
                results.append({
                    'fund_code': result.fund_code,
                    'fund_name': result.fund_name,
                    'estimated_change': result.estimated_change,
                    'stock_weight': result.stock_weight,
                    'cash_weight': result.cash_weight,
                    'data_quality': result.data_quality,
                    'estimation_time': result.estimation_time,
                    'top_contributions': result.contributions[:2] if result.contributions else []
                })
            except Exception as e:
                results.append({
                    'fund_code': fund['code'],
                    'fund_name': fund['name'],
                    'error': str(e),
                    'estimated_change': 0.0,
                    'success': False
                })
        
        # 计算统计信息
        successful_results = [r for r in results if 'error' not in r]
        up_count = sum(1 for r in successful_results if r['estimated_change'] > 0)
        down_count = sum(1 for r in successful_results if r['estimated_change'] < 0)
        
        # 准备响应数据
        response_data = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_funds': len(funds),
                'successful': len(successful_results),
                'failed': len(results) - len(successful_results),
                'up_count': up_count,
                'down_count': down_count,
                'flat_count': len(successful_results) - up_count - down_count
            },
            'results': results,
            'api_info': {
                'version': '1.0.0',
                'endpoint': '/api/batch',
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
                'endpoint': '/api/batch',
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