---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, taxa-juros]
---

# CDI

## Definição

Certificado de Depósito Interbancário. É um produto, não uma taxa: o documento que registra um banco emprestando para outro, overnight, sem garantia em título público.

A taxa correta é **taxa DI**, popularmente chamada de "taxa CDI".

## Diferença para [[SELIC]]

- SELIC over: operação interbancária com garantia (livre de risco)
- CDI: operação sem garantia (carrega risco de crédito)

Desde 2018, **DI = SELIC numericamente**, mas conceitualmente DI tem risco e SELIC não. Por isso produtos com risco usam DI como benchmark.

## Cálculo de produto a X% do CDI

Regra: aplicar o percentual sobre a taxa **diária**, nunca sobre a anual.

```
DI_dia = (1 + DI_ano)^(1/252) − 1
r_dia  = DI_dia × p
Fator  = (1 + r_dia)^n
```

## Convenções de mercado

- **> 100% CDI**: prêmio de risco. Banco menor, captação agressiva
- **< 100% CDI**: produto isento de IR (LCI, LCA), troca rentabilidade bruta por benefício fiscal
- Quem define o percentual é o emissor

## Conceitos relacionados

- [[SELIC]]
- [[CDB]]
- [[LCI]]
- [[LCA]]
- [[Capitalização diária]]
- [[Risco de crédito]]
