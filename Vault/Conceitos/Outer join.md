---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# Outer join

## Definição

Tipo de junção (`how="outer"`) usado em [[merge]]. Retorna **a união dos dois conjuntos de chaves**. Mantém todas as linhas, dos dois lados, mesmo as que não têm correspondência.

Onde a chave existe num lado mas não no outro, o Pandas preenche as colunas vazias com NaN (Not a Number, valor faltante).

## Fórmula / aplicação

```python
pd.merge(left, right, on="produto", how="outer")
```

Exemplo: `left` tem produtos A, B, C, E. `right` tem A, B, C, D.
Resultado de `outer`: **A, B, C, D, E**.

- A, B, C → têm dados dos dois lados.
- D → tem dados do right; colunas do left ficam NaN.
- E → tem dados do left; colunas do right ficam NaN.

Comparar com [[Inner join]] (só intersecção), [[Left join]], [[Right join]].

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[merge]]
- [[Inner join]]
- [[Left join]]
- [[Right join]]
- [[Chave de juncao]]
