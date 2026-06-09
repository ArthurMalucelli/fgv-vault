---
materia: ProdutosFinanceiros
tipo: simulado
bloco: 2
tema: Preço de títulos de renda fixa (precificação, YTM, marcação a mercado)
fonte_estilo: Lista 6 (Preço de Renda Fixa) + questões Extra autorais do professor
data: 2026-06-09
tags: [simulado, prova, renda-fixa, ytm]
---

# Simulado Bloco 2 — Preço de Renda Fixa

30 questões: 10 tópicos, cada um com terceto **fácil / média / difícil**. **Tudo cálculo**, no estilo da Lista 6. Nada de teoria solta: o que era conceito (ágio/deságio, relação preço-YTM) virou conta, que é como ele cobra.

**Como usar:** resolve no Excel/papel, confere o número no toggle, me chama nas que errar pra eu abrir a resolução. As difíceis são as "Extra" autorais dele (venda intermediária, face reverso, YTM de fluxo exótico).

> [!warning] As duas armadilhas deste bloco
> **1. Unidade e base.** Sempre declare a.a., a.s., a.p. e confira se o cupom é anual ou semestral.
> **2. Convenção semestral (ele usa as duas, leia o enunciado):**
> - **Nominal (americana):** taxa por semestre = YTM_nominal / 2; cupom por semestre = cupom_anual / 2. Use quando o enunciado disser "nominal".
> - **Efetiva:** taxa por semestre = (1 + YTM_efetiva)^(1/2) − 1; cupom por semestre = cupom_anual / 2. Use quando disser "efetiva".

> [!tip] Achar YTM dado o preço não tem fórmula fechada
> Quando o título tem cupom, a YTM sai por TIR ou Atingir Meta no Excel. Cupom zero tem fórmula fechada: YTM = (face/preço)^(1/n) − 1.

---

## 1. Preço de título com cupom anual (dado YTM)

**Fácil.** Um título do governo alemão (bund) de 10 anos tem valor nominal de € 100 e cupom de 5% ao ano (€ 5/ano). A taxa de juros de mercado é 6% ao ano. Qual o preço (VP) do título?

> [!success]- Resposta
> € 92,64. Deságio, porque o cupom (5%) é menor que a YTM (6%).

**Média.** Título de 6 anos, face R$ 1.000, cupom anual de 8% (R$ 80). A YTM é 9,5% ao ano. Qual o preço?

> [!success]- Resposta
> R$ 933,70.

**Difícil.** Título de 8 anos, face R$ 1.000, cupom anual de 7% (R$ 70), YTM 5,8% ao ano. Qual o preço, e de quanto é o ágio ou deságio em reais sobre o valor de face?

> [!success]- Resposta
> R$ 1.075,11. Ágio de R$ 75,11 (cupom 7% > YTM 5,8% → preço acima do par).

---

## 2. Preço de título com cupom semestral (dado YTM)

**Fácil (convenção nominal/americana).** Um Treasury de 10 anos, face $ 1.000, paga cupom nominal de 5,5% a.a. em parcelas semestrais; a YTM nominal é 5,2% a.a. Use a convenção americana (cupom e taxa divididos por 2). Qual o preço?

> [!success]- Resposta
> $ 1.023,16. Cupom $ 27,50/semestre, taxa 2,6%/semestre, 20 períodos.

**Média (convenção efetiva).** Título de 7 anos, face R$ 1.000, cupom de 8% a.a. pago semestralmente (R$ 40/semestre). A YTM é 6,75% efetiva ao ano. Qual o preço? (taxa semestral = (1,0675)^0,5 − 1)

> [!success]- Resposta
> R$ 1.075,18.

**Difícil (convenção efetiva).** Título de 4 anos, face R$ 1.000, cupom de 9% a.a. pago semestralmente (R$ 45/semestre), YTM efetiva anual de 7,4%. Qual o preço?

> [!success]- Resposta
> R$ 1.059,20.

---

## 3. YTM de título de cupom zero (dado preço)

**Fácil.** Um título de cupom zero, face R$ 1.000, é negociado por R$ 915 e vence em 1 ano. Qual a YTM?

> [!success]- Resposta
> 9,29% a.a. (= 1.000/915 − 1).

**Média.** Cupom zero, face R$ 1.000, preço R$ 863,80, vence em 3 anos. Qual a YTM?

> [!success]- Resposta
> 5,00% a.a. (= (1.000/863,80)^(1/3) − 1).

**Difícil.** Dois títulos de cupom zero, ambos face R$ 1.000: o A custa R$ 955,10 (vence em 1 ano) e o B custa R$ 765,10 (vence em 5 anos). Ache a YTM de cada e diga qual oferece o maior rendimento.

> [!success]- Resposta
> A = 4,70% a.a.; B = 5,50% a.a. O B rende mais.

---

## 4. YTM de título com cupom (dado preço)

**Fácil.** Título de 3 anos, face R$ 1.000, cupom anual de R$ 100, negociado a R$ 1.000 (ao par). Qual a YTM?

> [!success]- Resposta
> 10,00% a.a. Ao par, a YTM é igual à taxa de cupom.

**Média.** Título de 4 anos, face R$ 1.000, cupom anual de R$ 80, preço R$ 940. Qual a YTM? (TIR)

> [!success]- Resposta
> 9,89% a.a.

**Difícil.** Título de 5 anos, face R$ 1.000, cupom anual de R$ 70, preço R$ 1.045. Qual a YTM?

> [!success]- Resposta
> 5,93% a.a. Ágio, então a YTM fica abaixo da taxa de cupom (7%).

---

## 5. Ágio, par ou deságio (cupom vs YTM)

**Fácil.** Título de 5 anos, face R$ 1.000, cupom de 9% a.a., YTM 9% a.a. Qual o preço, sem fazer a conta toda? Justifique pelo número.

> [!success]- Resposta
> R$ 1.000 (ao par). Quando cupom = YTM, o preço é exatamente o valor de face.

**Média.** Título de 4 anos, face R$ 1.000, cupom de 6% a.a. (R$ 60), YTM 8% a.a. Calcule o preço e classifique em ágio, par ou deságio.

> [!success]- Resposta
> R$ 933,76. Deságio (cupom 6% < YTM 8% → preço abaixo do par).

**Difícil.** Três títulos de 10 anos, face R$ 1.000, cupons anuais de 2%, 4% e 8%, negociados respectivamente a R$ 816,20, R$ 983,90 e R$ 1.334,20. Ache a YTM de cada e diga qual tem o maior e qual tem o menor rendimento.

> [!success]- Resposta
> 2% → 4,30% | 4% → 4,20% | 8% → 3,90%. Maior YTM: o de cupom 2%. Menor YTM: o de cupom 8%. (Cupom maior não significa rendimento maior.)

---

## 6. Reprecificação quando a YTM muda

**Fácil.** Título de 10 anos, face R$ 1.000, cupom de 6% a.a., emitido com YTM 4%. Logo após a emissão a YTM sobe pra 5%. Calcule o preço antes e depois. O preço sobe ou desce?

> [!success]- Resposta
> A 4% = R$ 1.162,22; a 5% = R$ 1.077,22. Desce: YTM e preço andam em sentidos opostos.

**Média.** Título de 6 anos, face R$ 1.000, cupom de 7% a.a., negociado ao par (YTM 7%). A YTM sobe pra 9%. Qual o novo preço e a variação percentual?

> [!success]- Resposta
> De R$ 1.000,00 para R$ 910,28. Variação de −8,97%.

**Difícil.** Título de 7 anos, face R$ 1.000, cupom de 8% a.a. pago semestralmente, negociado a YTM efetiva de 6,75% a.a. Se a YTM subir pra 7% efetiva, qual o novo preço?

> [!success]- Resposta
> R$ 1.061,31 (era R$ 1.075,18 a 6,75%).

---

## 7. Venda intermediária (rendimento no período)

> Contexto comum às três: você compra, segura quase um ano e vende **segundos antes do primeiro cupom**. O preço de venda já embute o cupom iminente.

**Fácil.** Título de 5 anos, cupom anual de R$ 30, face R$ 720, comprado hoje a YTM 9,23% a.a. Pouco menos de um ano depois, segundos antes do primeiro cupom, você vende a YTM de mercado de 9,08% a.a. Qual o rendimento efetivo no período (≈ a.a.)?

> [!success]- Resposta
> Comprou por R$ 579,04, vendeu por R$ 635,59. Rendimento ≈ 9,77% no período.

**Média.** Título de 7 anos, cupom anual de R$ 40 (5% sobre face R$ 800), comprado a YTM 9,14% a.a. Você comprou 7 unidades. Vende quase um ano depois, segundos antes do 1º cupom, a YTM 9,56% a.a. Ache: (a) o investimento inicial; (b) o retorno em reais; (c) a taxa de retorno (% no período).

> [!success]- Resposta
> (a) R$ 4.438,62; (b) R$ 314,73; (c) 7,09%.

**Difícil.** Título de 5 anos, cupom anual de R$ 45, face R$ 900, comprado a YTM 10,2% a.a. Vendido segundos antes do 1º cupom a YTM 8,7% a.a. (a YTM caiu). Ache o rendimento no período e decomponha em quanto veio do cupom (carrego) e quanto do ganho de capital.

> [!success]- Resposta
> Rendimento ≈ 15,61%. Cupom (carrego) ≈ 6,22% + ganho de capital ≈ 9,39%. A queda da YTM puxou o ganho de capital pra cima.

---

## 8. Valor de face reverso (dado preço, cupom %, YTM)

> Truque: quando o cupom é um % do face, o preço é **linear no face**. P = face × [Σ c/(1+y)^t + 1/(1+y)^n]. Logo face = preço / fator.

**Fácil.** Um título de 1 ano paga cupom de 8% do valor de face e tem YTM de 12% a.a. Foi negociado por R$ 950. Qual o valor de face?

> [!success]- Resposta
> R$ 985,19 (P = face × 1,08/1,12 → face = 950 × 1,12/1,08).

**Média.** Título de 3 anos, cupom de 10% do face ao ano, YTM 14% a.a., preço R$ 880. Qual o valor de face?

> [!success]- Resposta
> R$ 970,09.

**Difícil.** Você comprou por R$ 782,10 um título de prazo 5 anos, cupom anual de 6,5% do face e YTM de 16,8% a.a. Qual o valor de face (par value)?

> [!success]- Resposta
> R$ 1.169,15.

---

## 9. YTM de fluxo irregular

**Fácil.** Você paga R$ 960 por um papel que pagará R$ 40 daqui a 1 ano e R$ 1.040 daqui a 2 anos. Qual a YTM?

> [!success]- Resposta
> 6,19% a.a.

**Média.** Você paga R$ 900 por um papel que pagará R$ 100 (ano 1), R$ 150 (ano 2) e R$ 880 (ano 3). Qual a YTM efetiva anual?

> [!success]- Resposta
> 8,89% a.a.

**Difícil.** Você pagou R$ 1.025 por um título exótico: cupom de R$ 55 daqui a um semestre; R$ 140 daqui a um ano; R$ 180 daqui a um ano e meio; e R$ 220 mais o principal de R$ 800 (R$ 1.020) daqui a dois anos. Qual a YTM efetiva anualizada?

> [!success]- Resposta
> Taxa semestral 9,15% → YTM 19,13% a.a. (resolve a TIR em base semestral e anualiza por (1+i)² − 1).

---

## 10. Retorno real de um título (ponte com inflação)

**Fácil.** Você compra um título de 2 anos com cupom de 8% a.a. pelo valor de face (ao par). Se a inflação for 3% a.a. durante toda a vida do título, qual o retorno real anual?

> [!success]- Resposta
> 4,85% a.a. Ao par, o nominal é 8%; real = 1,08/1,03 − 1.

**Média.** Um título prefixado é comprado a YTM de 11,5% a.a. (nominal). A inflação esperada é 5,2% a.a. Qual o retorno real anual esperado?

> [!success]- Resposta
> 5,99% a.a.

**Difícil.** Título prefixado comprado a YTM de 12% a.a., mantido até o vencimento em 3 anos. A inflação realizada foi 6%, 7,5% e 4% nos três anos. Qual o retorno nominal total e o retorno real total no período?

> [!success]- Resposta
> Nominal total = (1,12)³ − 1 = 40,49%. Inflação acumulada = (1,06)(1,075)(1,04) − 1 = 18,51%. Retorno real no período = 1,4049/1,1851 − 1 = 18,55%.

---

## Conceitos (vault)

[[YTM]] · [[Cupom]] · [[Valor de Face]] · [[Ágio e Deságio]] · [[Cupom Zero]] · [[Preço de Renda Fixa]] · [[Marcação a Mercado]] · [[Fisher]]
