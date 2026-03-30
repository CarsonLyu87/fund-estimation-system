"""
基金估算系统 - Vercel入口点
"""

from flask import Flask, request, jsonify, make_response
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(__file__))

try:
    from src.estimator import TiantianEastmoneyEstimator
    ESTIMATOR_AVAILABLE = True
except ImportError as e:
    print(f"导入错误: {e}")
    ESTIMATOR_AVAILABLE = False

# 创建Flask应用
app = Flask(__name__)

# 简单的CORS支持
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

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

@app.route('/')
def home():
    """主页"""
    return {
        'name': '基金实时涨跌幅估算系统',
        'version': '1.0.0',
        'description': '基于天天基金网持仓 + 东方财富网股票数据的基金估算系统',
        'endpoints': {
            '单基金估算': '/api/estimate',
            '批量估算': '/api/batch',
            '文档': '/docs'
        },
        'timestamp': datetime.now().isoformat()
    }

@app.route('/api/estimate', methods=['GET', 'POST', 'OPTIONS'])
def api_estimate():
    """单基金估算API"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            fund_code = data.get('fund_code', '006228')
            fund_name = data.get('fund_name', '中欧医疗创新股票A')
        else:  # GET
            fund_code = request.args.get('fund_code', '006228')
            fund_name = request.args.get('fund_name', '中欧医疗创新股票A')
        
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
                'method': request.method
            }
        }
        
        if 'error' in result:
            response_data['error'] = result['error']
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/batch', methods=['GET', 'POST', 'OPTIONS'])
def api_batch():
    """批量基金估算API"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            funds = data.get('funds', [
                {'code': '006228', 'name': '中欧医疗创新股票A'},
                {'code': '005827', 'name': '易方达蓝筹精选混合'}
            ])
        else:  # GET
            # 默认基金列表
            funds = [
                {'code': '006228', 'name': '中欧医疗创新股票A'},
                {'code': '005827', 'name': '易方达蓝筹精选混合'},
                {'code': '161725', 'name': '招商中证白酒指数'}
            ]
        
        # 批量估算
        results = []
        for fund in funds:
            result = estimate_fund(fund['code'], fund['name'])
            results.append({
                'fund_code': fund['code'],
                'fund_name': fund['name'],
                'estimated_change': result.get('estimated_change', 0.0),
                'stock_weight': result.get('stock_weight', 0.0),
                'cash_weight': result.get('cash_weight', 0.0),
                'data_quality': result.get('data_quality', 'N/A'),
                'estimation_time': result.get('estimation_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'top_contributions': result.get('contributions', []),
                'success': result.get('success', False),
                'error': result.get('error')
            })
        
        # 计算统计
        successful_results = [r for r in results if r.get('success') and 'error' not in r]
        up_count = sum(1 for r in successful_results if r.get('estimated_change', 0) > 0)
        down_count = sum(1 for r in successful_results if r.get('estimated_change', 0) < 0)
        
        # 构建响应
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
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/docs')
def docs():
    """API文档"""
    return {
        'api_documentation': {
            '单基金估算 (GET)': {
                'endpoint': '/api/estimate',
                'method': 'GET',
                'parameters': {
                    'fund_code': '基金代码 (默认: 006228)',
                    'fund_name': '基金名称 (默认: 中欧医疗创新股票A)'
                },
                'example': 'GET /api/estimate?fund_code=006228&fund_name=中欧医疗'
            },
            '单基金估算 (POST)': {
                'endpoint': '/api/estimate',
                'method': 'POST',
                'body': {
                    'fund_code': '基金代码',
                    'fund_name': '基金名称'
                },
                'example': 'POST /api/estimate {"fund_code": "006228", "fund_name": "中欧医疗"}'
            },
            '批量估算 (GET)': {
                'endpoint': '/api/batch',
                'method': 'GET',
                'description': '使用默认基金列表进行批量估算'
            },
            '批量估算 (POST)': {
                'endpoint': '/api/batch',
                'method': 'POST',
                'body': {
                    'funds': '基金列表，每个基金包含code和name字段'
                },
                'example': 'POST /api/batch {"funds": [{"code": "006228", "name": "中欧医疗"}]}'
            }
        },
        'timestamp': datetime.now().isoformat()
    }

# Vercel需要这个变量
if __name__ == '__main__':
    app.run(debug=True)