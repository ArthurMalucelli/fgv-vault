# Independência

Dois eventos A e B são independentes se a ocorrência de um não muda a probabilidade do outro. Formalmente:

<pre>
P(A ∩ B) = P(A) · P(B)
</pre>

Equivalente: P(A | B) = P(A), e P(B | A) = P(B). A informação sobre B não atualiza a probabilidade de A.

## Por que importa

Independência é o que permite multiplicar probabilidades. Sem independência, a fórmula correta usa probabilidade condicional:

<pre>
P(A ∩ B) = P(A | B) · P(B)
</pre>

Erro clássico de prova: aplicar P(A) · P(B) em situação dependente. Sempre checar se a independência é razoável antes de multiplicar.

## Casos típicos onde independência é válida

- ensaios da [[Distribuicao binomial]] (por construção)
- duas tarefas executadas separadamente, sem influência uma na outra
- amostras com reposição
- eventos em experimentos físicos diferentes

## Casos típicos onde NÃO é válida

- amostras sem reposição (a primeira retirada muda a composição da pingela)
- eventos correlacionados no tempo (preço de hoje vs amanhã)
- variáveis ligadas por uma causa comum

## Variáveis aleatórias independentes

Para [[Variavel aleatoria discreta|variáveis aleatórias]] X e Y serem independentes:

<pre>
P(X = x, Y = y) = P(X = x) · P(Y = y)  para todo (x, y)
</pre>

Consequências importantes em independência de VAs:

<pre>
E(X · Y)   = E(X) · E(Y)
Var(X + Y) = Var(X) + Var(Y)
</pre>

A primeira é só com independência. A segunda é só com independência (em geral, Var(X+Y) = Var(X) + Var(Y) + 2·Cov(X,Y), e Cov = 0 quando independentes). [[Variancia e desvio padrao]] tem mais detalhes.

A esperança da soma E(X+Y) = E(X) + E(Y) **sempre** vale, com ou sem independência.

## Exemplo prático

Duas tarefas independentes, cada uma com 45% de chance de terminar em <3 dias. Probabilidade de ambas terminarem em <3 dias:

P(ambas) = 0,45 · 0,45 = 0,2025
