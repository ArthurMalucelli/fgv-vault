---
materia: Programacao
aula: 13
tema: Aula de exercícios — síntese listas + loops + condicionais (sem funções)
quiz: 2026-05-05
---

# Aula 13: Exercícios (síntese pré-funções)

NÃO temos o notebook teórico desta aula. Os exercícios indicam que foi uma aula de revisão/aplicação combinando TUDO até aula 12 (listas, loops, condicionais), JÁ SEM funções (que vêm na 14).

Foco: aplicação em problemas de negócio (estoque, receita, AOV de pedidos). Esses padrões caem com peso porque misturam vários conceitos numa só pergunta.

## Tópicos cobertos

### Bloco 1: predição de output (revisão de listas + loops)

```python
a = ['Batman', 'Hulk', 'Thor', 'Aquaman']
```

| Código | Output |
|---|---|
| `for i in a: print(i)` | `Batman / Hulk / Thor / Aquaman` (cada um numa linha) |
| `for i in range(len(a)): print(a[i])` | mesma coisa |
| `for i in a: print(len(i))` | `6 / 4 / 4 / 7` |
| `for i in a: print(a)` | imprime a lista inteira 4 VEZES (uma por iteração!) |

A última é a pegadinha do quiz: `print(a)` está dentro do loop e imprime a lista TODA cada vez.
Output completo:
```
['Batman', 'Hulk', 'Thor', 'Aquaman']
['Batman', 'Hulk', 'Thor', 'Aquaman']
['Batman', 'Hulk', 'Thor', 'Aquaman']
['Batman', 'Hulk', 'Thor', 'Aquaman']
```

### Bloco 2: Estoque (listas paralelas + condicional dentro de loop)

```python
estoque = [19, 7, 5, 1, 2, 16, 8, 20, 13, 4, 18, 10, 10, 8, 4, 15, 19, 3, 7, 3]
limite  = [20, 9, 7, 16, 4, 7, 10, 13, 14, 11, 5, 4, 7, 11, 3, 1, 8, 15, 11, 13]

lista_de_reposicao = []
for i in range(len(estoque)):
    if estoque[i] < limite[i]:
        lista_de_reposicao.append(i)

print(lista_de_reposicao)
```

Padrão clássico: duas listas paralelas, percorre por ÍNDICE pra acessar a mesma posição em ambas. `for i in range(len(...))` é o jeito de fazer isso.

### Bloco 3: Crescimento percentual de receita

Fórmula:
$$\text{crescimento} = \frac{\text{receita}_t - \text{receita}_{t-1}}{\text{receita}_{t-1}} \times 100$$

```python
receitas = [100000, 110000, 115000]
for i in range(1, len(receitas)):
    crescimento = (receitas[i] - receitas[i-1]) / receitas[i-1] * 100
    print(f'Crescimento ano {i}: {crescimento:.2f}%')
```

CRÍTICO: começa em `range(1, ...)` porque o primeiro elemento não tem ano anterior pra comparar. Se começar em 0, dá IndexError quando tenta `receitas[-1]` (que vira o ÚLTIMO elemento, comportamento errado).

### Bloco 4: AOV (Average Order Value)

Fórmula:
$$\text{AOV} = \frac{\text{soma dos pedidos}}{\text{quantidade de pedidos}}$$

```python
pedidos = [1151.16, 1605.16, 861.19, 1276.47, 1611.14, 1873.11, 1764.36, 1548.02, 1448.20, 683.16]

soma = 0
acima_1000 = 0
for p in pedidos:
    soma = soma + p
    if p > 1000:
        acima_1000 = acima_1000 + 1

aov = soma / len(pedidos)
print(f'AOV: {aov:.2f}')
print(f'Pedidos acima de R$1000: {acima_1000}')
```

Padrão acumulador duplo: uma variável pra soma, outra pra contagem. Tudo no mesmo loop pra evitar percorrer duas vezes.

### Bloco 5: Manipulação de strings (palindromo)

```python
word = input('palavra:')
backwards = ''
for i in range(len(word) - 1, -1, -1):   # do fim pro início
    backwards = backwards + word[i]

if word == backwards:
    print('palindromo!')
else:
    print('não é palindromo. Invertido:', backwards)
```

Forma mais Pythonic (mas a aula provavelmente não cobriu): `word[::-1]` inverte direto.

Exemplo de palindromo dado: `'socorrammesubinoonibusemmarrocos'`.

### Bloco 6: Listas via loop com input (LISTA + LISTA2)

```python
# Parte 1: coletar nomes em LISTA, em maiúsculas, parar com ENTER vazio
LISTA = []
while True:
    nome = input('digite um nome (ENTER pra parar):')
    if nome == '':
        break
    LISTA.append(nome.upper())
print(LISTA)

# Parte 2: filtrar nomes que começam com consoante em LISTA2
vogais = ['A', 'E', 'I', 'O', 'U']
LISTA2 = []
for nome in LISTA:
    if nome[0] not in vogais:
        LISTA2.append(nome)
print(LISTA2)
```

Padrão: dois loops separados, cada um com seu propósito. Vai cair MUITO em quiz e prova final.

## Pegadinhas pro quiz

**1. `for i in a: print(a)` imprime a lista inteira N vezes**
- O que está dentro do loop é o que se repete. Se `print(a)` está lá, repete.

**2. Listas paralelas usam mesmo índice**
- `estoque[i]` e `limite[i]` são valores DA MESMA POSIÇÃO i.
- Loop sobre `range(len(...))` com uma das listas (qualquer uma, mesmo tamanho).

**3. Comparação de períodos: pula primeiro elemento**
- Crescimento entre `t` e `t-1` exige `range(1, len(...))`.
- Se começar em 0, `lista[-1]` retorna o ÚLTIMO (não dá erro mas comportamento errado).

**4. Acumulador duplo no mesmo loop**
- Uma variável pra soma, outra pra contagem, ambas inicializadas em zero ANTES do loop.

**5. Inverter string com loop**
- `range(len(s) - 1, -1, -1)` vai do último ao primeiro índice.
- Mais simples: `s[::-1]` (slice reverso, mas pode não ter sido coberto).

**6. `while True` + `break` é padrão pra "parar quando..."**
- Combinação típica pra ler input até user mandar parar.

**7. `not in` é o oposto de `in`**
- `'x' not in lista` é o mesmo que `not ('x' in lista)`.

## Aplicação financeira: ETH (preview de pandas)

O notebook menciona spoiler de pandas para próximas aulas:
```python
import pandas as pd
eth = pd.read_csv('...ETHUSDT.csv.gzip', compression='gzip', index_col='open_time')
```

Provavelmente NÃO cai no quiz desta semana (pandas vem depois), mas saber que existe ajuda.

## Pra fixar

- Listas paralelas: `for i in range(len(...))`, acessa por índice
- Crescimento ou diff sequencial: começa loop em 1, usa `lista[i]` e `lista[i-1]`
- Acumulador soma + contador no MESMO loop
- `while True` + `if cond: break` pra parar com input vazio
- `not in` pra negação de pertence
- Output dentro vs fora do loop: indentação muda tudo
