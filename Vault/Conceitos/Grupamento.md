---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, renda-variavel, evento-societario]
---

# Grupamento (Inplit, Reverse Split)

## Definição

Evento societário em que **N ações são agrupadas em 1 ação nova**, com aumento proporcional no preço unitário. Inverso do [[Desdobramento]]. Patrimônio do acionista e valor de mercado da empresa **não mudam**.

## Fórmula / aplicação

```
Preço pós-grupamento = Preço pré × Fator
Quantidade pós-grupamento = Quantidade pré / Fator
```

**Motivação**:
- Sair da faixa de **penny stock** (< R$ 1,00). Penny stocks são excluídos do Ibovespa, perdem visibilidade e liquidez.
- Reduzir volatilidade. Variação mínima de R$ 0,01 sobre preço baixo é % grande.

**Exemplo**: ação a R$ 0,50, grupamento 20:1. Vira 1 ação a R$ 10,00. Acionista com 20 ações passa a ter 1.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Desdobramento]]
