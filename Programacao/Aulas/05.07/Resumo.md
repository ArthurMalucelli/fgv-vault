---
materia: Programacao
data: 2026-05-07
tema: Manipulação de dados com Pandas — DataFrames, seleção, ordenação e filtros lógicos
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Pandas]] | Biblioteca Python pra dados tabulares (planilhas). Importada como `pd` |
| [[DataFrame]] | Objeto tabular com várias linhas e várias colunas. Análogo a uma planilha |
| Index (índice) | Identificador de **linha**. Pode ser número, string, qualquer coisa |
| Column (coluna) | Identificador de **coluna**. Em Pandas pode ser qualquer tipo, diferente do Excel |
| [[Wesley McKinney]] | Criador do Pandas. Veio do mercado financeiro, queria ferramenta melhor que R/Matlab |
| [[Fatiamento lógico]] | Selecionar linhas com base em condição booleana. `df[df["col"] > 5]` |
| [[loc]] | Acessório para indexar por **nome** (label). `df.loc[linhas, colunas]` |
| [[iloc]] | Acessório para indexar por **posição numérica**. `df.iloc[0:5, 1:3]` |
| Série temporal | DataFrame onde o índice é instante no tempo (eletiva) |

## Importação

```python
import pandas as pd
```

`pd` é apelido convencional. Pandas não está no Python padrão, sempre precisa importar.

## Seleção

```python
df["gold"]                      # uma coluna (string)
df[["gold", "silver", "bronze"]] # várias colunas (lista de strings)
df.loc[1]                       # uma linha por nome
df.loc[[1, 2, 3]]               # várias linhas por nome
df.loc[[linhas], [colunas]]     # forma canônica: fragmento
df.iloc[0]                      # linha 0 (posição)
df.iloc[0:5, 1:3]               # slice por posição
```

Regra: **colchete duplo** `df[[...]]` quando o que está dentro é uma lista (várias colunas/linhas). Colchete externo = "fatie o df", interno = "esta é uma lista".

## Ordenação

```python
df.sort_values("gold")                      # ascending=True (default)
df.sort_values("gold", ascending=False)     # do maior pro menor
df = df.sort_values("gold")                 # PERSISTE no objeto
```

**Pegadinha**: `sort_values` sozinho **não altera o objeto**. Só exibe o resultado ordenado. Pra persistir, reatribui (`df = df.sort_values(...)`).

Diferente do `.sort()` da lista, que altera in-place. Em Pandas é `sort_values`, não `sort`.

## Fatiamento lógico

```python
df[df["gold"] == 0]                              # filtra
df[~(df["gold"] > 10)]                           # NOT
df[(df["gold"] > 5) & (df["gold"] < 10)]         # AND
df[(df["gold"] > 10) | (df["silver"] < 10)]      # OR
df[df["country"] == "Russia"]                    # busca por valor
```

Operadores lógicos em Pandas (não usar `and`/`or`/`not` do Python puro):

| Operação | Símbolo |
|---|---|
| AND | `&` |
| OR | `\|` (barra vertical) |
| NOT | `~` (til) |

Cada condição precisa estar entre **parênteses** quando combinada com `&` ou `|`.

## Funções de consolidação

```python
df["gold"].sum()           # 307
df["gold"].mean()          # 3.56
df["gold"].std()           # desvio padrão
df["gold"].value_counts()  # contagem por valor (27 zeros, 21 uns, ...)
df["gold"].unique()        # valores distintos
df["gold"].nunique()       # quantos valores distintos
df.head()                  # primeiras 5 (ou df.head(n))
df.tail()                  # últimas 5 (ou df.tail(n))
```

Encadeamento (lê esquerda pra direita):

```python
df[df["gold"] > 30]["gold"].sum()
# 1. df[df["gold"] > 30]  → linhas com gold > 30
# 2. ["gold"]             → só a coluna gold
# 3. .sum()               → soma → 245
```

## Pegadinhas / pontos de prova

- **Pandas vai cair na prova final** (professor falou explicitamente).
- `sort_values` por default não altera o objeto. Para alterar, **reatribui** (`df = df.sort_values(...)`).
- Operadores lógicos em Pandas são `&`, `|`, `~`, **não** `and`, `or`, `not`. Esquecer isso é erro comum.
- Cada condição num filtro composto precisa estar **entre parênteses**: `df[(cond1) & (cond2)]`.
- `df[...]` interpreta o conteúdo como **coluna** por default. Para fatiar **linha**, precisa do `.loc` ou `.iloc`.
- `.loc` usa **nome** (label), `.iloc` usa **posição numérica**.
- Colchete duplo `df[["a", "b"]]`: o externo fatia, o interno é lista. Não são colchetes redundantes.
- Acima de 50 linhas, o Jupyter omite o meio do DataFrame (mostra só primeiras e últimas 5). É só display, os dados estão lá.
- Distribuição assimétrica (mediana 1, média 3.56) é típica de medalhas, renda, salário. Muitos com pouco, poucos com muito.

## Pra fixar

- [[Pandas]]
- [[DataFrame]]
- [[Fatiamento lógico]]
- [[loc]]
- [[iloc]]
- [[Wesley McKinney]]

## Próxima aula

Seguir com Pandas (provavelmente mais funções, agrupamento, `groupby`, etc., dado que conteúdo vai cair na prova final).
