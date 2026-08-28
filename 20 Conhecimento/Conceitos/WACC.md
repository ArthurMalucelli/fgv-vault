---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, financas-corporativas]
---

# WACC (Weighted Average Cost of Capital)

## Definição

Custo médio ponderado do capital de uma empresa. Mistura custo do capital próprio (acionistas) e custo da dívida (credores), ponderados pela participação de cada um na estrutura de capital. É a taxa de desconto usada em modelos de [[DDM]]/DCF quando se considera estrutura de capital completa.

// preencher detalhes específicos no curso de Finanças Corporativas (futuro)

## Fórmula / aplicação

<pre>
WACC = (E/V) × R_E  +  (D/V) × R_D × (1 − T)
</pre>

Onde:
- `E` = capital próprio (equity)
- `D` = dívida (debt)
- `V` = E + D (valor total da firma)
- `R_E` = custo do capital próprio (estimado via [[CAPM]])
- `R_D` = custo da dívida (taxa que a empresa paga pra captar)
- `T` = alíquota de IR (a dívida tem benefício fiscal porque juros são dedutíveis)

**Lógica**: empresa capta dinheiro de duas formas, com custos diferentes. O custo médio "para a empresa" é a média ponderada.

**Uso**: taxa de desconto em valuation de empresa **toda** (firma). Pra valuation só do equity, usa-se R_E direto.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[CAPM]]
- [[DDM]]
- [[Valuation]]
