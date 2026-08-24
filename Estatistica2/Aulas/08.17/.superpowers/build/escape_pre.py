#!/usr/bin/env python3
"""Escapa &, < e > dentro de todo bloco <pre>...</pre> do md da aula (idempotente:
desescapa antes de escapar). Obsidian trata <pre> como HTML cru, então '<-' do R e
'p<alpha' viram tag se ficarem crus."""
import html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); AULA = os.path.dirname(os.path.dirname(HERE))
MD = os.path.join(AULA, "AulaTestesHipoteseExcelR.md")
txt = open(MD, encoding="utf-8").read()
def esc(m):
    body = html.unescape(m.group(1))
    return "<pre>" + body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
novo, n = re.subn(r"<pre>(.*?)</pre>", esc, txt, flags=re.S)
open(MD, "w", encoding="utf-8").write(novo)
print(f"blocos <pre> escapados: {n}")
