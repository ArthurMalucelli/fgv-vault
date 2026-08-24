---
tipo: conceito
materias: [Estatistica]
tags: [conceito, probabilidade, distribuicao]
---

# Distribuição de Poisson

## Definição

[[Variavel aleatoria discreta]] que conta número de eventos num intervalo fixo de tempo ou espaço, quando os eventos ocorrem independentemente a taxa constante. Notação: X ~ Poisson(μ), onde μ é a média (também é o número esperado de eventos no intervalo).

## Fórmula

```
P(X = k) = e^(-μ) · μ^k / k!        para k = 0, 1, 2, ...
E(X) = μ
V(X) = μ
```

Característica única: **média = variância**. Útil pra checar se modelo de Poisson faz sentido pros dados.

## Como reconhecer

Enunciado fala de:
- "número de chamadas em uma hora"
- "defeitos por metro de tecido"
- "acidentes por mês"
- "clientes que chegam num intervalo"

Sinal: contagem de eventos raros em intervalo definido, taxa média conhecida.

## Excel

```
=DISTR.POISSON(k; μ; FALSO)        → P(X=k) pontual
=DISTR.POISSON(k; μ; VERDADEIRO)   → P(X≤k) acumulada
```

## Relação com [[Distribuicao binomial]]

Poisson é o limite da Binomial(n, p) quando n → ∞ e p → 0 mantendo n·p = μ constante. Aproximação prática: pra n grande e p pequeno, Bin(n,p) ≈ Poisson(np). Útil quando n é tão grande que C(n,k) fica impraticável.

## Relação com [[Distribuicao exponencial]]

Se contagem segue Poisson com taxa λ, **tempo entre eventos** segue Exponencial com média 1/λ.

## Conceitos relacionados

- [[Variavel aleatoria discreta]]
- [[Distribuicao binomial]] (aproximação para n grande, p pequeno)
- [[Distribuicao exponencial]] (tempo entre eventos)
