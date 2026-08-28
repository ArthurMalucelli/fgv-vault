---
materia: Programacao
aula: 14
tema: Funções (def, return, parâmetros)
quiz: 2026-05-05
---

# Aula 14: Funções

Última aula do bloco. Conceito MUITO importante: distinção entre `print` e `return`. Provavelmente vai cair "qual o output" ou "qual o valor da variável" misturando função com print.

## Conceitos centrais

| Conceito | O que é |
|---|---|
| `def nome(...)` | Define uma função |
| Parâmetro | Variável que a função recebe (definida no `def`) |
| Argumento | Valor passado quando chama a função |
| `return` | Devolve valor pra quem chamou |
| Sem `return` | Função retorna `None` (implícito) |
| Variável local | Existe só dentro da função |
| Função built-in | Já vem no Python: `print`, `len`, `sum`, `int`, `str`, `input`... |

## Sintaxe

```python
def nome_da_funcao(parametro1, parametro2):
    # corpo da função (indentado)
    resultado = parametro1 + parametro2
    return resultado
```

Chamada:
```python
x = nome_da_funcao(5, 10)   # x = 15
```

## Exemplos canônicos

### 1. Função built-in vs definida

Built-ins prontas:
```python
lista = [1, 2, 3]
sum(lista)         # 6
len(lista)         # 3
sum(lista) / len(lista)   # 2.0 (média)
```

Definindo a sua própria:
```python
def mean(l):
    return sum(l) / len(l)

mean([1, 2, 3])         # 2.0
mean([-3, 0, 4, 10])    # 2.75
```

### 2. Função que IMPRIME (sem return)

```python
def greet(nome):
    print('hello,', nome)

greet('John')   # imprime: hello, John
greet('Mary')   # imprime: hello, Mary
```

### 3. Função com múltiplos parâmetros

```python
def g(x, y):
    m = (x + y) / 2
    return m

g(-10, 5)   # -2.5
```

## A pegadinha CENTRAL: print vs return

Compare estas duas funções:

```python
def f(x):
    return x ** 2

def escreve_x_ao_quadrado(x):
    print(x ** 2)
```

Visualmente parecidas. Comportamento DIFERENTE.

```python
f(-4)                        # mostra 16 (Jupyter mostra valor de retorno)
escreve_x_ao_quadrado(-4)    # imprime 16

y = f(5)                     # y = 25 (valor de retorno)
print(y)                     # 25

z = escreve_x_ao_quadrado(5) # imprime 25 NA HORA, e z recebe None
print(z)                     # None
```

**Resumo:**
- `return` DEVOLVE valor pra usar fora
- `print` SÓ MOSTRA na tela
- Função sem `return` retorna `None`
- Atribuir `x = funcao_que_so_imprime(...)` faz `x = None`

ESSA É A PEGADINHA #1 DE FUNÇÕES NO QUIZ.

## Padrões típicos dos exercícios

### Função com tratamento de caso

```python
def divisao(a, b):
    if b == 0:
        return 999999
    else:
        return a / b
```

Sem print. Devolve resultado, quem chamou decide o que fazer.

### Função booleana (retorna True/False)

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
```

Usa: `if is_prime(7): print('é primo')`.

### Função pra lookup por faixa (alíquota IR)

```python
def get_aliquota(pdi):
    if pdi <= 180:
        aliquota = 0.225
    elif pdi <= 360:
        aliquota = 0.20
    elif pdi <= 720:
        aliquota = 0.175
    else:
        aliquota = 0.15
    return aliquota
```

### Função que recebe LISTA e processa

```python
def conta_discos(tipos):
    discos_por_tipo = {
        'simple': 1,
        'Special Edition': 2,
        '3D': 2,
        'series': 6,
        'series - sitcom': 4
    }
    total = 0
    for t in tipos:
        total = total + discos_por_tipo.get(t, 0)
    return total
```

(Note: `dict` ainda não foi formalmente coberto até Aula 14, mas o exercício do DVD pode ser implementado com if/elif).

## Pegadinhas pro quiz

**1. Função sem `return` devolve `None`**
- `def f(x): print(x)`
- `r = f(5)` → imprime 5, mas `r = None`
- `print(r)` → `None`

**2. `return` PARA a função imediatamente**
```python
def f(x):
    if x > 0:
        return 'positivo'
    return 'não positivo'
    print('nunca executa')   # essa linha morre
```
Tudo depois do `return` que executou é IGNORADO.

**3. Múltiplos `return` são OK**
- A função sai no primeiro `return` cuja condição foi atingida.

**4. Variável dentro da função NÃO existe fora**
```python
def f():
    x = 10
    return x

f()
print(x)   # NameError, x não existe aqui
```

**5. Variável fora pode ser LIDA dentro**
```python
y = 10
def f():
    print(y)   # 10, lê do escopo externo

f()
```
Mas REASSIGNAR dentro cria uma local nova (não muda a externa) sem `global`.

**6. Argumentos passados por VALOR (pra imutáveis)**
```python
def f(x):
    x = x + 1

a = 5
f(a)
print(a)   # 5, não 6
```
Modificar `x` dentro NÃO afeta `a` fora (int, float, str, bool são imutáveis).

**7. Listas SÃO modificadas se você fizer `.append`/`.remove` dentro**
```python
def adiciona(lst):
    lst.append(99)

minha = [1, 2, 3]
adiciona(minha)
print(minha)   # [1, 2, 3, 99]
```
Listas são mutáveis, a modificação dentro persiste fora. Pegadinha sutil mas importante.

**8. Ordem dos argumentos importa (posicional)**
```python
def divisao(a, b):
    return a / b

divisao(10, 2)   # 5.0
divisao(2, 10)   # 0.2
```

**9. Função pode chamar outra função**
- `def media(l): return sum(l) / len(l)` chama `sum` e `len`.

**10. Critério de correção típico (mencionado nos exercícios)**
- "Não usar print dentro da função" significa devolver com return
- "Não retornar com return" zera a questão
- Se quiz mostra função com print onde devia ser return, opção provavelmente errada

## "Modelo mental" das funções

Pensa numa função como uma máquina:
1. Recebe entradas (parâmetros)
2. Processa
3. DEVOLVE saída (`return`) ou IMPRIME na tela (`print`)

`return` te dá um valor pra GUARDAR ou USAR em outra conta. `print` é só visualização.

Exemplo claro:
```python
def soma(a, b):
    return a + b   # devolve o valor

resultado = soma(3, 4)   # resultado = 7
total = resultado * 2    # 14, conseguiu USAR o retorno

# Compare com:
def soma_print(a, b):
    print(a + b)   # imprime, mas não devolve

resultado = soma_print(3, 4)   # imprime 7, resultado = None
total = resultado * 2          # TypeError (None * 2)
```

## Pra fixar

- `def nome(args):` cria função, indentação no corpo
- `return x` devolve, função PARA aí
- Sem return → função retorna `None`
- `print` mostra na tela, NÃO devolve nada
- Variável dentro não vaza pra fora (escopo local)
- Lista passada e modificada DENTRO persiste FORA (mutável)
- Atribuir resultado: `x = funcao(...)` só faz sentido se a função tem `return`
