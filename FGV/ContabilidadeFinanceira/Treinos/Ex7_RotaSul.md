---
materia: ContabilidadeFinanceira
tema: Treino de elaboração das DFs
nivel: dificil
tags: [treino, exercicio]
---

# Ex7. Transportadora Rota Sul S.A.

**Nível:** difícil | **Transações:** 17 | **Tempo alvo:** 55 min | **Planilha:** `Ex7_RotaSul.xlsx`

**Valores em R$ mil.**

## Contexto do negócio

A Rota Sul opera fretes rodoviários no Sul e Sudeste. O ativo dela é a frota, e a gestão do negócio é em boa parte gestão de caminhão: comprar, rodar, depreciar e vender antes que o custo de manutenção estoure. No ano 4 a empresa renovou parte da frota, vendendo duas unidades antigas e comprando duas novas, e teve problemas de inadimplência com um cliente grande.

Esse caso introduz três coisas que os anteriores não tinham: resultado na venda de ativo imobilizado, baixa de estoque obsoleto e provisão para devedores duvidosos. As três têm a mesma característica incômoda: o número que aparece na DRE não é o número que aparece na DFC.

## Balanço inicial (início do ano 4)

| Ativo | R$ mil | Passivo e PL | R$ mil |
|---|---|---|---|
| Caixa | 60 | Fornecedores | 80 |
| Contas a Receber | 200 | Empréstimos | 200 |
| (-) Provisão p/ Devedores Duvidosos | (10) | Capital Social | 300 |
| Estoque de Peças | 70 | Lucros Acumulados | 100 |
| Imobilizado (frota) | 600 | | |
| (-) Depreciação Acumulada | (240) | | |
| **Total** | **680** | **Total** | **680** |

## Transações (Ano 4)

1. **Receita de fretes:** 920 no ano, sendo 620 recebidos à vista e 300 a prazo.
2. **Manutenção:** consumo de 45 de peças da oficina nas manutenções da frota.
3. **Custos de operação:** 540 pagos à vista, entre combustível, pedágio e salários de motoristas.
4. **Reposição de peças:** compra de 60, integralmente a prazo.
5. **Venda de ativo:** vende à vista um caminhão por 50. Ele custou 180 e tinha 150 de depreciação acumulada.
6. **Venda de ativo:** vende à vista outro caminhão por 25. Ele custou 120 e tinha 80 de depreciação acumulada.
7. **Renovação da frota:** compra dois caminhões novos por 260, pagando 100 à vista e financiando 160 em longo prazo.
8. **Depreciação do ano:** 70.
9. **Obsolescência:** baixa de 12 de peças de modelos que saíram da frota.
10. **Inadimplência esperada:** constituição de provisão para devedores duvidosos de 18.
11. **Inadimplência confirmada:** baixa definitiva de um cliente incobrável de 14, consumindo a provisão já constituída.
12. **Recebimento de clientes:** 240.
13. **Pagamento a fornecedores:** 95.
14. **Despesas administrativas:** 110 no ano, pagas à vista.
15. **Serviço da dívida:** paga 20 de juros e amortiza 40 do principal.
16. **Tributos:** IR e CSLL de 33, pagos integralmente à vista.
17. **Distribuição:** dividendos de 20 declarados e pagos em dinheiro.

## Pede-se

a) Registre o efeito de cada transação na Equação do Balanço (aba `Equação`).

b) Elabore o Balanço Patrimonial, a DRE e a DFC na aba `Plan`.

c) Monte o FCO pelo método indireto, fora da planilha, e confirme que bate com a DFC direta.

d) Responda às perguntas abaixo.

## Perguntas de análise

1. O caminhão da transação 5 foi vendido por 50, mas a DRE mostra 20. Por quê? E qual dos dois números vai para a DFC?
2. Na transação 6 a empresa registra uma perda de 15. Ela perdeu 15 de dinheiro nessa operação?
3. A baixa do cliente incobrável de 14 não aparece na DRE. Por quê?
4. Ao montar o FCO pelo indireto, o que você faz com o resultado da venda de imobilizado?
5. A frota da empresa encolheu ou cresceu no ano?
6. A Rota Sul está saudável?

> [!tip]- Respostas
> 1. Porque a DRE registra **resultado**, não preço. O valor contábil do caminhão era 180 de custo menos 150 de depreciação acumulada, ou seja, 30. Vendido por 50, sobra um ganho de 20, e é esse o número que vai para a DRE. Na DFC vai o preço inteiro, 50, no fluxo de investimento, porque foi isso que entrou na conta bancária. É o descolamento mais comum entre as duas demonstrações em alienação de ativo.
> 2. Não. Ela **recebeu** 25 de dinheiro. A perda é puramente contábil: o caminhão estava registrado por 40 nos livros (120 menos 80) e o mercado pagou só 25. O que a perda diz é que a depreciação acumulada estava subestimada, o ativo valia menos do que o balanço mostrava. Entrada de caixa com perda contábil no mesmo evento.
> 3. Porque a despesa já foi reconhecida lá atrás, quando a provisão foi constituída. A provisão é justamente o reconhecimento antecipado da perda esperada. Quando o calote se confirma, você só consome a provisão que já existia: sai o direito de contas a receber e some a provisão correspondente. Registrar despesa de novo seria contar a mesma perda duas vezes.
> 4. Tira ele. O resultado líquido das duas vendas é um ganho de 5, e ele precisa sair do FCO porque o caixa inteiro dessas operações, os 75, já está no fluxo de investimento. Se deixasse os 5 no FCO, você contaria parte do mesmo dinheiro nos dois blocos. Conferindo: lucro 77, mais depreciação 70, menos o ganho de 5, menos o aumento de 42 de contas a receber líquidas de provisão, menos o aumento de 3 do estoque, menos a queda de 35 de fornecedores, dá 62. Igual à DFC direta. Repare que a perda com estoque obsoleto e a despesa de provisão **não** entram como ajuste separado: elas já estão embutidas na variação do estoque e do contas a receber líquido. Somar de novo seria contar duas vezes.
> 5. Cresceu, apesar de ter vendido dois caminhões. O custo bruto foi de 600 para 560, então em valor de nota a frota encolheu. Mas o valor contábil líquido foi de 360 para 480, porque saíram unidades quase totalmente depreciadas e entraram unidades novas. Olhar só o imobilizado bruto engana, o que importa é o líquido de depreciação.
> 6. Razoável, com uma ressalva. O FCO de 62 cobre o capex líquido de 25 e sobra. A margem líquida de 8,4% é magra mas típica de transporte rodoviário, que é negócio de ativo pesado e margem apertada. O ponto de atenção é a inadimplência: a empresa reconheceu 18 de perda esperada e confirmou 14 de calote no ano, somando cerca de 3,5% da receita virando problema de crédito. E o contas a receber fechou em 246 contra receita de 920, o que dá quase 98 dias de faturamento parado na mão do cliente. Prazo longo desses em setor de margem fina é o começo de um problema de caixa.

## O que esse exercício treina

Os três casos em que o número da DRE e o número da DFC são diferentes por natureza, não por prazo: alienação de ativo, baixa de estoque e provisão. Também treina a leitura do imobilizado líquido contra o bruto, e o ajuste de itens não caixa no método indireto sem contar duas vezes.

## Antes de conferir o gabarito

- A linha "Diferença, se houver" deu zero nas dezessete colunas?
- Nas transações 5 e 6 você mexeu em quatro contas cada: caixa, imobilizado, depreciação acumulada e lucros acumulados. Se mexeu em menos, faltou alguma.
- A depreciação acumulada **cai** quando o caminhão é vendido, porque a depreciação daquele bem sai junto com ele. No teu balanço ela entra positiva nessas duas colunas.
- A transação 11 tem efeito zero no total do ativo e nada no lado direito.
- As transações 2, 8, 9, 10 e 11 não tocam a DFC.
