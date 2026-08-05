---
materia: Programacao
data: 2026-05-12
tema: Pandas, indexação, fatiamento lógico, str accessor e criação de colunas
topicos: [DataFrame, loc, iloc, Fatiamento lógico, str accessor, Criação de coluna, DataFrame vazio]
tags: [aula, transcrito]
---

## Recap da aula passada

Vamos passar para esse outro notebook. Deixa eu recapitular um pouquinho o que a gente viu na aula passada.

Apresentei pra vocês o que é o [[DataFrame]]. DataFrame é esse objeto tabular que tem coluna e tem linha. Nessa parte aqui de dentro são os dados.

Vimos algumas funções: `LEN`, `SHAPE`. `SHAPE` retorna a quantidade de linhas e colunas. Para acessar uma coluna, ou seja, para recuperar, indexar ou fatiar, basta você colocar o nome da coluna entre colchetes. Se for uma coluna só, passa o nome direto. Se for mais de uma coluna, você precisa passar em forma de lista.

Também vimos algumas funções tipo ordenação, `sort_values`. Você coloca o nome da coluna que quer usar como critério de ordenação, pode ser alfabético, pode ser numérico.

[[Fatiamento lógico]] por valor. Só relembrando essa questão aqui, a primeira vez pode causar um pouquinho de confusão. A maneira como eu costumo pensar é o seguinte: esse colchete aqui fora, basicamente eu estou selecionando uma sequência de linhas onde a coluna `gold` é igual a zero. A maneira de pensar isso é que o colchete mais de fora significa que você vai fazer algum tipo de indexação. E essa parte aqui de dentro é o que efetivamente é o seletor. Basicamente eu estou pegando a coluna `Gold` do `df` e estou fazendo `== 0`, ou seja, estou selecionando as linhas onde `Gold` é igual a zero.

Esse colchete de dentro tem um propósito relacionado com esse `df` aqui dentro, enquanto o colchete de fora tem outro propósito que é com o `df` de fora. A primeira vista parece que você está sendo redundante, colocando o `df` duas vezes, mas são propósitos diferentes.

Fatiamento usando [[loc]] e [[iloc]]. Quando é que você usa o `loc`? Quando você quer indexar por esses valores aqui, que sejam strings ou números, mas esses identificadores que fazem parte do nome de coluna, do nome de linha. A forma canônica do `loc` é você separar por vírgula. O que vem antes da vírgula é o identificador de linha e o que vem depois da vírgula é o identificador de coluna.

O `iloc` é quase igual, só que você usa o número (posição). E sempre é o identificador de linha antes da vírgula, identificador de coluna depois.

Estatísticas. Soma, média, desvio padrão, sempre nesse formato: `df["coluna"].sum()`, `df["coluna"].mean()`, `df["coluna"].std()`.

Valores únicos com `unique()`.

## Slicing com loc vs iloc

Façam esse exercício: selecionar as linhas 5 até 10.

```python
df.loc[5:10]    # retorna até a linha 10 (INCLUSIVO)
df.iloc[5:11]   # retorna até a linha 10 (precisa colocar 11)
```

Repara o seguinte: se você usar o `loc` até o 11, ele vai até o 11. Se você usar o `iloc`, ele segue exatamente aquela mecânica que a gente aprendeu na indexação de lista, que é sempre um número posterior ao último número retornado.

Então no `iloc` você tem que colocar `11` pra incluir até o 10. No `loc` não, você coloca só o 10 e ele retorna exatamente até o 10.

> Pergunta: e o `loc` considera a posição da linha?
>
> O `loc` ele considera o identificador, não a posição. Só que por coincidência, se você olhar aqui, o identificador zero corresponde à posição zero, o identificador um corresponde à posição um. Tem uma coincidência, mas não necessariamente. Poderia ser qualquer outra coisa, poderia ser o próprio nome da cidade.

Quando é slice (com dois pontos), não precisa de colchete duplo. O pandas já entende.

## Selecionar coluna depois de fatiar linhas

Se eu quisesse só a coluna `cidades` dessa seleção, o que eu teria que modificar?

```python
df.loc[5:10, "cidades"]
# ou
df.loc[5:10][["cidades"]]
```

O colchete que você abre, ele só fecha no final.

## Fatiamento lógico — cidades de SP

Selecionar as cidades do Estado de São Paulo.

```python
df[df["UF"] == "SP"]
```

Esse colchete externo serve para indicar que você vai indexar. Aqui dentro é a condição lógica.

## Coluna booleana usada diretamente

Selecionar as cidades que são capitais.

```python
df[df["capital"] == True]
# ou simplesmente
df[df["capital"]]
```

Isso aqui é um valor booleano, o tipo dele é `bool`. Não é uma string `"True"`. Se fosse string aí teria que colocar aspas.

> Pergunta: dá pra omitir o `== True`?
>
> Confere. Essa coluna aqui já é true ou false por natureza, então a comparação `== True` é redundante. Eu simplesmente posso omitir e ele retorna o mesmo resultado.

## Combinando condições — & com parênteses

Selecionar linhas do RJ exceto a capital.

São duas condições. Quando você tem duas condições, você tem que uni-las através de operadores. Lembrando que em pandas os operadores são esses:

| Operação | Símbolo |
|---|---|
| E (AND) | `&` |
| OU (OR) | `\|` |
| NÃO (NOT) | `~` |

```python
df[(df["UF"] == "RJ") & (df["capital"] == False)]
```

Quando você usa o `&`, você precisa colocar cada condição entre parênteses.

Maneira alternativa usando `~` (não):

```python
df[(df["UF"] == "RJ") & ~df["capital"]]
```

Como `df["capital"]` já retorna booleano, o `~` inverte direto.

## Estatísticas em coluna

```python
df["população"].mean()
df["população"].std()
```

Se você não colocar os parênteses, ele não dá erro, mas retorna um negócio bizarro tipo `bound method`. Pra realmente rodar a função, você tem que colocar os parênteses.

Quando dá erro (aquela caixa vermelha), normalmente a dica pra você consertar tá na **última linha** do traceback.

## Combinando loc com seleção lógica e cálculo

Calcular a média de população das capitais.

```python
df.loc[df["capital"], "população"].mean()
```

Vamos quebrar:

- `df["capital"]` retorna booleano por coluna (true/false por linha).
- `df.loc[df["capital"], "população"]` seleciona as linhas onde capital é true E a coluna população.
- `.mean()` calcula a média.

Como eu tenho que selecionar tanto linha quanto coluna, eu necessariamente tenho que usar o [[loc]]. Esses dois separadores aqui: o primeiro é seletor de linha, o segundo é seletor de coluna.

## Display para mostrar dois resultados

Por padrão, quando você junta duas expressões numa célula, o Jupyter só mostra a última. Se você quer mostrar as duas, força com `display()`:

```python
display(df.loc[df["capital"], "população"].mean())
display(df.loc[df["UF"] == "SP", "população"].mean())
```

> Pergunta: se na prova pedir os dois pra retornar, tem que fazer separado?
>
> Tem que ser dois. Separado.

## str accessor — distribuir função em coluna de strings

Conceito novo. Dá uma olhada nessa coluna do DataFrame `times`. Nessa coluna tem vários strings, certo? A gente sabe manipular esse string individualmente. Por exemplo:

```python
t = "Flamengo"
t[0]        # primeira letra → "F"
t.upper()   # tudo maiúsculo → "FLAMENGO"
```

Essas funções existem para esse **objeto string**. Mas repara uma coisa: se eu tentar fazer `times["Time"].upper()`, vai dar erro. Se eu fizer `times["Time"][0]` achando que vai selecionar a primeira letra de cada time, vai dar um resultado bizarro (vai me trazer a linha de índice 0, não a primeira letra).

O [[str accessor]] é a maneira de você indexar ou utilizar funções que existem para string e aplicar a **todos os elementos** que estão na coluna.

```python
times["Time"].str.upper()    # tudo maiúsculo
times["Time"].str.lower()    # tudo minúsculo
times["Time"].str[0]          # primeiro caractere de cada string
times["Time"].str[-1]         # último caractere de cada string
times["Time"].str[-5:]        # últimos 5 caracteres
times["Time"].str.split()     # separa por espaço, retorna lista
times["Time"].str.len()       # quantidade de caracteres
```

O `str` serve para distribuir o que vem à direita dele (seja função ou indexação) em todos os elementos strings que estão na coluna.

## Criar coluna nova

Já mostrei como criar uma nova coluna do [[DataFrame]]. Repara: existe uma coluna chamada `Inicial` no DataFrame? Não. Então:

```python
times["Inicial"] = times["Time"].str[0]
```

Eu coloco o nome do DataFrame, abro colchete, coloco o nome de uma coluna **que não existe**. À direita do `=` coloco uma expressão que me retorna uma coluna. Essa coluna nova vai ser criada à direita da última coluna existente.

> Pergunta: por que você definiu variável com igual?
>
> O `=` no contexto de pandas serve para definir uma coluna nova **ou** para substituir uma que já existe. Se eu tivesse colocado `times["Time"]`, ele ia apagar o conteúdo dela e colocar as iniciais. Como coloquei uma coluna que não existe, ele entende que tem que criar nova.

Pode criar com valor constante também:

```python
times["País"] = "Brasil"
```

Cria a coluna `País` com o mesmo valor em todas as linhas.

> Pergunta: e se eu usar `loc` na hora de criar?
>
> Se você colocar o `loc`, você pode acabar diminuindo a quantidade de linhas. Imagina que tem 6 linhas. Se você fizer `loc` selecionando 3, você tá só selecionando 3. Aí o pandas precisa encaixar esses 3 numa estrutura de 6. Onde tem coincidência de índice ele coloca o valor. Onde não tem, ele coloca **NaN**, que é uma ausência de valor. Vai ficar um negócio meio esquisito. Mas isso é detalhe, não cai na prova.

## Drop de coluna

```python
times = times.drop("País", axis=1)
```

Mas essa função não deve cair na prova.

## Operação aritmética em coluna

Considerando que todos os times ganharam a próxima rodada (cada time ganha +3 pontos por vitória).

```python
times["Pontos próxima rodada"] = times["Pontos"] + 3
```

Estou pegando uma coluna que já é numérica, somando 3 para todos os valores, e colocando o resultado numa coluna nova. Dá pra fazer qualquer operação algébrica: multiplicar, dividir, elevar ao quadrado.

Importante: a coluna `Pontos` tem que ser número. Se tivesse aspas (fosse string) em todos os valores, eu não poderia fazer essa soma.

## DataFrame vazio

Existe algum username `Getulio`? Não existe. O que vocês acham que vai acontecer quando eu rodar isso?

```python
df[df["username"] == "Getulio"]
```

Não vai dar erro. Vai retornar um **DataFrame vazio**: tem as 5 colunas, mas tem zero linhas. Isso é importante.

## Validação de login — checar existência com len

Pergunte ao usuário pelo username e password. Verifica se a pessoa existe. Verifica se a senha corresponde aos últimos 5 dígitos do ID.

```python
username = input("Username: ")
password = input("Password: ")

resultado = df[df["username"] == username]

if len(resultado) == 0:
    print("Username não existe")
else:
    # checagem da senha
    ...
```

Vamos analisar essa expressão. `df[df["username"] == username]` me retorna um DataFrame que tem uma linha (se o username existe) ou zero linhas (se não existe).

- Se eu coloco `Adson` (existe), retorna 1 linha.
- Se eu coloco `Getulio` (não existe), retorna DataFrame vazio (0 linhas).

Então o `len()` dessa seleção me diz se o usuário existe. Se `len == 0`, não existe. Senão, existe e parto para a verificação da senha.

> A parte específica da senha aqui (usando `str[-5:]`) não cai na prova, é detalhe de como o slicing funciona. Mas a parte de **fazer uma seleção lógica e usar `len` pra checar existência** é o tipo de coisa que pode cair.

## Próxima aula

Quiz da aula 16 com o arquivo `tips.csv` e o notebook `tips.ipynb`. Baixar os dois e abrir no Jupyter.
