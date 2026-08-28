---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, renda-variavel]
---

# DDM (Dividend Discount Model)

## Definição

Modelo de avaliação de ação em que o preço hoje é o valor presente do fluxo esperado de [[Dividendos|dividendos]] futuros, descontado por uma taxa que reflete o risco da empresa. Também referido como DCF (Discount Cash Flow) ou [[Modelo de Gordon]] (quando há simplificação por taxa de crescimento constante).

## Fórmula / aplicação

Fórmula geral pra N períodos:

<pre>
P₀ = Σ[t=1..N] Div_t / (1+R_E)^t  +  P_N / (1+R_E)^N
</pre>

Onde:
- `Div_t` = dividendo esperado no período t
- `R_E` = retorno esperado (= [[Taxa Livre de Risco]] + [[Premio de Risco]])
- `P_N` = preço terminal no fim do horizonte projetado, calculado tipicamente via [[Perpetuidade]] → [[Valor Terminal]]

Caso de um período:

<pre>
P₀ = (Div₁ + P₁) / (1 + R_E)
</pre>

**Insight central**: em horizontes longos, o termo do preço terminal P_N/(1+R_E)^N tende a zero por causa do desconto exponencial. O preço da ação acaba dominado pelo somatório de dividendos. Por isso o foco é em projetar dividendo, não preço terminal.

A taxa R_E é o custo de capital próprio, estimado via [[CAPM]] ou via [[WACC]] (quando se considera estrutura de capital com dívida).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Modelo de Gordon]]
- [[Valor Intrinseco]]
- [[Dividend Yield]]
- [[Retorno Esperado]]
- [[Valor Terminal]]
- [[WACC]]
- [[CAPM]]
