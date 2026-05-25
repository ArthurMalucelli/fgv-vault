---
tipo: conceito
materias: [Programacao, Estatistica]
tags: [conceito]
---

# Variavel categorica ordinal

## Definição

Variável cujos valores são categorias **com ordem natural** entre si. Categorias podem ser ranqueadas, mas a distância entre elas não é necessariamente uniforme.

Exemplos:
- Tamanho: pequeno < médio < grande
- Classes sociais IBGE: A > B > C > D > E (A acima de 20 SM, B entre 10 e 20, etc.)
- Escolaridade: fundamental < médio < superior < pós-graduação

Para distribuição, usar [[value_counts]]. Por ter ordem, faz sentido falar em mediana ou percentis se a codificação for numérica.

## Fórmula / aplicação

```python
df["classe_social"].value_counts()
```

Diferente de [[Variavel categorica nominal]], onde não há ordem.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Variavel categorica nominal]]
- [[value_counts]]
- [[Mediana]]
