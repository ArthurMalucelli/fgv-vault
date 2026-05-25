---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# agg

## Definição

Método do [[Pandas]] usado depois de [[groupby]] para aplicar **múltiplas funções de agregação** ou aplicar **funções diferentes por coluna**, em uma única operação.

Mais flexível que chamar uma função única como `.sum()` ou `.mean()`.

## Fórmula / aplicação

```python
# Função diferente por coluna (dicionário)
df.groupby("método").agg({
    "quantidade": "sum",
    "preço": "mean"
})

# Múltiplas funções para a mesma coluna (lista)
df.groupby("método").agg({
    "quantidade": ["mean", "min", "max"],
    "preço": "median"
})
```

Sintaxe: dicionário com `nome_da_coluna: função_de_agregação`. Para múltiplas funções na mesma coluna, valor é lista.

Funções aceitas como string: `"sum"`, `"mean"`, `"median"`, `"count"`, `"max"`, `"min"`, `"std"`, entre outras. Também aceita função Python passada por referência (sem string).

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
