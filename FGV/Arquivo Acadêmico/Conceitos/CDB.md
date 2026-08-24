---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, renda-fixa]
---

# CDB (Certificado de Depósito Bancário)

## Definição

Título de renda fixa privado emitido por bancos para captar recursos. Coberto pelo FGC até R$ 250 mil por CPF/instituição.

## Tipos por indexador

- **Prefixado**: taxa definida na contratação.
- **Pós-fixado**: indexado a [[CDI]] ou [[SELIC]] (X% do CDI).
- **Híbrido**: IPCA + taxa fixa.

## CDB %CDI: cálculo

A regra crítica: o percentual se aplica na taxa **diária**, não na anual nem no fator.

```
i_DI_dia = (1 + CDI_aa)^(1/252) − 1
i_CDB_dia = %CDI × i_DI_dia
Fator = (1 + i_CDB_dia)^n_du
```

**Erro comum**: aplicar o % no fator (1+CDI)^%. Não funciona.

Quando CDI varia entre sub-períodos, calcular i_CDB_dia por sub-período e encadear:
```
Fator_total = Π_k (1 + %CDI × i_DI_dia_k)^n_k
```

## Tributação

Alíquota regressiva ([[IR Renda Fixa]]) cobrada sobre o ganho no resgate. Sem come-cotas.

## Conceitos relacionados

- [[CDI]]
- [[SELIC]]
- [[LCI]]
- [[IR Renda Fixa]]
