---
materia: Programacao
aula: 9
tema: Tipos básicos (revisão), strings, listas
quiz: 2026-05-05
---

# Aula 9: Tipos básicos, strings, listas

Aula DUPLA (dois notebooks): manipulação de dados básica + listas. Provavelmente a aula com maior densidade de conteúdo do bloco 7-14. Tudo daqui cai com peso no quiz.

## Parte A: tipos básicos e operadores

### Os 4 tipos vistos

| Tipo | Exemplo | `type()` retorna |
|---|---|---|
| `int` (inteiro) | `10`, `-5`, `0` | `<class 'int'>` |
| `float` (decimal) | `-5.5`, `0.1`, `3.14` | `<class 'float'>` |
| `str` (texto) | `'Hello'`, `"abc"` | `<class 'str'>` |
| `bool` (booleano) | `True`, `False` | `<class 'bool'>` |

### Operadores aritméticos completos

| Operador | Nome | Exemplo | Output |
|---|---|---|---|
| `+` | soma | `10 + 3` | `13` |
| `-` | subtração | `10 - 3` | `7` |
| `*` | multiplicação | `10 * 3` | `30` |
| `/` | divisão (sempre float) | `10 / 3` | `3.3333...` |
| `**` | potência | `10 ** 3` | `1000` |
| `%` | resto (módulo) | `10 % 3` | `1` |
| `//` | divisão inteira | `10 // 3` | `3` |

**Aplicação típica:** converter total de meses em (anos, meses):
```python
dur = 173
qtd_anos = dur // 12   # 14
qtd_meses = dur % 12   # 5
```
Output: `o contrato tem a duração de 14 anos e 5 meses`

## Parte B: strings (métodos)

| Método | O que faz | Exemplo | Output |
|---|---|---|---|
| `len(s)` | tamanho do string | `len('Fundação Getulio Vargas')` | `23` |
| `s.strip()` | remove espaços nas pontas | `'   FGV '.strip()` | `'FGV'` |
| `s.replace(a, b)` | troca todas ocorrências de `a` por `b` | `'Fundacao'.replace('c', 'ç')` | `'Fundaçao'` |
| `s.find(c)` | índice da PRIMEIRA ocorrência | `'Fundação'.find('d')` | `2` |
| `s.find(c)` se não acha | retorna `-1` | `'abc'.find('z')` | `-1` |
| `s.lower()` | tudo minúsculo | `'FGV'.lower()` | `'fgv'` |
| `s.upper()` | tudo MAIÚSCULO | `'fgv'.upper()` | `'FGV'` |
| `s.capitalize()` | só primeira letra maiúscula | `'fundação getulio'.capitalize()` | `'Fundação getulio'` |
| `s.split()` | quebra em lista por espaços | `'Pedro de Alcantara'.split()` | `['Pedro', 'de', 'Alcantara']` |
| `s.split('a')` | quebra por separador específico | `'banana'.split('a')` | `['b', 'n', 'n', '']` |

### Indexação e slicing de strings

```python
n1 = 'Fundação '   # 9 caracteres incluindo o espaço final
```

| Acesso | Output | Por quê |
|---|---|---|
| `n1[0]` | `'F'` | primeira letra (índice começa em 0) |
| `n1[1]` | `'u'` | segunda letra |
| `n1[-1]` | `' '` | última (espaço) |
| `n1[-3]` | `'ã'` | antepenúltima |
| `n1[2:5]` | `'nda'` | índices 2, 3, 4 (NÃO inclui 5) |
| `n1[-6:-2]` | `'daçã'` | slice com índices negativos |
| `n1[:3]` | `'Fun'` | do início até índice 3 (excluso) |
| `n1[3:]` | `'dação '` | do índice 3 até o fim |

### Concatenação com número

```python
n1, n2, n3 = 'Fundação ', 'Getúlio ', 'Vargas'
nota = 10
n1 + n2 + n3 + ' é nota ' + nota   # TypeError!
n1 + n2 + n3 + ' é nota ' + str(nota)   # OK: 'Fundação Getúlio Vargas é nota 10'
```

## Parte C: listas

### Criação e características

```python
l = [1, 2, 3, 4, 5]                          # lista de ints
m = ['Star Wars', 'LOTR', 'Jurassic Park']   # lista de strings
mix = [1, 'a', 2.5, True]                    # lista pode misturar tipos
```

| Operação | Exemplo | Output |
|---|---|---|
| Tamanho | `len(l)` | `5` |
| Índice positivo | `l[2]` | `3` (terceiro elemento, índice começa em 0) |
| Índice negativo | `l[-2]` | `4` (segundo do fim) |
| Slice | `m[0:2]` | `['Star Wars', 'LOTR']` |
| Slice abreviado início | `m[:2]` | `['Star Wars', 'LOTR']` |
| Slice abreviado fim | `m[1:]` | `['LOTR', 'Jurassic Park']` |
| Modificar | `m[2] = 'Jurassic Park 2'` | substitui in-place |

### Métodos de lista

| Método           | O que faz                                              | Antes                       | Depois                                     |
| ---------------- | ------------------------------------------------------ | --------------------------- | ------------------------------------------ |
| `m.append(x)`    | adiciona no FIM                                        | `['A','B']`                 | `['A','B','x']`                            |
| `m.remove(x)`    | remove PRIMEIRA ocorrência de x                        | `['A','B','A']`             | `['B','A']`                                |
| `m.insert(i, x)` | insere x na posição i                                  | `['A','B']`, insert(1,'X')  | `['A','X','B']`                            |
| `m.sort()`       | ORDENA in-place (não retorna nada)                     | `[3,1,2]`                   | `[1,2,3]`                                  |
| `sorted(m)`      | retorna NOVA lista ordenada (sem modificar a original) | `[3,1,2]`                   | retorna `[1,2,3]`, original fica `[3,1,2]` |
| `'X' in m`       | testa se X está na lista, retorna bool                 |                             | `True`/`False`                             |
| `m.index(x)`     | retorna índice da primeira ocorrência de x             | `['A','B','C']`, index('B') | `1`                                        |

### Iteração com for (preview da Aula 12)

```python
myInt = [132, 234, 268, 444, 908]
soma = 0
for eachNum in myInt:
    soma = soma + eachNum
soma   # 1986
```

```python
m = ['Avatar', 'Star Wars', 'Jurassic Park', 'Superman', 'Terminator']
soma = 0
for filme in m:
    soma = soma + len(filme)
print(soma)   # 6 + 9 + 13 + 8 + 10 = 46
```

## Pegadinhas pro quiz

**1. Índice começa em 0**
- `l = [1, 2, 3, 4, 5]`. `l[0]` é `1`, não `2`. `l[5]` dá **IndexError** (não existe).
- Listo de tamanho 5 tem índices válidos 0, 1, 2, 3, 4.

**2. Slice `[a:b]` exclui o `b`**
- `l[0:2]` retorna elementos nos índices 0 e 1, NÃO no 2.
- Total de elementos no slice = `b - a` (quando ambos válidos e positivos).

**3. `sort()` vs `sorted()`** — pegadinha clássica
- `m.sort()` MODIFICA `m` e retorna `None`. Se você fizer `x = m.sort()`, `x = None`.
- `sorted(m)` retorna uma nova lista ordenada. `m` continua como estava.
- Quiz típico: "qual o valor de `m` depois de `sorted(m)`?". Resposta: igual ao que era antes (sorted não modifica).

**4. `len()` em string vs lista**
- `len('FGV')` = `3` (caracteres)
- `len(['a', 'bb', 'ccc'])` = `3` (elementos, não caracteres totais!)
- `len([])` = `0`

**5. `find()` e `index()` se NÃO acham**
- `'abc'.find('z')` → `-1` (não dá erro)
- `[1,2,3].index(99)` → **ValueError** (DÁ erro)

**6. `replace()` retorna NOVA string**
- Strings são imutáveis. `s.replace('a', 'b')` NÃO modifica `s`, retorna nova string.
- `s = 'abc'; s.replace('a', 'X'); print(s)` → ainda imprime `abc`.
- Pra modificar: `s = s.replace('a', 'X')`.

**7. Slice retorna NOVO objeto**
- `m[1:]` cria nova lista. Modificar o slice não afeta a original.

**8. `0.1 + 0.2` ≠ `0.3` (precisão de float)**
- Em Python: `0.1 + 0.2` = `0.30000000000000004`. Se o quiz mostra um output estranho com float, é provavelmente isso.

## Pra fixar

- 4 tipos: int, float, str, bool
- Operadores aritméticos: `+ - * / // % **`
- Strings têm len, slice, replace, find, lower, upper, split, strip
- Listas: append, remove, insert, sort, sorted, in, index, slice
- Index começa em 0; slice `[a:b]` exclui b
- `sort()` modifica e retorna None; `sorted()` retorna nova
- Strings são IMUTÁVEIS, listas são MUTÁVEIS
