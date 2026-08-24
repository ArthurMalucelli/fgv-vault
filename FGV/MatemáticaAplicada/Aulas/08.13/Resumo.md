---
materia: MatemáticaAplicada
data: 2026-08-13
tema: Limites infinitos e no infinito, termo de maior grau
tags: [resumo]
---

> [!warning] Resumo parcial
> Gravação com captação muito ruim (longos trechos viraram "Obrigado"/"Música" no Plaud). O que está aqui é o núcleo verificável da aula. Conteúdo completo do tema: slides "3 - Aula - Limites infinitos e no infinito.pdf" em `Aulas/08.18/Slides/`.

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Limites Laterais]] | Limite chegando só por um lado: pela direita (x → a⁺) ou pela esquerda (x → a⁻). Podem dar resultados diferentes |
| [[Limite Infinito]] | A função estoura pra +∞ ou −∞ perto de um ponto finito (ex.: 1/x perto de 0). Detecta com tabela de valores |
| [[Limite no Infinito]] | Comportamento de f(x) quando x → +∞ ou x → −∞ |
| [[Termo de Maior Grau]] | Em polinômio (e em quociente de polinômios), o termo de maior grau domina o limite no infinito ("regra do mais significativo"): ignora o resto |

## Fórmulas

```
lim (x→0⁺) 1/x = +∞        lim (x→0⁻) 1/x = −∞

Tabela pra (5+x)/x perto de 0
  x = 0,5  →  5,5/0,5 = 11
  x = 0,1  →  5,1/0,1 = 51         (estoura → +∞)
  x < 0    →  valores negativos    (→ −∞)

Limite no infinito de quociente de polinômios
  (6x³ + 4x² + …)/(x² + …)  ~  6x³/x²  =  6x
  x → +∞ :  6x → +∞
  x → −∞ :  6x → −∞
```

## Pegadinhas / pontos de prova

- A regra do termo de maior grau vale pra x → ±∞. Perto de um ponto (tipo x = 0), a ferramenta é outra: limites laterais e tabela de valores.
- 1/x em 0: cada lado vai pra um infinito diferente. Escreve os dois limites laterais, não um "= ∞" seco.
- Reduzir ao termo dominante não encerra a questão: ainda tem que checar o sinal por lado (6x → +∞ quando x → +∞, mas 6x → −∞ quando x → −∞).
- x negativo elevado a potência par dá positivo; potência ímpar mantém o negativo. É aí que o sinal do limite em −∞ vira.
- Quociente: reduz cima e baixo ao maior grau de cada um e simplifica (6x³/x² = 6x). Não decide só comparando graus sem olhar coeficiente e sinal.

## Pra fixar

- [[Limite (cálculo)]]
- [[Limites Laterais]]
- [[Limite Infinito]]
- [[Limite no Infinito]]
- [[Termo de Maior Grau]]
