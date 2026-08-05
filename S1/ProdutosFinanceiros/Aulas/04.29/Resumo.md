---
materia: ProdutosFinanceiros
data: 2026-04-29
tema: SELIC, CDI e cálculo de taxas diárias
tags: [resumo]
---

# Resumo — SELIC, CDI e taxas diárias (29.04.26)

## Conceitos-chave

| Item | O que é |
|---|---|
| [[SELIC]] meta | Taxa-alvo definida pelo Copom |
| [[SELIC]] over | Taxa praticada no overnight com garantia em título público (livre de risco) |
| Taxa [[CDI|DI]] | Taxa overnight interbancária sem garantia. Desde 2018 = SELIC numericamente, mas carrega risco conceitualmente |
| Base de cálculo | 252 dias úteis ao ano. Toda taxa é expressa ao ano e convertida pra diária |
| [[Tesouro SELIC]] | Pós-fixado, atualizado diariamente pela SELIC. Rentabilidade só conhecida ao final |

## Política monetária ([[Open Market]])

- SELIC over abaixo da meta: BC vende títulos, retira liquidez, taxa sobe
- SELIC over acima da meta: BC compra títulos, injeta liquidez, taxa cai

## Fórmulas essenciais

Conversão anual → diária:
```
r_dia = (1 + r_ano)^(1/252) − 1
```

Capitalização de período:
```
Fator = ∏(1 + r_dia_i)
r_periodo = Fator − 1
r_ano = Fator^(252/n) − 1
```

Produto a X% do [[CDI]]:
```
r_dia = [(1 + DI_ano)^(1/252) − 1] × p
Fator = (1 + r_dia)^n
```

**Regra de ouro**: percentual do CDI incide sempre na taxa diária, nunca na anual.

## Convenções de contagem

- `DIATRABALHOTOTAL(início; fim; feriados)`: conta dias úteis inclusivos (inclui início e fim)
- Overnight ([[CDB]], interbancário): subtrair 1 do total → conta noites
- Título público: data de vencimento é **exclusiva** (subtrair 1 da data final)
- CDB e similares: vencimento **inclusivo**
- Enunciado fala em "n dias" → são dias úteis, sem feriado a considerar
- Enunciado fala em datas → usar DIATRABALHOTOTAL com lista de feriados

## Por que [[CDI]] e não [[SELIC]] pra produto com risco

[[SELIC]] é livre de risco, não serve de benchmark pra crédito. Produtos com risco ([[CDB]], [[Debêntures]], [[LCI]], [[LCA]], fundos de renda fixa) cotam como % do CDI ou CDI + spread:

- > 100% CDI: prêmio de risco (banco menor, captação agressiva, ex: Master 124,5%)
- < 100% CDI: produto isento de IR ([[LCI]], [[LCA]]), troca rentabilidade bruta por benefício fiscal

Quem define o percentual é o emissor.

## Exemplo numérico de referência

[[SELIC]] pós-fixada, R$ 100k, 3 dias com taxas 7,40% / 7,38% / 7,36% ao ano:

```
r1 = (1,0740)^(1/252) − 1
r2 = (1,0738)^(1/252) − 1
r3 = (1,0736)^(1/252) − 1
Fator = (1+r1)(1+r2)(1+r3)
Bruto = 100.000 × Fator
```

## Pegadinhas

- Não aplicar percentual do CDI sobre taxa anual
- Não esquecer de tirar o 1 ao converter fator → taxa
- Conferir se o cálculo é em dias úteis (BR) ou corridos (EUA)
- Em overnight, lembrar a analogia do hotel: conta noites, não diárias
- Distinção título público (exclusivo) vs CDB (inclusivo) na data de vencimento

## Pra fixar

- [[SELIC]]
- [[CDI]]
- [[Tesouro SELIC]]
- [[Open Market]]
- [[CDB]]
- [[LCI]]
- [[LCA]]
- [[Capitalização diária]]

## Próxima aula

Resolução do último exercício (180 dias, 96% do DI) + [[IR]] e tributação pra chegar do bruto ao líquido.
