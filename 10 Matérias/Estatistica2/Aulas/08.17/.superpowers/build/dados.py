#!/usr/bin/env python3
"""Gera os dados simulados da aula. Seed começa em 2026 e sobe até todas as
intenções de resultado (spec §5) valerem. Números fixos do professor entram
como estão. Saída: dados.json (fonte única) e vetores prontos pra colar no R."""
import json, os
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
r1 = lambda a: [round(float(v), 1) for v in a]

def gerar(seed):
    rng = np.random.default_rng(seed)
    d = {"seed": seed}
    sla = r1(rng.normal(49.5, 4, 25))
    antes = r1(rng.normal(200, 30, 12))
    depois = r1(np.array(antes) + rng.normal(12, 15, 12))
    A = r1(rng.normal(85, 12, 15))
    B = r1(rng.normal(95, 18, 18))
    e3a_antes = r1(rng.normal(30, 5, 10))
    e3a_depois = r1(np.array(e3a_antes) - rng.normal(3, 4, 10))
    e3b_A = r1(np.clip(rng.normal(6.5, 1.2, 12), 0, 10))
    e3b_B = r1(np.clip(rng.normal(7.5, 1.0, 14), 0, 10))
    d.update(t2b_sla=sla, t3_antes=antes, t3_depois=depois, t4_A=A, t4_B=B,
             e3a_antes=e3a_antes, e3a_depois=e3a_depois, e3b_A=e3b_A, e3b_B=e3b_B)
    return d

def intencoes_ok(d):
    p_sla = stats.ttest_1samp(d["t2b_sla"], 48, alternative="greater").pvalue
    p_par = stats.ttest_rel(d["t3_depois"], d["t3_antes"], alternative="greater").pvalue
    p_wel = stats.ttest_ind(d["t4_A"], d["t4_B"], equal_var=False).pvalue
    p_e3a = stats.ttest_rel(d["e3a_depois"], d["e3a_antes"], alternative="less").pvalue
    p_e3b = stats.ttest_ind(d["e3b_A"], d["e3b_B"], equal_var=False).pvalue
    checks = {
        "sla 0.02<p<0.04": 0.02 < p_sla < 0.04,
        "pareado p<0.01": p_par < 0.01,
        "welch 0.05<p<0.10": 0.05 < p_wel < 0.10,
        "e3a p<0.05": p_e3a < 0.05,
        "e3b p<0.05": p_e3b < 0.05,
    }
    return all(checks.values()), checks, dict(p_sla=p_sla, p_par=p_par, p_wel=p_wel, p_e3a=p_e3a, p_e3b=p_e3b)

for seed in range(2026, 5026):
    d = gerar(seed)
    ok, checks, ps = intencoes_ok(d)
    if ok:
        break
else:
    raise SystemExit("nenhuma seed satisfez as intenções; afrouxar parâmetros")

# fixos do professor
d["t1_vendas"] = {"n": 36, "xbar": 520, "sigma": 30, "mu0": 500, "alpha": 0.05}
d["t2a_satisf"] = {"n": 20, "xbar": 6.8, "s": 0.5, "mu0": 7.0, "alpha": 0.05}
d["t2b_mu0"] = 48
d["t5_golfe"] = {"x": 100, "n": 400, "p0": 0.20, "alpha": 0.05}
d["t6_pagto"] = {"cat": ["Credito", "Debito", "Dinheiro"], "obs": [100, 60, 40], "p": [0.45, 0.35, 0.20]}
d["t7_canal"] = {"linhas": ["Email", "Social", "Search"], "colunas": ["Comprou", "NaoComprou"],
                 "obs": [[48, 72], [30, 90], [40, 40]]}
d["e1_atend"] = [9.7, 10.2, 10.4, 9.9, 10.1, 10.5, 9.8, 10.3, 10.0, 10.2, 10.4, 10.1]
d["e2_conv"] = {"x": 90, "n": 250, "p0": 0.30}
d["e4_sabores"] = {"cat": ["A", "B", "C", "D"], "obs": [18, 22, 20, 20]}

with open(os.path.join(HERE, "dados.json"), "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)

print("seed usada:", d["seed"])
for k, v in checks.items():
    print(f"  {k}: {v}")
print("  p-valores:", {k: round(v, 4) for k, v in ps.items()})
print("\n# vetores pra colar no R")
for k in ["t2b_sla", "t3_antes", "t3_depois", "t4_A", "t4_B", "e3a_antes", "e3a_depois", "e3b_A", "e3b_B"]:
    print(f"{k} <- c({', '.join(str(x) for x in d[k])})")
