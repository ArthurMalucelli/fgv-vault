---
materia: MatemáticaAplicada
data: 2026-08-20
tema: Introdução a derivadas
tags: [resumo]
---

# Resumo — Introdução a derivadas

| Item | O que é |
|---|---|
| [[Taxa de Variação Média]] | Δf/Δx entre dois pontos (x variou 2, f variou 24 → média 12); geometricamente, coeficiente angular da reta secante |
| Reta secante | Liga dois pontos do gráfico; sua inclinação é a variação média |
| [[Reta Tangente]] | Limite da secante quando os pontos se juntam; "abraça" a curva no ponto; equação y − f(a) = m(x − a) |
| [[Derivada]] f'(a) | Coeficiente angular da tangente em a = taxa de variação INSTANTÂNEA (radar: fotos cada vez mais próximas → velocidade) |
| Derivada como função | Trocando a por x, f'(x) dá a inclinação da tangente em CADA ponto |
| Análise de sinal em limites laterais | Testar valores dos dois lados (−7,1 e −6,99): sinal do numerador ÷ sinal do denominador decide se vai a +∞ ou −∞ |

## Fórmulas

```
f'(a) = lim(x→a) [f(x) − f(a)] / (x − a)
f'(a) = lim(h→0) [f(a+h) − f(a)] / h        (formas equivalentes)
Reta tangente em a:  y − f(a) = f'(a)·(x − a)
```

Receita do exemplo (f(x) = x² + 1, a = 2, f(2) = 5):

```
[(2+h)² + 1 − 5]/h  →  expandir  →  cancelar constantes  →  fatorar h  →  cortar  →  h = 0
```

## Pegadinhas / pontos de prova

- Derivada só existe se o limite dá igual pelos DOIS lados; aproximar por 2⁺ ou 2⁻ não muda o resultado quando ela existe.
- Denominador → 0 com numerador ≠ 0 NÃO é 0/0: é análise de sinal e limite infinito (assíntota vertical), outro procedimento.
- Não esquecer o f(a) na equação da tangente: a reta passa por (a, f(a)), não pela origem.
- No cálculo pela definição, o h SEMPRE corta; se não cortou, tem erro de expansão.

## Próxima aula

- Regras de diferenciação; derivadas de exponenciais e logarítmicas (ter 25/08, já na description do evento no calendar).

## Pra fixar

- [[Derivada]]
- [[Reta Tangente]]
- [[Taxa de Variação Média]]
- [[Limites Laterais]] · [[Assíntota Vertical]]
