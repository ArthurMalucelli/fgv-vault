---
tipo: conceito
materias: [Estatistica]
tags: [conceito, probabilidade, distribuicao]
---

# Distribuição uniforme contínua

## Definição

[[Variavel aleatoria continua]] em que todos os valores num intervalo [α, β] são igualmente prováveis. Notação: X ~ U(α, β). FDP é constante no intervalo, zero fora.

## Fórmulas

```
fdp = 1/(β-α)            para α ≤ X ≤ β
P(a ≤ X ≤ b) = (b-a)/(β-α)    se a, b dentro do intervalo
E(X) = (α+β)/2           ponto médio
V(X) = (β-α)²/12
```

## Como reconhecer

Enunciado fala de "tempo de espera entre 0 e 10 minutos com igual probabilidade", "ponto escolhido ao acaso no segmento", "número aleatório entre a e b". Sinal claro: igual probabilidade em qualquer subintervalo de mesmo tamanho.

## Probabilidade por geometria

Como FDP é retangular, P é só razão de comprimentos:

```
P(a ≤ X ≤ b) = (b-a) / (β-α)
```

Não precisa integrar.

## Conceitos relacionados

- [[Variavel aleatoria continua]]
- [[Funcao densidade de probabilidade]]
- [[Distribuicao normal]]
- [[Distribuicao exponencial]]
