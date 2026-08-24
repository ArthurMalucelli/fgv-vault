---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, amostragem]
---

# Média amostral

## Definição

Média aritmética de uma amostra de tamanho n. Notação: X̄ (lê-se "X-barra" ou "X-chapéu"). É a [[Estatistica amostral]] mais usada, e a estimadora natural da média populacional μ.

```
X̄ = (X₁ + X₂ + ... + Xₙ) / n
```

Onde X₁, ..., Xₙ são as observações da amostra. Como cada Xᵢ é uma variável aleatória, X̄ também é variável aleatória.

## Esperança e variância de X̄

Esses dois resultados são o coração da inferência:

<pre>
E(X̄)   = μ                   ← X̄ é estimador não-viesado
Var(X̄) = σ² / n              ← variância cai com n
DP(X̄)  = σ / √n              ← chamado de [[Erro padrao]]
</pre>

A demonstração usa linearidade da esperança e independência das observações:

<pre>
E(X̄) = E((X₁+...+Xₙ)/n) = (1/n)·n·μ = μ
Var(X̄) = Var((X₁+...+Xₙ)/n) = (1/n²)·n·σ² = σ²/n
</pre>

## Intuição: pasteurização dos extremos

Por que Var(X̄) < Var(X)?

Quando você tira a média de n observações, valores extremos se diluem. Se sortear três alunos e cair um jogador de basquete, a média dos três sobe um pouco, mas é puxada de volta pelos outros dois. A média individual é menos sensível a outliers que a observação individual.

Quanto maior n, mais "pasteurizado" fica, e menor a variabilidade da X̄.

## Caso normal

Se a [[Populacao|população]] X é normal, a média amostral X̄ também é normal:

```
X ~ N(μ, σ²)   ⟹   X̄ ~ N(μ, σ²/n)
```

Mesma média, variância dividida por n. Pra outras distribuições, o resultado análogo vem do Teorema do Limite Central.

## Excel

<pre>
DP(X̄) = σ / √n
P(a ≤ X̄ ≤ b) = DIST.NORM.N(b; μ; σ/RAIZ(n); 1) − DIST.NORM.N(a; μ; σ/RAIZ(n); 1)
</pre>

Pegadinha: o terceiro argumento de DIST.NORM.N é o desvio padrão. Pra X̄, passa σ/√n, NÃO σ.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Media amostral]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Distribuicao amostral da media]]
- [[Erro padrao]]
- [[Estatistica amostral]]
- [[Distribuicao normal]]
- [[Valor esperado]]
- [[Variancia e desvio padrao]]
