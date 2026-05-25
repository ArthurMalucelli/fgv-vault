---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# iloc

## Definição

Acessório do [[Pandas]] para indexar [[DataFrame]] por **posição numérica** de linha e/ou coluna. Toda linha e coluna tem um número associado, sempre começando do zero. Da esquerda pra direita nas colunas (0, 1, 2, ...) e de cima pra baixo nas linhas.

## Fórmula / aplicação

```python
df.iloc[0]              # linha 0
df.iloc[0:5]            # linhas 0 a 4 (slicing)
df.iloc[0:5, 1:3]       # linhas 0-4, colunas 1-2 (fragmento)
```

Aceita `:` (slicing), igual lista padrão do Python.

Diferente do [[loc]], que usa **nome** (label) em vez de posição.

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
- [[loc]]
- [[Fatiamento lógico]]
