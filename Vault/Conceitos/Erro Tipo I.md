---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Erro Tipo I

## Definição

Rejeitar [[Teste de hipotese|H0]] sendo que H0 é verdadeira. Analogia do julgamento: condenar um inocente.

A probabilidade de cometer Erro Tipo I é o próprio alfa (nível de significância) escolhido pro teste.

Pode acontecer por "azar de amostra": uma amostra pequena e não representativa pode levar a rejeitar uma hipótese que, na população inteira, seria verdadeira.

## Fórmula / aplicação

<pre>
P(Erro Tipo I) = alfa
</pre>

Reduzir alfa reduz o risco de Erro Tipo I, mas aumenta o risco de [[Erro Tipo II]] (com tamanho de amostra fixo).

## Onde aparece nas aulas

```dataview
LIST
FROM [[Erro Tipo I]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Erro Tipo II]]
- [[Teste de hipotese]]
- [[Nivel de Confianca]]
- [[Regiao de rejeicao]]
