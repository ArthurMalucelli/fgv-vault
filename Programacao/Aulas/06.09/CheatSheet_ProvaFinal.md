---
tipo: resumo
materia: Programacao
data: 2026-06-09
tema: Padrões da prova final (Fundamentos de Programação)
tags: [resumo, prova, cheatsheet, programacao]
---

# Cheat Sheet, Prova Final de Programação

Base: 3 finais individuais (`FinalFunProg202501`, `FinalFunProg202502`, `prova_simulado_202502`) + o gabarito da atividade em grupo (`AGP2025_GABARITO`, análise de dados), todos na mesma pasta. O professor sinalizou que a final pode ser **mista**: programação básica E análise de dados. Por isso o sheet tem duas camadas: os **5 arquétipos** dos finais (Q1 a Q5) e um **bloco extra de pandas-análise** (estilo AGP). Domine os moldes e você fecha. Este arquivo é gabarito de **padrão**, não de resposta: treine resolvendo sozinho.

## Mapa de pontos (onde investir tempo)

| Questão | Tipo | Pontos | Pontuação parcial? |
|---|---|---|---|
| Q1 | Conceito escrito (achar erro / justificar) | 1,0 | **Não.** 100% ou zero |
| Q2 | Ler código pandas e explicar | 1,0 | Por bloco (~0,33 cada) |
| Q3 | `input` + validação + `if/elif` | 2,0 a 2,5 | Não dentro de cada rubrica |
| Q4 | Manipular [[DataFrame]] | 2,0 a 2,5 | Por rubrica |
| Q5 | Parsear strings num laço | 3,0 | Por etapa |

Q3 + Q4 + Q5 = 7 a 8 pontos nos três de código. É onde o jogo é ganho. Q1/Q2 são rápidos: responde, justifica, segue. Se a final puxar análise de dados, o peso migra pras questões de `groupby`/`pivot`/`merge` (bloco extra no fim): mesma lógica, o grosso do ponto está em manipular o DataFrame certo.

---

## Bloco Q1, Conceito escrito (1,0, sem parcial)

Leia o código linha a linha e ache o erro de **tipo** ou de **sintaxe**. Sempre justifique. As três pegadinhas que já caíram:

**1. [[input]] sempre retorna texto (`str`).**
```python
idade = input("Qual é a sua idade? ")
if idade < 18:          # ERRO AQUI, não na linha do input
    ...
```
O erro é na **comparação** (`idade < 18`), não na linha do `input`. Comparar `str` com `int` dá `TypeError: '<' not supported between instances of 'str' and 'int'`. Conserto: `idade = int(input("Qual é a sua idade? "))`.

**2. `for` vs `while`.** Regra: `for` quando você **sabe o número de repetições**; `while` quando repete **enquanto uma condição for verdadeira**.
- 3 chances pagas (número fixo) leva `for`.
- "R$4 por tentativa enquanto tiver saldo" depende do dinheiro, leva `while`.

**3. Sintaxe correta de [[loc]] (múltipla escolha).** Para `vendas.loc[mascara, "coluna"]`:
```python
vendas.loc[vendas["Ano"]==2026, "Valor"] *= 0.9          # CORRETO
vendas.loc[vendas["Ano"]==2026, "Valor"] = vendas.loc[vendas["Ano"]==2026, "Valor"] * 0.9   # CORRETO
```
Erradas e por quê:
- `vendas[vendas["Ano"]==2026, "Valor"] = ...`: faltou `.loc`, indexar com vírgula assim no `[]` simples é inválido.
- `vendas[vendas[Ano]=="2026"]`: `Ano` sem aspas vira variável inexistente (`NameError`), e `"2026"` (texto) não bate com coluna numérica.
- `vendas.loc["Ano"==2026, ...]`: `"Ano"==2026` resolve pra `False`, não é máscara booleana.

---

## Bloco Q2, Ler pandas e explicar (1,0)

Decomponha em blocos e diga o que cada um faz. Toda operação [[loc]] tem três partes: **máscara booleana** (filtro de linha) + **coluna** selecionada + **operação**.

**Exemplo filtro + contagem:**
```python
meusPedidos = pedidos.loc[pedidos["Estado"] == "SP", "Cód. Cliente"]
print(len(meusPedidos))
```
Filtra os pedidos cujo Estado é SP e pega só a coluna do código do cliente (uma Series). `len` imprime **quantos pedidos** são de SP. Cuidado: conta pedidos, não clientes únicos (um cliente pode repetir).

**Exemplo atribuição condicional (3 blocos, ~0,33 cada):**
```python
import pandas as pd                                          # bloco 1: carrega
pedidos = pd.read_excel(URL)
pedidos.loc[pedidos["Estado"]=="SP","Preço unitário"] = pedidos["Preço unitário"] * 0.2   # bloco 2
print(pedidos.head(10))                                       # bloco 3: mostra 10 primeiras
```
PEGADINHA: `* 0.2` faz o preço **virar 20%** do original (verificado: `100*0.2 = 20`), ou seja **reduz 80%**, não "reduz 20%".

---

## Bloco Q3, input + validação + condicional (2,0 a 2,5)

Padrão fixo: pede [[input]], **valida** (tipo + domínio), se erro imprime `ERRO DE ENTRADA`, senão calcula com [[Condicional]] (`if/elif` por faixa ou categoria) e imprime.

Molde (caso frete, o mais limpo):
```python
peso = input("Peso em gramas: ")
uf = input("UF: ").upper()                 # normaliza "sp" -> "SP"
ufs_validas = ["SP", "PR", "MG", "RJ", "ES"]

# 1) VALIDA ANTES de converter
if not peso.isdigit() or uf not in ufs_validas:
    print("ERRO DE ENTRADA")
else:
    peso = int(peso)                        # só converte depois de validar
    # 2) faixas de peso (proporcional por kg)
    if peso <= 10000:
        frete = (peso / 1000) * 0.98
    elif peso <= 50000:
        frete = (peso / 1000) * 0.74
    elif peso <= 100000:
        frete = (peso / 1000) * 0.42
    else:
        frete = 100                         # fixo, independe do peso
    # 3) adicional por estado
    if uf in ["MG", "RJ", "ES"]:
        frete = frete * 2                   # dobra (inclusive o fixo: 100 -> 200)
    print(frete)
```

**O que zera a rubrica:**
- Validar ANTES do `int()`. Se converter antes, `int("12.3")` ou `int("abc")` quebra a execução em vez de imprimir `ERRO DE ENTRADA`.
- [[isdigit]] rejeita ponto, sinal e espaço (verificado: `"12.3"`, `"-5"`, `"12 "` dão `False`). É o que a questão quer pra "inteiro".
- `.upper()` no UF pra aceitar minúsculas.
- Bordas das faixas: `<=` no topo de cada faixa; o `elif` já garante o piso (passou do anterior = é maior que o limite anterior).
- Frete fixo (R$100) NÃO multiplica peso, mas AINDA dobra pra MG/RJ/ES (vira 200).
- Sem parcial: acertar só alguns estados ou faixas dá 0 na rubrica de cálculo. Teste todas as faixas e todos os estados.

**Variante desconto (mesma estrutura, `if` aninhado estado depois faixa de valor):** `valor = qtd * preco`. SP: `<3000` 9%, `>=3000` 6,5%. RJ: `<2600` 10%, `>=2600` 8%. Demais: `1000 <= valor <= 1900` 8%, senão 6%. Valor com desconto = `valor * (1 - pct)`. Apresentar original, com desconto e a diferença.

---

## Bloco Q4, manipular DataFrame (2,0 a 2,5)

Dois sabores caíram. Sempre carregue, mexa com [[loc]], e some no fim.

> **Antes de tudo: confira o nome EXATO das colunas com `df.columns`.** Nome errado = `KeyError` = zero. As provas usam acento e maiúscula (`Preço Unitário`, `Código do Produto`, `Mês`).

**Sabor 1, corrigir preço e faturar (MrPacoca.xlsx tem `Preço Unitário`):**
```python
import pandas as pd
df = pd.read_excel("MrPacoca.xlsx")
cod = input("Código com erro: ")
preco = float(input("Preço correto: "))

df.loc[df["Código do Produto"] == cod, "Preço Unitário"] = preco   # troca condicional
df["Total"] = df["Preço Unitário"] * df["Quantidade"]              # cria coluna
print("Faturamento:", df["Total"].sum())                          # soma global
```

**Sabor 2, derivar preço, reajustar um mês, achar diferença (pedidos.xlsx NÃO tem preço, só `Total`):**
```python
import pandas as pd
df = pd.read_excel("pedidos.xlsx", index_col=0)
reajuste = 0.04
mes = 12

total_antes = df["Total"].sum()                                   # guarda antes
df["Preço Unitário"] = df["Total"] / df["Quantidade"]             # deriva preço
df.loc[df["Mês"] == mes, "Preço Unitário"] += reajuste            # reajusta só dezembro
df["Total"] = df["Preço Unitário"] * df["Quantidade"]             # recalcula total
print("Diferença:", df["Total"].sum() - total_antes)
```

**Sabor 3, consultar linha por chave + árvore de decisão (dataset_checkup csv):**
```python
import pandas as pd
pacientes = pd.read_csv("dataset_checkup_1000linhas.csv")
pid = int(input("id do paciente: "))

if pid not in pacientes["id"].values:
    print("Paciente não encontrado")
else:
    linha = pacientes[pacientes["id"] == pid].iloc[0]   # a linha como Series
    idade = linha["idade"]
    if linha["pressao_sistolica"] >= 140 or linha["pressao_diastolica"] >= 90:
        rec = "fazer checkup"
    elif idade >= 50:
        rec = "fazer checkup"
    elif linha["diabetes"]=="sim" or linha["historico_familiar"]=="sim" or linha["fumante"]=="sim":
        rec = "fazer checkup"
    else:
        rec = "não precisa checkup"
    print(f"Paciente {pid} (idade: {idade}) – Recomendação: {rec}")
```

**O que zera a rubrica:**
- Setar com `df.loc[mascara, "coluna"] = valor`. NUNCA `df[df[...]==x]["col"] = ...` (chained assignment, não altera o original).
- O `FutureWarning / ChainedAssignmentError` que aparece: a própria prova manda ignorar.
- Use as variáveis dadas (`cod`, `preco`, `reajuste`, `mes`), não hardcode os números do exemplo. Tem que rodar "pra qualquer cenário".
- Ordem no sabor 2: guardar total antes, criar preço, reajustar, recalcular total, então a diferença.
- Árvore de decisão: respeitar a ORDEM de prioridade com `elif` (para na primeira verdadeira). Pegar valor de célula com `.iloc[0]` na linha filtrada ou `df.loc[df["id"]==pid, "col"].values[0]`. Checar existência com `in df["col"].values`.
- Formato de saída do sabor 3 pede o caractere "–" exato (o enunciado chama de travessão). Copie do enunciado pra não trocar por hífen.

---

## Bloco Q5, parsear lista de strings num laço (3,0, vale mais)

Padrão: lista de strings delimitadas, [[Loop]] `for` em cada uma, `.split(delim)` pra separar, reorganizar/reformatar, **acumular total**, imprimir linha por item + linha totalizadora. Tem que rodar pra **qualquer** lista.

Molde genérico:
```python
total = 0
for item in lista:
    partes = item.split("#")        # ou "," . split SEMPRE devolve lista de str
    campo1, valor, data = partes[0], partes[1], partes[2]
    total += float(valor)           # converte antes de somar
    print(f"{campo1} - {valor}")    # formato pedido
print(f"Total: {total:.2f}")        # 2 casas quando pedir (ex: 41918.70)
```

**Sub-rotina datas (três formatos que caíram):**

Data junta `YYYYMMDD` para `dd/mm/aaaa` com [[Fatiamento lógico]] (verificado: `"20251119"` vira `19/11/2025`):
```python
ano, mes, dia = data[0:4], data[4:6], data[6:8]
print(f"{dia}/{mes}/{ano}")
```

Data por extenso (`"2025-10-02 10:00"` para `2 de outubro de 2025 às 10 horas`):
```python
meses = ['janeiro','fevereiro','março','abril','maio','junho',
         'julho','agosto','setembro','outubro','novembro','dezembro']
for reg in lista:
    partes = reg.split(" ")              # ["2025-10-02"] OU ["2025-10-02","10:00"]
    ano, mes, dia = partes[0].split("-")
    texto = f"{int(dia)} de {meses[int(mes)-1]} de {ano}"
    if len(partes) == 2:                 # tem hora
        h, m = int(partes[1].split(":")[0]), int(partes[1].split(":")[1])
        texto += " à 1 hora" if h == 1 else f" às {h} horas"
        if m == 1:
            texto += " e 1 minuto"
        elif m > 1:
            texto += f" e {m} minutos"
    print(texto)
```

Pedido `"Cliente001,Produto002,250"` para `Cliente001 - Produto002 - 250 unidades` + linha `N pedidos - T unidades`: mesmo molde, `.split(",")`, contador de pedidos e soma das quantidades.

**O que zera a rubrica:**
- `.split()` devolve **str**. Converter quantidade/valor com `int()`/`float()` antes de somar.
- Funcionar pra qualquer lista: usar `len(lista)` ou contador, nunca o número "4" do exemplo.
- Singular vs plural: "à 1 hora" vs "às X horas"; "1 minuto" vs "X minutos"; omitir minutos se 0; omitir hora se só data.
- `int('02')` vira `2` (tira zero à esquerda). `meses[int(mes)-1]` porque a lista é base 0 e o mês é base 1 (verificado: mês `10` vira `outubro`).

---

## Bloco extra, análise de dados com pandas (estilo AGP, pode cair junto)

Aqui o pandas opera no DataFrame **inteiro de uma vez** (vetorizado), sem `for`. Discriminador rápido: se a questão te dá um dataset grande e pede média/ranking/cruzamento, é este bloco. Se te dá uma lista de strings pra processar item a item, é a Q5 (laço).

### Carregar e explorar
CSV brasileiro exige `sep` e `decimal`, senão o número vem como texto e toda conta quebra:
```python
import pandas as pd
df = pd.read_csv("postos_sp_2025.csv", sep=";", decimal=",")

df.shape                                              # (n_linhas, n_colunas)
list(df.columns)                                      # nomes das colunas
df["Produto"].value_counts()                          # conta cada categoria
df["Valor de Venda"].agg(["min", "mean", "max"]).round(2)   # 3 stats numa operação só
```

### Criar coluna derivada (vetorizado, sem laço)
```python
df["Total"] = df["Preço"] * df["Quantidade"]          # cálculo entre colunas

# data "DD/MM/AAAA" -> "AAAA-MM" fatiando a coluna toda com .str[] (verificado):
df["Mes"] = df["Data da Coleta"].str[6:10] + "-" + df["Data da Coleta"].str[3:5]
# alternativa datetime:
# df["Mes"] = pd.to_datetime(df["Data da Coleta"], dayfirst=True).dt.to_period("M").astype(str)
```
Esse `.str[6:10]` é a versão vetorizada do `s[6:8]` que você usa no laço da Q5. Mesma ideia de [[Fatiamento lógico]], aplicada na coluna inteira.

### Agrupar, resumir, rankear
```python
df.groupby("Bandeira")["Margem"].mean().sort_values(ascending=False)   # ranking
df.groupby("Produto")["Valor"].agg(["mean", "max"])                    # vários stats por grupo
serie.sort_values().head(5)                                            # top 5 menores
```

### pivot_table (cada valor de uma coluna vira uma coluna)
```python
comparacao = df.pivot_table(index=["Municipio", "Mes"],
                            columns="Produto",
                            values="Valor de Venda",
                            aggfunc="mean").reset_index()
comparacao.columns.name = None        # limpa o rótulo "Produto" do cabeçalho
```

### merge (cruzar dois DataFrames pelas chaves em comum)
```python
dados = pd.merge(postos, distribuicao, on=["Municipio", "Mes", "Produto"])
```

### Classificar sem if (vetorizado)
```python
df["Razao"] = df["ETANOL"] / df["GASOLINA"]
df["Vantajoso"] = (df["Razao"] <= 0.708).replace({True: "Etanol", False: "Gasolina"})
# alternativa robusta: np.where(df["Razao"] <= 0.708, "Etanol", "Gasolina")
ge = df[df["Produto"].isin(["GASOLINA", "ETANOL"])]   # filtrar vários valores de uma vez
```

**O que zera ponto na análise:**
- CSV brasileiro: faltar `decimal=","` faz o número virar texto e toda conta quebra. `sep=";"` separa as colunas certas.
- `pivot_table` / `groupby` sem `.reset_index()` devolve índice multinível em vez de colunas comuns.
- `merge` tem que usar TODAS as chaves certas. Faltar uma (ex: `Produto`) cruza gasolina com preço de etanol e multiplica linhas.
- `.agg(["min","mean","max"])` resolve numa operação só. Se a questão pede "uma única operação", três chamadas separadas perdem ponto.
- `<=` vs `<` no limiar muda a classificação (verificado: `0.708 <= 0.708` é `True`). Lê o enunciado.
- É tudo vetorizado: usar `for` aqui geralmente é o caminho errado.
- Interpretação: quando pede análise (qual município, qual bandeira, decisão de investimento), os dados sozinhos não decidem. Cite o que eles NÃO capturam (custos da franquia, volume real, risco, concorrência). É onde mora o meio ponto.
- Amostra pequena engana: uma "maior margem" baseada em 22 registros é frágil. Se notar, comente em vez de só responder o literal.

---

## Kit de sobrevivência (cola rápida)

| Preciso | Código |
|---|---|
| Ler inteiro do usuário | `n = int(input("..."))` |
| Validar inteiro | `if texto.isdigit():` |
| Normalizar texto | `texto.upper()` / `.lower()` / `.strip()` |
| Carregar planilha / csv | `pd.read_excel("a.xlsx")` / `pd.read_csv("a.csv")` |
| Carregar CSV brasileiro | `pd.read_csv("a.csv", sep=";", decimal=",")` |
| Trocar valor condicional | `df.loc[df["col"]==x, "alvo"] = v` |
| Criar coluna | `df["nova"] = df["a"] * df["b"]` |
| Somar coluna | `df["col"].sum()` |
| Vários stats de uma vez | `df["col"].agg(["min","mean","max"])` |
| Contar categorias | `df["col"].value_counts()` |
| Média por grupo (ranking) | `df.groupby("g")["v"].mean().sort_values(ascending=False)` |
| Fatiar coluna de texto | `df["col"].str[6:10]` |
| Filtrar vários valores | `df["col"].isin(["A","B"])` |
| Reorganizar linhas×colunas | `df.pivot_table(index=..., columns=..., values=..., aggfunc="mean").reset_index()` |
| Cruzar dois DataFrames | `pd.merge(a, b, on=["chave1","chave2"])` |
| Pegar 1 célula filtrada | `df.loc[df["id"]==x, "col"].values[0]` |
| Existe valor na coluna? | `x in df["col"].values` |
| Separar string | `"a,b,c".split(",")` |
| Fatiar string | `s[0:4]` (do índice 0 ao 3) |
| Formatar com 2 casas | `f"{valor:.2f}"` |

## Estratégia de prova

- Preencha a Q0 (nome, turma `AE_`, código) sem apagar os `#` nem o texto pré-existente.
- Ordem sugerida: Q1 e Q2 primeiro (conceito, rápido, 2 pontos), depois Q5 (3 pontos), depois Q3 e Q4. Se travar na Q1/Q2 (sem parcial), não insista, volta depois.
- Discriminador de questão: dataset grande pedindo média/ranking/cruzamento é pandas vetorizado (bloco extra), não laço. Lista de strings pra processar item a item é Q5 (laço). Saber qual é qual já é meio caminho.
- Q3 e Q4 sem parcial dentro da rubrica: melhor **um** cenário 100% certo que vários meio certos. Teste o exemplo dado E um caso de borda (faixa limite, estado fora da lista, id inexistente).
- Não tente rodar nada com URL: a internet da prova é bloqueada. Use os arquivos locais.
- Código tem que servir pra qualquer cenário, nunca hardcode o exemplo do enunciado.

## Pra fixar

**Programação básica:**
- [[input]]
- [[Condicional]]
- [[loc]]
- [[DataFrame]]
- [[Loop]]
- [[split]]
- [[isdigit]]
- [[Fatiamento lógico]]

**Análise de dados:**
- [[read_csv]]
- [[value_counts]]
- [[groupby]]
- [[agg]]
- [[pivot_table]]
- [[merge]]
- [[isin]]
- [[str accessor]]
