---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, lean]
---

# Just-in-Time

## Definicao

**"A peca certa, no tempo certo, na quantidade certa."** E um dos dois pilares da [[Casa do Lean]] (o outro e [[Jidoka]]). Visa entregar exatamente o que o proximo elo da cadeia precisa, exatamente quando precisa, na quantidade certa, sem estoque intermediario.

Apresentado na aula 11.05 como parte da introducao ao [[Pensamento Enxuto]].

## Quatro elementos (slide do professor)

1. **Fluxo continuo** — minimizar interrupcao entre etapas (ver [[Fluxo]]).
2. **[[Takt time]]** — ritmo alinhado com a demanda do cliente.
3. **[[Sistema puxado]]** — proxima etapa puxa, nao se empurra producao.
4. **Mao-de-obra flexivel** — operador apto a varias estacoes, capacidade redistribuivel.

## Por que importa

Ataca diretamente tres dos 8 [[MUDA]]:
- Superproducao (#4) — so se produz o que foi puxado.
- Estoque (#3) — WIP minimo entre etapas.
- Espera (#5) — fluxo continuo elimina filas.

## Pre-requisitos

- [[Heijunka]] (nivelamento) pra suavizar a variacao de demanda.
- [[Trabalho Padronizado]] pra cada estacao operar de forma previsivel.
- Estabilidade operacional na base.

Sem isso, JIT vira improviso e quebra.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Casa do Lean]]
- [[Jidoka]]
- [[Fluxo]]
- [[Takt time]]
- [[Sistema puxado]]
- [[Tempo de Ciclo]]
- [[Balanceamento de Linha]]
