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
sla <- c(51.4, 41.8, 58.3, 48.5, 49.7, 49.5, 58.0, 49.1, 49.4, 48.9, 47.3, 49.1, 52.1,
         45.4, 54.7, 53.5, 49.7, 49.3, 49.0, 48.1, 43.6, 47.3, 52.1, 41.8, 54.0)
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
antes  <- c(177.0, 254.8, 225.2, 226.1, 221.5, 203.9, 198.6, 198.5, 208.9, 212.3, 213.6, 225.1)
depois <- c(166.3, 280.9, 253.2, 253.8, 207.3, 224.2, 226.6, 204.5, 238.0, 240.1, 246.0, 272.0)
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
A <- c(86.0, 67.0, 91.0, 80.2, 90.7, 84.2, 68.6, 76.0, 86.1, 84.0, 60.3, 85.1, 86.6, 100.4, 80.4)
B <- c(79.1, 92.0, 76.0, 74.4, 76.2, 64.1, 78.6, 102.5, 85.6, 103.5, 87.9, 90.9, 104.9, 96.3,
       81.6, 111.1, 125.0, 83.5)
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
e3a_antes  <- c(35.6, 26.5, 29.3, 35.4, 23.0, 25.4, 39.8, 29.6, 29.4, 28.2)   # mesmas 10 pessoas, min/tarefa antes
e3a_depois <- c(33.2, 26.3, 23.4, 30.6, 14.8, 21.7, 26.6, 27.1, 21.5, 15.3)   # depois. "o treinamento reduziu o tempo?"
e3b_A <- c(5.9, 8.3, 10.0, 3.9, 7.4, 3.8, 5.5, 7.4, 6.3, 6.4, 4.5, 4.2)                # notas turma A
e3b_B <- c(7.3, 8.2, 7.0, 9.4, 6.2, 9.4, 8.1, 6.9, 7.2, 9.4, 7.3, 6.8, 6.6, 7.1)      # notas turma B (outras pessoas). "as médias diferem?"
e4_obs <- c(A = 18, B = 22, C = 20, D = 20)                                           # "preferência uniforme?"

# ---- 9. GABARITO (descomente depois de tentar) ------------------------
# E1: t.test(e1_atend, mu = 10)                       # bicaudal; t ~ 1.85, p ~ 0.09, não rejeita
# E2: z <- (e2_x/e2_n - e2_p0)/sqrt(e2_p0*(1-e2_p0)/e2_n); 2*(1-pnorm(abs(z)))   # p ~ 0.038: rejeita a 5%, não a 1%
# E3a: t.test(e3a_depois, e3a_antes, paired = TRUE, alternative = "less")   # pareado, cauda esquerda
# E3b: t.test(e3b_A, e3b_B)                                                  # Welch bicaudal
# E4: chisq.test(e4_obs)                              # p uniforme é o default; qui2 = 0.4, gl 3, não rejeita
