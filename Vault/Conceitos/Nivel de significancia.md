---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Nivel de significancia

## Definição

Alfa (α): a probabilidade máxima de [[Erro Tipo I]] (rejeitar H0 sendo ela verdadeira) que quem decide aceita correr. Escolhido antes de olhar os dados; default 5%. É o número contra o qual o [[Valor-p]] é comparado, e o que define o [[Valor critico]]. Complementar do [[Nivel de Confianca]]: confiança 95% equivale a α = 5%.

## Fórmula / aplicação

<pre>
alfa = P(rejeitar H0 | H0 verdadeira)

Regra de decisão:  valor-p < alfa  →  rejeita H0
Unicaudal: todo o alfa numa cauda (z crítico 1,645 a 5%)
Bicaudal:  alfa/2 em cada cauda   (z crítico 1,96 a 5%)

Mudar alfa pode mudar a decisão com a mesma amostra:
SLA 48h: valor-p 0,028 → rejeita a 5%, não rejeita a 1%.
</pre>

Alfa não é a probabilidade de H0 ser falsa. Baixar alfa (1%) reduz o risco de Erro Tipo I e aumenta o de [[Erro Tipo II]] com n fixo.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Nivel de significancia]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Erro Tipo I]]
- [[Erro Tipo II]]
- [[Valor-p]]
- [[Valor critico]]
- [[Nivel de Confianca]]
