---
materias: [estatistica-2]
semestre: 2026.2
data: 2026-08-21
tipo: resumo
tema: Fechamento de qui-quadrado - exercício em Excel e R, anúncio do quiz
status: completo
contract_version: 1
tags: [resumo]
---

# Resumo — Qui-quadrado na prática (Excel + R) e quiz

## QUIZ TERÇA 25/08 (na aula, 11h)

- ~1 hora, 10 questões, sai quando terminar.
- Ferramenta livre: R, Excel ou na mão.
- Cobra INTERPRETAÇÃO, não só a conta (é o que ele vem reforçando).
- Referência do calendar: "1ª Provinha (ref. Classes 2 a 6)".
- Dica explícita do professor: organizar bem os dados pra não perder questão por erro operacional.

| Item | O que é |
|---|---|
| [[Teste qui-quadrado de aderencia]] | Distribuição observada desvia do esperado? H0: segue a esperada; gl = k − 1 |
| [[Teste qui-quadrado de independencia]] | Categorias de uma variável direcionam as da outra? H0: independentes; gl = (R − 1)(C − 1); tabela de contingência |
| [[Frequencia esperada]] | E = (total linha × total coluna) / total geral; totais NÃO contam como categoria |
| Estatística | Soma de (O − E)²/E: "quanto a tabela inteira desvia do esperado" |
| Decisão | Estatística vs crítico OU p-valor vs alfa (equivalentes) |

## Números do exercício da aula

```
Tabela 3×4 → gl = (3−1)(4−1) = 6
χ² calculado = 31
p-valor ≈ 1,9 × 10⁻⁵  → rejeita H0
χ² crítico (5%, 6 gl) = 12,59
```

## Excel

<pre>
Esperado: =total_linha * total_coluna / total_geral   (travar referências com $ antes de arrastar)
Desvios:  =(O − E)^2 / E   célula a célula → SOMA = χ² calculado
</pre>

## R

<pre>
m <- matrix(c(valores), nrow = 3, byrow = TRUE)   # só valores, sem totais; 3×4
chisq.test(m)                                     # estatística + gl + p-valor de uma vez
qchisq(0.95, 6)                                   # crítico 12,59 — CUIDADO: default é cauda ESQUERDA
</pre>

- 0,95 pela esquerda = 5% pela direita. Botar 0,05 sem ajustar a cauda dá o valor do lado errado.
- Nomear linhas/colunas é opcional (boa prática, não requisito).

## Pegadinhas / pontos de prova

- Se a questão pede o crítico, não responder o calculado (e vice-versa).
- Totais da tabela não entram na matriz nem na contagem de categorias.
- gl de independência vem da TABELA (R−1)(C−1), não do número de células.
- Erro operacional (dado digitado errado, célula destravada) perde questão: conferir a matriz antes de rodar.

## Pra fixar

- [[Teste qui-quadrado de aderencia]]
- [[Teste qui-quadrado de independencia]]
- [[Frequencia esperada]]
- [[Graus de liberdade]]
- [[Valor-p]] · [[Valor critico]]
- [[Teste de hipotese]]
