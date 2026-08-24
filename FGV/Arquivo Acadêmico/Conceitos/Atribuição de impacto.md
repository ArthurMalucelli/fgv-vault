---
tipo: conceito
materias: [IntroducaoAGestao]
tags: [conceito, gestao, metricas, avaliacao]
---

# Atribuição de impacto

## Definição

Problema metodológico de separar o efeito causado por uma intervenção do efeito causado pelo contexto. Sem grupo de comparação (ou método quasi-experimental), uma organização pode reportar como impacto próprio mudanças que aconteceriam mesmo sem ela.

Exemplo: ONG atende população em favela e relata aumento de renda. Se no mesmo período subiu o salário mínimo nacional ou Bolsa Família, parte (ou todo) o aumento é contexto, não atribuição. Sem dado comparativo, organização infla seu efeito.

Distinção importante:
- **Atribuição**, "este resultado existe por causa da nossa ação"
- **Contribuição**, "nossa ação somou para este resultado, junto com outros fatores"

A maioria das organizações de impacto deveria reportar contribuição, não atribuição. Reportar atribuição sem desenho experimental é exagero.

## Fórmula / aplicação

Métodos de fortalecer atribuição:
1. **RCT** (randomized controlled trial), mais rigoroso, separa beneficiário e controle por sorteio
2. **Quasi-experimental** (diff-in-diff, propensity score matching), comparação com grupo similar não tratado
3. **Análise de séries temporais**, comparação com tendência pré-intervenção

Sem nada disso, ficar honestamente no nível de contribuição.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teoria da Mudança]]
- [[Vanity metrics]]
- [[Investimento de impacto]]
