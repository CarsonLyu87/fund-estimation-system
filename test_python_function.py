#!/usr/bin/env python3
"""
测试Python函数格式是否符合Vercel要求
"""

import sys
import ast

def check_python_function(file_path):
    """检查Python函数格式"""
    print(f"🔍 检查文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含handler函数
        if 'def handler(request):' not in content:
            print("❌ 错误: 文件中没有找到 'def handler(request):' 函数")
            return False
        
        # 使用AST解析检查函数格式
        tree = ast.parse(content)
        
        has_handler = False
        handler_indent = None
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'handler':
                has_handler = True
                
                # 检查函数是否在最外层（没有父节点是ClassDef）
                parent = None
                for parent_node in ast.walk(tree):
                    if hasattr(parent_node, 'body') and node in parent_node.body:
                        parent = parent_node
                        break
                
                if parent and isinstance(parent, ast.ClassDef):
                    print(f"❌ 错误: handler函数在class内部: {parent.name}")
                    return False
                
                # 检查函数是否顶格（col_offset为0）
                if node.col_offset != 0:
                    print(f"❌ 错误: handler函数有缩进 (col_offset={node.col_offset})")
                    return False
                
                print(f"✅ handler函数位置正确 (col_offset={node.col_offset})")
        
        if not has_handler:
            print("❌ 错误: 没有找到handler函数定义")
            return False
        
        # 检查import语句
        if 'import akshare' not in content:
            print("⚠️  警告: 没有找到 'import akshare'")
        
        print("✅ Python函数格式检查通过!")
        return True
        
    except Exception as e:
        print(f"❌ 解析错误: {e}")
        return False

def check_vercel_config(file_path):
    """检查Vercel配置"""
    print(f"\n🔍 检查Vercel配置: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含正确的运行时配置
        if '"runtime": "python@3.11"' not in content:
            print("❌ 错误: Vercel配置中没有 'python@3.11' 运行时")
            return False
        
        # 检查rewrites配置
        if '"rewrites"' not in content:
            print("❌ 错误: Vercel配置中没有rewrites规则")
            return False
        
        print("✅ Vercel配置检查通过!")
        return True
        
    except Exception as e:
        print(f"❌ 读取错误: {e}")
        return False

def check_requirements(file_path):
    """检查requirements.txt"""
    print(f"\n🔍 检查依赖文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        required_packages = ['akshare', 'pandas', 'requests']
        missing = []
        
        for package in required_packages:
            found = False
            for line in lines:
                if line.startswith(package):
                    found = True
                    break
            if not found:
                missing.append(package)
        
        if missing:
            print(f"❌ 错误: 缺少依赖包: {missing}")
            return False
        
        print(f"✅ 依赖检查通过! 找到包: {lines}")
        return True
        
    except Exception as e:
        print(f"❌ 读取错误: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Vercel Python函数部署验证工具")
    print("=" * 50)
    
    # 检查所有文件
    python_ok = check_python_function('api/index.py')
    vercel_ok = check_vercel_config('vercel.json')
    req_ok = check_requirements('requirements.txt')
    
    print("\n" + "=" * 50)
    print("📊 验证结果:")
    print(f"  Python函数格式: {'✅ 通过' if python_ok else '❌ 失败'}")
    print(f"  Vercel配置: {'✅ 通过' if vercel_ok else '❌ 失败'}")
    print(f"  依赖文件: {'✅ 通过' if req_ok else '❌ 失败'}")
    
    if python_ok and vercel_ok and req_ok:
        print("\n🎉 所有检查通过! 项目应该可以成功部署到Vercel!")
        print("💡 部署提示:")
        print("  1. 提交代码到GitHub")
        print("  2. Vercel会自动检测并部署")
        print("  3. 检查Vercel部署日志")
        print("  4. 测试API端点: /api/index.py?code=005827")
    else:
        print("\n❌ 检查失败! 请修复上述问题后再尝试部署。")
        sys.exit(1)