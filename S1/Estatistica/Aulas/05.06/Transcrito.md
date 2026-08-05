---
materia: Estatistica
data: 2026-05-06
tema: Inferência estatística e distribuição amostral da média
topicos: [Inferencia estatistica, Amostragem, Media amostral, Erro padrao, Distribuicao amostral da media]
tags: [aula, transcrito]
---

# Inferência estatística e distribuição amostral da média

## Reorganização do bloco de slides

Esse é o bloco de slides que estava previsto pra essa aula e pra próxima. Eu pensei melhor e vou quebrar em duas aulas. Acho que fica mais claro fazer assim, conceito numa aula, gincana com prêmios comestíveis na próxima.

## Problema motivador: bolacha de creme com gordura trans

Suponham que vocês foram contratados, como estagiários ou consultores, por uma empresa pra verificar como está o processo de produção da bolacha de creme. A embalagem anuncia, por bolacha, 0,2 gramas de gordura trans.

Olhando a população, vejo todo mundo comprando essa bolacha desesperado, dando pra criança. É uma alimentação que não tem nada a ver, só tem gordura. E o rótulo informa esses 0,2 gramas em média.

Em média. Em média porque nada é fixo na produção da bolacha. Tem variabilidade. Suponham que o desvio padrão é 0,5g. Ou seja, a fábrica anuncia 0,2g de média, mas com desvio padrão de 0,5g.

Quem acha que isso é normal? Por quê?

A média está muito desviada do padrão. Ou melhor, o desvio padrão é alto demais em relação à média. Se a média é 0,2 e o desvio é 0,5, na prática você tem bolachas com muito mais que 0,2g rodando.

Agora suponham outra realidade: medi a produção e deu média 0,24g, com desvio padrão menor. O que vocês acham agora? Está suave? Não sei se é suficiente pra parar a produção, mas tem que ser considerado. Eu acho que tem que parar a máquina imediatamente.

A questão de fundo: a média sozinha não te diz nada se você não olha a variabilidade junto. E é isso que [[Inferencia estatistica]] vem resolver.

## Os três blocos da estatística

A gente está abrindo agora o terceiro bloco da disciplina. O terceiro é a inferência. Inferência significa que eu tenho informação de uma [[Amostragem|amostra]] e a partir disso eu infiro algo sobre a população.

Imagina uma população em azul: tem pessoas, tem cachorros, tem chamadas telefônicas, tem eventos. Eu não tenho acesso à população inteira. Quero saber a altura média do aluno da FGV, mas não consigo medir todos. Então faço uma amostra.

Quando vocês fizeram aquele trabalho de pesquisa, a população de interesse era os alunos da FGV, mas vocês só conseguiram entrevistar uma amostra. O que vocês estão querendo dizer com a média da amostra é que o valor da população deve ser parecido com esse que a amostra mostrou.

Quanto melhor a amostragem, mais próxima a estimativa fica do parâmetro real.

## [[Parametros populacionais]] vs [[Estatistica amostral|estatísticas amostrais]]

Vou usar duas notações distintas. Da [[Populacao|população]], eu falo em parâmetros. Da amostra, eu falo em estatísticas.

Parâmetros populacionais (geralmente desconhecidos):
- μ: média populacional
- σ²: variância populacional
- p: proporção populacional

Estatísticas amostrais (calculadas a partir dos dados):
- X̄ ("X-barra" ou "X-chapéu"): [[Media amostral]]
- s²: variância amostral
- p̂ ("p-chapéu"): proporção amostral

A notação chapéu/barra é convenção pra dizer "estimador". Em português a gente diz "X-chapéu" mesmo, em inglês é hat. A ideia é a mesma: é o que a amostra te dá como melhor chute pra um parâmetro da população.

Então a gente usa as estatísticas da amostra pra tentar chutar o valor do parâmetro populacional. A dúvida é se esse chute pode ser inferido pra valer pra população. A inferência é exatamente esse problema: do que eu observei na amostra, o que eu posso afirmar sobre a população?

## Médias amostrais: tirar a amostra muitas vezes

Vou colocar todas as notas dessa classe num saco. A nota média da classe (populacional) é 100, com alguma variabilidade. Vou sortear três notas, anoto, devolvo, sorteio outras três. O saco nunca acaba, é como se eu tivesse reposição infinita.

Quantas amostras de tamanho 3 eu posso fazer com esse processo? Muitas, infinitas com reposição.

Para cada amostra eu calculo a média amostral. Tenho X̄₁, X̄₂, X̄₃, ... uma médias amostral pra cada amostra que eu tirar.

Repete isso com altura agora. Vou pegar três alunos sorteados, anota a altura, calcula a média do grupo de três. Volta esses três pra turma, sorteio outros três, anota a altura, calcula a média do segundo grupo. E assim por diante.

A pergunta é: se eu fizer isso muitas vezes, o que acontece com essas médias amostrais? Qual é a esperança delas? E qual é a variância delas?

## Esperança de X̄

A primeira pergunta é fácil. Quanto vale E(X̄)?

Vale μ. A esperança da média amostral é a própria média populacional.

```
E(X̄) = μ
```

Isso significa que, em média, o X̄ acerta. Se você tirar muitas amostras e calcular muitas médias, a média dessas médias converge pro valor populacional. Essa propriedade é o que torna X̄ um estimador não-viesado de μ.

## Variância de X̄

Aqui é a pergunta de cinco milhões de dólares. Quanto vale Var(X̄)?

Pensem comigo. Você concorda que a variabilidade entre médias amostrais é menor do que a variabilidade dos valores individuais? Por quê?

Suponham que eu sorteio três alunos. Vem um cara monstrinho, jogador de basquete, e duas pessoas habituais em altura. Quando eu calculo a média desses três, o efeito do gigante sobe um pouco a média, mas é diluído pelos outros dois. Eu estou pasteurizando o valor extremo.

Se tem alguém muito alto, tem mais duas pessoas que equilibram. Se tem alguém muito baixinho, tem mais duas pessoas que equilibram. Então as médias amostrais são mais parecidas entre si do que as alturas originais.

Conclusão: a variância das médias amostrais é menor que a variância da variável original.

Quanto menor? Não vou demonstrar, mas o resultado é:

```
Var(X̄) = σ² / n
```

Onde σ² é a variância populacional e n é o tamanho da amostra. Eu não demonstrei, mas parece razoável que seja menor. E quanto maior o n, menor ainda. Faz sentido: se em vez de pegar três alunos eu pegasse 39, a média daquela amostra ia ser quase indistinguível da média populacional. As X̄ ficariam todas muito próximas entre si.

Quanto maior o n, menor a variabilidade das médias amostrais. Isso está consistente com a fórmula: σ² no numerador, n no denominador.

## [[Erro padrao]]: o desvio padrão de X̄

Como o desvio padrão de uma variável é a raiz da variância, o desvio padrão de X̄ é:

```
DP(X̄) = σ / √n
```

Esse desvio padrão de X̄ tem nome próprio: **erro padrão**. Erro padrão é definido como o desvio padrão da estatística amostral. Quando alguém fala "erro padrão", está falando da dispersão das médias amostrais em torno de μ, não da dispersão da variável original.

Atenção: em nenhum lugar dessa conta apareceu a variância interna de uma amostra individual. Vocês pegaram três pessoas e calcularam a média, mas não calcularam a variância dessas três. O que estamos discutindo aqui é a variância da X̄, que é outra coisa: é a variância de várias médias entre amostras diferentes.

```
σ²        ← variância populacional (da variável X)
σ²/n      ← variância da média amostral X̄
σ         ← desvio padrão populacional
σ/√n      ← erro padrão (desvio padrão de X̄)
```

## Caso normal: se X é normal, X̄ também é

Considera uma população X com média μ e desvio padrão σ, normalmente distribuída.

Eu tiro amostras de tamanho 4 dessa população. Calculo X̄ pra cada amostra: X̄₁, X̄₂, X̄₃, ...

O que está escrito no slide é que, se X é normal, então X̄ também é normal. Cacete, mas é demonstrado. Não vou demonstrar agora, mas essa é uma propriedade conhecida: combinação linear de normais é normal, e X̄ é uma média ponderada de variáveis normais.

```
Se X ~ N(μ, σ²), então X̄ ~ N(μ, σ²/n)
```

Mesma média, variância dividida por n. Graficamente, o histograma de X̄ tem o mesmo centro da distribuição original, mas é mais "magrinho", mais concentrado em torno da média.

Repara que isso vale **se a população X já é normal**. Pra outras distribuições, o resultado de X̄ ser normal vem do Teorema do Limite Central, que a gente vê depois.

## Exemplo: altura na FGV

Suponham que a altura X dos alunos da FGV seja normal com média 1,70 m e desvio padrão 10 cm. Está desenhado o histograma da altura, normal, centrado em 1,70.

Pegunta: se eu sortear muitas amostras aleatórias de tamanho 100, qual fração dessas amostras vai ter X̄ entre 1,69 m e 1,71 m?

O primeiro impulso é: vou calcular a probabilidade de uma pessoa ter altura entre 1,69 e 1,71. Mas a pergunta não é essa. A pergunta é sobre a média amostral X̄, não sobre o indivíduo.

Pra responder, eu preciso da distribuição de X̄. A média de X̄ é μ = 1,70 m. O desvio padrão de X̄ não é 10 cm. É:

```
σ/√n = 10 / √100 = 10 / 10 = 1 cm = 0,01 m
```

Então X̄ ~ N(1,70 ; 0,01²).

Agora a pergunta vira: P(1,69 ≤ X̄ ≤ 1,71). Isso é μ ± 1·σ_X̄ (um desvio padrão da média amostral pra cada lado). Pela regra empírica, dá aproximadamente 68%.

A diferença chave: se a pergunta fosse sobre uma única pessoa, o cálculo usaria σ = 10 cm e a probabilidade seria muito menor. Por usar a distribuição de X̄, o desvio padrão é 1 cm, e a mesma faixa cobre uma proporção muito maior das amostras.

## Exemplo: tempo de chamada telefônica

Vamos pegar antes da internet existir. Vocês todos nasceram com internet. Quando eu trabalhava, lá em 1999, a gente tinha telefone fixo. Você pegava o aparelho, discava, e fazia uma ligação internacional. Antes ainda, na época do meu pai, ele importava coisas da Tchecoslováquia, e era complicado. Agora hoje em dia, com WhatsApp, a chamada custa zero, mas o tempo da ligação ainda tem distribuição estatística.

Suponham então que o tempo T de uma chamada internacional tem distribuição normal com média 8 minutos e desvio padrão 2 minutos.

```
T ~ N(μ = 8 ; σ = 2)
```

### Pergunta 1: probabilidade individual

Qual a probabilidade de a próxima chamada ter duração entre 7,8 e 8,2 minutos?

```
P(7,8 ≤ T ≤ 8,2) = DIST.NORM.N(8,2; 8; 2; 1) − DIST.NORM.N(7,8; 8; 2; 1)
                 ≈ 0,0797 ≈ 7,97%
```

A faixa é estreita comparada ao desvio padrão de 2 minutos, então a área é pequena.

### Pergunta 2: probabilidade pra média amostral

Agora, se selecionarmos amostras aleatórias de 25 chamadas cada, e pra cada amostra calcularmos a média T̄, qual fração dessas amostras vai ter T̄ entre 7,8 e 8,2?

A curva de T̄ é mais "magrinha". Mesma média 8, mas o desvio padrão de T̄ é:

```
σ_T̄ = σ / √n = 2 / √25 = 2 / 5 = 0,4 minuto
```

Então T̄ ~ N(8 ; 0,4²). Calcula com Excel:

```
P(7,8 ≤ T̄ ≤ 8,2) = DIST.NORM.N(8,2; 8; 0,4; 1) − DIST.NORM.N(7,8; 8; 0,4; 1)
                 ≈ 0,3829 ≈ 38,3%
```

Comparação:
- Individual (T): faixa cabe em 0,1 desvio padrão de cada lado → ≈ 7,97%
- Média de 25 (T̄): faixa cabe em 0,5 desvio padrão de cada lado → ≈ 38,3%

Se a curva é mais magra, a mesma faixa fixa em valor absoluto cobre mais área proporcionalmente. É a mesma distância no eixo, mas em "unidades de desvio padrão" ela cresceu cinco vezes.

## Mensagem central da aula

Não confundir três coisas distintas:

```
σ        desvio padrão da variável X (dispersão dos indivíduos)
σ/√n     erro padrão (dispersão de X̄ entre amostras)
s        desvio padrão amostral interno (calculado em uma amostra individual)
```

A inferência se constrói sobre o erro padrão. Quando a gente vai fazer intervalo de confiança ou teste de hipótese, é a [[Distribuicao amostral da media]] que importa, não a distribuição da variável original.

## Próxima aula

Continua o assunto de amostragem. Vai ter gincana em aula com prêmios comestíveis. Ainda no terreno conceitual, sem cálculo pesado.
