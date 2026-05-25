---
materia: ProdutosFinanceiros
data: 2026-05-20
tema: Valuation por Dividendos e Retorno Esperado
tags: [resumo]
---

# Resumo: Valuation por Dividendos e Retorno Esperado

## Ideia central

Preço de uma ação = valor presente do fluxo de dividendos esperados, descontado a uma taxa que reflete o risco da empresa. Em horizontes longos, o preço terminal vira irrelevante e o que domina é o fluxo de dividendos. Por isso o foco é em **projetar dividendo**, não preço futuro.

## Conceitos-chave

| Conceito | O que é |
|---|---|
| [[Valor Intrinseco]] | Valor "verdadeiro" da empresa baseado no que ela gera ao longo do tempo (dividendos). Contraste com valor de mercado |
| [[DDM]] (Dividend Discount Model) | Modelo geral: P₀ = Σ Div_t/(1+R_E)^t. Também chamado DCF ou Modelo de Gordon |
| [[Modelo de Gordon]] | Simplificação do DDM com taxa de crescimento constante g. Próxima aula |
| [[Dividend Yield]] | Div₁/P₀. Quanto da ação retorna em forma de dividendo |
| [[Ganho de Capital]] | (P₁ − P₀)/P₀. Variação de preço como fonte de retorno |
| [[Retorno Esperado]] | R_E = Dividend Yield + Capital Gain. Total esperado |
| [[Valor Terminal]] | Preço da empresa no fim do horizonte projetado. Calculado via perpetuidade |
| [[WACC]] | Weighted Average Cost of Capital. Taxa de desconto que mistura custo de capital próprio e de terceiros. Matéria de finanças corporativas |
| [[CAPM]] | Modelo pra estimar o custo de capital próprio ajustado ao risco. Matéria de finanças |
| [[Price Earnings]] | Múltiplo P/E. Quantas vezes o preço é em relação aos earnings. Método alternativo de valuation |
| [[Guidance]] | Projeção que a empresa dá sobre estratégia e lucro futuros. Tipicamente cobre 2-5 anos |
| [[Perpetuidade]] | Fluxo de caixa infinito. Usado pra calcular valor terminal |

## Fórmulas

**Modelo de um período:**

<pre>
P₀ = (Div₁ + P₁) / (1 + R_E)
</pre>

**Retorno esperado (decomposto):**

<pre>
R_E = (Div₁ + P₁ − P₀) / P₀
    = Div₁/P₀  +  (P₁ − P₀)/P₀
    = Dividend Yield + Capital Gain
</pre>

**Modelo geral (DDM):**

<pre>
P₀ = Σ[t=1..N] Div_t/(1+R_E)^t  +  P_N/(1+R_E)^N
</pre>

**P/E (preço sobre earnings):**

<pre>
P/E = Preço da ação / Earnings por ação
Preço estimado = P/E médio do setor × Earnings da empresa
</pre>

## Exemplos numéricos da aula

**Ex.1**: P₀=100, P₁=110, Div₁=5 → R_E = 15% (Yield 5%, Capital Gain 10%)

**Ex.2 (Walgreens)**: Div₁=0,44, P₁=33, R_E=8,5% → P₀ = US$ 30,82
- Yield ≈ 1,42% / Capital Gain ≈ 7,07%
- Lição: retorno dominado pelo capital gain → alto risco (preço futuro é mais volátil que dividendo)

**Ex.3**: Div₁=1,92, P₁=65, R_E=11% → P₀ máximo = R$ 78,31
- Se você paga 79, retorno cai abaixo dos 11% desejados

## Pegadinhas / pontos de prova

1. **Taxa de desconto NÃO é taxa livre de risco**. Ação tem risco, então R_E = taxa livre + prêmio de risco. Análogo ao prêmio de crédito num CDB.

2. **P₀ é o preço MÁXIMO que você pagaria** dado um retorno desejado. Se a ação tá sendo negociada por valor maior, seu retorno realizado vai ficar abaixo do retorno-meta.

3. **Dividend Yield + Capital Gain = Retorno Esperado**. Sempre fecha matematicamente.

4. **Decomposição revela perfil de risco**: se o retorno depende muito mais do capital gain do que do dividendo, a ação é mais arriscada (preço futuro é menos previsível que dividendo).

5. **Horizonte longo zera o peso do preço terminal**. Pra ações de empresas "que nunca acabam", o que importa é o fluxo de dividendos. Pra horizonte curto (1 ano), o preço terminal domina.

6. **DDM, DCF e Modelo de Gordon são tratados como sinônimos** nessa aula. Tecnicamente: DDM é a fórmula geral, Gordon é a versão simplificada com g constante, DCF é a abordagem por fluxo de caixa descontado em geral.

7. **Quando empresa acaba**, acionista só recebe depois de despesas operacionais, obrigações trabalhistas e impostos. Em recuperação judicial, valor a receber tipicamente é zero.

8. **Por que analista não gosta de surpresa em dividendo**: surpresa, seja pra cima ou pra baixo, quebra o modelo. Empresas têm disciplina pra entregar próximo do guidance.

## Pra fixar

- [[DDM]]
- [[Modelo de Gordon]]
- [[Dividend Yield]]
- [[Retorno Esperado]]
- [[Valor Terminal]]
- [[Valor Intrinseco]]
- [[WACC]]
- [[CAPM]]
- [[Price Earnings]]
- [[Guidance]]
- [[Perpetuidade]]

## Próxima aula (segunda 25.05)

[[Modelo de Gordon]]: simplificação do DDM. Você só precisa de:
- Um dividendo (o próximo)
- A taxa de crescimento g do dividendo

Fórmula fechada, sem precisar fazer somatório termo a termo.
