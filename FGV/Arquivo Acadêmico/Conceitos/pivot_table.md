---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# pivot_table

## Definição

Função do [[Pandas]] que constrói uma tabela dinâmica, equivalente direto à tabela dinâmica do Excel. Alternativa ao [[groupby]] + [[unstack]], com sintaxe que mapeia 1-pra-1 aos quadrantes do Excel.

## Fórmula / aplicação

| Excel | pivot_table |
|---|---|
| rows | `index` |
| columns | `columns` |
| values | `values` |
| função | `aggfunc` |

```python
df.pivot_table(
    index="região",
    columns="método de envio",
    values="quantidade",
    aggfunc="sum",
    margins=True              # adiciona total
)
```

Funções aceitas em `aggfunc`: `"sum"`, `"mean"`, `"median"`, `"count"`, `"max"`, `"min"`, `"std"`.

`margins=True` adiciona uma linha "All" e uma coluna "All" com os totais agregados.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Pandas]]
- [[DataFrame]]
- [[groupby]]
- [[unstack]]
- [[agg]]
