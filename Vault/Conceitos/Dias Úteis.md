---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, renda-fixa]
---

# Dias Úteis (du)

## Definição

Convenção brasileira para mensuração de prazos em renda fixa. Base **252 dias úteis por ano** (em vez de 365 dias corridos), excluindo finais de semana e feriados nacionais.

## Por que importa

Todas as fórmulas de [[LTN]], [[NTN-F]], [[CDI]], [[SELIC]] e produtos indexados usam base 252 no Brasil. STRIPS americanos e bonds europeus usam base anual (365).

## Convenção do Tesouro Direto

- Data de **liquidação** da compra (inclusive)
- Data de **vencimento** do título (exclusive)

A liquidação ocorre em D+1 da data de compra.

## Excel

```
Data de liquidação a partir da compra:
=DIATRABALHO(data_compra; 1; Feriados)

Dias úteis entre liquidação e vencimento:
=DIATRABALHOTOTAL(liquidação; vencimento − 1; Feriados)
```
O `−1` é porque DIATRABALHOTOTAL conta os dois extremos e o vencimento é exclusive.

## Conversão direta ↔ útil (aproximada)

```
1 ano = 252 du ≈ 365 dc
1 mês = 21 du ≈ 30 dc
1 semestre = 126 du ≈ 180 dc
```

## Conceitos relacionados

- [[LTN]]
- [[NTN-F]]
- [[Tesouro Direto]]
