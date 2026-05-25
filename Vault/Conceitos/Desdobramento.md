---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, renda-variavel, evento-societario]
---

# Desdobramento (Split)

## Definição

Evento societário em que **1 ação é dividida em N ações novas**, com queda proporcional no preço unitário. Patrimônio do acionista e valor de mercado da empresa **não mudam**.

## Fórmula / aplicação

```
Preço pós-split = Preço pré-split / Fator
Quantidade pós-split = Quantidade pré-split × Fator
```

**Motivação**: reduzir o preço unitário pra atrair investidores menores. Lote-padrão no Brasil é 100 ações, então uma ação a R$ 40 exige R$ 4.000 mínimos.

**Exemplo**: ação a R$ 40, split 1:4. Vira 4 ações a R$ 10 cada. Acionista que tinha 1 ação passa a ter 4. Investimento mínimo cai de R$ 4.000 pra R$ 1.000.

**Contraste**: [[Grupamento]] (inplit, reverse split) faz o inverso.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Grupamento]]
- [[Bonificacao]]
