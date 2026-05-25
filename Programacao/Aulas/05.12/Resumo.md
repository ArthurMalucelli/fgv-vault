---
materia: Programacao
data: 2026-05-12
tema: Indexação avançada, str accessor e criação de colunas em Pandas
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[loc]] | Indexa por **label** (nome). Range é **inclusivo** no fim |
| [[iloc]] | Indexa por **posição numérica**. Range é **exclusivo** no fim (igual lista Python) |
| Coluna booleana | Pode ser usada direto: `df[df["col"]]` sem precisar `== True` |
| [[str accessor]] | `.str` distribui função ou indexação string em **todos** os elementos da coluna |
| Criação de coluna | `df["nova"] = expressão`. Cria à direita da última. Igual define ou substitui |
| Operação aritmética em coluna | `df["nova"] = df["pontos"] + 3` aplica em todas as linhas |
| [[DataFrame vazio]] | Filtro sem match retorna DataFrame com colunas mas **0 linhas**. Não é erro |
| Display | `display(x)` força mostrar resultado intermediário no Jupyter (senão só mostra o último) |

## Slicing loc vs iloc — pegadinha clássica

```python
df.loc[5:10]    # INCLUI a linha 10 (vai do 5 ao 10 inclusivo)
df.iloc[5:11]   # vai do 5 ao 10 (exclusivo no 11, igual Python)
```

`loc` é por label e inclui as duas pontas. `iloc` é por posição e segue a regra do Python (último é exclusivo).

## Fatiamento com lógica e coluna ao mesmo tempo

Forma canônica do `loc`: `df.loc[linha, coluna]`.

```python
df.loc[df["capital"], "população"].mean()
```

- `df["capital"]` retorna booleano (true/false por linha).
- `df.loc[boolean, "população"]` retorna a coluna "população" só das linhas onde capital é true.
- `.mean()` agrega.

Como precisa selecionar linha **e** coluna ao mesmo tempo, é obrigatório usar `loc` (ou `iloc`).

## Operadores lógicos pandas — recap

| Op | Símbolo |
|---|---|
| AND | `&` |
| OR | `\|` |
| NOT | `~` |

Cada condição **entre parênteses** quando combinada:

```python
df[(df["UF"] == "RJ") & (df["capital"] == False)]
df[(df["UF"] == "RJ") & ~df["capital"]]              # equivalente
```

Como a coluna `capital` já é booleana, posso usar direto sem `== False/True`.

## str accessor

```python
times["Time"].str.upper()    # tudo maiúsculo
times["Time"].str.lower()    # tudo minúsculo
times["Time"].str[0]          # primeiro caractere de cada string
times["Time"].str[-1]         # último caractere
times["Time"].str[-5:]        # últimos 5 caracteres
times["Time"].str.split()     # separa por espaço, vira lista
times["Time"].str.len()       # quantidade de caracteres
```

Regra: tudo que vem à direita do `.str` (função ou indexação) é distribuído em **cada string** da coluna. Sem o `.str`, tentar `df["col"].upper()` ou `df["col"][0]` dá erro ou retorna coisa que não é o que você quer.

## Criação de coluna

```python
times["Inicial"] = times["Time"].str[0]      # coluna derivada
times["País"] = "Brasil"                      # coluna constante
times["Pontos prox"] = times["Pontos"] + 3    # operação aritmética
```

- Se a coluna **não existe**: cria nova à direita da última.
- Se a coluna **já existe**: substitui o conteúdo.
- O `=` no pandas tem esse duplo papel.

## Validação de login — padrão de uso

Padrão que pode cair na prova: usar uma filtragem lógica + `len` para checar existência.

```python
resultado = df[df["username"] == username]

if len(resultado) == 0:
    print("Username não existe")
else:
    # username existe, partir pra próxima checagem
    ...
```

Por quê funciona: `df[df["username"] == "Getulio"]` retorna um [[DataFrame vazio]] (0 linhas com as colunas originais) quando não há match. `len(dataframe)` é a quantidade de linhas. Zero linhas → não existe.

## Drop de coluna (não cai na prova)

```python
times = times.drop("País", axis=1)
```

Removido conteúdo da aula. Reatribui pra persistir.

## Pegadinhas / pontos de prova

- `df["col"].mean()` precisa dos **parênteses**. Sem parênteses retorna `bound method`, não o valor.
- Em `.loc`, range é **inclusivo no fim**. Em `.iloc`, **exclusivo** (igual Python). Errar isso fora-by-one.
- Operadores são `&`, `|`, `~`. **Não** `and`, `or`, `not`.
- Cada condição **entre parênteses**: `df[(c1) & (c2)]`.
- Coluna já booleana **dispensa** `== True`: `df[df["capital"]]` funciona.
- Filtro sem match → [[DataFrame vazio]] (não erro). `len(...) == 0` é o teste de existência.
- `display()` força mostrar resultado intermediário. Sem ele, célula só exibe a última expressão.
- Operação aritmética em coluna exige coluna **numérica**. Se for string, não soma.
- Quando der erro, ler a **última linha** do traceback.

## NÃO cai na prova (professor falou)

- `df.drop()`.
- Slicing avançado tipo `str[-5:]`.
- O caso de `.loc` em atribuição diminuir a quantidade de linhas e gerar `NaN`.
- O exercício de validação de login como tá. Mas o **padrão de uso** (`len` + filtro lógico) pode cair.

## Pra fixar

- [[loc]]
- [[iloc]]
- [[str accessor]]
- [[Fatiamento lógico]]
- [[DataFrame vazio]]

## Próxima aula

Quiz da **aula 16** com arquivo `tips.csv` e notebook `tips.ipynb`. Baixar os dois e abrir no Jupyter.
