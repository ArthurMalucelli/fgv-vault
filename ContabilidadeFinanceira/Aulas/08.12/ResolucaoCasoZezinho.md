---
materia: ContabilidadeFinanceira
data: 2026-08-12
tema: Caso Pipoca do Zezinho (A e B), lucro vs caixa nos 3 meses, competência, dividendos
tags: [caso, resolucao]
---

# Caso Pipoca do Zezinho (A): resolução

## Respostas diretas

| Pergunta | Resposta |
|---|---|
| Lucro do dia (fase aposentado) | **$80** |
| Q1: Lucro em M1 | **$1.150** |
| Q2: Quanto pode retirar em M1 | **$1.150** (não os $3.200 do caixa) |

Quiz do Tema 4 (gabarito confirmado 12/08): lucro M2 **1.370**, caixa operações M2 **(350)**, caixa operações M3 **1.260**, lucro M3 **1.590**.

## Fase 1: o dia único

```
Receita de vendas       125
(-) Ingredientes        (25)
(-) Aluguel do carrinho (20)
= Lucro do dia           80
```

Aqui [[Regime de Caixa]] e [[Regime de Competência]] dão o mesmo número, e não é coincidência: todos os eventos econômicos e financeiros acontecem dentro do mesmo período.

- Vende à vista: receita ganha e caixa entram juntos.
- Consome tudo que comprou (as sobras são descartadas): compra do dia = custo do dia, estoque final zero.
- Paga tudo no mesmo dia: nenhuma conta a pagar atravessa a meia-noite.

Sem estoque, sem contas a receber, sem contas a pagar. O que sobrou no bolso ($80) é exatamente o lucro. A armadilha do caso é o Zezinho concluir que "lucro = o que sobra no bolso" vale sempre. Vale só quando não existe descasamento temporal.

## Fase 2: Mês 1

Agora cada evento econômico descasa do evento financeiro. Mapa completo:

| Evento | Competência (M1) | Caixa (M1) | Caixa (quando sai) |
|---|---|---|---|
| Vendas à vista | Receita 3.200 | +3.200 | dentro de M1 |
| Ingredientes 450 + 250, tudo consumido | [[CMV]] (700) | 0 | dia 15 de M2 |
| Salário do rapaz | Despesa (750) | 0 | dia 05 de M2 |
| Aluguel do carrinho | Despesa (600) | 0 | período subsequente |
| **Total** | **Lucro 1.150** | **+3.200** | |

### Q1: lucro de M1

Pela [[DRE]] (competência):

```
Receita de vendas        3.200
(-) CMV                   (700)   [450 + 250, estoque final zero]
= Lucro bruto            2.500
(-) Salário               (750)   [trabalhado em M1, pago em M2]
(-) Aluguel               (600)   [carrinho usado em M1, pago depois]
= Lucro líquido de M1    1.150
```

O gatilho de reconhecimento é o fato gerador, nunca o pagamento: o rapaz trabalhou em M1, o carrinho rodou em M1, os ingredientes viraram pipoca vendida em M1. As três despesas pertencem a M1 mesmo que nenhum centavo tenha saído do caixa em M1.

### Q2: quanto pode retirar

Política: distribuir 100% do lucro, pago no próprio mês. Logo retira **$1.150**, e o caixa de $3.200 comporta o pagamento.

O erro que o caso quer provocar: olhar o caixa de $3.200 e achar que "sobrou" tudo isso. Os $2.050 de diferença não são do Zezinho, são dos credores: fornecedor ($700), rapaz ($750) e dono do carrinho ($600) só ainda não passaram pra cobrar. [[Dividendos]] saem do lucro, não do saldo bancário.

Prova de que fecha, [[Balanço Patrimonial]] no fim de M1 após pagar o dividendo:

```
ATIVO                        PASSIVO + PL
Caixa           2.050        Fornecedores          700
                             Salários a pagar      750
                             Aluguéis a pagar      600
                             PL (capital 0 +
                                 lucros retidos 0)   0
Total           2.050        Total               2.050  ✓
```

O caixa restante de 2.050 cobre exatamente as obrigações de 2.050. [[Equação Patrimonial]] fecha com PL zero: capital inicial era zero (ele nunca quis investir) e [[Lucros Acumulados]] zeram porque distribuiu 100%. Se retirasse os 3.200, o PL ficaria negativo em 2.050: ele teria distribuído dinheiro que pertence aos credores, e M2 começaria com dívida e caixa zero.

Pela [[DFC]] (método direto) de M1:

```
FCO   +3.200   [recebimento de clientes; nada foi pago]
FCF   (1.150)  [dividendos]
= Variação de caixa +2.050   (caixa: 0 -> 2.050) ✓ bate com o BP
```

## Mês 2 (dados reais + gabarito do quiz)

Eventos de M2: vendeu 3.400 (metade à vista, metade no cartão de crédito que só entra em M3), comprou 1.340 de ingredientes (pagos dia 15 de M3) e consumiu só 680, o resto (660) ficou em estoque. Pagou em M2 as três contas de M1: supermercado 700, salário 750, aluguel 600. Dividendo de 100% do lucro pago dentro do mês.

```
DRE M2
Receita de vendas        3.400   [competência: à vista + cartão]
(-) CMV                   (680)  [consumo, NÃO a compra de 1.340]
= Lucro bruto            2.720
(-) Salário               (750)
(-) Aluguel               (600)
= Lucro líquido          1.370

DFC M2 (método direto)
FCO
  Recebimento de clientes        1.700   [só a metade à vista]
  (-) Fornecedor (super de M1)    (700)
  (-) Salários (M1)               (750)
  (-) Aluguel (M1)                (600)
  = FCO                           (350)
FCF
  Dividendos pagos              (1.370)
= Variação de caixa             (1.720)   [caixa: 2.050 -> 330]

BP fim de M2
ATIVO                          PASSIVO + PL
Caixa               330        Fornecedores        1.340
Contas a receber  1.700        Salários a pagar      750
Estoque             660        Aluguéis a pagar      600
                               PL                      0
Total             2.690        Total               2.690  ✓
```

Pontos de prova de M2:

- [[CMV]] é o consumido (680), nunca o comprado (1.340). Os 660 não consumidos são ativo (estoque), não despesa.
- Lucro positivo (1.370) com FCO negativo ((350)): a receita do cartão é reconhecida inteira pela competência, mas o caixa só vê os 1.700 à vista enquanto as contas de M1 vencem. Mesma lição da Sofia, agora via contas a receber.
- O caixa termina M2 em 330: o distractor "(330)" do quiz era esse saldo, disfarçado de negativo.
- PL fecha em zero de novo (capital 0, lucro todo distribuído), e o ativo de 2.690 é 100% financiado por terceiros.

## Mês 3 (parte B, último mês de repouso)

Eventos de M3: no começo do mês paga as contas de M2 (supermercado 1.340, salário 750, aluguel 600). Nenhuma compra; todo o estoque remanescente (660) vendido por 3.600 à vista. Banco paga os 1.700 do cartão de M2. No fim do mês, pra não deixar dívida pra M4, paga também salário (750) e aluguel (600) do próprio M3.

```
DRE M3
Receita de vendas        3.600
(-) CMV                   (660)  [estoque que sobrou de M2]
= Lucro bruto            2.940
(-) Salário               (750)
(-) Aluguel               (600)
= Lucro líquido          1.590   ✓ gabarito (Q5)

DFC M3 (método direto)
  Vendas à vista                 3.600
  Cartão de M2                   1.700
  (-) Fornecedor (M2)           (1.340)
  (-) Salário (M2)                (750)
  (-) Aluguel (M2)                (600)
  (-) Salário + aluguel de M3   (1.350)   [pagos no próprio mês]
  = FCO                          1.260   ✓ gabarito
  (-) Dividendos                (1.590)
= Variação de caixa              (330)   [caixa: 330 -> 0]

BP fim de M3: tudo zero
Caixa 0, contas a receber 0, estoque 0 | passivo 0, PL 0
```

Q6: há caixa pra pagar o dividendo? Sim, exatamente: caixa antes do dividendo = 330 + 1.260 = 1.590 = lucro de M3. Paga e termina com caixa zero. Total distribuído nos 3 meses: 1.150 + 1.370 + 1.590 = **4.110**.

## Síntese do trimestre

| | M1 | M2 | M3 | Trimestre |
|---|---|---|---|---|
| Lucro | 1.150 | 1.370 | 1.590 | 4.110 |
| Caixa das operações | 3.200 | (350) | 1.260 | 4.110 |
| Dividendo | 1.150 | 1.370 | 1.590 | 4.110 |
| Caixa fim do mês | 2.050 | 330 | 0 | |

O arco pedagógico dos três meses cobre os três descasamentos possíveis:

- M1: caixa maior que lucro (despesas incorridas, nada pago ainda)
- M2: lucro positivo com caixa operacional negativo (venda no cartão reconhece receita sem caixa, estoque comprado além do consumo, enquanto as contas de M1 vencem)
- M3: caixa fecha o ciclo (cartão entra, estoque vira venda, todas as dívidas quitadas)

Lição central: lucro e caixa das operações respondem a gatilhos diferentes ([[Regime de Competência]] vs [[Regime de Caixa]]) e qualquer prazo (a pagar OU a receber) e estoque descolam um do outro, em qualquer direção. Mas quando o balanço volta a zero (sem giro pendente), **lucro acumulado = caixa gerado = dividendos pagos**. O descasamento é só de timing; no ciclo completo, competência e caixa convergem.

Planilha com tudo em fórmulas: `ZezinhoDFs.xlsx` nesta pasta (o enunciado da parte B só existe em foto no WhatsApp/celular, não foi salvo aqui).

## Pegadinhas / pontos de prova

- Lucro não é caixa. M1 tem lucro de 1.150 e geração operacional de caixa de 3.200. Na aula da Sofia (08.10) era o inverso: lucro positivo com FCO negativo. Os dois casos juntos mostram que o descasamento vai nas duas direções.
- No dia único os regimes coincidem porque o período fecha todas as pontas (sem estoque, sem prazo). Qualquer prazo introduzido (fornecedor, salário, aluguel) separa lucro de caixa.
- CMV usa o consumo, não a compra. Aqui deu igual (700 comprado, 700 consumido) porque o estoque final é zero. Se tivesse sobrado ingrediente, CMV < compras e a sobra ficaria como estoque no ativo.
- Dividendo não passa pela DRE. É distribuição do lucro já apurado, aparece na DMPL e como saída de caixa no FCF.
- Limite saudável de retirada = lucro do período, não saldo de caixa. Retirar acima do lucro (sem capital aportado antes) descapitaliza: PL negativo, caixa insuficiente pra honrar passivo.
- O aluguel diz "pagar $600 por mês no primeiro dia do período subsequente". Se "período" é o mês, paga 600 em cada início de mês seguinte; se é o trimestre, paga 1.800 no início do mês 4. Pra M1 tanto faz (despesa de 600 e caixa zero nos dois cenários), mas afeta o fluxo de caixa de M2 e M3. Provável gancho pra parte (B) do caso.

## Pra fixar

[[Regime de Competência]], [[Regime de Caixa]], [[CMV]], [[DRE]], [[DFC]], [[Balanço Patrimonial]], [[Equação Patrimonial]], [[Dividendos]], [[Lucros Acumulados]]
