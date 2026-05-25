# Transformação linear de variável aleatória

Quando uma nova variável Y é definida como Y = a + bX, com a e b constantes. Caso especial fácil de [[Funcao de variavel aleatoria]] em que as fórmulas de [[Valor esperado]] e [[Variancia e desvio padrao]] passam direto.

## Fórmulas

<pre>
E(a + bX) = a + b · E(X)
Var(a + bX) = b² · Var(X)
DP(a + bX)  = |b| · DP(X)
</pre>

## Intuição

**Esperança**: a esperança é linear, distribui sobre soma e escala. Faz sentido: deslocar tudo por **a** desloca a média por **a**, multiplicar tudo por **b** multiplica a média por **b**.

**Variância**: a constante aditiva (a) **some**. Deslocar a distribuição inteira não muda o quanto ela se espalha em torno da própria média. Já o coeficiente multiplicativo (b) **entra ao quadrado**, porque variância tem unidade ao quadrado (se X está em reais, Var(X) está em reais²).

**Desvio padrão**: como DP é a raiz da variância, o b sai da raiz como módulo (raiz de b² é |b|, não b). Em geral o b é positivo em problema de prova, então sai sem o módulo.

## Pegadinhas clássicas em prova

Erros comuns que aparecem nas alternativas erradas de múltipla escolha:

- esquecer que a constante aditiva **a** some na variância (gente coloca a no resultado)
- esquecer de elevar **b** ao quadrado na variância (usa só b)
- aplicar quadrado na variância mas não no desvio padrão (b² entra na variância, mas no DP é |b|, não b²)

## Aplicação típica

Modelo macro de consumo: C = a + b · Y, onde Y é renda disponível (variável aleatória). Dado E(Y) e Var(Y), pede E(C) e Var(C).

C = 1,5 + 0,8 · Y, com E(Y) = 100, Var(Y) = 10.

E(C) = 1,5 + 0,8 · 100 = 81,5
Var(C) = 0,8² · 10 = 0,64 · 10 = 6,4

## Cuidado

Se a transformação for **não-linear** (ex: Y = X², Y = log(X), Y = preço · indicadora), essas fórmulas de atalho **não valem**. Tem que tratar como [[Funcao de variavel aleatoria]] geral, computando Y caso a caso e ponderando pelas probabilidades de X.

## Conceitos relacionados

- [[Valor esperado]]
- [[Variancia e desvio padrao]]
- [[Funcao de variavel aleatoria]]
