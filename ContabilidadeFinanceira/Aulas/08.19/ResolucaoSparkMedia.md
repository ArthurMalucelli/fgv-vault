---
materia: ContabilidadeFinanceira
data: 2026-08-19
tema: Atividade SparkMedia (Ativ CxComp), balanços 31/12 e 31/01, DRE x Fluxo de Caixa, conciliação caixa e competência
tags: [caso, resolucao]
---

# Atividade SparkMedia: resolução

Grupo 10. Enunciado: agência de microinfluenciadores, empréstimo de 120.000 (5 parcelas anuais, juros prefixados 1,5% a.m.) usado no mesmo dia pra comprar equipamentos, capital de 20.000 em caixa, cinco transações em janeiro de 2026.

## Respostas diretas

| Pergunta | Resposta |
|---|---|
| Lucro de janeiro ([[Regime de Competência]]) | **11.700** |
| Variação de caixa de janeiro ([[Regime de Caixa]]) | **(11.000)**, caixa vai de 20.000 pra 9.000 |
| Total do balanço 31/12/2025 | 140.000 |
| Total do balanço 31/01/2026 | 177.500 |

## Balanço de abertura (31/12/2025)

O ponto que mais derruba gente: o empréstimo **não fica no caixa**. Entrou 120.000 e saiu 120.000 no mesmo dia pra comprar computadores, softwares e equipamentos. O único dinheiro que sobra em caixa é o capital do Enzo.

```
ATIVO                              PASSIVO E PL
Caixa                 20.000       Empréstimos (NC)      120.000
Imobilizado          120.000       Capital Social         20.000
Total                140.000       Total                 140.000
```

## Mapa das transações (formato da planilha da professora)

Colunas: 1 = receita de serviços; 1' = adiantamento recebido; 2 = aluguel; 3 = materiais; 4 = salários; 5 = depreciação; Ajustes = juros do mês.

| Conta | 31/12/25 | 1 | 1' | 2 | 3 | 4 | 5 | Ajustes | 31/01/26 |
|---|---|---|---|---|---|---|---|---|---|
| Caixa | 20.000 | 10.000 | 15.000 | (24.000) | (12.000) | | | | **9.000** |
| Contas a Receber | | 30.000 | | | | | | | 30.000 |
| [[Estoque]] | | | | | 4.500 | | | | 4.500 |
| Adiantamento (a fornecedor) | | | | | | | | | 0 |
| [[Despesa Antecipada|Despesas Antecipadas]] | | | | 16.000 | | | | | 16.000 |
| Imobilizado | 120.000 | | | | | | | | 120.000 |
| (−) [[Depreciação]] acumulada | | | | | | | (2.000) | | (2.000) |
| **Total do Ativo** | 140.000 | 40.000 | 15.000 | (8.000) | (7.500) | 0 | (2.000) | 0 | **177.500** |
| Fornecedores | | | | | | | | | 0 |
| Salários a Pagar | | | | | | 9.000 | | | 9.000 |
| [[Adiantamento de Cliente|Adiantamento de Clientes]] (PC) | | | 15.000 | | | | | | 15.000 |
| Empréstimos e financiamentos (NC) | 120.000 | | | | | | | | 120.000 |
| Juros a Pagar | | | | | | | | 1.800 | 1.800 |
| Capital Social | 20.000 | | | | | | | | 20.000 |
| Lucro Acumulado | | 40.000 | | (8.000) | (7.500) | (9.000) | (2.000) | (1.800) | **11.700** |
| **Total Passivo + PL** | 140.000 | 40.000 | 15.000 | (8.000) | (7.500) | 0 | (2.000) | 0 | **177.500** |

Cada coluna fecha sozinha (total do ativo = total do passivo + PL). Se uma coluna não fecha, o erro está nela.

Lógica de cada coluna:

- **1**: receita 40.000 ganha (serviço prestado). 25% à vista = 10.000 no caixa, 30.000 em Contas a Receber. Lucro +40.000.
- **1'**: 15.000 em dinheiro por campanha a entregar em abril. Caixa +15.000, mas receita zero: é obrigação de entregar serviço, vai pro passivo circulante. Lucro não mexe.
- **2**: pagou 24.000 por jan, fev e mar. Caixa (24.000). Janeiro foi consumido: despesa 8.000. Fev e mar ainda são direito de uso: Despesas Antecipadas 16.000.
- **3**: comprou 12.000 à vista, sobrou 4.500 no inventário. Caixa (12.000). A sobra é ativo (Estoque 4.500). O consumido, 12.000 − 4.500 = 7.500, é despesa.
- **4**: salários de janeiro, pagos em fevereiro. Despesa 9.000 agora, Salários a Pagar 9.000, caixa zero.
- **5**: imobilizado 120.000 / 60 meses = 2.000 por mês. Depreciação acumulada (2.000) como redutora do ativo, lucro (2.000), caixa zero.
- **Ajustes**: juros de janeiro = 120.000 × 1,5% = 1.800. Juros a Pagar +1.800, lucro (1.800), caixa zero. Não tem transação numerada pra isso, por isso vai em Ajustes.

## [[DRE]] de janeiro (competência)

```
Receita de serviços                     40.000
(−) Aluguel (1 mês de 3)                 (8.000)
(−) Materiais consumidos (12.000 − 4.500)(7.500)
(−) Salários e encargos                  (9.000)
(−) Depreciação (120.000 / 60)           (2.000)
(−) Juros (120.000 × 1,5%)               (1.800)
= Lucro líquido                          11.700
```

## Fluxo de caixa de janeiro ([[DFC]], regime de caixa)

```
Entradas
  Serviços recebidos à vista (25% de 40.000)   10.000
  Adiantamento de cliente                      15.000
  Subtotal                                     25.000
Saídas
  Aluguel (3 meses)                           (24.000)
  Materiais                                   (12.000)
  Subtotal                                    (36.000)
= Variação no caixa                           (11.000)
Caixa inicial 20.000 → caixa final 9.000
```

## Conciliação lucro → caixa

| Item | Valor | Por quê |
|---|---|---|
| Lucro do período | 11.700 | ponto de partida |
| (+) Depreciação | 2.000 | despesa sem saída de caixa |
| (+) Juros a pagar | 1.800 | despesa sem saída de caixa |
| (+) Salários a pagar | 9.000 | despesa sem saída de caixa |
| (−) Contas a receber | (30.000) | receita sem entrada de caixa |
| (+) Adiantamento de clientes | 15.000 | caixa sem receita |
| (−) Despesas antecipadas | (16.000) | caixa sem despesa |
| (−) Estoque | (4.500) | caixa sem despesa |
| **= Variação no caixa** | **(11.000)** | bate com o fluxo de caixa |

Tabela comparativa no formato Marcus Dent:

| | Fluxo de Caixa | DRE |
|---|---|---|
| Serviços | 10.000 | 40.000 |
| Adiantamento | 15.000 | 0 |
| Subtotal entradas / receitas | 25.000 | 40.000 |
| Aluguel | (24.000) | (8.000) |
| Materiais | (12.000) | (7.500) |
| Salários | 0 | (9.000) |
| Depreciação | 0 | (2.000) |
| Juros | 0 | (1.800) |
| Subtotal saídas / despesas | (36.000) | (28.300) |
| **Variação no caixa / Lucro** | **(11.000)** | **11.700** |

## Balanço 31/01/2026

```
ATIVO                                     PASSIVO E PL
Circulante                                Circulante
  Caixa                    9.000            Salários a Pagar             9.000
  Contas a Receber        30.000            Adiantamento de Clientes    15.000
  Estoque                  4.500          Não circulante
  Despesas Antecipadas    16.000            Empréstimos e financ.      120.000
Não circulante                              Juros a Pagar                1.800
  Imobilizado            120.000          PL
  (−) Deprec. acumulada   (2.000)           Capital Social              20.000
                                            Lucro Acumulado             11.700
Total                    177.500          Total                        177.500
```

Checks: caixa 20.000 − 11.000 = 9.000 (bate com o fluxo de caixa); PL 20.000 + 11.700 (bate com a DRE).

## Item b: desempenho do primeiro mês

Lucrou 11.700 sobre 40.000 de receita (margem ~29%) e ao mesmo tempo queimou 11.000 de caixa. Não é contradição, é descasamento temporal típico de início de operação:

- 75% da receita virou Contas a Receber (30.000), entra só em fevereiro.
- Pagou 3 meses de aluguel de uma vez, 16.000 ainda estão "estocados" em Despesas Antecipadas.
- Comprou material além do consumo, 4.500 parados em estoque.
- O único caixa que entrou "de graça" foi o adiantamento de 15.000, e ele não é lucro: é obrigação de entregar uma campanha em abril, que vai consumir recursos.

A empresa ficou mais rica (PL subiu 11.700) com menos dinheiro no bolso. Pergunta do slide 2 invertida: caixa caiu e mesmo assim houve enriquecimento.

Pontos de atenção:

1. Liquidez de fevereiro: caixa de 9.000 contra salários de 9.000 vencendo no 5º dia útil. Depende dos 30.000 de Contas a Receber entrarem em dia.
2. Serviço da dívida: a 1ª parcela de 24.000 + juros acumulados (1.800 × 12 = 21.600) vence em janeiro de 2027. Precisa gerar ~45.600 de caixa no ano só pra isso. No ritmo de janeiro (lucro 11.700 + depreciação 2.000 + juros 1.800 ≈ 15.500 de geração operacional por mês quando os recebíveis normalizarem), dá, mas sem folga pra crescer muito em estoque e prazo.
3. Depreciação de 2.000/mês é consumo real de riqueza: em 5 anos os equipamentos precisam ser repostos, e isso não aparece no caixa hoje.

Veredito: operacionalmente boa (margem saudável, receita real), financeiramente apertada por timing. Se fevereiro recebe os 30.000, a situação normaliza.

## Erros que estavam na planilha antes (pra não repetir)

1. Balanço de abertura com Caixa 140.000 e Imobilizado zero. O empréstimo virou equipamento no mesmo dia: Caixa 20.000, Imobilizado 120.000. Erro propaga pro caixa final e pra base da depreciação.
2. Adiantamento de 15.000 lançado como ativo e dentro do lucro (55.000). Adiantamento recebido é passivo circulante e receita zero até entregar. Lucro da transação 1 é 40.000.
3. Materiais de 12.000 lançados em Imobilizado. Material de consumo não é imobilizado: Caixa (12.000), Estoque +4.500, Lucro (7.500) na mesma coluna.
4. Aluguel de 24.000 inteiro em Despesas Antecipadas, sem reconhecer os 8.000 de janeiro.
5. Depreciação (coluna 5) e juros (Ajustes) não lançados.
6. Numeração: a coluna 1' do template é o adiantamento, não o aluguel. Aluguel é a 2, materiais é a 3.

## Refinamento opcional (rigor de classificação)

Em 31/01/2026 a 1ª parcela do empréstimo (jan/2027, 24.000) está a 12 meses, então tecnicamente passaria pro passivo circulante (linha "Empréstimos" do template), deixando 96.000 no não circulante. Mesma lógica pros juros. O total do balanço não muda. Só aplica se a professora cobrou isso em aula; no padrão Marcus Dent ela deixou tudo no não circulante.

## Pegadinhas do caso

- "O dinheiro do empréstimo foi imediatamente utilizado": caixa de abertura é só o capital.
- "Recebeu adiantamento em dinheiro": entra no caixa, não entra na receita.
- "Pagou 3 meses de aluguel": só 1 mês é despesa.
- "Constatou que havia sobrado 4.500": despesa = compra − sobra, sobra é ativo.
- "Pagamento no 5º dia útil de fevereiro": despesa de janeiro, caixa de fevereiro.
- "Vida útil de 5 anos": base é 120.000 (todo o imobilizado), não o material.
- Juros de 1,5% a.m. não aparecem nas transações numeradas, mas correm todo mês: despesa sem caixa.

## Pra fixar

- [[Regime de Caixa]]
- [[Regime de Competência]]
- [[DRE]]
- [[DFC]]
- [[Depreciação]]
- [[Despesa Antecipada]]
- [[Adiantamento de Cliente]]
- [[Estoque]]
