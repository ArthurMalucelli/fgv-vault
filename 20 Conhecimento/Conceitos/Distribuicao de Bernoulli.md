---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, probabilidade, distribuicao]
---

# Distribuição de Bernoulli

## Definição

Distribuição de uma variável dicotômica (0 ou 1) num único ensaio: vale 1 ("sucesso") com probabilidade p e 0 com probabilidade 1 − p. É o bloco básico da [[Distribuicao binomial]] (soma de n Bernoullis independentes) e da [[Proporcao amostral]] (média de n Bernoullis).

## Fórmula / aplicação

<pre>
E[X] = p
Var(X) = p(1 − p)

Variância máxima em p = 0,5; zero em p = 0 ou p = 1
(p(1 − p) é uma parábola com concavidade pra baixo)
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Distribuicao de Bernoulli]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Distribuicao binomial]]
- [[Proporcao amostral]]
- [[Variancia e desvio padrao]]
- [[Valor esperado]]
