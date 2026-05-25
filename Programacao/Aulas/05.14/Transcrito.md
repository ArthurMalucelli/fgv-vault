---
materia: Programacao
data: 2026-05-14
tema: Manipulação de DataFrames com Pandas — value_counts, str accessor, condições compostas
topicos: [value_counts, variavel categorica, str.replace, str.contains, astype, describe, condicao composta, notacao cientifica]
tags: [aula, transcrito]
---

## Contar linhas com filtro booleano e value_counts

Como contar quantas linhas têm `gender == "F"`? Mesma seleção lógica que a gente já fez:

```python
df[df["gender"] == "F"]
```

Aquele primeiro colchete de fora significa "vou selecionar alguma coisa do DataFrame". A parte de dentro (`df["gender"] == "F"`) é o critério de seleção. Para contar, envolve com `len`:

```python
len(df[df["gender"] == "F"])
```

Outra maneira de ver a distribuição de uma coluna categórica é [[value_counts]]:

```python
df["gender"].value_counts()
```

Retorna a contagem por categoria (ex: 18 M e 2 F).

## Variável categórica nominal vs ordinal

Quando a coluna é categórica, a maneira de ver distribuição é fazer contagem. Quando é numérica, a gente usa as estatísticas já vistas (média, desvio padrão, mediana).

A diferença entre [[Variavel categorica nominal]] e [[Variavel categorica ordinal]]:

- **Nominal**: não tem ordem entre as categorias. Ex: `M` e `F`. Nenhuma é "maior" que a outra.
- **Ordinal**: existe ordem entre as categorias. Ex: pequeno, médio, grande. Ou classes sociais A, B, C, D, E segundo o IBGE (A é acima de 20 salários mínimos, B entre 10 e 20, etc.).

## Adicionar coluna com valor fixo

Para adicionar coluna nova com valor fixo:

```python
df["planet"] = "Earth"
```

Como `planet` não existe entre as colunas, o Pandas cria uma nova, sempre à direita da última. Se já existisse, ele substituiria o conteúdo (mesma sintaxe).

Para apagar a coluna, duas maneiras. A primeira já foi vista na aula passada. A outra é:

```python
del df["planet"]
```

Inspecionando o DataFrame depois, a coluna some.

## str accessor — recap rápido

`df["name"].str.len()` aplica `len` em **cada string** da coluna e retorna uma coluna nova com a quantidade de caracteres de cada elemento. O `.str` é o distribuidor: sem ele, o `len` tentaria rodar na coluna inteira em vez de em cada elemento.

Definindo o resultado em uma coluna nova:

```python
df["tamanho_nome"] = df["name"].str.len()
```

A coluna nova entra à direita.

## sort_values

```python
df.sort_values("tamanho_nome")                       # crescente (default)
df.sort_values("tamanho_nome", ascending=False)      # decrescente
```

## Reatribuir conteúdo de coluna existente

Primeira vez que aparece atribuir a uma coluna que já existe:

```python
df["username"] = df["username"].str.lower()
```

O conteúdo antigo some, é reposto pelo novo. Se fosse `.str.upper()`, viraria tudo maiúsculo. `str.swapcase()` inverte (minúsculo vira maiúsculo e vice-versa).

> Não precisa decorar essas funções. Na prova final, é permitido trazer uma folha A4 de anotações. Precisa saber **que existe** uma função para cada coisa.

## str.contains — filtro por substring

```python
df["email"].str.contains("fgv.br")
```

Retorna uma coluna de booleanos (true/false por linha). Para usar como filtro:

```python
cond = df["email"].str.contains("fgv.br")
df[cond]
```

Essa maneira de criar uma variável temporária e usar dentro do `df[...]` é equivalente a colocar tudo em uma linha só:

```python
df[df["email"].str.contains("fgv.br")]
```

Mas dividir em duas linhas fica mais legível, evita parênteses aninhados.

## Soma de colunas numéricas linha a linha

```python
df["id_plus_18"] = df["id"] + df["idade"]
```

Como as duas colunas são numéricas, o Pandas entende que é pra somar linha a linha. Cria uma coluna nova com o resultado linha-a-linha.

Notação `10_000_000` é convenção opcional do Python para separar milhão/milhar e ficar mais legível. Na hora de interpretar, o Python ignora os underscores. Equivale a `10000000`.

## Pandas embute for, if, while por baixo dos panos

Pergunta de aluno: usando Pandas, a gente precisa escrever `for`, `while`, `if`, `elif`, `else`? Não. Quando se trabalha com Pandas, você opera no nível acima do Python puro. Para somar duas colunas linha a linha, tem um `for` embutido dentro do método do Pandas, você não vê e não precisa ver. Mesma coisa para `df[df["gender"] == "F"]`: tem um `if` embutido aí dentro, mas não precisa programar.

## astype — conversão de tipo

Não dá pra concatenar string com número direto:

```python
"C" + df["id"]    # erro: id é número
```

Precisa converter a coluna inteira para string com [[astype]]:

```python
df["id"] = df["id"].astype(str)
"C" + df["id"]    # agora funciona
```

Depois do astype, a coluna inteira deixa de ser numérica e vira string.

## str.replace e encadeamento (pipeline)

```python
df["gender"].str.replace("F", "FM")
```

Substitui todas as ocorrências de `F` por `FM` na coluna. Para substituir `F → FM` **e** `M → MM`, encadeia:

```python
df["gender"].str.replace("F", "FM").str.replace("M", "MM")
```

A interpretação é tipo pipeline: o resultado do primeiro `str.replace` é input do segundo. O primeiro substitui só o `F` (o `M` continua como está), o segundo pega esse resultado e substitui o `M`. Se uma função retorna um objeto do mesmo tipo, dá pra encadear indefinidamente.

Funciona com qualquer função de `str` que retorna algo, ex: pode encadear `.str.upper().str.len()` para virar maiúsculo e depois contar caracteres.

## str.split com expand=True

```python
df["name"].str.split()
```

Pega cada string e separa por espaço, cria uma lista por linha. Com `expand=True`:

```python
df["name"].str.split(expand=True)
```

Gera um DataFrame derivado, uma coluna para cada elemento da lista (col 0 = primeiro nome, col 1 = segundo nome, etc.).

## Acessar último elemento depois do split

```python
df["name"].str.split().str[-1]
```

Pega o último elemento da lista produzida pelo split. É o sobrenome (último nome) de cada linha.

## Exercício de prova — DataFrame `laminas` (fundos de investimento)

A) **Mediana do investimento inicial mínimo**

```python
df["investe inicial mínimo"].median()
```

Resultado: R$ 1.000. Mediana significa que metade dos fundos tem investimento mínimo abaixo de mil, metade acima.

`df.describe()` dá várias estatísticas de uma vez: média, desvio padrão, mínimo, máximo, e os percentis 25%, 50%, 75%. O 50% é a [[Mediana]], o 25% é o **primeiro [[Quartil]]**, o 75% é o terceiro quartil.

B) **Fundos com investimento inicial igual à mediana**

```python
M = df["investe inicial mínimo"].median()
laminas_cel = laminas[laminas["investe inicial mínimo"] == M]
```

Igual exatamente (não maior-igual). São 189 fundos com investimento inicial = R$ 1.000.

Se quisesse só o nome do fundo (uma coluna em vez de todas), tem que usar [[loc]] para combinar seleção de linha + coluna:

```python
laminas.loc[laminas["investe inicial mínimo"] == M, "nome_do_fundo"]
```

C) **Dentre os fundos de B, os que têm CDI ou IMAB no índice de referência**

Trabalha sobre `laminas_cel` (já filtrado pela B). Duas condições com OR (`|`):

```python
cond1 = laminas_cel["índice de referência"].str.contains("CDI")
cond2 = laminas_cel["índice de referência"].str.contains("IMAB")
laminas_cel2 = laminas_cel[cond1 | cond2]
len(laminas_cel2)    # 135
```

Bem mais legível do que escrever tudo numa linha com parênteses aninhados. Atenção: `CDI 100%` está contido em `CDI` via `.str.contains`, então selecionar os dois daria sobreposição (por isso o problema foi reformulado para `CDI` ou `IMAB`).

D) **Média do patrimônio líquido em bilhões**

```python
laminas_cel2["patrimônio líquido"].mean() / 1e9
```

[[Notacao cientifica]]: `1e9` é 10⁹, ou seja, 1 bilhão. `1e6` é 10⁶ (milhão). É o mesmo que escrever `10**9`, só mais compacto.

## Próximo dataset — clubes de futebol

Aula próxima: 100 clubes com maior capitalização de mercado do mundo. Madrid lidera com market cap ~1,4 bilhão. Tem 29 jogadores no plantel, idade média 25-27, valor médio por jogador 46M euros.

Coluna de market cap vem como string (`1.4B`, `850M`), mistura `B` e `M`. Para fazer cálculo algébrico com média, precisa transformar em número, multiplicando `M` por 10⁶ e `B` por 10⁹. Tema da próxima aula: estratégia para parsear isso.
