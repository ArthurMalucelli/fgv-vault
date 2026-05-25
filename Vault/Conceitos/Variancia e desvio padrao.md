# Variância e desvio padrão

Medidas de dispersão de uma [[Variavel aleatoria discreta]]: o quanto os valores se espalham em torno do [[Valor esperado]]. Em finanças, é a definição operacional clássica de **risco**.

**Definição**

<pre>Var(X) = E[(X - E(X))^2]</pre>

A variância é o valor esperado do desvio quadrático em relação à média.

**Fórmula curta (mais prática pra cálculo)**

<pre>Var(X) = E(X^2) - [E(X)]^2</pre>

Onde E(X²) = Σ x² · P(X = x).

Essa é a forma que se usa em prova: calcula E(X), calcula E(X²) na mesma tabela, subtrai o primeiro ao quadrado do segundo.

**Desvio padrão**

<pre>DP(X) = sqrt(Var(X))</pre>

DP tem a mesma unidade que X (variância está em unidade ao quadrado, o que é estranho de interpretar).

**Excel**

<pre>
E(X^2):  =SOMARPRODUTO(coluna_x^2; coluna_prob)
Var:     =E(X^2) - E(X)^2
DP:      =RAIZ(Var)
</pre>

**Propriedades**

Variância de transformação linear (decorar):

<pre>
Var(aX + b) = a^2 · Var(X)
DP(aX + b)  = |a| · DP(X)
</pre>

A constante aditiva (b) some, deslocar tudo não muda dispersão. A constante multiplicativa (a) entra ao quadrado na variância.

Variância de soma:

<pre>
Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y)
Var(X + Y) = Var(X) + Var(Y)             (se X e Y independentes)
</pre>

Ver [[Independencia]] e [[Transformacao linear de variavel aleatoria]].

**Interpretação em finanças**

Dois ativos com mesmo retorno esperado mas DPs diferentes: o de menor DP é menos arriscado. Comparar só pela média esconde risco. DP é a base do Sharpe ratio (retorno excedente dividido por DP).

**Pegadinha clássica**

Em prova, a fonte de erro mais comum em transformação linear é:
- esquecer que **b** (aditivo) some na variância
- esquecer de elevar **a** (multiplicativo) ao quadrado

As duas armadilhas geralmente aparecem nas alternativas erradas.
