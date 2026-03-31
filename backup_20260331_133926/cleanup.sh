#!/bin/bash

echo "🧹 清理不需要的文件，只保留Vercel Python函数必需文件..."
echo "======================================================"

# 备份当前状态
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "1. 备份当前文件到 $BACKUP_DIR/"
cp -r ./* "$BACKUP_DIR/" 2>/dev/null || true

echo "2. 删除所有非必需文件..."
echo "   保留: api/index.py, requirements.txt, index.html, README.md, .gitignore"

# 创建临时目录保存必需文件
mkdir -p temp_keep
cp -r api temp_keep/ 2>/dev/null || true
cp requirements.txt temp_keep/ 2>/dev/null || true
cp index.html temp_keep/ 2>/dev/null || true
cp README.md temp_keep/ 2>/dev/null || true
cp .gitignore temp_keep/ 2>/dev/null || true

# 清空当前目录（保留.git）
find . -maxdepth 1 ! -name '.git' ! -name 'temp_keep' ! -name 'backup_*' ! -name '.' ! -name '..' -exec rm -rf {} +

# 恢复必需文件
cp -r temp_keep/* . 2>/dev/null || true
rm -rf temp_keep

echo "3. 验证文件结构..."
echo ""
echo "当前目录结构:"
ls -la
echo ""
echo "api/目录结构:"
ls -la api/
echo ""
echo "文件内容检查:"
echo "- api/index.py 存在: $( [ -f "api/index.py" ] && echo "✅" || echo "❌" )"
echo "- requirements.txt 存在: $( [ -f "requirements.txt" ] && echo "✅" || echo "❌" )"
echo "- index.html 存在: $( [ -f "index.html" ] && echo "✅" || echo "❌" )"
echo "- README.md 存在: $( [ -f "README.md" ] && echo "✅" || echo "❌" )"
echo ""
echo "4. 检查Python函数格式..."
if [ -f "api/index.py" ]; then
    echo "api/index.py 内容预览:"
    head -20 api/index.py
    echo "..."
    
    # 检查是否包含handler函数
    if grep -q "def handler" api/index.py; then
        echo "✅ api/index.py 包含 handler(request) 函数"
    else
        echo "❌ api/index.py 缺少 handler(request) 函数"
    fi
fi

echo ""
echo "======================================================"
echo "🧹 清理完成！"
echo ""
echo "必需文件:"
echo "  - api/index.py        Vercel Python函数入口"
echo "  - requirements.txt    Python依赖"
echo "  - index.html         前端测试页面"
echo "  - README.md          项目说明"
echo "  - .gitignore         Git忽略规则"
echo ""
echo "备份文件保存在: $BACKUP_DIR/"
echo ""
echo "下一步:"
echo "  1. git add ."
echo "  2. git commit -m 'fix: 按照Vercel官方标准重构Python函数'"
echo "  3. git push origin main"
echo "  4. 在Vercel上重新部署"