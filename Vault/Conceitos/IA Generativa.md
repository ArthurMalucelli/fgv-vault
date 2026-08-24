---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, ia, tecnologia]
---

# IA Generativa

## Definicao

Algoritmos baseados em [[LLM]] (large language models) que **criam conteudo novo** a partir de interacao com o usuario ou de forma autonoma.

Conteudo gerado: texto, codigo, imagem, audio, video, dados sinteticos.

## Diferenca pra IA "classica"

- IA classica: classifica, prediz, otimiza sobre dados existentes (regressao, classificacao, clusterizacao).
- IA generativa: **gera** output novo que nao existia antes, alinhado a um prompt ou contexto.

## Modos de operacao

- **Interativo**: usuario manda prompt, IA responde, conversa iterativa.
- **Autonomo**: [[Agente de IA]] executa tarefa multi-step sem prompt-resposta passo a passo.

## Aplicacao em operacoes

Exercicio final da disciplina: usar GenAI (gratuita ou paga) pra classificar comentarios EBIT (e-commerce) em categorias, contar frequencia, e gerar recomendacao estrategica de operacoes.

Outros usos: gerar codigo pra analytics, resumir relatorios, criar simulacoes, escrever postagens, gerar imagens de marketing.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[LLM]]
- [[Agente de IA]]
- [[Machine Learning]]
- [[Dados nao estruturados]]
