---
materia: ContabilidadeFinanceira
data: 2026-08-19
tema: Caso Marcus Dent, regime de caixa vs competência num mês de consultório
tags: [caso, resolucao]
---

# Caso Marcus Dent: resolução

Enunciado em `Slides/Atividade Marcus Dent 2024-2.pdf`. Planilha com tudo em fórmulas: `MarcusDentDFs.xlsx` nesta pasta. É o exercício de fechamento do tema 4 ([[Regime de Caixa]] vs [[Regime de Competência]]), na mesma linha do [[Caso Zezinho Pipoqueiro]], mas com o descasamento no sentido oposto.

## Respostas diretas

| Pergunta | Resposta |
|---|---|
| Lucro ou prejuízo de janeiro | **Lucro de $2.120** |
| Caixa gerado ou utilizado em janeiro | **Utilizou $1.600** (caixa de 10.000 para 8.400) |
| Balanço inicial (31/12/2023) | Total **$64.000** |
| Balanço final (31/01/2024) | Total **$69.700** |

Caixa caiu e lucro subiu. Os dois estão certos ao mesmo tempo: respondem a gatilhos diferentes.

## Balanço inicial (31/12/2023)

Três fatos antes de janeiro: empréstimo de 54.000, compra imediata dos equipamentos com esse dinheiro, depósito de 10.000 das economias como capital.

```
ATIVO                            PASSIVO + PL
Caixa e bancos        10.000     Empréstimo a pagar       54.000
Equipamentos          54.000     Capital social           10.000
Total                 64.000     Total                    64.000  ✓
```

Nada de receita, despesa ou depreciação ainda: os equipamentos chegaram em 31/12 e só começam a ser usados em janeiro.

## Mapa das transações de janeiro

Pra cada evento, as três perguntas do roteiro dos Treinos: mexeu no caixa? gerou receita ou consumiu recurso no mês? o que mudou no balanço?

| # | Evento | Caixa | DRE | Balanço |
|---|---|---|---|---|
| T1a | Serviços de 8.000, recebe 20% à vista | +1.600 | Receita 8.000 | [[Contas a Receber\|Clientes]] +6.400 |
| T1b | Adiantamento de 2.000 por serviços de março | +2.000 | nada | [[Adiantamento de Cliente\|Receita antecipada]] (passivo) +2.000 |
| T2 | Aluguel de janeiro e fevereiro, 2.200 pagos | (2.200) | Despesa (1.100) | [[Despesa Antecipada]] (ativo) +1.100 |
| T3 | Materiais 3.000 à vista, sobra 1.300 | (3.000) | Despesa (1.700) | [[Estoque]] +1.300 |
| T4 | Salário de 500, pago em fevereiro | nada | Despesa (500) | [[Contas a Pagar\|Salários a pagar]] +500 |
| T5 | [[Depreciação]]: 54.000 / 36 meses | nada | Despesa (1.500) | Depreciação acumulada (1.500) |
| T6 | Juros: 2% x 54.000 | nada | Despesa (1.080) | [[Juros a Pagar]] +1.080 |

Três eventos tocam o caixa num valor e a DRE em outro (T1b, T2, T3), e três tocam a DRE sem tocar o caixa (T4, T5, T6). Só T1a mexe nos dois, e mesmo assim em valores diferentes.

## Tabela comparativa (layout da professora)

| | Fluxo de Caixa (regime de caixa) | DRE (regime de competência) |
|---|---|---|
| **Receitas/Entradas** | | |
| Serviços | 1.600 | 8.000 |
| Adiantam. Serv. | 2.000 | 0 |
| Subtotal | 3.600 | 8.000 |
| **Despesas/Saídas** | | |
| Aluguel | (2.200) | (1.100) |
| Salários | 0 | (500) |
| Material | (3.000) | (1.700) |
| Depreciação do Equipamento | 0 | (1.500) |
| Juros | 0 | (1.080) |
| Subtotal | (5.200) | (5.880) |
| **Lucro / Variação no Caixa** | **(1.600)** | **2.120** |

## DRE de janeiro

```
Receita de serviços                    8.000
(-) Aluguel                           (1.100)   [2.200 pagos, só janeiro é competência]
(-) Salários e encargos                 (500)   [trabalhado em janeiro, pago em fevereiro]
(-) Materiais consumidos              (1.700)   [3.000 comprados, 1.300 ficaram em estoque]
(-) Depreciação dos equipamentos      (1.500)   [54.000 / 36]
= Resultado operacional (EBIT)         3.200
(-) Juros do empréstimo               (1.080)   [2% x 54.000, pagos só em dez/2025]
= Lucro líquido do mês                 2.120
```

Sem imposto de renda no caso. O [[EBIT]] de 3.200 mostra que a operação em si se paga; o [[Resultado Financeiro]] de (1.080) é o custo de ter financiado o equipamento com dívida em vez de capital.

## Fluxo de caixa de janeiro ([[Método Direto]])

```
Entradas
  Recebimento de clientes (20% de 8.000)      1.600
  Adiantamento de clientes                    2.000
Saídas
  Aluguel (janeiro e fevereiro)              (2.200)
  Materiais                                  (3.000)
= Caixa utilizado nas operações (FCO)        (1.600)
FCI em janeiro                                    0   [equipamentos comprados em 31/12]
FCF em janeiro                                    0   [empréstimo e capital em 31/12]
= Variação de caixa                          (1.600)
Caixa inicial 10.000, caixa final 8.400  ✓
```

## Balanço final (31/01/2024)

```
ATIVO                                    PASSIVO + PL
Circulante                               Circulante
  Caixa e bancos               8.400       Salários a pagar               500
  Clientes                     6.400       Receita antecipada           2.000
  Estoque de materiais         1.300     = Passivo circulante           2.500
  Despesas antecipadas         1.100     Não circulante
= Ativo circulante            17.200       Empréstimo a pagar          54.000
Não circulante                             Juros a pagar                1.080
  Equipamentos                54.000     = Passivo não circulante      55.080
  (-) Depreciação acumulada   (1.500)    Total do passivo              57.580
= Imobilizado líquido         52.500     Patrimônio líquido
                                           Capital social              10.000
                                           Lucros acumulados            2.120
                                         = PL                          12.120
Total                         69.700     Total                         69.700  ✓
```

Amarras: a [[Equação Patrimonial]] fecha (69.700 = 57.580 + 12.120); o lucro de 2.120 é exatamente a variação do PL (10.000 para 12.120), que vai pra [[Lucros Acumulados]] porque nada foi distribuído; o caixa do [[Balanço Patrimonial]] (8.400) é o caixa final da [[DFC]].

Classificação: empréstimo e juros vencem em dezembro de 2025, mais de 12 meses depois da data do balanço, então ficam no [[Passivo Não Circulante]]. Salários e receita antecipada se resolvem em fevereiro e março, [[Passivo Circulante]]. Equipamentos menos depreciação acumulada é o [[Imobilizado]] líquido, o único item do [[Ativo Não Circulante]]; todo o resto do ativo é [[Ativo Circulante]].

## Reconciliação: do lucro ao caixa ([[Método Indireto]])

Lucro 2.120 e caixa (1.600) diferem em 3.720. A ponte, item por item:

```
Lucro líquido do mês                                          2.120
(+) Depreciação (despesa sem saída de caixa)                  1.500
(+) Juros provisionados e não pagos                           1.080
(-) Aumento de clientes (80% da receita ainda não entrou)    (6.400)
(-) Aumento de estoque (comprou mais do que consumiu)        (1.300)
(-) Aumento de despesa antecipada (aluguel de fev já pago)   (1.100)
(+) Aumento de salários a pagar (despesa sem pagamento)         500
(+) Aumento de receita antecipada (caixa sem receita)         2.000
= Caixa utilizado nas operações                              (1.600)  ✓
```

Leitura: 2.580 de despesas que não saíram do caixa empurram pra cima; 8.800 de ativos de giro que cresceram (dinheiro travado em clientes, estoque e aluguel antecipado) puxam pra baixo; 2.500 de passivos de giro que cresceram (terceiros financiando o consultório) empurram pra cima de novo. 2.120 + 2.580 - 8.800 + 2.500 = (1.600). O [[Capital de Giro]] cresceu 6.300 no mês e engoliu o lucro inteiro e mais um pouco.

## Pegadinhas / pontos de prova

- Adiantamento não é receita. Os 2.000 entram no caixa e viram passivo (obrigação de prestar o serviço em março). Só viram receita quando o serviço for prestado. É o caso "antecipado" do slide de vendas x recebimento: afeta o caixa de agora e o lucro do futuro.
- Compra não é despesa. Comprou 3.000 de material, consumiu 1.700. A despesa é o consumo; os 1.300 que sobraram são ativo, não custo do mês. Mesma lógica do [[CMV]] do Zezinho em M2.
- Pagamento não é despesa. Pagou 2.200 de aluguel, mas só 1.100 competem a janeiro. Os outros 1.100 são despesa antecipada: afetam o caixa agora e o lucro de fevereiro.
- Despesa sem caixa, três vezes. Salário (paga em fevereiro), depreciação (o caixa já saiu em 31/12, na compra) e juros (só em dez/2025). As três reduzem o lucro de janeiro sem mexer um centavo do caixa do mês.
- Depreciação é consumo de riqueza. 54.000 / 36 = 1.500 por mês. O equipamento se desgasta a cada mês de uso, com ou sem pagamento. Mesma lógica do motoboy com a moto de 12.000 e vida útil de 48 meses.
- Juros correm desde o dia 1. 2% x 54.000 = 1.080 em janeiro, despesa financeira e juros a pagar, mesmo com pagamento só em dois anos. Em janeiro dá 1.080 tanto em juros simples quanto compostos; a diferença aparece a partir de fevereiro (2% sobre 55.080 no composto).
- [[Reconhecimento da Receita]] no fato gerador. Prestou 8.000, a DRE reconhece 8.000, no momento da prestação do serviço, não do recebimento nem do contrato. O que não entrou (6.400) vira clientes a receber e não reduz a receita.
- [[Confrontação]]: as despesas de janeiro (material consumido, aluguel de janeiro, salário do mês, depreciação, juros) são reconhecidas no mesmo mês da receita que ajudaram a gerar. É isso que a competência faz: casar esforço com benefício no mesmo período.
- Caixa caiu e ele ficou mais rico. Caixa de 10.000 para 8.400, PL de 10.000 para 12.120. A riqueza aumentou 2.120 e está espalhada em clientes, estoque e aluguel antecipado, não em dinheiro. Resposta direta à pergunta do slide 2: caixa subindo ou caindo não diz se está ficando mais rico.
- Inverso do Zezinho M1. Lá, caixa maior que lucro (despesas incorridas sem pagamento). Aqui, lucro maior que caixa (receita reconhecida sem recebimento e capital de giro crescendo). Os dois sentidos do descasamento.
- Equipamento comprado em 31/12 não entra no fluxo de caixa de janeiro. O FCI de janeiro é zero. Se a pergunta fosse "desde a abertura", aí sim: FCF +64.000 (empréstimo e capital), FCI (54.000).

## Pra fixar

[[Regime de Caixa]], [[Regime de Competência]], [[Reconhecimento da Receita]], [[Confrontação]], [[DRE]], [[DFC]], [[Balanço Patrimonial]], [[Equação Patrimonial]], [[Depreciação]], [[Despesa Antecipada]], [[Adiantamento de Cliente]], [[Contas a Receber]], [[Contas a Pagar]], [[Estoque]], [[Juros a Pagar]], [[Imobilizado]], [[Ativo Circulante]], [[Ativo Não Circulante]], [[Passivo Circulante]], [[Passivo Não Circulante]], [[EBIT]], [[Resultado Financeiro]], [[Método Direto]], [[Método Indireto]], [[Lucros Acumulados]], [[Capital de Giro]], [[Caso Marcus Dent]]
