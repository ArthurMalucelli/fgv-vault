---
materia: Estatistica
data: 2026-05-20
professor: Nelson
tema: Intervalo de Confiança para média (parte 2), Z vs T, distribuição T de Student
topicos: [Intervalo de Confiança, Margem de Erro, Distribuicao T de Student, Graus de liberdade, Teorema do limite central, Amostragem aleatoria simples, Z de alfa sobre 2]
tags: [aula, transcrito]
---

# IC para média (parte 2): σ desconhecido, Z vs T e Teorema do Limite Central

## Avisos administrativos

Na quarta-feira a gente vai ter [[Intervalo de Confiança|intervalo de confiança]] para proporção de uma população. E acabou tudo, é o último episódio dessa parte. Na quarta-feira também vai ter a quarta provinha, estilo de sempre, e dessa vez eu não vou arredondar feito maluco, vocês vão entender por quê. São intervalos que a gente vai explicar no final da aula.

Depois, na última aula, tem apresentações que eu também vou explicar o que é no final da aula de hoje.

No site tem o PDF da última aula, tem o intervalo de confiança para média (segunda aula, que é a aula de hoje), e tem o simulador, que eu talvez mostre para vocês na próxima aula. Tem também o vídeo da primeira aula: há dois semestres atrás eu não pude dar a primeira aula de intervalo de confiança porque o prédio estava interditado, então gravei a aula remota. É a mesma aula que vocês tiveram aula passada, gravada para outra turma. Vocês podem assistir trechos em 2x se quiserem. Os vídeos dessa aula de hoje, da época da pandemia, já sumiram do servidor, faz muito tempo.

## Recap: a fórmula da aula passada e o problema dela

A gente aprendeu [[Estimacao por intervalo|intervalo de confiança]] para [[Media amostral|média populacional]] **supondo que a gente conhece, não sei como, o desvio padrão populacional**. O intervalo é:

```
IC_γ% = X̄ ± Z_(α/2) · σ / √n
```

A parte do ± é a [[Margem de Erro|margem de erro]]. Esse alfa é 1 − γ, complemento da confiança. Se γ = 95%, então α = 5%, e o [[Z de alfa sobre 2]] é o ponto da [[Distribuicao normal|normal padrão]] que deixa 2,5% na cauda à direita. Você não precisa ficar pensando isso a cada vez. A fórmula é pronta, só precisa lembrar da demonstração.

Mas no trabalho de vocês, vocês têm um X̄, têm o tamanho da amostra (100 pessoas, por exemplo), mas **não têm o σ da população**. Vocês têm o S da amostra. Como é que vocês fariam o intervalo de confiança? Esse é o objetivo da aula de hoje.

## O que a amostra serve para

A [[Amostragem|amostra]] é utilizada para obter uma **estimativa intervalar** para a média populacional, com um determinado [[Nivel de Confianca|nível de confiança]]. Para quê você usa a amostra? Para ter uma previsão, um intervalo em que você acredita que a média populacional está dentro.

Algumas frases dessas que eu falo, depois vocês falam "hum, caiu uma questão conceitual". Eu falo de todas elas, só presta atenção. Eu sei que é um desafio prestar atenção durante uma hora e tanto, mas é um exercício.

Quando vocês obtêm o intervalo, é **certo** que vocês cercaram a média populacional? **Não é certo, vocês só têm 95% de confiança.** Pode não estar lá dentro.

Segunda pergunta, que eu já cobrei em prova: qual é a probabilidade do X̄ estar dentro do intervalo de confiança? **É 100%.** O intervalo é construído ao redor do X̄, e sempre está no meio por construção. Eles costumam cair nessas pegadinhas.

## Suposição que precisa valer: X̄ tem que ser normal

Tudo isso aí funciona desde que o X̄ tenha [[Distribuicao normal|distribuição normal]]. O X̄ é a coleção de médias amostrais que eu obteria se pegasse uma amostra, outra amostra, outra amostra. Isso acontece em dois casos:

1. **Quando X (a variável de interesse) já tem distribuição normal**, X̄ vai ter distribuição normal pra qualquer n.
2. **Quando X tem qualquer distribuição**, pelo [[Teorema do limite central]], se n > 30, X̄ terá formato de normal independente do formato de X.

No caso de vocês, no trabalho, vocês não têm nem ideia do formato da [[Distribuicao amostral da media|distribuição]] da população. Não dá nem pra desenhar o [[Distribuicao normal|histograma]] da população, vocês não têm acesso a ela inteira. Mas eu pedi pra vocês fazerem com n > 40, que é maior que 30. Então, garantidamente, X̄ tem distribuição normal.

Claro, vocês só levantaram uma amostra. Outros alunos com o mesmo tema poderiam estar levantando outras amostras, e elas estariam aqui dentro de algum lugar dessa distribuição.

## Os Z mágicos (decorou na aula passada, repete agora)

Alguns números mágicos:

| γ | Z_(α/2) |
|---|---------|
| 90% | 1,645 |
| 95% | 1,96 |
| 99% | 2,58 |

O 1,96 e o 1,645 vocês já decoraram. O 2,58 do 99% eu não sei de cor, devia saber. Claro que na prova às vezes coloco uma confiança de 93,5% só para o sacanagem, mas esses três são os mais usados.

## Exercício conceitual 1: verdadeiro ou falso sobre IC

Vocês pediram exercícios conceituais. A resposta já está aqui, em vermelho. **O objetivo não é achar a resposta, é entender o porquê.**

A fórmula do IC é curtinha: `IC_γ% = X̄ ± Z_(α/2) · σ / √n`. A parte do ± é a margem de erro.

### Afirmação 1: "Quanto maior o desvio padrão da população, menor a margem de erro" → **ERRADO**

Pela fórmula é evidente, né? Quanto maior o desvio padrão, maior a margem de erro. Mas vou colocar uma intuição ao contrário, pra vocês entenderem.

Olha, a gente fez umas reuniões aí e aboliu o vestibular. Agora, pra entrar na GV, você tem que ter 1,67m de altura. Esse é o único quesito, não tem prova nenhuma. Alguns de vocês não entrariam, outros entrariam fácil. Conclusão: **nessa classe, todo mundo tem 1,67m**. Se eu fosse fazer uma pesquisa sobre a média da altura, daria 1,67m. Se eu recolhesse uma amostra de algumas pessoas, daria 1,67m.

O σ da população é praticamente zero. **Que margem de erro eu preciso para prever μ?** X̄ ± zero. Quanto menor o sigma, menor a margem de erro necessária.

O problema é: quanto mais dispersa a população, pra conseguir a mesma precisão eu preciso aumentar a amostra. Pesquisa em população dispersa sai mais cara. Por isso a primeira é errada.

### Afirmação 2: "Quanto maior o nível de confiança, maior a margem de erro" → **CERTO**

Se a confiança aumenta, o Z_(α/2) aumenta, e portanto E aumenta. Uma é consequência da outra.

Exemplo intuitivo. O Arthur tem essa cara de bom moço, mas ele porta uma arma dentro do bolso. Imagina que o Arthur chegou pra mim, apontou a arma na minha cabeça e falou "Prof, se você não acertar a altura do próximo aluno que entrar atrasado, eu te dou um tiro". **Não posso errar.** Tenho que ter confiança 99,9%. O que eu faço? Eu falo: "Arthur, o próximo cara que vai entrar aqui tem 1,70m **mais ou menos 17km**". Tem como errar?

**Quanto maior a confiança, maior a margem de erro.** Se eu quero acertar com certeza absoluta, basta colocar uma margem enorme. Não tem como errar.

### Afirmação 3: "Quando o tamanho da amostra é menor que 30, o intervalo não é válido" → **ERRADO**

Para o intervalo ser válido, X̄ tem que ser normal. Mas existe um caso em que **não precisa de n > 30**: se a população **já tiver distribuição normal**, pode ter n = 8 sem problema nenhum. O n > 30 é a condição do TLC, mas se X já é normal, X̄ é normal pra qualquer n.

### Afirmação 4: "Ao quadruplicar o tamanho da amostra, a margem de erro cai pela metade" → **CERTO**

Se eu multiplico n por 4, o denominador (√n) é multiplicado por 2, então E cai pela metade. Foi o que a gente viu na aula passada: para diminuir a margem de erro pela metade, tem que quadruplicar o tamanho da amostra.

Eu gosto desse exercício porque vocês não ficam conceitualmente presos na fórmula. Vocês entendem o que está acontecendo.

## Entrando na aula de hoje: e quando σ não é conhecido?

Agora vamos começar a aula de hoje. **O que acontece quando o desvio padrão da população, o sigma, não é conhecido?** Isso é 100% das pesquisas. Vocês não conhecem o σ da população, vocês conhecem o S da amostra. Vocês calcularam X̄, o S da amostra, recalcularam a mediana (que não interessa).

### Exemplo: paulistanos e tempo de deslocamento

> Uma amostra aleatória de 180 paulistanos foi entrevistada para estimar o tempo médio que as pessoas demoram para chegar ao trabalho. A média amostral foi **67 minutos**, com desvio padrão de **17 minutos**.

Pessoal, nós estamos falando da amostra, então isso não é σ, é **S**. É o desvio padrão da amostra, que vocês calcularam.

Deu uma estimativa do tempo médio que os paulistanos demoram pra chegar ao trabalho, com 95% de confiança.

**Suposições:**

Pelo Teorema do Limite Central, a média amostral tem distribuição normal: n = 180, então qualquer que seja o formato de X, X̄ será normal.

Tem outra suposição que precisa admitir: **é uma [[Amostragem aleatoria simples|amostragem aleatória simples]]**. Não pode depender dos amiguinhos. Senão não representa: se eu pegar só as pessoas que chegam rápido, ou só os meus amigos que moram perto do trabalho, não vai dar certo. Tem que sortear da população inteira dos paulistanos de alguma forma.

**Resolução (a sacanagem):**

Como a amostra é grande, de fato 180 é grande (ninguém aqui fez com 180, né?), **vamos assumir que o desvio padrão populacional σ é também 17 minutos**. Em vez de colocar σ, eu ponho o desvio padrão amostral S.

```
IC_95% = 67 ± 1,96 · 17 / √180
```

Vocês vão falar: "pô, uma hora inteira pra dizer que quando você não tem o sigma, você põe o S e pronto". **Não é bem assim.** Eu só posso fazer isso porque a amostra é grande. Quando ela é grande, o S é uma boa estimativa do σ.

Mas o que é "amostra grande"? Depende do livro: tem livro que fala n > 50, tem livro que fala n > 100. **O nosso livro fala 50, então a gente adota 50.** Se n > 50, em vez de σ você põe S e acabou.

**E se o tamanho da amostra não for maior que 50?** É o que a gente vai fazer agora.

## A solução pra amostras pequenas: distribuição T de Student

A fórmula da margem de erro é Z_(α/2) · σ/√n. Se n > 50, eu troco σ por S e fica:

```
E = Z_(α/2) · S / √n      (se n > 50)
```

Mas se n ≤ 50, isso pode dar errado. A gente precisa "cozinhar" a fórmula: além de trocar σ por S, **em vez de Z, coloca um tal de T**. Esse T é uma outra distribuição, **um pouco maior que o Z, que compensa a coisa errada de ter trocado σ por S**.

```
E = T_(α/2, n-1) · S / √n      (qualquer n)
```

Esse T é a [[Distribuicao T de Student|distribuição T de Student]]. Tem uma história bonitinha por trás: o cara que descobriu era estudante (William Gosset, mas era o pseudônimo "Student" que ele usou pra publicar porque trabalhava numa cervejaria que não deixava publicar com nome próprio). Dá uma pesquisada depois.

A distribuição T tem cara parecida com a normal, mas **um pouco mais larga**. Ela dá uma ajustada na margem de erro pra suprir o fato de você ter trocado σ por S.

### O T depende do tamanho da amostra (diferente do Z)

Pra calcular o T eu preciso saber **a confiança E o tamanho da amostra**. O Z só dependia da confiança.

Aliás, para amostras grandes (n > 50), o T dá igual ou muito parecido com o Z. Por isso no exemplo dos paulistanos, com n = 180, eu simplesmente troquei σ por S e deixei o Z, porque pra esse n o Z é muito próximo do T.

Pra n pequeno, o T é bem maior que o Z. Por exemplo, com confiança 95%:

| n | T | Z |
|---|---|---|
| 8 | bem maior | 1,96 |
| 36 | 2,03 | 1,96 |
| 120 | ~1,98 | 1,96 |
| 36.000 | 1,96 | 1,96 |

Para n acima de 50, com poucos milímetros acima de 100, ele já é muito próximo de Z.

### Como calcular T no Excel

```
T_(α/2, n-1) = INV.T(1 − α/2; n − 1)
```

Pelo amor de Deus, **não esqueçam de botar o pontinho**. `INV.T` (com ponto) é uma coisa, `INVT` sem ponto é outra coisa no Excel.

O começo é igual ao Z: coloca 1 − α/2. A diferença é o segundo parâmetro, que são os **[[Graus de liberdade]]**. Por enquanto, saiba que **graus de liberdade = n − 1**. A gente vai aprender isso direito em Estatística 2.

Exemplo: confiança 95%, n = 36.

```
INV.T(1 − 0,025; 36 − 1) = INV.T(0,975; 35) ≈ 2,03
```

Compara com o Z de 95% que é 1,96. O T deu um pouquinho maior.

Agora, só pela brincadeira, n = 36.000:

```
INV.T(0,975; 35.999) ≈ 1,96
```

**Pra amostra grande, T = Z.** Em outras palavras, **se n > 50, deixo vocês usarem o Z** porque dá bem próximo. Abaixo de 50, é obrigado a usar T.

## Exercício conceitual 2: T ou Z?

> Considere um problema em que o desvio padrão populacional não é conhecido (que é quase todo problema de pesquisa). Vou fazer um IC. Devo usar T ou Z?

A resposta certa é a alternativa A: **usar T qualquer que seja o tamanho da amostra**.

Pessoal, **quando aqui você põe o S, ali você tem que botar T**. Eu profissionalmente, **só uso T**. Tanto faz se a amostra é pequena ou grande, **porque T é o certo**. Eu nunca tenho o σ, só tenho o S.

Se você quer, pode usar o Z se a amostra for maior que 50, vou considerar certo na prova. Se a amostra for 49, vou considerar errado. Justo? Ou usa o T sempre, aí não tem problema. Mas o certo é T.

Vamos ver por que as outras estão erradas:

- **B) Usar T ou Z é indiferente, porque as duas distribuições são similares**: errado. São similares pra amostras grandes, mas pra n < 50 o T é bem maior que o Z. Se fossem sinônimos, eu não ia ensinar duas.
- **C) Usar Z qualquer que seja o tamanho da amostra**: errado. Só posso usar Z se o n for grande (acima de 50).
- **D) Usar Z apenas se n for pequeno**: é exatamente o contrário. Permito Z se n for grande.
- **E) Usar T apenas se n for grande**: errado. Aliás, pra n grande, eu posso usar Z. Ou T sempre. T sempre é o mais correto.

> **Dúvida do aluno**: se for exatamente n = 50, pode usar Z ou T?
>
> Esse 50 não é número mágico, o livro fala 50 e o livro fala 100. Se a tua amostra é exatamente 50, usa o que você quiser. **Mas o T é sempre mais preciso.** Se ela é 49, ainda dá pra usar Z na prática, mas formalmente é T.

## Exercício 3: tempo na loja (n pequeno + população normal)

> O gerente de uma loja monitora o tempo em que os clientes permanecem na loja, e esse tempo segue uma distribuição normal. O lojista quer medir o tempo, e quanto mais tempo, melhor (o cliente compra mais).
>
> Coletou o tempo de **25 clientes** aleatoriamente. Média **18 minutos**, desvio padrão **6 minutos**.
>
> Construa uma estimativa intervalar com 95% de confiança para o tempo médio de todos os clientes da loja (passado, presente e futuro).

(Marketing de loja é um truque pra fazer o cliente ficar mais tempo. Livraria tem café, atmosfera. Giovanna Baby, antigamente, criava ambiente todo cor-de-rosa pra ativar instinto maternal. Loja de roupa pra adolescente bota música insuportável que adulto odeia, mas o público-alvo curte.)

**Resolução:**

```
γ = 95%, α = 5%, α/2 = 2,5%
n = 25, então graus de liberdade = 24

T_(2,5%; 24) = INV.T(1 − 0,025; 24)
             = INV.T(0,975; 24)
             ≈ 2,064
```

Importante: aqui eu sou **obrigado a usar T** porque n = 25 < 50.

Mas atenção: o n = 25 é menor que 30. O TLC normalmente exigia n > 30. **Por que ainda funciona?** Porque o enunciado diz que **a população segue distribuição normal**. Como X já é normal, X̄ é normal pra qualquer n. Graças a Deus o enunciado falou isso.

```
E = T · S / √n
  = 2,064 · 6 / √25
  = 2,064 · 6 / 5
  = 2,064 · 1,2
  ≈ 2,48
```

```
IC_95% = 18 ± 2,48
       = [15,52 ; 20,48] minutos
```

**Resposta:** o intervalo de 15 e tanto a 20 e tanto minutos contém o tempo médio de todos os clientes da loja com 95% de confiança.

## Próxima aula

Acabou o assunto **intervalo de confiança para média**. Próxima aula (quarta-feira) a gente estuda **[[Intervalo de Confiança|intervalo de confiança para proporção]]** (caso de pesquisa eleitoral). Tem exercício, e às vezes eu não dou a média da amostra, dou os dados, então em 10 minutos vocês vão calcular tudo.

## Resumo das regras de quando usar Z ou T

| Situação | σ conhecido? | n | Use |
|---|---|---|---|
| σ conhecido | sim | qualquer | **Z** |
| σ desconhecido, amostra grande | não | n > 50 | **Z** (aproximação) **ou T** (correto) |
| σ desconhecido, amostra pequena | não | n ≤ 50 | **T obrigatório** |
| σ desconhecido, n < 30, mas X é normal | não | qualquer | **T** (porque X̄ é normal pela suposição) |

Regra do Nelson: **se você puser S, ponha T.** O resto é simplificação.
