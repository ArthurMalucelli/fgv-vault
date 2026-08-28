---
materia: Estatistica
data: 2026-05-06
tema: Inferência estatística e distribuição amostral da média
tags: [resumo]
---

# Resumo: distribuição amostral da média

Terceiro bloco do curso: [[Inferencia estatistica]]. Antes era probabilidade, agora a gente usa amostra pra estimar parâmetro populacional.

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Inferencia estatistica]] | Tirar conclusões sobre a população a partir de uma [[Amostragem\|amostra]] |
| [[Parametros populacionais]] | μ, σ², p — valores reais da população, geralmente desconhecidos |
| [[Estatistica amostral]] | X̄, s², p̂ — calculados a partir da amostra, usados pra estimar parâmetros |
| [[Media amostral]] | X̄ ("X-barra" ou "X-chapéu"): média de uma amostra de tamanho n |
| [[Distribuicao amostral da media]] | Distribuição do X̄ se eu pudesse repetir a amostragem infinitas vezes |
| [[Erro padrao]] | Desvio padrão da estatística amostral (no caso da média, σ/√n) |

## Fórmulas

<pre>
E(X̄)   = μ                     ← X̄ é não-viesado
Var(X̄) = σ² / n                ← variância da média cai com n
DP(X̄)  = σ / √n                ← erro padrão

Se X ~ N(μ, σ²),
então X̄ ~ N(μ, σ²/n)            ← caso normal: X̄ também é normal
</pre>

Atenção à hierarquia de "desvios padrão":

<pre>
σ        ← DP da variável X (dispersão dos indivíduos na população)
σ/√n     ← erro padrão (DP da X̄, dispersão de médias entre amostras)
s        ← DP amostral interno (calculado em UMA amostra)
</pre>

## Excel (caso normal)

<pre>
P(a ≤ X̄ ≤ b) = DIST.NORM.N(b; μ; σ/RAIZ(n); 1) − DIST.NORM.N(a; μ; σ/RAIZ(n); 1)
</pre>

Pegadinha: em DIST.NORM.N o terceiro argumento é o **desvio padrão** σ. Pra distribuição amostral da média, passa σ/√n. Não passa σ². Não passa σ. Passa σ/√n.

## Pegadinhas / pontos de prova

1. **σ vs σ/√n.** Erro mais comum: usar σ no lugar de σ/√n quando a pergunta é sobre X̄. Sempre olhar se a pergunta é "qual a probabilidade de **uma** observação" ou "qual a probabilidade da **média de n**".

2. **A variância interna da amostra (s²) NÃO entra na fórmula de Var(X̄).** A variância de X̄ depende de σ² (variância populacional) e n (tamanho da amostra), nada mais. s² aparece em outros lugares (intervalos de confiança), não aqui.

3. **A média não muda, só o desvio.** E(X̄) = μ. A média populacional e a média da distribuição amostral são iguais. A diferença é só na dispersão.

4. **Quanto maior n, menor o erro padrão.** Faz sentido intuitivo: amostras maiores estimam melhor a média. Quantitativamente, cai com √n, não com n. Pra reduzir erro padrão pela metade, precisa quadruplicar a amostra.

5. **"Pasteurização" das médias.** Valores extremos individuais somem na média. Por isso a curva de X̄ é mais magrinha que a de X.

6. **Caso normal só.** A regra "X̄ ~ N(μ, σ²/n)" vale exatamente quando X já é normal. Pra outras distribuições, a normalidade de X̄ vem do Teorema do Limite Central, vem nas próximas aulas.

## Comparação numérica (exemplo do telefonema)

T ~ N(μ=8, σ=2). Faixa fixa: 7,8 a 8,2 (largura 0,4 minutos = 0,2 de cada lado).

| Quantidade | DP relevante | Z da faixa | P |
|---|---|---|---|
| Uma chamada (T) | σ = 2 | ± 0,1 | ≈ 7,97% |
| Média de 25 chamadas (T̄) | σ/√25 = 0,4 | ± 0,5 | ≈ 38,3% |

Mesma faixa, distribuição mais concentrada, probabilidade maior. Esse é o ponto-chave.

## Pra fixar

- [[Inferencia estatistica]]
- [[Amostragem]]
- [[Media amostral]]
- [[Erro padrao]]
- [[Distribuicao amostral da media]]
- [[Parametros populacionais]]
- [[Estatistica amostral]]

## Próxima aula

Continua amostragem, mas conceitual com gincana. Provavelmente puxa pro Teorema do Limite Central depois.
