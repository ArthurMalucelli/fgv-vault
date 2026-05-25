---
materia: Programacao
aula: 8
tema: input(), conversão de tipos, concatenação, primeiro if/else
quiz: 2026-05-05
---

# Aula 8: input(), conversão de tipos, concatenação

Aula que explica como o Python lida com texto vs número, e introduz pela primeira vez `if/else`.

## Conceitos centrais

| Conceito | O que é |
|---|---|
| `input()` | Pede texto do usuário, SEMPRE retorna string (mesmo se digitar número) |
| `int(x)` | Converte para inteiro |
| `float(x)` | Converte para decimal |
| `str(x)` | Converte para texto |
| Concatenação `+` em string | Cola dois textos: `"Hello " + "World"` → `"Hello World"` |
| Concatenação `+` em número | Soma: `5 + 10` → `15` |
| Erro de tipo misto | `"Hello " + 5` quebra (TypeError), precisa `"Hello " + str(5)` |
| `if/else` | Estrutura de decisão (introdução, vai a fundo na Aula 11) |
| Palavras reservadas | Nomes que o Python já usa: `if`, `else`, `for`, `while`, `lambda`, `in`, `def`, `return`... |

## Sintaxe e código → output

| Código | Output |
|---|---|
| `print(123)` | `123` (número) |
| `print('123')` | `123` (texto, indistinguível visualmente do número) |
| `n = input('digite:'); print('voce digitou', n)` | imprime o que o usuário digitou, como string |
| `n = input(...); int(n) + 4` | converte e soma. Se `n='5'`, vira `9` |
| `'Hello ' + 'World'` | `'Hello World'` |
| `'Hello ' + 5` | **TypeError**: can only concatenate str to str |
| `'Hello ' + str(5)` | `'Hello 5'` |
| `4 != 4` | `False` |
| `'Hello' == 'hello'` | `False` (case-sensitive) |

## Conversão de tipos: regra de ouro

`input()` SEMPRE devolve string. Se você quer fazer conta, converte primeiro.

```python
n = input('digite um numero:')   # n = '5' (string!)
n = int(n)                       # n = 5 (int)
n = n + 1                        # n = 6
print(n)
```

Se esquecer o `int()`:
```python
n = input('digite:')   # n = '5'
n + 1                  # TypeError: can only concatenate str (not "int") to str
```

## Pegadinhas pro quiz

**1. `input()` SEMPRE retorna string**
- Se o quiz pergunta o tipo de `n` depois de `n = input("...")`, é sempre `str`, mesmo que o usuário digite "5".
- Pra fazer conta com input, converte ANTES com `int()` ou `float()`.

**2. `+` muda comportamento conforme o tipo**
- `5 + 10` = `15` (soma)
- `'5' + '10'` = `'510'` (concatenação, junta os textos)
- `5 + '10'` = TypeError
- Se as duas alternativas são `15` e `510`, olha os tipos.

**3. `int(5.7)` trunca, não arredonda**
- `int(5.7)` = `5` (corta a parte decimal, não arredonda pra cima)
- `int(5.99)` = `5`
- `int(-5.7)` = `-5` (trunca em direção ao zero)
- Pra arredondar use `round()`, não `int()`.

**4. `float(10)` vira `10.0`**
- Convertendo int pra float adiciona `.0` na exibição.

**5. Aspas `"` e `'` são iguais**
- `"abc"` é o mesmo que `'abc'`. Não muda comportamento, só estilo.
- Importa quando tem aspas dentro: `"it's"` vs `'it\'s'`.

**6. Palavras reservadas não podem ser nomes de variável**
- `if = 5` é erro de sintaxe.
- Lista mencionada na aula: `if`, `else`, `lambda`, `for`, `while`, `in`, `def`, `return`...
- Mas `meu_numero = 10` funciona (não é palavra reservada).

## Exercícios típicos da Aula 8 (formato do quiz)

**1. Multiplicação simples:** imprimir `2020 * 2019` (= 4_058_380)
**2. Atribuir a variável:** `x = 2020 * 2019`
**3. Triplo do input:** ler número, converter, multiplicar por 3
**4. Média ponderada:** `media = P1*0.30 + P2*0.35 + PF*0.35`
**5. PF necessária pra passar:** `PF = (6 - P1*0.30 - P2*0.35) / 0.35`
**6. Divisão da pizza:** valor com taxa de 10% dividido entre N pessoas, motorista não paga taxa

## Pra fixar

- `input()` → string SEMPRE
- `int()` trunca, `round()` arredonda
- `+` em string concatena, em número soma
- `str(x)` antes de juntar texto com número
- Palavras reservadas: `if, else, for, while, in, def, return, lambda`
