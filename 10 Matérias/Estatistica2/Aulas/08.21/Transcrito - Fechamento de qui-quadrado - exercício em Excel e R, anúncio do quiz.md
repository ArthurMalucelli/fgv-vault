---
materias: [estatistica-2]
semestre: 2026.2
data: 2026-08-21
tipo: transcrito
tema: Fechamento de qui-quadrado - exercício em Excel e R, anúncio do quiz
status: completo
contract_version: 1
topicos: [teste qui-quadrado, aderência vs independência, graus de liberdade, Excel referências travadas, R matrix e chisq.test, qchisq, quiz]
tags: [aula, transcrito]
---

## Anúncio do quiz (terça 25/08)

Conforme a gente combinou, hoje fechamos o qui-quadrado na prática (a teoria a gente já fez), com mais um exercício para praticar. Na terça-feira faremos o nosso quiz: chegou, faz o quiz, quando termina vai embora. Mais ou menos uma hora, dez questões. Não é só fazer os testes: é fazer aquelas interpretações que eu estou reforçando com vocês.

Professor, posso fazer no R? Pode. Posso fazer no Excel? Pode. Posso fazer na mão? Pode. O que vocês preferirem.

## Revisão: para que serve o qui-quadrado

O que é o teste de qui-quadrado? Quero saber se alguma distribuição de dados que eu tenho desvia significativamente do que eu estou esperando: esse é o [[Teste qui-quadrado de aderencia|teste de aderência]]. E tem o [[Teste qui-quadrado de independencia|teste de independência]]: saber se as categorias de uma variável direcionam ou não as de outra, montando uma tabela de contingência.

O que vocês precisam dominar: como calcular a estatística de teste, e os [[Graus de liberdade|graus de liberdade]] de cada caso. Para a aderência, o grau de liberdade é k − 1. Para a independência, (linhas − 1) × (colunas − 1). E os H0: no teste de aderência, H0 é que a distribuição observada segue a esperada; no de independência, H0 é que as variáveis são independentes. Isso vem junto com o que a gente já fez de [[Teste de hipotese|testes de hipótese]] para média e proporção.

## Exercício no Excel (feito junto)

Primeiro a tabela do esperado: a [[Frequencia esperada|frequência esperada]] de cada célula é o total da linha vezes o total da coluna dividido pelo total geral. Atenção que o total não conta como categoria: numa tabela com 3 linhas e 4 colunas de dados, os graus de liberdade são (3 − 1) × (4 − 1) = 6.

Para arrastar a fórmula sem quebrar, tem que travar as referências certas com o cifrão (trava a linha do total de coluna e a coluna do total de linha, destrava para o resto): quem fez a lista no Excel sabe, é o jeitinho de copiar e colar sem refazer célula a célula.

Depois, a tabelinha das diferenças: cada célula vai ser (observado − esperado) ao quadrado sobre o esperado. O ao quadrado tira o negativo. E mantendo a somatória, a soma dessas células é o qui-quadrado calculado: é o quanto a tabela inteira está desviada do esperado. No exercício, deu 31.

Aí a decisão: com 6 graus de liberdade, o p-valor desse 31 dá 1,9 vezes 10 elevado a menos 5, um número muito pequeno (a área na cauda é 0,0001 e pouco). Ou seja, rejeita H0. Pelo caminho do valor crítico dá na mesma: o qui-quadrado crítico com 5% e 6 graus de liberdade é 12,59, e 31 está muito além. Ou você compara a estatística com o crítico, ou compara o [[Valor-p|p-valor]] com o alfa.

Se a alternativa da questão pedir especificamente o qui-quadrado crítico, cuidado para não responder o calculado no lugar.

## O mesmo exercício no R

Para quem quer fazer no R: ou importa as informações do Excel, ou monta a matriz na mão com a função matrix. Passa os valores (só os valores, sem os totais), diz em quantas linhas quebra e que é por linha: uma matriz 3 por 4. Organizem bem as informações para não perderem a questão por erro operacional. Dá para dar nome ao objeto (chamei a matriz de Catarina em homenagem à aluna): escreve o nome e ele mostra a matriz do jeitinho que estava na tabela. Colocar nomes de linhas e colunas é opcional, boa prática para projetos mais elaborados, mas para resolver o problema não precisa.

Com a matriz montada, a função do teste qui-quadrado resolve de uma vez: devolve a estatística, os graus de liberdade e o p-valor, e aí é só interpretar se rejeita ou não.

E o crítico? A função de quantil do qui-quadrado: entra a probabilidade e os graus de liberdade. Cuidado com o default: ele conta a área pela cauda esquerda (lower tail). Por isso eu coloquei 0,95 com 6 graus de liberdade, que dá o 12,59: contar da esquerda para a direita separando 95% é a mesma coisa que contar da direita para a esquerda separando 5%. Se você põe 0,05 sem ajustar a cauda, sai o valor errado do outro lado.

Sofia e Catarina estão fazendo Economia: quem mais estiver, dá uma olhada nessas duas formas, porque esse detalhe de cauda aparece direto.
