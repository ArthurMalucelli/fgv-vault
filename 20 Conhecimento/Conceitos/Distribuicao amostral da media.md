---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, distribuicao]
---

# Distribuição amostral da média

## Definição

Distribuição de probabilidade da [[Media amostral|média amostral]] X̄, considerando todas as amostras de tamanho n que poderiam ser tiradas de uma população. É a base de toda a [[Inferencia estatistica]].

Conceitualmente: imagina repetir a [[Amostragem]] infinitas vezes, calculando X̄ em cada uma. O histograma dessas X̄ converge pra essa distribuição.

## Parâmetros

Independente da forma da distribuição da população, valem:

<pre>
E(X̄)   = μ                   ← centrada na média populacional
Var(X̄) = σ² / n              ← variância cai com n
DP(X̄)  = σ / √n              ← [[Erro padrao]]
</pre>

## Caso normal: forma exata

Se a população X é normal, X̄ é exatamente normal pra qualquer n:

```
X ~ N(μ, σ²)   ⟹   X̄ ~ N(μ, σ²/n)
```

Mesma média, mesma forma de sino, só mais concentrada (mais "magrinha"). Quanto maior n, mais magra.

## Caso geral: Teorema do Limite Central

Se X **não** é normal, X̄ ainda é aproximadamente normal pra n suficientemente grande (regra prática: n ≥ 30). Esse é o resultado conhecido como Teorema do Limite Central, vem em aulas posteriores.

## Comparação visual: X vs X̄

| Característica | X (variável original) | X̄ (média amostral) |
|---|---|---|
| Média | μ | μ |
| Variância | σ² | σ² / n |
| DP | σ | σ / √n |
| Forma (se X é normal) | normal | normal |

A curva de X̄ tem o mesmo centro da curva de X, mas é mais alta e mais estreita. Quanto maior n, mais concentrada perto de μ.

## Por que isso é a base da inferência

Toda afirmação probabilística sobre estimativas (intervalos de confiança, testes de hipótese, p-valores) é construída em cima dessa distribuição. Quando você diz "tenho 95% de confiança que μ está em [a, b]", está usando a distribuição amostral pra calibrar essa confiança.

## Pegadinha

Se a pergunta é sobre uma única observação, você usa σ. Se é sobre a média de n observações, você usa σ/√n. O erro mais comum em prova é confundir isso e calcular probabilidade individual quando a pergunta é sobre média amostral.

## Excel

<pre>
P(a ≤ X̄ ≤ b) = DIST.NORM.N(b; μ; σ/RAIZ(n); 1) − DIST.NORM.N(a; μ; σ/RAIZ(n); 1)
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Distribuicao amostral da media]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Media amostral]]
- [[Erro padrao]]
- [[Distribuicao normal]]
- [[Inferencia estatistica]]
- [[Amostragem]]
