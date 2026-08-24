---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Valor Crítico

## Definição

Ponto de corte, em unidades de Z ou T, que delimita a [[Regiao de rejeicao]] de um [[Teste de hipotese]], dado o nível de significância alfa.

Se a [[Estatistica de teste]] calculada ultrapassa o valor crítico (em módulo, num teste bicaudal), cai na região de rejeição e H0 é rejeitada.

## Fórmula / aplicação

<pre>
Teste bicaudal, alfa dado:
- Z crítico = [[Z de alfa sobre 2]], se usar distribuição normal
- T crítico = T(α/2, gl), se usar [[Distribuicao T de Student]]

Regra de decisão:
Se |estatística de teste| > valor crítico  →  rejeita H0
</pre>

Num teste bicaudal, alfa se divide meio a meio entre as duas caudas (ex: alfa 5% vira 2,5% em cada lado).

## Onde aparece nas aulas

```dataview
LIST
FROM [[Valor critico]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Valor-p]]
- [[Regiao de rejeicao]]
- [[Z de alfa sobre 2]]
- [[Distribuicao T de Student]]
- [[Graus de liberdade]]
