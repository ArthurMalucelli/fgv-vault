---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, lean, qualidade]
---

# Cinco Porques

## Definicao

Ferramenta de analise de causa raiz desenvolvida na Toyota. Diante de um problema, perguntar **"por que?"** sucessivamente (em geral cinco vezes) ate chegar a uma causa **sistemica**, nao sintomatica.

## Como aplicar

1. Definir o problema de forma objetiva e mensuravel.
2. Perguntar "por que isso acontece?".
3. Sobre a resposta, perguntar "por que isso acontece?" de novo.
4. Repetir ate atingir uma causa que, se atacada, impede a recorrencia do problema.
5. O numero 5 e regra de bolso, nao lei. Pode ser 3, pode ser 7.

## Relacao com Ishikawa

- [[Ishikawa]] e **qualitativo e amplo**: mapeia varias categorias de causas em arvore (6M: maquina, metodo, material, mao-de-obra, medida, meio-ambiente).
- Cinco Porques e **vertical e profundo**: desce em uma cadeia causal especifica ate o nivel sistemico.

Os dois se complementam: usar Ishikawa pra abrir o leque, escolher uma causa relevante (priorizada por [[Pareto]]) e descer com 5 Porques.

## Cuidados

- Parar em causa pessoal ("Joao errou") e armadilha. Empurrar mais um nivel ("por que o processo permitiu o erro do Joao?").
- Confirmar com dados, nao so com opiniao.
- Causa raiz boa aponta pra mudanca de **design de processo**, nao de pessoa.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Ishikawa]]
- [[Pareto]]
- [[PDCA]]
- [[Kaizen]]
- [[5W2H]]
