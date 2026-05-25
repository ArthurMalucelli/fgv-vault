---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao, estrutura-dados]
---

# Estruturas de Dados Python

## Quatro estruturas principais

| Estrutura | Sintaxe | Mutável | Ordenado | Permite repetição |
|---|---|---|---|---|
| Lista | `[1, 2, 3]` | Sim | Sim | Sim |
| Tupla | `(1, 2, 3)` | Não | Sim | Sim |
| Dicionário | `{'a': 1, 'b': 2}` | Sim | Sim (3.7+) | Não (chaves) |
| Conjunto (set) | `{1, 2, 3}` | Sim | Não | Não |

## Lista

Ordenada, mutável. Acesso por índice (começa em 0).

```python
nomes = ['Ana', 'Bruno', 'Caio']
nomes[0]              # 'Ana'
nomes[-1]             # 'Caio' (último)
nomes.append('Davi')  # adiciona no fim
nomes.remove('Bruno') # remove primeiro 'Bruno'
nomes[1:3]            # slicing: ['Bruno', 'Caio']
len(nomes)            # tamanho
```

Métodos: `.append()`, `.insert()`, `.remove()`, `.pop()`, `.sort()`, `.reverse()`, `.count()`, `.index()`, `.copy()`.

## Tupla

Como lista, mas **imutável**. Usada quando o conteúdo não deve mudar (coordenadas, retorno de função múltiplo).

```python
coord = (10, 20)
coord[0]              # 10
coord[0] = 5          # TypeError: tupla é imutável
```

Pegadinha: tupla com 1 item precisa vírgula: `(5,)`. Sem vírgula é só parênteses.

## Dicionário

Pares chave-valor. Acesso por chave, não índice.

```python
aluno = {'nome': 'Ana', 'idade': 19, 'curso': 'CGAE'}
aluno['nome']                 # 'Ana'
aluno['cidade'] = 'SP'        # adiciona chave nova
del aluno['idade']            # remove chave
aluno.keys()                  # dict_keys(['nome', 'curso', 'cidade'])
aluno.values()                # dict_values(['Ana', 'CGAE', 'SP'])
aluno.items()                 # pares (chave, valor)
'nome' in aluno               # True
```

Iterar:

```python
for chave, valor in aluno.items():
    print(chave, '=', valor)
```

## Set (conjunto)

Coleção sem ordem, sem repetição. Útil pra deduplicar.

```python
numeros = {1, 2, 2, 3, 3, 3}   # vira {1, 2, 3}
a = {1, 2, 3}
b = {3, 4, 5}
a | b                          # união: {1,2,3,4,5}
a & b                          # interseção: {3}
a - b                          # diferença: {1, 2}
```

## Quando usar qual

| Situação | Estrutura |
|---|---|
| Coleção que muda, ordem importa | Lista |
| Coleção fixa que não muda | Tupla |
| Lookup por chave (nome → valor) | Dicionário |
| Conjunto único, operações de conjunto | Set |

## Pegadinha clássica

`lista[0]` acessa elemento. `dicionario[chave]` também acessa, mas chave não é índice numérico. Confundir os dois é erro comum em iniciantes.

## Conceitos relacionados

- [[Loop]] (iterar sobre estruturas)
- [[Funcao Python]] (passar e retornar estruturas)
