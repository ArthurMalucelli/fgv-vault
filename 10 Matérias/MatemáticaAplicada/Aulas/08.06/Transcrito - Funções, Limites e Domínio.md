---
materias: [matematica-aplicada]
semestre: 2026.2
data: 2026-08-06
tipo: transcrito
tema: Funções, Limites e Domínio
status: completo
contract_version: 1
professor: Larissa Marques Sartori
topicos: [funcao potencial, dominio, funcao composta, limite, forma indeterminada, racionalizacao por conjugado]
tags: [aula, transcrito]
---

> [!warning] Áudio com falha de captação
> O Plaud perdeu a maior parte da fala dessa aula (blocos longos sem captura, não é o ruído normal). Abaixo está só o que é recuperável, com reescrita leve. Palavras entre [colchetes] são reconstrução minha, cruzando o transcript com o slide 2 (na pasta Slides) e com a tua anotação manual [[Limites - Introdução]]. Lacunas grandes estão marcadas em itálico com o timestamp aproximado, caso queira reouvir o trecho na nuvem do Plaud.

## Organização do curso

No e-mail vocês têm uma pasta, a pasta de slides das aulas. Eu já coloquei tudo ali, tá? Todas as aulas que a gente vai ver. Essas coisinhas aqui parecem muito simples quando a gente faz, mas quando a gente coloca a função, muda.

A gente tem exercício ao longo das aulas, e [perto das provas] tem umas duas semanas que é só exercício de provas passadas. Aqui é onde eu vou colocar a minha pasta, uma pasta de exercícios de matemática.

Depois a gente vai ter atividade 2, atividade 3, atividade 4 e atividade 5. A gente vai ter uma série de avaliações.

*Lacuna (00:13 a 00:19): pesos e datas das avaliações não foram capturados. As três Atividades Monitoradas (A, B e C) já estão salvas na pasta Atividades da matéria.*

## Funções de uma variável

Bom, a gente vai aprender como resolver essas situações em cima de funções, funções de uma variável. O conteúdo do curso: a gente vai ver as funções lineares, quadráticas, [potenciais, exponenciais].

Na [[Função Potencial|função potencial]] a gente tem o expoente fixo [e a base variando]. Quando [inverte], a gente tem uma base [fixa] e o expoente [variando]: a [[Função Exponencial|função exponencial]]. A gente tem que saber a diferença dessas duas, porque a regra que eu uso [numa] é totalmente diferente da regra [da outra]. Não [dá pra] aplicar a regra [de uma] na outra.

*Lacuna (00:24 a 00:28): a passagem pelos cinco casos de função potencial (n par positivo, ímpar positivo, par negativo, ímpar negativo, racional) não foi capturada. Os cinco casos com domínio estão na tua anotação [[Limites - Introdução]] e na tabela do [[Resumo - Funções, Limites e Domínio]].*

## Domínio

Qual que é o [[Domínio de Função|domínio]] dessas funções aqui? Posso falar? Não tem dúvida, tá certo? Positivo? Óbvio.

[No caso da raiz, os radicandos] são reais maiores ou iguais a zero.

## Função composta

O que a gente precisa lembrar também: quando a gente tiver uma [[Função Composta|função composta]]... Perceba, toda vez que for uma função composta, vai vir uma informação colocada aqui. Vou colocar uma função composta agora, que é uma raiz. Agora a gente vai ter raiz de x, e é assim que a gente vai resolver.

O que vale é a regra da f: a f é uma função raiz, e no lugar do x [entra a outra função]. E agora analisamos o que tem dentro da raiz.

E aí, gente, é uma composta. A gente tem dúvida? Não tem dúvida.

*Lacuna (00:47 a 00:53): trecho perdido (chamada e conversa de fundo dominam o áudio).*

## Limites: a ideia

O que acontece com os valores de [f(x)], com a imagem, quando a gente faz os valores de [x] variar próximo do número?

*Nota: aqui entra a construção da tabela de aproximação do slide: f(x) = x² com x perto de 2 pelos dois lados (1,9; 1,99; 1,999... e 2,1; 2,01; 2,001...), f(x) fechando em 4. No áudio sobrou só a pergunta de um colega, "a gente vai precisar fazer essa tabela?", sem a resposta capturada. O slide seguinte responde a intenção: "como calcular sem fazer a tabela de valores?"*

E quando a gente pode substituir o nosso valor, nós podemos substituir. [Se a substituição dá um número, o limite] é substituir.

## Forma indeterminada e conjugado

*Nota: o exemplo em jogo aqui é o exercício do slide, reconstruído abaixo. Se calcular direto em x = 0, a raiz dá √16 = 4, e sobra 0/0: [[Forma indeterminada|forma indeterminada]].*

[Pra deixar a expressão] mais fácil de ser utilizada, a gente vai multiplicar ela por 1: uma [fração] criada [com] esse termo que tem a raiz, só que com [o] sinal [trocado]. É a [[Racionalização por conjugado|racionalização por conjugado]].

A raiz vezes [a raiz dá o radicando]: [fica o radicando] menos o [4 ao] quadrado.

Olha só que maravilhoso.

```
lim(x→0) (√(x²+16) − 4)/x²          substituindo: (√16 − 4)/0 = 0/0

multiplica por (√(x²+16) + 4)/(√(x²+16) + 4):

= (x² + 16 − 16) / (x² · (√(x²+16) + 4))
= x² / (x² · (√(x²+16) + 4))
= 1 / (√(x²+16) + 4)   →   1/(4+4) = 1/8
```

*Nota: o outro exemplo da aula, lim(x→1) (x−1)/(x²−1), foi resolvido por fatoração: (x−1)/[(x+1)(x−1)] = 1/(x+1) → 1/2. O slide mostra o cálculo pelos dois lados (x→1⁻ e x→1⁺), os dois dando 1/2: o [[Limite (cálculo)|limite]] existe porque os laterais coincidem. A frase que um colega leu do quadro ("o limite de f de x é igual ao limite da f de x") era exatamente isso.*

*Fim do áudio recuperável (01:18). Propriedades operatórias de limites (soma, produto, quociente, potência, raiz, ln) estão nos slides 6 e 7 e condensadas no [[Resumo - Funções, Limites e Domínio]].*
