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

**9. Q4C, `IndentationError: unexpected indent`.**
Um espaço a mais antes de `imc` dentro do bloco do `if`. Linhas do mesmo bloco começam TODAS na mesma coluna. Quando o erro fala de indentação, é espaço, não lógica: seleciona o bloco e alinha com `Cmd+[` / `Cmd+]`.

**10. Q4C, print colando string e variável: `print("Paciente" input_id, ...)`.**
SyntaxError. Saída formatada é caso de f-string: `print(f"Paciente {input_id} (IMC: {imc:.1f}) – Risco: {risco}")`. O `f` liga o modo, `{}` avalia variável, resto é literal. Montar formato exato com vírgulas de print não funciona (espaços sobrando).

**11. Q4C, coluna inteira onde era a linha do paciente.**
`pacientes["fumante"] == "sim"` compara a COLUNA (1000 valores) e dá `ValueError: truth value of a Series is ambiguous` dentro do if. Depois do `.iloc[0]`, todos os dados do paciente vêm de `linha[...]`, nunca de `pacientes[...]`. Tabela = todo mundo; linha = o paciente.

**12. Q4C, `and` onde o enunciado diz "OU" (regra 3).**
Com `and`, jovem obeso não-fumante caía em risco baixo. Traduzir conectivo do enunciado literalmente: OU = `or`, E = `and`, e a ordem das regras é a prioridade do `elif`.

## Dúvidas tiradas (conceitos pra fixar)

**`print()` vs auto-display no Jupyter:** célula de notebook exibe sozinha só a ÚLTIMA expressão. Script `.py` não exibe nada sem print. Pra prova: usa `print` sempre que o enunciado pedir "apresente/imprima", e obrigatório quando precisa mostrar mais de uma coisa na mesma célula.

**Float binário, o `3.5999999999999996`:** o computador não representa `1.2` exato em binário, então `3.0 * 1.2` sai com resíduo. NÃO é erro de lógica. Se aparecer na prova, não entra em pânico nem "conserta" a conta: formata a saída com `f"{x:.2f}"` ou `round(x, 2)` e segue.

**Criar coluna nova em DataFrame:** atribuição direta cria, `df["Nova"] = df["A"] * df["B"]`. Vetorizado, sem laço. Nome de coluna existente tem que ser EXATO (acento, maiúscula), senão `KeyError`; confere com `df.columns`.

**Checar se valor existe numa coluna:** `x in df["col"].values`. O `.values` é obrigatório: sem ele o `in` checa o ÍNDICE, não o conteúdo. E o tipo tem que bater: input é `str`, coluna numérica exige `int(input(...))` antes, senão dá `False` sempre.

**Selecionar UMA linha por chave e ler as células:** `linha = df[df["id"] == x].iloc[0]`, depois `linha["coluna"]`. O filtro devolve mini-DataFrame; `.iloc[0]` extrai a linha como Series. Pra saída formatada: decidir o resultado numa variável e dar UM print no final com f-string (`{imc:.1f}`); caractere especial do enunciado (travessão `–`) se copia, não se digita.

**O que é `.iloc[0]`:** filtro devolve TABELA (mesmo com 1 linha só); `.iloc[0]` pega a linha na POSIÇÃO 0 dessa tabela como Series. `iloc` = por posição física, `loc` = por nome do índice (a linha filtrada mantém o índice original, então `.loc[0]` quebraria). Cadeia: filtrar → tabela; `.iloc[0]` → linha; `linha["col"]` → valor.

**Texto + variável no print, os 3 jeitos:** Python não tem justaposição (`"texto" variavel` é SyntaxError; tudo precisa de vírgula, operador ou estar numa string só).

```python
print("Paciente", x, "(IMC:", imc, ")")    # vírgulas: espaço automático entre args, suja formato exato
print("Paciente " + str(x))                # +: exige str() em tudo
print(f"Paciente {x} (IMC: {imc:.1f})")    # f-string: controle total, USAR ESTE
```

Anatomia do f-string: `f` antes das aspas liga o modo; `{}` avalia variável/expressão; resto sai literal. `{imc:.1f}` = "imc com 1 casa decimal" (antes do `:` o quê, depois o como). Mesmo mecanismo de `{total:.2f}`. Em formato exato, f-string é o único dos 3 que serve.

**8. Q4C, `"1" in coluna de ints` deu Falha.**
Mesmo erro do input-é-string, TERCEIRA ocorrência do dia (Q1A, Q3, Q4C). `input()` devolveu `"1"` e `"1" == 1` é False, então o `in` nunca acha. Conserto: `int(input(...))` na mesma linha. Aconteceu MINUTOS depois do aviso explícito: é o teu erro número 1, checar input ANTES de qualquer comparação.

**Indexação de lista, `partes[0]`:** lista é fila de caixinhas numeradas DO ZERO. `split` = Texto para Colunas do Excel: `"Ana,8.5".split(",")` → `["Ana", "8.5"]`, onde `partes[0]` é "Ana" e `partes[1]` é "8.5". Batizar (`nome = partes[0]`) é opcional mas evita trocar campo. Mesmo zero de `meses[int(mes)-1]` e `.iloc[0]`: Python conta tudo do 0. Atalho: `loja, nota, valor = reg.split("|")` batiza os 3 de uma vez.

**Padrão ACUMULADOR (o esqueleto da Q5, 3,0 pts em toda prova):** acumuladores nascem zerados FORA do laço; crescem DENTRO (`contador += 1`, `total += valor`); o print de cada item fica dentro, o totalizador fica DEPOIS do laço, sem indentação (indentado = imprime a cada item). Dentro do laço a ordem é: split → batizar pedaços → converter numérico (`float`/`int`, split devolve str) → acumular → print do item.

## Padrões recorrentes (o meta-erro)

**17. Q5A, `return` solto pra "fechar" o laço.**
`SyntaxError: 'return' outside function`. Bloco em Python fecha por DESINDENTAÇÃO: a primeira linha que volta à margem já está fora do laço. Não existe End/Next/fechamento. `return` é exclusivo de função (`def`), serve pra sair dela, nada a ver com loop.

**16. Q5A, híbrido de `+` com `{}` fora de f-string.**
`print("Nota"+ {numero} ...)` → SyntaxError. Chaves só injetam variável DENTRO de `f"..."`; soltas criam set. Regra: escolher UM método e ir até o fim. F-string = UMA string contínua, `f` na frente, chaves dentro das aspas, zero `+`. Segunda tropeçada em f-string do dia (ver erro 10): na prova, escrever o texto literal primeiro e só depois envolver as variáveis com chaves.

**13. Q5A, split na LISTA em vez do item do laço: `registros.split("|")`.**
`AttributeError: 'list' object has no attribute 'split'`. O `for i in registros` entrega UM registro por vez no `i`; dentro do laço se trabalha com `i`, nunca com a lista inteira. Split é da fruta, não da cesta.

**14. Q5A, `float(valor)` solto, QUARTA ocorrência do conversão-sem-atribuir.**
Q1A, Q3, Q4C, Q5A. Conversão devolve valor novo: `valor = float(partes[2])`. Sem isso o `total += valor` estoura TypeError.

**15. Q5A, esqueceu os dois prints do padrão acumulador.**
Print do item DENTRO do laço, totalizadora FORA (depois dele). Juntos valem 1,5 da rubrica. Acumular sem mostrar não pontua.

- **TODO input()/conversão nasce string até atribuir (4 ocorrências hoje).** A primeira pergunta depois de qualquer input ou split: "converto pra quê, e atribuí?". Comparação ou conta com número exige `valor = int(...)`/`float(...)` na mesma linha.
- **Aplicar só o primeiro conserto da lista e re-rodar (2 ocorrências: Q3 e Q4C).** Correção é checklist: aplicar TODAS, riscando uma a uma, depois rodar. Na prova: conferir cada exigência do enunciado contra o código, item a item.
- **Achar que método altera a variável in place.** Strings são imutáveis: `int()`, `.upper()`, `.replace()`, `.split()` retornam valor novo. Sempre atribuir.
- **Testar só o caminho feliz.** Os bugs sobreviveram a 2 rodadas porque o teste era sempre o mesmo input confortável.
- **Tradução literal da fala pra lógica.** "Não é D nem N" não vira `!= "D" or "N"`. Montar a tabela mental: cada lado do `and`/`or` precisa ser comparação completa.
