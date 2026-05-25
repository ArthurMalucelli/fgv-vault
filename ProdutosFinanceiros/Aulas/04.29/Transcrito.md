---
materia: ProdutosFinanceiros
data: 2026-04-29
tema: SELIC, CDI e cálculo de taxas diárias no mercado brasileiro
topicos: [SELIC, CDI, taxas-diarias, dias-uteis, overnight, Tesouro-SELIC]
tags: [aula, transcrito]
---

# Aula 29.04.26 — SELIC, CDI e cálculo de taxas diárias

## Política monetária e [[SELIC]] over

O principal dilema é esse. O Banco Central coloca o desafio e o impacto da política. Amanhã vocês passam a ter nova SELIC over, porque as pessoas falam: o BC prestou no Open Market, ou o banco prestou pro outro banco. Então amanhã a SELIC vai estar acima ou abaixo da meta.

Quando a operação de mercado está abaixo da SELIC meta, o Banco Central vende títulos. Ao vender títulos, ele tira dinheiro da economia. O preço do título sobe. Caso final: se a SELIC over está acima da meta, ele vai ao mercado e compra títulos. Quer dizer, ele entrega dinheiro, põe mais dinheiro na economia, está tirando os títulos. Essa é a dinâmica.

## Conversão da [[SELIC]] anual pra diária

A [[SELIC]] meta e a SELIC over são sempre expressas ao ano. Vocês vão ter que sempre transformar a SELIC pra fazer as contas.

Quero saber qual é a SELIC diária capitalizada por 252 dias que me dá SELIC ao ano. Nada mais é do que pegar 1 mais a taxa de SELIC over, elevado a 1 sobre 252, menos 1. Praticamente tudo nós vamos transformar em base de dia.

De agora em diante, o ano sempre tem 252 dias úteis.

## Por que 252 dias úteis e a questão do feriado

Vou mostrar como usar a função DIATRABALHOTOTAL e a coluna feriado, que vai ser importante.

Em 2020, infelizmente, criaram um feriado pra evitar circulação de pessoas durante a pandemia. O motivo era nobre, mas pra indústria financeira causou impacto brutal. Pensa: quando você faz um empréstimo no mercado financeiro, leva em conta os feriados pra saber quantos dias úteis você tem de um dia pro outro. A taxa overnight é pra dias úteis. Se você empresta por 252 dias úteis e de repente cria um feriado no meio, sua remuneração passa a ser sobre 251 dias úteis, você perdeu um dia. Imagina isso pro mercado como um todo, é um impacto direto no sistema financeiro.

Por isso, sempre que se cria um feriado, ele vale a partir do ano seguinte, pra que haja tempo hábil de ajustar contratos.

**Pergunta de aluno:** se tem todo esse problema, por que eles não fixam o número de dias em 252?

**Resposta:** se você põe um feriado no meio, o número de dias úteis muda. Não adianta mudar como você mede o ano. Se você criar um feriado naquele ano, necessariamente tirou um dia útil daquela conta. A alternativa seria mudar pra dias corridos, igual nos Estados Unidos (360 dias). Aqui é dias úteis. É convenção, não é certo nem errado. É a regra que o Brasil adotou, herança da época de inflação alta.

## DIATRABALHOTOTAL e operação overnight

Pega esse exemplo: 20 de abril de 2026 a 22 de abril de 2026. Se você usar `DIATRABALHOTOTAL` no Excel com data inicial e data final, ele dá 3. Tem segunda, terça e quarta.

No entanto, pra fins de SELIC estamos sempre olhando operação overnight. Quantas noites você tem em dois dias? É igual diária de hotel: se você fica dois dias, é uma noite. Então na operação overnight, faz a conta e tira 1.

Aqui o método é **inclusivo** (inclui as duas datas). Quando eu for explicar título público, terá uma diferença sutil: lá a data de vencimento é **exclusiva**, faz esse ajuste.

Mas no dia 21 foi feriado. Como a gente faz isso? Usa o terceiro argumento da função, a coluna de feriados. Selecionando todos os feriados (shift+ctrl+down pra pegar a coluna inteira), o DIATRABALHOTOTAL passa a contar 2 ao invés de 3.

Aí, de fato, ele deu 1 dia overnight. Você tem segunda, terça (feriado) e quarta. Terça não conta. É como se você tomasse o dinheiro na segunda e devolvesse na quarta de manhã. Você ficou com o dinheiro uma noite só.

Analogia do hotel: você viaja, faz check-in e check-out. A noite é a estadia. O dia que você sai não conta. Hoje pra amanhã é uma noite, não dois dias.

## Exemplo: investimento em [[SELIC]] pós-fixada por 3 dias

Cenário: investe R$ 100.000 num título indexado à SELIC por 3 dias. As taxas SELIC over praticadas foram 7,40%, 7,38% e 7,36% ao ano.

Quando o enunciado fala em "3 dias", são 3 dias úteis. Quando fala em datas, aí precisa contar feriado.

A SELIC está em base anual, transforma em diária:

```
r1 = (1 + 0,0740)^(1/252) − 1
r2 = (1 + 0,0738)^(1/252) − 1
r3 = (1 + 0,0736)^(1/252) − 1
```

Capitaliza pelo período:

```
Fator = (1 + r1) × (1 + r2) × (1 + r3)
Taxa_periodo = Fator − 1
```

Princípio fundamental: o fator do período é igual ao produtório dos fatores diários. Se quiser anualizar de volta, capitaliza por 252 dias.

A lógica geral é: tem uma taxa em um período qualquer, primeiro transforma em taxa ao dia, depois leva pra onde quiser.

## [[Tesouro SELIC]]

Pós-fixado, atualizado diariamente pela [[SELIC]]. É um produto onde você nunca sabe a priori a rentabilidade exata, a não ser que use estimativa. O único jeito de saber é ao final do prazo, ou usando a estimativa da curva de juros.

Exemplo: Tesouro SELIC com vencimento em 2031, paga SELIC + 0,0X. Pra investir você precisa de R$ 188 (cota do título). Hoje, baseado na curva de juros que vocês pegaram na B3, o sistema mostra estimativa de quanto você vai receber em 2031. Se você colocar mil reais, em 5 anos teria mais de 50% de ganho composto. Compara com poupança no mesmo período: 1.392.

## [[CDI]] e taxa DI

Agora o primo-irmão da [[SELIC]], o [[CDI]].

O CDI é uma taxa governamental. É um sinônimo de Certificado de Depósito Interbancário. Certificado é um documento que uma instituição emite para outra. Vocês conhecem CDB (Certificado de Depósito Bancário). CDI é Certificado de Depósito **Interbancário**: de um banco emprestando para outro.

A taxa correta é **taxa DI**. Popularmente fala-se "taxa CDI", mas tecnicamente errado. CDI é o produto. Como ninguém fala "taxa CDB", também não existe "taxa CDI" no sentido formal.

CDI também é overnight, banco emprestando pra banco, **sem garantia** (sem título público como colateral). O banco A empresta pro banco B porque acha o risco de crédito do B aceitável. Foi a dinâmica do mercado brasileiro por muitos anos.

## Distorção histórica: SELIC vs CDI

Por bizarro que pareça: operação entre bancos com garantia (em título público) deveria ter taxa **menor** que sem garantia, pelo menor risco. No Brasil, durante muitos anos, **não era assim**. A taxa DI era às vezes igual ou menor que a SELIC, mesmo carregando risco de crédito. Discutia-se distorção tributária, manipulação dos bancos, sem consenso.

Certo ou errado, esse mercado deixou de existir. Hoje banco não empresta pra outro banco dessa modalidade. Empresta só via operação compromissada (com garantia em título). Uma pergunta natural é: e o que eu posso garantir? Pode ser título privado, pode ser título público.

## A taxa DI desde 2018

Como a taxa DI continua indexando praticamente tudo na economia, foi resolvido assim: desde 2018, ela é exatamente igual à [[SELIC]], pega a SELIC com regra equivalente. Está na página da B3, hoje 14,65%, idêntica à SELIC.

Pra fim de cálculo, vocês podem pensar: é taxa overnight, expressa ao ano, todos os cálculos em base diária. Numericamente DI = SELIC.

## Por que produtos com risco usam [[CDI]] e não [[SELIC]]

A SELIC é taxa **livre de risco**. Pra operações com risco, você tem que usar uma taxa com risco, que é a taxa DI. Por mais que numericamente sejam iguais hoje, conceitualmente são diferentes.

Vocês vão sempre encontrar:

- [[CDB]] pré-fixado: 15% ao ano, por exemplo
- CDB pós-fixado: CDI mais alguma coisa, OU X% do CDI

Não existe "X% da SELIC". Mas existe "124,5% do CDI". Vou explicar como faz essa conta.

## Exemplo: CDB do Banco Master a 124,5% do [[CDI]]

Em 2022, Banco Master pagava 124,5% do CDI no CDB. O que captura esse percentual?

**Pergunta de aluno:** o banco bota essa taxa alta pra atrair?

**Resposta:** sim. Quando produto tem 124,5% do DI, quer dizer que vai pagar mais do que 100% do DI. É um adicional pelo risco. Você empresta dinheiro pra um banco que paga prêmio de risco.

Inverso vale também: [[LCI]] e [[LCA]] pagam menos de 100% do DI, porque são produtos isentos de IR. Você abre mão de parte do bruto pelo benefício fiscal.

Quem define o percentual é o emissor do papel. O investidor aceita ou não. Quanto maior o spread acima de 100%, mais arriscado tende a ser o emissor.

## Cálculo de produto a X% do [[CDI]]

A regra: aplicar o percentual sobre a taxa **diária**, não sobre a anual.

A taxa DI está expressa ao ano. Primeiro transforma em diária, depois aplica o percentual:

```
DI_dia = (1 + DI_ano)^(1/252) − 1
r_dia  = DI_dia × p
Fator  = (1 + r_dia)^n
```

Se aplicar o percentual direto na taxa anual, dá diferente. Pra garantir que o resultado está correto, sempre aplica no diário.

### Exemplo trivial: 95% do CDI por 65 dias com taxa única

DI 8,5% ao ano, produto a 95% do CDI, 65 dias úteis.

```
DI_dia = (1,085)^(1/252) − 1
r_dia  = DI_dia × 0,95
Fator  = (1 + r_dia)^65
Taxa_periodo = Fator − 1
Bruto  = 100.000 × Fator
```

Isso é taxa do período. Se quiser anualizar, capitaliza por 252.

### Exemplo com taxa variável: 95% do CDI por 2 dias

Dia 1: DI 8,40% ao ano. Dia 2: DI 8,50% ao ano.

```
r1_dia = [(1,0840)^(1/252) − 1] × 0,95
r2_dia = [(1,0850)^(1/252) − 1] × 0,95
Fator  = (1 + r1_dia) × (1 + r2_dia)
```

Em casos de taxa única dá pra usar taxa média, mas como critério geral o método de aplicar percentual em diária e capitalizar funciona sempre. Padroniza.

## Exemplo final: 96% do DI por 180 dias com taxas variáveis

180 dias, 88 dias com DI a 7,15% e 87 dias com DI a 6,90% (números aproximados, conferir slide).

```
r1_dia = [(1 + 0,0715)^(1/252) − 1] × 0,96
r2_dia = [(1 + 0,0690)^(1/252) − 1] × 0,96
Fator  = (1 + r1_dia)^88 × (1 + r2_dia)^87
Bruto  = Aplicação × Fator
```

Pra chegar no líquido, falta abater [[IR]]. Próxima aula.

## Pontos que vão cair em prova

- Sempre transformar taxa anual em diária antes de qualquer manipulação
- Em overnight, contar **noites** (subtrair 1 do DIATRABALHOTOTAL inclusivo)
- Título público: data de vencimento é **exclusiva**. CDB e similares: **inclusiva**
- Percentual do CDI sempre incide na taxa **diária**, nunca na anual
- DI = SELIC numericamente desde 2018, mas DI carrega risco e SELIC não

Próxima aula vou começar com o último exercício e entrar na parte de [[IR]] e tributação.
