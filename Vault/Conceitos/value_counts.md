---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# value_counts

## Definição

Método do [[Pandas]] que retorna a distribuição de valores de uma coluna. Para coluna categórica, é a forma natural de ver a contagem por categoria (equivalente ao que `mean`, `std`, `median` são para coluna numérica).

## Fórmula / aplicação

```python
df["gender"].value_counts()
# F    12
# M     8
```

Por default, ordena por contagem decrescente. Útil para inspecionar variáveis [[Variavel categorica nominal]] ou [[Variavel categorica ordinal]].

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
- [[Variavel categorica nominal]]
- [[Variavel categorica ordinal]]
