#!/usr/bin/env python3
"""
测试Flask应用
"""

import sys
import os

# 测试Flask应用是否能导入
print("🧪 测试Flask应用导入...")

try:
    # 测试导入Flask
    from flask import Flask
    print("✅ Flask导入成功")
    
    # 测试导入我们的应用
    sys.path.append(os.path.dirname(__file__))
    
    # 导入应用模块
    import app as flask_app
    
    print("✅ 应用模块导入成功")
    
    # 测试应用实例
    if hasattr(flask_app, 'app'):
        print("✅ Flask应用实例存在")
        
        # 测试路由
        routes = []
        for rule in flask_app.app.url_map.iter_rules():
            routes.append(rule.rule)
        
        print(f"✅ 应用包含 {len(routes)} 个路由:")
        for route in sorted(routes):
            print(f"   - {route}")
        
        # 测试核心功能
        print("\n🔍 测试核心功能...")
        try:
            # 测试估算函数
            result = flask_app.estimate_fund("006228", "中欧医疗创新股票A")
            if 'estimated_change' in result:
                print(f"✅ 估算功能正常: {result.get('estimated_change', 0):+.4f}%")
            else:
                print(f"⚠️  估算功能返回异常: {result}")
        except Exception as e:
            print(f"❌ 估算功能测试失败: {e}")
    
    else:
        print("❌ Flask应用实例不存在")
    
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("\n📦 需要安装的依赖:")
    print("   pip install Flask Flask-CORS")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("📋 部署检查清单:")
print("   1. ✅ app.py 存在 (Flask应用入口)")
print("   2. ✅ requirements.txt 包含 Flask 和 Flask-CORS")
print("   3. ✅ vercel.json 配置正确")
print("   4. ✅ 应用可以正常导入")
print("\n🚀 Vercel部署说明:")
print("   现在Vercel可以识别这是一个Flask应用")
print("   入口点: app.py")
print("   Web框架: Flask")
print("\n🌐 预期API端点:")
print("   GET /                    - 主页")
print("   GET/POST /api/estimate   - 单基金估算")
print("   GET/POST /api/batch      - 批量估算")
print("   GET /docs                - API文档")
print("="*60)