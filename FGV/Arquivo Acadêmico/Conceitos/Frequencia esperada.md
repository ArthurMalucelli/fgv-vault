---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Frequencia esperada

## Definição

Contagem que cada célula teria se H0 fosse verdadeira. É o "E" da estatística qui-quadrado Σ(O − E)²/E. Na aderência, vem da distribuição teórica; na independência, vem dos totais marginais da tabela. Você calcula as esperadas; a função pronta (CHISQ.TEST no Excel) não as devolve, o `chisq.test` do R devolve em `$expected`.

## Fórmula / aplicação

<pre>
Aderência:      E_i  = n × p_i                              (ex.: 200 × 0,45 = 90)
Independência:  E_ij = (total linha i × total coluna j) / n  (ex.: 120 × 118 / 320 = 44,25)

Regra de aplicação: E ≥ 5 na maioria das células. Esperadas pequenas invalidam a
aproximação qui-quadrado; saídas: juntar categorias ou teste exato de Fisher (2 × 2).
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Frequencia esperada]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste qui-quadrado de aderencia]]
- [[Teste qui-quadrado de independencia]]
- [[Distribuicao qui-quadrado]]
