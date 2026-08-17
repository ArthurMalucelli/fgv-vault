---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste Unicaudal

## Definição

Teste de hipótese em que a alternativa aponta uma única direção (H1: parâmetro maior que o baseline, ou menor), então todo o alfa fica concentrado numa cauda só. Identificação pelo enunciado: "aumentou?" ou "diminuiu?" pede unicaudal; "é diferente?" pede bicaudal. O baseline entra no H0 com ≤ ou ≥.

## Fórmula / aplicação

<pre>
Com alfa = 5%:
- Unicaudal: z crítico = 1,645 (os 5% inteiros numa cauda)
- Bicaudal:  z crítico = 1,96  (2,5% em cada cauda)

Região de rejeição (cauda direita): de 1,645 a +∞
Valor-p unicaudal: P(Z > z calculado)
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste unicaudal]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Valor critico]]
- [[Regiao de rejeicao]]
- [[Z de alfa sobre 2]]
- [[Valor-p]]
