---
tipo: conceito
materias: [Estatistica]
tags: [conceito, probabilidade, distribuicao]
---

# Distribuição normal

## Definição

[[Variavel aleatoria continua]] mais importante da estatística. Forma de sino, simétrica em torno da média. Notação: X ~ N(μ, σ²). Atenção: notação usa **variância** σ², mas Excel usa **desvio padrão** σ.

## Padronização (Z-score)

Qualquer Normal vira Normal padrão (Z) por:

```
Z = (X - μ) / σ      Z ~ N(0, 1)
```

Z mede em quantos desvios padrão um valor está da média. Usado pra:
- Comparar valores de distribuições com escalas diferentes
- Identificar outliers (|z| ≥ 3 é critério clássico)
- Localizar quantis usando tabela Z padrão

## Excel

```
P(X ≤ a)   = DIST.NORM.N(a; μ; σ; 1)
P(X > a)   = 1 - DIST.NORM.N(a; μ; σ; 1)
P(a<X<b)   = DIST.NORM.N(b; μ; σ; 1) - DIST.NORM.N(a; μ; σ; 1)

INV.NORM.N(p_acumulada; μ; σ)        ← passa acumulada, NÃO cauda
INV.NORMP.N(0,975) = 1,96            ← Z padrão
```

**Pegadinha 1:** Excel usa σ, NÃO σ². Se enunciado dá variância, tira raiz.

**Pegadinha 2:** INV.NORM.N pede acumulada. Se P(X > k) = 5%, passa 0,95, não 0,05.

## Z críticos (decora)

| Cauda α | z |
|---|---|
| 0,10 | 1,282 |
| 0,05 | 1,645 |
| 0,025 | 1,96 |
| 0,01 | 2,326 |
| 0,005 | 2,576 |

## Regra empírica

Se X ~ Normal:
- μ ± 1σ contém ≈ 68% da distribuição
- μ ± 2σ contém ≈ 95%
- μ ± 3σ contém ≈ 99,7%

## Aproximação Binomial → Normal

Pra n grande e p não próximo de 0 ou 1 (regra prática: n·p > 5 e n·(1-p) > 5):

```
[[Distribuicao binomial|Bin(n,p)]] ≈ N(np, np(1-p))
```

## Conceitos relacionados

- [[Variavel aleatoria continua]]
- [[Funcao densidade de probabilidade]]
- [[Distribuicao binomial]] (aproximação)
- [[Variancia e desvio padrao]]
