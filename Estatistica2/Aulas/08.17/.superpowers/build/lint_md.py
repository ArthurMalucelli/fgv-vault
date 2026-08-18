#!/usr/bin/env python3
"""Regras de escrita do Arthur + quirks do vault + números-chave. Sai 1 se falhar."""
import csv, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); AULA = os.path.dirname(os.path.dirname(HERE))
MD = os.path.join(AULA, "AulaTestesHipoteseExcelR.md"); CONC = os.path.expanduser("~/FGV/Vault/Conceitos")
txt = open(MD, encoding="utf-8").read(); erros = []
if "—" in txt or "–" in txt: erros.append("travessão/en-dash encontrado")
if re.search(r"\((i|ii|iii|iv|v)\)", txt): erros.append("enumerador inline (i)/(ii)")
if "```" in txt: erros.append("fenced code block (usar <pre>)")
if re.search(r"`=", txt): erros.append("backtick começando com = (Dataview inline query): escrever =`FUNCAO()`")
for m in re.finditer(r"<pre>(.*?)</pre>", txt, flags=re.S):
    body = m.group(1)
    if "<" in body or ">" in body: erros.append("'<' ou '>' cru dentro de <pre>: escapar com &lt; &gt;"); break
if txt.count("<pre>") != txt.count("</pre>"): erros.append("<pre> sem fechamento")
existentes = {os.path.splitext(os.path.basename(p))[0].lower() for p in glob.glob(os.path.join(CONC, "*.md"))}
faltando = sorted({l.split("|")[0].strip() for l in re.findall(r"\[\[([^\]]+)\]\]", txt) if l.split("|")[0].strip().lower() not in existentes})
if faltando: erros.append("wikilinks sem nota: " + ", ".join(faltando))
# números-chave (formato PT) precisam aparecer no texto
r = {row["nome"]: float(row["valor"]) for row in csv.DictReader(open(os.path.join(HERE, "r_results.csv")))}
txt_num = txt.replace("\u2212", "-")   # aceita sinal de menos Unicode no texto
def pt(x, nd): return f"{x:.{nd}f}".replace(".", ",")
chaves = {"t1_z": 1, "t2a_t": 3, "t2a_crit_bi": 3, "t2a_crit_esq": 3, "t2b_t": 3, "t2b_crit": 3, "t3_t": 3, "t4_t": 3, "t4_gl": 2,
          "t5_z": 1, "t5_crit": 3, "t6_x2": 3, "t6_crit": 3, "t7_x2": 3, "t7_crit": 3, "e2_z": 2, "e4_x2": 1,
          "t2b_p": 4, "t3_p": 4, "t2a_p_bi": 4, "t2a_p_esq": 4, "t6_p": 4, "t7_p": 4, "e1_t": 3, "e1_p": 4, "e2_p": 4, "e4_p": 4}
for k, nd in chaves.items():
    if pt(r[k], nd) not in txt_num and pt(r[k], nd).rstrip("0").rstrip(",") not in txt_num: erros.append(f"número-chave ausente: {k} = {pt(r[k], nd)}")
front = txt.split("---")[1] if txt.startswith("---") else ""
for campo in ["materia: Estatistica2", "data: 2026-08-17", "tags: [aula, estudo]"]:
    if campo not in front: erros.append("YAML sem " + campo)
print("\n".join(erros) if erros else "lint ok"); sys.exit(1 if erros else 0)
