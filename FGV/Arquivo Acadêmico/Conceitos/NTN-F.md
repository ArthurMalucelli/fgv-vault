---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, renda-fixa, titulos-publicos]
---

# NTN-F (Nota do Tesouro Nacional série F)

## Definição

Título público federal prefixado com pagamento de juros semestrais. Marca comercial no [[Tesouro Direto]]: "Tesouro Prefixado com Juros Semestrais".

- Valor de face: **R$ 1.000**.
- Taxa cupom: **10% a.a. efetivo** (capitalizado semestralmente).
- Cupons pagos sempre em **01/01 e 01/07**.

## Cupom semestral

Por se tratar de taxa efetiva (não nominal):
```
i_cs = (1,10)^0,5 − 1 = 4,8809%
Cupom em R$ = 1000 × 4,8809% = R$ 48,8088
```

No último fluxo, paga cupom + principal: **R$ 1.048,81**.

## Preço

Soma do VP de cada cupom + VP do principal:
```
P = Σ_k [48,8088 / (1 + YTM)^(du_k/252)] + 1000/(1+YTM)^(du_N/252)
```

YTM dado o preço: **não tem fórmula fechada**. Usar Atingir Meta (Goal Seek) ou TIR sobre o fluxo.

## Relação cupom × YTM

- Cupom (10%) > YTM → preço com **prêmio** (P > 1.000).
- Cupom = YTM → preço = par (P = 1.000).
- Cupom < YTM → preço com **deságio** (P < 1.000).

## Venda intermediária

Preço pode cair por dois motivos simultâneos: YTM mudou, e alguns cupons já foram pagos (saem do fluxo restante).

## Conceitos relacionados

- [[LTN]]
- [[Tesouro Direto]]
- [[Cupom Semestral]]
- [[YTM]]
