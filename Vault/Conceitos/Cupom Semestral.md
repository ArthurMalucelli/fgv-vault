---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, renda-fixa]
---

# Cupom Semestral

## Definição

Pagamento periódico (a cada 6 meses) de juros de um título de renda fixa. Característica da [[NTN-F]] e da NTN-B brasileiras, e de bonds americanos com cupom.

## NTN-F: cupom efetivo

Taxa cupom 10% a.a. **efetivo**, capitalizada semestralmente:
```
i_cs = (1 + 10%)^0,5 − 1 = 4,8809%
Cupom em R$ = 1000 × 4,8809% = R$ 48,81
```

Pago sempre em 01/01 e 01/07.

## Bonds americanos: cupom linear

Convenção americana usa taxa **nominal** com divisão linear:
```
i_cs_americano = taxa_anual_nominal / 2
```
Bond com cupom nominal 10% a.a. paga 5% a cada semestre.

## Diferença Brasil vs EUA

| | Brasil (NTN-F) | EUA (bond típico) |
|---|---|---|
| Convenção cupom | Efetivo capitalizado | Nominal linear |
| Cálculo do cupom | (1+i)^0,5 − 1 | i/2 |
| Base do prazo | 252 dias úteis | 365 dias corridos |

## Conceitos relacionados

- [[NTN-F]]
- [[LTN]]
- [[YTM]]
