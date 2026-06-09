---
tipo: conceito
materias: [Programacao]
tags: [conceito, python, programacao, pandas]
---

# read_csv

## Definição

Função do [[Pandas]] que carrega um arquivo de texto tabular (CSV) num [[DataFrame]]. Os parâmetros controlam como o arquivo é interpretado.

## Fórmula / aplicação

```python
import pandas as pd
df = pd.read_csv("arquivo.csv")                        # padrão (vírgula separa, ponto decimal)
df = pd.read_csv("arquivo.csv", sep=";", decimal=",")  # CSV brasileiro
df = pd.read_excel("arquivo.xlsx")                     # versão pra Excel
df = pd.read_excel("arquivo.xlsx", index_col=0)        # usa a 1ª coluna como índice
```

## Pegadinha central (CSV brasileiro)

Arquivo gerado no Brasil costuma separar colunas por `;` e usar `,` como decimal. Sem `sep=";"`, tudo cai numa coluna só. Sem `decimal=","`, os números viram **texto**, e qualquer conta (`mean`, `sum`, `*`) quebra ou dá resultado errado.

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
- [[astype]]
