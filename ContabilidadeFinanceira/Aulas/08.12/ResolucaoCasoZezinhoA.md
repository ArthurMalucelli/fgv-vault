---
materia: ContabilidadeFinanceira
data: 2026-08-12
tema: Caso Pipoca do Zezinho (A), lucro vs caixa, competência, limite de retirada de dividendos
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

## Meses 2 e 3 (gabarito do quiz do Tema 4)

Números oficiais do quiz, com a reconstrução dos dados implícitos (o enunciado B não está salvo aqui; a reconstrução é a única que fecha os quatro números exatos):

| | M1 | M2 | M3 |
|---|---|---|---|
| Vendas (competência) | 3.200 | 3.400 (1.700 a prazo) | 3.290 |
| Compras consumidas ([[CMV]]) | 700 | 680 | 350 |
| Salário + aluguel | 1.350 | 1.350 | 1.350 |
| **Lucro** | **1.150** | **1.370** | **1.590** |
| Recebimentos | 3.200 | 1.700 | 3.290 |
| Pagamentos (contas do mês anterior) | 0 | 2.050 | 2.030 |
| **Caixa das operações** | **+3.200** | **(350)** | **+1.260** |

A conta do caixa de cada mês: recebe as vendas à vista do mês e paga as três contas do mês anterior (salário 750 dia 05, fornecedor dia 15, aluguel 600 dia 01).

O arco pedagógico dos três meses cobre os três descasamentos possíveis:

- M1: caixa maior que lucro (despesas incorridas, nada pago ainda)
- M2: lucro positivo com caixa operacional negativo (venda a prazo reconhece receita sem caixa, enquanto as contas de M1 vencem)
- M3: os dois positivos e próximos (operação normaliza)

Lição central: lucro e caixa das operações respondem a gatilhos diferentes ([[Regime de Competência]] vs [[Regime de Caixa]]) e qualquer prazo (a pagar OU a receber) descola um do outro, em qualquer direção.

## Pegadinhas / pontos de prova

- Lucro não é caixa. M1 tem lucro de 1.150 e geração operacional de caixa de 3.200. Na aula da Sofia (08.10) era o inverso: lucro positivo com FCO negativo. Os dois casos juntos mostram que o descasamento vai nas duas direções.
- No dia único os regimes coincidem porque o período fecha todas as pontas (sem estoque, sem prazo). Qualquer prazo introduzido (fornecedor, salário, aluguel) separa lucro de caixa.
- CMV usa o consumo, não a compra. Aqui deu igual (700 comprado, 700 consumido) porque o estoque final é zero. Se tivesse sobrado ingrediente, CMV < compras e a sobra ficaria como estoque no ativo.
- Dividendo não passa pela DRE. É distribuição do lucro já apurado, aparece na DMPL e como saída de caixa no FCF.
- Limite saudável de retirada = lucro do período, não saldo de caixa. Retirar acima do lucro (sem capital aportado antes) descapitaliza: PL negativo, caixa insuficiente pra honrar passivo.
- O aluguel diz "pagar $600 por mês no primeiro dia do período subsequente". Se "período" é o mês, paga 600 em cada início de mês seguinte; se é o trimestre, paga 1.800 no início do mês 4. Pra M1 tanto faz (despesa de 600 e caixa zero nos dois cenários), mas afeta o fluxo de caixa de M2 e M3. Provável gancho pra parte (B) do caso.

## Pra fixar

[[Regime de Competência]], [[Regime de Caixa]], [[CMV]], [[DRE]], [[DFC]], [[Balanço Patrimonial]], [[Equação Patrimonial]], [[Dividendos]], [[Lucros Acumulados]]
