#!/usr/bin/env python3
"""Recalcula o xlsx no LibreOffice headless (recalc.py da skill xlsx, in place; fallback:
soffice --convert-to), lê os valores das células do cell_map e compara com r_results.csv (R)
e com scipy. Sai com código 1 se algum par falhar."""
import csv, json, os, shutil, subprocess, sys, tempfile
import openpyxl
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
AULA = os.path.dirname(os.path.dirname(HERE))
XLSX = os.path.join(AULA, "TestesHipotese.xlsx")
RECALC = ("/Users/arthurmalucelli/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/"
          "f3275e4f-979d-4cd2-a4be-5b3b463fea2d/c1d131c7-b2a5-48e5-b6dc-dffeecfc54ac/skills/xlsx/scripts/recalc.py")
d = json.load(open(os.path.join(HERE, "dados.json")))
cell_map = json.load(open(os.path.join(HERE, "cell_map.json")))
r_vals = {row["nome"]: float(row["valor"]) for row in csv.DictReader(open(os.path.join(HERE, "r_results.csv")))}

# 1) recálculo headless
if os.path.exists(RECALC):
    out = subprocess.run([sys.executable, RECALC, XLSX, "120"], capture_output=True, text=True, timeout=200)
    print("recalc.py:", out.stdout.strip().replace("\n", " ")); recalc_file = XLSX; tmp = None
else:
    tmp = tempfile.mkdtemp()
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", tmp, XLSX],
                   check=True, capture_output=True, timeout=180)
    recalc_file = os.path.join(tmp, "TestesHipotese.xlsx"); print("recalc via soffice --convert-to")
wb = openpyxl.load_workbook(recalc_file, data_only=True)
def xl(name):
    sh, cell = cell_map[name].split("!"); return wb[sh][cell].value

# 2) scipy como terceiro juiz
sp = {}
v = d["t1_vendas"]; sp["t1_z"] = (v["xbar"]-v["mu0"])/(v["sigma"]/v["n"]**0.5); sp["t1_p"] = stats.norm.sf(sp["t1_z"]); sp["t1_crit"] = stats.norm.ppf(0.95)
s2 = d["t2a_satisf"]; t = (s2["xbar"]-s2["mu0"])/(s2["s"]/s2["n"]**0.5); gl = s2["n"]-1
sp.update(t2a_t=t, t2a_crit_bi=stats.t.ppf(0.975, gl), t2a_p_bi=2*stats.t.sf(abs(t), gl), t2a_crit_esq=stats.t.ppf(0.05, gl), t2a_p_esq=stats.t.cdf(t, gl))
r = stats.ttest_1samp(d["t2b_sla"], 48, alternative="greater"); sp.update(t2b_t=r.statistic, t2b_p=r.pvalue, t2b_crit=stats.t.ppf(0.95, 24))
r = stats.ttest_rel(d["t3_depois"], d["t3_antes"], alternative="greater"); sp.update(t3_t=r.statistic, t3_p=r.pvalue, t3_crit=stats.t.ppf(0.95, 11))
r = stats.ttest_ind(d["t4_A"], d["t4_B"], equal_var=False); sp.update(t4_t=r.statistic, t4_p=r.pvalue, t4_gl=r.df, t4_crit=stats.t.ppf(0.975, r.df))
g = d["t5_golfe"]; z = (g["x"]/g["n"]-g["p0"])/((g["p0"]*(1-g["p0"])/g["n"])**0.5); sp.update(t5_z=z, t5_p=stats.norm.sf(z), t5_crit=stats.norm.ppf(0.95))
q = d["t6_pagto"]; r = stats.chisquare(q["obs"], [200*p for p in q["p"]]); sp.update(t6_x2=r.statistic, t6_p=r.pvalue, t6_crit=stats.chi2.ppf(0.95, 2))
r = stats.chi2_contingency(d["t7_canal"]["obs"], correction=False); sp.update(t7_x2=r.statistic, t7_p=r.pvalue, t7_crit=stats.chi2.ppf(0.95, 2))
r = stats.ttest_1samp(d["e1_atend"], 10); sp.update(e1_t=r.statistic, e1_p=r.pvalue, e1_crit=stats.t.ppf(0.975, 11))
e = d["e2_conv"]; z = (e["x"]/e["n"]-e["p0"])/((e["p0"]*(1-e["p0"])/e["n"])**0.5); sp.update(e2_z=z, e2_p=2*stats.norm.sf(abs(z)))
r = stats.ttest_rel(d["e3a_depois"], d["e3a_antes"], alternative="less"); sp.update(e3a_t=r.statistic, e3a_p=r.pvalue)
r = stats.ttest_ind(d["e3b_A"], d["e3b_B"], equal_var=False); sp.update(e3b_t=r.statistic, e3b_p=r.pvalue)
r = stats.chisquare(d["e4_sabores"]["obs"]); sp.update(e4_x2=r.statistic, e4_p=r.pvalue, e4_crit=stats.chi2.ppf(0.95, 3))

# 3) tabela cruzada
TOL = {"t4_crit": 0.02, "t4_p": 0.01}   # Excel/LibreOffice truncam gl de Welch em T.DIST/T.INV (documentado no md e na aba 4_Welch)
falhas = 0
print(f"{'nome':14}{'R':>12}{'Excel':>12}{'scipy':>12}  status")
for name in r_vals:
    rv = r_vals[name]; ev = xl(name) if name in cell_map else None; sv = sp.get(name)
    tol = TOL.get(name, 1e-3); status = []
    if ev is not None:
        if not isinstance(ev, (int, float)): status.append(f"EXCEL NÃO NUMÉRICO: {ev!r}"); falhas += 1
        elif abs(ev - rv) > tol: status.append(f"R x Excel diff={ev-rv:+.5f}"); falhas += 1
    if sv is not None and abs(float(sv) - rv) > 1e-6: status.append(f"R x scipy diff={float(sv)-rv:+.2e}"); falhas += 1
    print(f"{name:14}{rv:12.5f}{(ev if isinstance(ev,(int,float)) else float('nan')):12.5f}{(float(sv) if sv is not None else float('nan')):12.5f}  {'ok' if not status else '; '.join(status)}")
for extra, ref in [("t4_p_ttest", "t4_p"), ("t3_p_ttest", "t3_p"), ("t6_p_chisqtest", "t6_p"), ("t7_p_chisqtest", "t7_p")]:
    ev = xl(extra); ok = isinstance(ev, (int, float)) and abs(ev - r_vals[ref]) <= 1e-3
    if not ok: falhas += 1
    print(f"{extra:14}{'':>12}{(ev if isinstance(ev,(int,float)) else float('nan')):12.5f}{'':>12}  {'ok (atalho Excel = ' + ref + ')' if ok else 'ATALHO DIVERGE de ' + ref}")
if tmp: shutil.rmtree(tmp)
print("\nFALHAS:", falhas); sys.exit(1 if falhas else 0)
