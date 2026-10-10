# -*- coding: utf-8 -*-
import sys, re, os
from pypdf import PdfReader

src = r"C:\Users\woshi\Downloads\R语言数据可视化之美：专业图表绘制指南（增强版）+(张杰)+(z-library.sk,+1lib.sk,+z-lib.sk).pdf"
out = r"C:\Users\woshi\WorkBuddy\2026-10-10-10-59-05\book_text.txt"

r = PdfReader(src)
print("pages:", len(r.pages))
txt = []
for i, p in enumerate(r.pages):
    try:
        t = p.extract_text() or ""
    except Exception as e:
        t = ""
        print("ERR page", i, e, file=sys.stderr)
    txt.append(f"\n===== PAGE {i+1} =====\n" + t)

full = "\n".join(txt)
with open(out, "w", encoding="utf-8") as f:
    f.write(full)
print("chars:", len(full))
# 粗略统计中文/代码密度
code_lines = len(re.findall(r"(library\(|ggplot\(|geom_|theme\()", full))
print("code_markers:", code_lines)
