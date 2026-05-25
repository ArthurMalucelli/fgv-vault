---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, tributacao]
---

# IR sobre Renda Fixa (BR)

## Regra geral

Alíquota **regressiva** sobre o **ganho** (não sobre o total resgatado). Quanto mais tempo aplicado, menor a alíquota. Recolhido pela fonte no resgate.

## Tabela regressiva

| Prazo (dias corridos) | Alíquota |
|---|---|
| Até 180 | 22,5% |
| 181 a 360 | 20,0% |
| 361 a 720 | 17,5% |
| Acima de 720 | 15,0% |

## Cálculo

```
Ganho = P_venda − P_compra
IR = alíquota × Ganho
Líquido = P_venda − IR
```

**Erro comum**: aplicar a alíquota sobre o total resgatado em vez do ganho.

## Aplicação a títulos

- [[LTN]], [[NTN-F]], [[CDB]]: tabela regressiva clássica.
- Fundos de investimento abertos: come-cotas semestral + ajuste no resgate.
- [[LCI]] e LCA: **isentos** para pessoa física (por isso pagam < 100% do CDI).
- Tesouro IPCA+ (NTN-B): mesma tabela regressiva.

## Conversão útil → corrido (aproximada)

Para enquadrar na tabela quando o exercício dá dias úteis:
```
dias_corridos ≈ dias_úteis × 1,4
```

## Conceitos relacionados

- [[LTN]]
- [[NTN-F]]
- [[CDB]]
- [[Come-cotas]]
