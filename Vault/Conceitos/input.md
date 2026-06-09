---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao]
---

# input

## Definição

Função built-in que lê uma linha digitada pelo usuário e devolve **sempre como texto (`str`)**, mesmo quando a pessoa digita um número.

## Fórmula / aplicação

```python
nome  = input("Nome: ")            # str
idade = int(input("Idade: "))      # converte pra int
preco = float(input("Preço: "))    # converte pra float
```

## Pegadinha central

O retorno é `str`. Fazer conta ou comparar com número sem converter dá `TypeError`:

```python
idade = input("Idade: ")   # "18" (texto)
if idade < 18:             # TypeError: '<' not supported between 'str' and 'int'
    ...
```

Conserto: envolver com `int()` ou `float()`. Antes de converter um inteiro vindo do usuário, validar com [[isdigit]] pra não quebrar a execução.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Funcao Python]]
- [[Condicional]]
- [[isdigit]]
