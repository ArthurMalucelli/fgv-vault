---
materia: ContabilidadeFinanceira
data: 2026-08-10
tema: As 4 DFs principais a fundo e como se conectam
topicos: [relatório da administração, balanço patrimonial, DRE, DFC, conexões entre demonstrações]
tags: [estudo]
---

# As 4 DFs principais e como se conectam

## 1. O mapa geral

O framework da professora: cada relatório existe pra responder uma pergunta central do negócio. Se você sabe qual pergunta cada um responde, sabe qual relatório abrir em qualquer questão.

| Relatório | Pergunta que responde | Foto ou filme |
|---|---|---|
| [[Relatório da Administração]] | O que aconteceu no período e pra onde a empresa vai, na voz da gestão | Narrativa do período |
| [[Balanço Patrimonial]] | Onde o dinheiro está aplicado e de onde ele veio | Foto de uma data |
| [[DRE]] | Qual o resultado das operações no período, onde vai bem e onde precisa melhorar | Filme do período |
| [[DFC]] | Quais as principais entradas e saídas de caixa no período | Filme do período |

A lógica do conjunto (diagrama do slide 4): a empresa define estratégia e modelo de negócio (contado no RA), capta recursos (financiamentos: lado direito do BP), aplica esses recursos (investimentos: lado esquerdo do BP) e opera comprando, produzindo, vendendo e administrando (DRE). O caixa que circula por todas essas decisões é filmado pela DFC.

Existem outras demonstrações (DMPL, que abre a movimentação do PL, e DVA), mas o núcleo da disciplina são essas quatro.

## 2. Relatório da Administração

O que é: a "capa de jornal" da empresa. Texto da gestão com gráficos e comentários sobre o período: mercado, estratégia, resultados, expansão, guidance.

Perguntas que responde: qual é o modelo de negócio, o que a gestão diz que aconteceu, quais os planos.

Grau de isenção: baixo, e isso é ponto de prova. É a gestão escrevendo sobre a própria performance. Vitrine: destaca o que foi bem, suaviza o que foi mal. Não passa pelo mesmo rigor de auditoria das demonstrações em si. Uso correto: contexto e guia de leitura antes de mergulhar nos números, nunca fonte primária de julgamento. Toda afirmação do RA deve ser checável contra as DFs.

Estrutura típica do relatório completo: primeiro o RA, depois as demonstrações principais, depois as [[Notas Explicativas]] (que detalham linha a linha o que está condensado nas demonstrações).

Duas regras de leitura que valem pra tudo:

- Sempre coluna **consolidado**, ano mais recente. [[Consolidado vs Controladora]]: consolidado é o grupo econômico inteiro, controladora é a pessoa jurídica sozinha. Queremos a visão econômica. Empresa com "Participações" no nome é [[Holding]]: não opera nada, só reúne as empresas do grupo.
- O nome que a empresa dá a uma linha não manda. O que vale é o conceito (o caso da linha "lucro operacional" da Vivara que não era só operacional).

## 3. Balanço Patrimonial a fundo

Pergunta básica: como representar a riqueza da organização em determinado momento? É **foto**: retrata uma data, não um período.

### A estrutura e por que ela faz sentido

Dois lados que são a mesma coisa vista de ângulos diferentes:

- **Lado esquerdo (Ativo)**: APLICAÇÃO de recursos. Onde o dinheiro está investido: caixa, estoque, contas a receber, imobilizado.
- **Lado direito (Passivo + PL)**: ORIGEM de recursos. De onde o dinheiro veio: fornecedores, empréstimos, capital dos sócios, lucros retidos.

Daí a [[Equação Patrimonial]]:

```
Ativo = Passivo + Patrimônio Líquido
```

Não existe aplicação sem origem. Todo real investido em algum ativo veio de algum lugar. Se os dois lados não batem, tem erro em algum lugar (e a premissa serve até pra detectar corrupção e sonegação: patrimônio sem origem declarada).

Dentro de cada lado, a ordenação é por **prazo**:

| Bloco | Critério |
|---|---|
| [[Ativo Circulante]] | Vira caixa em até 1 ano (caixa, aplicações, contas a receber, estoques) |
| [[Ativo Não Circulante]] | Acima de 1 ano (realizável a LP, investimentos, imobilizado, intangível) |
| Passivo Circulante | Vence em até 1 ano (fornecedores, empréstimos CP, salários, impostos) |
| Passivo Não Circulante | Vence acima de 1 ano (empréstimos LP, arrendamentos) |
| [[Patrimônio Líquido]] | Capital próprio, sem vencimento: capital social, reservas, lucros acumulados |

O lado direito ainda se divide em **capital de terceiros** (todo o passivo, CP e LP) e **capital próprio** (PL). Essa divisão responde: quem financia a empresa, credores ou sócios?

### Como ler se a empresa vai bem a partir do BP

Três perguntas da atividade em aula:

```
% financiado por capital próprio = PL / Ativo total
% aplicado no longo prazo       = Ativo não circulante / Ativo total
Investimentos mais relevantes   = maiores linhas do ativo
```

Caso Vivara: ANC / Ativo total deu 35%, baixo pra quem fabrica (indústria costuma pesar mais no imobilizado). Top 3 ativos: estoque, contas a receber, imobilizado (caixa em 4º).

Pegadinha clássica: "investimentos" numa questão de análise significa **ativo** (onde o dinheiro está aplicado). Capital social, reservas de lucros e arrendamentos a pagar não são investimentos, são origens, lado direito.

## 4. DRE a fundo

Pergunta básica: qual o resultado das operações no período? Onde está indo bem e quais os pontos a melhorar? É **filme**: acumula receitas e despesas entre duas datas.

### A estrutura e por que ela faz sentido

No Brasil a DRE é organizada **por função** (pra que eu gastei), não por natureza (com que eu gastei). Três camadas de atividade, da mais central pra mais periférica:

Primeiro a **atividade-fim**: produzir (indústria), prestar o serviço (serviços) ou comprar mercadoria pra revender (comércio). O gasto da atividade-fim é [[Custo vs Despesa|custo]] (CPV, CMV ou CSP). Receita menos custo dá o [[Lucro Bruto]]: o valor agregado da atividade-fim.

Depois as **atividades-meio**: vender e administrar, comuns a qualquer empresa. São as [[Despesas Operacionais]]. Depois delas vem o [[EBIT]] (LAJIR), o lucro operacional.

Por fim a **atividade financeira**: relacionamento com bancos. Pegou emprestado, despesa financeira; aplicou sobra de caixa, receita financeira. O [[Resultado Financeiro]] não é operacional. Depois dele vem o LAIR, aí IR e CSLL, e sobra o lucro líquido.

```
Receita líquida
(-) CPV                        = Lucro bruto        <- atividade-fim
(-) Despesas operacionais      = EBIT (LAJIR)       <- atividades-meio
(+/-) Resultado financeiro     = LAIR               <- atividade financeira
(-) IR/CSLL                    = Lucro líquido
```

Essa estrutura faz sentido porque cada subtotal isola uma camada de decisão: lucro bruto mede o produto, EBIT mede a operação inteira, lucro líquido mede o que sobra pro acionista depois de banco e governo.

### Regime de competência

A DRE segue [[Regime de Competência]]: receita e despesa entram quando o fato acontece (venda entregue, serviço prestado), não quando o caixa se move. Vendeu 100 a prazo: receita de 100 hoje, caixa zero hoje. É por isso que lucro não é caixa, e é por isso que a DFC existe.

### Custo vs despesa: o teste da função

Mesmo gasto, classificação diferente conforme a função. Mão de obra: quem fabrica o produto é custo, quem vende é despesa de venda, quem administra é despesa administrativa. Vale em qualquer setor:

| Setor | Custo é o quê |
|---|---|
| Comércio | O que pagou pela mercadoria vendida (compra a 5, vende a 7: custo 5) |
| Indústria | Fabricação: matéria-prima, mão de obra fabril, energia da fábrica |
| Serviço | Quem presta o serviço (professor da FGV é custo do serviço) |

### Margem bruta e a pegadinha do tributo

```
Margem bruta = Lucro bruto / Receita líquida
```

Vivara: ~70%. Fabricar a joia custa ~30% do preço; o resto é marca, design, exclusividade. Cuidado ao comparar margem entre setores: a receita líquida já vem descontada de tributo, e cerveja perde ~40% em tributo antes de qualquer margem. Margem baixa ali não significa que o negócio agrega pouco valor.

## 5. DFC a fundo

Pergunta básica: quais são as principais entradas e saídas de caixa no período? É **filme**, igual à DRE, mas filmando caixa em vez de competência.

### Por que existe, se já temos a DRE

Porque lucro não paga boleto. A DRE reconhece receita na venda; o caixa só entra no recebimento. Empresa pode mostrar lucro alto e quebrar sem caixa (vendeu muito a prazo, estocou demais), ou mostrar prejuízo contábil e estar confortável de caixa. A DFC reconcilia os dois mundos.

### A estrutura: três atividades

| Atividade | O que agrupa | Exemplos |
|---|---|---|
| **Operacional (FCO)** | O dia a dia; transações que normalmente aparecem na DRE | Recebimento de clientes, pagamento a fornecedores, salários, impostos |
| **Investimento (FCI)** | Movimentos ligados a ativo não circulante e aplicações financeiras | [[Capex]] (compra de imobilizado e intangível), venda de imobilizado, aquisição de empresas, aplicações e resgates |
| **Financiamento (FCF)** | Relação com quem financia: acionistas e credores | Captação e amortização de empréstimos, aumento de capital, dividendos, recompra de ações |

A estrutura faz sentido porque separa três decisões diferentes: quanto caixa a operação gera, quanto a empresa reinveste, e como ela se financia. A leitura saudável típica: FCO positivo bancando FCI, com FCF equilibrando o resto.

```
FCO + FCI + FCF = Variação do caixa
Caixa inicial + Variação = Caixa final
```

### Método indireto: o formato que você vai ver na prática

A DFC da Ambev (e da maioria) não lista recebimentos um a um. Ela parte do lucro líquido e ajusta até chegar no caixa operacional. É o [[Método Indireto]]:

```
Lucro líquido
(+) D&A e outros itens sem efeito caixa
(+/-) Variação do capital de giro
      (- aumento de contas a receber e estoques)
      (+ aumento de fornecedores e contas a pagar)
= FCO
```

A lógica dos ajustes:

- **D&A volta somando** porque foi despesa na DRE mas nenhum caixa saiu neste período (o caixa saiu lá atrás, quando o ativo foi comprado).
- **Aumento de contas a receber subtrai** porque tem receita na DRE que ainda não virou caixa.
- **Aumento de estoque subtrai** porque caixa saiu pra comprar mercadoria que ainda não foi vendida.
- **Aumento de fornecedores soma** porque a empresa usou a mercadoria mas ainda não pagou: o fornecedor está financiando a operação.

Essas variações são o [[Capital de Giro]] em movimento.

## 6. Como as quatro se conectam

O princípio geral: **o BP é o estoque, DRE e DFC são os fluxos**. Toda variação de uma conta do balanço entre duas fotos tem que ser explicada ou pela DRE (via PL) ou pela DFC (via caixa). Se sobrar variação sem explicação, tem erro.

### Conexão 1: o lucro líquido é a dobradiça

Fecha a DRE, abre a DFC (método indireto) e alimenta o PL:

```
PL final = PL inicial + Lucro líquido - Dividendos + Aportes de capital
```

Exemplo: LL de 119, dividendos de 30. PL sobe 89. Na DFC, o 119 é a primeira linha do FCO e o 30 sai no FCF.

### Conexão 2: D&A, o triângulo

Uma única figura, três aparições: despesa na DRE (reduz EBIT), redutor do imobilizado no BP, soma de volta no FCO. Exemplo: D&A de 30 derruba o lucro em 30, derruba o imobilizado em 30, e volta somando 30 na DFC porque caixa nenhum se moveu.

### Conexão 3: o ciclo do capex

Caixa sai hoje no FCI, vira imobilizado no BP, e é devolvido à DRE ao longo dos anos como D&A. Comprou máquina de 100 com vida de 10 anos: FCI de -100 hoje, imobilizado +100 no BP, e 10 por ano de D&A nas próximas 10 DREs. Competência distribui no tempo o que o caixa reconhece de uma vez.

### Conexão 4: capital de giro, a ponte entre competência e caixa

Venda de 100 a prazo, cliente pagou 70 até o fechamento: DRE mostra receita de 100 (competência), BP mostra contas a receber +30, DFC ajusta o FCO em -30. Os 30 são lucro que ainda não é caixa. Mesma mecânica pra estoque (caixa que virou mercadoria) e fornecedores (mercadoria que ainda não virou saída de caixa).

### Conexão 5: dívida, principal e juros andam separados

Principal: entra e sai pelo FCF, saldo fica no passivo do BP. Juros: despesa financeira na DRE (resultado financeiro). Pegou 60 emprestado e pagou 5 de juros: FCF +60, passivo +60, DRE -5.

### Conexão 6: dividendos nunca passam pela DRE

Saem direto do PL (lucros acumulados) e do caixa via FCF. Dividendo não é despesa, é distribuição do lucro que já foi apurado.

### Conexão 7: o fechamento

O caixa final da DFC é a primeira linha do ativo circulante no BP da mesma data. E o BP tem que fechar: Ativo = Passivo + PL. São os dois checks que amarram o sistema inteiro.

## 7. Cheat sheet final

| | BP | DRE | DFC | RA |
|---|---|---|---|---|
| Natureza | Foto | Filme | Filme | Narrativa |
| Regime | Saldos | Competência | Caixa | Discurso da gestão |
| Pergunta | Onde está o dinheiro e de onde veio | Deu lucro? Onde vai bem? | De onde veio e pra onde foi o caixa | O que a gestão conta |
| Linha-síntese | Ativo = Passivo + PL | Lucro líquido | Variação do caixa | Sem número, checar contra as DFs |

```
Ativo = Passivo + PL
Margem bruta = Lucro bruto / Receita líquida
% capital próprio = PL / Ativo total
% longo prazo = ANC / Ativo total

DRE: Receita -> Lucro bruto -> EBIT -> LAIR -> LL
DFC: LL + não-caixa - ΔWC = FCO; FCO + FCI + FCF = ΔCaixa
Elo: PL final = PL inicial + LL - Dividendos + Aportes
Check: Caixa final DFC = Caixa do BP
```

Pra fixar: [[DFC]], [[Relatório da Administração]], [[Regime de Competência]], [[Capital de Giro]], [[Método Indireto]], [[Capex]], [[DRE]], [[Balanço Patrimonial]], [[Equação Patrimonial]], [[EBIT]], [[Margem Bruta]], [[Consolidado vs Controladora]]
