---
materia: Programacao
aula: 12
tema: Loops (for, while, range, break, nested)
quiz: 2026-05-05
---

# Aula 12: Loops (for, while, range)

A aula mais densa do bloco. for, while, nested loops, break, range. Garantido cair no quiz.

## Conceitos centrais

| Conceito | O que é |
|---|---|
| `for` | Repete bloco para cada elemento de um iterável |
| `range(n)` | Gera números 0, 1, 2, ..., n-1 |
| `range(a, b)` | Gera números a, a+1, ..., b-1 |
| `range(a, b, passo)` | Com passo (step) |
| Iterável | Lista, string, range, qualquer coisa que dá pra percorrer |
| `while` | Repete enquanto condição True |
| `break` | Sai do loop imediatamente |
| `from time import sleep` | Pausa execução em segundos |
| Nested loop | Loop dentro de loop |

## Sintaxe `for`

```python
for variavel in iteravel:
    # bloco do loop (indentado)
```

### Variantes de `range`

| Código | Gera |
|---|---|
| `range(8)` | `0, 1, 2, 3, 4, 5, 6, 7` (8 números, COMEÇA em 0) |
| `range(0, 8)` | igual ao anterior |
| `range(1, 8)` | `1, 2, 3, 4, 5, 6, 7` (7 números, NÃO inclui 8) |
| `range(0, 20)` | `0, 1, 2, ..., 19` |
| `range(0, 101)` | `0, 1, ..., 100` |
| `range(0, 10, 2)` | `0, 2, 4, 6, 8` (passo de 2) |

**Regra crítica:** `range(a, b)` vai de `a` até `b-1`, NUNCA inclui `b`. Pra somar de 1 a 1000, use `range(1, 1001)`.

### Iterando sobre lista

```python
for x in [0, 1, 2, 3, 4, 5, 6, 7]:
    print(x)
```
Output: cada número numa linha (igual a `for x in range(8)`).

### Iterando sobre string

```python
escola = 'Fundação Getúlio Vargas'
for l in escola:
    print(l)
```
Output: cada caractere numa linha (incluindo espaços e acentos).

### Iterando sobre lista mista

```python
lista = [1, 'a', 2, -3, 10.3, 'xyz']
for elemento in lista:
    print(elemento)
```
Output:
```
1
a
2
-3
10.3
xyz
```

## `for` com `if` dentro: padrão básico

```python
for x in range(0, 20):
    if x % 4 == 0:
        print(x, "is divisible by 4.")
    else:
        print(x, "is not divisible by 4.")
```
Output: 20 linhas, alternando "is divisible" pra 0, 4, 8, 12, 16 e "is not" pros outros.

## Padrão acumulador (CAI MUITO)

```python
escola = "Fundacao Getulio Vargas"
contador_a = 0
for letra in escola:
    if letra == 'a':
        contador_a = contador_a + 1
print(contador_a)   # 4
```

Variantes:
- contar caracteres específicos
- somar elementos
- multiplicar elementos
- encontrar máximo/mínimo

### Padrão de soma

```python
s = 0
for i in range(1, 1001):
    s = s + i
print(s)   # 500500
```

Atenção ao `range(1, 1001)` (NÃO `range(1, 1000)` — esse última iria até 999).

## Loops aninhados (nested)

Loop dentro de loop. Para cada iteração do externo, o interno roda completo.

```python
naipes = ['♥', '♠', '♣', '♦']
cartas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

baralho = []
for carta in cartas:
    for naipe in naipes:
        baralho.append(carta + ' de ' + naipe)
```
Resultado: lista com 13 × 4 = 52 cartas.

### Contar vogais (nested loop com if)

```python
escola = "Fundacao Getulio Vargas"
vogais = ['a', 'e', 'i', 'o', 'u']
contador_vogais = 0
for letra in escola:
    for vogal in vogais:
        if letra == vogal:
            contador_vogais = contador_vogais + 1
print(contador_vogais)   # 10
```

Forma alternativa mais Pythonic:
```python
for letra in escola:
    if letra in vogais:
        contador_vogais += 1
```

## `while`

Continua repetindo ENQUANTO a condição for True.

```python
x = 0
while x < 6:
    print("I like number: " + str(x))
    x = x + 1
```
Output:
```
I like number: 0
I like number: 1
I like number: 2
I like number: 3
I like number: 4
I like number: 5
```

CRUCIAL: precisa atualizar a variável dentro do loop. Esquecer `x = x + 1` causa LOOP INFINITO.

### Padrão de validação

```python
myPass = ""
while myPass != "password":
    myPass = input("Type password and enter")
print("You are a LOTR fan...!")
```
Continua pedindo até digitar "password".

## `break`

Sai do loop imediatamente, mesmo se a condição ainda seria True.

```python
import random
for rodada in range(0, 20):
    j = random.randint(1, 6)
    print('jogo:', j)
    if j == 6:
        print('o numero aleatorio gerado foi', j, 'então o loop foi quebrado')
        break
```
Para no momento que tirar 6, mesmo que ainda faltem rodadas.

## Pegadinhas pro quiz

**1. `range(n)` NUNCA inclui `n`**
- `range(5)` → `0, 1, 2, 3, 4` (5 valores, terminando em 4)
- `range(1, 5)` → `1, 2, 3, 4` (4 valores)
- Pra ir de 1 a 1000 inclusive: `range(1, 1001)`.

**2. Indentação dentro do for muda comportamento**

CÓDIGO A:
```python
for x in range(5):
    print("Valor de x:")
    print(x)
```
Output: 5 pares "Valor de x:" + número, em cada iteração.

CÓDIGO B:
```python
for x in range(5):
    print("Valor de x:")
print(x)
```
Output: 5 vezes "Valor de x:", e UMA VEZ no fim, o último valor de `x` (que é `4`). O segundo print está FORA do for.

**3. Loop infinito no while**
- Se você esquece de atualizar a variável de controle, while roda pra sempre.
- `while True:` é loop infinito intencional (precisa de `break` lá dentro).

**4. `break` sai apenas do loop ATUAL**
- Em loop aninhado, `break` no interno NÃO sai do externo.

**5. Ordem de iteração em nested loops**
- Outer roda primeiro. Pra cada outer, inner roda do começo ao fim.
- Outer = `cartas` (13), inner = `naipes` (4): você gera A♥, A♠, A♣, A♦, depois 2♥, 2♠, ...

**6. Variável do loop sobrevive depois**
- Depois de `for x in range(5):`, `x` ainda existe e tem o último valor (`4`).
- Por isso o Código B do exemplo de indentação imprime `4`.

**7. `range(0)` é vazio, loop não roda**
- `for x in range(0): print(x)` não imprime nada.
- Mesma coisa pra `range(5, 5)` (vazio).

**8. `range` não é lista**
- Em Python 3, `range(5)` é um objeto range, não a lista `[0,1,2,3,4]`.
- Mas você pode iterar e tratar como tal pro quiz.

**9. Acumulador tem que ser inicializado FORA do loop**
- `soma = 0` fora, depois `soma = soma + x` dentro.
- Se você puser `soma = 0` dentro, ele zera a cada iteração.

**10. Diferença entre `s += 1` e `s = s + 1`**
- São equivalentes.
- Quiz pode misturar os dois.

## Aplicação típica do quiz: "qual a soma de 1 até 1000?"

```python
s = 0
for i in range(1, 1001):
    s = s + i
print(s)   # 500500
```

Alternativas comuns no multiple choice:
- `s = 0`, `range(1, 1001)`, `s = s + i` ✓ correto
- `s = 0`, `range(0, 1001)`, `s = s + i` ✓ também correto (soma com 0 não muda)
- `s = 0`, `range(1, 1000)`, `s = s + i` ✗ ERRADO (vai até 999, não 1000)
- `s = 1`, `range(1, 1001)`, `s = s + i` ✗ ERRADO (s começa em 1, soma um 1 a mais)

## Pra fixar

- `range(a, b)` exclui `b`
- Indentação define o que está dentro do loop
- Acumuladores: inicializa fora, atualiza dentro
- `break` sai do loop atual
- `while` precisa atualizar variável de controle ou loopa pra sempre
- Variável do for sobrevive após o loop com último valor
- Nested loop: outer × inner iterações totais
- Strings e listas são iteráveis
