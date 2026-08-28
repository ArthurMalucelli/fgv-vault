---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito, caso, competencia-vs-caixa]
---

# Caso Zezinho Pipoqueiro

## Definição

Caso de ContabilidadeFinanceira (aulas de 12/08 e 17/08) sobre apuração de resultado. Aposentado monta negócio de pipoca sem investir capital próprio (aluga o carrinho por dia, depois compra insumo a prazo) e retira 100% do lucro como renda pessoal. Cada fase do negócio introduz um descasamento novo entre lucro e caixa.

## O arco

- Dia único: paga e recebe tudo no dia, sem estoque. [[Regime de Caixa]] e [[Regime de Competência]] coincidem (lucro do dia 80)
- M1: despesas incorridas, nada pago ainda. Lucro 1.150 com FCO +3.200 (caixa maior que lucro)
- M2: venda no cartão e estoque entram. Lucro 1.370 com FCO (350) (lucro sem caixa)
- M3: cartão de M2 entra, operação normaliza. Lucro 1.590, FCO 1.260

## Por que é central

- [[CMV]] vs compra: M2 compra 1.340, consome 680, sobra [[Estoque|estoque]] de 660
- Limite de retirada é o lucro do período, nunca o saldo de caixa: o excedente pertence aos credores
- Payout de 100% mantém [[Lucros Acumulados]] e PL em zero: ativo 100% financiado por terceiros, sem colchão contra atraso de recebimento

## Material

Pasta `10 Matérias/ContabilidadeFinanceira/Aulas/08.12/` (caso A: PDF, [[ResolucaoCasoZezinhoA]], ZezinhoDFs.xlsx) e `Aulas/08.17/Slides/` (caso B, mês 3).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Regime de Competência]] e [[Regime de Caixa]]
- [[CMV]] e [[Estoque]]
- [[Contas a Pagar]] e [[Contas a Receber]]
- [[Dividendos]] e [[Lucros Acumulados]]
- [[Capital de Giro]]
