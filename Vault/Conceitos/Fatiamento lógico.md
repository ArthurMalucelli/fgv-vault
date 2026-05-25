---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# Fatiamento lógico

## Definição

Técnica em [[Pandas]] de selecionar linhas de um [[DataFrame]] com base em uma condição booleana. A sintaxe parece estranha à primeira vista porque envolve dois colchetes externos: o de fora fatia o DataFrame, e dentro vai a expressão lógica.

```python
df[df["gold"] == 0]   # linhas onde gold == 0
```

## Fórmula / aplicação

Operadores lógicos em Pandas são diferentes do Python puro:

| Operação | Python puro | Pandas |
|---|---|---|
| AND | `and` | `&` |
| OR | `or` | `\|` |
| NOT | `not` | `~` |

Cada condição combinada precisa estar **entre parênteses**:

```python
df[(df["gold"] > 5) & (df["gold"] < 10)]    # AND
df[(df["gold"] > 10) | (df["silver"] < 10)] # OR
df[~(df["gold"] > 10)]                       # NOT
df[df["country"] == "Russia"]                # busca por valor
```

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
- [[loc]]
- [[iloc]]
