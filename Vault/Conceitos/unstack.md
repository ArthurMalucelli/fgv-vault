---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# unstack

## Definição

Método do [[Pandas]] que pivota um nível do índice multi-nível para virar coluna. Útil depois de um [[groupby]] com múltiplos critérios para visualizar o resultado em formato de matriz (uma das chaves como linha, outra como coluna).

## Fórmula / aplicação

```python
# Default: pega o último nível do índice (-1) e joga pra coluna
df.groupby(["método", "região"])["quantidade"].sum().unstack()

# Especificar nível por posição
df.groupby([...])[...].sum().unstack(0)

# Especificar nível por nome
df.groupby([...])[...].sum().unstack("método")
```

Antes do `unstack`, o resultado de `groupby` vinha vertical (uma linha por combinação). Depois do `unstack`, vira matriz. Células sem correspondência preenchem com NaN.

Operação inversa: `stack()` (pega coluna e empilha como índice).

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
- [[pivot_table]]
