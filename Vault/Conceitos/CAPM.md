---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, financas-corporativas, risco]
---

# CAPM (Capital Asset Pricing Model)

## Definição

Modelo que estima o custo de capital próprio (R_E) ajustado ao risco sistemático da empresa. É o retorno que um investidor exige pra investir em uma ação, dado o risco que ela carrega em relação ao mercado.

// preencher detalhes específicos no curso de Finanças Corporativas (futuro)

## Fórmula / aplicação

<pre>
R_E = R_f + β × (R_m − R_f)
</pre>

Onde:
- `R_f` = [[Taxa Livre de Risco]] (tipicamente título do governo)
- `β` (beta) = sensibilidade da ação em relação ao mercado
  - β = 1 → ação se move junto com o mercado
  - β > 1 → ação amplifica movimentos do mercado (mais risco)
  - β < 1 → ação amortece movimentos do mercado (menos risco)
- `R_m` = retorno esperado do mercado
- `(R_m − R_f)` = [[Premio de Risco|prêmio de risco]] de mercado

**Uso**: estimar R_E em [[DDM]], dentro do [[WACC]], ou pra ajustar retornos esperados ao risco quando se compara empresas com perfis diferentes.

**Crítica importante**: assume risco sistemático como única dimensão relevante; ignora risco específico (não-diversificável só em teoria de portfólio bem diversificado).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[WACC]]
- [[Taxa Livre de Risco]]
- [[Premio de Risco]]
- [[Retorno Esperado]]
