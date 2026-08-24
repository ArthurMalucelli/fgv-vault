---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, lean]
---

# Fluxo

## Definicao

Movimento continuo de produtos, informacoes ou servicos atraves de um processo. Quanto mais **interrupcoes**, **esperas** e **retrabalhos**, menor o fluxo. Objetivo Lean: criar um **fluxo suave e previsivel**, onde cada etapa agrega [[Valor]].

E um dos 3 pilares do [[Pensamento Enxuto]].

## Lotes (batch) vs One-piece flow

- **Batch**: cada etapa processa o lote inteiro antes de passar. Aumenta WIP, aumenta lead time, esconde defeito.
- **One-piece flow**: uma peca de cada vez, passa imediatamente. Reduz lead time mesmo com mesma quantidade de trabalho.

No exemplo da aula (video do slide 9): Order=10 entrega em 0:29 com batch=1 e 0:36 com batch=10. Mesmo trabalho, fluxo continuo entrega mais rapido.

## Exemplo (slide do professor)

Pedir comida: pedido → preparo → entrega → consumo. Se o pedido atrasa ou o sistema cai, o fluxo e interrompido.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Pensamento Enxuto]]
- [[Just-in-Time]]
- [[Sistema puxado]]
- [[Takt time]]
- [[MUDA]]
