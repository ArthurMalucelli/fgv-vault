---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, distribuicao]
---

# Distribuição T de Student

## Definição

Distribuição contínua, parecida com a [[Distribuicao normal|normal padrão]], mas com **caudas mais pesadas** (mais larga). Surge quando você quer construir [[Intervalo de Confiança|intervalo de confiança]] para a média populacional **sem conhecer o σ da população**, usando S (desvio padrão amostral) no lugar.

Formato sino simétrico ao redor de zero, mas com mais massa nas pontas que a normal. Conforme [[Graus de liberdade]] aumentam, ela converge para a normal.

## Por que existe

Quando você troca σ por S na fórmula do IC, está usando um **estimador** no lugar do parâmetro verdadeiro. Essa substituição introduz incerteza extra: o S calculado de cada amostra é diferente. Pra compensar isso, em vez do Z usa-se um número um pouco maior, que vem de uma distribuição com caudas mais largas: a T.

A T "cozinha" o intervalo, alargando ele um pouco pra absorver a incerteza adicional.

## Fórmula / aplicação

IC para média, σ desconhecido (qualquer n):

<pre>
IC_γ% = X̄ ± T_(α/2, n−1) · S / √n
</pre>

Excel:

<pre>
T_(α/2, n−1) = INV.T(1 − α/2; n − 1)
</pre>

**Cuidado**: `INV.T` (com ponto) ≠ `INVT` (sem ponto). São funções diferentes no Excel.

## Comparação com Z (γ = 95%)

| n | T_(2,5%, n−1) | Z_(2,5%) |
|---|---|---|
| 8 | bem maior que 1,96 | 1,96 |
| 25 | 2,064 | 1,96 |
| 36 | 2,03 | 1,96 |
| 120 | 1,98 | 1,96 |
| ∞ | 1,96 | 1,96 |

Pra **n > 50**, T ≈ Z. Pra n pequeno, T é nitidamente maior.

## Quando usar T vs Z

| σ conhecido? | n | Use |
|---|---|---|
| Sim | qualquer | **Z** |
| Não | n > 50 | **Z** (aproxima) ou **T** (correto) |
| Não | n ≤ 50 | **T obrigatório** |

**Regra do Nelson**: *"Se você puser S, ponha T."* Tecnicamente, T é o certo qualquer n.

## Diferença chave em relação à normal

A T depende de **dois parâmetros**: a confiança E os graus de liberdade (= n − 1 pra IC de média). O Z depende só da confiança.

## História do nome

"Student" era o pseudônimo de **William Gosset**, que trabalhava na cervejaria Guinness no início do século XX. A empresa não deixava funcionários publicarem com nome próprio, então ele publicou os trabalhos sobre essa distribuição com o pseudônimo "Student". Daí "T de Student".

## Onde aparece nas aulas

```dataview
LIST
FROM [[Distribuicao T de Student]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Intervalo de Confiança]]
- [[Margem de Erro]]
- [[Graus de liberdade]]
- [[Distribuicao normal]]
- [[Z de alfa sobre 2]]
- [[Distribuicao amostral da media]]
- [[Erro padrao]]
- [[Tamanho da amostra]]
- [[Teorema do limite central]]
