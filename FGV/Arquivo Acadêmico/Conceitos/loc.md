---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# loc

## Definição

Acessório do [[Pandas]] para indexar [[DataFrame]] por **nome** (label) de linha e/ou coluna. Sem o `.loc`, o que vai dentro de `df[...]` é interpretado como identificador de coluna. O `.loc` sinaliza que o que vem dentro é identificador de linha (e opcionalmente de coluna).

## Fórmula / aplicação

```python
df.loc[1]                       # uma linha por nome
df.loc[[1, 2, 3]]               # várias linhas (lista)
df.loc[[linhas], [colunas]]     # forma canônica: linhas + colunas (fragmento)
```

A forma canônica retorna um fragmento: aquelas linhas, só com aquelas colunas. Pode-se omitir a parte das colunas e passar só as linhas.

Diferente do [[iloc]], que indexa por **posição numérica**.

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
- [[iloc]]
- [[Fatiamento lógico]]
