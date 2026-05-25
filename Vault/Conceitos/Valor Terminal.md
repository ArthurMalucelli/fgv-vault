---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, renda-variavel]
---

# Valor Terminal

## Definição

Valor da empresa no fim do horizonte explícito de projeção, dentro de um modelo de [[DDM]] ou DCF. Como na prática só dá pra projetar dividendo com confiança pra ~5 anos, depois disso usa-se uma simplificação pra capturar o valor de todos os fluxos restantes em um único número.

## Fórmula / aplicação

Cálculo via [[Perpetuidade]] (versão Gordon):

<pre>
P_N = Div_{N+1} / (R_E − g)
</pre>

Onde:
- `Div_{N+1}` = primeiro dividendo após o horizonte explícito
- `R_E` = custo de capital
- `g` = taxa de crescimento perpétua do dividendo

Depois traz a valor presente:

<pre>
VP do Valor Terminal = P_N / (1 + R_E)^N
</pre>

**Insight da aula**: em horizontes longos (N grande), o peso desse termo no preço da ação **cai muito** por causa do desconto exponencial. Em horizonte curto (N=1), o valor terminal domina o preço. Por isso o foco em projetar dividendo só funciona pra empresas que "nunca acabam" — N → ∞.

**Cuidado**: o valor terminal frequentemente representa **50-80%** do valor total da empresa em modelos DCF curtos (5-10 anos). Pequenas mudanças em g ou R_E mudam dramaticamente o resultado.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[DDM]]
- [[Modelo de Gordon]]
- [[Perpetuidade]]
