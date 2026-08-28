---
materia: ContabilidadeFinanceira
data: 2026-08-28
tema: Revisão de erros dos quizzes (Delícia Gelada, Sing's, Nosso Doce Amor, Lojas Paulistas)
topicos: [regime de caixa, regime de competência, equação de saldo, contas antecipadas, CMV, dividendos]
tags: [resumo, revisao]
---

# Revisão de erros: quizzes de mecanismos contábeis

Compilado dos erros e dúvidas reais nos quizzes de 27 e 28/08. Cada item abaixo foi um erro cometido, não teoria genérica.

## 1. Timing: caixa vs competência (maior fonte de erro)

Pergunta-filtro pra qualquer transação:

- [[Regime de Caixa]]: "o dinheiro andou DENTRO deste período?"
- [[Regime de Competência]]: "a entrega ou o consumo aconteceu neste período?"

São dois filmes independentes da mesma empresa. Quase nunca batem no mesmo mês.

| Erro cometido | Respondi | Certo | Regra que faltou |
|---|---|---|---|
| Seguro pago em março, caixa de abril | (144) | 0 | Caixa só registra dinheiro que andou no mês. Pagamento foi em março |
| Ingredientes pagos na semana seguinte, caixa | (-24) | (180) | 3 dos 4 boletos caem dentro de abril. Estoque não é caixa |
| Vendas no cartão de crédito, caixa | 528 | 240 | Cartão cai em 30 dias, mês seguinte. Só o que foi à vista entrou |
| Vendas no cartão, resultado | 0 | 288 | Receita segue a ENTREGA, não o recebimento |
| Pedidos pagos antecipados, 60% entregues | tudo em adiantamento | 72 receita + 48 passivo | Entregou, é receita. Só o não entregue fica no passivo |

## 2. Sinal e formato de resposta

- [[DRE]] registra efeito no lucro com sinal: custo é (216), nunca 216 seco. Número sem parêntese = aumentou o lucro.
- Parêntese substitui o sinal de menos. "(-24)" erra duas vezes.
- Cada questão define a própria convenção no aviso destacado (com sinal, sem sinal, ponto de milhar). Ler o aviso antes de digitar. Corretor automático compara string exata: 1620 ≠ 1.620.

## 3. O quadrado das contas "antecipadas"

| Conta | O que houve | Lado do BP |
|---|---|---|
| Receita Antecipada / [[Adiantamento de Cliente]] | cliente pagou, eu não entreguei | Passivo |
| [[Contas a Receber]] | eu entreguei, cliente não pagou | Ativo |
| [[Despesa Antecipada]] (seguro, propaganda) | eu paguei, não consumi | Ativo |
| [[Fornecedores]] | eu consumi, não paguei | Passivo |

Chave: o nome descreve a receita ou despesa que ainda VAI existir, não o que a conta é agora. Quem deve algo está no passivo, quem tem algo a receber está no ativo. Erros ligados: somei Receita Antecipada na receita da DRE (é dívida, não entra) e achei que Propaganda Antecipada zerava no 1º trimestre (cobria 12 meses, consumiu 3, sobram 9 × 5 = 45).

## 4. Equação de Saldo (caixa d'água): o padrão que resolve metade da prova

```
Saldo inicial + entradas − saídas = Saldo final
```

Ver [[Equação de Saldo]]. A prova esconde UMA peça e dá as outras três. Casos reais errados ou travados:

| Conta | Entra | Sai | Peça escondida | Resposta |
|---|---|---|---|---|
| [[Estoque]] | compras | [[CMV]] | compras = 1.750 + 850 − 980 | 1.620 |
| [[Fornecedores]] | compras a prazo | pagamentos | pago = 970 + 1.620 − 740 | 1.850 |
| [[Contas a Receber]] | vendas a prazo | recebimentos | recebido = 370 + 3.200 − 350 | 3.220 |
| [[Lucros Acumulados]] | lucro líquido | [[Dividendos]] | div = 465 + 130 − 490 | 105 |
| [[Imobilizado]] | aquisições | [[Depreciação]] | inicial = 400 − 300 + 40 | 140 |

Armadilhas específicas que caí:

- Andando PRA TRÁS no tempo, a depreciação SOMA de volta (respondi 100 e 60, era 140).
- "Ainda devido" é o saldo final, não o pagamento. Pago e devido são complementares, somam a dívida total, nunca são o mesmo número (usei 216, era 212).
- Consumo de estoque: % de sobra incide sobre o DISPONÍVEL (inicial + compras), não só sobre a compra do período.
- Coluna de transação na planilha = variação líquida, não saldo. Saldo final = inicial + soma das colunas.
- Sempre conferir DE IDA depois de achar a peça: encaixa o resultado e verifica se chega no saldo final dado. Dez segundos, pega quase tudo.

## 5. Não inventar fórmula: derivar do mecanismo

Erro repetido 3x no caso dos dividendos: montar combinações plausíveis dos números do enunciado ("Div = LA − LL" deu 360, "sobra = LA − LL − Div" deu 255, nada significa nada). Fórmula montada de trás pra frente parece plausível e quase sempre está errada, porque mistura estoque (saldo numa data) com fluxo (o que aconteceu no período).

Caminho único: escrever a equação de saldo da conta, encaixar os três números dados, isolar o quarto. Derivados corretos:

```
LA final = LA inicial + Lucro Líquido − Dividendos
Lucro retido = LL − Dividendos = LA final − LA inicial
```

Antes de calcular, perguntar: "quais são as ÚNICAS coisas que mexem nesta conta?" Lucros Acumulados: lucro entra, dividendo sai. Só.

## 6. Classificação de contas

- [[Passivo Circulante]]: respondi 144, era 78. Empréstimo "longo prazo" NÃO entra; Fornecedores entra. Vocabulário do enunciado: "a pagar" e "a receber" é balanço, "do mês" e "consumido" é DRE.
- Juros ≠ principal: financiamento não circulante era 400, não 430. Juros do período viram [[Juros a Pagar]] (circulante), conta própria, não somam no principal quando são pagos e não capitalizados. Parcela que vence em até 12 meses migra pro circulante.
- Compra 100% financiada não mexe no caixa: lancei Caixa (200) numa compra sem entrada. Imobilizado +600, Financiamento +600.
- Pagamento de salários "inclusive os devidos do período anterior": o caixa leva o total (112 + 20 = 132) e a conta Salários a Pagar zera.
- [[Depreciação]] entra com as duas pernas negativas: conta redutora fica mais negativa, PL cai. Lançar +15 na acumulada seria "rejuvenescer" o bem.
- Depreciação acumulada É POR CLASSE de ativo: campo pedia só veículos (15), respondi (255) misturando a dos equipamentos.
- Prazo de amortização sai do ENUNCIADO: licença de 2 anos = 144/24 = 6 por mês. Respondi (12) assumindo 1 ano por default.
- Custo vs despesa: quem produz é custo (cozinha, depreciação de equipamento produtivo), quem vende/entrega é despesa de vendas (propaganda, carro de entrega), quem sustenta a estrutura é administrativa (contabilidade), juros é financeira.

## 7. DRE em cascata

Respondi lucro líquido 48 fazendo [[Lucro Bruto]] − IR direto, pulando degraus. Ordem fixa:

```
Receita − Custo = Lucro Bruto
− Despesas operacionais (vendas, adm) = Lucro Operacional
± Resultado Financeiro = LAIR
− IR = Lucro Líquido
```

Check final obrigatório: sobrou conta de resultado sem usar em algum degrau? Então o número está errado.

## 8. Quiz Voe Alto (28/08): os 6 campos errados de uma vez

Padrão: classifiquei linhas da DRE pelo pagamento (lógica de caixa). Correções que valem regra:

- **Campo = linha da DRE.** "Receita de Serviços" é a linha bruta (300), sem descontar custo. Se descontar combustível/salário dentro da receita, o corretor subtrai duas vezes ao montar o lucro. Cada campo é um degrau da cascata.
- **Teste do verbo pro caixa:** "recebido", "pago" = caixa do mês. "A ser pago", "vencimento no próximo mês" = caixa de outro mês. O particípio vs futuro decide, não o mês do trabalho ou do voo. Apliquei o filtro na entrada (excluí o cartão) e esqueci na saída (incluí salário e aluguel "a ser pago").
- **Simetria de conferência:** item que saiu da DRE do mês (pago adiantado ou atrasado) tende a estar no caixa, e vice-versa. Depreciação não está em lugar nenhum do caixa. Se um item aparece nos dois, é porque foi feito E pago no mês.
- **Consumo com estoque final:** comprou 100, sobrou 20, CSP leva 80.
- **Pago por 1 ano, vigência no mês:** caixa leva o total (216), DRE leva 1/12 (18).
- Drill pra esse formato de questão: pra cada linha da tabela, duas colunas no rascunho, "DRE março?" e "caixa março?", item por item, antes de preencher qualquer campo.

## 9. Processo (2 pontos perdidos por processo, não por conceito)

- Typo: digitei 244 com 240 certo no rascunho. Releitura campo a campo antes do submit.
- Número condicional de terceiro (IA incluída) não entra em campo de prova sem validar a condição no enunciado.
- [[Balanço Patrimonial]] que não fecha é bug, sempre: minha planilha mostrava ativo 1.516 contra passivo 2.068 e passou batido. Checagem ativo = passivo + PL é automática e gratuita, em toda coluna e no final.
