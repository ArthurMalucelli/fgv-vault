---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao]
---

# split

## Definição

Método de string que quebra o texto em pedaços a cada ocorrência do separador e devolve uma **lista de strings**.

## Fórmula / aplicação

```python
"a,b,c".split(",")           # ['a', 'b', 'c']
"2025-10-02".split("-")      # ['2025', '10', '02']
"x#y#z".split("#")           # ['x', 'y', 'z']

ano, mes, dia = "2025-10-02".split("-")   # desempacota em 3 variáveis
```

Combina com [[Loop]] pra processar uma lista de registros delimitados: `for item in lista:` depois `item.split(sep)`.

## Pegadinhas

- Devolve sempre `str`. Pra somar quantidades ou valores, converter com `int()` / `float()` primeiro.
- Desempacotar (`a, b, c = ...split(...)`) exige que o número de pedaços seja igual ao número de variáveis, senão `ValueError`.
- `.split()` sem argumento quebra por qualquer espaço em branco.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Loop]]
- [[Fatiamento lógico]]
- [[Estruturas de Dados Python]]
