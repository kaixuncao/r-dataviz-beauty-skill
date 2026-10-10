# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
t = open(r'C:\Users\woshi\WorkBuddy\2026-10-10-10-59-05\book_text.txt', encoding='utf-8').read()
parts = t.split('===== PAGE ')
pages = {}
for p in parts[1:]:
    num = int(re.match(r'(\d+)', p).group(1))
    pages[num] = p.split(' =====\n', 1)[1] if ' =====\n' in p else ''

# 书籍页码 = PDF页码 - 12 ; 章节起始书籍页码
secs = [
    ('ch01', 1, 84),    # 第1章 R语言编程与绘图基础
    ('ch02', 84, 93),   # 第2章 数据处理基础
    ('ch03', 93, 117),  # 第3章 类别比较型
    ('ch04', 117, 155), # 第4章 数值关系型
    ('ch05', 155, 186), # 第5章 数据分布型
    ('ch06', 186, 205), # 第6章 时间序列型
    ('ch07', 205, 216), # 第7章 局部整体型
    ('ch08', 216, 242), # 第8章 高维数据可视化
    ('ch09', 242, 260), # 第9章 层次关系型
    ('ch10', 260, 287), # 第10章 网络关系型
    ('ch11', 287, 341), # 第11章 地理空间型
    ('ch12', 341, 380), # 第12章 学术图表升级技能
]
os.makedirs(r'C:\Users\woshi\WorkBuddy\2026-10-10-10-59-05\chapters', exist_ok=True)
for name, b, e in secs:
    lines = []
    for n in range(b + 12, min(e + 12, 377)):
        if n in pages:
            lines.append(f'\n<<<BOOKPAGE {n-12}>>>\n' + pages[n])
    body = ''.join(lines)
    fp = rf'C:\Users\woshi\WorkBuddy\2026-10-10-10-59-05\chapters\{name}.txt'
    open(fp, 'w', encoding='utf-8').write(body)
    print(name, len(body))
