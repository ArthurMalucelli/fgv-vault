---
materia: ProdutosFinanceiros
data: 2026-05-20
tema: Valuation por Dividendos e Retorno Esperado
topicos: [DDM, Modelo de Gordon, Dividend Yield, Retorno Esperado, Valor Terminal, Valor Intrinseco, WACC, CAPM]
tags: [aula, transcrito]
---

# Valuation por Dividendos e Retorno Esperado

## Abertura: capital investido vs. resultado, e o caso NVIDIA x Volkswagen

Aqui você tem dois casos com capital investido grande, mas resultados bem distintos. De um lado, o capital investido tem dificuldade pra se transformar em produto. Por outro, quando você pensa numa empresa como a NVIDIA, ela foi muito competente em identificar qual seria o negócio que ia fazer nos próximos anos, antecipou toda a discussão de inteligência artificial e se posicionou de tal maneira que aquele capital que ela tinha, lá quando decidiu investir agressivamente na produção do chip, virou uma decisão estratégica perfeita do ponto de vista da administração. A NVIDIA conseguiu converter esse capital investido, que é um capital muito caro, numa máquina de fazer dividendo nos próximos anos. Enquanto na Volkswagen isso não é verdade: a indústria automotiva tradicional, tirando a Ásia, tem tido um período bastante complicado pra gerar resultado positivo.

## O que o acionista recebe quando a empresa acaba

Como acionista, normalmente a gente não pensa "por que uma empresa acaba?". A intuição é que se ela tá funcionando, vai funcionar pra sempre. Empresa familiar, do pai passa pro filho, pro neto, e assim por diante. Quando uma empresa de maneira geral não se sustenta e entra em [[Recuperacao Judicial]], é porque não tem capacidade pra ter sucesso. Mas você pode ter o caso de uma empresa em condições normais em que o acionista decide encerrar as atividades. Não é algo regular, mas é importante pra entender o que o acionista tem na mão.

Se uma empresa encerra, seja por razões extrajudiciais ou por falência, o que você tende a receber só vem depois das despesas operacionais, obrigações trabalhistas e impostos serem pagos. Então quando uma empresa acaba, você ainda assim tem a receber um valor proporcional ao que restou. Pode ser, em muitos casos de recuperação judicial, que o valor a receber seja zero, porque ela solicitou falência justamente por não ter condição de arcar com as obrigações. Mas em outras circunstâncias pode ter saldo credor.

## Por que olhar pro dividendo

Por que trazer essa discussão? Porque quando a gente olha o fluxo de caixa de uma empresa, a gente pode abstrair de várias coisas que compõem esse fluxo. Ao longo da disciplina, vocês vão calcular o saldo profissional, depósito, lucro antes e depois do imposto de renda. Mas o que você quer chegar é no lucro que essa empresa teve ou no [[Dividendos|dividendo]] que ela vai pagar. Se você tem essa informação, só com ela você consegue uma projeção de quanto deveria custar o valor da empresa. Você não precisa passar por todas as contas contábeis pra fazer o [[Valuation]]. Se você só tem o dividendo projetado, mesmo assim você consegue chegar no valor da empresa com bastante precisão.

Isso é o que a gente chama de avaliar o [[Valor Intrinseco]] da empresa: o que ela realiza ao longo do tempo, gera de resultado e acaba pagando como dividendo.

## Por que dividendo importa: ações respondem rápido a choques em dividendo

Por que isso é relevante? Porque ações respondem rápido a choques em dividendos. Quando a gente olha, o lucro líquido do Bradesco caiu 22%, mas o impacto na ação foi praticamente da mesma magnitude. O resultado do trimestre sinalizou quase um pra um o preço da ação. Não foi marginal. Veja, os investidores não enxergam "ah, foi só no semestre, os próximos vão ser melhores". Quando você tem um impacto no dividendo, isso vai de maneira brutal impactar o preço da ação.

A narrativa que eu vou mostrar logo na sequência é que o preço de uma ação nada mais é do que um VPL, como vocês já viram várias vezes. E o que entra na fórmula é o dividendo. No fim, será o dividendo que é pago ao acionista. E o dividendo é função do lucro daquela empresa, mas não num momento único, sim ao longo de vários momentos. A empresa nunca acaba (em teoria), ela vai produzindo dividendos ao longo dos anos. Mas se num semestre o dividendo vem abaixo do esperado pelos analistas, o impacto é sentido naquele exato momento, ignorando toda a história que pode vir pra frente. Ação responde muito rápido.

## Outras formas de fazer valuation (e por que a gente foca em dividendo)

Essa não é a única maneira de fazer valuation. Vocês vão ver outras: análise técnica (eu tenho dificuldade de entender a fundamentação), análise pelo balanço, comparação por múltiplos.

Um dos múltiplos mais usados é a relação preço sobre earnings, o [[Price Earnings|P/E]]. Você quer entender quanto vale um banco que ainda não é negociado em bolsa? Pega um banco listado, calcula o P/E dele e usa essa relação pra extrapolar pro banco que não é listado. Isso é muito comum: empresa estabelecida serve de referência pra uma empresa que ainda vai listar.

P/E é uma relação de quantas vezes o preço da ação é em relação aos earnings da empresa. Se aparece 10x P/E, quer dizer que se uma empresa paga dividendo de R$ 10, o preço da ação seria R$ 100. É bem mecânico.

Mas o foco aqui vai ser o dividendo, por uma razão: em essência, é a última linha do balanço da empresa. Se a gente tem essa informação, a gente consegue fazer muita coisa. O principal método é o [[DDM]] (Dividend Discount Model), também chamado de [[Modelo de Gordon]] ou DCF (Discount Cash Flow). São todos sinônimos pro que a gente vai ver hoje.

## Por que o dividendo é o ponto certo de olhar

Os dividendos, na ótica do valor de uma empresa, são a informação que eu quero saber sobre quando o dinheiro vai entrar no meu bolso. Sendo acionista, eu sou sócio de uma empresa. A empresa não tem obrigação de pagar nada. Minha expectativa é receber, no curso das decisões, que o capital que eu investi se transforme em bons fluxos de caixa.

Então sim, eu quero valorização do capital. Se eu pago 100, idealmente eu queria que valesse 115, 120 ao longo do tempo. Mas eu também quero saber qual o resultado periódico que a empresa vai dar. O preço de uma ação vai ser formado pela expectativa desse movimento: quanto eu recebo de pagamento de dividendos e por quanto eu vou vender essa ação lá na frente.

Quando eu concentro só nisso, o preço de uma ação é o valor presente do fluxo dos dividendos esperados. A gente volta pro mundo que a gente já fez até agora: projeta o fluxo em vários períodos, traz a valor presente. A discussão toda passa a ser: a qual taxa?

## A taxa de desconto não é a [[Taxa Livre de Risco]]

Não vai ser a taxa livre de risco. Lembra que num CDB existia o risco de prêmio, então a remuneração tinha que ser taxa livre de risco mais [[Premio de Risco|prêmio de risco]]. No caso de uma ação é análogo: eu não posso simplesmente trazer fluxo de dividendos a taxa livre de risco, porque eu não tenho certeza de que aquele pagamento vai acontecer. É uma expectativa. Você tem que ajustar pelo risco que aquela empresa impõe.

Isso vocês vão ver na disciplina de finanças corporativas: é o cálculo do [[WACC]] (Weighted Average Cost of Capital). Quanto custa o capital pra essa empresa? Muitas vezes a empresa tem dívida, então captou dinheiro via dívida, e também tem dinheiro próprio. Você faz uma média dessas duas coisas. Esse é o conceito que vocês vão aprender no curso de administração financeira.

Pra estimar o R (custo de capital), o modelo mais comum é o [[CAPM]]. Vocês vão usar esse modelo pra encontrar a composição entre capital próprio e capital de terceiros. Mas toda essa parte aqui é matéria de finanças.

## Fórmula geral do preço de uma ação

O preço de uma ação é igual ao somatório dos dividendos em cada momento, divididos por (1 + taxa de desconto) elevado ao período:

```
P_0 = Σ E[Div_t] / (1 + R_E)^t
```

Onde:
- `E[Div_t]` é o dividendo esperado no momento t (não é certo, é expectativa)
- `R_E` é a taxa de desconto = taxa livre de risco + prêmio de risco
- t vai de 1 até quando? Por enquanto, indefinido.

## Modelo de um período

Vamos começar simples, com um modelo de um período. Como acionista, eu compro a ação hoje por P_0 e vou vender no momento 1, recebendo o preço de mercado P_1 mais o dividendo Div_1 que a empresa me pagou.

Fluxo de caixa:
- Investe: -P_0
- Recebe no momento 1: Div_1 + P_1

Logo:

```
P_0 = (Div_1 + P_1) / (1 + R_E)
```

Perceba que eu não tô trabalhando só com dividendo: aqui tem o preço da ação que eu vou vender lá na frente.

## Recursividade: o preço terminal some

Isso gera uma recursividade. Se eu tiver dois períodos, qual vai ser o preço da ação no instante 1? É o dividendo no instante 2 mais o preço no instante 2, trazido a valor presente. E assim sucessivamente, eu resolvo recursivamente até ficar só com fluxo de dividendos.

Eu vou mostrar pra vocês que esse preço lá na frente perde importância e o que domina a análise é de fato o fluxo de dividendos. Pra isso, a gente vai usar o conceito de [[Perpetuidade]] pra calcular o [[Valor Terminal]] da empresa, justamente pra se livrar do termo de preço terminal.

## Por que não dá pra projetar dividendo pra sempre

A fórmula somatória diz: dá pra projetar dividendo pra sempre? Em teoria sim, na prática não. Projetar no futuro depende de muitas condições. Seja no Brasil ou em outros lugares do mundo, você tem uma boa previsão pra cinco anos à frente. Mais do que isso, qualquer previsão se mostra muito diferente da realidade.

É o que os analistas chamam de [[Guidance]]: a empresa dá um guidance da sua estratégia e, consequentemente, do lucro que ela deve ter nos próximos anos. Mas não pra 10 anos. Pra 2, 3. Empresas já consolidadas fazem isso pra 5 anos. Então a gente tem um desafio: a fórmula pressupõe horizonte definido, mas eu acabei de dizer que sou incapaz de projetar fluxos mais de 5 anos. A solução vai passar por calcular o preço terminal da ação.

## NTNF como analogia

Quanto custa uma NTNF hoje? É o fluxo de caixa descontado até o vencimento. Tem uma data futura T que é o vencimento da NTNF. Você pode interpretar que os cupons são análogos aos dividendos. A gente já fez essa conta pra título.

Eu tô dizendo que uma ação é a mesma analogia. O preço de uma ação é o fluxo de caixa descontado daquilo que ela gera pros acionistas. O desafio é projetar esses dividendos e o valor final.

## Retorno esperado: análogo ao YTM de um bônus

Vocês lembram que quando eu comprava um bônus e carregava até o vencimento, eu calculava o retorno incorporando os dividendos, dividindo o preço final pelo inicial. Esse era o YTM. Aqui tem uma análise parecida.

Se eu levo em conta o dividendo da ação mais a variação de preço, dividido pelo preço inicial, isso dá o meu retorno esperado:

```
R_E = (Div_1 + P_1 - P_0) / P_0
```

É análogo a quando eu falava em 2014: comprei um bônus por 800 e vendi por 1.000, mais os dividendos. Esse é todo o fluxo. Dividindo pelo preço inicial, eu tenho a taxa de retorno do período. Se eu fui até o vencimento, equivale ao YTM (com reinvestimento dos cupons).

Então seu retorno esperado é uma composição entre o que você espera de dividendos, mais uma variação de preço, ou seja, o [[Ganho de Capital|ganho de capital]].

## Decomposição do retorno: Dividend Yield + Capital Gain

Eu posso reescrever a fórmula como:

```
R_E = Div_1/P_0  +  (P_1 - P_0)/P_0
       ↓              ↓
   Dividend       Capital
   Yield           Gain
```

A primeira parcela é o [[Dividend Yield]]. Por que isso é importante? Porque é um critério que vários analistas usam pra escolher quais ações comprar.

Exemplo: ação custa 100 e a empresa paga anualmente 10 unidades de dividendo. Em 10 anos, se o preço da ação não fizer absolutamente nada, tudo o que você gastou volta na forma de dividendos. Permite comparar empresas: como você compara uma de preço 10 com uma de preço 20? A de 10 tá barata e a de 20 cara? Ainda que sejam do mesmo setor. A maneira é analisar dividendo dividido por preço. Muitas vezes uma empresa cara paga muito dividendo, então o preço alto já reflete a expectativa de dividendo. Não é que ela esteja excessivamente valorizada.

## Exercício 1: cálculo do retorno esperado

Dado:
- Preço inicial: P_0 = 100
- Preço esperado de venda em 1 ano: P_1 = 110
- Dividendo esperado: Div_1 = 5

Pergunta: qual é o retorno esperado de investir nessa ação?

```
R_E = (5 + 110 - 100) / 100 = 15/100 = 15%
```

Resposta: **15%**.

Decompondo:
- Dividend Yield = 5/100 = **5%**
- Capital Gain = (110 - 100)/100 = **10%**

A gente compara o retorno esperado dessa empresa com o de outras empresas, com a premissa que elas têm riscos compatíveis. Nesse momento a gente não tá ajustando ao risco. Quando quiser ajustar, usa o CAPM.

## Ajuste pelo risco

Se duas empresas têm risco diferente, a de risco maior deveria ter um retorno esperado maior pra compensar o investidor. Pensa numa empresa cujo dividendo flutua muito: um ano paga bastante, outro ano paga menos, muito atrelado à dinâmica da economia. Essa empresa precisa de uma taxa de retorno maior pro acionista compensar essas flutuações.

Se eu não falei do risco e tô comparando duas empresas só por retorno esperado, eu tô implicitamente assumindo que o risco das duas é igual. Pode não ser verdade. Nessa disciplina essa premissa é válida. Em finanças vocês vão calcular o ajuste em relação ao risco.

## Exercício 2: Walgreens (achar P_0)

Dado:
- Dividendo esperado por ação: Div_1 = US$ 0,44
- Preço esperado de venda em 1 ano: P_1 = US$ 33
- Retorno esperado de investimentos com risco equivalente: R_E = 8,5%

Pergunta: qual o **preço máximo** que você pagaria por essa ação hoje?

Aplicação direta da fórmula:

```
P_0 = (Div_1 + P_1) / (1 + R_E)
P_0 = (0,44 + 33) / 1,085
P_0 = 30,82
```

Resposta: **US$ 30,82**.

Decomposição do 8,5%:
- Dividend Yield = 0,44 / 30,82 ≈ **1,42%**
- Capital Gain = (33 - 30,82) / 30,82 ≈ **7,07%**
- Total: ≈ 8,5%

Ou seja, do retorno total de 8,5%, **a maior parte vem do capital gain**, não do dividendo. Conclusão: pra essa empresa, o resultado depende muito mais de prever o preço da ação no fim do ano do que de prever o dividendo. Por isso, quando o Itaú corta a expectativa de preço-alvo, isso já te permite refazer rapidamente essas contas.

## Pergunta do João: por que isso indica alto risco?

A pergunta foi: o que essa decomposição diz sobre o risco da ação?

Capital gain de 7,07% sobre 8,5% é o maior contribuidor pro retorno total. Mas isso depende da projeção do preço daqui a um ano. Essa projeção é muito mais volátil do que prever o próximo dividendo. Empresas costumam ter disciplina pra entregar dividendo próximo do guidance (analista não gosta de surpresa, seja pra cima ou pra baixo). Mas o preço da ação um ano à frente flutua bem mais.

Então essa ação é de alto risco: quase todo o retorno vem da expectativa do preço futuro, não do dividendo. Quanto mais à frente, mais incerteza.

## Exercício 3: outra empresa (achar P_0 máximo)

Dado:
- Div_1 = 1,92
- P_1 = 65
- R_E (risco equivalente) = 11%

Pergunta: qual o máximo que você pagaria hoje?

```
P_0 = (1,92 + 65) / 1,11 = 78,31
```

Resposta: **R$ 78,31**.

E se a ação tá sendo negociada por R$ 79? Recalcula o retorno realizado:
- Dividend Yield = 1,92 / 79 ≈ 2,43%
- Capital Gain = (65 - 79) / 79 ≈ -17,7%? 

Errei aqui na transcrição. Na verdade, na aula:
- Dividend Yield ≈ **2,43%**
- Capital Gain calculado pelo professor: a ideia é que o retorno cai abaixo de 11%, dando algo próximo de 10,03% (vs. os 11% desejados).

Conclusão: se você paga mais do que R$ 78,31, o retorno realizado é **menor** do que o retorno desejado. Não significa que você não possa comprar, só significa que vai ficar abaixo do retorno-meta de 11%.

## Modelo de dois ou N períodos

Soltando o modelo de um período só, com dois períodos o fluxo vira:

```
P_0 = Div_1/(1+R_E) + (Div_2 + P_2)/(1+R_E)^2
```

E pra N períodos:

```
P_0 = Σ[t=1..N] Div_t/(1+R_E)^t  +  P_N/(1+R_E)^N
```

Isso é o **Modelo de Dividendo Descontado (DDM)**. Representa de maneira objetiva o preço de uma ação hoje.

## Por que o preço terminal perde importância em horizontes longos

Pra um ano, o preço terminal P_1 tem peso enorme no preço hoje (o dividendo é só uma parcela pequena). Conforme você estica o horizonte (10, 50, 100 anos), o termo P_N/(1+R_E)^N vira praticamente zero por causa do desconto, e o que domina o preço hoje é o **somatório dos dividendos**.

Então, se a empresa "nunca acaba", você pode quase ignorar o preço terminal: ele é trazido a valor presente com um expoente grande, virando irrelevante proporcionalmente aos dividendos. Isso é a lógica que justifica focar em projetar dividendo, e não preço final, que é muito mais difícil de projetar com horizonte longo.

## Próxima aula

Na segunda a gente vê a simplificação do DDM que é o **[[Modelo de Gordon]]**. Nele você precisa saber apenas:
- Um dividendo (o próximo)
- A taxa de crescimento do dividendo (g)

E você chega numa fórmula fechada muito simples, sem precisar fazer a conta termo a termo.
