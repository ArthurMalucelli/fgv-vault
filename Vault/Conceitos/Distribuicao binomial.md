# Distribuição binomial

Distribuição discreta que conta o número de sucessos em **n** ensaios independentes, todos com a mesma probabilidade **p** de sucesso. Notação: X ~ Binomial(n, p).

## Como reconhecer

Quatro condições que precisam estar todas presentes:

- número fixo de ensaios n
- cada ensaio tem só dois resultados (sucesso/fracasso)
- probabilidade p de sucesso é a mesma em todo ensaio
- ensaios são [[Independencia|independentes]]

Se algum requisito quebrar (ex: probabilidade muda, ou ensaios dependentes), não é binomial. O caso clássico de "amostra sem reposição" gera dependência: para amostras pequenas relativas à população, ainda dá pra usar binomial como aproximação.

## PMF

<pre>
P(X = k) = C(n,k) · p^k · (1-p)^(n-k)

onde C(n,k) = n! / (k! · (n-k)!) é o coeficiente binomial
</pre>

## Esperança e variância

<pre>
E(X)  = n · p
Var(X) = n · p · (1-p)
DP(X)  = sqrt(n · p · (1-p))
</pre>

## Excel

| Objetivo | Fórmula |
|----------|---------|
| P(X = k) pontual | <pre>=DISTR.BINOM.N(k; n; p; FALSO)</pre> |
| P(X ≤ k) acumulada (CDF) | <pre>=DISTR.BINOM.N(k; n; p; VERDADEIRO)</pre> |
| P(X ≥ k) | <pre>=1 - DISTR.BINOM.N(k-1; n; p; VERDADEIRO)</pre> |
| Quantil k tal que P(X ≤ k) ≥ α | <pre>=INV.BINOM(n; p; α)</pre> |

## Truques de prova

**Complemento**: P(X ≥ k) é trabalhoso de somar. Calcula 1 menos a CDF até k-1.

**Sanity check de E(X)**: se a pergunta dá um valor muito acima ou abaixo de n·p, a probabilidade tem que ser baixa. Isso ajuda a eliminar alternativas absurdas em múltipla escolha.

**Aproximação normal**: para n grande e p não muito perto de 0 ou 1 (regra prática: n·p > 5 e n·(1-p) > 5), a Binomial(n, p) é bem aproximada por Normal(np, np(1-p)). Útil quando Excel não está disponível e o cálculo manual da binomial é impraticável.

## Conceitos relacionados

- [[Variavel aleatoria discreta]]
- [[Valor esperado]]
- [[Variancia e desvio padrao]]
- [[Independencia]]
- Bernoulli (caso particular: n = 1)
