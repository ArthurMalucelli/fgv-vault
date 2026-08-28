---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, taxa-juros]
---

# SELIC

## Definição

Taxa básica de juros da economia brasileira. Definida pelo Copom (Comitê de Política Monetária do Banco Central). Existe em duas formas:

- **SELIC meta**: alvo definido pelo Copom
- **SELIC over**: taxa praticada nas operações overnight com garantia em título público (livre de risco)

## Fórmula

Conversão anual → diária (base 252 dias úteis):

```
SELIC_dia = (1 + SELIC_ano)^(1/252) − 1
```

## Política monetária

- SELIC over abaixo da meta: BC vende títulos, retira liquidez, taxa sobe
- SELIC over acima da meta: BC compra títulos, injeta liquidez, taxa cai

## Conceitos relacionados

- [[CDI]]
- [[Tesouro SELIC]]
- [[Open Market]]
- [[Capitalização diária]]

## Onde aparece

```dataview
LIST
FROM ""
WHERE contains(file.outlinks, this.file.link) AND file.name != this.file.name
SORT file.path ASC
```
