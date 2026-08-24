---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# str.replace

## Definição

Método do [[str accessor]] que substitui todas as ocorrências de um substring por outro em cada string da coluna. Retorna uma nova coluna.

## Fórmula / aplicação

```python
df["gender"].str.replace("F", "FM")
# F vira FM, M continua M
```

Encadeamento (pipeline). Como retorna do mesmo tipo, dá pra encadear:

```python
df["gender"].str.replace("F", "FM").str.replace("M", "MM")
# F → FM, M → MM (simultâneo)
```

Interpretação: o resultado do primeiro `str.replace` é input do segundo. O primeiro só mexe no F, o segundo pega esse resultado e mexe no M.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[str accessor]]
- [[str.contains]]
- [[Pandas]]
