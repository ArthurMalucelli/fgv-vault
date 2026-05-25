---
materia: Programacao
data: 2026-05-07
tema: Manipulação de dados com Pandas — DataFrames, seleção, ordenação e filtros lógicos
topicos: [Pandas, DataFrame, loc, iloc, fatiamento lógico, sort_values, value_counts]
tags: [aula, transcrito]
---

## Contexto: Pandas vai cair na prova final

Esse conteúdo de [[Pandas]] vai cair na prova final, junto com o conteúdo que vem antes da avaliação.

## O que é Pandas

[[Pandas]] é uma biblioteca para manipular dados tabulares, aqueles dados que parecem planilhas. Até agora a gente viu definições de variáveis, atribuição: variável A recebe valor 3, variável B recebe valor falso. A gente fez várias operações com essas variáveis: somar, subtrair, usar elas. Mas todos os objetos que a gente viu até agora eram razoavelmente simples: número inteiro, número com ponto decimal (float), booleano (verdadeiro/falso), string e listas. Talvez a string seja a mais complexa dentro dos que a gente viu.

A partir de hoje, a gente vai ver um tipo de objeto bem mais complexo. Vamos colocar dentro de uma variável um objeto inteiro, tabular, ou seja, um objeto como se fosse uma planilha, com várias linhas e várias colunas. Por exemplo, vou chamar isso de `df`. Poderia ter chamado de `a`, poderia de `b`, mas vamos chamar de `df`. Esse objeto inteiro, que tem várias linhas e várias colunas, vai ser rotulado como `df`.

Junto com essa complexidade, vem o fato de que esse tipo de dado vai ter várias funções para a gente manipular. Várias delas vocês vão poder relacionar com operações que fazem no Excel. Muita coisa que se faz no Excel, dá pra fazer aqui no Python, só que aqui no Python a gente faz de maneira programática. No Excel está tudo mapeado em menus e botões. No Python, vocês vão precisar chamar funções específicas para fazer determinados procedimentos. Existe um paralelo entre os dois, mas o Python é bem mais flexível.

A biblioteca para utilizar dados tabulares em Python chama-se [[Pandas]].

## Origem do Pandas

O [[Pandas]] foi criado por uma pessoa chamada [[Wesley McKinney]], que trabalhou em uma instituição financeira. Ele queria fazer análises relacionadas ao trabalho dele, em inteligência financeira, e não estava contente com as ferramentas que tinha disposto na época: R, Matlab, etc. Resolveu escrever a própria biblioteca dele, que é o Pandas. Depois, ele tornou a biblioteca de domínio público. Muita gente usa nos trabalhos do dia a dia. Eu uso muito no meu, várias instituições financeiras do mundo e do Brasil também usam.

## Importação da biblioteca

```python
import pandas as pd
```

[[Pandas]] é uma biblioteca instalada no ambiente, mas não faz parte da biblioteca padrão no momento em que você carrega o Python. Algumas funções, como `print` ou `input`, já estão pré-carregadas quando você ativa o Jupyter. As funções de Pandas não estão. Por isso você precisa importar.

Essa linha importa todas as funcionalidades do Pandas e atribui um apelido (`pd`). É uma atribuição como `A = 3` ou `B = False`: o que está à direita do igual é colocado à esquerda. `pd` é o apelido da biblioteca; quando você quiser chamar uma função do Pandas, vai usar `pd.alguma_coisa`.

## Anatomia de um DataFrame

```python
df
```

Quando o Jupyter renderiza o `df` na tela, vocês vão ver:

- A parte em negrito na **parte de cima** é o **identificador de coluna**. Eu vou chamar esse cara aqui de **coluna**: a coluna `short`, a coluna `gold`, a coluna `country`.
- A parte em negrito à **esquerda** é o **identificador de linha**. Eu vou chamar de **índice** (em inglês, `index`).
- A parte de dentro são **os dados**.

Então: índice, coluna, e os dados.

No Excel, o identificador de linha é sempre um número, e o identificador de coluna é sempre uma letra. Não dá pra atribuir um nome qualquer no Excel. Em Pandas você pode atribuir qualquer coisa: o índice pode ser um número, pode ser um string, pode ser uma letra, qualquer tipo.

Esse [[DataFrame]] específico tem 5 colunas e 86 países. Cada linha corresponde à quantidade de medalhas que cada país ganhou na edição de 2016: medalhas de ouro, prata, bronze, junto com nome do país e o acrônimo.

A gente vai fazer várias coisas: operações, seleções. Vamos usar instruções para selecionar uma coluna, três colunas, fatiar linhas, fatiar colunas, fatiar fragmentos (não todas as linhas, mas um conjunto selecionado). E também vamos aprender a fazer **fatiamento lógico**: por exemplo, todas as linhas que tiveram mais de 20 medalhas de ouro, ou todas as linhas que tiveram mais de 10 medalhas de prata. É uma seleção baseada em critério lógico.

## Funções básicas: len e shape

```python
len(df)
df.shape
```

`len` é o velho conhecido. Quando o argumento é uma string, ele conta caracteres. Quando é uma lista, conta a quantidade de elementos. Quando é um objeto complexo, ele retorna a quantidade de linhas. `shape` retorna dois valores: quantidade de linhas e quantidade de colunas.

## Fatiamento (selecionar pedaços do DataFrame)

A regra: **sempre usando colchete**. Não confundam colchete com parênteses. Sempre que vocês virem `df[...]`, significa: vou extrair alguma coisa, algum fragmento do DataFrame. Pode ser uma coluna, um conjunto de colunas, uma linha, um conjunto de linhas, ou uma seleção lógica.

### Selecionar uma coluna

```python
df["gold"]
```

Coloca o nome da coluna entre aspas porque o nome é uma string. Retorna a coluna inteira.

Esse DataFrame tem 86 linhas, mas nem todas estão sendo exibidas. A partir de um certo limite, ele mostra só as primeiras 5 e as últimas 5, e no meio omite com `...`. O padrão é 50: até 50 ele mostra tudo, acima de 50 ele começa a omitir. É configurável.

### Selecionar várias colunas

```python
df[["gold", "silver", "bronze"]]
```

Aqui parece que abriu e fechou colchete duas vezes. Mas a interpretação é a seguinte:

- O **colchete mais externo** significa: vou fatiar o DataFrame.
- O **colchete mais interno** é a definição de uma **lista**.

Ou seja, dentro do colchete externo eu coloco uma lista com os nomes das colunas que quero. Os dois colchetes têm significados diferentes, mesmo que pareçam a mesma coisa.

## Ordenação: sort_values

```python
df.sort_values("country")
```

Essa é uma maneira de chamar a função: a gente considera que `df` é o primeiro argumento da função `sort_values`. É como se quisesse chamar `sort_values` em cima do `df`, usando a coluna `country` como critério.

Quando é número, ordena numericamente. **O default é do menor para o maior**. Se quiser o contrário:

```python
df.sort_values("gold", ascending=False)
```

`ascending=False` inverte: ordena do maior para o menor.

### Ponto crucial: sort_values não altera o objeto

Quando aperto Shift+Enter e ele apresenta o resultado ordenado na tela, o objeto **não foi alterado**. Na memória, o `df` continua exatamente como estava antes. O comando significa: ordena e apresenta na tela como seria a versão ordenada.

Para efetivamente alterar o objeto, é preciso reatribuir:

```python
df = df.sort_values("gold")
```

Aí sim o conteúdo ordenado vai sobrescrever o `df` original.

Cuidado: o `sort_values` do Pandas é diferente do `.sort()` da lista. São duas pessoas diferentes que escreveram cada coisa, e cada uma fez de um jeito diferente. Inclusive o nome da função é diferente: na lista é `sort`, no Pandas é `sort_values`.

## Fatiamento por critério lógico

Essa sintaxe parece estranha na primeira vista, mas é assim que se faz.

```python
df[df["gold"] == 0]
```

Lendo de fora pra dentro: o colchete externo serve pra fatiar. O que está dentro do colchete: se você bota uma string, ele fatia uma coluna; se bota uma lista de strings, fatia várias colunas. Aqui a sintaxe é diferente.

O que isso significa: **selecionar todas as linhas onde o valor da coluna `gold` é igual a zero, e retornar só essas linhas**. Resultado prático: todos os países que não ganharam medalhas de ouro.

A sintaxe é: `df[ ... ]`, e dentro do colchete vai `df["gold"] == 0` (nome da coluna, dois iguais, valor de comparação).

### Operadores lógicos: ~ & |

Os operadores de comparação (`==`, `>`, `<`, `>=`, `<=`) são os mesmos do Python.

O que muda em Pandas são os operadores **AND, OR e NOT**:

| Operador | Python puro | Pandas |
|---|---|---|
| AND | `and` | `&` |
| OR | `or` | `|` |
| NOT | `not` | `~` |

A barra vertical (`|`) está, no teclado de vocês, do lado do Shift à esquerda.

### Negação: ~

```python
df[~(df["gold"] > 10)]
```

Para negar a condição lógica, envolve em parênteses e coloca um `~` antes. É o "not" do Pandas.

### AND: duas condições concatenadas

```python
df[(df["gold"] > 5) & (df["gold"] < 10)]
```

Países com mais de 5 medalhas de ouro **E** menos de 10. As duas condições têm que ser atendidas.

### OR: pelo menos uma condição

```python
df[(df["gold"] > 10) | (df["silver"] < 10)]
```

Países com mais de 10 medalhas de ouro **OU** menos de 10 de prata. Vai retornar uma quantidade maior, porque basta atender uma das condições.

Dica do Jupyter: quando você clica logo depois de um parênteses, ele faz o highlight do parênteses correspondente que abre. Vale também pra colchete.

## Fatiamento por linha: .loc

Quando coloco `df["coluna"]`, ele retorna a coluna. Para fatiar pela **linha**, é preciso usar o acessório `.loc`.

```python
df.loc[1]
df.loc[[1, 2, 3]]
```

Dentro de `df.loc[...]`, o que vai dentro **não é identificador de coluna, é identificador de linha**. Para passar várias linhas, usa lista (precisa de dois colchetes, igual no caso das colunas).

Por que `.loc`? Porque se você usa `df[...]` direto, tudo que entra dentro do colchete é interpretado como identificador de coluna. Para sinalizar que é linha, precisa do `.loc`.

### Forma canônica do .loc

```python
df.loc[[linhas], [colunas]]
```

Identificador de linha, vírgula, identificador de coluna. Você pode omitir a parte das colunas e passar só as linhas, como fiz acima. Mas se passar as duas, ele retorna o **fragmento** correspondente: aquelas linhas, só com aquelas colunas.

Pergunta da turma: e se eu quero buscar pela Rússia, pelo nome do país? Aí você usa um critério lógico para selecionar:

```python
df[df["country"] == "Russia"]
```

Atenção: às vezes o valor está com caracteres estranhos no final (espaço, quebra de linha invisível). Se acontecer, dá pra fazer um `strip` para limpar.

## Fatiamento por posição numérica: .iloc

Toda linha e coluna tem um número associado, sempre começando do zero. Da esquerda pra direita, vai 0, 1, 2, 3, 4 nas colunas. De cima pra baixo, 0, 1, 2, 3 nas linhas.

```python
df.iloc[0]
df.iloc[0:5, 1:3]
```

`.iloc` é a maneira de indexar **sempre usando o número**, em vez do nome.

Então:

- `.loc` → usa o **nome** (label) da linha/coluna
- `.iloc` → usa o **número** (posição)

Tanto um quanto o outro aceitam dois pontos (`:`) pra significar "do tal número até o tal número", igual o slicing de lista.

## Funções de consolidação (agregação)

### sum

```python
df["gold"].sum()
```

Pega a coluna inteira e soma. Resultado: 307 medalhas (total da coluna).

A sintaxe `objeto.metodo()`: a parte antes do `.sum` seleciona a coluna inteira; o `.sum()` à direita soma os números da coluna.

```python
df[df["gold"] > 30]["gold"].sum()
```

Dissecando da esquerda pra direita: `df[df["gold"] > 30]` seleciona todas as linhas onde gold é maior que 30 (fatiamento lógico). Em cima desse fragmento, `["gold"]` seleciona só a coluna gold. E `.sum()` soma. Resultado: 245, que significa o total de medalhas de ouro dos países que tiveram mais de 30 medalhas de ouro.

### mean, std

```python
df["gold"].mean()   # média
df["gold"].std()    # desvio padrão (standard deviation)
```

A média da coluna gold é 3.56 medalhas por país.

### value_counts

```python
df["gold"].value_counts()
```

Dá a contagem de cada ocorrência. Tem 27 países que ganharam zero medalha de ouro, 21 países que ganharam uma, 11 países que ganharam duas, etc.

A moda dessa distribuição é zero (valor mais frequente). A mediana é 1, e a média é 3.56.

### Distribuição assimétrica

Mediana 1, média 3.56. Essa é uma distribuição muito comum: muitos países que ganham poucas medalhas, e poucos países que ganham muitas. Onde mais aparece esse formato? Distribuição de renda, salário (principalmente salário em empresa). Diferente da altura ou peso das pessoas, que é uma distribuição mais simétrica.

### unique e nunique

```python
df["gold"].unique()    # valores distintos
df["gold"].nunique()   # quantos valores distintos
```

Quais são os valores únicos que aparecem na coluna gold: 0, 1, 2, 3, 8, 10... Não tem nenhum país que ganhou 11 medalhas, nem 13, 14, 15, 16. Tem 17, mas não tem 18.

### head e tail

```python
df.head()    # 5 primeiras linhas (default)
df.head(10)  # 10 primeiras linhas
df.tail()    # 5 últimas
df.tail(3)   # 3 últimas
```

Default é 5. Se quiser número diferente, passa como argumento.

## Aperitivo: série temporal (eletiva de manipulação de dados)

Esse conteúdo a gente não vai ver nessa disciplina, mas eu dou uma eletiva chamada "Manipulação de Dados em Python" e a gente vê muito desse tipo.

Esse outro [[DataFrame]] tem dados de Ethereum. No índice não tem mais 0, 1, 2, 3: tem instantes no tempo. Sempre que o índice denota tempo, a gente chama de **série temporal**.

Colunas: preço de abertura, maior preço, menor preço, preço de fechamento, e quantidade de tokens negociados naquele minuto. É um DataFrame de minuto a minuto, de 1º de janeiro de 2020 até final de 2022.

Dá pra fazer muita coisa: agregar, tirar média. Pegar o preço de fechamento de cada dia (último valor do último minuto). Antes era minuto a minuto, agora é dia a dia. Dá pra plotar, agregar por mês, por trimestre. Dá pra fazer média móvel (média dos últimos 14 dias).
