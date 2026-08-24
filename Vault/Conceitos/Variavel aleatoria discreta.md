# Variável aleatória discreta

Variável aleatória que assume um número finito (ou enumerável) de valores possíveis, cada um com uma probabilidade associada. Ex: número de camisas vendidas, número de defeitos numa amostra, retorno discretizado em cenários.

A distribuição é descrita pela PMF (probability mass function), também chamada de função de probabilidade: f(x) = P(X = x).

**Propriedades obrigatórias da PMF**

Toda PMF tem que satisfazer dois requisitos:

- f(x) ≥ 0 pra todo x
- soma de f(x) sobre todo o suporte = 1

Se uma probabilidade está faltando, é só achar pela diferença pra fechar 1.

**Como identificar**

A variável conta algo (sucessos, defeitos, eventos) ou pega um valor de uma lista discreta. Se o resultado pode ser qualquer número real num intervalo, é variável contínua, não discreta.

**Operadores associados**

- [[Valor esperado]] (média da distribuição)
- [[Variancia e desvio padrao]] (dispersão)
- [[Funcao de variavel aleatoria]] (transformações, Y = g(X))

**Distribuições discretas comuns**

- [[Distribuicao binomial]] (contagem de sucessos em n ensaios independentes)
- Bernoulli (caso particular da binomial com n=1)
- Poisson (eventos raros num intervalo)
- Geométrica (tempo até o primeiro sucesso)
