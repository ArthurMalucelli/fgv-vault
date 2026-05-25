---
tipo: conceito
materias: [Estatistica, Programacao]
tags: [conceito]
---

# Quartil

## Definição

Valores que dividem um conjunto de dados ordenados em quatro partes iguais. Cada parte contém 25% das observações.

- **Primeiro quartil (Q1, 25%)**: 25% dos dados estão abaixo desse valor.
- **Segundo quartil (Q2, 50%)**: igual à [[Mediana]]. 50% abaixo, 50% acima.
- **Terceiro quartil (Q3, 75%)**: 75% dos dados estão abaixo desse valor.

São percentis em pontos específicos. Generalização: o percentil 90 é o valor abaixo do qual estão 90% dos dados.

## Fórmula / aplicação

```python
df["col"].quantile(0.25)   # Q1
df["col"].quantile(0.50)   # mediana
df["col"].quantile(0.75)   # Q3
df["col"].describe()       # já traz Q1, Q2, Q3
```

Intervalo interquartil (IQR) = Q3 - Q1. Útil para detectar outliers.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Mediana]]
- [[describe]]
- [[Pandas]]
