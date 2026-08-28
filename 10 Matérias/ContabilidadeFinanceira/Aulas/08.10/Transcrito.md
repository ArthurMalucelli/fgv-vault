---
materia: ContabilidadeFinanceira
data: 2026-08-10
tema: Exercício prático (Loja da Sofia) - registro pela equação patrimonial, montagem de BP/DRE/DFC em planilha e leitura dos relatórios
topicos: [equação patrimonial, balanço patrimonial, DRE, DFC método direto, margem bruta, margem líquida, liquidez, lucros acumulados, dividendos, DMPL]
tags: [aula, transcrito]
---

## O exercício

A turma trabalha em grupos no caso da Sofia, que acabou de abrir uma loja. O pedido: mostrar como está o valor da empresa depois de uma série de transações do primeiro mês. Cada grupo registra o efeito de cada transação na [[Equação Patrimonial]] e depois monta [[Balanço Patrimonial]], [[DRE]] e [[DFC]] numa planilha integrada.

## As seis transações

Cada transação é lançada nos dois lados da equação, sempre com contrapartida:

**1. Aporte de capital.** Sofia integraliza R$60.000 em dinheiro pra abrir a loja.
- Ativo: caixa +60.000
- Patrimônio líquido: capital social +60.000

**2. Compra de imobilizado (prateleiras).** A loja compra móveis e prateleiras, pagos à vista.
- Ativo: imobilizado +25.000, caixa -25.000
- Classificação no DFC: atividade de investimento, porque é gasto ligado a ativo não circulante, não ao dia a dia da operação.

**3. Compra de mercadoria.** Compra de estoque de R$50.000, parte à vista e parte a prazo.
- Ativo: estoque +50.000, caixa -30.000
- Passivo: fornecedores (contas a pagar) +20.000

**4. Venda de mercadoria.** Vende à vista por R$45.000 mercadoria que tinha custado R$25.000.
- Ativo: caixa +45.000, estoque -25.000
- Patrimônio líquido: lucros acumulados +20.000 (o lucro bruto da venda)

**5. Despesa de marketing.** Gasta R$12.000 com marketing, pago em caixa. O professor usa essa transação pra fixar um ponto conceitual: marketing não é um ativo, porque o gasto em si não gera valor, ele gera receita futura. Portanto é despesa, consome patrimônio líquido.
- Ativo: caixa -12.000
- Patrimônio líquido: lucros acumulados -12.000

**6. Pagamento de dívida.** Paga R$10.000 de uma dívida que tinha com os fornecedores.
- Ativo: caixa -10.000
- Passivo: fornecedores -10.000

## Montando a planilha integrada

Depois de resolver as seis transações no papel, a turma reproduz o exercício numa planilha. A lógica que o professor ensina, célula por célula:

Cada linha de conta (caixa, estoque, fornecedores, capital social...) soma tudo que foi lançado nela ao longo das seis transações: `=SOMA()` da faixa de colunas de lançamento. Copia a fórmula pra todas as linhas.

O total do ativo e o total do passivo mais patrimônio líquido são somados separadamente, e depois entra a linha de checagem: **diferença do balanço**, igual à soma do ativo menos a soma do passivo mais PL. Tem que dar zero em todas as colunas. Se aparecer qualquer coisa diferente de zero, tem erro de lançamento em algum lugar. Essa checagem é o motivo de a planilha existir: ela mostra o efeito de cada transação e, ao mesmo tempo, controla visualmente se a equação continua batendo depois de cada uma.

Uma célula puxa direto o número já lançado no balanço em vez de ser digitada de novo (por exemplo, a compra do imobilizado referenciada de volta na hora de montar o DFC). A regra: sempre que possível, referenciar em vez de redigitar. Reduz erro.

## Do balanço para a DRE

Com o balanço fechado, a turma monta a demonstração de resultado com os mesmos números, isolando os efeitos que passaram pelo patrimônio líquido:

```
Receita de vendas                    45.000
(-) Custo da mercadoria vendida     (25.000)
= Lucro bruto                        20.000
(-) Despesa de marketing            (12.000)
= Lucro líquido                       8.000
```

O professor pede pra somar em duas etapas (primeiro o [[Lucro Bruto]], depois o lucro líquido puxando o bruto pra baixo e somando as despesas), pra deixar os subtotais intermediários visíveis na planilha, não só o resultado final.

## DFC pelo método direto

A parte central do exercício: pegar os mesmos lançamentos de caixa e reclassificá-los em três blocos, sem calcular nada de novo, só reclassificar o que já está na planilha (**[[Método Direto]]**, diferente do método indireto que parte do lucro líquido e faz ajustes).

O professor é explícito sobre a ordem de raciocínio: a operação nunca começa pelo negativo. O primeiro item é sempre a principal entrada de caixa da operação, que numa loja é recebimento de clientes. Depois vêm as saídas: pagamento a fornecedores é a principal, e o resto entra genericamente como pagamento de despesas.

Classificação de cada fluxo:

```
Operação (FCO)
  Recebimento de clientes              +45.000
  Pagamento a fornecedores             (30.000)  [compra de estoque à vista]
  Pagamento de despesas (marketing)    (12.000)
  Pagamento a fornecedores             (10.000)  [quitação de dívida]
  = FCO                                 (7.000)

Investimento (FCI)
  Compra de imobilizado                (25.000)
  = FCI                                (25.000)

Financiamento (FCF)
  Aporte de capital                    +60.000
  = FCF                                 60.000

Variação de caixa = FCO + FCI + FCF = 28.000
Caixa inicial (0) + Variação (28.000) = Caixa final (28.000)
```

A checagem final do DFC é a mesma lógica da checagem do balanço: o saldo final de caixa da demonstração tem que bater exatamente com a linha de caixa do balanço na mesma data. Se não bater, é erro de classificação em algum lançamento.

## O que os relatórios mostram sobre a Sofia

Com tudo montado, o professor pergunta o que dá pra concluir sobre a empresa a partir de cada relatório.

**Pelo balanço**: a empresa tem caixa, patrimônio líquido positivo e já teve lucro no primeiro mês, então a leitura inicial é favorável. Olhando liquidez ([[Ativo Circulante]] contra passivo circulante): ativo circulante de cerca de R$53.000 (caixa mais estoque) contra R$10.000 de dívida de curto prazo com fornecedores. Não há risco de não conseguir pagar as dívidas no curto prazo.

**Pela DRE**: [[Margem Bruta]] de 44% (lucro bruto de 20 sobre receita de 45), o que é uma margem forte. [[Margem Líquida]] de cerca de 18% (lucro líquido de 8 sobre receita de 45), também considerada boa pra um varejo desse tipo.

**Pelo DFC**: aqui está o alerta. A operação sozinha (FCO) é negativa em R$7.000: entrou 45 mas saiu 52 (40 de pagamento a fornecedores mais 12 de marketing). Isso não significa que a empresa deu prejuízo, ela teve lucro contábil de 8. O problema é de tempo: a Sofia está pagando o fornecedor mais rápido do que está vendendo o estoque. Pagou 40 aos fornecedores enquanto o custo da mercadoria já vendida foi só 25, ou seja, uma parte do que ela pagou é estoque que ainda não virou venda. Se o fornecedor desse mais prazo, ou se ela esperasse vender antes de pagar tudo, o caixa da operação não ficaria negativo. Não é um problema grave ainda, porque o financiamento (o aporte de capital) cobre a diferença e o caixa final segue positivo, mas é o primeiro sinal de que a empresa pode precisar de financiamento de capital de giro se esse padrão continuar.

## Lucros acumulados: por que nem sempre começam do zero

Como é o primeiro mês da loja, o saldo inicial de lucros acumulados é zero e o saldo final é igual ao lucro do período (8). Mas isso é uma particularidade de empresa nova. Numa empresa que já opera há anos, lucros acumulados é o saldo que a empresa já tinha acumulado até o início do período, mais o lucro gerado agora. É o conceito de acumulação: ganhar mais do que gasta, mês após mês, faz o saldo crescer com o tempo.

O professor usa um exemplo hipotético pra ilustrar o efeito de distribuir lucro em vez de reinvestir: se a Sofia decidisse sacar parte do lucro que a empresa gerou (como sócia, ela tem esse direito), a empresa continuaria bem, com margem de 18% igual antes. O que muda é a composição do balanço: antes o patrimônio líquido representava cerca de 69% do ativo total (riqueza acumulada), e com o saque cai pra algo em torno de 60%. Na medida em que o sócio retira o lucro gerado em vez de reinvestir, a empresa não acumula patrimônio, mesmo continuando lucrativa. O caso extremo, que a turma vai ver numa aula futura, é o de um empreendedor que retira todo o lucro gerado pra sustentar o próprio padrão de vida: a empresa dá lucro contábil todo período, mas nunca cresce patrimonialmente, porque nada fica retido.

O normal nas empresas reais é um meio-termo: reinveste uma parte e distribui outra, com a proporção variando (algo entre 40% e 60% de distribuição, dependendo da necessidade de crescimento da empresa).

## Fechamento: qual relatório responde qual pergunta

Uma aluna nota que, ao olhar só a DRE, o lucro dá uma coisa, mas o saldo final de lucros acumulados no balanço é outro, porque no meio do caminho teve distribuição de dividendos. O professor esclarece: a DRE mostra o lucro gerado no período, cheio, sem descontar distribuição nenhuma. A distribuição de dividendos não é uma despesa, é uma decisão sobre o que fazer com o lucro depois de apurado, então ela não aparece na DRE. O relatório que mostra essa movimentação (lucro gerado, mais o que entrou, menos o que foi distribuído) é a **[[DMPL]]**, a demonstração das mutações do patrimônio líquido.
