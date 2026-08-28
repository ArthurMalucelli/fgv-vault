---
materias: [estatistica-2]
semestre: 2026.2
data: 2026-08-07
tipo: transcrito
tema: Testes de Hipótese e Distribuições Z e T
status: completo
contract_version: 1
topicos: [teste de hipotese, hipotese nula, hipotese alternativa, erro tipo I, erro tipo II, valor-p, graus de liberdade, distribuicao t de student, regiao de rejeicao]
tags: [aula, transcrito]
---

## Motivação: por que inferência estatística

A gente quer inferir informações da população a partir de uma amostra. Por quê? Porque se eu já tivesse a população inteira, eu faria estatística descritiva direto, não precisaria inferir nada. A motivação é: a partir de uma amostra pequena, ver o que acontece com a população.

O professor deu um exemplo de viés amostral com um candidato político visitando uma igreja pra tirar fotos: se eu pego só a amostra da igreja pra avaliar a aprovação de um candidato, isso dá uma boa medida da população geral? Provavelmente não, porque a amostra não é representativa.

## Revisão: padronização e intervalo de confiança

Revisão rápida do que já foi visto: a [[Distribuicao normal|normal padrão]] é o eixo de referência, com média 0. Tudo o que acontece de um lado da distribuição acontece simetricamente do outro.

Quando o exercício pede alfa de 5%, isso quer dizer: considerando que a distribuição é normal, eu quero um intervalo que cubra 95% das observações. Nesse caso, o valor procurado fica entre a média amostral mais ou menos 1,96 (o [[Z de alfa sobre 2|Z de alfa sobre 2]] padronizado). Essa é basicamente a massa de dados debaixo de uma curva normal.

## O que é um teste de hipótese

Exemplo de motivação, controle de qualidade: numa linha de produção, você aceita que, a cada mil produtos, saia um certo número de defeituosos. De tempos em tempos você audita o processo: coleta uma amostra, vê quantos defeituosos tem ali. Você não sabe exatamente quanto isso vai dar pra população inteira, mas pode assumir que a média de defeitos da amostra está perto do valor esperado, dentro de uma margem.

É isso que o teste de hipótese faz: avalia se os dados da amostra fornecem evidências suficientes para rejeitar, ou não, uma afirmação inicial sobre a população. Toda vez a gente vai definir:

- **H0** (hipótese nula): a afirmação inicial, presumida como verdadeira até prova em contrário.
- **H1** (hipótese alternativa): o que eu estou tentando verificar se tenho evidência pra sustentar.

## Analogia do julgamento

A lógica do teste de hipótese é a mesma de um julgamento: o réu é inocente até que se prove o contrário. Eu nunca afirmo com certeza que H0 é verdadeira ou falsa, porque estou lidando com probabilidade: sempre existe uma chance de eu ter errado. A decisão é tomada com um grau de confiança, no caso da aula, 95%.

Então a gente nunca fala "ele é inocente" ou "ele é culpado" no sentido absoluto. A gente fala: os dados, as evidências, apontam nessa direção.

## Exemplo: amostra não representativa

Outro exemplo do professor: avaliar se ele é um bom professor. Se no fim do semestre ele for até a coordenação e disser "peguem uma amostra de cinco alunos que tiraram 10", isso não é uma amostra representativa. Do mesmo jeito, se ele pegar cinco alunos que foram mal e nem vieram na aula, também não é representativo. Existe sempre uma chance de pegar uma amostra ruim e fazer uma inferência errada sobre a população. Por isso a decisão é tomada com um grau de confiança, não com certeza absoluta.

## Exemplo: região de rejeição (corrida de 100 metros)

Exemplo: você quer entrar pro time de corrida da atlética e afirma que corre 100 metros em 12 segundos. Pra verificar isso, você cronometra vários treinos e calcula a média. Se os treinos, na média, ficam perto de 12 segundos, essa é a região de aceitação do H0. Se ficar muito distante, é a região de rejeição.

## Roteiro para resolver um teste de hipótese

O professor deu uma receita fixa pra resolver qualquer exercício de teste de hipótese:

1. Definir o nível de significância, alfa (ex: 5%).
2. Calcular a estatística de teste (Z ou T, dependendo do caso).
3. Achar o valor crítico (ou o valor-p) e comparar com alfa.
4. Decidir: rejeitar ou não rejeitar H0.

Em prova, muitas vezes o alfa já vem dado no enunciado; quando não vier explícito, é pra assumir um valor razoável (a aula trabalhou com 5%).

## Por que alfa de 5%? O trade-off de confiança

Por que não usar 99% de confiança sempre, já que parece "mais seguro"? Se eu aumento o nível de confiança, o intervalo fica mais largo, os limites ficam mais distantes da média. Isso torna mais difícil rejeitar H0: eu corro o risco de aceitar coisas que deveriam ser rejeitadas.

Do lado oposto, se eu diminuo o nível de confiança, o intervalo fica mais estreito, e eu passo a rejeitar H0 com mais frequência, inclusive quando não deveria. Não existe uma escolha "cientificamente correta" de alfa isolada; é uma decisão prática. O importante é ser capaz de justificar a escolha e verificar se ela separa bem os casos que são de fato diferentes dos que não são.

## Quando usar Z vs T de Student

Quando eu tenho um número pequeno de observações, eu não uso a distribuição normal (Z), eu uso a [[Distribuicao T de Student|distribuição T de Student]]. Além de média e variância, a T depende de mais um parâmetro: os [[Graus de liberdade|graus de liberdade]].

A regra prática de "acima de 30 posso usar Z" existe porque, conforme o número de observações cresce, a T converge pra distribuição normal, fica muito próxima dela. Com poucas observações (o professor deu o exemplo de n=15), a T se distancia mais da normal e usar Z direto seria errado.

O professor fez a piada da cartomante pra fixar isso: se eu acordo, vou na cartomante e pergunto "posso usar a T hoje?", ela pode responder sim de olhos fechados e vai estar sempre certa, porque a T vale em qualquer cenário: com muitas observações ela praticamente coincide com a normal, com poucas ela é a distribuição correta. Agora, se o livro dela diz que hoje mercúrio está retrógrado e eu pergunto "posso usar a Z com uma amostra de 15 elementos?", aí a resposta é não: com N pequeno a diferença entre as duas distribuições aparece de verdade.

## Calculando a estatística de teste

Como calcular o Z: pego o valor observado, subtraio a média e divido pelo desvio padrão. Isso mostra quantos desvios padrão aquele valor está distante da média, ou seja, em quantas unidades de erro padrão ele se desvia.

## Valor-p

Conceito novo: o valor-p. É a probabilidade de se observar um resultado tão ou mais extremo que o observado, supondo que H0 seja verdadeira.

O professor retomou o exemplo de controle de qualidade: até 5% de peças defeituosas eu aceito como normal (essa seria minha H0). Se eu coleto uma amostra e o percentual de defeituosos encontrado for muito distante desse valor esperado, dado o tamanho da amostra, fica pouco provável que a taxa real de defeitos seja realmente de 5%. Nesse caso a gente tem evidência pra descartar a hipótese nula. Se a amostra ficar próxima do esperado, não há evidência suficiente pra rejeitar H0, e a informação obtida não é suficiente pra mudar a decisão.

## Erro Tipo I e Erro Tipo II

Pensando no esquema do julgamento, existem quatro cenários possíveis:

- Falar que é inocente, e ele é de fato inocente: acerto.
- Falar que é culpado, e ele é de fato culpado: acerto.
- Falar que é inocente, mas ele é culpado: erro.
- Falar que é culpado, mas ele é inocente: erro.

No teste de hipótese, isso vira:

- **Erro Tipo I**: rejeitar H0 sendo que H0 é verdadeira. É "condenar um inocente". A probabilidade desse erro é o próprio alfa.
- **Erro Tipo II**: não rejeitar H0 (aceitar) sendo que H0 é falsa. É "absolver um culpado". Também chamado de beta.

O exemplo do professor: você rejeita a hipótese de que ele é um bom professor porque pegou uma amostra de cinco alunos muito ruins que tiraram nota baixa, quando na verdade a média da sala era mais alta. Isso é azar de amostra: um Erro Tipo I. Você rejeitou uma hipótese verdadeira porque calhou de pegar uma amostra não representativa.

## Do intervalo de confiança ao teste de hipótese

O teste de hipótese e o intervalo de confiança são duas faces da mesma regra, chegam na mesma conclusão por caminhos diferentes. No intervalo de confiança, você olha o valor da estatística de teste em desvios padrão e vê se ele cai dentro ou fora do intervalo. No teste de hipótese, você pode olhar em termos de área: quando o teste é bicaudal (dois lados), o alfa se divide meio a meio entre as duas caudas. Pra alfa de 5%, cada cauda fica com 2,5%.

Não é a mesma coisa comparar o valor-p com alfa e comparar a estatística de teste com o valor crítico, mas os dois caminhos levam à mesma decisão sobre H0. Em prova, às vezes você vai usar um caminho, às vezes o outro, dependendo do que o enunciado pede.

## Exemplo prático: tempo de atendimento

Exercício final da aula: um posto de atendimento tem histórico de 10 minutos por atendimento. O professor quer verificar, com uma amostra de 12 atendimentos, se a média mudou.

- H0: a média é igual a 10 minutos.
- H1: a média é diferente de 10 minutos (teste bicaudal).

Calculando a partir da amostra: a média amostral deu 10,13. O desvio padrão da amostra, levado em conta o tamanho da amostra, gera um erro padrão de aproximadamente 0,07.

Como o número de observações é pequeno, usa-se a distribuição T, com graus de liberdade igual a n - 1, ou seja, 11.

A estatística de teste (T) é calculada padronizando a diferença entre a média amostral e a média hipotética, dividida pelo erro padrão: T = (10,13 - 10) / 0,07.

Pra decidir, é preciso comparar essa estatística de teste com o valor crítico de T pra alfa de 5%, bicaudal, com 11 graus de liberdade (cada cauda com 2,5%). Alternativamente, dá pra achar o valor-p correspondente ao T calculado e comparar direto com alfa.

Na ferramenta, o professor mostrou que são duas funções espelhadas. A inversa da T recebe o alfa (e os graus de liberdade) e cospe o T crítico: você entra com a área e sai com o valor de corte. A função de distribuição da T faz o caminho contrário: recebe o T calculado e cospe a área, que é o valor-p. Uma entra área e devolve valor, a outra entra valor e devolve área.

Os dois caminhos, valor calculado contra valor crítico, ou valor-p contra alfa, levam à mesma decisão sobre rejeitar ou não H0.
