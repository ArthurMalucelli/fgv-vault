---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Valor-p

## Definição

Probabilidade de observar um resultado tão ou mais extremo que o observado na amostra, supondo que [[Teste de hipotese|H0]] seja verdadeira.

Valor-p baixo (menor que alfa) indica que o resultado observado seria pouco provável se H0 fosse verdadeira, o que dá evidência pra rejeitar H0. Valor-p alto (maior que alfa) indica que o resultado é plausível sob H0, e não há evidência suficiente pra rejeitar.

## Fórmula / aplicação

<pre>
Regra de decisão:
Se valor-p < alfa  →  rejeita H0
Se valor-p ≥ alfa  →  não rejeita H0
</pre>

Comparar valor-p com alfa é equivalente a comparar a [[Estatistica de teste]] com o [[Valor critico]]: os dois caminhos levam à mesma decisão.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Valor-p]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Valor critico]]
- [[Estatistica de teste]]
- [[Teste de hipotese]]
- [[Regiao de rejeicao]]
