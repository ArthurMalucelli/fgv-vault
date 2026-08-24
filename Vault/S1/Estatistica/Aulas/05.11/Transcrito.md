---
materia: Estatistica
data: 2026-05-11
professor: Nelson
tema: Teorema do Limite Central e distribuição da média amostral
topicos: [Teorema do limite central, Distribuicao amostral da media, Erro padrao, Distribuicao exponencial, Simulacao]
tags: [aula, transcrito]
---

# Teorema do Limite Central e distribuição da média amostral

## Recap da última aula

No último episódio, eu chamei aqui na frente triplas de pessoas sorteadas. Pedi pra cada grupinho anotar a média de altura das três. Depois trabalhamos com a coluna desses X̄ e tentamos ver quanto era a esperança do X̄, quanto era a variância dessa coluna. Não tem nada a ver com a variância e o desvio padrão interno da amostra.

Se a altura de vocês seguir uma normal, com média μ (não sei se segue, mas vou supor) e desvio padrão σ, então a esperança de X̄ é igual a μ, a variância de X̄ é a variância original dividida pelo tamanho de cada amostra (no caso, 3), e o desvio padrão é σ sobre raiz de n. Isso foi o que vimos na aula anterior.

Vimos também o problema da bolacha cream cracker. Admitimos que a quantidade de gordura trans seguiria uma normal, com média 0,2 gramas e desvio padrão 0,05. Num certo dia, pegamos uma amostra de n igual a 100 bolachas e deu 0,24. Isso é natural ou não?

```
X ~ Normal(0.20, 0.05²)
n = 100
X̄ ~ Normal(0.20, 0.05/√100) = Normal(0.20, 0.005)
```

Se X segue uma normal, X̄ também segue uma normal, com a mesma média 0,20 e desvio padrão do X̄ igual a 0,05 sobre raiz de 100, que dá 0,005. A pergunta é: qual a probabilidade de X̄ ter dado 0,24?

```excel
= 1 - DIST.NORM(0.24; 0.20; 0.005; 1)
```

Isso aqui dá aproximadamente zero, um monte de casas depois da vírgula. Principalmente porque 0,24 está a 8 desvios padrão do X̄ distante da média. É um super outlier.

Então esse fato, 0,24, é um milagre. A probabilidade é praticamente zero, mas aconteceu. Onde está o erro? Aconteceu um milagre? Não, provavelmente a média aqui não é mais 0,20. Para a máquina e vamos calibrar.

Só que eu menti pra vocês. Eu escrevi que X segue uma normal, em nenhum lugar do enunciado está escrito que a quantidade de gordura trans nas bolachas segue uma normal. Eu supus uma coisa que não era verdade.

## E quando X não é normal?

O que aprendemos na última aula foi isso aqui: a [[Distribuicao amostral da media|distribuição amostral de X̄]]. Se a distribuição da população X for normal, com média μ e variância σ², então X̄ seguirá também uma normal, com média μ e variância dividida por n. O desvio padrão do X̄ também é chamado de **[[Erro padrao|erro padrão]]**: σ sobre raiz de n.

```
Se X ~ N(μ, σ²)  ⟹  X̄ ~ N(μ, σ²/n)
```

Mas no exercício das bolachas não estava escrito que a distribuição da gordura trans segue uma normal. E agora?

## Teorema do Limite Central

Vou apresentar pra vocês o **[[Teorema do limite central]]**, que resolve um monte de problemas. Não vamos demonstrar, porque a demonstração é muito complexa. Não se assustem, nem todo teorema, nem o de geometria, vocês aprenderam tudo demonstrado. Aqui não vamos demonstrar nada. Ele existe.

Vamos ter uma população de distribuição uniforme, não é normal. Na normal, o meio tem mais frequência e as pontas são raras. Aqui é uniforme. Vamos tirar dessa população muitas amostras, infinitas amostras de tamanho 2. E vamos desenhar o histograma do X̄, colocando cada X̄ numa coluna e pedindo pro Excel fazer o histograma.

E se n for 5? Já arredonda. E se n for 30? Vai dar uma normal. Vamos mostrar isso.

Vamos pegar uma exponencial, que não é simétrica. Com n=2, se eu pegar várias amostras de tamanho 2 e tirar o histograma de X̄, vai dar um formato esquisito. Com n=5, melhora. Com n=30, já vira simétrica.

**Conclusão**: conforme o tamanho da amostra aumenta, a distribuição amostral da média se aproxima de uma normal. Para n muito grande, vai ser sempre normal. E os livros falam que **acima de 30 já se considera normal**.

Por que 30? Eu fazia Kung Fu três anos e meio, tinha um exercício de respiração no final que tinha que fazer 49 vezes. Perguntaram pro mestre: por que 49 e não 48? Porque é 49. A resposta é assim. Por que 30? Porque 30 é considerado um número suficiente para que, qualquer que seja a distribuição da população, a distribuição de X̄ já pareça normal.

Então a regra: **n > 30 é amostra grande**. Quando é grande, qualquer distribuição de X̄ vai ser normal, independente da distribuição da população. Isso quebra um galhão da gente, porque a gente nunca sabe qual é o formato da distribuição da população. No trabalho de vocês, a população é normal? Sei lá, se não tem acesso à população, muito bem.

## Demonstração visual (site da simulação)

Pra demonstrar de forma prática, tem um site que é mais velho do que eu. Tem uma população normal, "população clara". Tiro uma amostra de tamanho 5, sorteio. Aqui está o X̄. Outra amostra de tamanho 5, outro X̄. No fundo eu quero ver qual é a distribuição do X̄. Então vamos tirar 100 mil amostras de tamanho 5. Resultado: normal.

Agora a dúvida é quando a população não é normal. Vamos transformar isso em não-normal. Boto uma torre aqui, um buraco no meio. Isso é o histograma da landscape de uma fábrica, com chaminé. Tiro 100 mil amostras de tamanho 5: praticamente uma normal. Cuidado, só 5, nem chegou em 30.

> Pergunta (aluno): mas ele não explica a fórmula. Resposta: é só você pensar, você está fazendo a média das médias. É tipo o z-score do z-score.

A intuição é essa: mesmo com a população completamente esquisita, o histograma de X̄ vai se parecendo cada vez mais com uma normal conforme n cresce. Se chegou em 30, já é normal.

## Exercício: ligações telefônicas (exponencial)

Tempo de ligações de telefones internacionais tem [[Distribuicao exponencial|distribuição exponencial]] com média de 5 minutos.

**Dica**: em distribuição exponencial, o desvio padrão é igual à média. Então σ também é 5 minutos.

### Pergunta 1: qual a probabilidade de uma chamada demorar mais de 6 minutos?

Não é normal, então **não pode usar DIST.NORM**. É uma distribuição exponencial: sai do pontinho e nunca encosta no eixo, mas não é simétrica.

Quando é à direita da fronteira, a fórmula é:

```
P(X > a) = e^(-a/μ)
```

No Excel, sendo e o número de Euler (≈ 2,718):

```excel
= EXP(-6/5)
```

Isso dá aproximadamente **0,3012 → 30,12%**.

> Atenção: na exponencial à direita é `e^(-a/μ)` direto. À esquerda seria `1 - e^(-a/μ)`. É o contrário da DIST.NORM, onde a direita vira `1 - DIST.NORM(...)`.

### Pergunta 2: qual a probabilidade de **X̄** ser maior que 6, com n=100?

Não é a mesma pergunta. Agora está tirando uma amostra de tamanho 100 e quer a probabilidade de a média dessa amostra ser maior que 6.

Pelo Teorema do Limite Central, mesmo X sendo exponencial, como n=100 (> 30), X̄ segue normal:

```
X̄ ~ Normal(μ = 5, σ/√n = 5/√100 = 0.5)
```

```excel
= 1 - DIST.NORM(6; 5; 0.5; 1)
```

Dá um número pequeno (muito menor que 30,12%). A média de 100 chamadas dificilmente passa de 6 minutos, mesmo que cada chamada individual tenha 30% de chance de passar. É o efeito da concentração da média conforme n cresce.

**Quadro-resumo das vantagens do TLC**:

A gente nunca sabe a distribuição da população. Mas se quero saber a probabilidade de X̄ ser alguma coisa, desde que a amostra seja grandinha, **não precisa saber a distribuição da população**. Pelo TLC, X̄ é normal.

```
Se X ~ N(μ, σ²)            ⟹  X̄ ~ N(μ, σ²/n)     (sempre, qualquer n)
Se X não-normal e n ≥ 30   ⟹  X̄ ~ aprox. N(μ, σ²/n)  (TLC)
Se X não-normal e n < 30   ⟹  não dá pra concluir
```

Por isso a gente sempre trabalha com amostra acima de 30.

## Desafio: o elevador

Antigamente a gente usava o elevador da Nove de Julho, quando esse prédio não existia. Muita gente ainda usa aquele elevador. Já aconteceu de muita gente entrar e o elevador fazer "péh" e não andar? Acontece. Se entra muita gente, fica muito pesado.

A capacidade máxima do elevador é meia tonelada (500 kg). Se a distribuição dos pesos da população X for normal, com média 70 kg e desvio padrão 10 kg (atenção: agora não é altura, é peso), qual a probabilidade de, ao entrar **sete passageiros**, o elevador fazer péh?

```
X ~ Normal(70, 10²)
n = 7
Quero: P(ΣXᵢ > 500)
```

Tem dois jeitos de fazer. Um, você não consegue fazer. O outro, usando o que a gente aprendeu nas últimas aulas, dá.

### O truque (soma vira média)

A gente não sabe calcular probabilidade da **soma** de variáveis tiradas de uma distribuição. A gente sabe da **média**.

Pergunta: se eu sortear um de vocês, qual a probabilidade da altura ser maior que 1,80 m? Vocês chutaram 17%.

Agora: qual a probabilidade da **metade da altura** dessa pessoa ser maior do que metade de 1,80? É a mesma. Quando falo `P(algo > x)`, se eu dividir os dois lados por uma constante, a probabilidade não muda.

```
P(ΣXᵢ > 500)  =  P(ΣXᵢ/7 > 500/7)  =  P(X̄ > 500/7)
```

Dividir a soma por 7 é a média. Agora estou em casa, porque sei trabalhar com X̄.

### Resolvendo

```
X̄ ~ Normal(μ = 70, σ/√n = 10/√7)
P(X̄ > 500/7) = P(X̄ > 71.43...)
```

No Excel:

```excel
= 1 - DIST.NORM(500/7; 70; 10/RAIZ(7); 1)
```

Dá **35,27%**. A probabilidade do elevador parar com 7 passageiros é praticamente um terço.

### Pegadinha

Quem multiplicou um peso por 7 (tipo: "se cada um pesa 70, sete pesam 490, então P(X > 500) com X ~ N(490, ...)") fez errado. Não dá pra admitir que as sete pessoas têm o mesmo peso. Elas saíram da distribuição, então cada uma tem um peso diferente. Quem fez assim, dá errado.

## Homenagem ao Bussab e o "desalgoritmizado"

Pessoal, prestem atenção que essa parte eu faço questão de falar. O livro **Estatística Básica** do Bussab e Morettin é excelente, com exercícios maravilhosos. O Bussab era professor da USP, fez matemática lá no IME na época em que não existia estatística, depois doutorado em estatística na Inglaterra, e voltou pra cá. Foi quem praticamente criou o setor de estatística aqui. Todos nós somos discípulos dele.

Tem uma frase dele que vale guardar: **pior do que ser analfabeto é ser desalgoritmizado**. A pessoa sabe escrever, mas não tem a mínima noção de qualquer coisa de número. Dá 10, vai dar troco de 5, e precisa calcular tudo no caixa pra saber qual é o número.

## Simulação

Agora vou mostrar simulação. Simulação é uma técnica que, se eu fosse vocês, eu começaria a usar pra tudo. Profissionalmente é um diferencial: se você não sabe resolver por matemática, simulação resolve.

Exemplo: altura de uma população. Normalmente eu conheço a população? Não. Mas Deus conhece. Então aqui eu estou brincando de Deus e, supondo conhecida, fixei a altura de uma população indígena de 1000 pessoas. Calculo a média (169,7 cm), desvio padrão, variância. Isso é o **real** da população, em azul.

Eu, porém, só consigo amostrar. No trabalho de vocês, vocês pegaram amostras de 40, 100, etc. Eu vou pegar uma amostra de tamanho 4 (sou pobre, não tenho dinheiro pra amostra grande).

```excel
= ALEATÓRIO.ENTRE(1; 1000)   ← sorteia o índice
= PROCV(índice; população; 2)  ← pega a altura correspondente
```

Calculo X̄ dessa amostra. Calculo também a variância interna S² e o desvio padrão interno S, mas em verde, porque **não vou usar pra nada** nessa aula. Nessas aulas a gente não tem olhado quanto é a variância interna.

### Universos paralelos

Em simulação a gente brinca de mundos paralelos. Filme de ficção, Terra 2, universo 2. Tem outro Nelson, só que esse usa cabelo comprido e colete vermelho. O Nelson do mundo 2 também está sorteando, e o X̄ dele dá parecido, mas não igual.

E não tem só dois universos. Tem muitos. Muitas réplicas, que a gente chama. No meu Excel tem 600 universos paralelos. Pra cada um, um X̄ diferente.

O que a gente discutiu nas últimas aulas foi a **esperança, desvio padrão e variância dessa coluna de X̄s**, não de cada amostra individual.

Verificação empírica:

```
E(X̄) deveria ser μ            → simulação: 169,1 vs μ real 169,7. ✓
σ(X̄) deveria ser σ/√n         → σ_real ≈ 7,1, n=4, σ/√n ≈ 3,55. Simulação: ~3,4. ✓
Var(X̄) deveria ser σ²/n       → ~12. Simulação: bate.
```

F9 sorteia tudo de novo, outros universos paralelos. A esperança continua próxima de μ, o desvio padrão continua próximo de σ/√n. Não dá exato porque só tem 600 réplicas, não infinitas. Se eu esticasse pra 1 milhão (lento no Excel, melhor em Python com NumPy), daria rigorosamente igual.

### Distinção que não pode confundir

Vocês nunca mais vão confundir:

- **S = desvio padrão da amostra** (interno, 8,4 no exemplo) — mede dispersão **dentro** de uma amostra.
- **σ(X̄) = desvio padrão do X̄** (vertical, ~3,5 no exemplo) — mede dispersão **entre** os X̄s de diferentes amostras. É o erro padrão.

São coisas completamente diferentes.

### Histograma

O histograma da população: meio esquisito, lembra uma normal mas não é. O histograma do X̄ (com n=4): mais parecido com normal, mas ainda não é, porque n=4 não basta pro TLC ser aplicado.

### Por que simulação importa

Se eu não tivesse ensinado pra vocês essas duas últimas aulas, e quisessem saber como se comporta a distribuição de X̄ e qual o desvio padrão dele, por **simulação** dava pra descobrir tudo isso empiricamente. Você finge que conhece a população, sorteia muito, e observa o resultado.

Simulação é matemática experimental. Quando não sabe resolver analiticamente, simula.
