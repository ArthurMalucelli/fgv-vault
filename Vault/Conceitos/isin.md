---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao, pandas]
---

# isin

## Definição

Método do [[Pandas]] que testa, pra cada linha, se o valor da coluna está dentro de uma lista. Devolve uma máscara booleana, usada pra filtrar o [[DataFrame]].

## Fórmula / aplicação

```python
# filtra linhas cujo Produto é GASOLINA OU ETANOL, numa tacada:
ge = df[df["Produto"].isin(["GASOLINA", "ETANOL"])]
```

Equivale a `(df["Produto"]=="GASOLINA") | (df["Produto"]=="ETANOL")`, mas mais limpo quando são vários valores.

## Pegadinha

Recebe uma **lista** (`["A","B"]`), não valores soltos. Pra negar (tudo que NÃO está na lista), usar o til na frente: `~df["col"].isin([...])`.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[loc]]
- [[DataFrame]]
- [[Condicional]]
