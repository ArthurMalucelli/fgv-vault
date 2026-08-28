---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, cadeia, sustentabilidade]
---

# Ripple Effect

## Definicao

Efeito cascata. Uma operacao em um ponto da cadeia gera impactos indiretos em outros pontos, que por sua vez geram outros impactos, e assim por diante. O efeito se propaga como onda.

## Exemplo da aula

Demanda crescente por servicos digitais (YouTube, LinkedIn, e-commerce) → data centers operando quase no maximo → consumo massivo de **agua** (refrigeracao) e **energia** → impacto em geracao eletrica e logistica de combustivel → **preco de combustivel sobe** → corrida de aplicativo fica mais cara (ou mais barata, dependendo da direcao do efeito).

A relacao entre "alguem assistir video no YouTube" e "preco da Uber" parece distante, mas o ripple effect captura essa cadeia.

## Por que importa pra operacoes

- **Decisao operacional nunca e isolada.** Mover um botao na cadeia de suprimentos gera ondas em areas que nao apareciam no escopo original.
- **Sustentabilidade vira fator competitivo.** Operacoes que ignoram consumo de agua/energia geram custo indireto pra empresa e pra sociedade.
- **Risk management.** Mapear ripple effects e prerrequisito pra avaliar resiliencia de cadeia.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Big Data]]
- [[Cadeia produtiva]]
- [[ESG]]
