---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# str accessor

## Definição

Acessório do [[Pandas]] que distribui uma função ou uma indexação string para **todos** os elementos de uma coluna de strings. Sem o `.str`, tentar usar métodos de string ou indexação direto numa coluna não funciona (ou retorna algo inesperado, como uma linha do DataFrame em vez de um caractere).

A regra mental: tudo que vem à direita de `.str` é aplicado em **cada elemento string** da coluna, não na coluna como um todo.

## Fórmula / aplicação

```python
df["nome"].str.upper()       # tudo maiúsculo
df["nome"].str.lower()       # tudo minúsculo
df["nome"].str[0]            # primeiro caractere de cada string
df["nome"].str[-1]           # último caractere
df["nome"].str[-5:]          # últimos 5 caracteres (slicing)
df["nome"].str.split()       # separa por espaço, retorna lista
df["nome"].str.len()         # quantidade de caracteres de cada string
```

Caso típico: criar uma coluna derivada da manipulação string.

```python
df["Inicial"] = df["Nome"].str[0]
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Pandas]]
- [[DataFrame]]
- [[Fatiamento lógico]]
