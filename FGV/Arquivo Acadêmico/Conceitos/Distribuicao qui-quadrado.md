---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, distribuicao]
---

# Distribuicao qui-quadrado

## Definição

Distribuição de referência dos testes qui-quadrado (aderência e independência). Só assume valores positivos (soma de desvios ao quadrado), é assimétrica à direita e depende de um parâmetro: os [[Graus de liberdade|graus de liberdade]]. Por isso o teste é sempre de cauda direita: desvios grandes em qualquer sentido só aumentam a estatística.

## Fórmula / aplicação

<pre>
Estatística: χ² = Σ (O − E)² / E
gl: k − 1 (aderência) ou (r − 1)(c − 1) (independência)

Crítico (entra alfa, sai corte):   Excel CHISQ.INV.RT(α, gl)   |  R qchisq(1 − α, gl)
Valor-p (entra χ², sai área):      Excel CHISQ.DIST.RT(χ², gl) |  R pchisq(χ², gl, lower.tail = FALSE)

Críticos a 5%: gl 1 → 3,841 · gl 2 → 5,991 · gl 3 → 7,815
Com gl = 1, χ² = z² (é o que o prop.test do R mostra como X-squared).
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Distribuicao qui-quadrado]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste qui-quadrado de aderencia]]
- [[Teste qui-quadrado de independencia]]
- [[Graus de liberdade]]
- [[Distribuicao normal]]
