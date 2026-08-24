---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# DataFrame

## Definição

Estrutura de dados central do [[Pandas]]. Objeto tabular com várias linhas e várias colunas, análogo a uma planilha. Composto por três partes:

- **Index** (índice): identificador de linha. Pode ser número, string, qualquer tipo.
- **Columns** (colunas): identificador de coluna. Igualmente flexível.
- **Dados**: a parte interna.

Diferente do Excel, onde linha é sempre número e coluna é sempre letra, em DataFrame ambos podem ser qualquer tipo.

## Fórmula / aplicação

```python
df["gold"]                  # seleciona coluna
df[["gold", "silver"]]      # várias colunas
df.loc[1]                   # linha por nome
df.iloc[0]                  # linha por posição
df[df["gold"] > 5]          # fatiamento lógico
df.sort_values("gold")      # ordenação (não altera objeto)
df["gold"].sum()            # agregação
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
- [[loc]]
- [[iloc]]
- [[Fatiamento lógico]]
