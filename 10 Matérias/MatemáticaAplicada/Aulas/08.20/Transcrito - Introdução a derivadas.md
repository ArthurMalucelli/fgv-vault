---
materias: [matematica-aplicada]
semestre: 2026.2
data: 2026-08-20
tipo: transcrito
tema: Introdução a derivadas
status: completo
contract_version: 1
topicos: [limites laterais com análise de sinal, taxa de variação média, reta secante, reta tangente, definição de derivada, derivada como função]
tags: [aula, transcrito]
---

> Nota da transcrição: áudio degradado com muita conversa paralela. Reconstruído o fio da aula a partir dos trechos legíveis; os slides desta aula estão na pasta `Slides/`.

## Aquecimento: limites laterais com análise de sinal

Olhando o ponto que não está no domínio da função: no limite com x tendendo a −7, a gente testa valores próximos. Jogando −7,1 (pela esquerda): em cima dá −2,1 e embaixo −7,1 + 7 = −0,1. Divisão de negativo com negativo: positivo, e o denominador é minúsculo, então cresce sem parar. Jogando −6,99 (pela direita): número negativo dividido por um número positivo muito pequeno, o resultado é negativo e explode para baixo. Não dá zero embaixo e pronto: é a análise de sinal que diz se o limite lateral vai para mais ou menos infinito.

E na função exponencial com expoente negativo: elevar a menos alguma coisa inverte o comportamento, porque menos vezes o número negativo fica mais. É isso que controla para onde a exponencial vai em cada lado.

## [[Taxa de Variação Média|Taxa de variação média]]

Motivação da derivada: a variação correspondente que se tem na função. Quando x varia em duas unidades e a f varia em 24, tem uma variação média de 12 unidades por unidade de x. Só que a gente não vai ficar falando "variação média entre dois pontos" a aula toda: isso tem um nome, e geometricamente é o coeficiente angular da [[Reta Tangente|reta secante]] que liga os dois pontos do gráfico.

## Da secante à tangente

A ideia da derivada: pegar os dois pontos da secante e aproximar um do outro até a reta encostar na curva num ponto só. A reta que abraça a função num ponto é a reta tangente. O coeficiente angular dela, eu vou chamar de m. A reta tangente passa pelo ponto (a, f(a)), então a equação dela é y − f(a) = m(x − a).

Analogia do radar: ele bate uma foto muito próxima da outra, calcula a variação da distância naquele intervalinho, e consegue uma velocidade. Quanto mais próximas as fotos, mais aquilo vira a velocidade instantânea. Derivada é isso: taxa de variação instantânea.

## Definição de [[Derivada|derivada]]

O coeficiente angular da tangente no ponto a é o limite da taxa de variação média quando o segundo ponto se aproxima do primeiro. A gente chama isso de f'(a), que é a derivada da f no ponto a. Também dá para escrever trocando a variável: o x vai se chamar a + h, o f(a) continua f(a), e o limite fica com h tendendo a zero:

```
f'(a) = lim(x→a) [f(x) − f(a)] / (x − a)
f'(a) = lim(h→0) [f(a+h) − f(a)] / h
```

Pergunta de aluno: muda alguma coisa se eu me aproximo pelo lado do mais ou do menos? Não: para a derivada existir, o limite é o mesmo dos dois lados. As duas formas da definição são equivalentes; treina a que preferir.

## Exemplo: f(x) = x² + 1 no ponto a = 2

A função é uma regra que pega o que está dentro, eleva ao quadrado e soma um. Então f(2) = 5, e f(2 + h) = (2 + h)² + 1. A conta:

```
f'(2) = lim(h→0) [(2+h)² + 1 − 5] / h
```

Expande o termo ao quadrado, os números se cancelam, sobra h multiplicando: coloca o h em evidência (ou separa termo a termo), corta com o h de baixo, e o que resta avalia em h = 0. É o mesmo padrão sempre: expandir, cancelar, fatorar o h, cortar, substituir.

## Derivada como função

Quando eu calculava a derivada no ponto a, o resultado era um número: o coeficiente angular da tangente naquele ponto. Agora, no lugar do a, coloco um ponto x genérico: o resultado vira uma função, f'(x), que entrega o coeficiente angular da tangente em cada ponto do gráfico. Na próxima aula entram as regras de diferenciação, para não precisar fazer o limite na mão toda vez.
