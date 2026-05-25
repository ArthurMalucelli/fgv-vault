---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, normal]
---

# Z de α sobre 2

## Definição

Número de desvios padrão, numa [[Distribuicao normal|normal padrão]] (μ=0, σ=1), tal que a cauda à direita tenha área exatamente α/2.

Aparece como multiplicador em fórmulas de [[Intervalo de Confiança]] e [[Margem de Erro]].

## Cálculo

<pre>
Z_(α/2) = INV.NORM.P.N(1 − α/2)
        = INV.NORM(1 − α/2; 0; 1)
</pre>

A escolha de μ=0 e σ=1 é **artifício pra obter a constante**. Não tem relação com a média e o desvio padrão do problema concreto.

## Como derivar de γ

Sempre o mesmo caminho:

1. γ dado
2. α = 1 − γ
3. α/2 = α dividido por 2
4. Z_(α/2) = `INV.NORM.P.N(1 − α/2)`

## Tabela mental

| γ | α | α/2 | Z_(α/2) |
|---|---|-----|---------|
| 90% | 10% | 5% | **1,645** |
| 95% | 5% | 2,5% | **1,96** |
| 99% | 1% | 0,5% | **2,58** |

Decora os dois primeiros, é o que aparece em 90% dos problemas.

## Intuição visual

Numa normal padrão, marca um ponto à direita da média tal que a área da cauda direita seja exatamente α/2. A distância desse ponto até a média (em unidades de desvio padrão) é Z_(α/2).

Pela regra empírica, pra área de cauda de 2,5% (γ = 95%), o ponto fica a ≈2 desvios padrão. O valor exato é 1,96.

## Erro comum

Achar que como `INV.NORM.P.N` usa média 0 e desvio padrão 1, a fórmula está ignorando os parâmetros do problema. Não. Esse Z é uma constante adimensional que multiplica o σ/√n verdadeiro depois.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Z de alfa sobre 2]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Intervalo de Confiança]]
- [[Margem de Erro]]
- [[Nivel de Confianca]]
- [[Distribuicao normal]]
