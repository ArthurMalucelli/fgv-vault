---
materia: Programacao
data: 2026-06-12
tema: Correção prova final FunProg 2026-01 (versão PAR)
tags: [correcao, prova]
---

# Correção: Prova Final FunProg 2026-01

Nota estimada: **7,0 a 7,5 / 10** (piso 6,0 se o corretor testar cenários fora do exemplo, teto 8,25 se for leniente).

Todos os bugs abaixo foram verificados executando o código, não só lendo.

| Questão | Vale | Estimativa | O que perdeu |
|---|---|---|---|
| Q1 câmbio | 2,0 | 1,5 a 2,0 | Moeda Real não tratada (soma silenciosamente errada) |
| Q2 jogo | 2,0 | 2,0 | Nada |
| Q3 multa | 2,0 | 1,0 | Crash em tipo inválido + formato de saída errado |
| Q4 filmes | 2,0 | 1,0 | Item b ausente + validação não repete até válida |
| Q5 transações | 2,0 | 1,5 | Sem input(), string hardcoded |

## Q1 (rubrica: 1,0 câmbio em todas as linhas + 1,0 soma correta)

O resultado pro dataset dado está certo: R$51.223,97 (verifiquei a soma manualmente e por código).

O que quebra: o enunciado manda verificar Real, Dólar ou Euro, e o cabeçalho da prova exige que o código sirva pra qualquer cenário. O código só seta `Cambio` pra Euro e Dolar. Com uma linha em Real, `Cambio` vira NaN, `Preço BRL` vira NaN, e o `.sum()` do pandas pula NaN: a venda em Real **some da soma sem dar erro**. Testado: df com venda de R$100 em Real retorna total 100 reais menor, silenciosamente. Bug silencioso é pior que crash. Bastava `vendas.loc[vendas["Moeda"]=="Real", "Cambio"] = 1`.

Se o corretor rodar só a célula dada: 2,0. Se testar com Real: perde a rubrica de 1,0 do câmbio.

## Q2 (rubrica: 1,0 estrutura com parada + 0,5 pontos + 0,5 resultado)

Limpa. Loop while com parada ao acertar (via `chances = 0`), pontuação 50/20/5 por tentativa e -15 no erro, resultado impresso certo. A condição final `chute != numero` resolve corretamente o win/loss. **2,0.**

Nitpicks não pontuados: a mensagem "este e mais {chances}" tem off-by-one (na primeira tentativa diz "este e mais 3", mas são 3 no total). `pontos = pontos` é código morto.

## Q3 (rubrica: 0,5 coleta+validação + 1,0 cálculo + 0,5 formato, sem parcial dentro de rubrica)

Três quebras, por severidade:

1. **Tipo inválido imprime ENTRADA INVÁLIDA mas não encerra.** O `if tipo_contrato == "MENSAL"` está fora do else, então depois de imprimir a mensagem o fluxo continua, cai em `multa = multa / 2` e estoura `UnboundLocalError` (multa nunca foi definida). Testado com tipo "mensal": mensagem + traceback. O enunciado pede explicitamente "imprima ENTRADA INVÁLIDA **e encerre**". Rubrica de validação (0,5) perdida, e a regra diz sem parcial.
2. **Formato de saída errado nas três exigências.** Pedido: `Multa R$ X,XX` (vírgula decimal, duas casas, espaço após R$). Saiu: `Multa R$25.0` (ponto, uma casa, sem espaço). O caminho era `f"{multa:.2f}".replace(".", ",")`. Rubrica de 0,5 perdida quase certo.
3. **`int(input())` na fatura.** Fatura 1500.50 estoura ValueError. O enunciado diz que o usuário sempre digita número válido, e número válido inclui decimal (fatura tem centavos). Deveria ser `float()`. Reforça o risco na rubrica de coleta.

O cálculo em si está certo: faixas 0/2%/5%/10% com os limites corretos (10, 30) e ajuste ANUAL pela metade. Rubrica de 1,0 garantida no caminho feliz.

Estimativa: **1,0** (1,5 se o corretor ignorar o crash porque a mensagem foi impressa).

## Q4 (rubrica: 0,5 coleta + 0,5 validação em loop + 0,5 média + 0,5 itens b e c)

Três quebras, por severidade:

1. **Item b não existe.** O enunciado pede o(s) nome(s) do(s) filme(s) com a maior nota. O código nunca calcula max nem imprime nome de filme. A rubrica de 0,5 cobre b e c juntos; só c foi feito.
2. **Validação não repete "até" ser válida.** A rubrica diz "solicita novamente **enquanto** inválida": isso é while, não if. O código pede de novo exatamente uma vez e aceita o que vier. Testado: nota 10 seguida de 12, o 12 é aceito, média vira 7.5 e a contagem >=4 conta o 12. Rubrica de 0,5 perdida.
3. **Bug latente: nome do filme some no caminho inválido.** O `filmes.append(nome_filme)` está só no else, então filme que teve nota inválida na primeira tentativa nunca entra na lista de nomes. Não afeta o output atual porque o item b não foi tentado, mas teria matado o item b de qualquer jeito. No teste: 2 filmes avaliados, lista de nomes com 1.

Média correta com entradas válidas (uma nota appendada por filme nos dois caminhos, divisão por num_filmes). Contagem >=4 correta.

Estimativa: **1,0** (1,25 se der parcial pro item c dentro da rubrica 4).

## Q5 (rubrica: 1,0 separação + 0,5 soma em loop + 0,5 apresentação)

Uma quebra: o enunciado pede que o programa **receba as transações por input na tela**. A string de exemplo está hardcoded dentro de uma lista, sem `input()` em lugar nenhum. Detalhe que piora: se alguém só trocar por `banco = input()`, o `for i in banco` passa a iterar caractere por caractere e tudo quebra; a estrutura só funciona por causa da lista artificial de um elemento. O certo era `banco = input()` direto e `banco.split("#")` sem loop externo.

O resto está certo: split por # e por ;, conversão float, soma em loop, round, e o formato `Total: R$-234.4` bate exatamente com o exemplo.

Estimativa: **1,5** (-0,5 pelo input; -1,0 se o corretor enquadrar como "não recebe os dados").

## O que está bom

- Q2 inteira: estrutura de loop com parada, a parte mais armadilhada da prova.
- Lógica de negócio acerta em todas as questões no caminho feliz: faixas da multa, ajuste ANUAL, câmbio, parsing, somas.
- pandas idiomático na Q1 (`.loc` com máscara booleana, coluna vetorizada em vez de loop).
- Formato da Q5 bate com o exemplo, incluindo o caso negativo.

## Padrão pra levar

Os pontos perdidos têm uma única causa raiz: **o código foi testado só no caminho feliz do exemplo**. As quatro perdas (Real na Q1, tipo inválido na Q3, formato na Q3, dupla inválida na Q4, input na Q5) são todas de cenário fora do exemplo ou de releitura do enunciado. Antes de entregar: reler o enunciado frase por frase como checklist, e rodar uma vez com entrada inválida.
