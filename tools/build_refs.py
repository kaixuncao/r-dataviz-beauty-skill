# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Users\woshi\WorkBuddy\2026-10-10-10-59-05\notes'
dst = r'C:\Users\woshi\.workbuddy\skills\r-dataviz-beauty\references'

L = open(os.path.join(base, 'ch01-02.md'), encoding='utf-8').read().split('\n')

def seg(a, b):  # 1-based inclusive
    return '\n'.join(L[a - 1:b])

head_sel = """# 图表类型体系与选型规则（源自 1.8 节）

> 来源：《R 语言数据可视化之美：专业图表绘制指南（增强版）》（张杰）第 1 章 1.8 节，及全书判断性结论摘录。
> 用途：根据用户的数据形状与分析目的，判断该用哪一类、哪一种图表。
> 所有结论后 `(p.页码)` 为该书印刷页码，回答时应一并给出，便于用户回查原书。

"""

head_gram = """# ggplot2 语法速查与数据预处理（源自 1.6 节 + 第 2 章）

> 来源：《R 语言数据可视化之美：专业图表绘制指南（增强版）》第 1 章 1.6 节「R 语言绘图基础」、第 2 章「R 语言数据处理基础」。
> 用途：生成或修改 ggplot2 代码时查阅语法细节；在绘图前整理数据。
> 代码片段均摘自原书，可直接运行。

"""

head_color = """# 学术图表配色方案与色值（源自 1.7 节）

> 来源：《R 语言数据可视化之美：专业图表绘制指南（增强版）》第 1 章 1.7 节「学术图表的色彩运用原理」。
> 用途：为图表选择颜色主题、取色、适配彩色/黑白印刷。
> 书中所有出现的 HEX / RGB 色值均原样抄录，可直接复制使用。

"""

open(os.path.join(dst, 'chart-selection.md'), 'w', encoding='utf-8').write(
    head_sel + seg(5, 95) + '\n\n---\n\n' + seg(679, 699) + '\n')
open(os.path.join(dst, 'ggplot2-grammar.md'), 'w', encoding='utf-8').write(
    head_gram + seg(99, 341) + '\n\n---\n\n' + seg(514, 677) + '\n')
open(os.path.join(dst, 'color-schemes.md'), 'w', encoding='utf-8').write(
    head_color + seg(344, 510) + '\n')

# 第12章学术规范
M = open(os.path.join(base, 'ch11-12.md'), encoding='utf-8').read().split('\n')
head_pub = """# 学术期刊图表规范与 R 导出（源自第 12 章）

> 来源：《R 语言数据可视化之美：专业图表绘制指南（增强版）》第 12 章「论文中学术图表的升级技能」。
> 用途：论文投稿前按期刊要求设定图片格式、分辨率、色彩模式、物理尺寸、字号与容量，并在 R 中正确导出。
> 书中所有数字（dpi、cm、pt、MB）均原样抄录，引用时不要四舍五入。

"""
open(os.path.join(dst, 'academic-publishing.md'), 'w', encoding='utf-8').write(
    head_pub + '\n'.join(M[557:649]) + '\n')

for f in os.listdir(dst):
    p = os.path.join(dst, f)
    print(f, len(open(p, encoding='utf-8').read().split('\n')), 'lines')
