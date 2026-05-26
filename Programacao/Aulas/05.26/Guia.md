---
materia: Programacao
data: 2026-05-26
tema: Avaliação Prática em Grupo, guia do zero
tags: [estudo, prova, pandas]
---

# Guia Avaliação 26.05 — Pandas do zero

## Como usar este guia

Lê do começo. Cada seção depende da anterior. Não pula. Roda os exemplos no Jupyter Lab pra ver o resultado acontecer.

Tempo realista: 2 a 3 horas de leitura ativa cobre tudo. A seção 15 é a cola A4 pra imprimir e levar.

## 0. O que é Pandas (analogia com Excel)

Pandas é uma biblioteca de Python pra mexer em tabela de dados. Pensa nele como **Excel com sintaxe de código**.

| Excel | Pandas |
|---|---|
| Planilha | `DataFrame` |
| Coluna | `Series` (uma coluna do DataFrame) |
| Linha | Linha (com um identificador chamado **índice**) |
| Filtro de coluna | Filtro lógico |
| Tabela dinâmica | `groupby` ou `pivot_table` |
| PROCV (`VLOOKUP`) | `merge` |
| Fórmula numa célula | Operação em coluna inteira |
| =`AVERAGE(A:A)` | `df["A"].mean()` |
| =`COUNTIF(...)` | `df["col"].value_counts()` |

**Diferença mental importante:** no Excel você seleciona células com o mouse e aplica fórmula. No Pandas você **escreve** uma expressão e ela age na coluna inteira de uma vez. Não tem laço/loop manual.

Sempre que for usar, importa primeiro:

```python
import pandas as pd
```

`pd` é apelido padrão. A comunidade inteira escreve `pd`. Daqui pra frente todo `pd.algo` vem desse import.

## 1. As duas estruturas: DataFrame e Series

### DataFrame

Tabela de várias linhas e várias colunas. É o objeto principal. Quando você carrega um CSV, vira um DataFrame.

```python
df         # uma tabela inteira
```

### Series

Uma coluna sozinha de uma tabela. Quando você seleciona **uma** coluna do DataFrame, recebe uma Series.

```python
df["Produto"]      # é uma Series (1 coluna)
df[["Produto"]]    # é um DataFrame (1 coluna, mas ainda em formato tabela)
```

A diferença vai importar de vez em quando. Por enquanto: **um colchete vira Series, dois colchetes vira DataFrame**.

### Índice

Cada linha tem um identificador chamado **índice**. Por default é número 0, 1, 2, 3... Você quase nunca precisa mexer nele pra essa prova.

## 2. Os dois datasets da avaliação

### `postos_sp_2025.csv` (76 mil linhas)

Coletas de preço de combustível em postos de SP, mês a mês, de jan a jun/2025.

| Coluna | O que é |
|---|---|
| `Regiao` | Sempre `SE` |
| `Estado` | Sempre `SP` |
| `Municipio` | Cidade em maiúsculas, sem acento (`SAO PAULO`, `CAMPINAS`) |
| `Revenda` | Nome da empresa do posto (`AUTO POSTO MISTRAL LTDA.`) |
| `CNPJ` | CNPJ do posto (**começa com um espaço**, cuidado) |
| `Produto` | `GASOLINA`, `ETANOL`, ou `DIESEL S10` |
| `Data da Coleta` | Data formato `dd/mm/yyyy` |
| `Valor de Venda` | Preço cobrado, com vírgula decimal (`5,99`) |
| `Bandeira` | Distribuidora (`VIBRA`, `RAIZEN`, `IPIRANGA`, `ALE`, `BRANCA`...) |

### `distribuicao_municipios_sp_2025.csv` (3,5 mil linhas)

Preço de distribuição (atacado) por município, mês e produto.

| Coluna | O que é |
|---|---|
| `Municipio` | Mesma cidade que aparece em `postos` |
| `Mes` | Formato `2025-01` (ano-mes) |
| `Produto` | Mesmos 3 produtos |
| `Preco_Distribuicao` | Preço de atacado, com vírgula decimal |

**Como os dois se conectam:** chave de junção é `Municipio + Produto + Mes`. Você vai precisar criar a coluna `Mes` em `postos` antes de juntar.

## 3. Carregando os arquivos (`read_csv`)

```python
import pandas as pd

postos = pd.read_csv(
    "postos_sp_2025.csv",
    sep=";",
    decimal=",",
)

distrib = pd.read_csv(
    "distribuicao_municipios_sp_2025.csv",
    sep=";",
    decimal=",",
)
```

Por que cada argumento:

- **`sep=";"`** porque o arquivo usa ponto e vírgula como separador entre colunas, não vírgula. Se você esquecer, o pandas lê o arquivo inteiro como uma única coluna gigante de texto.
- **`decimal=","`** porque os preços vêm como `5,99` (padrão brasileiro). Sem isso, o pandas mantém como string `"5,99"` e você não consegue tirar média.

`postos` agora é um DataFrame com 76k linhas e 9 colunas. `distrib` é um DataFrame com 3,5k linhas e 4 colunas.

## 4. Primeira olhada nos dados

Sempre que carrega, dá uma olhada pra confirmar que veio do jeito certo.

### Ver as primeiras linhas

```python
postos.head()         # primeiras 5 linhas
postos.head(10)       # primeiras 10
postos.tail()         # últimas 5
postos.sample(3)      # 3 linhas aleatórias
```

Resultado de `.head()`: aparece uma tabela com 5 linhas, todas as 9 colunas, e o índice na esquerda (0, 1, 2, 3, 4).

### Ver dimensões

```python
postos.shape          # (76935, 9)
```

Retorna uma tupla `(linhas, colunas)`. Sem parênteses no final (é atributo, não função).

### Ver os tipos de cada coluna

```python
postos.info()
```

Mostra cada coluna, quantos não-nulos tem, e o tipo (`object` = string/texto, `int64` = número inteiro, `float64` = número decimal, `bool` = verdadeiro/falso).

**Importante na prova:** se `Valor de Venda` aparecer como `object` (texto) em vez de `float64`, é porque o `decimal=","` não pegou. Aí precisa converter manualmente (seção 12.3).

### Listar colunas

```python
postos.columns
```

### Ver estatísticas rápidas

```python
postos.describe()           # média, std, min, max etc. das colunas numéricas
postos.describe(include="all")   # inclui também as colunas de texto
```

## 5. Pegando colunas

### Uma coluna (Series)

```python
postos["Produto"]
```

Retorna uma Series com 76k valores: GASOLINA, ETANOL, GASOLINA, DIESEL S10... e o índice 0, 1, 2, 3...

### Várias colunas (DataFrame)

```python
postos[["Municipio", "Produto", "Valor de Venda"]]
```

Repare o colchete duplo. O externo é "fatie o df", o interno é "esta é uma lista de colunas". **Sem o duplo dá erro.**

### Lembrete sobre o nome da coluna

O nome tem que bater exatamente. Se a coluna se chama `Data da Coleta` (com espaços), você escreve:

```python
postos["Data da Coleta"]            # certo
postos["data da coleta"]            # erro (case)
postos["DatadaColeta"]              # erro
postos.Data                         # nem tenta, não funciona se tem espaço
```

## 6. Pegando linhas com filtro lógico

Esta é a operação mais importante. Funciona em duas etapas mentais:

1. Você cria uma **coluna booleana** (True/False por linha) com uma condição.
2. Joga essa coluna booleana dentro do `df[...]` pra ficar só com as linhas onde é True.

### Exemplo passo a passo

```python
postos["Produto"] == "GASOLINA"
```

Isto retorna uma Series de True/False com 76k valores. Onde a coluna `Produto` é igual a `"GASOLINA"`, vira True.

```python
postos[postos["Produto"] == "GASOLINA"]
```

Agora você está pegando do `postos` só as linhas onde a condição é True. Resultado: um DataFrame menor, só com gasolina.

### Operadores de comparação

| Símbolo | Significado |
|---|---|
| `==` | igual |
| `!=` | diferente |
| `>` `<` | maior, menor |
| `>=` `<=` | maior ou igual, menor ou igual |

Cuidado: `=` (um igual) é atribuição. `==` (dois iguais) é comparação. Errar é erro clássico.

### Exemplos

```python
postos[postos["Produto"] == "GASOLINA"]              # só gasolina
postos[postos["Valor de Venda"] > 7]                 # postos cobrando > 7
postos[postos["Municipio"] == "SAO PAULO"]           # só capital
postos[postos["Bandeira"] != "BRANCA"]               # tudo menos sem bandeira
```

### `.isin([lista])` quando tem várias opções

Em vez de usar várias condições com `|`, dá pra usar `.isin`:

```python
postos[postos["Bandeira"].isin(["VIBRA", "RAIZEN", "IPIRANGA"])]
```

Equivale a "bandeira é uma destas três".

### Contando quantas linhas batem a condição

```python
len(postos[postos["Produto"] == "GASOLINA"])
```

`len(...)` te dá a quantidade de linhas do DataFrame filtrado.

## 7. Combinando filtros (AND, OR, NOT)

### Regra ouro

Em pandas você **não** usa `and`, `or`, `not` (palavras do Python normal). Você usa:

| Operação | Símbolo |
|---|---|
| AND | `&` |
| OR | `\|` |
| NOT | `~` |

**E cada condição precisa estar entre parênteses.** Esquecer parêntese é o erro número um.

### Exemplos

```python
# Gasolina E preço > 6
postos[(postos["Produto"] == "GASOLINA") & (postos["Valor de Venda"] > 6)]

# Vibra OU Raizen
postos[(postos["Bandeira"] == "VIBRA") | (postos["Bandeira"] == "RAIZEN")]

# Tudo menos as brancas
postos[~(postos["Bandeira"] == "BRANCA")]
```

### Versão mais legível (variáveis temporárias)

Quando tem várias condições, fica mais fácil de ler assim:

```python
cond1 = postos["Produto"] == "GASOLINA"
cond2 = postos["Valor de Venda"] > 6
cond3 = postos["Municipio"] == "SAO PAULO"

postos[cond1 & cond2 & cond3]
```

Vale a pena na prova. Erra menos parêntese.

## 8. Filtrar linha E selecionar coluna ao mesmo tempo: `.loc`

Quando você quer fazer DUAS coisas ao mesmo tempo (filtrar linhas + escolher uma coluna específica), precisa usar `.loc`:

```python
postos.loc[postos["Produto"] == "GASOLINA", "Valor de Venda"]
```

Lê assim: "do postos, pega as linhas onde produto é gasolina, e me dá a coluna Valor de Venda".

A vírgula separa linha de coluna: `df.loc[LINHAS, COLUNAS]`.

```python
# Média do preço da gasolina
postos.loc[postos["Produto"] == "GASOLINA", "Valor de Venda"].mean()

# Várias colunas (lista)
postos.loc[postos["Municipio"] == "SAO PAULO", ["Revenda", "Valor de Venda"]]
```

Sem `.loc`, `postos[postos["x"]==1]["col"]` também funciona mas pode dar warning. **Use `.loc` quando combinar filtro com seleção de coluna.**

### `iloc` (parente do `loc`, por posição)

`iloc` faz a mesma coisa mas usando **posição numérica** em vez de nome:

```python
postos.iloc[0]              # primeira linha
postos.iloc[0:5]            # 5 primeiras linhas
postos.iloc[0:5, 0:3]       # 5 primeiras linhas, 3 primeiras colunas
```

Diferença sutil:
- `loc[0:5]` pega da linha 0 até a linha 5 **inclusive** (6 linhas).
- `iloc[0:5]` pega da posição 0 até a 5 **exclusivo** (5 linhas, igual lista Python).

Pra prova, `loc` é o que importa.

## 9. Mexendo em texto (`.str`)

Quando a coluna é texto, você precisa do **`.str`** antes de qualquer função de string. Sem o `.str` dá erro ou comportamento estranho.

A regra mental: `.str` significa "aplica essa operação em cada linha de texto separadamente, e me devolve uma coluna nova".

### Caixa (upper/lower/title)

```python
postos["Revenda"].str.upper()       # MAIÚSCULAS
postos["Revenda"].str.lower()       # minúsculas
postos["Revenda"].str.title()       # Primeira Letra Maiúscula
```

### Tamanho

```python
postos["Revenda"].str.len()         # quantidade de caracteres em cada linha
```

### Tirar espaços das pontas

```python
postos["CNPJ"].str.strip()          # útil pro CNPJ que tem espaço no começo
```

### Procurar substring

```python
postos["Revenda"].str.contains("AUTO POSTO")    # True/False por linha
postos["Revenda"].str.startswith("AUTO")        # começa com?
postos["Revenda"].str.endswith("LTDA")          # termina com?
```

`contains` é muito útil em filtro:

```python
postos[postos["Revenda"].str.contains("POSTO")]
```

### Substituir substring

```python
postos["Revenda"].str.replace("LTDA", "")        # remove "LTDA"
postos["Revenda"].str.replace(".", "")           # remove pontos
```

### Pegar caractere por posição

```python
postos["Municipio"].str[0]          # primeira letra de cada nome
postos["Municipio"].str[-3:]        # últimos 3 caracteres
postos["CNPJ"].str[1:15]            # do char 1 até o 14
```

### Quebrar (split)

```python
postos["Revenda"].str.split()                    # quebra por espaço, vira lista
postos["Revenda"].str.split(expand=True)         # quebra e vira DataFrame
postos["Revenda"].str.split().str[0]             # primeira palavra
postos["Revenda"].str.split().str[-1]            # última palavra
```

### Encadear (pipeline)

```python
postos["Revenda"].str.upper().str.replace("LTDA", "").str.strip()
```

Lê esquerda pra direita: maiúsculas, depois tira "LTDA", depois tira espaço. Cada etapa pega o resultado da anterior.

## 10. Estatísticas e contagens

### Em coluna numérica

```python
postos["Valor de Venda"].mean()         # média
postos["Valor de Venda"].median()       # mediana
postos["Valor de Venda"].std()          # desvio padrão
postos["Valor de Venda"].var()          # variância
postos["Valor de Venda"].min()
postos["Valor de Venda"].max()
postos["Valor de Venda"].sum()          # soma
postos["Valor de Venda"].count()        # qtd de valores não-nulos

postos["Valor de Venda"].quantile(0.25) # 1º quartil (25%)
postos["Valor de Venda"].quantile(0.75) # 3º quartil
```

Os parênteses no final são **obrigatórios**. Sem eles você não chama a função, recebe um objeto sem sentido.

### `describe()` (combo de tudo)

```python
postos["Valor de Venda"].describe()
```

Devolve em uma linha só:
- `count` (quantos)
- `mean` (média)
- `std` (desvio padrão)
- `min`
- `25%` (1º quartil)
- `50%` (mediana)
- `75%` (3º quartil)
- `max`

Pra DataFrame inteiro:

```python
postos.describe()                       # só colunas numéricas
postos.describe(include="all")          # inclui texto também
```

### Em coluna categórica (`value_counts`)

`value_counts` conta quantas vezes cada valor aparece. **Essencial pra dados categóricos** (bandeira, produto, município).

```python
postos["Bandeira"].value_counts()
```

Saída exemplo:
```
VIBRA              28473
BRANCA             19245
RAIZEN             12091
IPIRANGA            8123
...
```

Já vem ordenado decrescente.

Variações úteis:

```python
postos["Bandeira"].value_counts(normalize=True)   # em proporção (0 a 1)
postos["Bandeira"].value_counts(dropna=False)     # inclui nulos na contagem
postos["Bandeira"].value_counts().head(3)         # top 3
```

### `unique` e `nunique`

```python
postos["Bandeira"].unique()             # array de valores distintos
postos["Bandeira"].nunique()            # quantos valores distintos
postos["Municipio"].nunique()           # quantos municípios diferentes
```

## 11. Agrupamento (`groupby`)

Análogo direto: **tabela dinâmica do Excel**. Você define o critério (linhas da pivot), a coluna de valor, e a função de agregação (soma, média etc.).

### Estrutura mental

```
df.groupby(CRITÉRIO)[COLUNA].FUNÇÃO()
```

### Exemplos

```python
# Preço médio por município
postos.groupby("Municipio")["Valor de Venda"].mean()

# Preço médio por bandeira
postos.groupby("Bandeira")["Valor de Venda"].mean()

# Quantos postos por bandeira
postos.groupby("Bandeira").size()

# Quantos CNPJs distintos por município
postos.groupby("Municipio")["CNPJ"].nunique()
```

### Critério com várias colunas

```python
# Preço médio por município E produto
postos.groupby(["Municipio", "Produto"])["Valor de Venda"].mean()
```

Resultado fica com índice em dois níveis (Município no nível 1, Produto no nível 2).

### Funções aceitas

```python
.mean()    .sum()    .median()    .min()    .max()
.std()     .count()  .size()      .nunique()
.first()   .last()
```

`.size()` conta **linhas do grupo**. `.count()` conta **não-nulas numa coluna** (por isso precisa de `[col]` antes).

### Ordenar resultado do groupby

```python
postos.groupby("Bandeira")["Valor de Venda"].mean().sort_values(ascending=False)
```

Pega o resultado e ordena. Útil pra "top N" ou ranking.

### `agg` (múltiplas estatísticas de uma vez)

```python
postos.groupby("Bandeira").agg({
    "Valor de Venda": "mean",
    "CNPJ": "nunique",
})
```

Ou várias funções pra mesma coluna:

```python
postos.groupby("Bandeira").agg({
    "Valor de Venda": ["mean", "min", "max", "std"],
})
```

### `as_index=False`

Default: o critério do groupby vira **índice** do resultado. Se quiser ele como coluna normal:

```python
postos.groupby("Municipio", as_index=False)["Valor de Venda"].mean()
```

Vira DataFrame com índice 0,1,2... e Municipio como coluna comum.

### Combinando filtro + groupby

```python
# Preço médio de gasolina por município
postos[postos["Produto"] == "GASOLINA"].groupby("Municipio")["Valor de Venda"].mean()
```

Filtra primeiro, agrupa depois. Lê esquerda pra direita.

## 12. Juntando duas tabelas (`merge`)

Análogo: **PROCV no Excel** (mas mais poderoso, porque junta a tabela inteira de uma vez).

### Sintaxe básica

```python
pd.merge(left, right, on="chave", how="inner")
```

- `left` e `right` são os dois DataFrames.
- `on` é o nome da coluna que existe nos dois e serve de chave de junção.
- `how` é o tipo de junção (próxima subseção).

### Tipos de `how`

Imagina que o `left` tem chaves [A, B, C, E] e o `right` tem chaves [A, B, C, D].

| how | O que resulta |
|---|---|
| `inner` (default) | só A, B, C (intersecção) |
| `outer` | A, B, C, D, E (união, faltante vira NaN) |
| `left` | tudo do left: A, B, C, E |
| `right` | tudo do right: A, B, C, D |

Pra essa prova, `inner` é o que você vai usar quase sempre.

### Chave com várias colunas

```python
pd.merge(
    postos,
    distrib,
    on=["Municipio", "Produto", "Mes"],
    how="inner",
)
```

Quando a chave de junção é mais de uma coluna (caso desta prova), passa uma **lista**.

### Pegadinha gigante do merge

Se a chave de junção precisa de 3 colunas e você só passa 1, o pandas faz **produto cartesiano**. O resultado fica imenso (milhões de linhas). Se de repente o seu DataFrame ficou enorme depois do merge, é isso. Confere a chave.

### Conectando os dois datasets

Os dois datasets precisam de uma chave de junção em comum. `Municipio` e `Produto` já batem. Falta o **mês**: `distrib` tem `Mes` em `YYYY-MM`, mas `postos` tem `Data da Coleta` em `dd/mm/yyyy`. Precisa criar a coluna `Mes` no postos antes:

```python
# Cria Mes em postos no formato YYYY-MM
postos["Mes"] = postos["Data da Coleta"].str[6:10] + "-" + postos["Data da Coleta"].str[3:5]
```

O truque: `"01/01/2025"` tem o ano nas posições 6 a 10, e o mês nas posições 3 a 5. Junta as duas substrings com `-`.

Agora junta:

```python
juntos = pd.merge(
    postos,
    distrib,
    on=["Municipio", "Produto", "Mes"],
    how="inner",
)
```

Resultado: cada linha tem `Valor de Venda` (preço de revenda) **e** `Preco_Distribuicao` (preço de atacado) lado a lado.

```python
juntos["margem"] = juntos["Valor de Venda"] - juntos["Preco_Distribuicao"]
juntos.groupby("Bandeira")["margem"].mean().sort_values(ascending=False)
```

## 13. Conversões úteis que talvez precise

### 13.1 Criar coluna nova

```python
postos["Preco com imposto"] = postos["Valor de Venda"] * 1.1
postos["Pais"] = "Brasil"
postos["Cidade upper"] = postos["Municipio"].str.upper()
```

Se a coluna **não existe**, é criada. Se **já existe**, é substituída. Mesma sintaxe.

### 13.2 Converter tipo (`astype`)

```python
postos["Valor de Venda"] = postos["Valor de Venda"].astype(float)
postos["CNPJ"] = postos["CNPJ"].astype(str)
```

Útil quando o pandas leu uma coluna no tipo errado.

### 13.3 Quando o decimal não veio convertido

Se `Valor de Venda` aparecer como `object` (string) em vez de `float64`:

```python
postos["Valor de Venda"] = (
    postos["Valor de Venda"]
    .str.replace(",", ".")
    .astype(float)
)
```

### 13.4 Ordenar (`sort_values`)

```python
postos.sort_values("Valor de Venda")                  # crescente, NÃO altera o objeto
postos.sort_values("Valor de Venda", ascending=False) # decrescente
postos = postos.sort_values("Valor de Venda")         # PERSISTE (reatribui)
```

**Pegadinha:** `sort_values` sozinho só mostra o ordenado. Pra alterar o `postos`, você precisa reatribuir (`postos = postos.sort_values(...)`).

### 13.5 Tirar linhas duplicadas

```python
postos.drop_duplicates()                       # remove linhas 100% idênticas
postos.drop_duplicates(subset=["CNPJ"])        # único por CNPJ
```

### 13.6 Lidando com nulos

```python
postos.isnull().sum()              # quantos nulos por coluna
postos.dropna()                    # remove linhas com qualquer nulo
postos.dropna(subset=["Valor de Venda"])
postos.fillna(0)                   # preenche com 0
postos["col"].fillna("desconhecido")
```

### 13.7 Trocar valor inteiro (`replace`)

```python
postos["Bandeira"].replace("BRANCA", "SEM_BANDEIRA")
postos["Bandeira"].replace({"BRANCA": "SEM_BANDEIRA", "VIBRA": "BR"})
```

**Diferença chave:**
- `df["col"].replace("X", "Y")` troca o **valor inteiro** "X" por "Y".
- `df["col"].str.replace("X", "Y")` troca a **substring** "X" por "Y" dentro do texto.

## 14. Cenários completos (resolvidos com comentário)

Cada cenário cobre uma combinação típica. Lê os comentários, entende o porquê de cada linha.

### 14.1 Quantos postos distintos existem em SP capital?

```python
# 1. Filtra só linhas da capital
sp = postos[postos["Municipio"] == "SAO PAULO"]

# 2. Conta quantos CNPJs distintos (cada CNPJ é um posto físico)
sp["CNPJ"].nunique()
```

### 14.2 Preço médio de gasolina por bandeira (do mais caro pro mais barato)

```python
# 1. Filtra só gasolina
gas = postos[postos["Produto"] == "GASOLINA"]

# 2. Agrupa por bandeira, tira média do preço
# 3. Ordena decrescente
gas.groupby("Bandeira")["Valor de Venda"].mean().sort_values(ascending=False)
```

### 14.3 Top 5 municípios com etanol mais caro (média)

```python
# 1. Filtra etanol
et = postos[postos["Produto"] == "ETANOL"]

# 2. Agrupa, tira média, ordena, pega 5 primeiros
et.groupby("Municipio")["Valor de Venda"].mean().sort_values(ascending=False).head(5)
```

### 14.4 Quantas coletas existem de cada produto?

```python
postos["Produto"].value_counts()
```

### 14.5 Distribuição completa de preços por produto

```python
postos.groupby("Produto")["Valor de Venda"].describe()
```

Saída traz `count`, `mean`, `std`, `min`, 25%, 50%, 75%, `max` pra cada um dos 3 produtos.

### 14.6 Postos cuja razão social tem "AUTO POSTO" e cuja bandeira é VIBRA

```python
cond1 = postos["Revenda"].str.contains("AUTO POSTO")
cond2 = postos["Bandeira"] == "VIBRA"
postos[cond1 & cond2]
```

### 14.7 Preço médio mês a mês da gasolina em SP capital

```python
# 1. Filtra: só gasolina E só SP capital
gas_sp = postos[
    (postos["Produto"] == "GASOLINA") & (postos["Municipio"] == "SAO PAULO")
].copy()

# 2. Cria coluna Mes (formato YYYY-MM)
gas_sp["Mes"] = gas_sp["Data da Coleta"].str[6:10] + "-" + gas_sp["Data da Coleta"].str[3:5]

# 3. Agrupa por mês, tira média
gas_sp.groupby("Mes")["Valor de Venda"].mean()
```

`.copy()` é uma boa prática pra evitar warning quando você cria coluna num DataFrame que veio de filtro.

### 14.8 Margem média (preço de revenda menos atacado) por bandeira

```python
# 1. Cria Mes em postos pra poder juntar
postos["Mes"] = postos["Data da Coleta"].str[6:10] + "-" + postos["Data da Coleta"].str[3:5]

# 2. Junta as duas tabelas pela chave tripla
juntos = pd.merge(
    postos,
    distrib,
    on=["Municipio", "Produto", "Mes"],
    how="inner",
)

# 3. Calcula a margem (revenda - atacado)
juntos["margem"] = juntos["Valor de Venda"] - juntos["Preco_Distribuicao"]

# 4. Agrupa por bandeira, tira média, ordena
juntos.groupby("Bandeira")["margem"].mean().sort_values(ascending=False)
```

### 14.9 Municípios onde o maior preço de gasolina passou de R$ 7,00

```python
# 1. Só gasolina
g = postos[postos["Produto"] == "GASOLINA"]

# 2. Pra cada município, pega o MAIOR preço observado
mais_cara = g.groupby("Municipio")["Valor de Venda"].max()

# 3. Filtra só os que ficaram acima de 7
mais_cara[mais_cara > 7]
```

Repara que dá pra filtrar uma Series do mesmo jeito que filtra um DataFrame.

### 14.10 Quantas bandeiras diferentes operam em cada município (top 10)

```python
postos.groupby("Municipio")["Bandeira"].nunique().sort_values(ascending=False).head(10)
```

### 14.11 Preço médio dos postos "BRANCA" por produto

```python
brancas = postos[postos["Bandeira"] == "BRANCA"]
brancas.groupby("Produto")["Valor de Venda"].mean()
```

### 14.12 Município com diesel S10 mais caro

```python
# 1. Filtra diesel
d = postos[postos["Produto"] == "DIESEL S10"]

# 2. Média por município
med = d.groupby("Municipio")["Valor de Venda"].mean()

# 3. Município com maior valor
med.idxmax()        # nome do município
med.max()           # valor médio
```

`.idxmax()` devolve o **rótulo** (município neste caso) onde o valor é máximo.

### 14.13 Bandeira mais frequente em SP capital

```python
postos[postos["Municipio"] == "SAO PAULO"]["Bandeira"].value_counts().head(1)
```

### 14.14 Mês em que gasolina foi mais cara em média

```python
g = postos[postos["Produto"] == "GASOLINA"].copy()
g["Mes"] = g["Data da Coleta"].str[6:10] + "-" + g["Data da Coleta"].str[3:5]
g.groupby("Mes")["Valor de Venda"].mean().idxmax()
```

## 15. Cola A4 (imprimir e levar)

Versão comprimida pra consulta rápida. Tudo o que você precisa cabe nesta seção.

### Imports e leitura

```python
import pandas as pd

df = pd.read_csv("arquivo.csv", sep=";", decimal=",")
```

### Inspeção

```python
df.head(5)    df.tail()    df.sample(5)    df.shape    df.info()
df.columns    df.dtypes    df.describe()    len(df)
```

### Seleção

```python
df["col"]                 # Series (1 col)
df[["a","b"]]             # DataFrame (várias cols)
df.loc[5]                 # linha por nome
df.loc[5:10]              # linhas 5 a 10 (INCLUSIVO no fim)
df.loc[cond, "col"]       # filtro + coluna
df.iloc[0]                # linha por posição
df.iloc[0:5, 0:3]         # fim EXCLUSIVO
```

### Filtros (& | ~, cada cond entre parênteses)

```python
df[df["x"] == "A"]
df[df["x"] > 5]
df[(df["x"]==1) & (df["y"]>2)]      # AND
df[(df["x"]==1) | (df["y"]>2)]      # OR
df[~(df["x"]==1)]                   # NOT
df[df["x"].isin(["A","B"])]
len(df[df["x"]==1])                 # quantas linhas
```

### String (.str sempre antes)

```python
df["c"].str.upper()    .lower()    .title()    .strip()    .len()
df["c"].str.contains("x")    .startswith("x")    .endswith("x")
df["c"].str.replace("a","b")
df["c"].str[0]    .str[-3:]    .str[1:5]
df["c"].str.split()    .split(expand=True)    .split().str[-1]
```

### Conversões e edição

```python
df["c"].replace("A","B")                 # valor inteiro
df["c"].astype(float)                    # converte
df.drop_duplicates(subset=["c"])
df.sort_values("c", ascending=False)     # REATRIBUI pra persistir
df["c"].unique()    .nunique()
df.isnull().sum()    df.dropna()    df.fillna(0)
df["nova"] = df["a"] + df["b"]           # cria coluna
```

### Estatística

```python
df["c"].value_counts()    .value_counts(normalize=True)    .head(5)
df["c"].mean()    .median()    .std()    .var()
df["c"].min()     .max()       .sum()    .count()
df["c"].quantile(0.25)    .quantile([.25, .5, .75])
df["c"].describe()
df.describe()    df.describe(include="all")
```

### groupby

```python
df.groupby("c")["v"].mean()
df.groupby(["c1","c2"])["v"].sum()
df.groupby("c")[["v1","v2"]].mean()
df.groupby("c", as_index=False)["v"].mean()
df.groupby("c").agg({"v":"mean", "x":["min","max"]})
df.groupby("c").size()              # qtd linhas por grupo
df.groupby("c")["v"].nunique()
df.groupby("c")["v"].mean().sort_values(ascending=False)
df.groupby("c")["v"].mean().idxmax()    # rótulo do máximo
```

### merge

```python
pd.merge(L, R, on="k", how="inner")
pd.merge(L, R, on=["k1","k2"], how="inner")
pd.merge(L, R, left_on="A", right_on="B", how="left")
```

how: `inner` (default), `outer`, `left`, `right`.

### Data dd/mm/yyyy → YYYY-MM

```python
df["Mes"] = df["Data"].str[6:10] + "-" + df["Data"].str[3:5]
```

### Pegadinhas garantidas

- `sort_values` **não persiste sozinho**, reatribui.
- Operadores são `&` `|` `~`, nunca `and` `or` `not`.
- Cada condição **entre parênteses** em filtro composto.
- `.str` é **obrigatório** antes de função de string.
- `loc` é **obrigatório** quando filtra linha E seleciona coluna.
- `loc` fim **inclusivo**, `iloc` fim **exclusivo**.
- `df["c"]` retorna **Series** (1D); `df[["c"]]` retorna **DataFrame** (2D).
- Merge com chave incompleta vira **produto cartesiano**.
- `df.shape` é atributo, **sem parênteses**.
- `df["c"].mean` (sem `()`) retorna bound method, não o valor.
- `==` compara, `=` atribui. Errar é clássico.

## 16. Setup pronto da primeira célula

Cole isso na primeira célula do notebook da avaliação:

```python
import pandas as pd

# === LEITURA ===
postos = pd.read_csv("postos_sp_2025.csv", sep=";", decimal=",")
distrib = pd.read_csv("distribuicao_municipios_sp_2025.csv", sep=";", decimal=",")

# === LIMPEZA ===
postos["CNPJ"] = postos["CNPJ"].str.strip()
postos["Mes"] = postos["Data da Coleta"].str[6:10] + "-" + postos["Data da Coleta"].str[3:5]

# === CONFERE ===
print("postos:", postos.shape)
print("distrib:", distrib.shape)
postos.head()
```

Roda essa célula uma vez no começo. Daí em diante você só escreve as perguntas.

## 17. Fluxo durante a prova (100 min)

1. **Min 1 a 5:** lê todas as perguntas antes de tocar em código. Anota mentalmente cada uma (filtro? groupby? merge?).
2. **Min 5 a 10:** roda o setup da seção 16. Confere `shape` e `head`. Se `Valor de Venda` veio como string, faz a conversão da seção 13.3 já.
3. **Min 10 a 50:** resolve as fáceis primeiro (`value_counts`, `mean`, filtro simples). Trava pontos.
4. **Min 50 a 80:** resolve as combinadas (filtro + groupby, merge, encadeamento).
5. **Min 80 a 85:** revisa o notebook inteiro, confere se as células rodam em ordem (Kernel → Restart and Run All).
6. **Min 85 a 100:** eClass abre. Representante preenche o questionário com as respostas, sobe o `.ipynb`, confere o nome completo dos 3 membros do grupo.

### Dicas operacionais

- **Salva o notebook a cada exercício** (Cmd+S). Se o Jupyter travar, não perde.
- **Roda cada célula isolada antes de partir pra próxima.** Erro em célula não diagnosticado vira bola de neve.
- **Quando der erro, lê a ÚLTIMA linha do traceback.** É onde o pandas te diz o que houve.
- Erros mais comuns:
  - `KeyError: 'col'` → nome de coluna errado (case, espaço, acento).
  - `TypeError` em operação aritmética → coluna é string, precisa converter com `astype(float)`.
  - `AttributeError: 'Series' object has no attribute 'upper'` → esqueceu o `.str`.
  - DataFrame gigante depois de merge → faltou coluna na chave.

## Pra fixar

- [[Pandas]], [[DataFrame]], [[loc]], [[iloc]], [[Fatiamento lógico]]
- [[str accessor]], [[str.contains]], [[str.replace]], [[astype]]
- [[value_counts]], [[describe]], [[Quartil]]
- [[groupby]], [[agg]], [[merge]], [[Inner join]], [[Outer join]], [[Left join]], [[Right join]], [[Chave de juncao]]
