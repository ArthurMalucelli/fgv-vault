# Quiz Python, Erros pra Revisar

Tracker dos quizzes que errei. Organizado por tópico.

---

## TIPOS

### QE.T9, divisão `/`

**Pergunta:** Qual o tipo do resultado de `7 / 2`?

- Sua: `int`
- Correta: `float`

**Por quê:** `/` em Python 3 SEMPRE retorna `float`, mesmo divisão exata.

```python
7 / 2  # 3.5 (float)
6 / 2  # 3.0 (float, mesmo sendo divisão exata)
```

Pra resultado inteiro usa `//` (floor division).

---

### QE.T10, `bool` de coleção vazia

**Pergunta:** Qual o resultado de `bool([])`?

- Sua: `None`
- Correta: `False`

**Por quê:** Lista vazia `[]` é avaliada como `False` em contexto booleano. Lista com QUALQUER elemento é `True`, mesmo `[0]`, `[None]`, `[""]`. O que importa é se TEM elemento, não o conteúdo.

```python
bool([])        # False
bool([0])       # True
bool([None])    # True
bool([""])      # True
```

Mesma lógica vale pra `""`, `{}`, `()`, `0`, `None` (todos falsy).

---

### QE.T13, `int()` de string com decimal

**Pergunta:** Qual o resultado de `int('3.5')`?

- Sua: `3`
- Correta: `Erro (ValueError)`

**Por quê:** `int()` não aceita string com ponto decimal, gera `ValueError`. `int()` espera string com SÓ dígitos.

```python
int('3.5')          # ValueError
int(float('3.5'))   # 3 (passa por float antes)
int(3.5)            # 3 (de float direto, OK)
```

Regra: `int(str)` exige dígitos puros. `int(float)` trunca normal.

---

## COMPARAÇÕES

### QE.C04, `False == 0`

**Pergunta:** Qual é o resultado de `False == 0`?

- Sua: `Erro`
- Correta: `True`

**Por quê:** `False` equivale a `0` numericamente porque `bool` é subclasse de `int`.

```python
False == 0      # True
True == 1       # True
int(False)      # 0
int(True)       # 1
```

Consequência prática: `True + True == 2`, `sum([True, False, True]) == 2`.

---

### QE.C017, comparação de listas

**Pergunta:** Qual é o resultado de `[1, 2, 3] < [1, 2, 4]`?

- Sua: `Erro`
- Correta: `True`

**Por quê:** Listas comparam LEXICOGRAFICAMENTE, elemento por elemento, igual dicionário/palavra.

```
[1, 2, 3] vs [1, 2, 4]:
  1 == 1  ✓ (segue)
  2 == 2  ✓ (segue)
  3 < 4   ✓ → True
```

Mesma lógica de comparar palavras: "abc" < "abd" porque c < d.

Funciona pra qualquer sequência ordenável (listas, tuplas, strings).

---

### QE.T14, set equality ignora ordem

**Pergunta:** Qual o resultado de `{1, 2} == {2, 1}`?

- Sua: `False`
- Correta: `True`

**Por quê:** `set` é coleção SEM ordem. Igualdade compara só conteúdo. Diferente de lista/tuple, onde ordem importa.

```python
{1, 2} == {2, 1}   # True   (set, ordem irrelevante)
[1, 2] == [2, 1]   # False  (lista, ordem importa)
(1, 2) == (2, 1)   # False  (tuple, ordem importa)
{"a":1,"b":2} == {"b":2,"a":1}  # True (dict, chaves são set)
```

Detalhe: set não é indexável (`s[0]` dá erro), e a ordem que aparece no `print` não é confiável.

---

### QE.T15, indexação devolve ELEMENTO, não container

**Pergunta:** Qual o tipo de `[1, 2, 3][0]`?

- Sua: `list`
- Correta: `int`

**Por quê:** `[i]` extrai o elemento do índice i. O resultado é o tipo do CONTEÚDO, não do container.

```python
type([1, 2, 3])      # list
type([1, 2, 3][0])   # int  ← extraiu o 1
type("abc"[0])       # str  ← extraiu o "a"
type({"a": 1}["a"])  # int  ← extraiu o 1
```

Regra: indexação sempre devolve o elemento, nunca o container. Pra saber o tipo da expressão, mentaliza qual valor sai no final.

---

### QE.T16, isalnum significa "alfanumérico"

**Pergunta:** Qual o resultado de `'abc123'.isalnum()`?

- Sua: `False`
- Correta: `True`

**Por quê:** `isalnum` = "is **al**pha**num**eric" = letras OU dígitos. Não é "is all numbers".

```python
"abc123".isalnum()    # True   (letras + dígitos)
"abc 123".isalnum()   # False  (espaço quebra)
"abc!".isalnum()      # False  (símbolo quebra)
"".isalnum()          # False  (vazia também)
```

Família `is*()` em string:
- `isalpha()` só letras
- `isdigit()` só dígitos
- `isalnum()` letras OU dígitos (sem espaço/símbolo)
- `isspace()` só espaço/tab/newline
- `isupper()` `islower()` caso

Todos exigem string não vazia E todos os caracteres passando no teste.

---

### QE.T17, `not ''` é True (string vazia é falsy)

**Pergunta:** Qual a saída?

```python
if not '':
    print('A')
else:
    print('B')
```

- Sua: `B`
- Correta: `A`

**Por quê:** Cadeia de duas inversões. `''` é falsy → `bool('') == False` → `not '' == True` → entra no if.

```python
''           # string vazia, FALSY
bool('')     # False
not ''       # True (inverteu)
if True:     # ENTRA → print('A')
```

**Tudo que é vazio/zero/None é falsy:**

```python
bool('')   bool([])   bool({})   bool(())   # todos False
bool(0)    bool(0.0)  bool(None)             # todos False
```

E com `not`, tudo isso vira `True`.

**Padrão idiomático:** `if not x:` lê como "se x está vazio/zero/ausente". Mais limpo que `if x == "":` ou `if len(x) == 0:`.

```python
if not nome:      # se vazio
    pedir_de_novo()

if not lista:     # se vazia
    return
```

---

### QE.T18, `//` com negativo arredonda pra BAIXO, não trunca

**Pergunta:** Qual o resultado de `-7 // 2`?

- Correta: `-4` (não `-3`)

**Por quê:** `//` é **floor division**, arredonda em direção ao infinito negativo. Não é truncamento (arredondar pra zero).

```python
-7 / 2     # -3.5
-7 // 2    # -4    floor(-3.5) puxa PRA ESQUERDA
int(-7/2)  # -3    trunc(-3.5) puxa PRO ZERO
```

Pra positivo dá no mesmo (floor e trunc apontam pra mesma direção):

```python
7 // 2     # 3   = floor(3.5) = trunc(3.5)
```

Mas com negativo divergem:

| Operação | Cálculo | Resultado |
|---|---|---|
| `7 // 2` | floor(3.5) | `3` |
| `-7 // 2` | floor(-3.5) | `-4` |
| `7 // -2` | floor(-3.5) | `-4` |
| `-7 // -2` | floor(3.5) | `3` |

Regra: sinal do resultado segue sinal do divisor.

**Pra truncar (arredondar pra zero):** `int(a/b)` ou `math.trunc(a/b)`.

**Conexão com `%`:** Python garante `(a // b) * b + (a % b) == a`. Por isso `-7 % 2 = 1` (não `-1`):

```python
-7 // 2  =  -4
-7 % 2   =   1     porque -4*2 + 1 = -7
```

Em C/Java/JS o `//` trunca. Python escolheu floor pra que o módulo sempre tenha sinal do divisor (mais útil em relógio, hashing, módulo matemático).

---

## STRINGS

### QE.S01, find devolve índice da PRIMEIRA ocorrência

**Pergunta:** Qual o resultado de `'abcabc'.find('b')`?

- Correta: `1`

**Por quê:** `find()` varre da esquerda pra direita, devolve índice do primeiro hit. Para no primeiro, ignora os próximos.

```python
"abcabc".find("b")      # 1   (primeiro)
"abcabc".rfind("b")     # 4   (último, varre direita pra esquerda)
"abcabc".find("z")      # -1  (não achou, NÃO dá erro)
"abcabc".find("b", 2)   # 4   (começa do índice 2)
"abcabc".count("b")     # 2   (quantas vezes)
"b" in "abcabc"         # True (só sim/não)
```

Cuidado com `.index()` vs `.find()`: `.index()` LEVANTA ERRO se não acha, `.find()` devolve `-1`. Usa `find` quando "não achar" é resultado válido, `index` quando deveria ser bug.

---

## BUGS COMUNS

### Bug B01: `qtd + 1` em vez de `qtd += 1`

```python
qtd = 0
for letra in "aaa":
    if letra == "a":
        qtd + 1     # ERRADO: calcula 0+1=1, joga fora
print(qtd)          # 0 (não mudou nada)
```

`qtd + 1` é EXPRESSÃO, não atribuição. Calcula e joga fora. Pra modificar, precisa atribuir:

```python
qtd = qtd + 1   # forma longa
qtd += 1        # forma curta (equivalente)
```

Análogo: digitar 0+1 numa calculadora, ver o 1 e desligar sem anotar. A conta foi feita, o resultado sumiu.

### Bug B02: `type.letra` em vez de `type(letra)`

```python
type.letra       # ERRADO: AttributeError
type(letra)      # CERTO: chama função
```

`type` é função, chama com parênteses `()`. Ponto `.` é pra atributo de objeto. Não dá pra trocar.

### Bug B03: `letra = [0]` cria LISTA, não pega índice 0

```python
letra = [0]      # cria lista [0] com um elemento
letra = lista[0] # pega elemento 0 de "lista"
```

`[0]` sozinho do lado direito do `=` é lista literal. Só vira indexação quando vem DEPOIS de algo: `lista[0]`.

### Bug B04: `lista = lista.append(x)` mata a lista

Mesma família do B01 (`qtd + 1`). `.append()` modifica a lista no lugar E retorna `None`. Quando você atribui o resultado de volta, sobrescreve a lista por `None`.

```python
pares = []
for n in [1, 2, 3, 4]:
    if n % 2 == 0:
        pares = pares.append(n)   # ARMADILHA
```

Trace:
- n=2: `pares.append(2)` modifica pares pra `[2]`, retorna `None` → `pares = None`
- n=4: tenta `None.append(4)` → **AttributeError**

Forma certa, só chama, NÃO atribui:

```python
pares.append(n)        # certo
```

**Regra geral:** métodos que modificam in-place retornam `None`. Não atribua o resultado deles. Vale pra:

| Método | O que faz | NÃO faça |
|---|---|---|
| `.append(x)` | adiciona no fim | `l = l.append(x)` |
| `.extend(iter)` | adiciona vários | `l = l.extend(iter)` |
| `.insert(i, x)` | insere em posição | `l = l.insert(...)` |
| `.remove(x)` | remove primeira ocorrência | `l = l.remove(x)` |
| `.sort()` | ordena | `l = l.sort()` |
| `.reverse()` | inverte | `l = l.reverse()` |
| `.clear()` | esvazia | `l = l.clear()` |
| `dict.update(...)` | mescla | `d = d.update(...)` |

**Mnemônica:** se o método **modifica** o objeto, ele NÃO devolve o objeto. Devolve `None` de propósito, justamente pra você não cair na armadilha.

Versão "funcional" (não modifica, devolve nova) pode ser atribuída:

```python
l = sorted(l)              # sorted() devolve nova, OK atribuir
l = list(reversed(l))      # reversed() devolve iterador, OK
nova = l + [x]             # concatenação devolve nova, OK
```

---

## CONCEITOS BASE

### Iteração `for c in string`

```python
for c in "abc":
    print(c)
# a
# b
# c
```

`for <nome> in <iterável>:` cria variável temporária que recebe cada elemento por vez. Nome é arbitrário (pode ser `c`, `letra`, `x`, `banana`). Convenção: `c` pra char, `i` pra índice, `x` genérico.

String é iterável (caractere a caractere). Lista, tuple, dict, set, range também.

### Estruturas básicas: o que é cada literal

| Sintaxe | Tipo | Nota |
|---|---|---|
| `{1, 2}` | `set` | sem ordem, sem duplicata |
| `{"a": 1}` | `dict` | par chave: valor |
| `{}` | **`dict` vazio**, NÃO set | pra set vazio: `set()` |
| `[1, 2]` | `list` | ordenada, mutável |
| `[]` | `list` vazia | |
| `(1, 2)` | `tuple` | ordenada, IMUTÁVEL |
| `()` | `tuple` vazia | |
| `(1,)` | `tuple` com 1 elem | vírgula obrigatória |
| `(1)` | `int` | parênteses só agrupam |

### Métodos vs Funções (resumo)

```python
funcao(coisa)        # FUNÇÃO: nome primeiro
coisa.metodo()       # MÉTODO: objeto primeiro, com ponto
```

Detalhes em `Cheatsheet-Metodos-vs-Funcoes.md` na mesma pasta.
