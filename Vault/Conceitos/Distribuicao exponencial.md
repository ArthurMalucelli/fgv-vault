---
tipo: conceito
materias: [Estatistica]
tags: [conceito, probabilidade, distribuicao]
---

# Distribuição exponencial

## Definição

[[Variavel aleatoria continua]] que modela tempo até o próximo evento em processo de Poisson (chegadas, falhas, decaimentos). Notação: X ~ Exp(μ), onde μ é a média. Suporte X ≥ 0.

## Fórmulas

```
f(x) = (1/μ) · e^(-x/μ)        para x ≥ 0
P(X > k) = e^(-k/μ)
P(X ≤ k) = 1 - e^(-k/μ)
E(X) = μ
V(X) = μ²
```

DP = E(X). Característica única: média igual ao desvio padrão.

## Como reconhecer

Enunciado fala de "tempo até a próxima chamada", "tempo entre falhas", "tempo de vida de componente sem desgaste cumulativo". Sinal: tempo entre eventos independentes que ocorrem a taxa constante.

## Propriedade característica: falta de memória

```
P(X > s+t | X > s) = P(X > t)
```

Já esperou s minutos e o evento não ocorreu? A probabilidade de esperar mais t minutos é a mesma de quem chegou agora. Sem memória do tempo já passado.

## Relação com Poisson

- Se eventos chegam segundo [[Distribuicao de Poisson]] com taxa λ por unidade de tempo, o tempo entre eventos consecutivos é Exp(1/λ)
- Média da exponencial = 1/taxa de chegada

## Conceitos relacionados

- [[Variavel aleatoria continua]]
- [[Distribuicao de Poisson]]
- [[Funcao densidade de probabilidade]]
