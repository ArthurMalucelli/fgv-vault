---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# Inner join

## Definição

Tipo de junção (`how="inner"`) usado em [[merge]]. Default. Retorna **só as linhas onde a [[Chave de juncao]] existe nos dois DataFrames**. É a intersecção entre os conjuntos de chaves.

Linhas que só existem no left ou só no right são descartadas.

## Fórmula / aplicação

```python
pd.merge(left, right, on="produto", how="inner")
```

Exemplo: `left` tem produtos A, B, C, E. `right` tem A, B, C, D.
Resultado de `inner`: **A, B, C** (E e D somem).

Comparar com [[Outer join]] (mantém todos), [[Left join]] (mantém todos do left), [[Right join]] (mantém todos do right).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[merge]]
- [[Outer join]]
- [[Left join]]
- [[Right join]]
- [[Chave de juncao]]
