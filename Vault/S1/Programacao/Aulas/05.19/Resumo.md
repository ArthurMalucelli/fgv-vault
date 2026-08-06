---
materia: Programacao
data: 2026-05-19
tema: Agrupamento e junção de dados com Pandas — merge, groupby, pivot_table, unstack, plot
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[merge]] | Junção de dois [[DataFrame]]s por chave. `pd.merge(left, right, on="col", how="inner")` |
| [[Chave de juncao]] | Coluna(s) que une o left e o right. Pode ser única ou dupla (lista) |
| [[Inner join]] | Default. Só linhas com chave nos dois lados (intersecção) |
| [[Outer join]] | União. Pega tudo, preenche faltante com NaN |
| [[Left join]] | Todas as chaves do left + casamentos do right |
| [[Right join]] | Todas as chaves do right + casamentos do left |
| [[groupby]] | Agrega DataFrame por critério. `df.groupby("col")["valor"].sum()` |
| [[agg]] | Múltiplas funções, múltiplas colunas. Aceita dict `{col: func}` |
| [[pivot_table]] | Tabela dinâmica. Mapeia 1-pra-1 com Excel (index, columns, values, aggfunc) |
| [[unstack]] | Joga nível de índice para coluna. Default pega último nível (-1) |
| `as_index=False` | Em `groupby`, faz os critérios virarem coluna normal em vez de índice |
| `margins=True` | Em `pivot_table`, adiciona linha e coluna de total |
| left / right | Em `pd.merge`, primeiro arg é left (esquerda), segundo é right (direita) |
| Series vs DataFrame | `df["col"]` retorna Series (1D); `df[["col"]]` retorna DataFrame (2D) |

## Sintaxe — merge

```python
# Chave única
pd.merge(dados, dados_complementares, on="produto", how="inner")

# Chave dupla (lista)
pd.merge(
    df_vendas,
    df_custo_envio,
    on=["método de envio", "região"],
    how="inner"
)
```

Equivalente em Excel: PROCV (e arrastar). `how="inner"` é o default.

## Tipos de junção (how)

Se `left` tem A, B, C, E e `right` tem A, B, C, D:

| how | resultado |
|---|---|
| `inner` | A, B, C (intersecção) |
| `outer` | A, B, C, D, E (união, NaN onde não casa) |
| `left` | A, B, C, E |
| `right` | A, B, C, D |

**Pegadinha**: se você junta com **menos colunas** do que deveria, o Pandas faz produto cartesiano (cria todas as combinações possíveis). Resultado fica muito maior do que o esperado.

## Sintaxe — groupby

```python
# Estrutura: groupby(critério)[seleção].agregação()
df.groupby("produto")["quantidade"].sum()

# Múltiplos critérios — lista
df.groupby(["método de envio", "região"])["quantidade"].sum()

# Múltiplas colunas no resultado — dois colchetes
df.groupby("produto")[["quantidade", "preço"]].sum()
```

**Ordem das três partes**:

1. `groupby(...)` → função (parênteses)
2. `[...]` → seleção (colchetes)
3. `.sum()` → agregação (função)

## Parênteses vs colchetes (regra de ouro)

- **Parênteses `()`** → função. Ex: `groupby("col")`, `sum()`.
- **Colchetes `[]`** → seleção. Ex: `df["col"]`, `df[["a","b"]]`.

Confundir os dois é o erro mais comum.

## agg — múltiplas funções

```python
# Uma função diferente por coluna (dict)
df.groupby("método").agg({
    "quantidade": "sum",
    "preço": "mean"
})

# Múltiplas funções para a mesma coluna (lista)
df.groupby("método").agg({
    "quantidade": ["mean", "min", "max"],
    "preço": "median"
})
```

## Filtro + groupby encadeado

```python
# Inline (uma linha)
df[df["quantidade"] > 8].groupby("produto")["quantidade"].sum()

# Multi-linha legível (envolver com parênteses)
(
    df[
        (df["método"] == "Expresso")
        & (df["quantidade"] > 8)
    ]
    .groupby("produto")["quantidade"]
    .sum()
)

# Mais legível ainda: variáveis temporárias
cond1 = df["método"] == "Expresso"
cond2 = df["quantidade"] > 8
df[cond1 & cond2].groupby("produto")["quantidade"].sum()
```

Lê da esquerda pra direita em etapas: filtro primeiro, depois agrupamento.

## unstack — pivotar índice multi-nível

```python
# Default: pega último nível (-1) e joga pra coluna
df.groupby(["método", "região"])["quantidade"].sum().unstack()

# Especificar nível
.unstack(0)              # primeiro nível por posição
.unstack("método")       # primeiro nível por nome
```

## as_index=False

Default do `groupby`: critérios viram índice. Se quer eles como coluna normal:

```python
df.groupby(["método", "região"], as_index=False)["quantidade"].sum()
```

Vira DataFrame com índice numérico (0, 1, 2...) e os critérios como colunas.

## pivot_table — equivalência com Excel

| Excel | pivot_table |
|---|---|
| rows (linhas) | `index` |
| columns | `columns` |
| values | `values` |
| função | `aggfunc` |

```python
df.pivot_table(
    index="região",
    columns="método de envio",
    values="quantidade",
    aggfunc="sum",
    margins=True              # adiciona total
)
```

Funções aceitas em `aggfunc`: `"sum"`, `"mean"`, `"median"`, `"count"`, `"max"`, `"min"`, `"std"`.

## sort_values em groupby

```python
# Ordena pelo valor (decrescente)
df.groupby("método")["quantidade"].sum().sort_values(ascending=False)
```

Default do groupby é ordem alfabética do índice. `sort_values` ordena pelo valor, mas pode "bagunçar" o multi-nível quando o índice repete (Pandas omite repetição na visualização).

## plot — visualização

```python
df.plot(
    x="data",
    y="quantidade",
    kind="line",          # line, bar, pie, hist
    marker="o",           # o, ., x, --
    title="Título",
    xlabel="data",
    ylabel="quantidade"
)

# Múltiplas séries no Y
df.plot(x="data", y=["quantidade", "preço"], kind="line")
```

## Pegadinhas / pontos de prova

- **Merge sem chave completa** faz produto cartesiano. Se a junção precisa de duas colunas, passar `on=["a", "b"]` em vez de só `on="a"`.
- **Default de `how` é `inner`**. Se quer manter linhas sem correspondência, mudar para `outer`/`left`/`right`.
- **`groupby` sem seleção** soma todas as colunas numéricas (ignora as não-numéricas silenciosamente).
- **Um colchete vs dois colchetes**: `df["col"]` → Series; `df[["col"]]` → DataFrame (1 coluna).
- **`unstack()` default é nível -1** (último). Para o primeiro nível, passar `unstack(0)` ou nome.
- **`agg` com dict** é a forma flexível: pode misturar função única e lista de funções por coluna.
- **Parênteses x colchetes**: parênteses são chamada de função; colchetes são seleção. Confundir quebra tudo.
- **Excel pivot ↔ pivot_table**: rows = index; columns = columns; values = values; função = aggfunc.
- **Multi-linha precisa de `(` `)` externos** para o Python entender que é uma expressão única.
- **`as_index=False`** transforma critérios de groupby em colunas normais.

## Pra fixar

- [[merge]]
- [[groupby]]
- [[pivot_table]]
- [[unstack]]
- [[agg]]
- [[Inner join]]
- [[Outer join]]
- [[Left join]]
- [[Right join]]
- [[Chave de juncao]]

## Próxima aula

Quinta-feira (21/05): aula de tirar dúvidas sobre o trabalho em grupo.

## Atividade de valor (trabalho em grupo)

Terça-feira **26/05/2026**, em grupo (máx. 3 alunos, pode ser 2), **sem consulta**. Formato de prova mas em grupo, diferente dos semestres anteriores. Arquivo de dados publicado até 20/05; perguntas só no dia.

**A prova final é separada**, vem depois (data ainda não dita).
