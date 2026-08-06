---
materia: Programacao
data: 2026-05-19
tema: Agrupamento e junção de dados com Pandas — merge, groupby, pivot_table, unstack, plot
topicos: [merge, groupby, pivot_table, unstack, agg, inner join, outer join, chave de juncao, plot]
tags: [aula, transcrito]
---

## Aviso da atividade de valor em grupo

Quinta-feira (21/05) tem mais uma aula, é o momento de tirar dúvidas. Na terça-feira que vem (26/05) é a atividade de valor: um trabalho em grupo no formato de prova. Os professores decidiram fazer diferente dos semestres anteriores: vai ser "como se fosse uma prova em grupo", três alunos no máximo (pode ter grupo de dois), sem consulta. Não é a prova final em si, ela vem depois.

A sugestão é que cada grupo ocupe um computador no meio da bancada (cada oficina tem seis computadores). O arquivo de dados vai ser publicado até amanhã (20/05). As perguntas, obviamente, não vão ser compartilhadas. Tragam dúvidas na aula de quinta.

## Merge — junção de DataFrames

A primeira operação da aula é o `merge`, no contexto de junção de dados. A ideia é pegar dois [[DataFrame]]s e juntar eles através de uma coluna em comum.

Repare aqui: o DataFrame `dados` tem uma coluna `produto` (A, B, C) com quantidades e preços. Existe um segundo DataFrame `dados_complementares` que tem `produto` e `categoria` (X, Y, X). Quero criar uma coluna adicional à direita do primeiro DataFrame onde puxo a categoria correspondente, baseado no produto.

Ou seja: estou fazendo uma junção desses dois DataFrames usando como critério a coluna `produto`. Essa coluna é o que chamo de **chave** (em inglês, *key*). É o que une os dois lados.

Em Excel, isso seria um `PROCV` (e depois arrastar).

Em Pandas:

```python
pd.merge(dados, dados_complementares, on="produto", how="inner")
```

Os primeiros dois argumentos são os dois DataFrames. O primeiro é chamado de **left** (DataFrame da esquerda), o segundo é o **right** (DataFrame da direita). O próximo argumento é qual critério vou usar para juntar (`on="produto"`). E o último, `how="inner"`, é o tipo de junção.

Resultado: apareceu exatamente como esperava. Foi criada uma coluna `categoria` à direita, com o valor correspondente puxado do `dados_complementares`.

## Chave dupla (lista de colunas em `on`)

Agora um caso mais complexo. Tenho `df_vendas` (com data, produto, quantidade, preço, total, método de envio, tempo de envio, região) e `df_custo_envio` (três colunas: método de envio, região, custo de envio).

Quais são as chaves dos dois lados? São duas colunas comuns: `método de envio` e `região`. A chave agora é dupla, não única.

Preciso ver a coincidência das duas colunas ao mesmo tempo. Padrão + Sul casa com Padrão + Sul, e aí transporto o valor 20 do custo de envio para a linha correspondente.

```python
df_final = pd.merge(
    df_vendas,
    df_custo_envio,
    on=["método de envio", "região"],
    how="inner"
)
```

Antes eu tinha uma coluna em `on`, agora tem uma lista com duas colunas. O `how` continua `inner` (que é o default).

## Tipos de junção (how)

O `how` define o que fazer com as chaves que não casam:

- **[[Inner join]]** (default): só linhas onde a chave existe nos dois lados. É a intersecção entre os conjuntos de chaves.
- **[[Outer join]]**: união. Pega todas as chaves dos dois lados. Onde não tiver correspondência, preenche com vazio (NaN).
- **[[Left join]]**: todas as chaves do `left`, mais o que casar do `right`. Chaves que só existem no right somem.
- **[[Right join]]**: o contrário. Todas as chaves do `right`, mais o que casar do `left`.

Exemplo: se `left` tem produtos A, B, C, E e `right` tem A, B, C, D:

- `inner` → A, B, C (só intersecção)
- `outer` → A, B, C, D, E (união; D e E entram com vazio do outro lado)
- `left` → A, B, C, E
- `right` → A, B, C, D

É teoria de conjuntos aplicada a junção. Se você só usa chave única, dá pra pensar bidimensionalmente; com chave dupla, é a combinação que tem que casar.

Atenção a uma sutileza: se você junta com **menos colunas do que deveria**, o Pandas vai gerar todas as combinações possíveis. Exemplo: se eu fizesse `merge` só pelo método de envio (sem a região), ele ia tentar casar Expresso da esquerda com todas as linhas Expresso da direita, criando um produto cartesiano. Aí o DataFrame final fica muito maior do que deveria.

## groupby — agregação por critério

Agora o agrupamento. A ideia é a mesma da tabela dinâmica do Excel.

No Excel, eu arrasto `produto` para `rows`, `quantidade` para `values` e somo. Resultado: quantidade total por produto.

Em Pandas:

```python
df_final.groupby("produto")["quantidade"].sum()
```

Quebrando em três partes:

1. `groupby("produto")` — função (parênteses). Define o critério de agrupamento.
2. `["quantidade"]` — colchetes. É **seleção** de coluna, não argumento da função.
3. `.sum()` — função de agregação.

**Cuidado para não confundir parênteses com colchetes**:

- Parênteses → função (`groupby(...)`).
- Colchetes → seleção de coluna (`df["x"]`).

Resultado:

```
produto
A    18
B    11
C    10
```

São 39 unidades no total.

## groupby com múltiplos critérios

Se quero agrupar por mais de um critério, passa uma lista:

```python
df_final.groupby(["método de envio", "região"])["quantidade"].sum()
```

Resultado:

```
método de envio  região
Expresso         Leste     28
                 Norte     10
                 Oeste     12
Padrão           Sul       10
```

Esse objeto tem **dois níveis de índice** (método de envio como nível 0, região como nível 1) e uma coluna de valor. O Pandas omite a repetição do primeiro nível na visualização (só mostra `Expresso` uma vez), mas internamente cada linha tem os dois índices.

Se você omitir a seleção de coluna (`["quantidade"]`), o `groupby` vai tentar somar **todas** as colunas. Algumas não são numéricas (data, por exemplo) e o Pandas ignora, mas as numéricas todas entram na soma. Por isso o colchete: você restringe quais colunas quer agregar.

Se quer mais de uma coluna, dois colchetes (colchete externo + lista):

```python
df_final.groupby("produto")[["quantidade", "total de vendas"]].sum()
```

O colchete externo é "seleção", e o de dentro é a lista de colunas. Se você passa uma coluna só com dois colchetes, o resultado é um [[DataFrame]] com uma coluna; com um colchete só, é uma Series (uma dimensão).

## Filtro + groupby encadeado

Dá pra encadear seleção de linhas com agrupamento:

```python
df_final[df_final["quantidade"] > 8].groupby("produto")["quantidade"].sum()
```

Aqui:

- `df_final[df_final["quantidade"] > 8]` — seleciona só linhas onde quantidade > 8.
- `.groupby("produto")["quantidade"].sum()` — agrupa essa seleção menor.

O groupby age sobre a seleção, não sobre o DataFrame original. Quando você vê uma expressão dessas, leia da **esquerda para a direita** em etapas.

Pra ficar mais legível, programadores escrevem em múltiplas linhas, envolvido em parênteses:

```python
(
    df_final[
        (df_final["método de envio"] == "Expresso")
        & (df_final["quantidade"] > 8)
    ]
    .groupby("produto")["quantidade"]
    .sum()
)
```

Tem que envolver com parênteses externos (`(` e `)`) para o Python entender que é uma expressão única quebrada em várias linhas.

Outra opção (a mais limpa) é definir variáveis temporárias para cada condição:

```python
cond1 = df_final["método de envio"] == "Expresso"
cond2 = df_final["quantidade"] > 8
df_final[cond1 & cond2].groupby("produto")["quantidade"].sum()
```

## agg — múltiplas funções, múltiplas colunas

Se quero somar uma coluna e calcular a média de outra **na mesma operação**, uso `agg` com um dicionário:

```python
df_final.groupby("método de envio").agg({
    "quantidade": "sum",
    "total de vendas": "mean"
})
```

Dicionário (`{}`, chaves) com: nome da coluna como chave, função de agregação como valor.

Se quero múltiplas funções para a **mesma coluna**, passa uma lista:

```python
df_final.groupby("método de envio").agg({
    "quantidade": ["mean", "min"],
    "preço unitário": "median"
})
```

## unstack — empilhar índice como coluna

O resultado de um `groupby` com dois critérios fica vertical. Às vezes quero ver a coisa em formato de matriz, com um critério na linha e outro na coluna. No Excel, é arrastar `região` para columns em vez de rows.

Em Pandas, esse rearranjo se chama **[[unstack]]**:

```python
df_final.groupby(["método de envio", "região"])["quantidade"].sum().unstack()
```

Resultado:

```
região           Leste  Norte  Oeste  Sul
método de envio
Expresso         28     10     12     NaN
Padrão           NaN    NaN    NaN    10
```

Por default, `unstack()` pega o **último nível** do índice (nível -1) e joga para coluna. Se quero o primeiro nível, passa o índice (`unstack(0)`) ou o nome do nível (`unstack("método de envio")`).

## as_index=False — converter índice em coluna

Quando você faz `groupby`, por default os critérios de agrupamento viram índice do resultado. Se quer que voltem a ser colunas normais:

```python
df_final.groupby(
    ["método de envio", "região"],
    as_index=False
)["quantidade"].sum()
```

Resultado: em vez do índice multi-nível, vira um DataFrame com `método de envio` e `região` como colunas normais e um índice numérico (0, 1, 2...).

## pivot_table — tabela dinâmica do Excel

`pivot_table` é a tradução direta da tabela dinâmica do Excel. Tem quatro argumentos principais e cada um corresponde a um quadrante do Excel:

| Excel | pivot_table |
|---|---|
| rows (linhas) | `index` |
| columns | `columns` |
| values | `values` |
| função de agregação | `aggfunc` |

```python
df_final.pivot_table(
    index="região",
    columns="método de envio",
    values="quantidade",
    aggfunc="sum"
)
```

Pode usar várias funções: `sum`, `mean`, `median`, `count`, `max`, `min`, `std` (desvio padrão), entre outras.

Pra adicionar linha e coluna de total, passa `margins=True`:

```python
df_final.pivot_table(
    index="região",
    columns="método de envio",
    values="quantidade",
    aggfunc="sum",
    margins=True
)
```

`groupby` e `pivot_table` fazem coisas parecidas, são duas alternativas. Preferência é minha. Pra alguns casos, `pivot_table` é mais legível porque mapeia 1-pra-1 com o Excel.

## sort_values em groupby

O resultado de `groupby` vem ordenado pelo índice, em ordem alfabética. Se quero ordenar pelo valor (a quantidade somada, por exemplo), encadeo `sort_values`:

```python
df_final.groupby("método de envio")["quantidade"].sum().sort_values(ascending=False)
```

Quando ordena pelo valor, perde-se a sequência do índice (pode bagunçar o multi-nível). Quando o índice repete, o Pandas omite o nome a partir da segunda ocorrência.

## Plot — visualização direta

Pandas tem método `plot` que chama o matplotlib por baixo:

```python
df.plot(
    x="data",
    y="quantidade",
    kind="line",
    marker="o",
    title="Quantidade por data",
    xlabel="data",
    ylabel="quantidade"
)
```

Tipos comuns de gráfico (`kind`):

- `line` — linha
- `bar` — barras
- `pie` — pizza
- `hist` — histograma

`marker` controla o símbolo dos pontos: `"o"` (círculo), `"."` (ponto pequeno), `"x"`, `"--"` (tracejado).

Se quero múltiplas séries no eixo Y, passa uma lista:

```python
df.plot(x="data", y=["quantidade", "preço"], kind="line")
```

Cada série entra com sua legenda automaticamente.

## Encerramento

Esse foi o último conteúdo do curso. Quinta-feira (21/05) é aula de dúvidas; terça (26/05) é a atividade de valor em grupo.
