# Lista 3, Distribuições Discretas, Gabarito

**Conceitos cobertos:** [[Variavel aleatoria discreta]] · [[Valor esperado]] · [[Variancia e desvio padrao]] · [[Distribuicao binomial]] · [[Independencia]] · [[Transformacao linear de variavel aleatoria]] · [[Funcao de variavel aleatoria]]

---

## Pergunta 1

**Explicação**

[[Variavel aleatoria discreta]] com 4 valores possíveis. Toda distribuição de probabilidade tem que somar 1, então quando falta uma probabilidade, é só tirar das outras (1 menos a soma das conhecidas). Depois calcula o [[Valor esperado]], que é a média ponderada dos valores pelos seus pesos (probabilidades). É o "centro de massa" da distribuição. Em finanças, isso é o retorno esperado de um ativo dado um cenário probabilístico.

Fórmula: E(X) = Σ x · P(x).

**Setup**

Soma das probabilidades = 1, então P(X=0) = 1 - 0,25 - 0,25 - 0,10 = **0,40**.

**Excel**

| A (Retorno) | B (Probab) |
|-------------|------------|
| -1000       | 0,25       |
| 0           | 0,40       |
| 1000        | 0,25       |
| 2000        | 0,10       |

E(X) usando SOMARPRODUTO (multiplica linha a linha e soma):

<pre>=SOMARPRODUTO(A2:A5;B2:B5)</pre>

**Conta na mão**

E(X) = (-1000)(0,25) + (0)(0,40) + (1000)(0,25) + (2000)(0,10)
     = -250 + 0 + 250 + 200
     = **200**

**Resposta:** R$ 200

---

## Pergunta 2

**Explicação**

A PMF (função de probabilidade) é dada como uma fórmula em x, não como tabela. Primeiro avalia f(x) em cada valor inteiro do suporte (0 a 4), depois confirma que soma 1 (validação obrigatória de toda PMF, ver [[Variavel aleatoria discreta]]). Daí calcula [[Valor esperado|E(X)]], E(X²) e usa a fórmula curta da [[Variancia e desvio padrao|variância]]: Var(X) = E(X²) − [E(X)]². DP é a raiz da variância.

A segunda parte testa [[Independencia|independência]]. Se duas tarefas são independentes, P(A ∩ B) = P(A) · P(B). Aqui A = "tarefa 1 termina em <3 dias", B = "tarefa 2 termina em <3 dias". Como A e B têm a mesma distribuição, P(ambas) = P(A)².

**Setup**

f(x) = 0,05x + 0,1, x ∈ {0, 1, 2, 3, 4}.

| x | f(x) = 0,05x + 0,1 |
|---|--------------------|
| 0 | 0,10               |
| 1 | 0,15               |
| 2 | 0,20               |
| 3 | 0,25               |
| 4 | 0,30               |

Soma = 1,00, válido.

**Excel**

Coluna A: x, coluna B: f(x), coluna C: x·f(x), coluna D: x²·f(x).

<pre>
B2: =0,05*A2+0,1
C2: =A2*B2
D2: =A2^2*B2

E(X):     =SOMA(C2:C6)        ou  =SOMARPRODUTO(A2:A6;B2:B6)
E(X²):    =SOMA(D2:D6)
Var(X):   =E(X^2) - E(X)^2
DP(X):    =RAIZ(Var)
</pre>

**Conta na mão**

E(X) = 0(0,10) + 1(0,15) + 2(0,20) + 3(0,25) + 4(0,30)
     = 0 + 0,15 + 0,40 + 0,75 + 1,20 = **2,50**

E(X²) = 0(0,10) + 1(0,15) + 4(0,20) + 9(0,25) + 16(0,30)
      = 0 + 0,15 + 0,80 + 2,25 + 4,80 = **8,00**

Var(X) = 8,00 - 2,50² = 8,00 - 6,25 = **1,75**

DP(X) = √1,75 ≈ **1,3229**

**Probabilidade de ambas terminarem em menos de 3 dias**

P(X<3) = P(0) + P(1) + P(2) = 0,10 + 0,15 + 0,20 = 0,45

Tarefas independentes, então:

P(ambas < 3) = 0,45² = **0,2025** (20,25%)

Excel:

<pre>=0,45^2</pre>

---

## Pergunta 3

**Explicação**

Mesmo conceito da Pergunta 1, sem o passo de achar a probabilidade faltando. Distribuição já completa, é só aplicar [[Valor esperado|E(R) = Σ r · P(r)]]. Em finanças, esse é exatamente o cálculo de retorno esperado de um ativo com cenários probabilísticos atribuídos por um analista.

**Excel**

<pre>=SOMARPRODUTO(A2:A7;B2:B7)</pre>

com A = retornos (5%, 6%, ..., 10%) e B = probabilidades.

**Conta na mão**

E(R) = 5(0,1) + 6(0,2) + 7(0,3) + 8(0,2) + 9(0,1) + 10(0,1)
     = 0,5 + 1,2 + 2,1 + 1,6 + 0,9 + 1,0
     = **7,3%**

**Resposta:** 7,3%

---

## Pergunta 4

**Explicação**

Pergunta de finanças disfarçada de estatística. "Risco" em portfólio finance é tradicionalmente medido pelo [[Variancia e desvio padrao|desvio padrão]] dos retornos: ele mede o quanto os retornos se desviam do esperado, ou seja, a volatilidade. Menor DP = retornos mais previsíveis = menor risco.

Atenção: investimentos podem ter retorno esperado parecido mas DP muito diferente. Comparar só pela média é erro clássico. Tem que calcular E e Var dos três e ranquear pelo DP.

A fórmula é a de sempre: [[Valor esperado|E(X) = Σ x · P(x)]], [[Variancia e desvio padrao|Var(X) = E(X²) − [E(X)]²]], DP = √Var.

**Estratégia em Excel**

Monta cada investimento em colunas A (retorno) e B (probabilidade) e replica:

<pre>
E(X):    =SOMARPRODUTO(A:A; B:B)
E(X²):   =SOMARPRODUTO(A:A^2; B:B)
Var:     =E(X^2) - E(X)^2
DP:      =RAIZ(Var)
</pre>

**Investimento A**

E(A) = 5(0,1) + 6(0,2) + 7(0,3) + 8(0,2) + 9(0,1) + 10(0,1) = 7,30
E(A²) = 25(0,1) + 36(0,2) + 49(0,3) + 64(0,2) + 81(0,1) + 100(0,1) = 55,30
Var(A) = 55,30 - 7,30² = 55,30 - 53,29 = 2,01
DP(A) = √2,01 ≈ **1,418**

**Investimento B**

E(B) = 5(0,3) + 6(0,2) + 6,5(0,1) + 7(0,1) + 8(0,1) + 9(0,2) = 6,65
E(B²) = 25(0,3) + 36(0,2) + 42,25(0,1) + 49(0,1) + 64(0,1) + 81(0,2) = 46,425
Var(B) = 46,425 - 6,65² = 46,425 - 44,2225 = 2,2025
DP(B) = √2,2025 ≈ **1,484**

**Investimento C**

E(C) = 4(0,05) + 6(0,1) + 7(0,4) + 8(0,3) + 9(0,1) + 11(0,05) = 7,45
E(C²) = 16(0,05) + 36(0,1) + 49(0,4) + 64(0,3) + 81(0,1) + 121(0,05) = 57,35
Var(C) = 57,35 - 7,45² = 57,35 - 55,5025 = 1,8475
DP(C) = √1,8475 ≈ **1,359**

**Comparação**

| Inv | E    | DP    |
|-----|------|-------|
| A   | 7,30 | 1,418 |
| B   | 6,65 | 1,484 |
| C   | 7,45 | **1,359** |

C tem o melhor cenário de todos: maior retorno esperado **e** menor risco. Domina os outros dois.

**Resposta:** C tem o menor risco.

---

## Pergunta 5

**Explicação**

[[Funcao de variavel aleatoria]]. Y é definido como uma função de X, com regra condicional: se X ≥ 3, aplica desconto. Isso é o equivalente discreto de uma transformação não-linear (a regra de desconto cria uma quebra na função).

Estratégia: pra cada valor de X possível, calcula o Y correspondente. Depois aplica E(Y) = Σ y · P(X) usando a probabilidade de X (não muda, é a mesma). Importante: NÃO dá pra fazer E(Y) = E(X) · 35 com o desconto médio, porque o desconto é não-linear (só ativa em X ≥ 3). Tem que computar Y caso a caso.

E(X) é direto, fórmula padrão.

**E(X)**

E(X) = 0(0,30) + 1(0,30) + 2(0,20) + 3(0,10) + 4(0,10)
     = 0 + 0,30 + 0,40 + 0,30 + 0,40 = **1,40**

**Construção de Y**

Y depende de X com a regra do desconto. Pra X ≥ 3 aplica desconto de 20% (multiplica por 0,8).

| X | Camisas × 35 | Y                  |
|---|--------------|--------------------|
| 0 | 0            | 0                  |
| 1 | 35           | 35                 |
| 2 | 70           | 70                 |
| 3 | 105          | 105 × 0,8 = 84     |
| 4 | 140          | 140 × 0,8 = 112    |

E(Y) = 0(0,30) + 35(0,30) + 70(0,20) + 84(0,10) + 112(0,10)
     = 0 + 10,50 + 14,00 + 8,40 + 11,20 = **44,10**

**Excel**

Monta tabela com X em A, P(X) em B, Y(X) em C. A coluna C usa a fórmula condicional do desconto, daí E(X) e E(Y) saem por SOMARPRODUTO.

<pre>
C2: =SE(A2>=3; A2*35*0,8; A2*35)

E(X):  =SOMARPRODUTO(A2:A6; B2:B6)
E(Y):  =SOMARPRODUTO(C2:C6; B2:B6)
</pre>

**Resposta:** E(X) = 1,4 e E(Y) = 44,1

---

## Pergunta 6

**Explicação**

[[Transformacao linear de variavel aleatoria]]. C é função afim de Y: C = a + bY (com a=1,5 e b=0,8).

Propriedades importantes (decorar):
- E(a + bY) = a + b · E(Y), ou seja, esperança é linear, passa direto.
- Var(a + bY) = b² · Var(Y). A constante aditiva (a) some, porque deslocar tudo não muda a dispersão. A constante multiplicativa (b) entra ao quadrado, porque variância tem unidade ao quadrado.

Pegadinha clássica: gente esquece que **a** some na variância e/ou esquece de elevar **b** ao quadrado. As alternativas erradas testam exatamente isso (95,4 e 9,5 = errou aplicando b sem quadrado; 81,5 e 8,0 = errou usando b sem quadrado mas E correto; 81,5 e 7,9 = chute próximo).

**Aplicação**

C = 1,5 + 0,8Y

E(C) = 1,5 + 0,8 · E(Y) = 1,5 + 0,8(100) = **81,5**

Var(C) = 0,8² · Var(Y) = 0,64 · 10 = **6,4**

**Resposta:** 81,5 e 6,4

---

## Pergunta 7

**Explicação**

[[Distribuicao binomial]]. Como reconhecer: você tem n ensaios [[Independencia|independentes]], cada um com mesma probabilidade p de "sucesso", e quer contar quantos sucessos no total.

Aqui: n = 20 estudantes, p = 0,20 de desistir, X = número de desistentes. X ~ Binomial(20, 0,20).

A pergunta é P(X ≤ 3), probabilidade acumulada (CDF). No Excel, DISTR.BINOM.N com último argumento VERDADEIRO já entrega isso direto.

PMF binomial: P(X = k) = C(n,k) · p^k · (1−p)^(n−k).

A obs do enunciado pede resposta com 2 decimais, então 0,4114 vira 0,41.

**Excel (resposta direta)**

<pre>=DISTR.BINOM.N(3; 20; 0,2; VERDADEIRO)</pre>

(em versões antigas do Excel: DISTBINOM com os mesmos argumentos)

O argumento VERDADEIRO faz a função retornar a CDF, ou seja, P(X ≤ 3) já acumulado. Resultado ≈ **0,4114**.

**Conta na mão**

P(X=k) = C(20,k) · (0,2)^k · (0,8)^(20-k)

| k | C(20,k) | (0,2)^k | (0,8)^(20-k) | P(X=k)   |
|---|---------|---------|--------------|----------|
| 0 | 1       | 1       | 0,011529     | 0,01153  |
| 1 | 20      | 0,2     | 0,014412     | 0,05765  |
| 2 | 190     | 0,04    | 0,018014     | 0,13691  |
| 3 | 1140    | 0,008   | 0,022518     | 0,20536  |

Soma = **0,41145**

**Resposta:** 0,41

---

## Pergunta 8

**Explicação**

Mais uma [[Distribuicao binomial|binomial]]. n = 10 perguntas, p = 1/5 = 0,20 de acertar chutando (5 alternativas, só 1 correta). X = acertos. X ~ Binomial(10, 0,2).

Pergunta: P(X ≥ 4). Truque: somar de 4 até 10 dá trabalho (7 termos). Usa o complemento: P(X ≥ 4) = 1 − P(X ≤ 3). Só 4 termos pra calcular.

Saca o valor esperado pra ter intuição: E(X) = n·p = 10·0,2 = 2 acertos. Quatro acertos é bem acima da média, então a probabilidade tem que ser baixa. Isso elimina alternativas absurdas tipo 79,9% ou 87,9%.

**Excel**

<pre>=1 - DISTR.BINOM.N(3; 10; 0,2; VERDADEIRO)</pre>

Resultado ≈ **0,1209** (12,09%).

**Conta na mão**

P(X=0) = (0,8)^10 = 0,1074
P(X=1) = 10 · 0,2 · (0,8)^9 = 0,2684
P(X=2) = 45 · 0,04 · (0,8)^8 = 0,3020
P(X=3) = 120 · 0,008 · (0,8)^7 = 0,2013

P(X ≤ 3) = 0,1074 + 0,2684 + 0,3020 + 0,2013 = 0,8791

P(X ≥ 4) = 1 - 0,8791 = **0,1209** (12,1%)

**Resposta:** 12,1%

---

## Pergunta 9

**Explicação**

Problema de inventário/dimensionamento usando [[Distribuicao binomial|binomial]] inversa. X ~ Binomial(200, 0,6) é o número de passageiros que querem chicken. Queremos achar quantos pratos preparar (k) pra que falte com no máximo 5% de chance.

Formalmente: o menor k tal que P(X > k) ≤ 0,05, ou seja P(X ≤ k) ≥ 0,95.

Isso é o quantil 95% da distribuição binomial. Em finanças seria o equivalente de um VaR 95% (quantos pratos perder com 5% de chance vs quantos reais perder com 5% de chance).

Caminho 1: função **INV.BINOM** direto, retorna o quantil.

Caminho 2 (que o enunciado pediu): tentativa e erro com a CDF. Lista k de 120 a 135, calcula P(X ≤ k) pra cada, acha o primeiro que cruza 0,95.

Sanity check pela aproximação normal: μ = np = 120, σ = √(npq) = √48 ≈ 6,93. Quantil 95% ≈ μ + 1,645σ ≈ 131,4. Bate com 131.

**Excel (atalho)**

<pre>=INV.BINOM(200; 0,6; 0,95)</pre>

Retorna 131 direto. (em inglês a função se chama BINOM.INV com os mesmos argumentos)

**Excel (tentativa e erro, como o enunciado pediu)**

Monta uma coluna com k = 120, 121, 122, ..., 135 e ao lado calcula a CDF:

<pre>=DISTR.BINOM.N(k; 200; 0,6; VERDADEIRO)</pre>

Procura o primeiro k com valor ≥ 0,95.

| k   | P(X ≤ k) |
|-----|----------|
| 128 | 0,873    |
| 129 | 0,902    |
| 130 | 0,927    |
| 131 | **0,948** ≈ 0,95 |
| 132 | 0,964    |

Em k=131 a probabilidade de faltar (P(X > 131)) já está em torno de 5%.

**Resposta:** 131

---

## Pergunta 10

**Explicação**

Embrião de teste de hipótese, usando [[Distribuicao binomial|binomial]] pontual. A pergunta é: dado que o sorteio é supostamente aleatório (com p = 0,8 de câmera desligada por aluno), qual a probabilidade de observar o evento "todos com câmera desligada"?

Cada sorteio é Bernoulli [[Independencia|independente]] (com reposição), então X = número de câmeras desligadas em n sorteados é Binomial(n, 0,8). O evento "todos desligados" é X = n, com probabilidade exata (0,8)^n (porque C(n,n) = 1).

Lógica do teste: se a probabilidade desse evento sob a hipótese de aleatoriedade for muito baixa (tipicamente < 5%), rejeita a hipótese. Se for alta, não rejeita. Os 5% e 1% são níveis de significância padrão. Isso é a base de p-value.

Parte (a): n = 10 dá probabilidade 10,74%. Não dá pra rejeitar, porque é uma probabilidade comum (acontece em 1 a cada 10 aulas). O resultado é compatível com aleatoriedade.

Parte (b): qual o n mínimo pra a probabilidade cair abaixo do limiar de significância? Resolve a inequação (0,8)^n < 0,05 isolando n com logaritmo. Resultado: n = 14 já é suficiente a 5%.

**Modelagem**

X ~ Binomial(n, 0,8), evento de interesse: X = n.

P(X = n) = (0,8)^n

**Excel**

<pre>=POTÊNCIA(0,8; n)</pre>

ou equivalente, usando a binomial pontual (último argumento FALSO retorna probabilidade pontual, não acumulada):

<pre>=DISTR.BINOM.N(n; n; 0,8; FALSO)</pre>

**Parte (a), n = 10**

P(X = 10 | sorteio aleatório) = (0,8)^10 = **0,1074** (10,74%).

10,74% é uma probabilidade alta demais pra rejeitar aleatoriedade. Pelo padrão de 5% de significância, o resultado não rejeita. Em termos práticos, num sorteio honesto isso aconteceria em cerca de 1 a cada 10 aulas, então não é evidência contra o professor.

**Parte (b)**

Quero o menor n tal que (0,8)^n < 0,05 (significância 5%):

n · ln(0,8) < ln(0,05)
n > ln(0,05) / ln(0,8) = -2,996 / -0,2231 ≈ **13,42**

Então n = 14 já dá P = (0,8)^14 ≈ 0,0440 (4,40%), abaixo de 5%.

| n  | (0,8)^n  |
|----|----------|
| 12 | 0,0687   |
| 13 | 0,0550   |
| 14 | **0,0440** |
| 15 | 0,0352   |

**A partir de n = 14** dá pra dizer, com 95% de confiança, que o sorteio não está sendo aleatório.

(Se quisesse ser mais rigoroso, com 99% de confiança, precisaria de n = 21, porque (0,8)^21 ≈ 0,0092 < 0,01.)
