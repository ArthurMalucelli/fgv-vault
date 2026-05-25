---
tipo: conceito
materias: [IntroducaoAGestao]
tags: [conceito, gestao, metricas]
---

# Vanity metrics

## Definição

Indicadores que parecem mostrar progresso, mas não respondem se o objetivo final está sendo atingido. Tipicamente são contagens de atividade ou alcance (número de seguidores, downloads, pessoas atendidas, posts feitos), em vez de mudança no resultado-fim (receita gerada, comportamento alterado, vida transformada).

Comum no terceiro setor (vide [[Teoria da Mudança]]) confundir output com outcome: "atendemos X mil pessoas" é vanity metric se a pergunta era "quantas saíram da pobreza".

## Fórmula / aplicação

Teste de vanity metric:
1. A métrica pode subir sem que o objetivo-fim avance? Se sim, é vanity.
2. A métrica é acionável (mudar o que se faz amanhã)? Se não, é vanity.
3. A métrica tem benchmarking (comparação com grupo controle)? Se não, vai inflar atribuição.

Antídoto: usar métricas de outcome, com grupo de comparação, e separar explicitamente input/output/outcome/impacto na comunicação.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teoria da Mudança]]
- [[Atribuição de impacto]]
