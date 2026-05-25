---
materia: Programacao
data: 2026-05-14
tema: Pandas — value_counts, str accessor avançado, condições compostas, describe
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[value_counts]] | Distribuição de coluna categórica. `df["col"].value_counts()` retorna contagem por categoria |
| [[Variavel categorica nominal]] | Sem ordem. Ex: M/F, RJ/SP/MG |
| [[Variavel categorica ordinal]] | Com ordem. Ex: pequeno/médio/grande, classes A-E IBGE |
| `del df["col"]` | Apaga coluna (alternativa ao método visto na aula anterior) |
| [[astype]] | Converte tipo da coluna inteira: `df["id"].astype(str)` |
| [[str.contains]] | Booleano por linha: tem o substring ou não. `df["email"].str.contains("fgv.br")` |
| [[str.replace]] | Substitui substring. Pode encadear: `.str.replace("F","FM").str.replace("M","MM")` |
| `str.split(expand=True)` | Sem `expand`: lista por linha. Com: DataFrame com uma coluna por elemento |
| `str.split().str[-1]` | Último elemento depois do split (ex: sobrenome) |
| [[describe]] | Estatísticas resumo: média, std, min, max, 25%, 50%, 75% |
| [[Quartil]] | 25% = primeiro quartil, 50% = mediana, 75% = terceiro quartil |
| [[Notacao cientifica]] | `1e6` = 10⁶ = milhão; `1e9` = bilhão. Equivalente a `10**6` |
| Underscore em número | `10_000_000` = `10000000`. Convenção opcional de legibilidade |

## Filtro booleano, recap denso

```python
# Maneira inline
df[df["gender"] == "F"]

# Maneira com variável temporária (mais legível)
cond = df["gender"] == "F"
df[cond]

# Contagem
len(df[df["gender"] == "F"])

# Equivalente para coluna categórica:
df["gender"].value_counts()
```

## str accessor avançado

```python
df["col"].str.contains("xyz")        # booleano por linha
df["col"].str.replace("a", "b")      # substitui
df["col"].str.upper()                # maiúsculo
df["col"].str.lower()                # minúsculo
df["col"].str.swapcase()             # inverte case
df["col"].str.len()                  # quantidade de caracteres
df["col"].str.split()                # separa por espaço, vira lista
df["col"].str.split(expand=True)     # vira DataFrame com coluna por elemento
df["col"].str.split().str[-1]        # último elemento do split
```

**Pipeline (encadeamento)**: se uma função `.str.*` retorna algo do mesmo tipo, dá pra encadear. Cada chamada é input da próxima:

```python
df["gender"].str.replace("F","FM").str.replace("M","MM")
# resultado: F vira FM, M vira MM, simultaneamente
```

## Reatribuir coluna existente vs criar nova

```python
df["nova"] = expressao              # cria nova à direita
df["existente"] = expressao         # substitui conteúdo da existente
```

Mesma sintaxe. Se o nome já existe, é substituição; se não, é criação.

## Condição composta — & (and) e | (or)

```python
cond1 = df["col_a"].str.contains("CDI")
cond2 = df["col_a"].str.contains("IMAB")
df[cond1 | cond2]    # OR: linha entra se atender qualquer uma

cond3 = df["col_b"] > 1000
df[cond1 & cond3]    # AND: precisa atender as duas
```

Usar variáveis temporárias para cada condição é mais legível do que jogar tudo numa expressão única com parênteses aninhados. Lembrar: cada condição **entre parênteses** quando combinada na mesma linha.

## Concatenar string com coluna numérica

Não funciona direto:

```python
"C" + df["id"]    # erro: id é número
```

Solução, converte com [[astype]]:

```python
df["id"] = df["id"].astype(str)
"C" + df["id"]    # ok
```

## Soma de colunas numéricas

```python
df["soma"] = df["a"] + df["b"]    # linha a linha
```

Para fazer isso, o Pandas roda um `for` embutido. Você não escreve `for`, `if`, `while`, `else` ao trabalhar com Pandas — está tudo embutido nos métodos.

## describe e percentis

```python
df["col_numerica"].describe()
```

Retorna:
- `count`: quantidade
- `mean`: média
- `std`: desvio padrão
- `min`: mínimo
- `25%`: primeiro quartil
- `50%`: mediana
- `75%`: terceiro quartil
- `max`: máximo

## .loc para seleção linha + coluna

Quando precisa filtrar linhas E selecionar uma coluna específica, obrigatório usar [[loc]]:

```python
df.loc[df["x"] == 1000, "nome"]
# linhas onde x==1000, só a coluna "nome"
```

Sem `loc`, `df[df["x"] == 1000]` retornaria todas as colunas.

## Exercício de prova — fundos de investimento (laminas)

| Letra | O que pede | Como faz |
|---|---|---|
| A | Mediana do investimento inicial mínimo | `df["investe inicial mínimo"].median()` → R$ 1.000 |
| B | Fundos com inv. inicial = mediana | `laminas_cel = laminas[laminas["investe inicial mínimo"] == M]` |
| C | Dentre B, os que têm "CDI" ou "IMAB" no índice de referência | duas conds com `\|`, filtra sobre `laminas_cel` |
| D | Média do patrimônio líquido em bilhões | `laminas_cel2["pl"].mean() / 1e9` |

```python
# A
M = laminas["investe inicial mínimo"].median()

# B
laminas_cel = laminas[laminas["investe inicial mínimo"] == M]

# C
cond1 = laminas_cel["índice de referência"].str.contains("CDI")
cond2 = laminas_cel["índice de referência"].str.contains("IMAB")
laminas_cel2 = laminas_cel[cond1 | cond2]

# D
media_pl_bilhoes = laminas_cel2["patrimônio líquido"].mean() / 1e9
```

## Pegadinhas / pontos de prova

- **`str.contains` vs `==`**: contains acha substring (`"CDI 100%"` casa com `"CDI"`); `==` exige igualdade exata. Cuidado com sobreposição: `CDI` inclui `CDI 100%`.
- **Sem `.str`**: `df["col"].upper()` dá erro ou comportamento errado. Sempre precisa do `.str` antes de função de string.
- **astype antes de concatenar**: número + string sempre quebra, converter primeiro.
- **`loc` é obrigatório** quando filtra linha E seleciona coluna específica.
- **Operadores lógicos**: `&` (AND), `|` (OR), `~` (NOT). Cada condição entre parênteses quando combinada.
- **Notação científica**: `1e9` = 1 bilhão. `1e6` = 1 milhão. `4e12` = 4 trilhões. Usar para dividir números grandes.
- **Underscore em número**: `10_000_000` é só legibilidade, equivale a `10000000`. Python ignora os `_`.
- **Encadeamento**: se função retorna mesmo tipo, dá pra encadear infinito. `.str.replace().str.replace().str.upper()` funciona.
- **`expand=True` em split**: muda saída de "lista por linha" para "DataFrame com colunas".

## Pra fixar

- [[value_counts]]
- [[Variavel categorica nominal]]
- [[Variavel categorica ordinal]]
- [[astype]]
- [[str.contains]]
- [[str.replace]]
- [[describe]]
- [[Quartil]]
- [[Notacao cientifica]]
- [[loc]]
- [[Mediana]]

## Próxima aula

Dataset de 100 clubes de futebol com maior market cap. Coluna de market cap vem como string com sufixo `M` (milhão) e `B` (bilhão). Vai precisar lógica para converter em número (`M → ×1e6`, `B → ×1e9`) antes de fazer estatística.

## Lembrete de prova

Prova final permite trazer **uma folha A4 de anotações**. Não decora função, anota.
