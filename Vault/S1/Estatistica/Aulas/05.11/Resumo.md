---
materia: Estatistica
data: 2026-05-11
tema: Teorema do Limite Central e distribuição da média amostral
tags: [resumo]
---

# Resumo: Teorema do Limite Central

## Conceitos-chave

| Item | O que é |
|------|---------|
| [[Distribuicao amostral da media]] | Distribuição do X̄ considerando todas as amostras possíveis de tamanho n |
| [[Erro padrao]] | Desvio padrão do X̄, σ/√n. Mede dispersão **entre** médias amostrais |
| S (desvio padrão amostral) | Dispersão **dentro** de uma única amostra. ≠ erro padrão |
| [[Teorema do limite central]] | Para n ≥ 30, X̄ ~ aprox. Normal, independente da distribuição de X |
| Amostra grande | Convenção: n > 30 |
| Truque soma → média | P(ΣXᵢ > k) = P(X̄ > k/n). Divide os dois lados pela constante |
| [[Simulacao]] | Brincar de Deus: fixa a população, sorteia muitas amostras, observa empiricamente |
| Universos paralelos | Cada réplica de amostragem. Cada uma dá um X̄ diferente |

## Fórmulas

**Distribuição amostral de X̄:**

```
E(X̄)    = μ
Var(X̄)  = σ² / n
σ(X̄)    = σ / √n    ← erro padrão
```

**Quando X̄ é normal:**

```
Se X ~ N(μ, σ²)            ⟹  X̄ ~ N(μ, σ²/n)        (sempre, qualquer n)
Se X não-normal e n ≥ 30   ⟹  X̄ ~ aprox. N(μ, σ²/n) (TLC)
Se X não-normal e n < 30   ⟹  não dá pra concluir
```

**Truque para problemas de soma:**

```
P(X₁ + X₂ + ... + Xₙ > k)  =  P(X̄ > k/n)
```

Divide os dois lados por n. Funciona porque dividir os dois lados de uma desigualdade por constante positiva não muda a probabilidade.

**Exponencial (caso especial):**

```
P(X > a) = e^(-a/μ)         ← à direita, fórmula direta
P(X < a) = 1 - e^(-a/μ)     ← à esquerda
σ = μ                        ← desvio padrão = média, sempre
```

**Excel:**

```excel
P(X > a) normal:        = 1 - DIST.NORM(a; μ; σ; 1)
P(X̄ > a) normal:        = 1 - DIST.NORM(a; μ; σ/RAIZ(n); 1)
P(X > a) exponencial:   = EXP(-a/μ)
Sortear índice:         = ALEATÓRIO.ENTRE(1; N)
```

## Exemplos resolvidos

**Bolacha cream cracker (recap):** X ~ N(0.20, 0.05²), n=100, observou X̄=0.24.

```
X̄ ~ N(0.20, 0.05/√100 = 0.005)
0.24 está a 8 desvios padrão de 0.20 → P ≈ 0
```

Conclusão: a média da máquina mudou. Calibrar.

**Ligações exponenciais:** X ~ Exp(μ=σ=5 min).

```
Pergunta 1: P(X > 6)              = EXP(-6/5)  = 0.3012  (30.12%)
Pergunta 2: P(X̄ > 6), n=100        → pelo TLC, X̄ ~ N(5, 0.5)
                                   = 1 - DIST.NORM(6; 5; 0.5; 1)  → minúsculo
```

A média de 100 ligações dificilmente passa de 6, mesmo cada uma tendo 30% de chance individual.

**Elevador:** X ~ N(70, 10²), 7 passageiros, capacidade 500 kg. P(ΣXᵢ > 500)?

```
Truque:   P(ΣXᵢ > 500) = P(X̄ > 500/7 = 71.43)
X̄ ~ N(70, 10/√7)
P(X̄ > 71.43) = 1 - DIST.NORM(500/7; 70; 10/RAIZ(7); 1)
             = 35.27%
```

Quase 1/3 de chance do elevador parar.

## Pegadinhas / pontos de prova

- **Confundir S (interno da amostra) com σ(X̄) (entre amostras).** O primeiro mede dispersão dos pontos dentro da amostra. O segundo é o erro padrão, σ/√n. São coisas diferentes.
- **Usar DIST.NORM em distribuição que não é normal.** Se a aula avisou que é exponencial, uniforme, etc., e n < 30, não pode normalizar.
- **Multiplicar peso individual por n** (ex: 70 × 7 = 490) e tratar como se fossem todos iguais. Erro grave. Cada pessoa sai independente da distribuição; tem que usar o truque da média.
- **TLC só vale para X̄ (média), não pra X individual.** P(X > a) com população não-normal continua precisando da fórmula original (exponencial, uniforme, etc.).
- **Regra do n > 30** é convenção, não teorema rigoroso. Acima disso a aproximação fica boa pra qualquer distribuição com variância finita.
- **No Excel, exponencial à direita é fórmula direta** `EXP(-a/μ)`, ao contrário da normal que precisa do `1 - DIST.NORM(...)`.

## Pra fixar

- [[Teorema do limite central]]
- [[Distribuicao amostral da media]]
- [[Erro padrao]]
- [[Distribuicao exponencial]]
- [[Distribuicao normal]]
- [[Media amostral]]
- [[Simulacao]]

## Próxima aula

Não foi anunciado tema específico. Pelo arco do curso, próximos passos típicos são intervalos de confiança (relatório 3 entrega 01/06) e testes de hipótese, ambos construídos em cima do TLC.
