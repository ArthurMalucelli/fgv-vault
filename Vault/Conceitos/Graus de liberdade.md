---
tipo: conceito
materias: [Estatistica2, Estatistica]
tags: [conceito, inferencia, distribuicao]
---

# Graus de Liberdade

## Definição

Parâmetro extra da [[Distribuicao T de Student]], além de média e variância. Representa o número de valores da amostra que são livres pra variar depois de já ter fixado a média amostral.

Pra teste ou intervalo sobre uma média com uma amostra de tamanho n, graus de liberdade = n - 1.

Conforme os graus de liberdade aumentam (amostra maior), a distribuição T converge pra distribuição normal (Z). Por isso a regra prática de usar Z acima de ~30 observações.

## Fórmula / aplicação

<pre>
gl = n − 1
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Graus de liberdade]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Distribuicao T de Student]]
- [[Estatistica de teste]]
- [[Valor critico]]
- [[Tamanho da amostra]]
