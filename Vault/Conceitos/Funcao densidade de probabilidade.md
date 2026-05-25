---
tipo: conceito
materias: [Estatistica]
tags: [conceito, probabilidade]
---

# Função densidade de probabilidade

## Definição

FDP (ou f(x), pdf em inglês). Função que descreve a distribuição de uma [[Variavel aleatoria continua]]. **f(x) não é probabilidade**, é densidade. Probabilidade é a área embaixo da curva.

## Propriedades obrigatórias

Toda FDP precisa cumprir:
- f(x) ≥ 0 para todo x
- Área total embaixo de f(x) = 1

Se a fórmula da FDP tem constante desconhecida, usa Σ áreas = 1 pra achar.

## Cálculo de probabilidade

```
P(a ≤ X ≤ b) = área embaixo da FDP entre a e b
```

Em prova FGV típica, FDP é triangular ou retangular: usa fórmula da área (base × altura, ou (b×h)/2). Quando precisa de integral, geralmente é Uniforme ou Exponencial e tem fórmula fechada.

## Diferença pra PMF

| Aspecto | PMF (discreta) | FDP (contínua) |
|---|---|---|
| f(x) representa | Probabilidade direta P(X=x) | Densidade, não probabilidade |
| P(X = c) | Pode ser positivo | Sempre zero |
| Soma/Integral total | Σ = 1 | Área = 1 |
| P(intervalo) | Σ pontos | Área embaixo da curva |

## Conceitos relacionados

- [[Variavel aleatoria continua]]
- [[Distribuicao normal]]
- [[Distribuicao uniforme continua]]
- [[Distribuicao exponencial]]
