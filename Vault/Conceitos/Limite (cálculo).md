---
tipo: conceito
materias: [MatemáticaAplicada]
tags: [conceito]
---

# Limite (cálculo)

## Definição

Comportamento de f(x) quando x se aproxima de um valor "a", sem necessariamente que f atinja esse valor em a. Notação: lim f(x), x → a.

// preencher: definição formal (épsilon-delta), limites laterais, quando o professor cobrir

## Fórmula / aplicação

Exemplo direto: f(x) = x², a = 2 → lim x² = 4 (x → 2)

Exemplo com indeterminação 0/0, resolvido por fatoração:
lim (x-1)/(x²-1), x → 1 = lim (x-1)/[(x+1)(x-1)] = lim 1/(x+1) = 0,5

Exemplo com raiz, resolvido por [[Racionalização por conjugado]]

## Onde aparece nas aulas

```dataview
LIST
FROM [[Limite (cálculo)]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Domínio de Função]]
- [[Racionalização por conjugado]]
