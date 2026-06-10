---
tipo: resumo
materia: Programacao
data: 2026-06-09
tema: Erros e dúvidas do treino pré-final (log pessoal)
tags: [resumo, prova, erros]
---

# Teus erros do treino, 09.06

Log do que você errou resolvendo o `SimuladoFinalCompleto`. Leitura obrigatória amanhã 14:30 junto com os bullets "o que zera ponto" do cheat sheet. Os erros daqui são os TEUS padrões, mais valiosos que qualquer lista genérica.

## Erros (com o porquê)

**1. Q2B, leitura de pandas: "imprime as 5 primeiras linhas da coluna".**
`estoque.head()` imprime as 5 primeiras linhas do **dataframe inteiro, todas as colunas**. Precisão importa em questão de leitura: cada bloco vale 0,33. Conserto: responder em 3 linhas, uma por bloco da rubrica.

**2. Q3, `int(distancia)` e `periodo.upper()` soltos, sem atribuir.**
Função/método **retorna** o valor novo, não altera a variável. `int(x)` sozinho joga o resultado fora; `x` continua `str` e estoura `TypeError` na comparação (a MESMA pegadinha da Q1A, que você tinha acabado de responder certo). Conserto: `distancia = int(distancia)`, `periodo = periodo.upper()`.
O caso do `.upper()` é pior: não crasha, só dá resposta errada em silêncio ("d" virava taxa dobrada).

**3. Q3, `is not` em vez de `!=`.**
`is` compara identidade de objeto, não conteúdo. Pra string é `==`/`!=`. O Python avisou no SyntaxWarning ("Did you mean !=?"): **ler os warnings, eles entregam o conserto**.

**4. Q3, `x != "D" or "N"` achando que é "nem D nem N".**
Python lê `(x != "D") or ("N")`, e `"N"` é sempre truthy: condição sempre True, tudo virava ERRO DE ENTRADA. O `or` não distribui como na fala. Idioma certo: `periodo not in ["D", "N"]`. Versão verbosa: `periodo != "D" and periodo != "N"` (com `!=` o conector é `and`, nunca `or`).

**5. Q3, `1,2` em vez de `1.2`.**
Vírgula em Python cria **tupla**: `x / 1000 * 1,2` vira `(x/1000*1, 2)`. Decimal é ponto. Reflexo brasileiro de vírgula decimal: caçar isso no código antes de entregar.

**6. Q3, bordas `<` onde o enunciado diz "até X" (inclusive).**
"Até 2.000" inclui o 2000: é `<=`. Com `<`, as entradas exatas 2000/8000/15000 caem na faixa errada. Rubrica é binária ("todos os cenários"): 3 bordas erradas = 1,5 pt zerado.

**7. Q3, declarar vitória com UM teste.**
"Agora foi" com só `1500 + d` testado, que não passa nem perto dos bugs restantes. Um caminho verde não valida os outros ramos. Protocolo: testar **cada faixa + cada borda exata + cada categoria** antes de seguir. Na prova: rodar o exemplo do enunciado E um caso de borda inventado.

## Dúvidas tiradas (conceitos pra fixar)

**`print()` vs auto-display no Jupyter:** célula de notebook exibe sozinha só a ÚLTIMA expressão. Script `.py` não exibe nada sem print. Pra prova: usa `print` sempre que o enunciado pedir "apresente/imprima", e obrigatório quando precisa mostrar mais de uma coisa na mesma célula.

## Padrões recorrentes (o meta-erro)

- **Achar que método altera a variável in place.** Strings são imutáveis: `int()`, `.upper()`, `.replace()`, `.split()` retornam valor novo. Sempre atribuir.
- **Testar só o caminho feliz.** Os bugs sobreviveram a 2 rodadas porque o teste era sempre o mesmo input confortável.
- **Tradução literal da fala pra lógica.** "Não é D nem N" não vira `!= "D" or "N"`. Montar a tabela mental: cada lado do `and`/`or` precisa ser comparação completa.
