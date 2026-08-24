---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, renda-variavel]
---

# Valor Intrínseco

## Definição

Valor "verdadeiro" de uma empresa, baseado no que ela realiza ao longo do tempo (gera resultados e paga [[Dividendos|dividendos]]), em contraste com o **valor de mercado** (preço atual da ação). É o que se busca calcular num exercício de [[Valuation]] fundamentalista via [[DDM]] ou DCF.

## Fórmula / aplicação

Não tem fórmula única. É o output do método de valuation escolhido. No DDM:

<pre>
Valor Intrínseco = P₀ = Σ Div_t / (1 + R_E)^t
</pre>

**Uso prático**: comparar valor intrínseco com valor de mercado.
- Se intrínseco > mercado → ação subvalorizada → potencial compra
- Se intrínseco < mercado → ação sobrevalorizada → potencial venda

**Cuidado**: depende fortemente das premissas (g, R_E, projeção de dividendos). Dois analistas podem chegar a valores intrínsecos muito diferentes pra mesma empresa.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Valuation]]
- [[DDM]]
- [[Dividendos]]
