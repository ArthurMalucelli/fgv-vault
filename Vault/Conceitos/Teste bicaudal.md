---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste bicaudal

## Definição

Teste de hipótese em que a alternativa não aponta direção: H1 é "diferente de" (≠). O alfa se divide meio a meio entre as duas caudas (2,5% em cada, com alfa de 5%). Enunciado típico: "mudou?", "é diferente?". Contraste com o [[Teste unicaudal]], onde todo o alfa fica numa cauda só.

## Fórmula / aplicação

<pre>
Com alfa = 5%:
- z crítico bicaudal = ±1,96  (Z de alfa sobre 2)
- t crítico bicaudal = ±T.INV.2T(0,05; gl)  |  qt(0.975, gl)   (ex.: 2,093 com gl 19)

Valor-p bicaudal = 2 × P(T > |t calculado|)
  Excel: T.DIST.2T(ABS(t), gl)   /   2*(1-NORM.S.DIST(ABS(z),TRUE))
  R:     2 * pt(-abs(t), gl)     /   2 * (1 - pnorm(abs(z)))

Rejeita H0 se |estatística| > crítico, ou valor-p < alfa.
</pre>

Mesma amostra pode rejeitar no unicaudal e não rejeitar no bicaudal (satisfação 6,8 vs 7,0: p unicaudal 0,045, bicaudal 0,090). A cauda vem do enunciado, não do dado.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste bicaudal]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Teste unicaudal]]
- [[Z de alfa sobre 2]]
- [[Valor critico]]
- [[Valor-p]]
