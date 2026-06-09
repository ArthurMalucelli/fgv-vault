---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao]
---

# isdigit

## Definição

Método de string que devolve `True` se **todos** os caracteres forem dígitos (0-9) e a string não for vazia. Caso contrário, `False`.

## Fórmula / aplicação

```python
"123".isdigit()    # True
"12.3".isdigit()   # False  (ponto não é dígito)
"-5".isdigit()     # False  (sinal não é dígito)
"12 ".isdigit()    # False  (espaço)
"".isdigit()       # False  (vazia)
```

## Uso na prova

Validar que o usuário digitou um inteiro **antes** de chamar `int()`, pra poder mostrar `ERRO DE ENTRADA` em vez de a execução quebrar. Casa exatamente com a regra "o peso deve ser um número inteiro, sem ponto decimal".

```python
if not peso.isdigit():
    print("ERRO DE ENTRADA")
else:
    peso = int(peso)
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Condicional]]
- [[input]]
