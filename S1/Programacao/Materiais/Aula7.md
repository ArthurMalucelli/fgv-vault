---
materia: Programacao
aula: 7
tema: Variáveis, atribuição, print e comparações iniciais
quiz: 2026-05-05
---

# Aula 7: Variáveis, atribuição, print, comparações

Primeira aula prática de Python. Conceitos fundadores que voltam em todas as outras.

## Conceitos centrais

| Conceito | O que é | Exemplo |
|---|---|---|
| Variável | Nome que aponta para um valor na memória | `a = 5` |
| Atribuição | Operador igual (NÃO é igualdade matemática) | `x = 10` |
| `print()` | Função built-in que escreve na tela | `print(a)` |
| Comparação igualdade | Pergunta "é igual?", retorna True/False | `a == 3` |
| Comparação diferença | Pergunta "é diferente?" | `a != 3` |
| Comparação ordem | Maior, menor, e variantes com igualdade | `2 < 5`, `a >= 3` |
| `NameError` | Erro quando você usa variável não definida | `z` (sem `z = ...` antes) |

## Sintaxe e código → output

| Código | Output |
|---|---|
| `a = 5; print(a)` | `5` |
| `b = 10; print(a + b)` | `15` (assume `a = 5`) |
| `c = "Hello"; print(c)` | `Hello` |
| `a + b` (sem print, célula final) | `15` (Jupyter mostra valor da última expressão) |
| `x = a + b` | (nada na tela, valor armazenado em x) |
| `x = print(a + b)` | imprime `15`, mas `x` recebe `None` |
| `2 < 5` | `True` |
| `4 > 10` | `False` |
| `a = 3; a == 3` | `True` |
| `z == 3` (sem `z` definido) | `NameError: name 'z' is not defined` |
| `a != 3` | `False` (assume `a = 3`) |

## Operadores aritméticos vistos

```
+  soma
-  subtração
*  multiplicação
**  potência (a**b é a elevado a b)
```

Exemplo do exercício do triângulo retângulo:
```python
a = 3
b = 4
c = (a**2 + b**2) ** (1/2)
```
Output: `c = 5.0` (note o `.0`, virou float por causa da divisão `1/2`)

## Pegadinhas pro quiz

**1. Atribuição vs comparação (um igual vs dois iguais)**
- `a = 3` atribui o valor 3 à variável `a`. Não retorna nada.
- `a == 3` testa se `a` é igual a 3. Retorna True ou False.
- Se a alternativa mistura os dois numa condição, é erro de sintaxe ou comportamento errado.

**2. `print()` retorna `None`**
- `x = print(a + b)` IMPRIME o valor mas atribui `None` a `x`.
- Se o quiz pergunta "qual o valor de x depois desse comando?", a resposta é `None`, não `15`.
- `print()` faz efeito (mostrar texto), `return` (na função) DEVOLVE valor. Confundir os dois é a pegadinha clássica.

**3. Última expressão da célula no Jupyter**
- No Jupyter, se a última linha é uma expressão (sem atribuição), o notebook mostra o valor automaticamente.
- `a + b` no fim de uma célula mostra `15` mesmo sem `print`.
- Mas isso é um efeito do Jupyter, NÃO do Python. Em script `.py` você precisa de `print` pra ver.

**4. Variável não definida → NameError**
- Tudo que você tenta usar precisa ter sido criado antes.
- `z == 3` sem antes ter feito `z = ...` quebra com NameError.
- O ERRO é "name 'z' is not defined", não "z is undefined".

**5. Float aparece com `.0`**
- `5/1` é `5.0`, não `5`. Divisão sempre gera float em Python 3.
- Já `5*1` é `5` (inteiro).

## Pra fixar

- Um igual define (`a = 5`), dois iguais testam (`a == 5`)
- `print()` imprime e retorna None
- Variáveis vazias dão NameError
- Toda expressão tem um tipo (int, float, str, bool)
- `True` e `False` começam com maiúscula em Python
