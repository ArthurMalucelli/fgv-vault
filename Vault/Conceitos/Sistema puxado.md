---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, lean]
---

# Sistema puxado

## Definicao

Sistema de producao em que cada etapa **so produz quando a etapa seguinte pede**. O cliente final puxa a producao pra tras, ao longo da cadeia. Oposto do sistema empurrado, onde se produz com base em previsao e se acumula estoque.

E o "Pull" dos cinco principios Lean. Componente do [[Just-in-Time]].

## Mecanismo classico

**Kanban**: cartao ou sinal visual que autoriza a etapa anterior a produzir. Sem kanban, nao produz.

## Vantagem

- Reduz [[MUDA]] de **superproducao** (#4) e **estoque** (#3).
- Faz o WIP cair, o que reduz lead time.
- Expoe rapidamente desbalanceamentos do processo.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Just-in-Time]]
- [[Takt time]]
- [[Fluxo]]
- [[MUDA]]
