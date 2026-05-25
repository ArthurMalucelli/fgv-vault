---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, renda-variavel, multiplos]
---

# Price/Earnings (P/E)

## Definição

Múltiplo de [[Valuation]] que expressa quantas vezes o preço da ação é em relação aos earnings (lucro) por ação da empresa. Método alternativo ao [[DDM]], usado especialmente pra comparar empresas dentro do mesmo setor ou pra estimar valor de empresas que ainda não são listadas.

## Fórmula / aplicação

<pre>
P/E = Preço da ação / Earnings por ação
</pre>

**Exemplo da aula**: se uma empresa tem P/E de 10x e paga dividendo de R$ 10, o preço da ação seria R$ 100.

**Uso típico (extrapolação por múltiplos)**:
1. Pega uma empresa comparável já listada
2. Calcula o P/E dessa empresa
3. Aplica esse múltiplo aos earnings da empresa que você quer avaliar

```
Preço estimado = P/E médio do setor × Earnings da empresa-alvo
```

**Quando usar**:
- Empresa não tem histórico de dividendos
- Pré-IPO (não tem preço de mercado)
- Análise rápida de relativo (essa empresa está cara ou barata em relação às pares?)

**Limitação**: ignora qualidade dos earnings, taxa de crescimento, risco. Por isso é complementar ao DDM, não substituto.

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
- [[Dividend Yield]]
