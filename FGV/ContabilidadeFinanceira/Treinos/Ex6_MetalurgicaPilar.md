---
materia: ContabilidadeFinanceira
tema: Treino de elaboração das DFs
nivel: dificil
tags: [treino, exercicio]
---

# Ex6. Metalúrgica Pilar S.A.

**Nível:** difícil | **Transações:** 14 | **Tempo alvo:** 45 min | **Planilha:** `Ex6_MetalurgicaPilar.xlsx`

**Valores em R$ mil.**

## Contexto do negócio

A Pilar fabrica peças estampadas para a indústria automotiva. É a primeira indústria destes treinos, e isso muda a espinha dorsal do caso: no comércio a mercadoria entra pronta e sai pronta, aqui ela entra como chapa de aço e sai como peça. O estoque se parte em três estágios, matéria-prima, produtos em elaboração e produtos acabados, e tudo que é gasto para fabricar fica **dentro do estoque** até a peça ser vendida.

Isso significa que salário de fábrica e depreciação de máquina não são despesa do período. São custo de produção, ficam guardados no balanço, e só viram linha de DRE quando o produto sai pela porta.

## Balanço inicial (início do ano 3)

| Ativo | R$ mil | Passivo e PL | R$ mil |
|---|---|---|---|
| Caixa | 110 | Fornecedores | 90 |
| Contas a Receber | 80 | Salários a Pagar | 20 |
| Estoque de Matéria-Prima | 40 | Empréstimos | 150 |
| Produtos em Elaboração | 20 | Capital Social | 260 |
| Produtos Acabados | 60 | Lucros Acumulados | 70 |
| Imobilizado | 400 | | |
| (-) Depreciação Acumulada | (120) | | |
| **Total** | **590** | **Total** | **590** |

## Transações (Ano 3)

1. **Compra de insumos:** matéria-prima por 260, sendo 60 à vista e 200 a prazo.
2. **Requisição para a produção:** 250 de matéria-prima saem do almoxarifado e entram na linha.
3. **Folha da fábrica:** 180 no ano, apropriados ao custo de produção.
4. **Pagamento de salários:** 190 em dinheiro, incluindo os 20 que a empresa devia do ano anterior.
5. **Depreciação do ano:** 40, sendo 30 das máquinas da fábrica e 10 dos móveis do escritório.
6. **Produção concluída:** 470 transferidos de produtos em elaboração para produtos acabados.
7. **Vendas do ano:** 700, sendo 450 à vista e 250 a prazo. O custo dos produtos vendidos foi de 480.
8. **Recebimento de clientes:** 210 referentes a vendas de anos anteriores.
9. **Pagamento a fornecedores:** 230.
10. **Despesas comerciais e administrativas:** 90 no ano, pagas à vista.
11. **Investimento:** compra à vista de uma nova prensa por 60.
12. **Serviço da dívida:** paga 20 de juros e amortiza 50 do principal.
13. **Tributos:** IR e CSLL de 30, pagos integralmente à vista.
14. **Distribuição:** dividendos de 25 declarados e pagos em dinheiro.

## Pede-se

a) Registre o efeito de cada transação na Equação do Balanço (aba `Equação`).

b) Elabore o Balanço Patrimonial, a DRE e a DFC na aba `Plan`. Atenção às três contas de estoque, o material circula entre elas.

c) Monte o FCO pelo método indireto, fora da planilha, e confirme que bate com a DFC direta.

d) Responda às perguntas abaixo.

## Perguntas de análise

1. A folha da fábrica de 180 não aparece em lugar nenhum da DRE. Onde ela foi parar?
2. Da depreciação de 40 do ano, só 10 aparecem na DRE. Por quê?
3. Ao montar o FCO pelo indireto, você soma de volta 40 de depreciação ou só os 10 que passaram pela DRE?
4. O lucro do ano foi de 70 e o caixa caiu 95. Reconstrua essa diferença.
5. Se a Pilar quisesse inflar o lucro do ano sem vender uma peça a mais, o que ela poderia fazer com a produção?

> [!tip]- Respostas
> 1. Dentro do estoque. Os 180 entraram em produtos em elaboração, seguiram para produtos acabados junto com a produção concluída, e só chegaram na DRE como parte dos 480 de custo dos produtos vendidos. O pedaço que corresponde às peças que ainda não foram vendidas continua parado no balanço, dentro dos 10 de produtos em elaboração e dos 50 de produtos acabados. Salário de fábrica não é despesa do período, é custo capitalizado no produto.
> 2. Mesma lógica. Os 30 das máquinas são custo de produção e foram capitalizados no estoque junto com a matéria-prima e a folha. Os 10 do escritório não têm produto nenhum para carregar, então viram despesa do período direto. Mesma máquina depreciando, dois destinos contábeis diferentes conforme a função.
> 3. Soma os 40 inteiros. Parece errado à primeira vista, já que 30 nem passaram pela DRE, mas a conta se ajusta sozinha pela variação dos estoques: os 30 que ficaram guardados aparecem como aumento de estoque, que entra negativo no [[Capital de Giro]] e cancela exatamente a parte indevida. Conferindo: lucro 70, mais depreciação 40, mais a queda de estoques de 10, menos o aumento de contas a receber de 40, menos a queda de fornecedores de 30, menos a queda de salários a pagar de 10, dá 40. É o mesmo FCO da DFC direta.
> 4. O FCO foi de 40 e não cobriu nada do resto. Saíram 60 de capex na prensa, 50 de amortização de dívida e 25 de dividendo. Somando, 135 de saída contra 40 de geração, o que derruba o caixa em 95. A empresa pagou dívida e sócio com caixa que a operação não gerou.
> 5. Produzir mais do que vende. Produzindo em excesso, uma fatia maior da folha de fábrica e da depreciação fica guardada no estoque em vez de virar custo do período, o custo unitário cai e o lucro sobe sem que uma peça a mais tenha sido vendida. O estoque incha no balanço e o FCO piora, mas a DRE fica bonita. É por isso que estoque crescendo muito mais rápido que a receita é sinal de alerta em indústria.

## O que esse exercício treina

A diferença entre gasto que vira despesa e gasto que vira ativo, aplicada dentro do estoque. É a mesma discussão de capitalizar contra despesar, só que em vez de imobilizado o destino é o produto em fabricação. Também treina o método indireto num caso onde a depreciação está partida entre DRE e estoque, que é a situação real de qualquer indústria.

## Antes de conferir o gabarito

- A linha "Diferença, se houver" deu zero nas catorze colunas?
- As transações 2, 3 e 6 não tocam nem a DRE nem a DFC. São movimentos internos do estoque e de dívida. Deixou as três em branco nos dois relatórios?
- Produtos em Elaboração recebe quatro entradas e uma saída. Fechou em 10?
- A depreciação da fábrica entra somando em produtos em elaboração e a acumulada entra negativa. Os dois lançamentos são da mesma transação.
