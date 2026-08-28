---
materias: [estatistica-2]
semestre: 2026.2
data: 2026-08-14
tipo: transcrito
tema: Teste de Hipóteses para Proporções
status: completo
contract_version: 1
topicos: [proporcao amostral, teste de proporcao, teste unicaudal, valor critico unicaudal, distribuicao de bernoulli, valor-p, erro tipo I, erro tipo II]
tags: [aula, transcrito]
---

## Recap: a receita do teste de hipóteses

A lógica de sempre: eu tenho uma pergunta sobre a minha população, mas não tenho todas as observações. Eu pego uma amostra e, a partir dela, busco fazer [[Inferencia estatistica|inferências]] sobre a população. Se eu assumo que a [[Media amostral|média amostral]] se distribui conforme a distribuição normal (e o [[Teorema do limite central]] me deixa assumir isso), eu consigo, com um certo número de desvios abaixo ou acima da média, montar um [[Intervalo de Confiança|intervalo]] com uma certa confiabilidade. O [[Teste de hipotese|teste de hipótese]] aplica essa mesma base: eu tenho uma afirmação inicial sobre a população, e a minha amostra traz informação relevante pra rejeitar ou não rejeitar aquela afirmação.

A receita de bolo continua a mesma. Defino as hipóteses, calculo a [[Estatistica de teste|estatística de teste]], que mede o quanto a minha amostra se desvia do que a hipótese nula afirma. Depois, pra tomar a decisão, eu uso o [[Valor critico|valor crítico]] ou calculo o [[Valor-p|p-valor]]. As duas coisas dão a mesma base pra decisão, mas vocês vão ser perguntados das duas maneiras, tanto por p-valor quanto por valor crítico. A regra do p-valor: se ele é menor do que o alfa, rejeito; se é maior, não rejeito.

## Erro Tipo I e Erro Tipo II

O que é o alfa? É a probabilidade do [[Erro Tipo I]]: a área na cauda, assumindo que a hipótese nula seja verdadeira. Eu posso rejeitar H0 e ela ser verdadeira, porque calhou de eu pegar uma amostra muito atípica. Esse risco sempre existe, e a probabilidade dele é o próprio alfa. O [[Erro Tipo II]] é o oposto: não rejeitar H0 quando ela é falsa.

## Da média pra proporção

Até agora a gente testava média. Hoje entra proporção, e a lógica é a mesma: assim como a média amostral fala da média populacional, a proporção amostral fala da proporção populacional.

Como isso aparece na prática? Tem eleição daqui a dois meses. A proporção de eleitores de cada candidato, de verdade, só existe depois que fecham as urnas. Mas vocês já viram inúmeras pesquisas de intenção de voto. O que são essas pesquisas? Seleciona-se uma amostra, pergunta-se em quem cada pessoa vai votar, calcula-se a proporção da amostra que vota em cada candidato, e infere-se que essa será, aproximadamente, a proporção na população.

O que muda em relação à média? Proporção é pertencer ou não pertencer a um grupo. É uma coisa dicotômica: a variável só assume dois valores, 0 ou 1. E vocês já viram o modelo de probabilidade de uma variável assim. Com um ensaio só é a [[Distribuicao de Bernoulli|Bernoulli]], que vale 1 com probabilidade p e 0 com probabilidade 1 menos p. Com vários ensaios, é a [[Distribuicao binomial|binomial]].

## A distribuição da proporção amostral

A média amostral tinha distribuição normal, com média μ e desvio padrão σ/√n. E a proporção amostral?

A [[Proporcao amostral|proporção amostral]] p̂ nada mais é do que a média de um monte de zeros e uns: eu somo as observações (cada uma vale 0 ou 1) e divido por n. A média dela é o próprio p.

E a variância? Aqui entra uma propriedade que vocês já viram: multiplicar uma variável por uma constante multiplica a média pela constante, e a variância pela constante ao quadrado (ver [[Transformacao linear de variavel aleatoria]]). O professor relembrou com um exemplo numérico rápido: multiplicando todos os números de um conjunto por uma constante, a média sai multiplicada pela constante, e a variância pela constante ao quadrado. Aplicando aqui: p̂ é 1 sobre n vezes a soma das observações, então a variância de p̂ é 1 sobre n ao quadrado vezes a variância da soma. Cada observação 0/1 tem variância p(1 − p), a soma de n delas tem variância n vezes p(1 − p), e sobra:

Var(p̂) = p(1 − p) / n

O desvio padrão da proporção amostral, o [[Erro padrao|erro padrão]] dela, é a raiz disso: √(p(1 − p)/n).

## A estatística de teste pra proporção

A gente não fez outra coisa no teste da aula anterior: pego o que calculei na amostra, vejo o quão distante está do valor da hipótese sobre a população, e divido pelo desvio padrão. Agora faço exatamente isso com a proporção. Pego a proporção que calculei na amostra, vejo o quão distante está da proporção que estou testando, e divido pelo desvio padrão da proporção amostral:

z = (p̂ − p₀) / √(p₀(1 − p₀)/n)

O que muda na prática, na nossa conta, é só esse desvio padrão.

## Exemplo: a promoção no clube de golfe

Você começa a trabalhar num clube de golfe, olha as informações de quem joga e percebe que só 20% são mulheres. Vamos tentar melhorar isso: o clube faz uma promoção pra atrair mulheres, do tipo compre uma rodada e leve outra. Depois da promoção, você pega uma amostra de 400 pessoas e conta quantas são mulheres: a proporção da amostra deu 25%. Posso falar que a minha promoção foi bem-sucedida?

Primeiro, as hipóteses. Como é que eu vejo na prova se é unicaudal ou bicaudal? Neste caso é [[Teste unicaudal|unicaudal]], porque eu quero saber se a proporção aumentou. Não importa pra mim se ficou só "diferente": ficar igual ou ficar menor, pra minha decisão, dá no mesmo (a promoção não funcionou). O H0 é o meu baseline, aquilo contra o que eu vou testar: p menor ou igual a 0,20. A alternativa é o que eu quero verificar: p maior que 0,20.

Em termos absolutos, sim, 0,25 é maior que 0,20. Mas eu quero ver se esse desvio é estatisticamente significante. Pra isso preciso do desvio padrão da proporção amostral: raiz de 0,20 vezes 0,80, sobre 400. No numerador, 0,20 vezes 0,80 dá 0,16, e raiz de 0,16 é 0,4. Raiz de 400 é 20. Então 0,4 sobre 20: 0,02.

Agora a estatística de teste: estou com 0,25, testando contra 0,20, desvio padrão de 0,02. z = (0,25 − 0,20) / 0,02 = 2,5.

Com o valor calculado a 2,5 desvios de distância, o meu p-valor vai ser grande ou pequeno? Pequeno: quanto mais distante a estatística, menor a área que sobra na cauda. Então, rejeito ou não rejeito H0? Rejeito. E o que era o H0? Que a proporção seguia em 20% ou menos. Se eu rejeito isso: opa, muito bom, a proporção de mulheres subiu.

## Valor crítico unicaudal: 1,645, não 1,96

Dava pra decidir também pelo valor crítico, mas atenção: o crítico aqui não é 1,96. O 1,96 é o Z que deixa 2,5% em cada cauda, o [[Z de alfa sobre 2]] do teste bicaudal. Como o teste é unicaudal, eu quero o Z que deixa os 5% inteiros numa cauda só, e esse é 1,645, menor que o 1,96. Eu quero toda a minha área de rejeição de um lado: a [[Regiao de rejeicao|região de rejeição]] vai de 1,645 até o infinito. Como 2,5 cai dentro dela, a decisão é a mesma: rejeita.

## E se o n aumenta? (pergunta de quiz)

Uma questão mais teórica que às vezes dá um nó e que vale olhar com calma. Tudo mais igual, a única coisa que muda é o [[Tamanho da amostra|n]]: o que acontece se o n aumenta? O erro padrão, que tem raiz de n no denominador, diminui. A estatística de teste inteira, então, aumenta. E se a estatística aumenta, a chance de rejeitar é maior ou menor? Maior. Essa questão a gente gosta de colocar no quiz: vocês precisam entender todos os detalhes do que pode afetar a sua decisão.

## O que o resultado significa (pergunta de aluno)

Um aluno perguntou se o resultado quer dizer que agora tem mais mulheres jogando. A resposta exige cuidado. O que eu rejeitei foi o H0, de que a proporção era menor ou igual a 20%. Rejeitar isso significa que eu tenho fortes evidências de que a proporção populacional aumentou. Mas o 0,25 é a proporção da amostra, não é "a" proporção da população: o teste não me entrega o valor novo da proporção populacional, me entrega evidência de que ela passou de 0,20. E vocês vão ser cobrados nos quizzes não só de calcular, mas de interpretar o resultado do teste.

## Variância máxima: p = 0,5

Último ponto teórico. Se eu tenho uma variável que só assume dois valores, 0 ou 1, quando a variância dela é mínima? Se todos os elementos forem 0, ou todos forem 1, eu não tenho variabilidade nenhuma: variância zero. E quando ela é a maior possível? Quando a chance de cada valor é exatamente a metade, p igual a 0,5. Dá pra ver pela fórmula: p(1 − p) é uma parábola com concavidade pra baixo, que zera em p = 0 e em p = 1 e atinge o máximo no meio, em 0,5.

## Exercício e próxima aula

O professor deixou no eClass um exercício em Excel sobre o conteúdo de hoje, pra abrir e tentar fazer.

Semana que vem fecha a parte de testes com o teste de qui-quadrado, que é essencialmente a mesma lógica de teste de hipóteses.
