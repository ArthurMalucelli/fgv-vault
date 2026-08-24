---
materia: Estatistica2
data: 2026-08-18
tema: Qui-quadrado - fechamento da aderência e teste de independência
topicos: [teste qui-quadrado de aderência, teste qui-quadrado de independência, graus de liberdade, frequência esperada, tabela de contingência, funções do Excel]
tags: [aula, transcrito]
---

## Fechando o teste de aderência

Eu consigo obter um valor negativo para essa estatística? Não, né? O valor mínimo do qui-quadrado é zero. O qui-quadrado é o valor da estatística [[Teste qui-quadrado de aderencia|do teste de aderência]], e o Excel vai te pedir uma informação a mais: a [[Distribuicao qui-quadrado|distribuição qui-quadrado]] precisa de [[Graus de liberdade|graus de liberdade]]. Quantas categorias tem na lista? Com 4 categorias, eu vou procurar um qui-quadrado com 3 graus de liberdade.

Nesse exemplo, o valor crítico é 7,81 e o meu qui-quadrado deu muito baixo. O [[Valor-p|p-valor]] fica em 0,4, que é maior que o alfa, e a minha estatística é menor que a crítica. Rejeito ou não rejeito H0? Não rejeito. Logo, essa distribuição está fazendo sentido: pelo menos eu não obtive nenhuma informação que diga que aquilo pode ser questionado.

No Excel, a família de funções INV tem o INV da normal, o INV do t, e tem o INV da distribuição qui-quadrado, que é de onde vem o 7,81.

## Teste de independência

Agora eu quero saber se duas coisas são independentes. Vamos fazer um teste com a sala: você prefere rock, sertanejo ou MPB? Monto uma tabela com as respostas por sexo. Isso é o [[Teste qui-quadrado de independencia|teste de independência]]. Na aderência não tinha nem uma somatória dupla; agora são duas: o i varia de 1 até R e o j de 1 até C. O C vem de colunas e o R de linhas (rows). A soma marginal de cada linha e de cada coluna entra no cálculo.

A linha do observado eu tenho. Agora eu quero avaliar o quanto se desvia do esperado. Como calcular a [[Frequencia esperada|frequência esperada]] de cada célula? Intuição: quantas pessoas escolheram rock no total? 50. E qual é a proporção de homens e mulheres na amostra? Meio a meio. Então, se sexo e preferência fossem independentes, quantos homens deveriam ter escolhido rock e quantas mulheres? 25 e 25. É essa conta que a fórmula generaliza: o esperado da célula usa o total da linha vezes o total da coluna dividido pelo total geral. E aí, para todas as células, a estatística soma os (observado menos esperado) ao quadrado sobre o esperado: por exemplo, (30 − 25)² / 25.

Quantos graus de liberdade para esse teste? (R − 1) × (C − 1). Número de linhas: 2, menos 1, dá 1. Número de colunas: 3, menos 1, dá 2. 1 vezes 2, dá 2 graus de liberdade.

A soma da estatística deu 9,71. E a estatística crítica? Uso o INV do qui-quadrado: entrada é o alfa, 5%, e os graus de liberdade, 2. Dá 5,99. Qual é o valor da estatística que deixa 5% de área para a direita? 5,99. Onde está o meu valor, 9,71? Dentro da [[Regiao de rejeicao|região de rejeição]]. Então rejeito H0. E quem é o H0? As variáveis são independentes. Estou rejeitando a afirmação de que são independentes: tenho evidência de que existe associação entre sexo e preferência musical.

## Funções do Excel (português vs inglês)

Quem não achou a fórmula: o Excel de vocês está em português e o meu em inglês. Em português é a DIST.QUIQUA.CD, onde o CD é de cauda direita; em inglês está RT, right tail. Por isso eu quero que vocês façam a lista de exercícios e pratiquem: cada máquina é diferente, tem dia que o Excel está em inglês, tem dia que está em português, e eu preciso que vocês tenham o traquejo de entender o que estão fazendo, porque o Excel é só uma ferramenta de ajuda.

Tem também a função de teste do qui-quadrado: ela pede o vetor dos valores observados e o dos valores esperados, e devolve direto 0,28. Quem é esse 0,28? É o teu p-valor. Às vezes o enunciado está seguro o suficiente e pede só o p-valor, então essa função resolve em um passo.

Sobre o R-Commander: perguntaram se vai poder usar nas provas. Algumas outras turmas usam.

## Exercício em sala

Tem um exercício aqui da aula 5, o documento está no Eclass. Até me apontaram ontem que o gabarito pode não estar 100% correto, depois eu dou uma olhada. Mas tem que fazer esse exercício. No exercício: 100 no crédito, 60 no débito, 40 em dinheiro, contra as proporções esperadas (por exemplo, 45% de 200). A estatística calculada deu 2,54; a crítica, com alfa de 5% e 2 graus de liberdade, 5,99. O 2,54 fica fora da região de rejeição, então não rejeita H0. Cuidado na hora de digitar: o separador decimal é ponto, não vírgula.

Um dos exercícios ficou para a aula que vem. Quem terminou pode sair; eu fico aqui para fechar com quem precisar.
