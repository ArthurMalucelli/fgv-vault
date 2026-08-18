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
