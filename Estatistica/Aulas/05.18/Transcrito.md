---
materia: Estatistica
data: 2026-05-18
professor: Nelson
tema: Intervalo de Confiança para a média (parte 1) e discussão sobre uso de IA
topicos: [Intervalo de Confiança, Margem de Erro, Z de alfa sobre 2, Nivel de Confianca, Estimacao por ponto, Estimacao por intervalo, Tamanho da amostra, Distribuicao amostral da media]
tags: [aula, transcrito]
---

# Intervalo de Confiança para a média (parte 1) + uso de IA

## Avisos sobre prova final

Prova final está marcada para **8 de junho, às 15h**. Nas minhas três classes, ninguém deixou a prova parcial para a segunda chamada, o que é bom. Recomendo que ninguém deixe a prova final para a segunda chamada também. A não ser que você fique doente, claro.

Por que falo isso? A segunda chamada é pelo menos uma semana, dez dias depois. Para que as pessoas não deixem propositalmente, a gente faz a segunda chamada um tanto mais difícil que essa, proporcional ao tempo extra que vocês teriam para estudar. Então, a não ser que você queira estudar mais e fazer uma prova mais difícil, recomendo fazer no dia certo.

Para nenhuma disciplina eu recomendo deixar para a segunda chamada. É desconfortável, mistura várias disciplinas na mesma classe, não é um ambiente legal. A prova final não vai ser igualzinha à parcial, porque as questões da parcial vocês já conhecem. Vão ser outras, no mesmo estilo. Vou publicar também a prova simulada e os quizzes abertos após as próximas aulas.

O que eu cobro principalmente na prova é a partir da parcial em diante. Em média, pode aparecer um boxplot, mas não vai ser o foco.

## Sobre uso de IA pelos alunos

A aula de hoje é difícil, mas se vocês prestarem atenção, vão ter um ganho legal.

Antes de começar, queria falar uma coisa. Esse fim de semana eu fui para Minas Gerais, com muitos professores e alguns alunos convidados, e a gente trabalhou o fim de semana inteiro no hotel num planejamento estratégico do nosso curso.

Uma das coisas que a gente discutiu foi o uso de IA pelos alunos. Apareceu lá que muitos alunos fazem o seguinte: pegam os slides da matéria, os exercícios, tudo isso, e carregam na IA. Daí começam a fazer perguntas para tirar dúvidas, perguntar melhor forma de estudar, um monte de coisa, e a IA responde. Você passa a ter um professor particular em casa.

Quem usa isso? Um, dois, três… dez alunos. A gente não tinha a percepção de que tantos alunos estão fazendo isso, a gente achava que era raro. E percebemos, escutando vocês, que é muito comum. **Eu acho útil.** Você tem um professor particular esclarecendo dúvidas. Às vezes ele fala besteira, às vezes ele avança na matéria, coisa que vocês não aprenderam ainda, mas no geral é útil. Depende da IA que você usa, você pode restringir o contexto.

Parte 2 da história. Os alunos do quinto semestre tinham que escolher a área de concentração até domingo, 23h59. Durante o domingo, que ninguém fica olhando o sistema, o sistema caiu. Muitos alunos que tiveram aula comigo ficaram desesperados e mandaram e-mail direto pra mim. **Todos esses e-mails foram escritos com IA.** Estavam super educados, mas não foi o aluno que escreveu, não está na linguagem do aluno. Nada contra, mas…

Será que a gente não está perdendo a segurança de fazer texto sem IA? Isso vale também para quem está fazendo exercícios seguindo muito rápido e já pedindo pra IA explicar.

**Cuidado, isso pode minar a confiança de vocês em vocês mesmos**, a sensação de que você só vai conseguir fazer as coisas com IA. Várias habilidades a humanidade está perdendo a confiança em si mesma. Isso é mal.

Se você perder a confiança de resolver um problema por si só, o teu empregador não vai te contratar pra você fazer as coisas só usando IA. Porque senão ele usava IA direto e não te contratava. Claro que você vai usar IA como ferramenta, e a IA daqui a cinco anos vai estar mais envolvida, do mesmo jeito que você usa corretor ortográfico, Excel, calculadora. É mais uma ferramenta. Mas cuidado pra não perderem a confiança em vocês mesmos.

É um e-mail. Se você precisa de IA pra tudo, logo, logo chega no paralelo daquela atendente de supermercado que, se você dá uma nota de 10 e tem que dar 5 de troco, ela usa a calculadora. Cuidado pra não ficarem excessivamente dependentes de IA.

Vocês já viram que pras provas, tudo bem, você entendeu tudo. Mas pra fazer exercícios novos, você tem aquele desafio da página em branco na frente e tem que começar de algum lugar. Esse desafio é super importante, em todas as matérias. Não se privem dele.

## Recap: estimação por ponto

No trabalho de vocês, vocês entregaram, mostraram o que fizeram. A gente fez uma análise crítica de como poderia ser, claro que fazer uma amostra probabilística não é tão fácil pra vocês, porque vocês não têm verba pra isso, como é que vocês vão fazer uma amostra sorteada se a sua [[Populacao|população]] é a cidade de São Paulo? Não é tão fácil.

Mas o mais importante é que, apesar disso, vocês obtiveram alguns X̄ e algumas proporções amostrais. Das variáveis quantitativas, vocês obtiveram X̄ e falaram "a [[Media amostral|média amostral]] é tanto". Mas pra que vocês fizeram isso?

Ninguém está interessado na amostra que vocês fizeram. Na verdade, o que vocês estão implicitamente dizendo é que **o μ na população-alvo deve ser parecido com o X̄**. Se alguém calculou que a idade média da amostra é 19,4 anos, no fundo está dizendo que na população a idade média deve ser parecida com 19,4. Isso é uma **[[Estimacao por ponto|estimativa por ponto]]**: você obteve um número que diz que o [[Parametros populacionais|parâmetro populacional]] deve ser parecido com esse número.

O que nós vamos fazer hoje é a **[[Estimacao por intervalo|estimação por intervalo]]**. Se o teu X̄ deu 14, você vai dizer 14 com uma faixinha pra um lado e pra o outro. É uma estimativa intervalar, a mesma coisa que se faz em pesquisa eleitoral (que não é média, é proporção): o candidato A teve 20% dos votos da pesquisa com dois pontos percentuais para cima ou para baixo. Isso é estimativa intervalar. Hoje pra média, daqui a duas aulas pra proporção, eleições etc.

## Recap: símbolo Z de α

Primeira coisa que vimos no final da aula passada é um símbolo que aparece em fórmulas como anotação. Sempre que numa fórmula aparecer Z de, por exemplo, 2,5%, o que a gente quer dizer?

Se eu pegar uma [[Distribuicao normal|normal]] e colocar uma cauda à direita com exatamente 2,5% de área, quantos desvios padrão eu vou pôr além da média? **Esse "quantos" é o Z de 2,5%.**

Então, pra alguém falar numa fórmula "Z de 2,5%", quero saber quantos desvios padrão preciso acrescentar à média numa normal pra que a cauda direita tenha exatamente 2,5% de área.

A melhor forma de calcular é pegar o caso particular μ = 0 e σ = 1, porque daí esse ponto passa a ser exatamente o Z de 2,5%. Calculo com `INV.NORM(1 − 2,5%; 0; 1)`, dá 1,96. Forma resumida: `INV.NORM.P.N(1 − 2,5%)`, que já assume média 0 e desvio padrão 1.

Não é sempre 2,5%. Esse Z aparece numa fórmula pequenininha que vamos ver hoje.

## O slide mais difícil da aula

Entendendo isso, você entendeu o intervalo de confiança.

Na aula da [[Distribuicao amostral da media|distribuição amostral da média]], eu chamei trincas de pessoas aqui. Obtive um X̄₁ = 1,70 m, um X̄₂ = 1,69 m, um X̄₃ = 1,72 m. Eu podia ter quantas amostras quisesse, todas de tamanho 3. Construí um histograma desses X̄.

No meio da distribuição está a média, porque a esperança de X̄ é o μ da população. Vou pintar de azul **95% dessa área**: 95% dos X̄ caem dentro do azul, 2,5% caem fora para a direita e 2,5% caem fora para a esquerda. O pontilhado é o que separa a área azul da branca.

A distância do meio (μ) até esse pontilhado eu vou chamar de **E**. Pode ser Ernesto, Elefante, o que você quiser. Por enquanto é E. Do outro lado também é E.

Agora vou colocar no desenho cada um daqueles X̄: X̄₁ caiu aqui dentro, X̄₂ aqui dentro, X̄₃ caiu fora da faixa azul (em vermelho, é mais raro).

Ao redor de cada X̄, vou colocar um bracinho para a direita e para a esquerda, sempre do mesmo tamanho E. Chamo isso de **intervalo**.

Olha o caso de X̄₁: como X̄₁ está à esquerda do pontilhado direito, e o bracinho tem tamanho E (igual à distância do μ até o pontilhado), com certeza esse bracinho ultrapassa o μ. **O intervalo inclui o μ.**

X̄₂ está à direita do pontilhado esquerdo, com bracinho E para cada lado, ele também ultrapassa o μ. **Inclui o μ.**

Mas X̄₃, que é mais raro, está fora da faixa azul, à direita do pontilhado direito. Como o bracinho tem só tamanho E, ele não alcança o μ. **O intervalo NÃO inclui o μ.**

Conclusão: 95% dos X̄ caem entre os dois pontilhados. Logo, **95% dos intervalos construídos como X̄ ± E vão incluir o μ verdadeiro da população**.

Se eu pegar uma única amostra (ninguém pega 500 amostras na prática, pega uma), qual é a probabilidade do X̄ estar nessa faixa pontilhada? 95%. Qual é a probabilidade do bracinho de tamanho E incluir o μ da população? 95%.

A gente diz que isso é um **[[Intervalo de Confiança|intervalo com 95% de confiança]] de incluir o μ da população**.

## Quanto vale E

Falta saber quanto é E. Como aqui (no meio) é μ, e o pontilhado está a 1,96 desvios padrão de X̄ da média, então **E = 1,96 · σ_X̄**. E a gente aprendeu que σ_X̄ = σ/√n (o sigma da população original dividido por raiz de n, o [[Erro padrao|erro padrão]]).

Esse E não vai se chamar Ernesto nem Elefante. Vai se chamar **[[Margem de Erro|erro]] ou margem de erro**. É o tamanho do bracinho.

Pra 95% de confiança:

```
E = 1,96 · σ / √n
```

Mas como é que eu sei o μ? Como é que eu sei o σ da população?

Nessa aula tem esse mistério. Em **99% dos casos a gente não sabe quanto é o σ da população**. Mas nessa primeira aula a gente finge que sabe. Na próxima aula a gente supera isso, arrancando esse σ de algum jeito da amostra. Por enquanto, acredite: por estudos anteriores você sabe a dispersão, e quer cercar a média.

> **Pergunta (Luca)**: como você chegou no 1,96?
>
> Você pode tirar várias amostras de uma população. Na prática você só tira uma. Mas se tirar várias e desenhar o histograma de X̄, vou admitir que é normal (depois falo disso). Posso pintar 95% da área de azul. Sobra 2,5% pra cada lado. Quantos desvios padrão eu preciso pra ter 95% no meio? Pela regra empírica, mais ou menos dois desvios padrão dá 95%. Mais precisamente, **1,96** desvios padrão. Calcula com `INV.NORM(1 − 2,5%; 0; 1) = 1,96`.

## Generalizando: nível de confiança γ

A gente acabou de ver que o tamanho do bracinho é 1,96 · σ_X̄, e que σ_X̄ = σ/√n. Mas esse 1,96 é sempre 1,96? Não.

A gente usou 95% das amostras. Então minha **confiança (γ)** é 95%. E os 5% de chance do μ não estar dentro?

A gente chama esse complemento de **α** (alfa). Se γ = 95%, então α = 5%. Calcula α/2 = 2,5%. Em vez de escrever 1,96 na fórmula, escrevemos **Z de α/2**.

Se γ = 95%, então Z_(α/2) = 1,96. Se a confiança mudar, esse número muda.

A fórmula mágica da aula:

```
E = Z_(α/2) · σ / √n
```

Como chegar no Z? Pega γ, calcula α = 1 − γ, calcula α/2. Então:

```
Z_(α/2) = INV.NORM.P.N(1 − α/2)
```

Pra γ = 95%, dá `INV.NORM.P.N(1 − 0,025) = 1,96`.

## Exemplo 1: parque em SP, planejamento da pesquisa

Vai ser feito um estudo pra estimar o gasto médio com alimentação num certo parque na cidade de São Paulo. Não restaurantes, coisas tipo pipoca, água de coco, refri. Quero estimar na população, obviamente. Não consigo entrevistar todo mundo que foi ontem, hoje, amanhã. Tenho que fazer amostra.

**Dados**: serão entrevistadas n = 400 pessoas, com γ = 95% de confiança. Pressuposto: σ populacional = 100 (milagre, eu não sei como, na próxima aula superamos isso).

Sem ter feito a pesquisa ainda, eu já consigo saber o tamanho do bracinho:

```
γ = 95%
α = 5%
α/2 = 2,5%
Z_(α/2) = INV.NORM.P.N(1 − 0,025) = 1,96

E = Z_(α/2) · σ / √n
E = 1,96 · 100 / √400
E = 1,96 · 100 / 20
E ≈ 10
```

Bracinho de **R$ 10**. Quando eu fizer a pesquisa vou obter um X̄, e o meu intervalo de 95% de confiança vai ser X̄ ± 10.

Vocês acham adequada essa margem de erro de R$ 10? Depende. Se o gasto médio for tipo R$ 7, dez é muito (quase 2× o valor). Se for R$ 60, daria de 50 a 70, parece ok. Margem de erro só faz sentido em relação à grandeza do que você está medindo.

## Exemplo 2: pesquisa feita, IC concreto

Fiz a pesquisa com as 400 pessoas. Deu X̄ = 34,20. Construa o intervalo de confiança de 95%.

```
IC₉₅% = X̄ ± E
      = 34,20 ± 10
      = [24,20 ; 44,20]
```

Vocês estão felizes com esse intervalo? Pra suas decisões (montar uma franquia, por exemplo), dizer que o gasto médio varia entre R$ 24,20 e R$ 44,20 é útil? A aluna achou que está grande, porque a margem de erro é um terço do X̄.

## Exemplo 3: tamanho de amostra pra reduzir E pela metade

Como diminuo a margem de erro? Olhando a fórmula `E = Z · σ / √n`, eu quero E menor. A confiança você não quer mudar. O σ da população não dá pra mudar. Resta **aumentar o n**.

Aumentar pra quanto? Quero E = 5 (metade dos 10). Será que basta dobrar a amostra?

Inverte a fórmula:

```
E = Z_(α/2) · σ / √n
√n = Z_(α/2) · σ / E
n = (Z_(α/2) · σ / E)²
```

Com γ = 95%, σ = 100, E = 5:

```
n = (1,96 · 100 / 5)²
n = (196/5)²
n ≈ 1.537 (mais exato: 1536,64 → arredonda pra cima → 1.537)
```

**Pra dividir a margem de erro por 2, tenho que quadruplicar o n.** Sai muito mais caro: 400 vs 1.537 pessoas.

> **Fetiche dos estatísticos**: sempre arredonda pra cima. Mesmo que dê 1.536,01, vai pra 1.537. Pra "ser suficiente".

Por causa daquela raiz quadrada, é **muito custoso** diminuir a margem de erro.

## Exemplo 4: e se eu baixar a confiança?

Tudo bem, eu queria E = 5, mas não tenho dinheiro pra 1.537 entrevistas. O que faço? **Baixo a confiança**. Não é questão de vida ou morte, é alimentação.

Mesma fórmula, agora com γ = 90%:

```
γ = 90%
α = 10%
α/2 = 5%
Z_(α/2) = INV.NORM.P.N(1 − 0,05) = 1,645

n = (1,645 · 100 / 5)²
n = (32,9)²
n ≈ 1.082,4 → arredonda → 1.083
```

Melhor: 1.083 em vez de 1.537. Baixei a confiança e a amostra ficou um pouco menor.

> **Pergunta (recorrente todo semestre)**: se eu uso `INV.NORM.P.N`, estou admitindo média 0 e desvio padrão 1, que não bate com o problema.
>
> Não. Isso é só pra calcular o **Z_(α/2)**, que é uma constante. Pra calcular ele, eu pego uma normal de média 0 e desvio padrão 1 (caso particular). É um artifício, **não tem nada a ver com o desvio padrão do problema**.

## Exemplo 5 (exercício pra casa): assentos de avião

Uma empresa de aviação decidiu estudar o número de assentos ocupados em seus voos (pra ser ruim, deveria ser desocupados, mas vamos seguir o enunciado). Tomaram amostra de **n = 64 voos**, e o número médio de assentos ocupados foi **X̄ = 15,2**. Admita que o desvio padrão populacional é **σ = 6** (mesmo milagre).

**Item 1**: estime o número médio com IC de 95%.

```
γ = 95%, Z_(α/2) = 1,96
E = 1,96 · 6 / √64
  = 1,96 · 6 / 8
  = 1,47

IC₉₅% = 15,2 ± 1,47 assentos
      = [13,73 ; 16,67]
```

**Item 2**: que tamanho de amostra eu preciso pra ter E = 1?

```
n = (1,96 · 6 / 1)²
n = (11,76)²
n ≈ 138,29 → arredonda → 139 voos
```

Sempre confere a ordem de grandeza: 2 · 6 = 12, 12² = 144, deu próximo de 139. Bate.

## Tabela mental de Z mágicos

Confiança é quase sempre 90, 95 ou 99. Decora:

| γ | α | α/2 | Z_(α/2) |
|---|---|-----|---------|
| 90% | 10% | 5% | 1,645 |
| 95% | 5% | 2,5% | 1,96 |
| 99% | 1% | 0,5% | 2,58 |

O 1,96 e o 1,645 dá pra decorar. Esse 2,58 do 99% eu não sei de cor, acabo fazendo no Excel.

## Suposições pra tudo isso valer

Duas premissas grandes:

1. **σ populacional é conhecido**. Não sei de onde. Próxima aula superamos.
2. **X̄ é normal**. Pra eu desenhar aquela curva de sino e fazer 95% no meio, X̄ tem que ser normal. Dois casos em que vale:
   - X é normal → X̄ é normal pra qualquer n
   - X é qualquer coisa, mas n > 30 → X̄ é aproximadamente normal ([[Teorema do limite central|TLC]])

No trabalho de vocês, com certeza vocês não sabem o histograma populacional. Por isso eu pedi pra fazer com **n ≥ 40**. Daí tudo o que vimos hoje vale.
