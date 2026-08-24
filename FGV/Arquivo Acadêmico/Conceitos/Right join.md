---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# Right join

## Definição

Tipo de junção (`how="right"`) usado em [[merge]]. Retorna **todas as linhas do DataFrame right, mais o que casar do left**. Chaves que só existem no left são descartadas.

Onde a chave do right não tem correspondência no left, as colunas do left ficam preenchidas com NaN. Espelho do [[Left join]].

## Fórmula / aplicação

```python
pd.merge(left, right, on="produto", how="right")
```

Exemplo: `left` tem produtos A, B, C, E. `right` tem A, B, C, D.
Resultado de `right`: **A, B, C, D** (E some).

- A, B, C → têm dados dos dois lados.
- D → vem do right; colunas do left ficam NaN.

Na prática quase sempre se usa [[Left join]] em vez de `right` (mais natural manter o left como referência). Comparar com [[Inner join]], [[Outer join]].

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
- [[Left join]]
- [[Chave de juncao]]
