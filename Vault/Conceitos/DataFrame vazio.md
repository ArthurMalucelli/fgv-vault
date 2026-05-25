---
tipo: conceito
materias: [Programacao]
tags: [conceito]
---

# DataFrame vazio

## Definição

Resultado de uma filtragem em [[Pandas]] que não encontra nenhuma linha correspondente. Não é erro: retorna um [[DataFrame]] que **mantém todas as colunas** mas tem **zero linhas**.

```python
df[df["username"] == "Getulio"]   # username inexistente
```

Se `Getulio` não está na coluna, o resultado é um DataFrame com as 5 colunas originais e 0 linhas. Importante distinguir: pandas não lança exceção quando filtro não casa.

## Fórmula / aplicação

Padrão de uso: checar **existência** com `len()`.

```python
resultado = df[df["username"] == username]

if len(resultado) == 0:
    print("Não existe")
else:
    print("Existe")
```

`len(dataframe)` retorna a quantidade de **linhas**. Zero linhas significa que nenhuma linha satisfez a condição.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[DataFrame]]
- [[Fatiamento lógico]]
- [[Pandas]]
