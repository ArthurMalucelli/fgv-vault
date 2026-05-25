---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# groupby

## Definição

Função do [[Pandas]] que agrupa linhas de um [[DataFrame]] segundo um ou mais critérios e aplica função de agregação a cada grupo. Equivalente à tabela dinâmica do Excel (alternativa ao [[pivot_table]]).

A estrutura da chamada tem três partes em ordem fixa:

1. `groupby(critério)` — função (parênteses).
2. `[seleção]` — colchetes (não argumento da função).
3. `.função()` — agregação.

## Fórmula / aplicação

```python
# Critério único
df.groupby("produto")["quantidade"].sum()

# Múltiplos critérios — lista
df.groupby(["método", "região"])["quantidade"].sum()

# Múltiplas colunas no resultado — dois colchetes
df.groupby("produto")[["quantidade", "preço"]].sum()

# Sem seleção: agrega todas as colunas numéricas
df.groupby("produto").sum()
```

Por default, os critérios viram índice do resultado. Para mantê-los como coluna normal, `as_index=False`.

Para múltiplas funções por coluna, ver [[agg]].

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
- [[agg]]
- [[unstack]]
- [[pivot_table]]
