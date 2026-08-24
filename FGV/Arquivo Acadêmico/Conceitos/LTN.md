---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, renda-fixa, titulos-publicos]
---

# LTN (Letra do Tesouro Nacional)

## Definição

Título público federal prefixado, sem pagamento de cupom. Marca comercial no [[Tesouro Direto]]: "Tesouro Prefixado".

- Valor de face (VN): **sempre R$ 1.000**.
- Pagamento único no vencimento (principal + juros embutidos no deságio).
- Sempre negociada com **deságio** (P < 1.000), pois prêmio exigiria YTM negativa.

## Fórmulas

Preço a partir do YTM:
```
P = 1000 / (1 + YTM_aa)^(du/252)
```

YTM a partir do preço:
```
YTM = (1000/P)^(252/du) − 1
```

Excel:
```
=1000/(1+YTM)^(du/252)
=-VP(YTM; du/252; ; 1000)
=(1000/P)^(252/du)-1
```

## Venda intermediária (marcação a mercado)

```
P0 = 1000/(1+YTM_compra)^(du_compra/252)
P1 = 1000/(1+YTM_venda)^((du_compra − Δdu)/252)
Retorno período = P1/P0 − 1
```

YTM subiu → preço caiu → retorno < YTM contratada. YTM caiu → retorno > YTM contratada.

## Tributação

Alíquota regressiva ([[IR Renda Fixa]]) sobre o ganho (P_venda − P_compra).

## Conceitos relacionados

- [[NTN-F]]
- [[Tesouro Direto]]
- [[YTM]]
- [[Dias Úteis]]
- [[IR Renda Fixa]]

## Onde aparece

```dataview
LIST
FROM ""
WHERE contains(file.outlinks, this.file.link) AND file.name != this.file.name
SORT file.path ASC
```
