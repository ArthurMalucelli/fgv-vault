---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao]
---

# Função Python

## Definição

Bloco de código nomeado, parametrizado e reutilizável. Sintaxe `def nome(parametros):`. Pode ter `return` (devolve valor) ou não (retorna `None` implícito).

## Sintaxe

```python
def nome_da_funcao(parametro1, parametro2):
    resultado = parametro1 + parametro2
    return resultado

x = nome_da_funcao(5, 10)   # x = 15
```

## Conceitos atômicos

| Conceito | Diferença |
|---|---|
| Parâmetro | Variável definida no `def` |
| Argumento | Valor passado na chamada |
| Variável local | Existe só dentro da função |
| Função built-in | Já vem no Python: `print`, `len`, `sum`, `int`, `str`, `input` |
| Função definida | Criada com `def` pelo programador |

## Pegadinha central, print vs return

```python
def soma_print(a, b):
    print(a + b)         # imprime, mas a função retorna None

def soma_return(a, b):
    return a + b         # devolve o valor

x = soma_print(2, 3)     # imprime 5, x = None
y = soma_return(2, 3)    # nada impresso, y = 5
print(x + 1)             # TypeError: NoneType + int
print(y + 1)             # 6, ok
```

`print` mostra. `return` devolve. Quem chama uma função quer (em geral) o valor de volta, não que ela imprima.

## Diferença pra função em outras linguagens

- Python: tipagem dinâmica, parâmetros sem tipo declarado, função é objeto
- Excel: função built-in (SOMA, PROCV) usa argumentos posicionais ou nomeados, não dá pra definir custom sem VBA
- Excel já oferece SOMARPRODUTO e SE como equivalentes a funções compactas, mas perde reutilização

## Boas práticas

- Nome da função descreve o que retorna ou faz (`media`, `valida_cpf`, `calcula_juros`)
- Função pequena: faz uma coisa só
- Documentar com docstring se a lógica não é óbvia (dev sênior)

## Conceitos relacionados

- [[Loop]]
- [[Condicional]]
- [[Estruturas de Dados Python]]
