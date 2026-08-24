---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# merge

## Definição

Função do [[Pandas]] que faz junção (join) de dois [[DataFrame]]s baseado em uma ou mais colunas em comum. Equivalente ao `PROCV` do Excel.

Toda chamada de `merge` tem três decisões: qual é o **left** (DataFrame da esquerda), qual é o **right** (da direita), qual a [[Chave de juncao]] (`on=`) e que tipo de junção (`how=`).

## Fórmula / aplicação

```python
# Chave única
pd.merge(left, right, on="produto", how="inner")

# Chave dupla (lista)
pd.merge(left, right, on=["método", "região"], how="inner")
```

Tipos de `how`: [[Inner join]] (default), [[Outer join]], [[Left join]], [[Right join]].

Pegadinha: junção com menos colunas do que deveria gera produto cartesiano (todas as combinações). DataFrame final fica maior do que o esperado.

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
- [[Chave de juncao]]
- [[Inner join]]
- [[Outer join]]
- [[Left join]]
- [[Right join]]
