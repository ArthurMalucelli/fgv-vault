---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao, controle-fluxo]
---

# Condicional

## Definição

Estrutura que executa bloco de código só se uma condição for verdadeira. Em Python: `if`, `elif`, `else`.

## Sintaxe

```python
if condicao:
    # executa se condição True
elif outra_condicao:
    # executa se outra_condicao True (e if anterior False)
else:
    # executa se todas anteriores False
```

`elif` e `else` são opcionais. Pode ter só `if`.

## Operadores de comparação

| Operador | Significado |
|---|---|
| `==` | igual |
| `!=` | diferente |
| `>` | maior |
| `<` | menor |
| `>=` | maior ou igual |
| `<=` | menor ou igual |
| `in` | contém |
| `not in` | não contém |

## Operadores lógicos

| Operador | Significado | Tabela verdade |
|---|---|---|
| `and` | E (todos True) | True and True = True; resto False |
| `or` | OU (pelo menos 1 True) | False or False = False; resto True |
| `not` | inverte | not True = False |

## Aninhamento

Condicional dentro de condicional é válido. Indentação preserva ordem.

```python
if idade >= 18:
    if cnh:
        print('pode dirigir')
    else:
        print('precisa de CNH')
else:
    print('menor de idade')
```

Equivalente com `and`:

```python
if idade >= 18 and cnh:
    print('pode dirigir')
elif idade >= 18:
    print('precisa de CNH')
else:
    print('menor de idade')
```

A versão com `and` é mais legível em geral.

## Pegadinhas

- `=` é atribuição, `==` é comparação. Erro clássico
- `if 0:` é False (0, '', [], {}, None são todos falsy)
- `if x and y:` curto-circuita: se x é False, não avalia y
- Aninhamento profundo (3+ níveis) é code smell, simplificar com lógica composta ou função

## Conceitos relacionados

- [[Loop]]
- [[Funcao Python]]
