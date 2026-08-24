---
materia: Estatistica2
data: 2026-08-17
tema: Testes de hipótese em Excel e R (revisão aulas 2 a 6)
tags: [aula, estudo]
---

Revisão hands-on de [[Teste de hipotese|teste de hipótese]] pra Provinha 1 (25/08, aulas 2 a 6). Sete testes, cada um resolvido na mão no Excel e no R, com os mesmos números. Arquivos companheiros na mesma pasta: `TestesHipotese.xlsx` (uma aba por teste, fórmulas vivas) e `TestesHipotese.R` (script rodável, bloco por bloco).

## 0. Como usar

Três coisas abertas ao mesmo tempo: este md no Obsidian (a aula), o `TestesHipotese.xlsx` no Excel, o `TestesHipotese.R` no VS Code com o terminal rodando `R` (setup na seção 1).

**Ciclo por teste** (vale pros 7 blocos da seção 4):

1. Lê só o enunciado. Antes de ler o resto, escreve no papel H0, H1, cauda e qual teste é (tabela da seção 2 se travar). Só então lê os passos 1 a 3 e confere.
2. Excel: abre a aba do teste. Clica célula por célula do bloco de passos e lê a fórmula na barra (o bloco "Excel" de cada teste aqui é o mesmo, célula: fórmula). Apaga a célula do valor-p e reescreve a fórmula você mesmo. Muda um input azul (μ₀, α, um dado) e vê a decisão virar.
3. R: cola o bloco no console, lê o output. Digita os objetos um a um (`ep`, `t_calc`, `qt(...)`, `pt(...)`) e confere que batem com o Excel. Muda o mesmo input que mudou no Excel, roda de novo, mesma virada.
4. Lê os passos 4 e 5 e a pegadinha. Escreve a frase de interpretação com tuas palavras, sem olhar a daqui. Compara.
5. Anota uma linha: "teste X: quando usar, fórmula, função Excel, função R". No fim são 7 linhas, o cheat sheet de véspera.

**Ordem e sessões** (Provinha 1 em 25/08):

| Sessão | O quê | Tempo |
|---|---|---|
| 1 | Seções 1 e 2 só lendo. Ciclo em 4.1 e 4.2 (Z e t de uma média, os mais cobrados) | 1h |
| 2 | Ciclo em 4.3, 4.4, 4.5 (pareado, Welch, proporção) | 1h |
| 3 | Ciclo em 4.6 e 4.7 (qui-quadrado), de preferência depois da aula de ter 18/08 | 45 min |
| 4 | Exercícios E1 a E4 (roteiro abaixo) | 1h |
| 5 (véspera) | Reler seção 6. Pegar 2 enunciados da seção 4, cobrir a resposta, resolver do zero no papel com os 5 passos e o Excel só de calculadora | 45 min |

**Exercícios (sessão 4), um por vez:**

1. Lê o enunciado (seção 5) e decide o teste com a tabela da seção 2. Em E3 esse é o ponto: pareado ou Welch antes de qualquer conta.
2. Excel: aba nova, copia a estrutura da aba parecida (E1 usa o bloco 2b da `2_T_Media`, E2 a `5_Proporcao`, E3a a `3_Pareado`, E3b a `4_Welch`, E4 a `6_Qui_Aderencia`) e cola os dados da aba `Exercicios`. Monta os passos você mesmo.
3. R: digita (não cola) as linhas: estatística na mão, crítico, valor-p, depois a função pronta. Os vetores de dados estão prontos no bloco 8 do script, esses pode colar.
4. Escreve a frase de interpretação.
5. Só agora abre a seção 7 (gabarito) e descomenta o bloco 9 do script. Se um número não bater, procura o erro no teu Excel primeiro (referência de célula, cauda, `STDEV.S`), depois no R.

**Sinal de pronto**: um enunciado novo (inventa: "a espera média era 8 min, amostra de 15 deu 8,6 com s 1,1, piorou?"), 5 passos no papel, conta no Excel e no R, frase de interpretação, tudo sem abrir a seção 4. Onde travar é o que falta revisar.

## 1. Setup

### R no terminal

<pre>
brew install r          # instala (já feito nesta máquina, R 4.6.1)
cd ~/FGV/Estatistica2/Aulas/08.17
R                       # abre o console; o prompt vira "&gt;"
q()                     # sai; responde n (não salvar workspace)
Rscript TestesHipotese.R            # roda o script inteiro sem abrir o console
</pre>

**Roteiro de uso (duas janelas).** O jeito de "fazer no R" nesta aula é copiar bloco a bloco do script pro console e mexer nos objetos.

1. Abre o VS Code na pasta `~/FGV/Estatistica2/Aulas/08.17` e clica em `TestesHipotese.R` (o código, comentado, com os dados).
2. No VS Code, View → Terminal (Ctrl+`). No terminal digita `R` e Enter: o prompt vira `>`. Código em cima, R embaixo. Sem VS Code: Terminal com `R` numa janela e o `.R` aberto no TextEdit na outra.
3. Roda o bloco 0 primeiro (define `decide` e `alpha`): seleciona do `# ---- 0.` até antes do `# ---- 1.`, Cmd+C, clica no terminal, Cmd+V, Enter.
4. Pra cada teste: lê a seção 4.x aqui, copia o bloco correspondente do script, cola no console, lê o output. Depois digita os objetos um por vez no `>` (`ep`, `t1_z`, `qnorm(0.95)`, `1 - pnorm(t1_z)`) e vê os números aparecerem. Muda um input (`xbar <- 505`), roda o bloco de novo, vê a decisão virar.
5. Compara com a aba do xlsx e com os passos 4 e 5 do md. Mesmos números. Próximo bloco.

Sinais de que algo travou: prompt `+` em vez de `>` é comando incompleto (Esc ou Ctrl+C volta); `could not find function "decide"` é o bloco 0 que não rodou; `command not found: R` é o Terminal aberto antes da instalação (fecha e abre de novo).

Dez comandos de sobrevivência (tudo o que a aula usa além das funções de teste):

| Comando | O que faz |
|---|---|
| `x <- c(9.7, 10.2, 10.4)` | cria um vetor (a amostra). Decimal é ponto, separador é vírgula |
| `mean(x)`, `sd(x)`, `length(x)`, `sqrt(n)` | média, desvio amostral (n−1), n, raiz |
| `qnorm(1-alpha)`, `qt(1-alpha, gl)`, `qchisq(1-alpha, gl)` | valor crítico: entra área, sai valor de corte |
| `pnorm(z)`, `pt(t, gl)`, `pchisq(x2, gl)` | área à esquerda: entra valor, sai probabilidade. `lower.tail = FALSE` dá a área à direita |
| `t.test(x, mu = 48, alternative = "greater")` | teste t pronto (uma amostra, pareado, duas amostras) |
| `prop.test(x, n, p = 0.2, alternative = "greater", correct = FALSE)` | teste de proporção pronto |
| `chisq.test(x = obs, p = p_exp)` e `chisq.test(tab)` | qui-quadrado de aderência e de independência |
| `?t.test` | ajuda da função (argumentos e exemplos) |
| `source("TestesHipotese.R")` | roda o arquivo de dentro do console |
| `ls()` e `rm(list = ls())` | lista e limpa os objetos da sessão |

O professor usa base R puro (`matrix`, `dimnames`, `chisq.test`), sem pacote nenhum. A aula segue isso.

### Excel

- Fórmulas escritas em inglês, com vírgula entre argumentos, igual ao `Exercicio_aula02.xlsx` do professor. Se o teu Excel estiver em português: nomes na coluna PT da seção 3 e ponto e vírgula no lugar da vírgula.
- Convenção da planilha: azul = input que você pode mudar (μ₀, α, σ, dados), preto = fórmula. Muda um azul, tudo recalcula.
- Duas famílias de função, espelhadas: a inversa entra área e devolve valor de corte (=`NORM.S.INV`, =`T.INV`, =`T.INV.2T`, =`CHISQ.INV.RT`), a distribuição entra valor e devolve área (=`NORM.S.DIST`, =`T.DIST`, =`T.DIST.RT`, =`T.DIST.2T`, =`CHISQ.DIST.RT`). Foi assim que o professor mostrou em aula.
- Atalhos que devolvem só o valor-p: =`T.TEST`, =`Z.TEST`, =`CHISQ.TEST`. Servem pra conferir, não pra aprender: a estatística de teste não sai deles.
- Análise de Dados (suplemento) tem "t-Test" e "z-Test" prontos. Não usamos aqui: em prova você precisa da fórmula, não do menu.

## 2. A receita e a escolha do teste

Receita fixa do professor, vale pra qualquer enunciado. Ele cobra os dois caminhos de decisão (crítico e valor-p) e cobra a interpretação.

<pre>
1. H0 e H1. Baseline vai em H0 com =, &lt;= ou &gt;=. H1 é o que o enunciado quer verificar.
   Cauda vem do verbo: "aumentou?" / "diminuiu?" -&gt; unicaudal; "mudou?" / "é diferente?" -&gt; bicaudal.
2. alfa (nível de significância). Default 5%.
3. Estatística de teste: quantos erros-padrão o observado está do valor de H0.
   Z se sigma populacional é dado; t se usa s da amostra; qui-quadrado se são contagens.
4. Valor crítico (entra alfa, sai corte) e valor-p (entra estatística, sai área). Os dois levam à mesma decisão.
5. Decisão: valor-p &lt; alfa (ou estatística além do crítico) -&gt; rejeita H0. Interpretação empresarial em uma frase.
</pre>

| Situação do enunciado | Teste | Estatística | Distribuição e gl | Excel | R |
|---|---|---|---|---|---|
| uma média, σ populacional dado | Z uma média | (x̄ − μ₀)/(σ/√n) | [[Distribuicao normal|normal padrão]] | =`NORM.S.INV`, =`NORM.S.DIST` | `qnorm`, `pnorm` (na mão) |
| uma média, só s da amostra | t uma média | (x̄ − μ₀)/(s/√n) | [[Distribuicao T de Student|t]], gl = n − 1 | =`T.INV`/=`T.INV.2T`, =`T.DIST.RT`/=`T.DIST.2T` | `qt`, `pt`, `t.test(x, mu=)` |
| mesmas unidades medidas antes e depois | [[Teste pareado|t pareado]] | D̄/(s_D/√n), D = depois − antes | t, gl = n − 1 | coluna D + bloco de uma média; =`T.TEST(...,1)` | `t.test(dep, ant, paired=TRUE)` |
| dois grupos de unidades diferentes | [[Teste t para duas amostras|t duas amostras (Welch)]] | (x̄_A − x̄_B)/√(s²_A/n_A + s²_B/n_B) | t, gl de Welch | fórmula + =`T.DIST.2T`; =`T.TEST(A,B,2,3)` | `t.test(A, B)` |
| proporção (sim/não, 0/1) | Z proporção | (p̂ − p₀)/√(p₀(1−p₀)/n) | normal padrão | =`NORM.S.INV`, =`NORM.S.DIST` | `pnorm` na mão; `prop.test(correct=FALSE)` |
| contagens em k categorias de UMA variável vs distribuição teórica | [[Teste qui-quadrado de aderencia|qui-quadrado aderência]] | Σ(O−E)²/E | [[Distribuicao qui-quadrado|qui-quadrado]], gl = k − 1 | =`CHISQ.INV.RT`, =`CHISQ.DIST.RT`, =`CHISQ.TEST` | `chisq.test(x=obs, p=)` |
| contagens cruzadas de DUAS variáveis (tabela r × c) | [[Teste qui-quadrado de independencia|qui-quadrado independência]] | ΣΣ(O−E)²/E | qui-quadrado, gl = (r−1)(c−1) | idem, com matriz de esperadas | `chisq.test(tab)` |

Regra de bolso pro Z vs t que o professor deu: sempre que entra s (desvio da amostra) no lugar de σ, tecnicamente é t. Z só é exato com σ populacional conhecido; n grande é aproximação aceitável.

## 3. Mapa de funções

Mesma tabela da aba `Mapa` do xlsx. α = nível de significância, gl = graus de liberdade.

| Objetivo | Excel (EN) | Excel (PT) | R | Devolve | Observação |
|---|---|---|---|---|---|
| n | =`COUNT(range)` | =`CONT.NÚM(intervalo)` | `length(x)` | n | |
| média amostral | =`AVERAGE(range)` | =`MÉDIA(intervalo)` | `mean(x)` | x̄ | |
| desvio amostral s | =`STDEV.S(range)` | =`DESVPAD.A(intervalo)` | `sd(x)` | s, divide por n − 1 | =`STDEV.P` divide por n: errado pra amostra |
| raiz, valor absoluto | =`SQRT(x)`, =`ABS(x)` | =`RAIZ(x)`, =`ABS(x)` | `sqrt(x)`, `abs(x)` | | |
| Z crítico unicaudal | =`NORM.S.INV(1-α)` | =`INV.NORMP.N(1-α)` | `qnorm(1-alpha)` | 1,645 pra 5% | esquerda: =`NORM.S.INV(α)` = −1,645 |
| Z crítico bicaudal | =`NORM.S.INV(1-α/2)` | =`INV.NORMP.N(1-α/2)` | `qnorm(1-alpha/2)` | 1,960 pra 5% | α/2 em cada cauda ([[Z de alfa sobre 2]]) |
| valor-p Z, cauda direita | =`1-NORM.S.DIST(z,TRUE)` | =`1-DIST.NORMP.N(z;VERDADEIRO)` | `1-pnorm(z)` | área à direita | esquerda: =`NORM.S.DIST(z,TRUE)` |
| valor-p Z, bicaudal | =`2*(1-NORM.S.DIST(ABS(z),TRUE))` | =`2*(1-DIST.NORMP.N(ABS(z);VERDADEIRO))` | `2*(1-pnorm(abs(z)))` | dobro da cauda | |
| t crítico unicaudal direita | =`T.INV(1-α,gl)` | =`INV.T(1-α;gl)` | `qt(1-alpha, gl)` | ex. 1,729 (gl 19) | =`T.INV(α,gl)` dá o da esquerda, negativo |
| t crítico bicaudal | =`T.INV.2T(α,gl)` | =`INV.T.BC(α;gl)` | `qt(1-alpha/2, gl)` | ex. 2,093 (gl 19) | entra α inteiro, a função divide |
| valor-p t, cauda direita | =`T.DIST.RT(t,gl)` | =`DIST.T.CD(t;gl)` | `pt(t, gl, lower.tail=FALSE)` | área à direita | |
| valor-p t, cauda esquerda | =`T.DIST(t,gl,TRUE)` | =`DIST.T(t;gl;VERDADEIRO)` | `pt(t, gl)` | área à esquerda | |
| valor-p t, bicaudal | =`T.DIST.2T(ABS(t),gl)` | =`DIST.T.BC(ABS(t);gl)` | `2*pt(-abs(t), gl)` | dobro da cauda | =`T.DIST.2T` exige t ≥ 0: use =`ABS` |
| qui-quadrado crítico | =`CHISQ.INV.RT(α,gl)` | =`INV.QUIQUA.CD(α;gl)` | `qchisq(1-alpha, gl)` | ex. 5,991 (gl 2) | sempre cauda direita |
| valor-p qui-quadrado | =`CHISQ.DIST.RT(x2,gl)` | =`DIST.QUIQUA.CD(x2;gl)` | `pchisq(x2, gl, lower.tail=FALSE)` | área à direita | |
| atalho t pareado | =`T.TEST(dep,ant,caudas,1)` | =`TESTE.T(dep;ant;caudas;1)` | `t.test(dep, ant, paired=TRUE)` | só o valor-p | caudas=1 devolve a cauda de \|t\|, não sabe a direção de H1 |
| atalho t duas amostras | =`T.TEST(A,B,2,3)` | =`TESTE.T(A;B;2;3)` | `t.test(A, B)` | só o valor-p | tipo 3 = variâncias diferentes (Welch); tipo 2 = iguais |
| atalho Z uma média | =`Z.TEST(range,μ0,σ)` | =`TESTE.Z(intervalo;μ0;σ)` | na mão | valor-p da cauda superior | inferior: =`1-Z.TEST`; bicaudal: =`2*MIN(Z.TEST,1-Z.TEST)` |
| atalho qui-quadrado | =`CHISQ.TEST(obs,esp)` | =`TESTE.QUIQUA(obs;esp)` | `chisq.test(...)` | só o valor-p | as esperadas você calcula; a estatística não sai da função |
| proporção, função pronta | na mão | na mão | `prop.test(x, n, p=p0, alternative=, correct=FALSE)` | X-squared = z², mesmo valor-p | default `correct=TRUE` muda o valor-p |

## 4. Os sete testes

### 4.1 Z para uma média com σ conhecido (vendas, meta 500)

Enunciado (slide da aula 3): meta de vendas diárias R$ 500. Amostra de 36 dias, média R$ 520, σ populacional R$ 30. As vendas aumentaram? α = 5%.

Passos 1 e 2. "Aumentaram?" pede uma direção só: [[Teste unicaudal|unicaudal]] à direita. H0: μ ≤ 500. H1: μ > 500. α = 0,05.

Passo 3. σ foi dado, então Z é legítimo. [[Estatistica de teste|Estatística]] = quantos [[Erro padrao|erros-padrão]] a média da amostra está acima de 500.

<pre>
EP = σ/√n = 30/√36 = 5
z  = (x̄ − μ0)/EP = (520 − 500)/5 = 4,000
</pre>

Excel (aba `1_Z_Media`):

<pre>
D6  α           0,05          (azul)
D7  μ0          500           (azul)
D8  σ           30            (azul)
D9  n           36            (azul)
D10 x̄           520           (azul)
D11 EP          =D8/SQRT(D9)
D12 z           =(D10-D7)/D11
D13 z crítico   =NORM.S.INV(1-D6)             -&gt; 1,645
D14 valor-p     =1-NORM.S.DIST(D12,TRUE)      -&gt; 0,00003
D15 decisão     =IF(D14&lt;D6,"Rejeita H0","Não rejeita H0")
</pre>

R (bloco 1 do script). Base R não tem `z.test`: Z é sempre na mão, `qnorm` pro crítico e `pnorm` pro valor-p.

<pre>
xbar &lt;- 520; mu0 &lt;- 500; sigma &lt;- 30; n &lt;- 36; alpha &lt;- 0.05
ep   &lt;- sigma / sqrt(n)
z    &lt;- (xbar - mu0) / ep
qnorm(1 - alpha)          # crítico: 1.645
1 - pnorm(z)              # valor-p: área à direita de z
</pre>

<pre>
==== 1. Z uma média (vendas) ====
  z = 4 | z crítico = 1.645
  valor-p = 3.167e-05 &lt; 0.05 -&gt;  REJEITA H0
</pre>

Passos 4 e 5. [[Valor critico|Crítico]] 1,645, z = 4,0 está muito dentro da [[Regiao de rejeicao|região de rejeição]]. [[Valor-p]] = 0,00003 < 0,05. Rejeita H0. Frase: "A 5% de significância, há evidência de que a média diária de vendas superou a meta de R$ 500. O 520 é a média da amostra, não a nova média populacional."

Pegadinha: Z só porque σ = 30 veio no enunciado. Se viesse "desvio-padrão da amostra 30", seria t com gl = 35.

### 4.2 t para uma média: sumário (satisfação 7,0) e dados brutos (SLA 48h)

**4.2a Sumário.** Enunciado (slide da aula 3): benchmark de satisfação 7,0. Amostra de 20 clientes: x̄ = 6,8, s = 0,5, α = 5%. O slide não fixa a cauda, então roda as duas leituras: "é diferente de 7?" e "está abaixo de 7?".

Passo 3. Só temos s (amostral): t com gl = n − 1 = 19 [[Graus de liberdade|graus de liberdade]].

<pre>
EP = s/√n = 0,5/√20 = 0,1118
t  = (6,8 − 7,0)/0,1118 = −1,789
</pre>

Excel (aba `2_T_Media`, bloco C:D):

<pre>
D4  α          0,05         D5 μ0 7      D6 n 20      D7 x̄ 6,8      D8 s 0,5   (azuis)
D9  gl         =D6-1
D10 EP         =D8/SQRT(D6)
D11 t          =(D7-D5)/D10                          -&gt; −1,789
Leitura 1, H1: μ ≠ 7 (bicaudal)
D13 t crítico  =T.INV.2T(D4,D9)                      -&gt; ±2,093
D14 valor-p    =T.DIST.2T(ABS(D11),D9)               -&gt; 0,0896
D15 decisão    =IF(D14&lt;D4,"Rejeita H0","Não rejeita H0")
Leitura 2, H1: μ &lt; 7 (unicaudal esquerda)
D17 t crítico  =T.INV(D4,D9)                         -&gt; −1,729
D18 valor-p    =T.DIST(D11,D9,TRUE)                  -&gt; 0,0448
D19 decisão    =IF(D18&lt;D4,"Rejeita H0","Não rejeita H0")
</pre>

R (bloco 2a):

<pre>
xbar &lt;- 6.8; s &lt;- 0.5; n &lt;- 20; mu0 &lt;- 7; gl &lt;- n - 1
t_calc &lt;- (xbar - mu0) / (s / sqrt(n))
qt(1 - alpha/2, gl); 2 * pt(-abs(t_calc), gl)     # bicaudal: crítico ±2.093, valor-p
qt(alpha, gl);       pt(t_calc, gl)               # unicaudal esquerda: crítico -1.729, valor-p
</pre>

<pre>
==== 2a. t uma média, sumário (satisfação) ====
  bicaudal: t = -1.789 | crítico = ± 2.093
  valor-p = 0.08959 &gt;= 0.05 -&gt; NÃO rejeita H0
  unicaudal esq: t = -1.789 | crítico = -1.729
  valor-p = 0.0448 &lt; 0.05 -&gt;  REJEITA H0
</pre>

Passos 4 e 5. [[Teste bicaudal|Bicaudal]]: |−1,789| < 2,093 e p = 0,0896 > 0,05, não rejeita ("a amostra não dá evidência de que a satisfação difere de 7"). Unicaudal esquerda: −1,789 < −1,729 e p = 0,0448 < 0,05, rejeita ("há evidência de que a satisfação está abaixo do benchmark"). Mesma amostra, decisões opostas: **a cauda vem do enunciado, não do dado**. Se o enunciado disser "abaixo", é unicaudal e ponto.

**4.2b Dados brutos.** Enunciado (exercício 1 da aula 3): SLA promete 48h. Amostra de 25 entregas (horas, dados simulados na aba e no script). O tempo médio está estourando o SLA? α = 5%.

Passos 1 e 2. "Estourando" = maior: H0: μ ≤ 48, H1: μ > 48, unicaudal à direita. α = 0,05.

Passo 3. Agora os dados brutos entram e a estatística sai de =`COUNT`, =`AVERAGE`, =`STDEV.S`.

<pre>
n = 25   x̄ = 49,664   s = 4,150   EP = 4,150/√25 = 0,830   gl = 24
t = (49,664 − 48)/0,830 = 2,005
</pre>

Excel (aba `2_T_Media`, bloco F:G, dados em A4:A28):

<pre>
G6  α          0,05                     G7 μ0 48   (azuis)
G8  n          =COUNT(A4:A28)
G9  x̄          =AVERAGE(A4:A28)
G10 s          =STDEV.S(A4:A28)
G11 EP         =G10/SQRT(G8)
G12 gl         =G8-1
G13 t          =(G9-G7)/G11                        -&gt; 2,005
G14 t crítico  =T.INV(1-G6,G12)                    -&gt; 1,711
G15 valor-p    =T.DIST.RT(G13,G12)                 -&gt; 0,0282
G16 decisão 5% =IF(G15&lt;G6,"Rejeita H0","Não rejeita H0")
G17 α alt.     0,01   (azul)
G18 decisão 1% =IF(G15&lt;G17,"Rejeita H0","Não rejeita H0")
</pre>

R (bloco 2b). Primeiro na mão, depois a função pronta com os mesmos números:

<pre>
sla &lt;- c(51.4, 41.8, 58.3, 48.5, 49.7, 49.5, 58.0, 49.1, 49.4, 48.9, 47.3, 49.1, 52.1,
         45.4, 54.7, 53.5, 49.7, 49.3, 49.0, 48.1, 43.6, 47.3, 52.1, 41.8, 54.0)
n &lt;- length(sla); xbar &lt;- mean(sla); s &lt;- sd(sla); gl &lt;- n - 1
t_calc &lt;- (xbar - 48) / (s / sqrt(n))
qt(1 - alpha, gl)                        # crítico cauda direita
pt(t_calc, gl, lower.tail = FALSE)       # valor-p cauda direita
t.test(sla, mu = 48, alternative = "greater")   # mu = valor de H0; alternative = lado de H1
</pre>

<pre>
==== 2b. t uma média, dados brutos (SLA) ====
  n = 25 | média = 49.664 | s = 4.15
  t = 2.005 | crítico = 1.711
  valor-p = 0.02819 &lt; 0.05 -&gt;  REJEITA H0
  a 1%:   valor-p = 0.02819 &gt;= 0.01 -&gt; NÃO rejeita H0

	One Sample t-test

data:  sla
t = 2.0048, df = 24, p-value = 0.02819
alternative hypothesis: true mean is greater than 48
95 percent confidence interval:
 48.24397      Inf
sample estimates:
mean of x
   49.664
</pre>

Passos 4 e 5. t = 2,005 > 1,711 e p = 0,0282 < 0,05: rejeita a 5%. A 1% o crítico sobe pra 2,492 e p = 0,0282 > 0,01: não rejeita. Frase: "A 5% há evidência de que o tempo médio de entrega passa das 48h prometidas; a 1% a amostra não basta pra afirmar isso." O [[Nivel de significancia|nível de significância]] é escolha de quem decide, e o resultado pode virar com ele.

Pegadinhas: =`STDEV.S` (divide por n − 1), nunca =`STDEV.P`. No output do `t.test`, `alternative hypothesis: true mean is greater than 48` confirma que a cauda ficou certa; se aparecer `not equal`, você esqueceu o `alternative`.

### 4.3 t pareado (12 lojas, antes/depois)

Enunciado (exercício 2 da aula 3): vendas diárias (R$ mil) das mesmas 12 lojas antes e depois de uma campanha. A campanha aumentou as vendas? Reportar tamanho do efeito e IC. α = 5%.

Passos 1 e 2. Mesmas unidades medidas duas vezes: [[Teste pareado|pareado]]. Trabalha nas diferenças D = Depois − Antes. "Aumentou" = D positivo: H0: μ_D ≤ 0, H1: μ_D > 0, unicaudal à direita.

Passo 3. Pareado é um teste t de uma média sobre a coluna D, com μ₀ = 0.

<pre>
D̄ = 20,617   s_D = 17,963   EP = 17,963/√12 = 5,185   gl = 11
t = (20,617 − 0)/5,185 = 3,976
</pre>

Excel (aba `3_Pareado`, Antes em A4:A15, Depois em B4:B15, D em C4:C15):

<pre>
C4  D          =B4-A4   (arrasta até C15)
F6  α          0,05   (azul)
F7  n          =COUNT(C4:C15)
F8  D médio    =AVERAGE(C4:C15)                    -&gt; 20,617
F9  s_D        =STDEV.S(C4:C15)                    -&gt; 17,963
F10 EP         =F9/SQRT(F7)
F11 gl         =F7-1
F12 t          =(F8-0)/F10                         -&gt; 3,976
F13 t crítico  =T.INV(1-F6,F11)                    -&gt; 1,796
F14 valor-p    =T.DIST.RT(F12,F11)                 -&gt; 0,0011
F15 decisão    =IF(F14&lt;F6,"Rejeita H0","Não rejeita H0")
F16 IC 95% inf =F8-T.INV.2T(0.05,F11)*F10          -&gt; 9,20
F17 IC 95% sup =F8+T.INV.2T(0.05,F11)*F10          -&gt; 32,03
F18 atalho     =T.TEST(B4:B15,A4:A15,1,1)          -&gt; 0,0011 (caudas=1, tipo 1=pareado)
</pre>

R (bloco 3):

<pre>
antes  &lt;- c(177.0, 254.8, 225.2, 226.1, 221.5, 203.9, 198.6, 198.5, 208.9, 212.3, 213.6, 225.1)
depois &lt;- c(166.3, 280.9, 253.2, 253.8, 207.3, 224.2, 226.6, 204.5, 238.0, 240.1, 246.0, 272.0)
D &lt;- depois - antes
t_calc &lt;- mean(D) / (sd(D) / sqrt(length(D)))
qt(1 - alpha, length(D) - 1); pt(t_calc, length(D) - 1, lower.tail = FALSE)
t.test(depois, antes, paired = TRUE, alternative = "greater")   # paired = TRUE faz o pareado
t.test(depois, antes, paired = TRUE)$conf.int                    # IC 95% bicaudal de mu_D
</pre>

<pre>
==== 3. t pareado (vendas antes/depois) ====
  D médio = 20.617 | s_D = 17.963 | t = 3.976 | crítico = 1.796
  valor-p = 0.001087 &lt; 0.05 -&gt;  REJEITA H0

	Paired t-test

data:  depois and antes
t = 3.976, df = 11, p-value = 0.001087
alternative hypothesis: true mean difference is greater than 0
95 percent confidence interval:
 11.3044     Inf
sample estimates:
mean difference
       20.61667

  IC 95% de mu_D: [ 9.2 ; 32.03 ]
</pre>

Passos 4 e 5. t = 3,976 > 1,796, p = 0,0011: rejeita. Frase: "Há evidência forte de que a campanha aumentou as vendas. O efeito médio estimado é de R$ 20,6 mil por loja, com [[Intervalo de Confiança|IC]] 95% de 9,2 a 32,0 mil." O IC do `t.test` com `alternative = "greater"` é unilateral (11,3 a infinito); pra reportar a faixa de dois lados, roda o `t.test` bicaudal e pega o `$conf.int`.

Pegadinhas: o sinal de D. Se você definir D = Antes − Depois, H1 vira μ_D < 0 e a cauda vira esquerda. =`T.TEST` com caudas=1 devolve sempre a cauda do |t|: dá o valor-p certo aqui porque D̄ tem o sinal de H1; se D̄ tivesse sinal contrário, o valor-p verdadeiro seria 1 menos isso.

### 4.4 Duas médias independentes, Welch (ticket loja A vs B)

Extensão além dos slides. Enunciado: ticket médio (R$) de 15 clientes da loja A e 18 clientes da loja B (pessoas diferentes). Os tickets médios diferem? α = 5%.

Passos 1 e 2. Grupos de unidades diferentes: [[Teste t para duas amostras|duas amostras independentes]]. "Diferem?" = bicaudal. H0: μ_A = μ_B, H1: μ_A ≠ μ_B.

Passo 3. Erro-padrão da diferença junta as duas variâncias; gl vem da fórmula de Welch (não é n_A + n_B − 2, isso é a versão com variâncias iguais).

<pre>
x̄_A = 81,773   x̄_B = 89,622   s_A = 10,296   s_B = 15,260   n_A = 15   n_B = 18
EP  = √(s²_A/n_A + s²_B/n_B) = √(10,296²/15 + 15,260²/18) = 4,473
t   = (81,773 − 89,622)/4,473 = −1,755
gl  = EP⁴ / [ (s²_A/n_A)²/(n_A−1) + (s²_B/n_B)²/(n_B−1) ] = 29,84
</pre>

Excel (aba `4_Welch`, A em A4:A18, B em B4:B21):

<pre>
E7  nA   =COUNT(A4:A18)        E8  nB   =COUNT(B4:B21)
E9  x̄A   =AVERAGE(A4:A18)      E10 x̄B   =AVERAGE(B4:B21)
E11 sA   =STDEV.S(A4:A18)      E12 sB   =STDEV.S(B4:B21)
E13 EP   =SQRT(E11^2/E7+E12^2/E8)
E14 t    =(E9-E10)/E13                                        -&gt; −1,755
E15 gl   =E13^4/((E11^2/E7)^2/(E7-1)+(E12^2/E8)^2/(E8-1))      -&gt; 29,84
E16 t crítico  =T.INV.2T(E6,E15)                              -&gt; ±2,045
E17 valor-p    =T.DIST.2T(ABS(E14),E15)                       -&gt; 0,0898
E18 decisão    =IF(E17&lt;E6,"Rejeita H0","Não rejeita H0")
E19 atalho     =T.TEST(A4:A18,B4:B21,2,3)                     -&gt; 0,0895 (2 caudas, tipo 3 = Welch)
</pre>

R (bloco 4). `t.test(A, B)` já é Welch por default:

<pre>
A &lt;- c(86.0, 67.0, 91.0, 80.2, 90.7, 84.2, 68.6, 76.0, 86.1, 84.0, 60.3, 85.1, 86.6, 100.4, 80.4)
B &lt;- c(79.1, 92.0, 76.0, 74.4, 76.2, 64.1, 78.6, 102.5, 85.6, 103.5, 87.9, 90.9, 104.9, 96.3,
       81.6, 111.1, 125.0, 83.5)
ep &lt;- sqrt(var(A)/length(A) + var(B)/length(B))
t_calc &lt;- (mean(A) - mean(B)) / ep
gl &lt;- ep^4 / ((var(A)/length(A))^2/(length(A)-1) + (var(B)/length(B))^2/(length(B)-1))
qt(1 - alpha/2, gl); 2 * pt(-abs(t_calc), gl)
t.test(A, B)                       # Welch (var.equal = FALSE é o default)
# t.test(A, B, var.equal = TRUE)   # versão pooled, gl = 31: só pra saber que existe
</pre>

<pre>
==== 4. Welch (ticket médio loja A vs B) ====
  t = -1.755 | gl Welch = 29.84 | crítico = ± 2.043
  valor-p = 0.08954 &gt;= 0.05 -&gt; NÃO rejeita H0

	Welch Two Sample t-test

data:  A and B
t = -1.7549, df = 29.836, p-value = 0.08954
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -16.98524   1.28746
sample estimates:
mean of x mean of y
 81.77333  89.62222
</pre>

Passos 4 e 5. |−1,755| < 2,043 e p ≈ 0,09 > 0,05: não rejeita. Frase: "A 5% a amostra não sustenta que os tickets médios das duas lojas diferem. Isso não prova que são iguais: o IC da diferença vai de −17,0 a +1,3, e a diferença observada de R$ 7,8 pode ser real, só que a amostra é pequena pra afirmar."

Por que Excel deu 0,0898 e R deu 0,0895: =`T.DIST.2T` e =`T.INV.2T` truncam gl não inteiro (29,84 vira 29). O R usa 29,84. Diferença na 3ª casa, decisão igual. O atalho =`T.TEST(A,B,2,3)` usa o gl fracionário e bate com o R (0,0895). Em prova, escreve o gl com decimal e o valor-p; se a questão pedir tabela, arredonda gl pra baixo.

### 4.5 Z para uma proporção (golfe, 20% para 25%)

Enunciado (aula 4): 20% dos jogadores do clube eram mulheres. Após uma promoção, amostra de 400 jogadores tem 100 mulheres. A promoção aumentou a proporção? α = 5%.

Passos 1 e 2. "Aumentou" = unicaudal à direita. H0: p ≤ 0,20, H1: p > 0,20.

Passo 3. [[Proporcao amostral|p̂]] = 100/400 = 0,25. O erro-padrão usa o p₀ da hipótese, não o p̂ da amostra ([[Distribuicao de Bernoulli|variância]] p(1−p) calculada onde H0 diz que a população está).

<pre>
EP = √(p0(1−p0)/n) = √(0,20 × 0,80 / 400) = 0,02
z  = (0,25 − 0,20)/0,02 = 2,5
</pre>

Excel (aba `5_Proporcao`):

<pre>
D6  α          0,05     D7 x 100    D8 n 400    D9 p0 0,20   (azuis)
D10 p̂          =D7/D8
D11 EP         =SQRT(D9*(1-D9)/D8)                -&gt; 0,0200
D12 z          =(D10-D9)/D11                      -&gt; 2,500
D13 z crítico  =NORM.S.INV(1-D6)                  -&gt; 1,645
D14 valor-p    =1-NORM.S.DIST(D12,TRUE)           -&gt; 0,0062
D15 decisão    =IF(D14&lt;D6,"Rejeita H0","Não rejeita H0")
D16 EP errado  =SQRT(D10*(1-D10)/D8)              -&gt; 0,0217 (p̂ no denominador)
D17 z errado   =(D10-D9)/D16                      -&gt; 2,309
</pre>

R (bloco 5). Na mão e depois `prop.test`, que devolve X-squared = z² e o mesmo valor-p quando `correct = FALSE`:

<pre>
x &lt;- 100; n &lt;- 400; p0 &lt;- 0.20; phat &lt;- x / n
z &lt;- (phat - p0) / sqrt(p0 * (1 - p0) / n)
qnorm(1 - alpha); 1 - pnorm(z)
prop.test(x, n, p = p0, alternative = "greater", correct = FALSE)   # X-squared = 2.5^2 = 6.25
prop.test(x, n, p = p0, alternative = "greater")                    # default correct = TRUE
</pre>

<pre>
==== 5. Z proporção (golfe) ====
  p^ = 0.25 | z = 2.5 | crítico = 1.645
  valor-p = 0.00621 &lt; 0.05 -&gt;  REJEITA H0

	1-sample proportions test without continuity correction

data:  x out of n, null probability p0
X-squared = 6.25, df = 1, p-value = 0.00621
alternative hypothesis: true p is greater than 0.2
95 percent confidence interval:
 0.2161476 1.0000000
sample estimates:
   p
0.25

  valor-p com correção de continuidade (default do R): 0.007395
</pre>

Passos 4 e 5. z = 2,5 > 1,645, p = 0,0062 < 0,05: rejeita. Frase do professor: "Há fortes evidências de que a proporção de mulheres passou de 20%. Não dá pra dizer que a proporção agora é 25%: 0,25 é da amostra."

Pegadinhas: p₀ no denominador (com p̂ o z cai pra 2,309, ainda rejeita aqui, mas o número está errado). Crítico unicaudal 1,645, não 1,96. `prop.test` sem `correct = FALSE` aplica correção de continuidade e dá 0,0074 em vez de 0,0062: se o teu R "não bate" com a conta na mão, é isso. E o efeito de n que o professor gosta de cobrar: com n = 1600 e mesmo p̂, EP cai pra 0,01, z dobra pra 5, e fica mais fácil rejeitar ([[Tamanho da amostra]]).

### 4.6 Qui-quadrado de aderência (mix de pagamento)

Enunciado (exercício 1 da aula 5, mesmo do `Script_Aula05.R` do professor): mix esperado de pagamento é crédito 45%, débito 35%, dinheiro 20%. Amostra de 200 compras: 100, 60, 40. Os dados seguem o mix esperado? α = 5%.

Passos 1 e 2. Uma variável categórica com k = 3 categorias contra uma distribuição teórica: [[Teste qui-quadrado de aderencia|aderência]]. H0: a distribuição observada segue 45/35/20. H1: pelo menos uma proporção difere. Qui-quadrado é sempre cauda direita (desvios ao quadrado só somam).

Passo 3. [[Frequencia esperada|Esperadas]] E = n × p sob H0, depois soma dos desvios relativos.

<pre>
E = 200 × (0,45; 0,35; 0,20) = (90; 70; 40)
χ² = (100−90)²/90 + (60−70)²/70 + (40−40)²/40 = 1,111 + 1,429 + 0 = 2,540
gl = k − 1 = 2
</pre>

Excel (aba `6_Qui_Aderencia`, categorias em A4:A6, O em B4:B6, p em C4:C6):

<pre>
B7  n           =SUM(B4:B6)
D4  E           =C4*$B$7   (arrasta até D6)
E4  (O-E)²/E    =(B4-D4)^2/D4   (arrasta até E6)
H6  α           0,05   (azul)
H7  χ²          =SUM(E4:E6)                       -&gt; 2,540
H8  gl          =COUNT(B4:B6)-1                   -&gt; 2
H9  χ² crítico  =CHISQ.INV.RT(H6,H8)              -&gt; 5,991
H10 valor-p     =CHISQ.DIST.RT(H7,H8)             -&gt; 0,2809
H11 decisão     =IF(H10&lt;H6,"Rejeita H0","Não rejeita H0")
H12 atalho      =CHISQ.TEST(B4:B6,D4:D6)          -&gt; 0,2809 (só o valor-p; as esperadas são suas)
</pre>

R (bloco 6). Na mão e depois exatamente a chamada do professor:

<pre>
obs   &lt;- c(Credito = 100, Debito = 60, Dinheiro = 40)
p_exp &lt;- c(0.45, 0.35, 0.20)
esp   &lt;- sum(obs) * p_exp
x2    &lt;- sum((obs - esp)^2 / esp)
qchisq(1 - alpha, 2); pchisq(x2, 2, lower.tail = FALSE)
chisq.test(x = obs, p = p_exp)     # x = contagens observadas, p = proporções de H0
</pre>

<pre>
==== 6. Qui-quadrado aderência (pagamentos) ====
  esperadas: 90 70 40 | qui2 = 2.54 | gl = 2 | crítico = 5.991
  valor-p = 0.2809 &gt;= 0.05 -&gt; NÃO rejeita H0

	Chi-squared test for given probabilities

data:  obs
X-squared = 2.5397, df = 2, p-value = 0.2809
</pre>

Passos 4 e 5. 2,540 < 5,991 e p = 0,2809 > 0,05: não rejeita. Frase (gabarito do professor): "A amostra é consistente com o mix esperado; não há evidência forte de mudança no comportamento de pagamento."

Pegadinhas: gl = k − 1 = 2, não n − 1. =`CHISQ.TEST` devolve o valor-p direto, mas a estatística e as esperadas você tem que mostrar. `chisq.test(x = obs)` sem `p` assume proporções iguais (é o caso do E4).

### 4.7 Qui-quadrado de independência (canal x compra)

Enunciado (exercício 2 da aula 5): 320 leads por canal (Email 120, Social 120, Search 80), com a contagem de quem comprou: 48, 30, 40. A chance de compra depende do canal? α = 5%. Qual canal parece mais forte?

Passos 1 e 2. Duas variáveis categóricas cruzadas numa tabela 3 × 2: [[Teste qui-quadrado de independencia|independência]]. H0: canal e compra são independentes ([[Independencia]] no sentido probabilístico: a proporção de compra é a mesma em todo canal). H1: existe associação.

Passo 3. Esperada de cada célula = (total da linha × total da coluna)/n. gl = (r − 1)(c − 1) = 2 × 1 = 2.

<pre>
              Comprou   Não     Total      Esperadas: Comprou   Não
Email            48      72      120                    44,25   75,75
Social           30      90      120                    44,25   75,75
Search           40      40       80                    29,50   50,50
Total           118     202      320
χ² = Σ (O−E)²/E = 0,318 + 0,186 + 4,589 + 2,681 + 3,737 + 2,183 = 13,694
</pre>

Excel (aba `7_Qui_Independencia`, observado em B4:C6, totais em D4:D6, B7:C7, n em D7):

<pre>
D4  total linha   =SUM(B4:C4)          B7 total coluna  =SUM(B4:B6)      D7 n =SUM(D4:D6)
B10 esperada      =$D$4*B$7/$D$7       (arrasta até C12: $ trava a coluna do total de linha e a linha do total de coluna)
B16 (O-E)²/E      =(B4-B10)^2/B10      (arrasta até C18)
B22 resíduo       =(B4-B10)/SQRT(B10)  (arrasta até C24)
B27 taxa compra   =B4/D4               (arrasta até B29)
G6  α             0,05   (azul)
G7  χ²            =SUM(B16:C18)                          -&gt; 13,694
G8  gl            =(ROWS(B4:C6)-1)*(COLUMNS(B4:C6)-1)    -&gt; 2
G9  χ² crítico    =CHISQ.INV.RT(G6,G8)                   -&gt; 5,991
G10 valor-p       =CHISQ.DIST.RT(G7,G8)                  -&gt; 0,0011
G11 decisão       =IF(G10&lt;G6,"Rejeita H0","Não rejeita H0")
G12 atalho        =CHISQ.TEST(B4:C6,B10:C12)             -&gt; 0,0011
G13 menor E       =MIN(B10:C12)                          -&gt; 29,50 (regra: esperadas ≥ 5)
</pre>

R (bloco 7). A matriz é montada como no script do professor; `chisq.test(tab)` faz o resto e ainda entrega esperadas e resíduos:

<pre>
tab &lt;- matrix(c(48, 72,
                30, 90,
                40, 40), nrow = 3, byrow = TRUE)
dimnames(tab) &lt;- list(Canal = c("Email", "Social", "Search"), Compra = c("Comprou", "NaoComprou"))
esp &lt;- outer(rowSums(tab), colSums(tab)) / sum(tab)     # E_ij = linha x coluna / n
x2  &lt;- sum((tab - esp)^2 / esp)
qchisq(0.95, 2); pchisq(x2, 2, lower.tail = FALSE)
res &lt;- chisq.test(tab)
res; res$expected; res$residuals; prop.table(tab, 1)
</pre>

<pre>
==== 7. Qui-quadrado independência (canal x compra) ====
  qui2 = 13.694 | gl = 2 | crítico = 5.991
  valor-p = 0.001063 &lt; 0.05 -&gt;  REJEITA H0

	Pearson's Chi-squared test

data:  tab
X-squared = 13.694, df = 2, p-value = 0.001063

  esperadas:
        Compra
Canal    Comprou NaoComprou
  Email    44.25      75.75
  Social   44.25      75.75
  Search   29.50      50.50
  resíduos (O-E)/sqrt(E): sinal e tamanho dizem qual célula puxa o qui2
        Compra
Canal    Comprou NaoComprou
  Email     0.56      -0.43
  Social   -2.14       1.64
  Search    1.93      -1.48
  taxa de compra por canal:
 Email Social Search
  0.40   0.25   0.50
</pre>

Passos 4 e 5. 13,694 > 5,991 e p = 0,0011: rejeita. Frase (gabarito do professor): "A probabilidade de compra depende do canal. Search é o mais forte (50% compraram, contra 40% no email e 25% no social)." Os resíduos dizem o mesmo: Search comprou mais que o esperado (+1,93), Social muito menos (−2,14).

Pegadinhas: gl = (r−1)(c−1), não k − 1. Esperadas abaixo de 5 em muitas células invalidam a aproximação: é o exercício 3 do professor (loja C com 30 leads), em que o R avisa `Chi-squared approximation may be incorrect` e as saídas são juntar categorias ou usar teste exato de Fisher em 2 × 2. Independência e homogeneidade usam a mesma conta; muda só a pergunta.

## 5. Exercícios (faça nas duas ferramentas antes de olhar o gabarito)

Dados também na aba `Exercicios` do xlsx e na seção 8 do `TestesHipotese.R`. Pra cada um: os 5 passos, crítico e valor-p, frase de interpretação.

**E1.** Tempo de atendimento do professor (aula 2). Histórico: 10 min. Amostra de 12 atendimentos: 9,7  10,2  10,4  9,9  10,1  10,5  9,8  10,3  10,0  10,2  10,4  10,1. A média mudou? α = 5%. Confere com o Resumo de 08.07.

**E2.** A taxa de conversão do site era 30%. Com a landing nova, 90 conversões em 250 visitas. A conversão mudou? Decide a 5% e a 1%.

**E3.** Dois enunciados. Antes de calcular, decide qual teste é.
E3a: as mesmas 10 pessoas foram cronometradas numa tarefa (min) antes e depois de um treinamento. Antes: 35,6  26,5  29,3  35,4  23,0  25,4  39,8  29,6  29,4  28,2. Depois: 33,2  26,3  23,4  30,6  14,8  21,7  26,6  27,1  21,5  15,3. O treinamento reduziu o tempo? α = 5%.
E3b: notas de duas turmas diferentes. Turma A (12): 5,9  8,3  10,0  3,9  7,4  3,8  5,5  7,4  6,3  6,4  4,5  4,2. Turma B (14): 7,3  8,2  7,0  9,4  6,2  9,4  8,1  6,9  7,2  9,4  7,3  6,8  6,6  7,1. As médias diferem? α = 5%.

**E4.** Slide da aula 5: a empresa acredita em preferência uniforme por 4 sabores (25% cada). Amostra de 80: A 18, B 22, C 20, D 20. A preferência é uniforme? α = 5%.

## 6. Pegadinhas consolidadas e frases de interpretação

Na ordem em que o professor martelou:

- Unicaudal a 5% usa 1,645 (os 5% inteiros numa cauda). 1,96 é o [[Z de alfa sobre 2]] do bicaudal (2,5% em cada cauda). Mesma lógica em t: =`T.INV(1-α,gl)` vs =`T.INV.2T(α,gl)`.
- Na proporção, o erro-padrão usa p₀ da hipótese no denominador, não p̂ da amostra.
- Interpretação vale nota. Rejeitar H0 dá evidência de que o parâmetro passou do baseline; não diz qual é o valor novo (0,25, 520, 49,66 são da amostra). Não rejeitar não prova H0: só diz que a amostra não bastou.
- n maior, tudo mais igual: [[Erro padrao|erro-padrão]] menor, estatística maior, mais fácil rejeitar. "Essa a gente gosta de colocar no quiz."
- α = P([[Erro Tipo I]]) = rejeitar H0 verdadeira. Não é a probabilidade de H0 ser falsa. Baixar α reduz Tipo I e aumenta [[Erro Tipo II]] (com n fixo).
- A cauda vem do enunciado. Satisfação 6,8 vs 7,0: bicaudal não rejeita, unicaudal esquerda rejeita.
- Crítico e valor-p são caminhos equivalentes pra mesma decisão. A prova cobra os dois.
- Z só é exato com σ populacional dado; com s da amostra é t com gl = n − 1.
- =`T.DIST.2T` exige t ≥ 0 (use =`ABS`). =`T.INV(α,gl)` devolve o crítico da esquerda, negativo. =`STDEV.S`, não =`STDEV.P`.
- =`T.TEST` com caudas=1 devolve a cauda de |t| e não sabe a direção de H1. Confere o sinal.
- `prop.test` corrige continuidade por default; `correct = FALSE` bate com a conta na mão.
- Excel trunca gl não inteiro (Welch): valor-p difere do R na 3ª casa. =`T.TEST(A,B,2,3)` usa gl fracionário.
- Qui-quadrado é sempre cauda direita. gl = k − 1 (aderência) ou (r − 1)(c − 1) (independência). Esperadas ≥ 5. =`CHISQ.TEST` devolve o valor-p, não a estatística.
- Pareado vs independentes: mesmas unidades duas vezes é pareado; grupos diferentes é Welch. Errar isso é errar o teste inteiro.

Frases modelo (troca o que está entre colchetes):

- Rejeita, unicaudal: "Ao nível de [5%], há evidência de que [a média/proporção] [superou/ficou abaixo de] [baseline]. O valor [x̄/p̂] é da amostra, não o novo valor populacional."
- Não rejeita: "Ao nível de [5%], a amostra não dá evidência suficiente de que [parâmetro] [mudou/aumentou]. Isso não prova que [H0] é verdadeira."
- Bicaudal: "Ao nível de [5%], há evidência de que [parâmetro] é diferente de [baseline] (valor-p [p] < 0,05)."
- Qui-quadrado: "Ao nível de [5%], há evidência de que [a distribuição difere do esperado / as variáveis estão associadas]; [categoria] é a que mais contribui (resíduo [r])."

---

## 7. Gabarito (só depois de tentar)

| # | Teste | Estatística | Crítico (5%) | Valor-p | Decisão |
|---|---|---|---|---|---|
| E1 | t uma média, bicaudal, gl 11 | t = 1,849 | ±2,201 | 0,0915 | não rejeita: a amostra não dá evidência de que a média mudou de 10 min |
| E2 | Z proporção, bicaudal, p̂ = 0,36 | z = 2,07 | ±1,960 (5%), ±2,576 (1%) | 0,0384 | rejeita a 5%, não rejeita a 1% |
| E3a | t pareado, D = Depois − Antes, unicaudal esquerda, gl 9 | t = −4,448 (D̄ = −6,17) | −1,833 | 0,0008 | rejeita: há evidência de que o treinamento reduziu o tempo |
| E3b | Welch bicaudal, gl 16,84 | t = −2,408 | ±2,111 | 0,0278 | rejeita a 5%: as médias das turmas diferem |
| E4 | qui-quadrado aderência, gl 3 | χ² = 0,4 | 7,815 | 0,9402 | não rejeita: consistente com preferência uniforme |

Em R, uma linha cada: `t.test(e1_atend, mu = 10)`; `2*(1-pnorm(abs((90/250-0.3)/sqrt(0.3*0.7/250))))`; `t.test(e3a_depois, e3a_antes, paired = TRUE, alternative = "less")`; `t.test(e3b_A, e3b_B)`; `chisq.test(e4_obs)`. Em Excel, cada um é o bloco da aba correspondente com os dados da aba `Exercicios`.
