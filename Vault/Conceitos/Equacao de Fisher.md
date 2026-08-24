---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, taxa-juros]
---

# Equação de Fisher

## Definição

Relação entre taxa nominal, taxa real e inflação. Permite separar o ganho de poder de compra (real) do ganho aparente (nominal).

## Fórmula exata

```
(1 + i_nominal) = (1 + i_real) × (1 + inflação)
```

Isolando taxa real:

```
i_real = (1 + i_nominal) / (1 + inflação) − 1
```

## Aproximação (juros baixos)

Pra inflação e taxas pequenas:

```
i_nominal ≈ i_real + inflação
i_real ≈ i_nominal − inflação
```

A aproximação **subestima** a taxa real quando juros e inflação são altos. Pra prova ANBIMA, use a fórmula exata.

## Exemplo

Aplicação rendeu 12% no ano (nominal), inflação ([[IPCA]]) foi 4,5%:

```
i_real = 1,12 / 1,045 − 1 = 7,18%
```

Aproximação daria 12 − 4,5 = 7,5%, sobreestima em 0,32 pp.

## Aplicação prática

- **Decisão de investimento:** comparar taxas nominais sem ajustar por inflação induz erro. Investidor deve olhar taxa real esperada
- **Renda Fixa:** títulos prefixados (LTN) pagam taxa nominal, expostos à variação de inflação. NTN-B paga IPCA + cupom (taxa real travada)
- **Aposentadoria:** projeção de poder de compra futuro exige descontar inflação esperada

## Pegadinhas

- Taxa real **negativa** existe: nominal < inflação. Investidor perde poder de compra mesmo ganhando em reais
- "Taxa real ex-ante" (esperada) ≠ "taxa real ex-post" (realizada). Inflação efetiva pode surpreender
- Para conversão de período (anual → mensal), aplicar capitalização composta na real e na nominal separadamente, não na fórmula direto

## Conceitos relacionados

- [[IPCA]]
- [[SELIC]]
- [[Volatilidade]]
