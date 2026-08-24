# Valor esperado

Média ponderada dos valores que uma [[Variavel aleatoria discreta]] pode assumir, com pesos iguais às probabilidades. Equivalente ao "centro de massa" da distribuição. Notação: E(X), µ, ou ⟨X⟩.

**Fórmula (caso discreto)**

<pre>E(X) = Σ x · P(X = x)</pre>

Soma sobre todo o suporte de X.

**Interpretação**

Se você repetir o experimento muitas vezes, a média dos resultados converge pro valor esperado (lei dos grandes números). Em finanças, o valor esperado de um retorno é exatamente o que se chama de retorno esperado de um cenário probabilístico.

Importante: o valor esperado nem sempre é um valor que X pode assumir. Ex: dado de 6 faces tem E = 3,5, valor que o dado nunca dá.

**Excel**

<pre>=SOMARPRODUTO(coluna_x; coluna_prob)</pre>

**Propriedades**

Linearidade da esperança (mesmo sem independência):

<pre>
E(aX + b) = a · E(X) + b
E(X + Y)  = E(X) + E(Y)
</pre>

Pra produto, só vale com independência:

<pre>E(X · Y) = E(X) · E(Y)  (se X e Y independentes)</pre>

**Cuidado**

Em geral, E(g(X)) ≠ g(E(X)) quando g é não-linear. Pra calcular E de uma transformação não-linear, tem que aplicar g a cada x e ponderar. Ver [[Funcao de variavel aleatoria]].

**Conceitos relacionados**

- [[Variancia e desvio padrao]] (dispersão em torno do valor esperado)
- [[Transformacao linear de variavel aleatoria]] (caso especial fácil)
