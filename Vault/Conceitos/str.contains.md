---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# str.contains

## Definição

Método do [[str accessor]] que verifica se uma coluna de strings contém um substring. Retorna uma coluna booleana (true/false por linha). Usado tipicamente como filtro lógico em [[DataFrame]].

## Fórmula / aplicação

```python
df["email"].str.contains("fgv.br")
# retorna Series booleana
```

Filtragem direta:

```python
df[df["email"].str.contains("fgv.br")]
```

Forma mais legível, variável temporária:

```python
cond = df["email"].str.contains("fgv.br")
df[cond]
```

Combinado com outras condições:

```python
cond1 = df["col"].str.contains("CDI")
cond2 = df["col"].str.contains("IMAB")
df[cond1 | cond2]    # OR
```

**Cuidado**: `contains("CDI")` casa também com `CDI 100%`, `CDI+`, etc. Para igualdade exata, usar `==` em vez de `str.contains`.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[str accessor]]
- [[str.replace]]
- [[Pandas]]
- [[Fatiamento lógico]]
