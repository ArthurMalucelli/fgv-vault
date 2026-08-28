---
tipo: conceito
materias: [ProdutosFinanceiros, Estatistica]
tags: [conceito, risco, estatistica]
---

# Volatilidade

## Definição

Medida de dispersão dos retornos de um ativo em torno da média. Operacionalizada como **desvio-padrão dos retornos** (frequentemente anualizado). Proxy mais usado de risco em finanças.

## Cálculo básico

```
σ = √(Σ(r_i − r̄)² / (n − 1))
```

Pra anualizar a partir de série diária: σ_anual = σ_diário × √252 (252 dias úteis no ano).

## Características

- **Não distingue alta de baixa.** Mede oscilação dos dois lados. Retorno pode ser positivo e ainda ter volatilidade alta
- **Subindo em crise:** correlações vão pra 1 e volatilidades disparam (VIX)
- **Heteroscedástica:** volatilidade varia no tempo, períodos de calmaria e turbulência se alternam (efeito GARCH)

## Interpretação prática

| Nível | Tipo de ativo |
|---|---|
| ~5% a/a | Caderneta, fundos DI, CDB pós |
| 10-15% a/a | Renda Fixa prefixada/inflação |
| 20-25% a/a | Ações Brasil (Ibovespa) |
| 30-50% a/a | Small caps, mercados emergentes específicos |
| 50%+ a/a | Cripto |

## Volatilidade implícita vs realizada

- **Realizada (histórica):** calculada a partir da série passada
- **Implícita:** extraída do preço de opções, reflete expectativa de mercado pra volatilidade futura

VIX é volatilidade implícita do S&P 500. Quando VIX sobe, mercado espera turbulência.

## Pegadinhas

- Volatilidade não é o único risco. Ativo com baixa vol mas crédito ruim ainda quebra (Marfrig, Americanas)
- Retorno passado não prediz retorno futuro, e vol passada não prediz vol futura com precisão (mas é menos pior que retorno)
- Sharpe Ratio = (retorno excedente) / volatilidade. Compara prêmio por unidade de risco

## Conceitos relacionados

- [[Variancia e desvio padrao]]
- [[Diversificacao]]
- [[Marcacao a mercado]]
