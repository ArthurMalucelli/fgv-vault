---
tipo: conceito
materias: [Programacao]
tags: [conceito, pandas]
---

# Chave de juncao

## Definição

Coluna (ou combinação de colunas) usada para alinhar dois [[DataFrame]]s em uma operação de [[merge]]. Em inglês, *key*. É o que une o left e o right: para cada valor da chave que aparece nos dois lados, o Pandas casa as linhas correspondentes.

Pode ser **única** (uma coluna) ou **dupla / múltipla** (lista de colunas que precisam casar simultaneamente).

## Fórmula / aplicação

```python
# Chave única
pd.merge(left, right, on="produto", how="inner")

# Chave dupla
pd.merge(left, right, on=["método", "região"], how="inner")
```

Em chave múltipla, a junção exige que **todas** as colunas listadas em `on` casem ao mesmo tempo. Se você omitir alguma das colunas que deveria ser parte da chave, o Pandas gera o produto cartesiano (todas as combinações possíveis), e o DataFrame final fica artificialmente inflado.

Em Excel, equivale à coluna usada como referência no PROCV (ou ao critério múltiplo do PROCX / ÍNDICE+CORRESP).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[merge]]
- [[Inner join]]
- [[Outer join]]
- [[Left join]]
- [[Right join]]
