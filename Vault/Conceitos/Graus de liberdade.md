---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia]
---

# Graus de liberdade

## Definição

Parâmetro de várias distribuições (T, χ², F) que mede o número de "valores independentes" que entram no cálculo de uma estatística amostral. Intuição informal: **quantas observações livres você teve depois de descontar restrições impostas pelos parâmetros que você estimou da própria amostra**.

Para [[Distribuicao T de Student|IC de média]] usando S:

<pre>
gl = n − 1
</pre>

O "−1" sai do fato de que pra calcular o S você já usou o X̄ da amostra (uma estimativa). Isso impõe uma restrição: dada a média e n − 1 observações, a última observação fica determinada. Por isso uma das observações "perde" liberdade.

## Por que importa pra IC

A [[Distribuicao T de Student|distribuição T]] muda de formato dependendo dos graus de liberdade. Pra n pequeno (gl pequeno), T tem caudas mais pesadas (mais larga). Pra n grande (gl grande), T converge pra normal.

```
T_(α/2, n−1) = INV.T(1 − α/2; n − 1)
```

A segunda entrada da função Excel é justamente os graus de liberdade.

## Exemplo numérico

| n | gl | T_(2,5%, gl) |
|---|---|---|
| 8 | 7 | 2,365 |
| 25 | 24 | 2,064 |
| 36 | 35 | 2,03 |
| 120 | 119 | 1,98 |
| ∞ | ∞ | 1,96 (= Z) |

## Quando você vê outros graus de liberdade

Pra IC de média = n − 1. Em **Estatística 2** (regressão, ANOVA, χ²), aparecem outras fórmulas: n − k onde k é o número de parâmetros estimados, ou (linhas − 1)(colunas − 1) pra tabelas de contingência, etc. Por enquanto, **decora n − 1**.

## Pegadinha

Não é o n. É **n − 1** pra IC de média. Confundir os dois quebra o cálculo do T no Excel.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Graus de liberdade]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Distribuicao T de Student]]
- [[Intervalo de Confiança]]
- [[Tamanho da amostra]]
- [[Variancia e desvio padrao]]
- [[Estatistica amostral]]
