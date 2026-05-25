---
tipo: conceito
materias: [Programacao, Estatistica]
tags: [conceito]
---

# Variavel categorica nominal

## Definição

Variável cujos valores são categorias **sem ordem** entre si. Nenhuma categoria é "maior" ou "menor" que outra.

Exemplos:
- Gênero: M/F
- UF: SP, RJ, MG, PR
- Time: Palmeiras, Corinthians, São Paulo

Para ver distribuição, usar [[value_counts]] (não faz sentido média ou mediana).

## Fórmula / aplicação

```python
df["gender"].value_counts()
```

Diferente de [[Variavel categorica ordinal]], que tem ordem.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Variavel categorica ordinal]]
- [[value_counts]]
- [[Pandas]]
