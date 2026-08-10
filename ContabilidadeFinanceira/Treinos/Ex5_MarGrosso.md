---
materia: ContabilidadeFinanceira
tema: Treino de elaboração das DFs
nivel: dificil
tags: [treino, exercicio]
---

# Ex5. Cervejaria Mar Grosso S.A.

**Nível:** difícil | **Transações:** 12 | **Tempo alvo:** 45 min | **Planilha:** `Ex5_MarGrosso.xlsx`

**Valores em R$ mil.**

## Contexto do negócio

A Mar Grosso é uma cervejaria artesanal de Florianópolis que virou sociedade anônima depois de crescer para fora do estado. Está no segundo ano de operação e o cenário é bem mais complexo que o dos casos anteriores: tem imobilizado depreciando, dívida bancária com juros, um cliente corporativo que paga adiantado, imposto de renda a recolher e acionistas esperando dividendo. O conselho quer as três demonstrações do ano 2 e a explicação de por que o lucro de 63 não virou 63 de caixa.

## Balanço inicial (início do ano 2)

| Ativo | R$ mil | Passivo e PL | R$ mil |
|---|---|---|---|
| Caixa | 40 | Fornecedores | 70 |
| Contas a Receber | 60 | Empréstimos | 100 |
| Estoques | 90 | Capital Social | 200 |
| Imobilizado | 300 | Lucros Acumulados | 60 |
| (-) Depreciação Acumulada | (60) | | |
| **Total** | **430** | **Total** | **430** |

Esses saldos já vêm preenchidos na coluna "Balanço Inicial" da planilha. Repare que a depreciação acumulada entra como número negativo, porque é conta redutora do ativo.

## Transações (Ano 2)

1. **Vendas do ano:** 520, sendo 380 à vista e 140 a prazo. O custo das mercadorias vendidas foi de 300.
2. **Compras do ano:** 330 de estoque, integralmente a prazo.
3. **Recebimento de clientes:** 95 recebidos de vendas de anos anteriores.
4. **Pagamento a fornecedores:** 310.
5. **Adiantamento de cliente:** um distribuidor corporativo paga 25 adiantado por uma encomenda especial que só será produzida e entregue no ano 3.
6. **Despesas:** 90 de despesas de vendas e administrativas, pagas à vista.
7. **Depreciação:** o imobilizado deprecia 30 no ano.
8. **Nova dívida:** capta 80 de empréstimo bancário.
9. **Serviço da dívida:** amortiza 50 do principal e paga 10 de juros do período.
10. **Expansão:** compra um novo forno de maltagem por 120, pagando 45 à vista e 75 em financiamento de longo prazo.
11. **Tributos:** o IR e a CSLL do ano somam 27, dos quais 20 são pagos à vista e 7 ficam a recolher no ano 3.
12. **Distribuição:** declara e paga 25 de dividendos.

## Pede-se

a) Registre o efeito de cada transação na Equação do Balanço (aba `Equação`).

b) Elabore o Balanço Patrimonial, a DRE completa e a DFC na aba `Plan`, uma coluna por transação. A DRE aqui tem a escada inteira, de receita líquida até lucro líquido, passando por EBIT e LAIR.

c) Monte também o FCO pelo método indireto, fora da planilha, e confirme que ele bate com o FCO da DFC direta.

d) Responda às perguntas abaixo.

## Perguntas de análise

1. O adiantamento de 25 da transação 5 entra na receita do ano 2?
2. A depreciação de 30 reduz o lucro mas não o caixa. Onde ela aparece em cada uma das três demonstrações?
3. O forno custou 120, mas o fluxo de investimento mostra apenas 45 de saída. Cadê os outros 75?
4. Na transação 9, por que os 50 de principal e os 10 de juros vão para lugares diferentes?
5. Monte o FCO pelo método indireto partindo do lucro líquido de 63 e mostre que chega em 70.
6. Prove que o PL final é igual ao PL inicial mais o lucro líquido menos os dividendos.
7. A empresa está saudável?

> [!tip]- Respostas
> 1. Não. Vira passivo, na conta de adiantamentos de clientes, porque a obrigação de entregar a encomenda ainda existe. A receita só é reconhecida no ano 3, quando a cervejaria entregar. No caixa, entra agora, e é fluxo operacional. É o caso mais limpo de descolamento entre caixa e [[Regime de Competência]]: o dinheiro chegou antes do fato gerador.
> 2. Três aparições da mesma figura. Na [[DRE]], é despesa e derruba o EBIT em 30. No [[Balanço Patrimonial]], engorda a depreciação acumulada de 60 para 90, reduzindo o imobilizado líquido. Na [[DFC]] montada pelo método direto, ela simplesmente não aparece, porque nenhum caixa se moveu. Se você montasse pelo [[Método Indireto]], ela voltaria somando logo abaixo do lucro líquido.
> 3. Foram financiados pelo vendedor em longo prazo. Não passaram pelo caixa no ano 2, então não entram no fluxo de investimento agora. Viram passivo não circulante e vão consumir caixa nos anos seguintes. No balanço, o imobilizado sobe pelos 120 cheios, porque o forno já é da empresa.
> 4. Porque são naturezas diferentes. O principal é devolução de capital de terceiros, movimento com o financiador, e vai para o fluxo de financiamento. Os juros são o preço do dinheiro naquele ano, despesa financeira na DRE e saída operacional na DFC pela convenção brasileira. Confundir os dois faz o FCO parecer melhor ou pior do que é.
> 5. Lucro líquido 63, mais depreciação 30, dá 93. Menos o aumento de contas a receber de 45 (de 60 para 105). Menos o aumento de estoques de 30 (de 90 para 120). Mais o aumento de fornecedores de 20 (de 70 para 90). Mais o aumento de adiantamentos de 25. Mais o aumento de IR a pagar de 7. Resultado: 70, idêntico ao FCO da DFC direta. Repare que o único ajuste sem efeito caixa é a depreciação, todo o resto é [[Capital de Giro]].
> 6. PL inicial de 260 (200 de capital mais 60 de lucros acumulados), mais lucro líquido de 63, menos dividendos de 25, dá 298. No balanço final, capital social de 200 mais lucros acumulados de 98 dá exatamente 298. Não houve aporte no ano, então a variação do PL é integralmente explicada por resultado e distribuição.
> 7. Sim, com uma ressalva. A operação gera 70 de caixa e a margem bruta de 42,3% é consistente para cervejaria. O FCO de 70 banca o capex à vista de 45 e ainda sobra. Mas a empresa cresceu o imobilizado em 120 usando 75 de financiamento novo e ainda tomou 80 de empréstimo, então a alavancagem subiu: o capital de terceiros foi de 170 para 327 enquanto o PL foi de 260 para 298. O PL agora financia 47,7% do ativo, contra 60,5% no início do ano. Distribuir 25 de dividendo nesse contexto é defensável, mas aperta.

## O que esse exercício treina

Todas as sete conexões entre as demonstrações de uma vez: lucro líquido como dobradiça, o triângulo da [[Depreciação]], o ciclo do [[Capex]], o capital de giro como ponte entre competência e caixa, principal e juros separados, dividendo fora da DRE, e o fechamento do caixa. Se você monta esse sem consultar nada, o tema 3 está dominado.

## Antes de conferir o gabarito

- A linha "Diferença, se houver" deu zero nas doze colunas de transação, não só na final?
- A depreciação da transação 7 entra negativa na conta de depreciação acumulada. Se você somou positivo, o ativo cresceu em vez de cair.
- A transação 11 mexe em três contas do balanço, não duas.
- O caixa final da DFC bate com os 70 do balanço?
- O FCO direto e o indireto chegaram no mesmo número?
