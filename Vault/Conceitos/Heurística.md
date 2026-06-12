---
tipo: conceito
materias: [ComportamentoDoConsumidor]
tags: [conceito]
---

# Heurística

## Definição

Atalho mental: regra simplificada que leva a uma decisão rápida sem processar toda a informação disponível. Típica de decisões habituais e de baixo [[Envolvimento]].

## Fórmula / aplicação

Heurísticas vistas em aula:
- **Covariação**: inferir qualidade por sinais que costumam andar juntos.
- **País de origem**: alemão = engenharia boa, etc.
- **Nome de marca familiar**: o conhecido parece mais seguro.
- **Preço alto como proxy de qualidade**.

As regras de decisão não compensatórias (conjuntiva, disjuntiva, lexicográfica, eliminação por aspectos) também funcionam como heurísticas: cada uma pondera os atributos de um jeito, por isso **regras diferentes levam a escolhas diferentes** sobre a mesma tabela de alternativas.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Regra não compensatória]]
- [[Regra compensatória]]
- [[Nudge]]
