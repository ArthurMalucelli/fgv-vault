---
materia: Estatistica2
data: 2026-08-14
tema: Teste de Hipóteses para Proporções
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Proporcao amostral]] | p̂ = x/n, fração da amostra na categoria de interesse (ex.: pesquisa de intenção de voto). Média de variáveis 0/1: E[p̂] = p, Var(p̂) = p(1 − p)/n |
| [[Distribuicao de Bernoulli]] | Variável dicotômica de um ensaio só: vale 1 com probabilidade p, 0 com 1 − p. Var = p(1 − p). Base da [[Distribuicao binomial|binomial]] |
| [[Estatistica de teste]] pra proporção | z = (p̂ − p₀)/√(p₀(1 − p₀)/n): quantos erros-padrão o p̂ está do p₀ da hipótese |
| [[Teste unicaudal]] | H1 aponta uma direção só ("aumentou?"). Todo o alfa numa cauda |
| [[Valor critico]] unicaudal (5%) | 1,645, não 1,96. [[Regiao de rejeicao]]: de 1,645 a +∞ (cauda direita) |
| [[Erro Tipo I]] | Rejeitar H0 sendo ela verdadeira (azar de amostra atípica). Probabilidade = alfa |
| [[Erro Tipo II]] | Não rejeitar H0 sendo ela falsa |
| Efeito do [[Tamanho da amostra|n]] | n maior (tudo mais igual): erro padrão cai, z sobe, fica mais fácil rejeitar H0 |

## Fórmulas

<pre>
Proporção amostral:
p̂ = x / n

Distribuição de p̂:
E[p̂] = p
Var(p̂) = p(1 − p) / n
σ(p̂) = √( p(1 − p) / n )

Estatística de teste (proporção):
z = (p̂ − p₀) / √( p₀(1 − p₀) / n )
(no denominador entra o p₀ da hipótese, não o p̂ da amostra)

Decisão (unicaudal à direita, alfa = 5%):
- z calculado > 1,645             →  rejeita H0
- valor-p = P(Z > z calc) < 0,05  →  rejeita H0
(critérios equivalentes)

Variância de variável 0/1:
p(1 − p): máxima em p = 0,5, zero em p = 0 ou p = 1
(parábola com concavidade pra baixo)
</pre>

## Exemplo trabalhado em aula: promoção no clube de golfe

- Baseline: 20% de quem joga são mulheres. Clube faz promoção pra atrair mulheres. Funcionou?
- Amostra: n = 400, p̂ = 0,25
- H0: p ≤ 0,20 · H1: p > 0,20 (unicaudal à direita)
- σ(p̂) = √(0,20 × 0,80 / 400) = 0,4/20 = **0,02**
- z = (0,25 − 0,20) / 0,02 = **2,5**
- Crítico (5%, unicaudal) = **1,645**. Como 2,5 > 1,645 (valor-p = P(Z > 2,5) ≈ 0,006 < 0,05): **rejeita H0**
- Interpretação: fortes evidências de que a proporção de mulheres passou de 20%. A promoção funcionou.

## Pegadinhas / pontos de prova

- Unicaudal usa 1,645 (os 5% inteiros numa cauda), não 1,96. O 1,96 é o [[Z de alfa sobre 2]] do bicaudal (2,5% em cada cauda). O professor martelou isso.
- No denominador da estatística entra p₀ da hipótese (0,20 no exemplo), não o p̂ da amostra (0,25).
- Identificar caudalidade pelo enunciado: "aumentou?" ou "diminuiu?" pede unicaudal; "é diferente?" pede bicaudal. O baseline fica no H0, com ≤ ou ≥.
- n maior, tudo mais igual: erro padrão menor, z maior, mais fácil rejeitar H0. Professor: "essa questão a gente gosta de colocar no quiz".
- Interpretação vale nota: rejeitar H0 dá evidência forte de que p > 0,20. NÃO significa que a proporção populacional "é 25%" (0,25 é da amostra). Cobrança explícita: não só calcular, interpretar.
- Variância p(1 − p) é máxima em p = 0,5 e zero nos extremos (todos iguais = sem variabilidade).
- Rejeitar H0 nunca é certeza: sempre existe probabilidade alfa de [[Erro Tipo I]].

## Pra fixar

- [[Proporcao amostral]]
- [[Teste unicaudal]]
- [[Distribuicao de Bernoulli]]
- [[Estatistica de teste]]
- [[Valor critico]]
- [[Valor-p]]
- [[Regiao de rejeicao]]
- [[Erro padrao]]
- [[Erro Tipo I]]
- [[Erro Tipo II]]
- [[Transformacao linear de variavel aleatoria]]
- [[Distribuicao binomial]]

## Próxima aula

- Ter 18/08: testes de qui-quadrado ("essencialmente a mesma lógica"). Sex 21/08: fechamento de qui-quadrado e exercícios.
- Exercício de Excel sobre teste de proporções disponível no eClass, professor pediu pra tentar fazer.
- 1ª Provinha ter 25/08, ref. aulas 2 a 6 (já no calendário): o conteúdo de hoje cai nela.
