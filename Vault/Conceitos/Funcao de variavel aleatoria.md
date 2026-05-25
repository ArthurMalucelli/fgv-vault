# Função de variável aleatória

Quando uma nova variável Y é definida como Y = g(X), onde g é qualquer função (linear, não-linear, condicional, com quebras). Y também é variável aleatória, e a sua distribuição é induzida pela de X.

## Caso geral (qualquer g)

Para cada valor possível de X, calcula g(X) → valor de Y. As probabilidades de Y são as mesmas de X (P(Y = g(x)) = P(X = x), respeitando colapsos quando g leva valores diferentes de X ao mesmo Y).

Para calcular [[Valor esperado|E(Y)]]:

<pre>
E(Y) = Σ g(x) · P(X = x)
</pre>

Não computa E(X) primeiro e aplica g em cima. Na maioria dos casos, **E(g(X)) ≠ g(E(X))**.

## Caso linear (atalho)

Se g é linear, Y = a + bX, dá pra usar as fórmulas curtas. Ver [[Transformacao linear de variavel aleatoria]] pra fórmulas específicas e pegadinhas.

## Caso não-linear (cuidado)

Para g não-linear, a igualdade E(g(X)) = g(E(X)) **não vale**. Exemplos:

- E(X²) ≠ [E(X)]² (essa diferença é exatamente a variância: Var(X) = E(X²) - [E(X)]²)
- E(1/X) ≠ 1/E(X)
- E(log(X)) ≠ log(E(X))

A direção do "≠" tem nome: desigualdade de Jensen. Não é prova de cálculo, é só pra ter no radar que linearizar uma transformação não-linear é erro.

## Caso com regra condicional

Quando g tem quebras (ex: aplica desconto só acima de certo X), tem que tratar caso a caso. Computa Y para cada x do suporte e pondera.

Exemplo da Lista 3 (camisas com desconto a partir de 3 unidades):

| X | Y                      |
|---|------------------------|
| 0 | 0                      |
| 1 | 1 · 35 = 35            |
| 2 | 2 · 35 = 70            |
| 3 | 3 · 35 · 0,8 = 84      |
| 4 | 4 · 35 · 0,8 = 112     |

E(Y) sai pela ponderação Σ Y(x) · P(X=x), não dá pra simplificar como E(X) · 35.

## Excel pra caso condicional

Cria uma coluna Y(X) usando SE para a quebra:

<pre>
C2: =SE(A2>=3; A2*35*0,8; A2*35)
E(Y): =SOMARPRODUTO(C2:Cn; B2:Bn)
</pre>

## Conceitos relacionados

- [[Valor esperado]]
- [[Variancia e desvio padrao]]
- [[Transformacao linear de variavel aleatoria]] (caso linear, atalho)
