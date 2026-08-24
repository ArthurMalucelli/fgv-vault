---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# astype

## Definição

Método do [[Pandas]] que converte o tipo (dtype) de uma coluna inteira de uma vez. Sem o astype, operações entre tipos incompatíveis quebram (ex: somar string com número).

## Fórmula / aplicação

```python
df["id"] = df["id"].astype(str)        # número → string
df["preco"] = df["preco"].astype(float) # string → float
df["idade"] = df["idade"].astype(int)   # float → int
```

Caso clássico: concatenar prefixo numa coluna de números.

```python
"C" + df["id"]                  # ERRO: id é número
"C" + df["id"].astype(str)      # ok
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
- [[str accessor]]
