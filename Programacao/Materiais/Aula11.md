---
materia: Programacao
aula: 11
tema: Condicionais (if, elif, else, indentação)
quiz: 2026-05-05
---

# Aula 11: Condicionais (if, elif, else)

Aula sobre estruturas de decisão. Aqui MORA O DRAGÃO da indentação. Tema super provável de cair em "qual o output" do quiz.

## Conceitos centrais

| Conceito | O que é |
|---|---|
| `if` | Executa bloco SE condição True |
| `else` | Bloco que executa se if falhar |
| `elif` | "else if" — testa nova condição se a anterior falhou |
| Indentação | 4 espaços (ou 1 tab). DEFINE QUEM ESTÁ DENTRO do bloco |
| `and` | Operador lógico E (todas verdadeiras) |
| `or` | Operador lógico OU (uma verdadeira basta) |
| Encadeamento | `5 <= x < 6` é equivalente a `5 <= x and x < 6` |

## Sintaxe

```python
if condicao:
    # executado se True
elif outra_condicao:
    # executado se a anterior False E essa True
else:
    # executado se todas anteriores False
```

A condição pode ser qualquer coisa que retorne `True`/`False`:
- Comparação: `a > 10`, `nome == 'João'`
- Operador `in`: `'a' in lista`
- Booleano direto: `True`, `False`
- Combinação com `and`/`or`/`not`

## Exemplos canônicos

### Estrutura simples

```python
a = 10
if a > 10:
    print('o numero é maior do que 10')
    print('o numero é', a)
else:
    print('o numero é menor ou igual a 10')
    print('o numero é', a)
```
Output (com `a = 10`):
```
o numero é menor ou igual a 10
o numero é 10
```

### Com elif (3 caminhos)

```python
BRA = 1
ARG = 2

if BRA > ARG:
    print("Brazil wins")
elif ARG > BRA:
    print("Argentine wins")
else:
    print("We got a draw!")
```
Output: `Argentine wins`

### Sistema de notas com 3 status

```python
nota_final = 4.9

if nota_final >= 6:
    status = 'aprovado'
elif nota_final >= 5 and nota_final < 6:
    status = 'reaval'
else:
    status = 'reprovado'
```
Output: `status = 'reprovado'`

Nota: `nota_final >= 5 and nota_final < 6` pode ser escrito como `5 <= nota_final < 6` (encadeamento de comparação, jeito mais Pythonic).

### Condição composta com `and`

```python
nota_final = 9
media_semestral = 7

if nota_final >= 6:
    status = 'aprovado'
elif (5 <= nota_final < 6) and media_semestral >= 6:
    status = 'reaval'
else:
    status = 'reprovado'
```
Output: `status = 'aprovado'` (entrou no primeiro if, nem testou o elif)

## A pegadinha da indentação (CAI MUITO)

### Código A (correto)
```python
senha = input("Senha: ")

if senha == "123":
    print("Acesso permitido")
    print("Bem-vindo ao sistema")
```
Comportamento: as duas linhas SÓ imprimem se senha for "123". Caso contrário, NADA imprime.

### Código B (mesma cara, comportamento diferente)
```python
senha = input("Senha: ")

if senha == "123":
    print("Acesso permitido")
print("Bem-vindo ao sistema")
```
Comportamento: "Acesso permitido" só se senha for "123", mas "Bem-vindo ao sistema" SEMPRE imprime (está fora do if).

**Regra:** o que está indentado pertence ao bloco do `if`. O que volta pro nível anterior está FORA do if e roda independente.

### Quiz típico
> Se senha = "errado", qual o output do código B?

Resposta: só `Bem-vindo ao sistema`. O if não rodou (False), mas a última linha está FORA dele.

## Operadores lógicos

| Operador | Resultado |
|---|---|
| `True and True` | `True` |
| `True and False` | `False` |
| `False and qualquer` | `False` |
| `True or False` | `True` |
| `False or False` | `False` |
| `True or qualquer` | `True` |
| `not True` | `False` |
| `not False` | `True` |

### Curto-circuito (sutil mas importante)

`A and B`: se A é False, NEM AVALIA B. Útil quando B pode dar erro:
```python
if x != 0 and 10 / x > 2:   # se x = 0, não tenta dividir
    ...
```

`A or B`: se A é True, NEM AVALIA B.

## Pegadinhas pro quiz

**1. Indentação inconsistente quebra**
- Misturar tab e espaço dentro do mesmo bloco é IndentationError.
- O Python EXIGE que linhas no mesmo nível tenham mesma indentação.

**2. Atribuição vs comparação na condição (um igual vs dois iguais)**
- `if a = 5:` é SyntaxError (atribuição não retorna nada).
- `if a == 5:` é o teste correto.

**3. `elif` só é testado se anteriores foram False**
- Se cair no primeiro `if`, NENHUM `elif` é testado.
- Se nota_final = 9 e o 1º if é `nota_final >= 6`, entra ali. O elif nem é avaliado.

**4. Encadeamento `5 <= x < 6` é Pythonic**
- Equivalente a `(5 <= x) and (x < 6)`.
- Mas `5 <= x <= 6` é diferente de `5 <= x < 6` (incluir ou não o 6).

**5. `else` não tem condição**
- `else nota >= 7:` é SyntaxError.
- O `else` é o "tudo o que sobrou".

**6. Bug comum no exemplo de estoque**
```python
estoque = 5
venda = int(input(...))
if venda <= estoque:
    estoque = estoque - quantidade   # ERRO: 'quantidade' não foi definida!
    print("Venda realizada")
else:
    print("Estoque insuficiente")
```
A aula tinha esse bug pra ensinar: deveria ser `estoque - venda`. Cuidado com nomes de variáveis no quiz.

**7. String comparada lexicograficamente**
- `'abc' < 'abd'` → `True` (compara caractere por caractere via tabela ASCII/Unicode)
- `'A' < 'a'` → `True` (maiúsculas têm código menor)
- `'10' < '9'` → `True` (compara como string, não como número!)

**8. Booleanos são "tipo numérico" no fundo**
- `True == 1` → `True`
- `False == 0` → `True`
- `True + True` → `2`
- Mas isso é detalhe avançado. Foca no comportamento de fluxo.

## Pra fixar

- `if/elif/else`, indentação obrigatória, dois pontos no fim
- Dois iguais testam, um igual atribui
- `and`, `or`, `not` (e curto-circuito)
- Bloco do if é definido pela indentação. Sair da indentação = sair do bloco
- Encadeamento: `5 <= x < 6` funciona em Python
- Só PRIMEIRO bloco verdadeiro executa em if/elif/elif/else
