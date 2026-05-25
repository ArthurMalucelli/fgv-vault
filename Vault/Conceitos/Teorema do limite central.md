---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, distribuicao]
---

# Teorema do Limite Central (TLC)

## Definição

Para amostras suficientemente grandes (convencionalmente n ≥ 30), a [[Distribuicao amostral da media|distribuição amostral da média]] X̄ é aproximadamente [[Distribuicao normal|normal]], **independente da forma da distribuição original da população**.

```
Se X qualquer, com média μ e variância σ², e n ≥ 30
⟹ X̄ ~ aprox. Normal(μ, σ²/n)
```

Se X já é normal, X̄ é exatamente normal para qualquer n.

## Por que é importante

A distribuição da população raramente é conhecida. Sem o TLC, todo problema sobre X̄ exigiria conhecer a distribuição original. Com ele, basta saber μ, σ e n: o resto vira problema de normal.

## Convenção n > 30

Regra prática, não teorema rigoroso. 30 é considerado suficiente para que, qualquer que seja a forma da população (uniforme, exponencial, bimodal com torres e buracos, etc.), o histograma de X̄ já se aproxime bem de uma normal. Acima de 30, considera-se aplicável.

## Fluxograma de decisão

```
X é normal?
├─ Sim ⟶ X̄ ~ N(μ, σ²/n), qualquer n
└─ Não
    ├─ n ≥ 30 ⟶ X̄ ~ aprox. N(μ, σ²/n)  ← TLC
    └─ n < 30 ⟶ não dá pra concluir distribuição de X̄
```

## Aplicação em soma

Para `P(X₁ + X₂ + ... + Xₙ > k)`, divide os dois lados por n:

```
P(ΣXᵢ > k) = P(X̄ > k/n)
```

Agora trabalha com X̄ normal (pelo TLC ou pelo caso normal direto) em vez de soma, que a gente não sabe distribuir.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Distribuicao amostral da media]]
- [[Media amostral]]
- [[Erro padrao]]
- [[Distribuicao normal]]
- [[Inferencia estatistica]]
- [[Simulacao]]
