---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, câmbio, paridade]
---

# IRP (Interest Rate Parity / Paridade da Taxa de Juros)

## Definição

Relação de equilíbrio entre taxa de juros e taxa de câmbio que impede arbitragem entre dois países. A versão coberta (CIP) é a que aparece na aula.

## Fórmula central

```
(1 + r_country) / (1 + r_US) = Forward_country/USD / Spot_country/USD
```

Equivalentemente, para uma cotação `quote/base`:
```
F = S × (1 + r_quote) / (1 + r_base)
```

## Lógica

Se a moeda A tem juro maior que a B, a moeda A deve se **depreciar** no forward (em relação a B). Caso contrário, todo mundo aplicaria em A e teria ganho sem risco.

## Aplicação típica: forward sem arbitragem

JPY/USD spot = 128,77; i_USD = 5,08%; i_JPY = 1,88%.
```
F = 128,77 × (1 + 0,0188) / (1 + 0,0508) = 124,85 JPY/USD
```
USD se deprecia no forward (vale menos ienes) pois USD tem juro maior.

## Aplicação: taxa equivalente em outra moeda

BR juro 12%, spot 5,50 BRL/USD, forward 5,82 BRL/USD:
```
F/S = (1+r_BRL)/(1+r_USD)
5,82/5,50 = 1,12 / (1+r_USD)
r_USD = 5,84% a.a.
```

## Regra mnemônica de direção

Na cotação A/B: A = quote (numerador). Na razão de juros, mesma posição: `(1+r_A)/(1+r_B)`. Combina com `F_A/B / S_A/B`.

## Conceitos relacionados

- [[PPP]]
- [[Carry Trade]]
- [[Forward]]
- [[Cotação Direta]]
