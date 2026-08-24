---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, dados]
---

# Dados nao estruturados

## Definicao

Dados que nao tem padrao tabular. Diferente do Excel ou de uma tabela do Power BI (ID, nome, CEP, em linhas e colunas), dados nao estruturados nao tem schema fixo.

## Exemplos

- Comentario no LinkedIn.
- Post no Twitter / Threads.
- Like, share, view em rede social.
- Audio (chamada de SAC).
- Imagem (foto de produto, screenshot).
- Texto livre (review de e-commerce, ticket de suporte).
- Video.

## Desafio operacional

Sem padrao, nao da pra fazer consulta SQL direta. O desafio e **cruzar dados nao estruturados** pra gerar insight competitivo. Tecnicas tipicas: NLP, embeddings, topic modeling, classificacao automatica via [[LLM]] ou [[Machine Learning]].

## Aplicacao

Exercicio final da disciplina: pegar comentarios da plataforma EBIT (reviews de e-commerce) — dados nao estruturados — e classificar em categorias via [[IA Generativa]] pra extrair insight de operacoes.

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
- [[IA Generativa]]
- [[Machine Learning]]
