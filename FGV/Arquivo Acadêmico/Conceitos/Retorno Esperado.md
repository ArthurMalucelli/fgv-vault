---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, renda-variavel]
---

# Retorno Esperado

## Definição

Retorno percentual que o investidor espera realizar ao manter uma ação por um período. É composto por duas parcelas: o [[Dividend Yield]] (parcela do dividendo) e o [[Ganho de Capital]] (variação de preço). Em termos de [[DDM]], é a taxa de desconto que iguala o valor presente do fluxo de dividendos esperados ao preço da ação.

## Fórmula / aplicação

Para um período:

<pre>
R_E = (Div₁ + P₁ − P₀) / P₀
    = Div₁/P₀  +  (P₁ − P₀)/P₀
    = Dividend Yield + Capital Gain
</pre>

**Decomposição diz algo sobre o risco**: se a maior parte do retorno esperado vem de capital gain (preço futuro), a ação é mais arriscada, porque preço futuro é mais volátil que dividendo. Empresas tendem a dar [[Guidance]] estável de dividendo, então projetar dividendo é mais confiável que projetar preço.

**Como taxa de desconto**: nessa disciplina, R_E = [[Taxa Livre de Risco]] + [[Premio de Risco]]. Em finanças corporativas, será estimado via [[CAPM]] (custo de capital próprio) ou [[WACC]] (custo médio do capital, com dívida).

**Comparação entre empresas**: comparar retorno esperado de duas empresas só faz sentido se elas têm risco equivalente. Senão, é preciso ajustar pelo risco.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Dividend Yield]]
- [[Ganho de Capital]]
- [[DDM]]
- [[CAPM]]
- [[WACC]]
