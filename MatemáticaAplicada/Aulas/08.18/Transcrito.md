---
materia: MatemáticaAplicada
data: 2026-08-18
tema: Limite fundamental, continuidade e assíntotas
topicos: [forma indeterminada 1 elevado a infinito, limite no infinito, continuidade, assíntota horizontal, assíntota vertical]
tags: [aula, transcrito]
---

> Nota da transcrição: áudio muito degradado (transcrição do Plaud corrompeu grande parte das falas da professora, e há conversa constante de alunos jogando no fundo). Abaixo está o que é recuperável com confiança; os slides desta aula estão na pasta `Slides/` e completam o que o áudio perdeu.

## A [[Forma indeterminada|forma indeterminada]] 1 elevado a infinito

Sabendo o limite fundamental, a gente consegue resolver outros limites que têm esse formato. A discussão central: se a base fosse exatamente 1, elevado a qualquer coisa daria 1. Mas a base não é exatamente 1, ela tende a 1: é 1 mais uma coisa que tende a zero. Então, elevando ao infinito, não dá para afirmar nada de cara: é indeterminado. Não é "1 elevado a infinito igual a 1"; é uma indeterminação que se resolve pelo limite fundamental exponencial.

## [[Limite no Infinito|Limite no infinito]] com aplicação

Exemplo aplicado: uma quantidade de computadores em função de x, onde x é o tempo. Quando a pergunta é "no longo prazo" ou "para um tempo muito grande", a gente quer calcular o limite com x tendendo ao infinito. No cálculo, os termos de menor grau vão sumindo (corta com o infinito) e sobra o comportamento dominante: no exemplo, o resultado tende a 50. Interpretação: no longo prazo a quantidade se aproxima de 50, fica em 49, 49,9, cada vez mais perto de 50, sem nunca precisar cravar exatamente 50. Esse valor define a assíntota horizontal da função.

## [[Continuidade]]

O modo mais simples de pensar: a função é contínua quando a gente consegue fazer o gráfico dela sem tirar o lápis do papel.

Formalmente, para ser contínua num ponto, teria que existir o valor da função no ponto (por exemplo, f(2)), e o limite tendendo ao ponto teria que ser igual a esse valor. No exemplo do quadro: a função tem uma restrição no domínio, fatora (as raízes são 2 e −1), o termo dividido por ele mesmo dá 1, e sobra o limite de x + 1, que dá 3. Só que no ponto 2 a função não está definida (a bolinha fica aberta): o limite existe e vale 3, mas f(2) não acompanha. Como eu teria que definir f(2) para tornar a função contínua? f(2) teria que valer 3. Sem isso, ela fica descontínua no ponto.

## [[Assíntota Vertical|Assíntotas verticais]] e [[Assíntota Horizontal|horizontais]]

Assíntota vertical: só faz sentido procurar onde há restrição no domínio. Se o ponto pertence ao domínio, já pode afirmar que não tem assíntota vertical ali, nem precisa calcular. Onde há restrição, a gente calcula o limite tendendo ao ponto (são dois limites, os laterais, para uma mesma candidata a assíntota): se o resultado dá mais ou menos infinito, tem assíntota vertical; se dá um número, não tem. E pode existir mais de uma assíntota vertical se houver mais de uma restrição no domínio.

Assíntota horizontal: é a reta y = L dada pelo limite no infinito, como no exemplo dos computadores (y = 50). O gráfico vai se encostando na reta sem tocá-la.

## Fechamento

A última parte, sobre derivadas, fica para a sequência: tem videoaula cobrindo a parte de derivada, e a gente continua de lá.
