# Aula Testes de Hipótese em Excel e R: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar em `~/FGV/Estatistica2/Aulas/08.17/` a aula `AulaTestesHipoteseExcelR.md` + `TestesHipotese.xlsx` + `TestesHipotese.R`, com todos os números validados por cross-check R x Excel x scipy, mais notas de conceito novas no vault.

**Architecture:** Um gerador Python (`dados.py`, seed fixa, auto-ajuste de seed até as intenções de resultado valerem) produz `dados.json`, fonte única dos números. O script R é escrito à mão com esses dados hardcoded; um `check_r.R` separado faz `source()` nele e exporta os resultados em CSV. O xlsx é gerado por `build_xlsx.py` (openpyxl, fórmulas vivas, prefixo `_xlfn.`), recalculado no LibreOffice headless e conferido por `recalc_check.py` contra o CSV do R e contra scipy. O md é escrito à mão com os outputs reais do R e passa por `lint_md.py` (regras de escrita, wikilinks, `<pre>` escapado, números-chave).

**Tech Stack:** Python 3 (numpy 2.4, scipy 1.17, openpyxl 3.1), R via Homebrew (base R só), LibreOffice headless (`/opt/homebrew/bin/soffice`), Obsidian vault em `~/FGV/`.

Sem git: o vault não é repositório. Onde o skill pede commit, o passo é "conferir arquivo salvo".

Spec: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/2026-08-17-aula-testes-hipotese-design.md`.

Skill obrigatória na Task 4: `anthropic-skills:xlsx` (invocar antes de gerar o workbook; usar o `recalc.py` dela se existir, senão o fallback `soffice --convert-to` abaixo).

---

## Estrutura de arquivos

```
~/FGV/Estatistica2/Aulas/08.17/
├── AulaTestesHipoteseExcelR.md          (entregável, vault)
├── TestesHipotese.xlsx                  (entregável)
├── TestesHipotese.R                     (entregável)
└── .superpowers/
    ├── 2026-08-17-aula-testes-hipotese-design.md
    ├── 2026-08-17-aula-testes-hipotese-plan.md
    └── build/
        ├── dados.py           gera dados.json (seed auto-ajustada) e imprime vetores R
        ├── dados.json         fonte única dos números
        ├── check_r.R          source() no script R, escreve r_results.csv
        ├── r_output.txt       output completo do Rscript (base pros blocos do md)
        ├── r_results.csv      nome,valor dos resultados-chave
        ├── build_xlsx.py      gera TestesHipotese.xlsx + cell_map.json
        ├── cell_map.json      nome do resultado -> "Aba!Célula"
        ├── recalc_check.py    recalcula no LibreOffice, cruza Excel x R x scipy
        └── lint_md.py         regras de escrita, wikilinks, <pre>, números-chave
~/FGV/Vault/Conceitos/  (8 notas novas, Task 6)
```

Nomes de resultado (usados em `check_r.R`, `cell_map.json`, `recalc_check.py`, `lint_md.py`; manter idênticos):

`t1_z t1_crit t1_p | t2a_t t2a_crit_bi t2a_p_bi t2a_crit_esq t2a_p_esq | t2b_xbar t2b_s t2b_t t2b_crit t2b_p | t3_dbar t3_sd t3_t t3_crit t3_p t3_ic_lo t3_ic_hi | t4_t t4_gl t4_crit t4_p | t5_z t5_crit t5_p t5_p_corr | t6_x2 t6_crit t6_p | t7_x2 t7_crit t7_p | e1_t e1_crit e1_p | e2_z e2_p | e3a_t e3a_p | e3b_t e3b_p | e4_x2 e4_crit e4_p`

---

### Task 0: Instalar R (em background) e criar pasta build

**Files:**
- Create: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/` (pasta)

- [ ] **Step 1: Disparar a instalação em background**

Run: `brew install r > ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/brew_r.log 2>&1` (run_in_background). Enquanto roda, seguir pras Tasks 1 e 4 (não dependem de R).

- [ ] **Step 2: Criar pasta build**

Run: `mkdir -p ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build`

- [ ] **Step 3: Verificar quando o brew terminar**

Run: `Rscript --version`
Expected: linha `Rscript (R) version 4.x.y`. Se `brew` falhar por link/permission, ler `brew_r.log` e reportar ao Arthur (não improvisar sudo).

---

### Task 1: Gerador de dados com seed auto-ajustada

**Files:**
- Create: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/dados.py`
- Output: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/dados.json`

- [ ] **Step 1: Escrever `dados.py`**

```python
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
```

- [ ] **Step 2: Rodar**

Run: `python3 ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/dados.py`
Expected: `seed usada: <n>`, cinco checks `True`, p-valores dentro das faixas, e os 9 vetores `<- c(...)`. Anotar a seed e os p-valores na seção Registro no fim deste plano.

- [ ] **Step 3: Conferir `dados.json` salvo**

Run: `python3 -c "import json;d=json.load(open('$HOME/FGV/Estatistica2/Aulas/08.17/.superpowers/build/dados.json'));print(sorted(d))"`
Expected: lista com as 18 chaves (seed, 9 vetores, t1_vendas, t2a_satisf, t2b_mu0, t5_golfe, t6_pagto, t7_canal, e1_atend, e2_conv, e4_sabores).

---

### Task 2: Script R didático (entregável)

**Files:**
- Create: `~/FGV/Estatistica2/Aulas/08.17/TestesHipotese.R`

Depende de: Task 0 (R instalado), Task 1 (vetores).

- [ ] **Step 1: Escrever o script**

Substituir cada `c(...VETOR...)` pelo vetor impresso pela Task 1 (mesma ordem de casas). Conteúdo completo:

```r
# =====================================================================
#  Estatística II (FGV EAESP, prof. Chertman)  |  Testes de hipótese em R
#  Aula de revisão 17/08/2026, cobre aulas 2 a 6. Companheiro de
#  AulaTestesHipoteseExcelR.md e TestesHipotese.xlsx (mesmos dados).
#
#  Como rodar:
#    terminal:      Rscript TestesHipotese.R
#    dentro do R:   source("TestesHipotese.R")
#    pra aprender:  abrir o R no terminal (comando R), colar bloco a bloco,
#                   olhar cada objeto. Sair com q() e responder n.
#
#  Só base R. Padrão de cada bloco: dados -> cálculo na mão -> função pronta.
#  Convenção: t_calc = estatística calculada, t_crit = valor crítico, p_ = valor-p.
# =====================================================================

# ---- 0. Helper mínimo (o resto é função nativa, de propósito) --------
decide <- function(p, alpha = 0.05) {
  # imprime a decisão comparando valor-p com alfa
  if (p < alpha) cat("  valor-p =", format(p, digits = 4), "<", alpha, "->  REJEITA H0\n")
  else           cat("  valor-p =", format(p, digits = 4), ">=", alpha, "-> NÃO rejeita H0\n")
}
alpha <- 0.05     # nível de significância usado na aula inteira

# ---- 1. Z para uma média, sigma conhecido (vendas: meta 500) ---------
# H0: mu <= 500   H1: mu > 500  (unicaudal à direita: "aumentaram?")
cat("\n==== 1. Z uma média (vendas) ====\n")
xbar <- 520; mu0 <- 500; sigma <- 30; n <- 36
ep   <- sigma / sqrt(n)                 # erro-padrão da média
t1_z <- (xbar - mu0) / ep               # estatística Z
t1_crit <- qnorm(1 - alpha)             # 1.645: Z que deixa 5% na cauda direita
t1_p <- 1 - pnorm(t1_z)                 # área à direita de z (= pnorm(t1_z, lower.tail = FALSE))
cat("  z =", round(t1_z, 3), "| z crítico =", round(t1_crit, 3), "\n"); decide(t1_p)
# base R não tem z.test: pra Z é sempre na mão (qnorm pra crítico, pnorm pra valor-p)

# ---- 2a. t para uma média, só sumário (satisfação: benchmark 7,0) -----
cat("\n==== 2a. t uma média, sumário (satisfação) ====\n")
xbar <- 6.8; s <- 0.5; n <- 20; mu0 <- 7; gl <- n - 1
t2a_t <- (xbar - mu0) / (s / sqrt(n))   # usa s (amostral) -> t, não Z
# leitura 1: "é diferente de 7?"  H1: mu != 7  (bicaudal, alfa/2 em cada cauda)
t2a_crit_bi <- qt(1 - alpha / 2, gl)    # 2.093
t2a_p_bi    <- 2 * pt(-abs(t2a_t), gl)  # dobra a cauda
cat("  bicaudal: t =", round(t2a_t, 3), "| crítico = ±", round(t2a_crit_bi, 3), "\n"); decide(t2a_p_bi)
# leitura 2: "está abaixo do benchmark?"  H1: mu < 7  (unicaudal à esquerda)
t2a_crit_esq <- qt(alpha, gl)           # -1.729 (negativo: cauda esquerda)
t2a_p_esq    <- pt(t2a_t, gl)           # área à esquerda de t
cat("  unicaudal esq: t =", round(t2a_t, 3), "| crítico =", round(t2a_crit_esq, 3), "\n"); decide(t2a_p_esq)
# mesma amostra, decisões diferentes: a cauda vem do enunciado, não do dado

# ---- 2b. t para uma média, dados brutos (SLA 48h, n = 25 entregas) ----
# H0: mu <= 48   H1: mu > 48  (unicaudal à direita: "está estourando o SLA?")
cat("\n==== 2b. t uma média, dados brutos (SLA) ====\n")
sla <- c(...VETOR t2b_sla...)
n <- length(sla); t2b_xbar <- mean(sla); t2b_s <- sd(sla)   # sd() é o desvio AMOSTRAL (n-1)
ep <- t2b_s / sqrt(n); gl <- n - 1
t2b_t    <- (t2b_xbar - 48) / ep
t2b_crit <- qt(1 - alpha, gl)                     # cauda direita
t2b_p    <- pt(t2b_t, gl, lower.tail = FALSE)     # área à direita
cat("  n =", n, "| média =", round(t2b_xbar, 3), "| s =", round(t2b_s, 3), "\n")
cat("  t =", round(t2b_t, 3), "| crítico =", round(t2b_crit, 3), "\n"); decide(t2b_p)
cat("  a 1%: "); decide(t2b_p, 0.01)              # alfa muda a decisão
# função pronta: mesmos números
res2b <- t.test(sla, mu = 48, alternative = "greater")   # mu = valor de H0; alternative = lado de H1
print(res2b)

# ---- 3. t pareado (12 lojas, vendas antes/depois da campanha) ---------
# D = Depois - Antes.  H0: mu_D <= 0   H1: mu_D > 0
cat("\n==== 3. t pareado (vendas antes/depois) ====\n")
antes  <- c(...VETOR t3_antes...)
depois <- c(...VETOR t3_depois...)
D <- depois - antes                     # pareado = teste t de UMA média sobre as diferenças
n <- length(D); t3_dbar <- mean(D); t3_sd <- sd(D); gl <- n - 1
t3_t    <- (t3_dbar - 0) / (t3_sd / sqrt(n))
t3_crit <- qt(1 - alpha, gl)
t3_p    <- pt(t3_t, gl, lower.tail = FALSE)
cat("  D médio =", round(t3_dbar, 3), "| s_D =", round(t3_sd, 3), "| t =", round(t3_t, 3),
    "| crítico =", round(t3_crit, 3), "\n"); decide(t3_p)
print(t.test(depois, antes, paired = TRUE, alternative = "greater"))   # paired = TRUE é o que faz o pareado
ic <- t.test(depois, antes, paired = TRUE)$conf.int    # IC 95% bicaudal de mu_D (tamanho do efeito)
t3_ic_lo <- ic[1]; t3_ic_hi <- ic[2]
cat("  IC 95% de mu_D: [", round(t3_ic_lo, 2), ";", round(t3_ic_hi, 2), "]\n")

# ---- 4. t para duas médias independentes, Welch (ticket A vs B) -------
# H0: mu_A = mu_B   H1: mu_A != mu_B  (bicaudal). Extensão além dos slides.
cat("\n==== 4. Welch (ticket médio loja A vs B) ====\n")
A <- c(...VETOR t4_A...)
B <- c(...VETOR t4_B...)
nA <- length(A); nB <- length(B); vA <- var(A); vB <- var(B)
ep    <- sqrt(vA / nA + vB / nB)                          # erro-padrão da diferença
t4_t  <- (mean(A) - mean(B)) / ep
t4_gl <- ep^4 / ((vA / nA)^2 / (nA - 1) + (vB / nB)^2 / (nB - 1))   # gl de Welch (não é nA+nB-2)
t4_crit <- qt(1 - alpha / 2, t4_gl)
t4_p    <- 2 * pt(-abs(t4_t), t4_gl)
cat("  t =", round(t4_t, 3), "| gl Welch =", round(t4_gl, 2), "| crítico = ±", round(t4_crit, 3), "\n"); decide(t4_p)
print(t.test(A, B))                       # default = Welch (var.equal = FALSE)
# t.test(A, B, var.equal = TRUE)          # versão variâncias iguais (pooled), só pra saber que existe

# ---- 5. Z para uma proporção (golfe: 20% -> 100 de 400) --------------
# H0: p <= 0.20   H1: p > 0.20  (unicaudal à direita: "a promoção aumentou a proporção?")
cat("\n==== 5. Z proporção (golfe) ====\n")
x <- 100; n <- 400; p0 <- 0.20; phat <- x / n
ep0  <- sqrt(p0 * (1 - p0) / n)          # p0 no denominador (o da hipótese), não phat
t5_z <- (phat - p0) / ep0
t5_crit <- qnorm(1 - alpha)              # 1.645
t5_p    <- 1 - pnorm(t5_z)
cat("  p^ =", phat, "| z =", round(t5_z, 3), "| crítico =", round(t5_crit, 3), "\n"); decide(t5_p)
r5 <- prop.test(x, n, p = p0, alternative = "greater", correct = FALSE)   # X-squared = z^2, mesmo valor-p
print(r5)
r5c <- prop.test(x, n, p = p0, alternative = "greater")                   # default correct = TRUE
t5_p_corr <- r5c$p.value
cat("  valor-p com correção de continuidade (default do R):", format(t5_p_corr, digits = 4), "\n")

# ---- 6. Qui-quadrado de aderência (mix de pagamento) -----------------
# H0: distribuição observada segue 45/35/20   H1: pelo menos uma proporção difere
cat("\n==== 6. Qui-quadrado aderência (pagamentos) ====\n")
obs   <- c(Credito = 100, Debito = 60, Dinheiro = 40)
p_exp <- c(0.45, 0.35, 0.20)
esp   <- sum(obs) * p_exp                # frequências esperadas sob H0
t6_x2 <- sum((obs - esp)^2 / esp)
gl    <- length(obs) - 1                 # k - 1
t6_crit <- qchisq(1 - alpha, gl)         # sempre cauda direita
t6_p    <- pchisq(t6_x2, gl, lower.tail = FALSE)
cat("  esperadas:", esp, "| qui2 =", round(t6_x2, 3), "| gl =", gl, "| crítico =", round(t6_crit, 3), "\n"); decide(t6_p)
print(chisq.test(x = obs, p = p_exp))    # x = contagens observadas, p = proporções de H0

# ---- 7. Qui-quadrado de independência (canal x compra) ---------------
# H0: canal e compra são independentes   H1: existe associação
cat("\n==== 7. Qui-quadrado independência (canal x compra) ====\n")
tab <- matrix(c(48, 72,
                30, 90,
                40, 40), nrow = 3, byrow = TRUE)
dimnames(tab) <- list(Canal = c("Email", "Social", "Search"), Compra = c("Comprou", "NaoComprou"))
esp   <- outer(rowSums(tab), colSums(tab)) / sum(tab)   # E_ij = (total linha * total coluna) / n
t7_x2 <- sum((tab - esp)^2 / esp)
gl    <- (nrow(tab) - 1) * (ncol(tab) - 1)             # (r-1)(c-1)
t7_crit <- qchisq(1 - alpha, gl)
t7_p    <- pchisq(t7_x2, gl, lower.tail = FALSE)
cat("  qui2 =", round(t7_x2, 3), "| gl =", gl, "| crítico =", round(t7_crit, 3), "\n"); decide(t7_p)
res7 <- chisq.test(tab)
print(res7)
cat("  esperadas:\n"); print(round(res7$expected, 2))
cat("  resíduos (O-E)/sqrt(E): sinal e tamanho dizem qual célula puxa o qui2\n"); print(round(res7$residuals, 2))
cat("  taxa de compra por canal:\n"); print(round(prop.table(tab, 1)[, "Comprou"], 2))
# esperadas < 5 em muitas células: R avisa "Chi-squared approximation may be incorrect"

# ---- 8. Exercícios (dados; tente antes de abrir a seção 9) -----------
e1_atend   <- c(9.7, 10.2, 10.4, 9.9, 10.1, 10.5, 9.8, 10.3, 10.0, 10.2, 10.4, 10.1)  # "mudou de 10 min?"
e2_x <- 90; e2_n <- 250; e2_p0 <- 0.30                                                # "conversão mudou de 30%?"
e3a_antes  <- c(...VETOR e3a_antes...)    # mesmas 10 pessoas, minutos por tarefa antes do treinamento
e3a_depois <- c(...VETOR e3a_depois...)   # depois. "o treinamento reduziu o tempo?"
e3b_A <- c(...VETOR e3b_A...)             # notas turma A
e3b_B <- c(...VETOR e3b_B...)             # notas turma B (outras pessoas). "as médias diferem?"
e4_obs <- c(A = 18, B = 22, C = 20, D = 20)                                           # "preferência uniforme?"

# ---- 9. GABARITO (descomente depois de tentar) ------------------------
# E1: t.test(e1_atend, mu = 10)                       # bicaudal; t ~ 1.85, p ~ 0.09, não rejeita
# E2: z <- (e2_x/e2_n - e2_p0)/sqrt(e2_p0*(1-e2_p0)/e2_n); 2*(1-pnorm(abs(z)))   # p ~ 0.038: rejeita a 5%, não a 1%
# E3a: t.test(e3a_depois, e3a_antes, paired = TRUE, alternative = "less")   # pareado, cauda esquerda
# E3b: t.test(e3b_A, e3b_B)                                                  # Welch bicaudal
# E4: chisq.test(e4_obs)                              # p uniforme é o default; qui2 = 0.4, gl 3, não rejeita
```

- [ ] **Step 2: Rodar e guardar o output**

Run: `cd ~/FGV/Estatistica2/Aulas/08.17 && Rscript TestesHipotese.R > .superpowers/build/r_output.txt 2>&1; echo exit=$?; tail -5 .superpowers/build/r_output.txt`
Expected: `exit=0`, sem `Error`. Abrir `r_output.txt` e conferir: bloco 1 z = 4, bloco 2a bicaudal NÃO rejeita e unicaudal REJEITA, bloco 5 z = 2.5 e `X-squared = 6.25`, bloco 6 qui2 = 2.54, bloco 7 qui2 = 13.69.

- [ ] **Step 3: Escrever `check_r.R`**

```r
# Exporta os resultados-chave do script didático pra cross-check. Não é entregável.
# Uso: Rscript check_r.R /caminho/absoluto/TestesHipotese.R
script <- commandArgs(trailingOnly = TRUE)[1]
if (is.na(script)) stop("passe o caminho do TestesHipotese.R como argumento")
invisible(capture.output(source(script)))
# gabarito dos exercícios (calculado aqui, o script didático deixa comentado)
e1 <- t.test(e1_atend, mu = 10); e1_t <- unname(e1$statistic); e1_p <- e1$p.value; e1_crit <- qt(0.975, length(e1_atend) - 1)
e2_z <- (e2_x/e2_n - e2_p0)/sqrt(e2_p0*(1-e2_p0)/e2_n); e2_p <- 2*(1-pnorm(abs(e2_z)))
e3a <- t.test(e3a_depois, e3a_antes, paired = TRUE, alternative = "less"); e3a_t <- unname(e3a$statistic); e3a_p <- e3a$p.value
e3b <- t.test(e3b_A, e3b_B); e3b_t <- unname(e3b$statistic); e3b_p <- e3b$p.value
e4 <- chisq.test(e4_obs); e4_x2 <- unname(e4$statistic); e4_p <- e4$p.value; e4_crit <- qchisq(0.95, 3)
nomes <- c("t1_z","t1_crit","t1_p","t2a_t","t2a_crit_bi","t2a_p_bi","t2a_crit_esq","t2a_p_esq",
           "t2b_xbar","t2b_s","t2b_t","t2b_crit","t2b_p","t3_dbar","t3_sd","t3_t","t3_crit","t3_p","t3_ic_lo","t3_ic_hi",
           "t4_t","t4_gl","t4_crit","t4_p","t5_z","t5_crit","t5_p","t5_p_corr","t6_x2","t6_crit","t6_p","t7_x2","t7_crit","t7_p",
           "e1_t","e1_crit","e1_p","e2_z","e2_p","e3a_t","e3a_p","e3b_t","e3b_p","e4_x2","e4_crit","e4_p")
vals <- sapply(nomes, function(nm) get(nm))
out <- file.path(dirname(normalizePath(script)), ".superpowers", "build", "r_results.csv")
write.csv(data.frame(nome = nomes, valor = format(vals, digits = 15)), out, row.names = FALSE, quote = FALSE)
cat("escrito:", out, "\n"); print(round(vals, 5))
```

- [ ] **Step 4: Rodar o check**

Run: `Rscript ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/check_r.R ~/FGV/Estatistica2/Aulas/08.17/TestesHipotese.R`
Expected: `escrito: .../r_results.csv` e os 46 valores impressos. Conferir: `t1_z 4`, `t5_z 2.5`, `t6_x2 2.5397`, `t7_x2 13.69`, `e4_x2 0.4`, `e2_z 2.0702`.

---

### Task 3: Gerar o workbook (openpyxl, fórmulas vivas)

**Files:**
- Create: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/build_xlsx.py`
- Output: `~/FGV/Estatistica2/Aulas/08.17/TestesHipotese.xlsx`, `.superpowers/build/cell_map.json`

Depende de: Task 1. Antes de começar: invocar `anthropic-skills:xlsx`.

- [ ] **Step 1: Escrever `build_xlsx.py`**

Regras: funções novas com prefixo `_xlfn.` (helper `F()`); inputs em azul (`0000FF`), fórmulas em preto; estatística `0.000`, valor-p `0.0000`; cada resultado-chave registrado em `cell_map` com o nome da lista de resultados. Fórmulas em sintaxe EN (vírgula separa argumentos), como no arquivo do professor.

```python
#!/usr/bin/env python3
"""Gera TestesHipotese.xlsx a partir de dados.json. Fórmulas vivas, sem valor colado."""
import json, os, re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
AULA = os.path.dirname(os.path.dirname(HERE))
d = json.load(open(os.path.join(HERE, "dados.json")))
cell_map = {}

XLFN = ["NORM.S.INV", "NORM.S.DIST", "T.INV.2T", "T.INV", "T.DIST.2T", "T.DIST.RT", "T.DIST",
        "CHISQ.INV.RT", "CHISQ.DIST.RT", "CHISQ.TEST", "T.TEST", "Z.TEST", "STDEV.S"]
def F(s):
    """prefixa _xlfn. nas funções pós-2007 (openpyxl não faz sozinho; sem isso o Excel dá #NAME?)"""
    for fn in sorted(XLFN, key=len, reverse=True):
        s = re.sub(r'(?<![\w.])' + re.escape(fn) + r'\(', '_xlfn.' + fn + '(', s)
    return s

BLUE, BOLD, TITLE = Font(color="0000FF"), Font(bold=True), Font(bold=True, size=13)
GREY = PatternFill("solid", fgColor="EFEFEF")

def title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = TITLE
    if sub: ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="555555")

def put(ws, cell, value, *, inp=False, fmt=None, bold=False, name=None):
    c = ws[cell]
    c.value = F(value) if isinstance(value, str) and value.startswith("=") else value
    if inp: c.font = BLUE
    if bold: c.font = BOLD
    if fmt: c.number_format = fmt
    if name: cell_map[name] = f"{ws.title}!{cell}"
    return c

def rows(ws, col_label, col_val, start, items):
    """items: lista de (label, value, kwargs). Escreve rótulo e valor linha a linha; devolve dict label->célula do valor"""
    ref = {}
    r = start
    for label, value, kw in items:
        ws[f"{col_label}{r}"] = label
        if label.startswith(("1.", "2.", "3.", "4.", "5.")): ws[f"{col_label}{r}"].font = BOLD
        if value is not None: put(ws, f"{col_val}{r}", value, **kw)
        ref[label] = f"{col_val}{r}"
        r += 1
    return ref

def widths(ws, spec):
    for col, w in spec.items(): ws.column_dimensions[col].width = w

def data_col(ws, col, start, header, values, fmt="0.0"):
    ws[f"{col}{start-1}"] = header; ws[f"{col}{start-1}"].font = BOLD
    for i, v in enumerate(values):
        put(ws, f"{col}{start+i}", v, inp=True, fmt=fmt)
    return f"{col}{start}:{col}{start+len(values)-1}"

wb = Workbook()

# ---------------- Mapa ----------------
ws = wb.active; ws.title = "Mapa"
title(ws, "Mapa de funções: Excel (EN / PT) x R", "Sintaxe EN usa vírgula entre argumentos; Excel em português usa ponto e vírgula.")
head = ["Objetivo", "Excel (EN)", "Excel (PT)", "R", "Devolve", "Quando usar / observação"]
for j, h in enumerate(head, 1):
    c = ws.cell(row=4, column=j, value=h); c.font = BOLD; c.fill = GREY
mapa = [
 ("Tamanho da amostra n", "COUNT(range)", "CONT.NÚM(intervalo)", "length(x)", "n", ""),
 ("Média amostral", "AVERAGE(range)", "MÉDIA(intervalo)", "mean(x)", "x̄", ""),
 ("Desvio-padrão amostral s", "STDEV.S(range)", "DESVPAD.A(intervalo)", "sd(x)", "s (divide por n-1)", "STDEV.P divide por n: errado pra amostra"),
 ("Raiz e valor absoluto", "SQRT(x), ABS(x)", "RAIZ(x), ABS(x)", "sqrt(x), abs(x)", "", ""),
 ("Z crítico unicaudal", "NORM.S.INV(1-α)", "INV.NORMP.N(1-α)", "qnorm(1-alpha)", "1,645 pra 5%", "cauda esquerda: NORM.S.INV(α) = -1,645"),
 ("Z crítico bicaudal", "NORM.S.INV(1-α/2)", "INV.NORMP.N(1-α/2)", "qnorm(1-alpha/2)", "1,960 pra 5%", "α/2 em cada cauda"),
 ("valor-p Z, cauda direita", "1-NORM.S.DIST(z,TRUE)", "1-DIST.NORMP.N(z;VERDADEIRO)", "1-pnorm(z)", "área à direita de z", "cauda esquerda: NORM.S.DIST(z,TRUE)"),
 ("valor-p Z, bicaudal", "2*(1-NORM.S.DIST(ABS(z),TRUE))", "2*(1-DIST.NORMP.N(ABS(z);VERDADEIRO))", "2*(1-pnorm(abs(z)))", "dobro da cauda", ""),
 ("t crítico unicaudal direita", "T.INV(1-α,gl)", "INV.T(1-α;gl)", "qt(1-alpha,gl)", "ex. 1,729 (gl 19)", "T.INV(α,gl) dá o da esquerda (negativo)"),
 ("t crítico bicaudal", "T.INV.2T(α,gl)", "INV.T.BC(α;gl)", "qt(1-alpha/2,gl)", "ex. 2,093 (gl 19)", "entra α inteiro, a função divide"),
 ("valor-p t, cauda direita", "T.DIST.RT(t,gl)", "DIST.T.CD(t;gl)", "pt(t,gl,lower.tail=FALSE)", "área à direita", ""),
 ("valor-p t, cauda esquerda", "T.DIST(t,gl,TRUE)", "DIST.T(t;gl;VERDADEIRO)", "pt(t,gl)", "área à esquerda", ""),
 ("valor-p t, bicaudal", "T.DIST.2T(ABS(t),gl)", "DIST.T.BC(ABS(t);gl)", "2*pt(-abs(t),gl)", "dobro da cauda", "T.DIST.2T exige t >= 0: use ABS"),
 ("Qui-quadrado crítico", "CHISQ.INV.RT(α,gl)", "INV.QUIQUA.CD(α;gl)", "qchisq(1-alpha,gl)", "ex. 5,991 (gl 2)", "sempre cauda direita"),
 ("valor-p qui-quadrado", "CHISQ.DIST.RT(x2,gl)", "DIST.QUIQUA.CD(x2;gl)", "pchisq(x2,gl,lower.tail=FALSE)", "área à direita", ""),
 ("Atalho: t pareado", "T.TEST(dep,ant,caudas,1)", "TESTE.T(dep;ant;caudas;1)", "t.test(dep,ant,paired=TRUE)", "só o valor-p", "caudas=1 devolve a cauda do |t|, não sabe a direção de H1"),
 ("Atalho: t duas amostras (Welch)", "T.TEST(A,B,2,3)", "TESTE.T(A;B;2;3)", "t.test(A,B)", "só o valor-p", "tipo 3 = variâncias diferentes; tipo 2 = iguais"),
 ("Atalho: Z uma média", "Z.TEST(range,μ0,σ)", "TESTE.Z(intervalo;μ0;σ)", "(na mão)", "valor-p da cauda superior", "cauda inferior: 1-Z.TEST; bicaudal: 2*MIN(Z.TEST,1-Z.TEST)"),
 ("Atalho: qui-quadrado", "CHISQ.TEST(obs,esp)", "TESTE.QUIQUA(obs;esp)", "chisq.test(x=obs,p=p) / chisq.test(tab)", "só o valor-p", "esperadas você calcula; a estatística não sai da função"),
 ("Proporção: função pronta", "(na mão)", "(na mão)", "prop.test(x,n,p=p0,alternative=,correct=FALSE)", "X-squared = z², mesmo valor-p", "default correct=TRUE muda o valor-p"),
]
for i, row in enumerate(mapa, 5):
    for j, v in enumerate(row, 1):
        ws.cell(row=i, column=j, value=v)
widths(ws, {"A": 30, "B": 32, "C": 36, "D": 40, "E": 26, "F": 52})

# ---------------- 1_Z_Media ----------------
ws = wb.create_sheet("1_Z_Media"); v = d["t1_vendas"]
title(ws, "1. Z para uma média, σ conhecido: vendas diárias (meta R$ 500)", "Amostra de 36 dias, média 520, σ populacional 30. 'As vendas aumentaram?'")
ref = rows(ws, "C", "D", 4, [
 ("1. H0", "μ ≤ 500", {}), ("1. H1", "μ > 500  (unicaudal à direita)", {}),
 ("2. α", v["alpha"], {"inp": True}), ("μ0 (H0)", v["mu0"], {"inp": True}),
 ("σ populacional (dado)", v["sigma"], {"inp": True}), ("n", v["n"], {"inp": True}), ("x̄ (média amostral)", v["xbar"], {"inp": True}),
 ("3. Erro-padrão σ/√n", "=D8/SQRT(D9)", {"fmt": "0.000"}),
 ("3. z", "=(D10-D7)/D11", {"fmt": "0.000", "name": "t1_z"}),
 ("4. z crítico (1-α)", "=NORM.S.INV(1-D6)", {"fmt": "0.000", "name": "t1_crit"}),
 ("4. valor-p (área à direita)", "=1-NORM.S.DIST(D12,TRUE)", {"fmt": "0.00000", "name": "t1_p"}),
 ("5. Decisão", '=IF(D14<D6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("5. Interpretação", "Há evidência, a 5%, de que a média de vendas superou a meta de 500. O 520 é da amostra, não é 'a' média populacional.", {}),
])
widths(ws, {"C": 30, "D": 60})

# ---------------- 2_T_Media (2a sumário | 2b dados brutos) ----------------
ws = wb.create_sheet("2_T_Media"); s2 = d["t2a_satisf"]
title(ws, "2. t para uma média (σ desconhecido): 2a satisfação (sumário) e 2b SLA 48h (dados brutos)")
ws["C3"] = "2a. Satisfação: benchmark 7,0, n = 20, x̄ = 6,8, s = 0,5"; ws["C3"].font = BOLD
rows(ws, "C", "D", 4, [
 ("2. α", s2["alpha"], {"inp": True}), ("μ0", s2["mu0"], {"inp": True}), ("n", s2["n"], {"inp": True}),
 ("x̄", s2["xbar"], {"inp": True}), ("s (amostral)", s2["s"], {"inp": True}),
 ("gl = n-1", "=D6-1", {}), ("3. Erro-padrão s/√n", "=D8/SQRT(D6)", {"fmt": "0.000"}),
 ("3. t", "=(D7-D5)/D10", {"fmt": "0.000", "name": "t2a_t"}),
 ("Leitura 1: H1 μ ≠ 7 (bicaudal)", None, {}),
 ("4. t crítico bicaudal ±", "=T.INV.2T(D4,D9)", {"fmt": "0.000", "name": "t2a_crit_bi"}),
 ("4. valor-p bicaudal", "=T.DIST.2T(ABS(D11),D9)", {"fmt": "0.0000", "name": "t2a_p_bi"}),
 ("5. Decisão bicaudal", '=IF(D14<D4,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("Leitura 2: H1 μ < 7 (unicaudal esquerda)", None, {}),
 ("4. t crítico esquerda", "=T.INV(D4,D9)", {"fmt": "0.000", "name": "t2a_crit_esq"}),
 ("4. valor-p esquerda", "=T.DIST(D11,D9,TRUE)", {"fmt": "0.0000", "name": "t2a_p_esq"}),
 ("5. Decisão unicaudal", '=IF(D18<D4,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("Pegadinha", "Mesma amostra, decisões diferentes: a cauda vem do enunciado.", {}),
])
rng_sla = data_col(ws, "A", 4, "SLA (h)", d["t2b_sla"])
ws["F3"] = "2b. SLA 48h: n = 25 entregas na coluna A. 'Está estourando o SLA?'"; ws["F3"].font = BOLD
rows(ws, "F", "G", 4, [
 ("1. H0", "μ ≤ 48", {}), ("1. H1", "μ > 48  (unicaudal à direita)", {}),
 ("2. α", 0.05, {"inp": True}), ("μ0", d["t2b_mu0"], {"inp": True}),
 ("3. n", f"=COUNT({rng_sla})", {}), ("3. x̄", f"=AVERAGE({rng_sla})", {"fmt": "0.000", "name": "t2b_xbar"}),
 ("3. s", f"=STDEV.S({rng_sla})", {"fmt": "0.000", "name": "t2b_s"}),
 ("3. Erro-padrão s/√n", "=G10/SQRT(G8)", {"fmt": "0.000"}), ("gl = n-1", "=G8-1", {}),
 ("3. t", "=(G9-G7)/G11", {"fmt": "0.000", "name": "t2b_t"}),
 ("4. t crítico direita", "=T.INV(1-G6,G12)", {"fmt": "0.000", "name": "t2b_crit"}),
 ("4. valor-p direita", "=T.DIST.RT(G13,G12)", {"fmt": "0.0000", "name": "t2b_p"}),
 ("5. Decisão a 5%", '=IF(G15<G6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("α alternativo", 0.01, {"inp": True}),
 ("5. Decisão a 1%", '=IF(G15<G17,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("5. Interpretação", "A 5% há evidência de que o tempo médio passa das 48h prometidas; a 1% a amostra não basta. Reportar os dois.", {}),
])
widths(ws, {"A": 10, "C": 34, "D": 22, "F": 30, "G": 40})

# ---------------- 3_Pareado ----------------
ws = wb.create_sheet("3_Pareado")
title(ws, "3. t pareado: vendas diárias (R$ mil) das mesmas 12 lojas, antes e depois da campanha", "D = Depois − Antes. 'A campanha aumentou as vendas?'")
n3 = len(d["t3_antes"])
r_ant = data_col(ws, "A", 4, "Antes", d["t3_antes"]); r_dep = data_col(ws, "B", 4, "Depois", d["t3_depois"])
ws["C3"] = "D = Depois-Antes"; ws["C3"].font = BOLD
for i in range(n3): put(ws, f"C{4+i}", f"=B{4+i}-A{4+i}", fmt="0.0")
r_D = f"C4:C{3+n3}"
rows(ws, "E", "F", 4, [
 ("1. H0", "μ_D ≤ 0", {}), ("1. H1", "μ_D > 0  (unicaudal à direita)", {}), ("2. α", 0.05, {"inp": True}),
 ("3. n (pares)", f"=COUNT({r_D})", {}), ("3. D médio", f"=AVERAGE({r_D})", {"fmt": "0.000", "name": "t3_dbar"}),
 ("3. s_D", f"=STDEV.S({r_D})", {"fmt": "0.000", "name": "t3_sd"}),
 ("3. Erro-padrão s_D/√n", "=F9/SQRT(F7)", {"fmt": "0.000"}), ("gl = n-1", "=F7-1", {}),
 ("3. t", "=(F8-0)/F10", {"fmt": "0.000", "name": "t3_t"}),
 ("4. t crítico direita", "=T.INV(1-F6,F11)", {"fmt": "0.000", "name": "t3_crit"}),
 ("4. valor-p direita", "=T.DIST.RT(F12,F11)", {"fmt": "0.0000", "name": "t3_p"}),
 ("5. Decisão", '=IF(F14<F6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("IC 95% de μ_D: inferior", "=F8-T.INV.2T(0.05,F11)*F10", {"fmt": "0.00", "name": "t3_ic_lo"}),
 ("IC 95% de μ_D: superior", "=F8+T.INV.2T(0.05,F11)*F10", {"fmt": "0.00", "name": "t3_ic_hi"}),
 ("Atalho T.TEST(dep,ant,1,1)", f"=T.TEST({r_dep},{r_ant},1,1)", {"fmt": "0.0000"}),
 ("Obs. do atalho", "caudas=1 devolve a cauda de |t|: só vale se D médio tem o sinal de H1", {}),
 ("5. Interpretação", "Há evidência de que a campanha aumentou as vendas. Efeito médio = D médio, com o IC como faixa plausível.", {}),
])
widths(ws, {"A": 9, "B": 9, "C": 16, "E": 30, "F": 44})

# ---------------- 4_Welch ----------------
ws = wb.create_sheet("4_Welch")
title(ws, "4. t para duas médias independentes (Welch): ticket médio (R$) loja A vs loja B", "Amostras de clientes diferentes. 'Os tickets médios diferem?' Extensão além dos slides.")
r_A = data_col(ws, "A", 4, "Loja A", d["t4_A"]); r_B = data_col(ws, "B", 4, "Loja B", d["t4_B"])
rows(ws, "D", "E", 4, [
 ("1. H0", "μ_A = μ_B", {}), ("1. H1", "μ_A ≠ μ_B  (bicaudal)", {}), ("2. α", 0.05, {"inp": True}),
 ("nA", f"=COUNT({r_A})", {}), ("nB", f"=COUNT({r_B})", {}),
 ("x̄A", f"=AVERAGE({r_A})", {"fmt": "0.000"}), ("x̄B", f"=AVERAGE({r_B})", {"fmt": "0.000"}),
 ("sA", f"=STDEV.S({r_A})", {"fmt": "0.000"}), ("sB", f"=STDEV.S({r_B})", {"fmt": "0.000"}),
 ("3. Erro-padrão √(sA²/nA+sB²/nB)", "=SQRT(E11^2/E7+E12^2/E8)", {"fmt": "0.000"}),
 ("3. t", "=(E9-E10)/E13", {"fmt": "0.000", "name": "t4_t"}),
 ("gl de Welch", "=E13^4/((E11^2/E7)^2/(E7-1)+(E12^2/E8)^2/(E8-1))", {"fmt": "0.00", "name": "t4_gl"}),
 ("4. t crítico bicaudal ±", "=T.INV.2T(E6,E15)", {"fmt": "0.000", "name": "t4_crit"}),
 ("4. valor-p bicaudal", "=T.DIST.2T(ABS(E14),E15)", {"fmt": "0.0000", "name": "t4_p"}),
 ("5. Decisão", '=IF(E17<E6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("Atalho T.TEST(A,B,2,3)", f"=T.TEST({r_A},{r_B},2,3)", {"fmt": "0.0000", "name": "t4_p_ttest"}),
 ("Obs.", "Excel trunca gl não inteiro em T.DIST/T.INV; R usa gl fracionário. Diferença na 3ª casa do valor-p é isso.", {}),
 ("5. Interpretação", "A 5% a amostra não sustenta que os tickets médios diferem (valor-p acima de α por pouco). Não é prova de igualdade.", {}),
])
widths(ws, {"A": 9, "B": 9, "D": 34, "E": 44})

# ---------------- 5_Proporcao ----------------
ws = wb.create_sheet("5_Proporcao"); g = d["t5_golfe"]
title(ws, "5. Z para uma proporção: clube de golfe, baseline 20% de mulheres", "Após a promoção: 100 mulheres em 400 jogadores. 'A proporção aumentou?'")
rows(ws, "C", "D", 4, [
 ("1. H0", "p ≤ 0,20", {}), ("1. H1", "p > 0,20  (unicaudal à direita)", {}), ("2. α", g["alpha"], {"inp": True}),
 ("x (sucessos)", g["x"], {"inp": True}), ("n", g["n"], {"inp": True}), ("p0 (H0)", g["p0"], {"inp": True}),
 ("3. p̂ = x/n", "=D7/D8", {"fmt": "0.000"}),
 ("3. Erro-padrão √(p0(1-p0)/n)", "=SQRT(D9*(1-D9)/D8)", {"fmt": "0.0000"}),
 ("3. z", "=(D10-D9)/D11", {"fmt": "0.000", "name": "t5_z"}),
 ("4. z crítico (1-α)", "=NORM.S.INV(1-D6)", {"fmt": "0.000", "name": "t5_crit"}),
 ("4. valor-p direita", "=1-NORM.S.DIST(D12,TRUE)", {"fmt": "0.0000", "name": "t5_p"}),
 ("5. Decisão", '=IF(D14<D6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("Erro comum: EP com p̂ no denominador", "=SQRT(D10*(1-D10)/D8)", {"fmt": "0.0000"}),
 ("z errado com esse EP", "=(D10-D9)/D16", {"fmt": "0.000"}),
 ("5. Interpretação", "Fortes evidências de que a proporção de mulheres passou de 20%. Não diz que 'é 25%': 0,25 é da amostra.", {}),
])
widths(ws, {"C": 36, "D": 60})

# ---------------- 6_Qui_Aderencia ----------------
ws = wb.create_sheet("6_Qui_Aderencia"); q6 = d["t6_pagto"]; k = len(q6["obs"])
title(ws, "6. Qui-quadrado de aderência: mix de pagamento (esperado 45/35/20)", "n = 200 compras. 'A distribuição observada segue o mix esperado?'")
for j, h in enumerate(["Categoria", "Observado O", "p esperada", "Esperado E = n·p", "(O-E)²/E"], 1):
    c = ws.cell(row=3, column=j, value=h); c.font = BOLD; c.fill = GREY
for i in range(k):
    r = 4 + i
    ws[f"A{r}"] = q6["cat"][i]; put(ws, f"B{r}", q6["obs"][i], inp=True); put(ws, f"C{r}", q6["p"][i], inp=True)
    put(ws, f"D{r}", f"=C{r}*$B${4+k}", fmt="0.00"); put(ws, f"E{r}", f"=(B{r}-D{r})^2/D{r}", fmt="0.0000")
tot = 4 + k
ws[f"A{tot}"] = "Total"; put(ws, f"B{tot}", f"=SUM(B4:B{tot-1})"); put(ws, f"C{tot}", f"=SUM(C4:C{tot-1})"); put(ws, f"D{tot}", f"=SUM(D4:D{tot-1})")
rows(ws, "G", "H", 4, [
 ("1. H0", "distribuição observada segue 45/35/20", {}), ("1. H1", "pelo menos uma proporção difere", {}), ("2. α", 0.05, {"inp": True}),
 ("3. χ² = Σ(O-E)²/E", f"=SUM(E4:E{tot-1})", {"fmt": "0.000", "name": "t6_x2"}),
 ("gl = k-1", f"=COUNT(B4:B{tot-1})-1", {}),
 ("4. χ² crítico (cauda direita)", "=CHISQ.INV.RT(H6,H8)", {"fmt": "0.000", "name": "t6_crit"}),
 ("4. valor-p", "=CHISQ.DIST.RT(H7,H8)", {"fmt": "0.0000", "name": "t6_p"}),
 ("5. Decisão", '=IF(H10<H6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("Atalho CHISQ.TEST(obs,esp)", f"=CHISQ.TEST(B4:B{tot-1},D4:D{tot-1})", {"fmt": "0.0000"}),
 ("5. Interpretação", "A amostra é consistente com o mix esperado; não há evidência de mudança no comportamento de pagamento.", {}),
])
widths(ws, {"A": 12, "B": 13, "C": 12, "D": 18, "E": 12, "G": 32, "H": 46})

# ---------------- 7_Qui_Independencia ----------------
ws = wb.create_sheet("7_Qui_Independencia"); q7 = d["t7_canal"]; R, C = len(q7["linhas"]), len(q7["colunas"])
title(ws, "7. Qui-quadrado de independência: canal de marketing x compra (n = 320 leads)", "'A chance de compra depende do canal?'")
def matriz(ws, top, left, label, cells, fmt=None, inp=False):
    ws.cell(row=top, column=left, value=label).font = BOLD
    for j, h in enumerate(q7["colunas"]): ws.cell(row=top, column=left+1+j, value=h).font = BOLD
    for i, rl in enumerate(q7["linhas"]):
        ws.cell(row=top+1+i, column=left, value=rl)
        for j in range(C):
            put(ws, f"{get_column_letter(left+1+j)}{top+1+i}", cells[i][j], inp=inp, fmt=fmt)
    return top+1, left+1   # primeira célula de dados (linha, coluna)
r0, c0 = matriz(ws, 3, 1, "Observado", q7["obs"], inp=True)              # B4:C6
ws.cell(row=3, column=4, value="Total linha").font = BOLD
for i in range(R): put(ws, f"D{r0+i}", f"=SUM(B{r0+i}:C{r0+i})")
ws.cell(row=r0+R, column=1, value="Total coluna").font = BOLD
for j in range(C): put(ws, f"{get_column_letter(c0+j)}{r0+R}", f"=SUM({get_column_letter(c0+j)}{r0}:{get_column_letter(c0+j)}{r0+R-1})")
put(ws, f"D{r0+R}", f"=SUM(D{r0}:D{r0+R-1})")   # n em D7
nref = f"$D${r0+R}"
esp = [[f"=$D${r0+i}*{get_column_letter(c0+j)}${r0+R}/{nref}" for j in range(C)] for i in range(R)]
matriz(ws, 9, 1, "Esperado E", esp, fmt="0.00")                            # B10:C12
contrib = [[f"=(B{r0+i}-B{10+i})^2/B{10+i}" if j == 0 else f"=(C{r0+i}-C{10+i})^2/C{10+i}" for j in range(C)] for i in range(R)]
matriz(ws, 15, 1, "(O-E)²/E", contrib, fmt="0.0000")                       # B16:C18
resid = [[f"=(B{r0+i}-B{10+i})/SQRT(B{10+i})" if j == 0 else f"=(C{r0+i}-C{10+i})/SQRT(C{10+i})" for j in range(C)] for i in range(R)]
matriz(ws, 21, 1, "Resíduo (O-E)/√E", resid, fmt="0.00")                   # B22:C24
ws["A26"] = "Taxa de compra por canal"; ws["A26"].font = BOLD
for i in range(R):
    ws[f"A{27+i}"] = q7["linhas"][i]; put(ws, f"B{27+i}", f"=B{r0+i}/D{r0+i}", fmt="0%")
rows(ws, "F", "G", 4, [
 ("1. H0", "canal e compra são independentes", {}), ("1. H1", "existe associação", {}), ("2. α", 0.05, {"inp": True}),
 ("3. χ² = ΣΣ(O-E)²/E", "=SUM(B16:C18)", {"fmt": "0.000", "name": "t7_x2"}),
 ("gl = (r-1)(c-1)", "=(ROWS(B4:C6)-1)*(COLUMNS(B4:C6)-1)", {}),
 ("4. χ² crítico", "=CHISQ.INV.RT(G6,G8)", {"fmt": "0.000", "name": "t7_crit"}),
 ("4. valor-p", "=CHISQ.DIST.RT(G7,G8)", {"fmt": "0.0000", "name": "t7_p"}),
 ("5. Decisão", '=IF(G10<G6,"Rejeita H0","Não rejeita H0")', {"bold": True}),
 ("Atalho CHISQ.TEST(obs,esp)", "=CHISQ.TEST(B4:C6,B10:C12)", {"fmt": "0.0000"}),
 ("Menor esperada (regra ≥ 5)", "=MIN(B10:C12)", {"fmt": "0.00"}),
 ("5. Interpretação", "A probabilidade de compra depende do canal. Pelos resíduos e pelas taxas, Search é o canal forte, Social o fraco.", {}),
])
widths(ws, {"A": 22, "B": 13, "C": 13, "D": 12, "F": 30, "G": 52})

# ---------------- Exercicios ----------------
ws = wb.create_sheet("Exercicios")
title(ws, "Exercícios E1 a E4: só dados. Gabarito no fim do md.")
ws["A3"] = "E1 Atendimento (min). 'Mudou de 10 min?' α = 5%"; ws["A3"].font = BOLD
data_col(ws, "A", 5, "min", d["e1_atend"])
ws["C3"] = "E2 Conversão. Era 30%. 'Mudou?'"; ws["C3"].font = BOLD
rows(ws, "C", "D", 4, [("x (conversões)", d["e2_conv"]["x"], {"inp": True}), ("n (visitas)", d["e2_conv"]["n"], {"inp": True}), ("p0", d["e2_conv"]["p0"], {"inp": True})])
ws["F3"] = "E3a Mesmas 10 pessoas, min/tarefa antes e depois do treinamento. 'Reduziu?'"; ws["F3"].font = BOLD
data_col(ws, "F", 5, "Antes", d["e3a_antes"]); data_col(ws, "G", 5, "Depois", d["e3a_depois"])
ws["I3"] = "E3b Notas de duas turmas diferentes. 'As médias diferem?'"; ws["I3"].font = BOLD
data_col(ws, "I", 5, "Turma A", d["e3b_A"]); data_col(ws, "J", 5, "Turma B", d["e3b_B"])
ws["L3"] = "E4 Sabores. 'Preferência uniforme (25% cada)?'"; ws["L3"].font = BOLD
ws["L4"] = "Sabor"; ws["M4"] = "Observado"; ws["L4"].font = ws["M4"].font = BOLD
for i, (c_, o) in enumerate(zip(d["e4_sabores"]["cat"], d["e4_sabores"]["obs"])):
    ws[f"L{5+i}"] = c_; put(ws, f"M{5+i}", o, inp=True)
widths(ws, {"A": 10, "C": 18, "D": 10, "F": 10, "G": 10, "I": 10, "J": 10, "L": 10, "M": 12})

for w in wb.worksheets:
    w.sheet_view.showGridLines = True
    for row in w.iter_rows():
        for c in row:
            if isinstance(c.value, str) and len(c.value) > 40: c.alignment = Alignment(wrap_text=True, vertical="top")

out = os.path.join(AULA, "TestesHipotese.xlsx")
wb.save(out)
json.dump(cell_map, open(os.path.join(HERE, "cell_map.json"), "w"), indent=1)
print("salvo:", out); print("cell_map:", len(cell_map), "entradas")
```

- [ ] **Step 2: Rodar**

Run: `python3 ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/build_xlsx.py`
Expected: `salvo: .../TestesHipotese.xlsx` e `cell_map: 35 entradas` (34 nomes de teste + `t4_p_ttest`).

- [ ] **Step 3: Conferir prefixo `_xlfn.` gravado**

Run: `python3 -c "import openpyxl;wb=openpyxl.load_workbook('$HOME/FGV/Estatistica2/Aulas/08.17/TestesHipotese.xlsx');print(wb['1_Z_Media']['D13'].value, '|', wb['2_T_Media']['D14'].value)"`
Expected: `=_xlfn.NORM.S.INV(1-D6) | =_xlfn.T.DIST.2T(ABS(D11),D9)`.

---

### Task 4: Recalcular e cruzar Excel x R x scipy

**Files:**
- Create: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/recalc_check.py`

Depende de: Tasks 2 e 3.

- [ ] **Step 1: Escrever `recalc_check.py`**

```python
#!/usr/bin/env python3
"""Recalcula o xlsx no LibreOffice headless, lê os valores das células do cell_map e
compara com r_results.csv (R) e com scipy. Sai com código 1 se algum par falhar."""
import csv, json, os, shutil, subprocess, sys, tempfile
import openpyxl
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
AULA = os.path.dirname(os.path.dirname(HERE))
XLSX = os.path.join(AULA, "TestesHipotese.xlsx")
d = json.load(open(os.path.join(HERE, "dados.json")))
cell_map = json.load(open(os.path.join(HERE, "cell_map.json")))
r_vals = {row["nome"]: float(row["valor"]) for row in csv.DictReader(open(os.path.join(HERE, "r_results.csv")))}

# 1) recálculo headless (LibreOffice recalcula fórmulas sem valor em cache ao converter)
tmp = tempfile.mkdtemp()
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", tmp, XLSX],
               check=True, capture_output=True, timeout=180)
recalc = os.path.join(tmp, "TestesHipotese.xlsx")
wb = openpyxl.load_workbook(recalc, data_only=True)
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
r = stats.chi2_contingency(d["t7_canal"]["obs"], correction=False); sp.update(t7_x2=r[0], t7_p=r[1], t7_crit=stats.chi2.ppf(0.95, 2))
r = stats.ttest_1samp(d["e1_atend"], 10); sp.update(e1_t=r.statistic, e1_p=r.pvalue, e1_crit=stats.t.ppf(0.975, 11))
e = d["e2_conv"]; z = (e["x"]/e["n"]-e["p0"])/((e["p0"]*(1-e["p0"])/e["n"])**0.5); sp.update(e2_z=z, e2_p=2*stats.norm.sf(abs(z)))
r = stats.ttest_rel(d["e3a_depois"], d["e3a_antes"], alternative="less"); sp.update(e3a_t=r.statistic, e3a_p=r.pvalue)
r = stats.ttest_ind(d["e3b_A"], d["e3b_B"], equal_var=False); sp.update(e3b_t=r.statistic, e3b_p=r.pvalue)
r = stats.chisquare(d["e4_sabores"]["obs"]); sp.update(e4_x2=r.statistic, e4_p=r.pvalue, e4_crit=stats.chi2.ppf(0.95, 3))

# 3) tabela cruzada
TOL = {"t4_crit": 0.02, "t4_p": 0.01}   # Excel trunca gl de Welch (documentado no md e na aba 4_Welch)
falhas = 0
print(f"{'nome':14}{'R':>12}{'Excel':>12}{'scipy':>12}  status")
for name in r_vals:
    rv = r_vals[name]; ev = xl(name) if name in cell_map else None; sv = sp.get(name)
    tol = TOL.get(name, 1e-3); status = []
    if ev is not None:
        if not isinstance(ev, (int, float)): status.append(f"EXCEL NÃO NUMÉRICO: {ev!r}"); falhas += 1
        elif abs(ev - rv) > tol: status.append(f"R x Excel diff={ev-rv:+.5f}"); falhas += 1
    if sv is not None and abs(sv - rv) > 1e-6: status.append(f"R x scipy diff={sv-rv:+.2e}"); falhas += 1
    print(f"{name:14}{rv:12.5f}{(ev if isinstance(ev,(int,float)) else float('nan')):12.5f}{(sv if sv is not None else float('nan')):12.5f}  {'ok' if not status else '; '.join(status)}")
ev = xl("t4_p_ttest"); print(f"{'t4_p_ttest':14}{'':>12}{ev:12.5f}{'':>12}  (T.TEST tipo 3, comparar com t4_p)")
shutil.rmtree(tmp)
print("\nFALHAS:", falhas); sys.exit(1 if falhas else 0)
```

- [ ] **Step 2: Rodar**

Run: `python3 ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/recalc_check.py`
Expected: tabela com todas as linhas `ok` e `FALHAS: 0`. Se `EXCEL NÃO NUMÉRICO`, a fórmula não foi reconhecida (checar prefixo `_xlfn.` ou sintaxe). Se `R x Excel diff` fora da tolerância em algo além de t4, é bug de referência de célula: abrir a aba, corrigir em `build_xlsx.py`, refazer Task 3 Step 2 e este passo. Registrar no fim do plano o diff observado em t4_p (Excel trunca gl).

- [ ] **Step 3: Anotar no Registro**

Copiar a tabela final pra seção Registro deste plano.

---

### Task 5: Escrever a aula (md do vault)

**Files:**
- Create: `~/FGV/Estatistica2/Aulas/08.17/AulaTestesHipoteseExcelR.md`
- Create: `~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/lint_md.py`

Depende de: Tasks 2 e 4 (números finais). Fonte dos blocos de output: `r_output.txt`.

- [ ] **Step 1: Escrever `lint_md.py`**

```python
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
existentes = {os.path.splitext(os.path.basename(p))[0].lower() for p in glob.glob(os.path.join(CONC, "*.md"))}
faltando = sorted({l.split("|")[0].strip() for l in re.findall(r"\[\[([^\]]+)\]\]", txt) if l.split("|")[0].strip().lower() not in existentes})
if faltando: erros.append("wikilinks sem nota: " + ", ".join(faltando))
# números-chave (formato PT, 2 ou 3 casas) precisam aparecer no texto
r = {row["nome"]: float(row["valor"]) for row in csv.DictReader(open(os.path.join(HERE, "r_results.csv")))}
def pt(x, nd): return f"{x:.{nd}f}".replace(".", ",")
chaves = {"t1_z": 1, "t2a_t": 3, "t2a_crit_bi": 3, "t2a_crit_esq": 3, "t2b_t": 3, "t2b_crit": 3, "t3_t": 3, "t4_t": 3, "t4_gl": 2,
          "t5_z": 1, "t5_crit": 3, "t6_x2": 3, "t6_crit": 3, "t7_x2": 3, "t7_crit": 3, "e2_z": 2, "e4_x2": 1}
for k, nd in chaves.items():
    if pt(r[k], nd) not in txt and pt(r[k], nd).rstrip("0").rstrip(",") not in txt: erros.append(f"número-chave ausente: {k} = {pt(r[k], nd)}")
front = txt.split("---")[1] if txt.startswith("---") else ""
for campo in ["materia: Estatistica2", "data: 2026-08-17", "tags: [aula, estudo]"]:
    if campo not in front: erros.append("YAML sem " + campo)
print("\n".join(erros) if erros else "lint ok"); sys.exit(1 if erros else 0)
```

- [ ] **Step 2: Escrever o md**

Regras de forma: YAML da spec; sem travessão; sem (i)(ii); sem fonte; fórmula inline como =`FUNCAO()`; blocos multi-linha (Excel, R, output) em `<pre>` com `<` `>` `&` escapados (`&lt;` `&gt;` `&amp;`); wikilinks só nos conceitos da lista (existentes + os 8 novos da Task 6); números em formato PT no texto (vírgula decimal), outputs do R colados como saíram (ponto decimal). Todo número numérico do texto sai de `r_output.txt` ou `r_results.csv`.

Esqueleto obrigatório (títulos exatos, conteúdo mínimo por seção):

```
---
materia: Estatistica2
data: 2026-08-17
tema: Testes de hipótese em Excel e R (revisão aulas 2 a 6)
tags: [aula, estudo]
---

## 0. Como usar
3 linhas: ler o bloco do teste; refazer na aba correspondente do TestesHipotese.xlsx (mudar um dado, ver a decisão virar); refazer no R colando o bloco do TestesHipotese.R; depois os exercícios da seção 5 sem olhar o gabarito.

## 1. Setup
### R no terminal
<pre> brew install r; R; q() </pre>, 10 comandos de sobrevivência em tabela (c, mean, sd, length, sqrt, ?funcao, t.test, prop.test, chisq.test, source), como rodar o script (3 formas).
### Excel
Nomes EN x PT (aponta pra seção 3), separador de argumento (vírgula EN, ponto e vírgula PT), Análise de Dados como opcional (não usado na aula), regra azul = input, preto = fórmula.

## 2. A receita e a escolha do teste
Os 5 passos do professor (bloco `<pre>`). Tabela de escolha: colunas Situação do enunciado | Teste | Estatística | Distribuição e gl | Excel | R, linhas: uma média com σ dado; uma média com s; antes/depois nas mesmas unidades; dois grupos diferentes; proporção (0/1); contagens em categorias (1 variável); contagens cruzadas (2 variáveis). Parágrafo curto: caudalidade pelo verbo do enunciado, baseline fica em H0 com ≤, ≥ ou =.

## 3. Mapa de funções
Mesma tabela da aba Mapa (20 linhas), Objetivo | Excel EN | Excel PT | R | Devolve | Observação.

## 4. Os sete testes
### 4.1 Z para uma média com σ conhecido (vendas, meta 500)
### 4.2 t para uma média: sumário (satisfação 7,0) e dados brutos (SLA 48h)
### 4.3 t pareado (12 lojas, antes/depois)
### 4.4 Duas médias independentes, Welch (ticket loja A vs B)
### 4.5 Z para uma proporção (golfe, 20% para 25%)
### 4.6 Qui-quadrado de aderência (mix de pagamento)
### 4.7 Qui-quadrado de independência (canal x compra)
Cada subseção, nesta ordem: Enunciado (2 linhas) → Passos 1 e 2 (H0, H1, cauda com o verbo que a define, α) → Passo 3 (fórmula em <pre>, escolha Z ou T justificada) → Excel (bloco <pre> com célula: fórmula, espelhando a aba; ler "aba X do xlsx") → R (bloco <pre> com o código do script + bloco <pre> com o output real recortado de r_output.txt) → Passos 4 e 5 (crítico, valor-p, decisão, frase de interpretação empresarial) → Pegadinha (1 a 3 bullets). Em 4.2 mostrar as duas leituras da satisfação e a decisão a 5% e a 1% do SLA. Em 4.3 reportar D médio e IC. Em 4.4 explicar a divergência Excel x R no valor-p (gl truncado). Em 4.5 mostrar prop.test com e sem correção. Em 4.7 mostrar esperadas, resíduos e taxa por canal.

## 5. Exercícios (faça nas duas ferramentas antes de olhar o gabarito)
E1 a E4 com enunciado e dados (dados de E3 listados; aba Exercicios do xlsx e seção 8 do .R têm os mesmos).

## 6. Pegadinhas consolidadas e frases de interpretação
Bullets ordenados (o que o professor martelou primeiro): 1,645 vs 1,96; p0 no denominador; interpretação (rejeitar não diz o valor novo, não rejeitar não prova H0); n maior → EP menor → estatística maior; α = P(erro tipo I); a cauda vem do enunciado (satisfação); T.DIST.2T exige ABS; T.INV(α) é o crítico da esquerda; STDEV.S não STDEV.P; T.TEST caudas=1 não sabe a direção; prop.test corrige continuidade por default; Excel trunca gl não inteiro; qui-quadrado sempre cauda direita, gl k-1 ou (r-1)(c-1), esperadas ≥ 5; CHISQ.TEST devolve valor-p, não estatística.
Templates de frase: rejeita / não rejeita, uni e bicaudal, proporção, qui-quadrado (4 frases modelo).

---
## 7. Gabarito (só depois de tentar)
E1..E4: estatística, crítico, valor-p, decisão. Números de r_results.csv.
```

- [ ] **Step 3: Rodar o lint**

Run: `python3 ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/lint_md.py`
Expected: `lint ok`. Se listar `wikilinks sem nota`, e forem os 8 nomes da Task 6, seguir pra Task 6 e rodar de novo depois. Qualquer outro erro: corrigir no md.

---

### Task 6: Notas de conceito novas no vault

**Files:**
- Create em `~/FGV/Vault/Conceitos/`: `Teste bicaudal.md`, `Nivel de significancia.md`, `Teste pareado.md`, `Teste t para duas amostras.md`, `Teste qui-quadrado de aderencia.md`, `Teste qui-quadrado de independencia.md`, `Frequencia esperada.md`, `Distribuicao qui-quadrado.md`

- [ ] **Step 1: Confirmar que não existem**

Run: `cd ~/FGV/Vault/Conceitos && ls "Teste bicaudal.md" "Nivel de significancia.md" "Teste pareado.md" "Teste t para duas amostras.md" "Teste qui-quadrado de aderencia.md" "Teste qui-quadrado de independencia.md" "Frequencia esperada.md" "Distribuicao qui-quadrado.md" 2>&1 | grep -c "No such"`
Expected: `8`. Se algum existir, não tocar nele.

- [ ] **Step 2: Criar as 8 notas com o template**

Template exato (`~/FGV/Vault/Templates/Conceito.md`), preenchido só com o que a aula ensina; `materias: [Estatistica2]`; título H1 = nome do arquivo; Definição em 1 a 3 linhas; Fórmula / aplicação em `<pre>`; "Onde aparece nas aulas" mantém a query Dataview do template intacta; Conceitos relacionados com 2 a 4 wikilinks existentes. Modelo pra uma delas (as outras seguem o mesmo molde):

```
---
tipo: conceito
materias: [Estatistica2]
tags: [conceito]
---

# Teste pareado

## Definição

Teste t aplicado às diferenças D = Depois − Antes medidas nas mesmas unidades (mesmas lojas, mesmas pessoas). Vira um teste de uma média sobre D com μ_D = 0 em H0.

## Fórmula / aplicação

<pre>
t = D̄ / (s_D / √n),  gl = n − 1
Excel: coluna D e o bloco de uma média; atalho T.TEST(dep, ant, caudas, 1)
R: t.test(depois, antes, paired = TRUE, alternative = "greater")
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Distribuicao T de Student]]
- [[Teste t para duas amostras]]
- [[Intervalo de Confiança]]
```

Conteúdo mínimo das outras sete: Teste bicaudal (H1 com ≠, α/2 por cauda, 1,96 a 5%, T.INV.2T / qt(1-α/2)); Nivel de significancia (α = P(erro tipo I), 5% default, compara com valor-p, relação com nível de confiança 1−α); Teste t para duas amostras (grupos diferentes, Welch, EP e gl de Welch, t.test(A,B), T.TEST(A,B,2,3)); Teste qui-quadrado de aderencia (uma variável categórica vs distribuição teórica, χ² = Σ(O−E)²/E, gl k−1, chisq.test(x, p)); Teste qui-quadrado de independencia (duas variáveis, tabela de contingência, E_ij, gl (r−1)(c−1), chisq.test(tab), resíduos); Frequencia esperada (E = n·p ou linha×coluna/n, regra ≥ 5); Distribuicao qui-quadrado (assimétrica, só positiva, gl, cauda direita, qchisq/pchisq, CHISQ.INV.RT/CHISQ.DIST.RT).

- [ ] **Step 3: Rodar o lint do md de novo**

Run: `python3 ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/lint_md.py`
Expected: `lint ok`.

---

### Task 7: Verificação final e entrega

- [ ] **Step 1: Rodar tudo de novo, na ordem**

Run:
```
cd ~/FGV/Estatistica2/Aulas/08.17 && Rscript TestesHipotese.R > .superpowers/build/r_output.txt 2>&1 && echo R_OK && \
Rscript .superpowers/build/check_r.R "$PWD/TestesHipotese.R" > /dev/null && echo CHECK_R_OK && \
python3 .superpowers/build/recalc_check.py | tail -3 && python3 .superpowers/build/lint_md.py
```
Expected: `R_OK`, `CHECK_R_OK`, `FALHAS: 0`, `lint ok`.

- [ ] **Step 2: Estado da pasta**

Run: `ls -la ~/FGV/Estatistica2/Aulas/08.17/ ~/FGV/Estatistica2/Aulas/08.17/.superpowers/build/ && ls ~/FGV/Vault/Conceitos | grep -E "bicaudal|significancia|pareado|duas amostras|qui-quadrado|esperada"`
Expected: 3 entregáveis + `.superpowers/`, 9 arquivos de build, 8 notas novas.

- [ ] **Step 3: Mensagem final ao Arthur**

Conteúdo: caminho dos 3 arquivos, tabela cruzada R x Excel (colada do recalc_check), linha de "como usar", a nota sobre a divergência de Welch, e a pergunta padrão de didática (CLAUDE.md: perguntar se quer explicação simples do que foi feito).

---

## Registro (preencher durante a execução)

- Seed usada: 2038 (primeira a partir de 2026 que fechou as 5 intenções)
- p-valores das intenções: SLA 0,0282 · pareado 0,0011 · Welch 0,0895 · E3a 0,0008 · E3b 0,0278
- R instalado: 4.6.1 via brew (exit 0). Workbook: 118 fórmulas, 0 erros no recalc.
- Diff observado t4 Excel x R: t4_crit 2,04523 vs 2,04274 (+0,0025), t4_p 0,08984 vs 0,08954 (+0,0003). Causa confirmada: T.DIST.2T/T.INV.2T truncam gl 29,84 → 29 (qt(0,975, 29) = 2,0452). O atalho T.TEST(A,B,2,3) usa gl fracionário e bate com o R (0,08954).
- Tabela cruzada final (Task 4): 46 pares R x scipy ok (tol 1e-6), 34 pares R x Excel ok (tol 1e-3, exceção Welch), 4 atalhos Excel = valor-p do R. FALHAS: 0.

## Self-review do plano

Cobertura da spec: §2 escopo → Tasks 2 e 3 cobrem os 7 testes e E1 a E4; §3 arquivos → Tasks 2, 3, 5, 6; §4 estrutura do md → Task 5 Step 2 (esqueleto com títulos); §5 parâmetros de simulação → Task 1; §7 layout xlsx → Task 3 (Mapa, 7 abas, Exercicios, azul/preto, formatos, atalhos); §8 script R → Task 2 (helper único, seções 0 a 9); §9 validação → Tasks 4 e 5 (cross-check com tolerância 1e-3, exceção documentada de Welch; lint de escrita, wikilinks, `<pre>`, números-chave); §10 pronto → Task 7. Placeholders: os `...VETOR...` da Task 2 são substituídos pelo output da Task 1 (instrução explícita), não são TBD. Nomes: lista de resultados idêntica em check_r.R, cell_map (via `name=`), recalc_check.py e lint_md.py; `t4_p_ttest` só existe no Excel e é tratado à parte.
