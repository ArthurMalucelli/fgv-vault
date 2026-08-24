---
tipo: conceito
materias: [Programacao, Estatistica]
tags: [conceito]
---

# describe

## Definição

Método do [[Pandas]] que retorna um resumo estatístico de uma coluna numérica ou de todo o [[DataFrame]]. Atalho para ver várias estatísticas de uma vez.

## Fórmula / aplicação

```python
df["col_numerica"].describe()
```

Retorna:

| Linha | O que é |
|---|---|
| `count` | Quantidade de valores não-nulos |
| `mean` | Média |
| `std` | Desvio padrão |
| `min` | Mínimo |
| `25%` | Primeiro [[Quartil]] |
| `50%` | [[Mediana]] (segundo quartil) |
| `75%` | Terceiro quartil |
| `max` | Máximo |

Em coluna categórica, retorna `count`, `unique`, `top`, `freq`.

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
- [[Mediana]]
- [[Quartil]]
