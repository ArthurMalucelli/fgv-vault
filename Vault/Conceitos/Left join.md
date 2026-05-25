---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# Left join

## Definição

Tipo de junção (`how="left"`) usado em [[merge]]. Retorna **todas as linhas do DataFrame left, mais o que casar do right**. Chaves que só existem no right são descartadas.

Onde a chave do left não tem correspondência no right, as colunas do right ficam preenchidas com NaN.

## Fórmula / aplicação

```python
pd.merge(left, right, on="produto", how="left")
```

Exemplo: `left` tem produtos A, B, C, E. `right` tem A, B, C, D.
Resultado de `left`: **A, B, C, E** (D some).

- A, B, C → têm dados dos dois lados.
- E → vem do left; colunas do right ficam NaN.

Comparar com [[Right join]] (espelho), [[Inner join]] (só intersecção), [[Outer join]] (união).

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
- [[Outer join]]
- [[Right join]]
- [[Chave de juncao]]
