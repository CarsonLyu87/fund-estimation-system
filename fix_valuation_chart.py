#!/usr/bin/env python3
"""
修复ValuationChart.tsx中的toFixed调用
添加防御性检查防止undefined值调用toFixed方法
"""

import os
import re

file_path = "/Users/carson/.openclaw/workspace/fund-stock-dashboard/src/components/FundDetail/ValuationChart.tsx"

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复模式
fixes = [
    # 第70行: payload[0].value.toFixed(3)
    (r'(\{payload\[0\]\.value\.toFixed\(3\)%\})', 
     r'{payload[0].value !== undefined ? payload[0].value.toFixed(3) + "%" : "N/A"}'),
    
    # 第91行: (percent * 100).toFixed(1)
    (r'(\${\s*\(percent\s*\*\s*100\)\.toFixed\(1\)%\s*})', 
     r'${percent !== undefined ? (percent * 100).toFixed(1) + "%" : "N/A"}'),
    
    # 第101行: value.toFixed(3)
    (r'(\${\s*value\.toFixed\(3\)%\s*})', 
     r'${value !== undefined ? value.toFixed(3) + "%" : "N/A"}'),
    
    # 第120行: valuation.estimatedChangePercent.toFixed(2)
    (r'(\{valuation\.estimatedChangePercent\.toFixed\(2\)%\})', 
     r'{valuation.estimatedChangePercent !== undefined ? valuation.estimatedChangePercent.toFixed(2) + "%" : "N/A"}'),
    
    # 第159行: value.toFixed(2)
    (r'value\.toFixed\(2\)', 
     r'value !== undefined ? value.toFixed(2) : "N/A"'),
    
    # 第201行: valuation.weightedChange.toFixed(3)
    (r'(\{valuation\.weightedChange\.toFixed\(3\)%\})', 
     r'{valuation.weightedChange !== undefined ? valuation.weightedChange.toFixed(3) + "%" : "N/A"}'),
    
    # 第205行: 复杂的除法计算
    (r'\(Math\.abs\(valuation\.weightedChange\)\s*/\s*Math\.abs\(valuation\.estimatedChangePercent\)\)\s*\*\s*100\)\.toFixed\(1\)', 
     r'valuation.estimatedChangePercent !== undefined ? (Math.abs(valuation.weightedChange) / Math.abs(valuation.estimatedChangePercent) * 100).toFixed(1) : "N/A"'),
    
    # 第221行: valuation.cashContribution.toFixed(3)
    (r'(\{valuation\.cashContribution\.toFixed\(3\)%\})', 
     r'{valuation.cashContribution !== undefined ? valuation.cashContribution.toFixed(3) + "%" : "N/A"}'),
    
    # 第225行: 复杂的除法计算
    (r'\(Math\.abs\(valuation\.cashContribution\)\s*/\s*Math\.abs\(valuation\.estimatedChangePercent\)\)\s*\*\s*100\)\.toFixed\(1\)', 
     r'valuation.estimatedChangePercent !== undefined ? (Math.abs(valuation.cashContribution) / Math.abs(valuation.estimatedChangePercent) * 100).toFixed(1) : "N/A"'),
    
    # 第241行: valuation.otherContribution.toFixed(3)
    (r'(\{valuation\.otherContribution\.toFixed\(3\)%\})', 
     r'{valuation.otherContribution !== undefined ? valuation.otherContribution.toFixed(3) + "%" : "N/A"}'),
    
    # 第245行: 复杂的除法计算
    (r'\(Math\.abs\(valuation\.otherContribution\)\s*/\s*Math\.abs\(valuation\.estimatedChangePercent\)\)\s*\*\s*100\)\.toFixed\(1\)', 
     r'valuation.estimatedChangePercent !== undefined ? (Math.abs(valuation.otherContribution) / Math.abs(valuation.estimatedChangePercent) * 100).toFixed(1) : "N/A"'),
    
    # 第262行: valuation.estimatedChangePercent.toFixed(3)
    (r'(\{valuation\.estimatedChangePercent\.toFixed\(3\)%\})', 
     r'{valuation.estimatedChangePercent !== undefined ? valuation.estimatedChangePercent.toFixed(3) + "%" : "N/A"}'),
]

# 应用修复
for pattern, replacement in fixes:
    content, count = re.subn(pattern, replacement, content)
    if count > 0:
        print(f"修复了 {count} 处: {pattern}")

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ 已修复 {file_path}")

# 验证修复
print("\n验证修复结果:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if 'toFixed' in line:
            print(f"第{i}行: {line.strip()}")