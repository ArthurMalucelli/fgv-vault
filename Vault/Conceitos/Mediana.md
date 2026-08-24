---
tipo: conceito
materias: [Estatistica, Programacao]
tags: [conceito]
---

# Mediana

## Definição

Valor que separa a metade superior da metade inferior de um conjunto de dados ordenado. 50% das observações estão abaixo da mediana, 50% acima. É o **segundo [[Quartil]]** (Q2, percentil 50).

Robusta a outliers. Diferente da média, não é puxada por valores extremos. Exemplo: salário mediano costuma ser muito menor que salário médio em distribuições assimétricas.

## Fórmula / aplicação

```python
df["col"].median()         # mediana de uma coluna
df["col"].quantile(0.5)    # equivalente
df["col"].describe()       # linha 50% é a mediana
```

Para coluna numérica:
- Ordena os valores.
- Se n é ímpar, mediana = valor central.
- Se n é par, mediana = média dos dois valores centrais.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Quartil]]
- [[describe]]
- [[Pandas]]
