---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, câmbio, paridade]
---

# PPP (Purchasing Power Parity / Paridade do Poder de Compra)

## Definição

Teoria que relaciona taxa de câmbio nominal com diferencial de inflação entre dois países. Duas versões: absoluta (Big Mac index) e relativa.

## PPP relativa (a que cai na prova)

```
E(1 + π_local) / E(1 + π_estrangeira) = E(spot_local/estrangeira) / spot_local/estrangeira
```

Reorganizando:
```
S_new = S_old × (1 + π_local) / (1 + π_estrangeira)
```

## Lógica

Inflação local maior que estrangeira → moeda local perde poder de compra mais rápido → moeda local **deprecia** → precisa MAIS moeda local por unidade da estrangeira.

## PPP absoluta

```
S_PPP = P_local / P_estrangeira
```
Câmbio que igualaria o preço de uma cesta entre os dois países. Big Mac de R$ 30 no BR vs US$ 10 nos EUA → câmbio PPP = R$ 3/USD.

## Aplicação típica

BRL/EUR = 4,43 em 2022. π_BR = 9,74%, π_EUR = 6,62%. Câmbio em 2023:
```
S_2023 = 4,43 × (1,0974) / (1,0662) = 4,56 BRL/EUR
```
BRL deprecia (precisa mais BRL por EUR).

## Por que PPP falha na prática

- Custos de transporte
- Tarifas e barreiras comerciais
- Diferenças de qualidade
- Bens não-tradables (serviços, imóveis)
- Fluxos financeiros, expectativas, política monetária

## Conceitos relacionados

- [[IRP]]
- [[Carry Trade]]
- [[Cotação Direta]]
