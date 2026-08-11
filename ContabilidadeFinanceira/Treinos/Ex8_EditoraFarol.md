---
materia: ContabilidadeFinanceira
tema: Treino de elaboração das DFs
nivel: dificil
tags: [treino, exercicio]
---

# Ex8. Editora Farol S.A.

**Nível:** difícil | **Formato diferente** | **Tempo alvo:** 50 min | **Planilha:** `Ex8_EditoraFarol.xlsx`

**Valores em R$ mil.**

## O que muda aqui

Nos sete anteriores você recebeu a lista de transações e construiu as demonstrações a partir dela. Ninguém trabalha assim fora da sala de aula. Analista, investidor e banco não veem transação, veem relatório publicado, e a DFC quase sempre vem pelo método indireto, resumida.

Aqui o exercício é o inverso. Você recebe **dois balanços consecutivos e a DRE do ano 2**, e tem que reconstruir a DFC inteira de trás para frente. Nenhuma transação é dada. Cada número da DFC tem que ser deduzido da variação de uma conta do balanço combinada com uma linha da DRE.

O princípio que sustenta tudo: **toda variação de conta do balanço entre duas fotos tem que ser explicada**. Se você não consegue explicar, tem informação faltando ou erro de raciocínio.

## Dados

Os dois balanços, a DRE e as informações adicionais estão na aba `Dados` da planilha. Resumo do que você tem:

| | Ano 1 | Ano 2 |
|---|---|---|
| Caixa e Equivalentes | 90 | 145 |
| Contas a Receber | 320 | 395 |
| Estoques | 210 | 180 |
| Despesas Antecipadas | 15 | 25 |
| Imobilizado | 800 | 960 |
| (-) Depreciação Acumulada | (280) | (340) |
| **Total do Ativo** | **1.155** | **1.365** |
| Fornecedores | 240 | 285 |
| Salários e Encargos a Pagar | 45 | 38 |
| IR a Pagar | 30 | 42 |
| Empréstimos de Curto Prazo | 100 | 130 |
| Empréstimos de Longo Prazo | 260 | 300 |
| Capital Social | 300 | 350 |
| Lucros Acumulados | 180 | 220 |

Na DRE do ano 2: receita líquida de 1.680, lucro bruto de 670, depreciação de 95, perda na venda de imobilizado de 12, EBIT de 163, resultado financeiro de 45 negativos, IR de 38 e lucro líquido de 80.

Informações adicionais na aba `Dados`, incluindo a venda de um equipamento e a movimentação de empréstimos.

## Pede-se

a) **Parte A:** monte o FCO pelo método indireto, o fluxo de investimento e o fluxo de financiamento. Confirme que a variação total do caixa reproduz exatamente a diferença entre os dois balanços.

b) **Parte B:** monte o mesmo FCO pelo método direto, deduzindo cada recebimento e cada pagamento a partir da DRE e das variações de capital de giro. Os dois métodos têm que dar o mesmo número.

c) Responda às perguntas abaixo.

## Roteiro sugerido

Antes de escrever qualquer coisa na DFC, preencha a coluna Variação do balanço e ataque conta por conta:

- **Imobilizado**: subiu 160 no líquido, mas teve venda e depreciação no meio. Qual foi o capex de verdade?
- **Depreciação acumulada**: subiu 60, mas a despesa do ano foi 95. O que consumiu a diferença?
- **Lucros acumulados**: subiu 40, mas o lucro foi 80. Cadê os outros 40?
- **Capital social**: subiu 50. Entrou dinheiro ou foi capitalização de lucro?
- **Empréstimos**: o total subiu 70, mas as informações adicionais dão a captação e a amortização separadas.

## Perguntas de análise

1. Qual foi o capex do ano, e como você chegou nesse número?
2. Quanto de dividendo foi pago?
3. O lucro foi de 80 e o FCO deu 182. De onde vem uma diferença dessas?
4. O FCO de 182 cobriu o capex? Como a empresa financiou o que faltou?
5. Calcule o fluxo de caixa livre (FCO menos capex). Fazia sentido pagar dividendo nesse ano?
6. Olhando só a DRE, a empresa parece boa ou ruim? E olhando a DFC?

> [!tip]- Respostas
> 1. Capex de 235. O imobilizado bruto foi de 800 para 960, uma variação líquida de 160. Mas saiu um equipamento de 75 de custo na venda. Logo, 800 menos 75 mais capex igual a 960, o que dá 235. Quem esquece a baixa acha 160 e erra o número mais importante da análise.
> 2. Dividendo de 40. Lucros acumulados foi de 180 para 220, uma alta de 40, e o lucro do ano foi 80. A diferença só pode ter saído como distribuição. Confirma o elo: PL final igual a PL inicial mais lucro menos dividendo.
> 3. Cento e sete de despesa que não é caixa: 95 de depreciação e 12 de perda na venda do equipamento. O [[Capital de Giro]] ainda consumiu 5 líquidos no ano (contas a receber tomou 75 e despesas antecipadas 10, enquanto estoques liberaram 30, fornecedores 45 e IR a pagar 12, com salários a pagar consumindo 7). Somando, 80 mais 107 menos 5 dá 182.
> 4. Não cobriu. FCO de 182 contra capex de 235 deixa um buraco de 53, e ainda foram pagos 40 de dividendo. O buraco total de 93 foi tapado com 70 líquidos de dívida nova (180 captados menos 110 amortizados) e 50 de aumento de capital em dinheiro. Ou seja, o crescimento do ano foi bancado por credor e por sócio, não por geração própria.
> 5. Fluxo de caixa livre de 182 menos 235, igual a 53 negativos. Pagar 40 de dividendo com fluxo livre negativo significa distribuir dinheiro que a empresa não gerou, financiado por dívida e por aporte. Não é ilegal nem necessariamente errado, mas é uma escolha que o analista tem que enxergar: se o capex é expansão com retorno claro, dá para defender. Se é reposição, a empresa está se descapitalizando para manter uma política de dividendo.
> 6. Pela DRE, decente: margem bruta de 39,9% e lucro líquido positivo de 80. Pela DFC, a leitura muda de tom: a operação gera caixa de verdade (182), mas a empresa está num ciclo de investimento pesado que ela não consegue bancar sozinha, e escolheu alavancar mais e chamar dinheiro do sócio em vez de segurar o dividendo. O caixa subiu 55 no ano, o que parece bom, mas subiu porque entrou dívida e aporte, não porque a operação sobrou. É o exemplo clássico de por que a DRE sozinha não decide nada.

## O que esse exercício treina

A habilidade que se usa de verdade em análise: reconstruir o movimento de caixa a partir de demonstrações publicadas, sem ter acesso ao razão. Também consolida o [[Método Indireto]], que é o formato que quase toda empresa aberta publica, e força a checagem dos dois lados, porque o direto e o indireto têm que convergir no mesmo FCO.

## Antes de conferir o gabarito

- A variação total do caixa que você montou reproduz exatamente os 55 de diferença entre os dois balanços?
- O FCO da parte A e o da parte B deram o mesmo número?
- Você lembrou de tirar a perda na venda do imobilizado do FCO, já que o caixa dessa operação está no investimento?
- Contas a receber subiu, então entra **negativo** no FCO. Estoques caíram, então entram positivo. Se você inverteu os sinais, o FCO sai errado por bem mais que o dobro do erro.
