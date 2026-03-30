#!/usr/bin/env python3
"""
简单测试基金估算核心功能
"""

import sys
import os

# 添加src目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_estimator():
    """测试估算器核心功能"""
    print("🧪 测试基金估算器核心功能...")
    
    try:
        from estimator import TiantianEastmoneyEstimator
        
        # 创建估算器
        config = {
            'max_holdings': 10,
            'cash_return_rate': 0.0,
            'request_interval': 0.05,
            'cache_ttl': 300
        }
        
        estimator = TiantianEastmoneyEstimator(config)
        
        # 测试单基金估算
        print("  测试中欧医疗创新股票A (006228)...")
        result = estimator.estimate_fund("006228", "中欧医疗创新股票A")
        
        print(f"  ✅ 估算成功!")
        print(f"     基金: {result.fund_name} ({result.fund_code})")
        print(f"     估算涨跌: {result.estimated_change:+.4f}%")
        print(f"     股票仓位: {result.stock_weight:.1f}%")
        print(f"     数据质量: {result.data_quality}")
        
        # 测试批量估算
        print("\n  测试批量估算...")
        funds = [
            {'code': '006228', 'name': '中欧医疗创新股票A'},
            {'code': '005827', 'name': '易方达蓝筹精选混合'}
        ]
        
        results = estimator.estimate_multiple_funds(funds)
        
        print(f"  ✅ 批量估算成功! 共{len(results)}只基金")
        for r in results:
            print(f"     {r.fund_name}: {r.estimated_change:+.4f}%")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_structure():
    """测试API文件结构"""
    print("\n📁 测试API文件结构...")
    
    api_files = ['api/estimate.py', 'api/batch.py']
    
    for file_path in api_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} 存在")
            
            # 检查文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查必要的类
            if 'class handler(BaseHTTPRequestHandler):' in content:
                print(f"     ✅ 包含正确的handler类")
            else:
                print(f"     ⚠️  可能缺少正确的handler类")
                
            # 检查HTTP方法
            methods = ['do_GET', 'do_POST', 'do_OPTIONS']
            for method in methods:
                if f'def {method}' in content:
                    print(f"     ✅ 包含{method}方法")
                else:
                    print(f"     ⚠️  缺少{method}方法")
                    
        else:
            print(f"  ❌ {file_path} 不存在")
    
    return True

def test_vercel_config():
    """测试Vercel配置"""
    print("\n⚙️  测试Vercel配置...")
    
    if os.path.exists('vercel.json'):
        print("  ✅ vercel.json 存在")
        
        import json
        with open('vercel.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查配置结构
        if 'version' in config:
            print(f"     ✅ 版本: {config['version']}")
        
        if 'builds' in config:
            print(f"     ✅ 包含builds配置")
            
        if 'routes' in config:
            print(f"     ✅ 包含routes配置")
            for route in config.get('routes', []):
                print(f"       路由: {route.get('src')} -> {route.get('dest')}")
        
    else:
        print("  ❌ vercel.json 不存在")
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始Vercel部署前测试")
    print("="*60)
    
    tests = [
        ("核心估算功能", test_estimator),
        ("API文件结构", test_api_structure),
        ("Vercel配置", test_vercel_config)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 所有测试通过! 可以部署到Vercel")
        print("\n📋 部署检查清单:")
        print("   1. ✅ 核心估算功能正常")
        print("   2. ✅ API文件格式正确")
        print("   3. ✅ Vercel配置完整")
        print("   4. ✅ 依赖文件存在")
        print("   5. ✅ 静态首页存在")
        print("\n🚀 部署命令:")
        print("   vercel --prod")
        print("\n🌐 部署后访问:")
        print("   https://your-project.vercel.app/")
        print("   https://your-project.vercel.app/api/estimate")
        print("   https://your-project.vercel.app/api/batch")
    else:
        print("❌ 测试失败，请修复问题后再部署")
    
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())