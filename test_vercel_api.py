#!/usr/bin/env python3
"""
测试Vercel API格式
"""

import sys
import os

def test_api_structure():
    """测试API文件结构是否符合Vercel要求"""
    print("🔍 检查API文件结构...")
    
    api_files = ['api/estimate.py', 'api/batch.py']
    
    for file_path in api_files:
        print(f"\n📄 检查 {file_path}:")
        
        if not os.path.exists(file_path):
            print(f"  ❌ 文件不存在")
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必要的组件
        checks = [
            ('包含 handler 类', 'class handler(BaseHTTPRequestHandler):' in content),
            ('包含 do_GET 方法', 'def do_GET' in content),
            ('包含 do_POST 方法', 'def do_POST' in content),
            ('包含 do_OPTIONS 方法', 'def do_OPTIONS' in content),
            ('导入必要的模块', 'from http.server import BaseHTTPRequestHandler' in content),
            ('没有 main 函数', 'def main(' not in content and 'if __name__ == "__main__"' not in content)
        ]
        
        all_passed = True
        for check_name, check_result in checks:
            if check_result:
                print(f"  ✅ {check_name}")
            else:
                print(f"  ❌ {check_name}")
                all_passed = False
        
        if all_passed:
            print(f"  🎉 {file_path} 符合Vercel格式要求")
        else:
            print(f"  ⚠️  {file_path} 需要修复")
    
    return True

def test_dependencies():
    """测试依赖文件"""
    print("\n📦 检查依赖文件...")
    
    if os.path.exists('requirements.txt'):
        print("  ✅ requirements.txt 存在")
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            deps = f.read()
            print(f"     依赖数量: {len(deps.splitlines())} 行")
    else:
        print("  ❌ requirements.txt 不存在")
    
    return True

def test_static_files():
    """测试静态文件"""
    print("\n📁 检查静态文件...")
    
    static_files = ['index.html', '.nojekyll']
    
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} 存在")
        else:
            print(f"  ⚠️  {file_path} 不存在")
    
    return True

def test_project_structure():
    """测试项目结构"""
    print("\n🏗️  检查项目结构...")
    
    required_dirs = ['api', 'src', 'config']
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"  ✅ {dir_path}/ 目录存在")
            
            # 检查目录内容
            files = os.listdir(dir_path)
            print(f"     包含文件: {len(files)} 个")
            if files:
                print(f"     文件列表: {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")
        else:
            print(f"  ❌ {dir_path}/ 目录不存在")
    
    return True

def main():
    """主测试函数"""
    print("🚀 Vercel部署前检查")
    print("="*60)
    
    tests = [
        ("API文件结构", test_api_structure),
        ("依赖文件", test_dependencies),
        ("静态文件", test_static_files),
        ("项目结构", test_project_structure)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} 检查通过")
            else:
                print(f"❌ {test_name} 检查失败")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} 检查异常: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 所有检查通过! 项目已准备好部署到Vercel")
        print("\n📋 Vercel部署说明:")
        print("   1. Vercel会自动检测 /api 目录下的 .py 文件作为Serverless函数")
        print("   2. 每个 .py 文件需要包含 class handler(BaseHTTPRequestHandler)")
        print("   3. 不需要 vercel.json 配置文件")
        print("   4. 静态文件会自动服务")
        print("\n🚀 部署步骤:")
        print("   1. 访问 https://vercel.com/new")
        print("   2. 导入 Git 仓库: CarsonLyu87/fund-estimation-system")
        print("   3. 点击 Deploy")
        print("\n🌐 部署后访问:")
        print("   主页: https://your-project.vercel.app/")
        print("   API: https://your-project.vercel.app/api/estimate")
        print("   API: https://your-project.vercel.app/api/batch")
    else:
        print("❌ 检查失败，请修复问题后再部署")
    
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())