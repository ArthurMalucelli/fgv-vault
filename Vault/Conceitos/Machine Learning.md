---
tipo: conceito
materias: [OperacoesParaCompetitividade, Estatistica, Programacao]
tags: [conceito, dados, tecnologia, analytics]
---

# Machine Learning

## Definicao

Subarea da [[Inteligencia Artificial]] em que algoritmos **aprendem padroes a partir de dados** ao inves de seguirem regras programadas explicitamente. Modelo melhora com mais dados.

## Tipos

- **Supervisionado**: aprende com dados rotulados (regressao, classificacao). Ex: prever preco de imovel, classificar email como spam.
- **Nao supervisionado**: encontra estrutura em dados sem rotulo (clusterizacao, reducao de dimensao). Ex: segmentar clientes.
- **Por reforco**: aprende por tentativa e erro com recompensa. Ex: jogar Go, otimizar logistica.
- **Deep learning**: redes neurais profundas. Base de [[LLM]]s.

## Onde se encaixa em Big Data Analytics

Junto com **estatistica** (regressao, series temporais, inferencia) e **pesquisa operacional** (otimizacao), forma o tripe de tecnicas do [[Big Data Analytics]].

## Aplicacao em operacoes

- Previsao de demanda.
- Deteccao de anomalia em processo (qualidade).
- Otimizacao de rota.
- Manutencao preditiva.
- Segmentacao de cliente.
- Pricing dinamico.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Big Data]]
- [[Big Data Analytics]]
- [[LLM]]
- [[IA Generativa]]
