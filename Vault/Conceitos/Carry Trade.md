---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, câmbio]
---

# Carry Trade

## Definição

Estratégia que toma empréstimo em moeda de **juro baixo** e investe em moeda de **juro alto**, lucrando do diferencial de juros.

## Mecânica

1. Toma empréstimo em moeda A (juro baixo).
2. Converte para moeda B (juro alto) na taxa spot.
3. Aplica em moeda B pelo prazo desejado.
4. No vencimento: reconverte para A na taxa spot futura.
5. Paga o empréstimo em A.
```
Lucro = Valor final reconvertido − Custo do empréstimo capitalizado
```

## Riscos

- **Cambial**: se a moeda fraca (A) **se valorizar** durante o período (câmbio A/B cai), reconverter fica mais caro.
- **Taxa pós-fixada**: se o BC do país de juro baixo (A) subir os juros, custo da dívida sobe.

## Forward sem arbitragem ([[IRP]])

O forward que torna o carry trade neutro é exatamente o `F_IRP = S × (1+r_A)/(1+r_B)`. Carry trade hedgeado com forward dá lucro zero. O carry só funciona descoberto, apostando que a moeda fraca não vai apreciar tanto quanto o IRP "prevê".

## Exemplo (slide aula 21)

Toma 1M JPY a 0,1%, câmbio 120 JPY/USD, aplica em USD a 5%:
- Converte: 1M / 120 = 8.333 USD
- Investe 1 ano: 8.750 USD
- Cenário JPY desvalorizou (130 JPY/USD): reconverte 8.750 × 130 = 1.137.500 JPY; divida = 1.001.000; lucro 136.500 JPY ✓
- Cenário JPY se valorizou (110 JPY/USD) + BoJ subiu pra 1,5%: reconverte 8.750 × 110 = 962.500 JPY; divida = 1.015.000; prejuízo 52.500 JPY ✗

## Conceitos relacionados

- [[IRP]]
- [[Forward]]
- [[Cotação Direta]]
