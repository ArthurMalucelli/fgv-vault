---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, amostragem]
---

# Proporção Amostral

## Definição

Fração da amostra que pertence à categoria de interesse: p̂ = x/n, onde x é o número de "sucessos". É a média de n variáveis 0/1 (ver [[Distribuicao de Bernoulli]]) e serve de estimador da proporção populacional p (ex.: pesquisa de intenção de voto estimando a proporção de eleitores de um candidato). Para n grande, distribui-se aproximadamente como normal.

## Fórmula / aplicação

<pre>
p̂ = x / n
E[p̂] = p
Var(p̂) = p(1 − p) / n
σ(p̂) = √( p(1 − p) / n )

Estatística de teste (H0: p = p₀):
z = (p̂ − p₀) / √( p₀(1 − p₀) / n )
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Proporcao amostral]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Media amostral]]
- [[Distribuicao de Bernoulli]]
- [[Distribuicao binomial]]
- [[Estatistica de teste]]
- [[Erro padrao]]
- [[Teste de hipotese]]
