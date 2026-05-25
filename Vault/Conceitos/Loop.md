---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao, controle-fluxo]
---

# Loop

## Definição

Estrutura de controle que repete um bloco de código múltiplas vezes. Python tem dois: `for` (itera sobre algo) e `while` (repete enquanto condição é verdadeira).

## for

Itera sobre sequência (lista, string, range).

```python
for i in range(5):           # 0, 1, 2, 3, 4
    print(i)

for letra in 'FGV':
    print(letra)             # F, G, V

for nome in ['Ana', 'Bruno', 'Caio']:
    print(nome)
```

`range(start, stop, step)` cria sequência: `range(2, 10, 2)` → 2, 4, 6, 8.

## while

Repete enquanto condição é True. Cuidado com loop infinito.

```python
n = 0
while n < 5:
    print(n)
    n += 1                   # SEM isso, loop infinito
```

Caso clássico: ler input até usuário sair.

```python
texto = ''
while texto != 'sair':
    texto = input('digite: ')
```

## Quando usar qual

| Situação | Use |
|---|---|
| Sei quantas vezes vai rodar | `for` |
| Tenho uma sequência e quero passar por todos | `for` |
| Repete até condição mudar (e não sei quando) | `while` |
| Input do usuário até sinal de parada | `while` |

## break e continue

- `break`: sai do loop imediatamente
- `continue`: pula pra próxima iteração

```python
for x in range(10):
    if x == 5:
        break                # para no 5
    if x % 2 == 0:
        continue             # pula pares
    print(x)                 # imprime 1, 3
```

## Pegadinhas

- Modificar a lista enquanto itera sobre ela quebra. Use `lista.copy()` se for o caso
- Range é exclusivo no fim: `range(5)` vai de 0 a 4
- Indentação errada gera bug silencioso (Python depende de indentação)
- `while True` precisa de `break` em algum lugar, senão loop infinito

## Conceitos relacionados

- [[Condicional]]
- [[Funcao Python]]
- [[Estruturas de Dados Python]]
