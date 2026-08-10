---
materia: Estatistica2
data: 2026-08-07
tema: Testes de Hipótese e Distribuições Z e T
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Teste de hipotese]] | Procedimento pra avaliar se a amostra dá evidência suficiente pra rejeitar uma afirmação (H0) sobre a população |
| H0 (hipótese nula) | Afirmação inicial, presumida verdadeira até prova em contrário (analogia: réu inocente) |
| H1 (hipótese alternativa) | O que você quer verificar se há evidência pra sustentar |
| [[Estatistica de teste]] | Quantos erros-padrão o valor observado está distante do valor hipotético |
| [[Valor-p]] | Probabilidade de observar um resultado tão ou mais extremo que o observado, supondo H0 verdadeira |
| [[Valor critico]] | Ponto de corte (em Z ou T) que delimita a [[Regiao de rejeicao]], dado alfa |
| [[Erro Tipo I]] | Rejeitar H0 sendo H0 verdadeira. Probabilidade = alfa |
| [[Erro Tipo II]] | Não rejeitar H0 sendo H0 falsa. Probabilidade = beta |
| [[Graus de liberdade]] | n - 1. Parâmetro extra da [[Distribuicao T de Student]], além de média e variância |
| [[Distribuicao T de Student]] vs Z | T pra amostra pequena (regra prática: n ≤ 30, ou sempre que σ populacional é desconhecido); Z pra n > 30 ou σ conhecido |

## Fórmulas

<pre>
Padronização (Z):
Z = (valor observado − média) / desvio padrão

Estatística de teste (T, uma média, σ desconhecido):
T = (X̄ − μ₀) / (S / √n)

Graus de liberdade:
gl = n − 1

Regra de decisão bicaudal, alfa dado:
- Se |T calculado| > T crítico (α/2, gl)  →  rejeita H0
- Se valor-p < alfa                        →  rejeita H0
(os dois critérios são equivalentes)
</pre>

## Roteiro fixo pra resolver qualquer exercício

1. Define H0 e H1.
2. Define alfa (nível de significância).
3. Calcula a estatística de teste (Z ou T).
4. Acha o valor crítico ou o valor-p.
5. Compara e decide: rejeita ou não rejeita H0.

## Exemplo trabalhado em aula: tempo de atendimento

Histórico: 10 min por atendimento. Amostra de 12 atendimentos (dados do exercício da aula):
9.7, 10.2, 10.4, 9.9, 10.1, 10.5, 9.8, 10.3, 10.0, 10.2, 10.4, 10.1

- H0: μ = 10 · H1: μ ≠ 10 (bicaudal)
- X̄ = 10,13
- S ≈ 0,25 · erro padrão = S/√n ≈ 0,07
- gl = 11
- T calculado = (10,13 − 10) / 0,07 ≈ **1,85**
- T crítico (α = 5%, bicaudal, gl = 11) ≈ **2,20**
- Como 1,85 < 2,20 (valor-p ≈ 0,09 > 0,05): **não rejeita H0**

Interpretação: a amostra não dá evidência suficiente de que a média mudou de 10 minutos.

## Pegadinhas / pontos de prova

- Nível de confiança maior (99%) não é "mais seguro" de forma absoluta: alarga o intervalo, reduz o poder de rejeitar H0, aumenta o risco de Erro Tipo II.
- Erro Tipo I e Erro Tipo II são inversamente relacionados: reduzir um (com n fixo) tende a aumentar o outro.
- alfa = P(Erro Tipo I), não é a probabilidade de H0 ser falsa.
- Amostra pequena e não representativa pode gerar rejeição errada de H0 (Erro Tipo I por "azar de amostra") mesmo quando H0 é verdadeira.
- Comparar valor-p com alfa e comparar estatística de teste com valor crítico são caminhos equivalentes, chegam na mesma decisão.
- Teste bicaudal com alfa de 5%: cada cauda fica com 2,5%, não 5% cada.
- Regra prática Z vs T: sempre que usa S (desvio padrão amostral) no lugar de σ, o correto tecnicamente é T; Z só é exatamente correto com σ populacional conhecido (n > 30 é aproximação aceitável).

## Pra fixar

- [[Teste de hipotese]]
- [[Estatistica de teste]]
- [[Valor-p]]
- [[Valor critico]]
- [[Erro Tipo I]]
- [[Erro Tipo II]]
- [[Graus de liberdade]]
- [[Regiao de rejeicao]]
- [[Distribuicao T de Student]]
- [[Z de alfa sobre 2]]
- [[Nivel de Confianca]]

## Próxima aula

Não mencionado explicitamente pelo professor nesta aula.
