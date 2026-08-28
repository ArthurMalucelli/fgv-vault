---
materias: [estatistica-2]
semestre: 2026.2
data: 2026-08-18
tipo: resumo
tema: Qui-quadrado - fechamento da aderência e teste de independência
status: completo
contract_version: 1
tags: [resumo]
---

# Resumo — Qui-quadrado: aderência (fecho) + independência

| Item | O que é |
|---|---|
| [[Distribuicao qui-quadrado]] | Nunca negativa; valor mínimo da estatística é 0 |
| [[Teste qui-quadrado de aderencia]] | Compara distribuição observada vs esperada em UMA variável; gl = k − 1 (4 categorias → 3 gl) |
| [[Teste qui-quadrado de independencia]] | Duas variáveis categóricas em tabela de contingência; H0: as variáveis são independentes |
| [[Frequencia esperada]] (independência) | E_ij = (total da linha i × total da coluna j) / total geral |
| [[Graus de liberdade]] (independência) | (R − 1) × (C − 1); ex.: 2 linhas × 3 colunas → 1 × 2 = 2 gl |
| Decisão | Estatística > crítico (ou p-valor < alfa) → rejeita H0 |

## Fórmulas

```
χ² = Σᵢ Σⱼ (Oᵢⱼ − Eᵢⱼ)² / Eᵢⱼ        i = 1..R (linhas), j = 1..C (colunas)
E_ij = (total linha i × total coluna j) / n
gl aderência   = k − 1
gl independência = (R − 1)(C − 1)
```

Excel:

<pre>
INV.QUIQUA / INV.QUIQUA.CD  → valor crítico (entrada: alfa, gl); ex.: 5%, 2 gl → 5,99
DIST.QUIQUA.CD              → p-valor da estatística (CD = cauda direita; inglês: CHISQ.DIST.RT)
TESTE.QUIQUA                → p-valor direto dos vetores observado e esperado (CHISQ.TEST)
</pre>

## Exemplo da aula (música × sexo)

- 50 escolheram rock, proporção H/M meio a meio → esperado 25/25 por célula.
- χ² = 9,71 > crítico 5,99 (alfa 5%, 2 gl) → dentro da [[Regiao de rejeicao]] → rejeita H0 → sexo e preferência musical NÃO são independentes (há associação).
- Exercício aula 5 (crédito/débito/dinheiro: 100/60/40): χ² = 2,54 < 5,99 → não rejeita H0.

## Pegadinhas / pontos de prova

- Não rejeitar H0 ≠ provar H0: "não obtive evidência contra", nunca "provei que adere/é independente".
- gl da independência usa (R−1)(C−1), NÃO k−1: não confundir com aderência.
- H0 do teste de independência é sempre "as variáveis SÃO independentes"; rejeitar = evidência de associação.
- Excel PT vs EN: sufixo CD = RT (cauda direita); separador decimal é ponto na função.
- Nomes randomizam entre máquinas: saber a lógica, não decorar o menu.

## Pendências ditas em aula

- Exercício da aula 5 no Eclass é obrigatório (sem prazo dito); gabarito pode ter erro, professora vai revisar.
- Um exercício ficou para a próxima aula.
- R-Commander na prova: outras turmas usam; sem confirmação explícita pra essa turma.

## Pra fixar

- [[Teste qui-quadrado de independencia]]
- [[Teste qui-quadrado de aderencia]]
- [[Frequencia esperada]]
- [[Graus de liberdade]]
- [[Distribuicao qui-quadrado]]
- [[Valor-p]] · [[Valor critico]] · [[Regiao de rejeicao]]
