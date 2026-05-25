# Métodos vs Funções em Python

Cheatsheet de referência. Diferença sintática, lista de built-ins, lista de métodos por tipo.

## Diferença mecânica

```python
funcao(coisa)        # FUNÇÃO: nome primeiro, recebe coisa como argumento
coisa.metodo()       # MÉTODO: objeto primeiro, ponto, nome do método
```

Método tecnicamente é função, só que vive dentro de um tipo (`str`, `list`, `dict`, etc) e recebe o objeto automaticamente como primeiro argumento (o famoso `self`).

## Funções built-in (genéricas, funcionam em vários tipos)

Sempre disponíveis, sem importar nada.

| Função | O que faz | Exemplo |
|---|---|---|
| `len(x)` | tamanho | `len("abc")` = 3 |
| `type(x)` | tipo do objeto | `type(42)` = `int` |
| `print(x)` | imprime | `print("oi")` |
| `input(msg)` | lê do teclado | `nome = input("nome? ")` |
| `int(x)` | converte pra int | `int("42")` = 42 |
| `float(x)` | converte pra float | `float("3.14")` = 3.14 |
| `str(x)` | converte pra string | `str(42)` = `"42"` |
| `list(x)` | converte pra lista | `list("abc")` = `['a','b','c']` |
| `tuple(x)` | converte pra tuple | `tuple([1,2])` = `(1,2)` |
| `set(x)` | converte pra set | `set([1,1,2])` = `{1,2}` |
| `dict(x)` | converte pra dict | `dict([("a",1)])` = `{"a":1}` |
| `bool(x)` | converte pra booleano | `bool(0)` = `False` |
| `abs(x)` | valor absoluto | `abs(-5)` = 5 |
| `round(x, n)` | arredonda | `round(3.14, 1)` = 3.1 |
| `min(x)` / `max(x)` | menor/maior | `max([1,5,2])` = 5 |
| `sum(x)` | soma | `sum([1,2,3])` = 6 |
| `sorted(x)` | ordena (devolve nova) | `sorted([3,1,2])` = `[1,2,3]` |
| `reversed(x)` | inverte | `list(reversed([1,2]))` = `[2,1]` |
| `range(n)` | sequência de números | `list(range(3))` = `[0,1,2]` |
| `enumerate(x)` | adiciona índice | `list(enumerate("ab"))` = `[(0,"a"),(1,"b")]` |
| `zip(a, b)` | combina paralelamente | `list(zip([1,2],["a","b"]))` = `[(1,"a"),(2,"b")]` |
| `map(f, x)` | aplica função em cada elemento | `list(map(str, [1,2]))` = `["1","2"]` |
| `filter(f, x)` | filtra elementos | `list(filter(lambda x: x>1, [1,2,3]))` = `[2,3]` |
| `any(x)` / `all(x)` | algum/todos True | `any([0,1,0])` = `True` |
| `isinstance(x, t)` | x é do tipo t? | `isinstance(42, int)` = `True` |
| `help(x)` | mostra documentação | `help(str.find)` |
| `dir(x)` | lista métodos/atributos | `dir("")` |

## Métodos de `str` (string)

```python
"texto".metodo()
```

| Método | O que faz | Exemplo |
|---|---|---|
| `.upper()` | maiúsculas | `"abc".upper()` = `"ABC"` |
| `.lower()` | minúsculas | `"ABC".lower()` = `"abc"` |
| `.title()` | Primeira Maiúscula | `"abc def".title()` = `"Abc Def"` |
| `.capitalize()` | Só primeira | `"abc def".capitalize()` = `"Abc def"` |
| `.strip()` | tira espaços das pontas | `"  oi  ".strip()` = `"oi"` |
| `.lstrip()` / `.rstrip()` | tira só esquerda/direita | |
| `.replace(a, b)` | troca a por b | `"abc".replace("b","X")` = `"aXc"` |
| `.split(sep)` | divide em lista | `"a,b,c".split(",")` = `["a","b","c"]` |
| `.join(lista)` | une lista | `",".join(["a","b"])` = `"a,b"` |
| `.find(sub)` | índice (ou -1) | `"abc".find("b")` = 1 |
| `.index(sub)` | índice (ou erro) | `"abc".index("b")` = 1 |
| `.count(sub)` | quantas vezes aparece | `"aba".count("a")` = 2 |
| `.startswith(s)` | começa com? | `"abc".startswith("a")` = `True` |
| `.endswith(s)` | termina com? | `"abc".endswith("c")` = `True` |
| `.isalpha()` | só letras? | `"abc".isalpha()` = `True` |
| `.isdigit()` | só dígitos? | `"123".isdigit()` = `True` |
| `.isalnum()` | letras + dígitos? | `"abc123".isalnum()` = `True` |
| `.isspace()` | só espaços? | `"   ".isspace()` = `True` |
| `.format(...)` | formatação | `"{} anos".format(20)` |
| `.zfill(n)` | preenche com zeros | `"5".zfill(3)` = `"005"` |

## Métodos de `list`

```python
lista.metodo()
```

| Método | O que faz | Exemplo |
|---|---|---|
| `.append(x)` | adiciona no fim | `[1,2].append(3)` resulta em `[1,2,3]` |
| `.extend(iter)` | adiciona vários | `[1].extend([2,3])` resulta em `[1,2,3]` |
| `.insert(i, x)` | insere em posição | `[1,3].insert(1, 2)` resulta em `[1,2,3]` |
| `.remove(x)` | remove primeira ocorrência | `[1,2,1].remove(1)` resulta em `[2,1]` |
| `.pop(i)` | remove e devolve (default: último) | `[1,2,3].pop()` = `3` |
| `.clear()` | esvazia | `[1,2].clear()` resulta em `[]` |
| `.index(x)` | índice do elemento | `[1,2,3].index(2)` = 1 |
| `.count(x)` | quantas vezes aparece | `[1,2,1].count(1)` = 2 |
| `.sort()` | ordena no lugar | `[3,1,2].sort()` resulta em `[1,2,3]` |
| `.reverse()` | inverte no lugar | `[1,2,3].reverse()` resulta em `[3,2,1]` |
| `.copy()` | cópia rasa | `[1,2].copy()` |

## Métodos de `dict`

```python
d = {"a": 1, "b": 2}
```

| Método | O que faz | Exemplo |
|---|---|---|
| `.keys()` | lista chaves | `d.keys()` = `dict_keys(['a','b'])` |
| `.values()` | lista valores | `d.values()` = `dict_values([1,2])` |
| `.items()` | lista pares | `d.items()` = `[('a',1),('b',2)]` |
| `.get(k, default)` | pega valor (sem erro) | `d.get("z", 0)` = 0 |
| `.pop(k)` | remove e devolve | `d.pop("a")` = 1 |
| `.update(outro)` | mescla outro dict | `d.update({"c":3})` |
| `.setdefault(k, v)` | pega ou seta | `d.setdefault("z", 99)` |
| `.clear()` | esvazia | `d.clear()` resulta em `{}` |

## Métodos de `set`

```python
s = {1, 2, 3}
```

| Método | O que faz | Exemplo |
|---|---|---|
| `.add(x)` | adiciona | `{1,2}.add(3)` |
| `.remove(x)` | remove (erro se não existe) | |
| `.discard(x)` | remove (sem erro) | |
| `.union(outro)` | união | `{1,2} \| {2,3}` = `{1,2,3}` |
| `.intersection(o)` | interseção | `{1,2} & {2,3}` = `{2}` |
| `.difference(o)` | diferença | `{1,2} - {2,3}` = `{1}` |

## Como descobrir métodos de qualquer objeto

```python
dir("")              # lista todos os métodos de string
dir([])              # lista todos os métodos de lista
help(str.find)       # mostra documentação do método
"abc".find.__doc__   # mesmo, mais curto
```

No Jupyter/IPython, digita `"abc".` e aperta Tab que ele mostra o autocomplete.

## Regra mnemônica

- **Função solta**: operação **genérica**, faz sentido em vários tipos. Ex: `len`, `type`, `print`, `sum`, `max`. Sintaxe: `funcao(x)`.
- **Método**: operação **específica** daquele tipo. Ex: `.append` (só lista), `.upper` (só string). Sintaxe: `x.metodo()`.

## Erros comuns

```python
upper("abc")        # NameError: função 'upper' não existe solta
"abc".len()         # AttributeError: string não tem método len
len("abc")          # CERTO: função built-in
"abc".upper()       # CERTO: método de string
```
