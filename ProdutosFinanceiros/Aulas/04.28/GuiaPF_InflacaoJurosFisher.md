# Guia de Estudos: Inflação, Juros Real e Identidade de Fisher

Calibrado pela Aula 10 do De Genaro (08.04.26). Cada bloco tem intuição, derivação, exemplo resolvido passo a passo (com fórmula Excel em PT-BR pra colar) e checagem de domínio.

**Convenção Excel BR**: separador de argumentos é ponto-vírgula (`;`), decimal é vírgula (`,`), `^` ou `POTÊNCIA(base;exp)` pra potência. `VPL(taxa;v1;v2;...)` desconta os valores começando em t=1, então pra fluxo em t=0 some fora: `=v0 + VPL(taxa;v1;v2;...)`.

---

## Bloco 1. O que é inflação e por que medimos

### A intuição
Inflação é a perda de poder de compra do dinheiro. Quando você ouve "a inflação foi de 5% no ano", isso significa que a cesta de produtos que custava R$100 no começo do ano custa R$105 no fim. Os mesmos R$100 valem menos.

Isso importa pra finanças por uma razão direta. Se você aplicou R$1.000 e recebeu R$1.040 num ano em que a inflação foi 5%, você nominalmente "ganhou" R$40. Mas seu poder de compra caiu. Antes, R$1.000 compravam algo. Agora, R$1.040 não compram nem o equivalente. Você empobreceu, mesmo com retorno positivo no extrato.

A consequência prática: nunca dá pra avaliar um investimento só pelo retorno nominal. Tem que descontar a inflação. Esse desconto é o juro real, e a ponte entre nominal e real é a identidade de Fisher, que vamos derivar no bloco 2.

### Como o Brasil mede inflação
Existem vários índices porque cada um responde uma pergunta diferente: inflação de quem? IPCA e INPC são os dois cobertos na aula.

**IPCA** (Índice de Preços ao Consumidor Amplo). Calculado pelo IBGE. Cesta representa famílias com renda de 1 a 40 salários mínimos. Coletado em 13 áreas metropolitanas: Belém, Fortaleza, Recife, Salvador, BH, Vitória, RJ, SP, Curitiba, POA, DF, Goiânia e Campo Grande. É o índice oficial do regime de metas, ou seja, é o que o Bacen tem que manter dentro do alvo.

**INPC** (Índice Nacional de Preços ao Consumidor). Mesmo IBGE, mesmas 13 áreas. Cesta representa famílias com renda de 1 a 5 salários mínimos. Usado pra reajuste de salário mínimo e benefícios da previdência.

Por que dão valores diferentes? Dois motivos.

Primeiro, os pesos dos grupos de produtos são distintos. INPC pesa mais Alimentos (31,11% vs 25,52% do IPCA) e Habitação. Isso reflete que famílias de baixa renda gastam proporção maior do orçamento em comida e moradia. IPCA pesa mais Transportes e Educação. Quando os preços de Alimentos sobem mais que os de Transportes, INPC mostra inflação maior, e vice-versa.

Segundo, os pesos das regiões são diferentes. IPCA dá peso de 30,67% pra SP e 12,06% pro RJ. INPC redistribui mais peso pras capitais nordestinas. Choques regionais distintos puxam os índices em direções opostas.

A pergunta clássica de prova: "por que dois índices que medem inflação dão números diferentes no mesmo mês?". Resposta: cestas com pesos diferentes, tanto por grupo de produto quanto por região metropolitana.

### Histórico relevante
A história relevante pra prova é a sequência de regimes monetários:

Antes de 1994 vieram tentativas falhas com congelamento de preços (Cruzado, Bresser, Verão) e com confisco de depósitos (Collor). Tratavam sintoma, não causa, e a inflação voltava com força. O pico foi em 1990, com inflação de 12 meses passando de 6.700% no IPCA.

O Plano Real, de julho de 1994, atacou a indexação e usou âncora cambial. Entre julho de 1994 e janeiro de 1999, o real teve paridade próxima a 1 USD = 1 BRL. Essa âncora segurou a inflação.

Em fevereiro de 1999, com a desvalorização cambial, a âncora caiu e o Brasil adotou o regime de metas de inflação, que é o que vigora até hoje. Nesse regime, o CMN define a meta e o Bacen executa via taxa Selic através do Copom. Os canais pelos quais a Selic afeta inflação são cinco: consumo e investimento (juro alto desestimula gasto), crédito (encarece empréstimo), expectativas (sinaliza compromisso), câmbio (juro alto valoriza moeda) e riqueza (afeta preço de ativos).

### Como calcular inflação em diferentes prazos

**Inflação no período**:
```
π = P_final / P_inicial - 1
```
Excel BR: `=P_final/P_inicial-1`

**Acumular inflações de subperíodos** (composição multiplicativa, nunca soma):
```
(1 + π_total) = (1 + π_1)(1 + π_2)...(1 + π_n)
π_total = ∏(1 + π_t) - 1
```
Excel BR: `=(1+π_1)*(1+π_2)*(1+π_3)-1`
Forma com função: `=PRODUTO(1+A1;1+A2;1+A3)-1`

A razão da multiplicação é que cada inflação age sobre o nível de preços que já foi inflado pela inflação anterior. Se janeiro teve 1% e fevereiro teve 1%, no fim de fevereiro os preços não estão 2% acima de dezembro, estão 1,01 × 1,01 - 1 = 2,01% acima. O extra de 0,01 ponto vem do efeito composto, e ele cresce muito quando os números são maiores.

**Anualizar uma inflação de período**:
```
π_anual = (1 + π_total)^(1/anos) - 1
```
Excel BR: `=(1+π_total)^(1/anos)-1`
Ou: `=POTÊNCIA(1+π_total;1/anos)-1`

Pra mensal vira anual: `=POTÊNCIA(1+π_mensal;12)-1`.

**Exemplo da aula (slide 18 e 19)**. Um produto custava R$100 no ano 0 e custava R$120 no fim do ano 2.

Inflação acumulada:
```
π = 120/100 - 1 = 20%
```
Excel BR: `=120/100-1` → 0,2 (20%)

Inflação anual equivalente:
```
π_a = (1,20)^(1/2) - 1 = 9,54% a.a.
```
Excel BR: `=(1+20%)^(1/2)-1`
Ou: `=POTÊNCIA(1,2;1/2)-1` → 0,0954 (9,54%)

**Outro exemplo (slide 20 e 21)**. IPCA mensal jan/fev/mar 2023 foi 0,53%, 0,84%, 0,71%.

Inflação trimestral acumulada:
```
π_trim = (1,0053)(1,0084)(1,0071) - 1 = 2,0942%
```
Excel BR: `=(1+0,53%)*(1+0,84%)*(1+0,71%)-1` → 0,020942 (2,0942%)

Note que somar daria 2,08%. A diferença vem do efeito composto.

### Domínio do bloco 1
Você precisa conseguir, sem consulta:
- Definir inflação em uma frase
- Listar IPCA e INPC com cesta e função
- Explicar por que dois índices divergem no mesmo mês (pesos de grupo e região)
- Dizer quando começou o regime de metas (fevereiro de 1999) e quem define meta vs quem executa
- Calcular inflação acumulada multiplicando (1+π_t)
- Anualizar uma inflação de período usando potência (1/anos), não multiplicação

---

## Bloco 2. Juros nominal vs juros real

### A intuição
A taxa que aparece na tela do banco, no contrato do CDB ou no título público é a taxa nominal. Ela diz quanto seu saldo cresce em reais. Mas reais valem menos a cada ano. Pra saber quanto seu poder de compra cresce de verdade, você desconta a inflação. Isso te dá a taxa real.

Pensa no exemplo concreto. Você emprestou R$1.000 a 10% por um ano e recebe R$1.100 no fim. Se a inflação foi 8%, os R$1.100 do fim valem o que valeriam R$1.100 / 1,08 = R$1.018,52 hoje, em poder de compra equivalente. Em termos reais, seu R$1.000 virou R$1.018,52, ou seja, cresceu 1,85%. Esse 1,85% é seu juro real. Não é o 10% do contrato.

```
Excel BR: =1100/1,08 → 1018,52
         =1018,52/1000-1 → 0,0185 (1,85%)
```

A regra geral. Juros nominal mede o crescimento dos reais. Juros real mede o crescimento do poder de compra. Os dois nem sempre andam juntos.

Casos importantes:
- Nominal maior que inflação: juros real positivo, ganho de poder de compra
- Nominal menor que inflação: juros real negativo, perda de poder de compra
- Nominal igual à inflação: juros real zero, neutralidade

### Identidade de Fisher (a ponte entre nominal e real)
Fisher mostra que crescer um saldo em termos nominais é equivalente a corrigir o saldo pela inflação e depois aplicar o juro real:

```
(1 + i) = (1 + π) × (1 + r)
```

Onde i é nominal, π é inflação no período, r é juros real.

A intuição da multiplicação. Imagina seu R$1 hoje. Pra ter o mesmo poder de compra daqui a um ano, sob inflação π, você precisa de (1 + π) reais nominais. Pra ter ganho real de r em cima desse poder de compra preservado, você multiplica de novo por (1 + r). O total: (1 + π)(1 + r). Esse total tem que igualar (1 + i), porque é assim que seu saldo cresce em reais ao longo do ano.

Reorganizando pra isolar o juro real:
```
r = (1 + i) / (1 + π) - 1
```
Excel BR: `=(1+i)/(1+π)-1`

Essa é a fórmula que você vai usar mais. Sempre que a prova der nominal e inflação, você acha o real por essa.

### A aproximação r ≈ i - π e seus limites
Expandindo Fisher:
```
1 + i = 1 + π + r + π·r
i = π + r + π·r
```

O termo π·r é o "termo cruzado". Quando π e r são pequenos (ambos abaixo de 5%), o produto deles é desprezível. Aí vale a aproximação:
```
r ≈ i - π
```
Excel BR: `=i-π`

Mas em cenário de inflação alta isso quebra. Brasil dos anos 80 e 90 tinha inflação anual de 100%, 1.000%, 6.000%. A aproximação ali daria erro absurdo. Mesmo hoje, se um exercício do quiz tem π de 8% ou 10%, a aproximação introduz erro perceptível.

A regra prática pra prova: use sempre a forma exata.

### Exemplo resolvido 1 (slide 25)
**Enunciado**. José investiu a 5,25% a.a. nominal. Inflação foi 8% no ano. Qual o juro real?

**Resolução**. Aplica Fisher pra isolar r:
```
r = 1,0525 / 1,08 - 1 = -2,55%
```

Excel BR:
```
=(1+5,25%)/(1+8%)-1     → -0,0255  (-2,55%)
=1,0525/1,08-1          → mesmo resultado
```

**Conclusão**. José perdeu poder de compra. Mesmo com retorno positivo de 5,25% no extrato, em termos reais ele ficou 2,55% mais pobre. A pegadinha desse exercício é a inflação ser maior que o nominal, forçando você a perceber que o real é negativo. Aproximação aqui daria -2,75% (`=5,25%-8%`), próximo mas errado.

### Exemplo resolvido 2 (slides 26 e 27, Securato 2.27)
**Enunciado**. Investidor aplicou $500.000 no início de janeiro e resgatou $530.000 em abril. Inflação mensal foi: jan 0,51%, fev 0,96%, mar 0,45%, abr 0,28%. Calcule taxa nominal, inflação acumulada e taxa real.

**Resolução em três passos**.

Passo 1, taxa nominal no período (4 meses):
```
i = 530.000 / 500.000 - 1 = 6,00%
```
Excel BR: `=530000/500000-1` → 0,06 (6%)

Passo 2, inflação acumulada de 4 meses:
```
π = (1,0051)(1,0096)(1,0045)(1,0028) - 1 = 2,22%
```
Excel BR: `=(1+0,51%)*(1+0,96%)*(1+0,45%)*(1+0,28%)-1` → 0,0222 (2,22%)

Passo 3, taxa real no período (Fisher):
```
r = 1,06 / 1,0222 - 1 = 3,70%
```
Excel BR: `=(1+6%)/(1+2,22%)-1` → 0,0370 (3,70%)

**Comentário**. Esse é o template clássico de questão composta. A sequência sempre é: acha nominal pelos valores monetários (VF/VP - 1), acha inflação acumulada multiplicando, acha real por Fisher. Decora a sequência.

### Exemplo resolvido 3 (slides 29 e 30)
**Enunciado**. Investimento de R$10.000 virou R$11.900 em 7 meses. Inflação foi 0,6% a.m. nos 3 primeiros meses e 0,8% a.m. nos 4 últimos. Calcule a taxa real no período e ao ano.

**Resolução**.

Nominal no período:
```
i = 11.900 / 10.000 - 1 = 19%
```
Excel BR: `=11900/10000-1` → 0,19 (19%)

Inflação acumulada (7 meses):
```
π = (1,006)^3 × (1,008)^4 - 1 = 5,11%
```
Excel BR: `=POTÊNCIA(1+0,6%;3)*POTÊNCIA(1+0,8%;4)-1`
Ou: `=(1+0,6%)^3*(1+0,8%)^4-1` → 0,0511 (5,11%)

Real no período (Fisher):
```
r_periodo = 1,19 / 1,0511 - 1 = 13,22%
```
Excel BR: `=(1+19%)/(1+5,11%)-1` → 0,1322 (13,22%)

Real ao ano:
```
r_ano = (1,1322)^(12/7) - 1 = 23,71%
```
Excel BR: `=POTÊNCIA(1+13,22%;12/7)-1`
Ou: `=(1+13,22%)^(12/7)-1` → 0,2371 (23,71%)

**Detalhe importante**. Pra anualizar uma taxa real de período, você eleva a (12/n), com n em meses. Não dá pra multiplicar por (12/n). Anualização é capitalização composta, não regra de três.

### Domínio do bloco 2
Você precisa conseguir:
- Saber Fisher de cor: (1+i) = (1+π)(1+r)
- Isolar r sem hesitar: r = (1+i)/(1+π) - 1
- Saber quando r ≈ i - π funciona (π baixo) e quando quebra (π alto)
- Resolver "nominal e inflação dados, achar real" sem travar
- Anualizar taxa real de período usando potência (12/n)

---

## Bloco 3. Aplicações de Fisher

Fisher não é só uma identidade abstrata. Ela aparece em todo produto financeiro brasileiro que envolve inflação. Aqui estão os tipos cobertos na aula, ordenados por probabilidade de cair.

### Aplicação 1. VPL com inflação (slides 36 a 41)

**A regra dura**. Nominal com nominal, real com real. Nunca cruzar.

**Por que misturar dá erro**. Se você tem fluxo real (em poder de compra de hoje) e desconta por taxa nominal, está descontando pela inflação duas vezes: uma na taxa, e outra implícita no fato de o fluxo não crescer nominalmente como cresceria se fosse nominal de verdade. Resultado: VPL artificialmente baixo, decisão errada de investimento. O erro também acontece no sentido inverso (fluxo nominal com taxa real), gerando VPL artificialmente alto.

**Atenção com a função VPL do Excel**. A `VPL(taxa;v1;v2;...)` do Excel BR desconta TODOS os valores como se estivessem em t=1, t=2, t=3, etc. Pra incluir o investimento inicial em t=0, soma fora da função:
```
VPL_total = v0 + VPL(taxa; v1; v2; v3; ...)
```

**Exemplo da aula (slides 37 a 41)**. Projeto com fluxos reais -100, 35, 50, 30 nos anos 0, 1, 2, 3. Taxa nominal de desconto 15%, inflação 10%. Calcule o VPL pelas duas formas e mostre que dão o mesmo.

**Forma 1, descontar por taxa real**.

Acha r real por Fisher:
```
r = 1,15 / 1,10 - 1 = 4,54%
```
Excel BR: `=(1+15%)/(1+10%)-1` → 0,0454 (4,54%)

Desconta os fluxos reais por r. Forma expandida:
```
VPL = -100 + 35/1,0454 + 50/1,0454^2 + 30/1,0454^3 ≈ $5,5
```
Excel BR expandido:
```
=-100 + 35/(1+4,54%) + 50/(1+4,54%)^2 + 30/(1+4,54%)^3
```

Excel BR usando função VPL (lembrando da pegadinha do t=0):
```
=-100 + VPL(4,54%;35;50;30)   → ≈ 5,5
```

**Forma 2, inflar fluxos pra nominal e descontar por 15%**.

Conversão dos fluxos:
```
Ano 1: 35 × 1,10 = 38,50
Ano 2: 50 × 1,10^2 = 60,50
Ano 3: 30 × 1,10^3 = 39,90
```
Excel BR:
```
=35*(1+10%)        → 38,5
=50*(1+10%)^2      → 60,5
=30*(1+10%)^3      → 39,93
```

Desconta por 15% nominal:
```
VPL = -100 + 38,5/1,15 + 60,5/1,15^2 + 39,9/1,15^3 ≈ $5,5
```
Excel BR:
```
=-100 + 38,5/(1+15%) + 60,5/(1+15%)^2 + 39,9/(1+15%)^3
=-100 + VPL(15%;38,5;60,5;39,9)
```

As duas formas dão o mesmo VPL. Essa equivalência é a confirmação prática de Fisher. Se elas não dessem o mesmo, Fisher estaria errada.

**Conversão chave entre fluxos**:
```
CF_nominal_t = CF_real_t × (1 + π)^t
```
Excel BR: `=CF_real*(1+π)^t` ou `=CF_real*POTÊNCIA(1+π;t)`

### Aplicação 2. Investimento IPCA + x% (slides 44 e 45)

**O produto**. É o formato mais comum de renda fixa indexada no Brasil. "Tesouro IPCA+ 7%" ou "CDB IPCA+ 6%". O 7% (ou 6%) é o juro real fixo, e a inflação corrige por cima a cada período.

**Exemplo**. Investimento de 2 anos a IPCA+7%. Inflação ano 1: 4%. Inflação ano 2: 5,6%.

**Q1: qual a taxa nominal anual esperada?**

Cada ano o saldo cresce por (1 + π_ano)(1 + r), onde r = 7% é fixo:
```
(1 + i)^2 = (1,04)(1,07)(1,056)(1,07) = 1,2575
i = 12,13% a.a.
```
Excel BR:
```
=(1+4%)*(1+7%)*(1+5,6%)*(1+7%)              → 1,2575
=POTÊNCIA((1+4%)*(1+7%)*(1+5,6%)*(1+7%);1/2)-1   → 0,1213 (12,13%)
```

**Q2: qual a taxa real anual esperada?**

Aplica Fisher com π acumulado dos 2 anos:
```
(1 + r)^2 = 1,2575 / (1,04 × 1,056) = 1,1449
r = 7,00% a.a.
```
Excel BR:
```
=POTÊNCIA(1,2575/((1+4%)*(1+5,6%));1/2)-1   → 0,07 (7%)
```

**Comentário**. O 7% real cai exato porque é o que o papel promete por construção. Não é coincidência. A inflação realizada pode variar, mas o cupom real fixo continua sendo o cupom real fixo.

### Aplicação 3. Título com cupom real e inflação variável (slides 42 e 43)

**Enunciado**. $25.000 em IPCA+7,5% por 3 anos. Inflação anual: 3,2%, 4,3%, 5,6%. Qual o valor de resgate?

**Resolução**. Cada ano o saldo cresce por (1 + IPCA_ano)(1 + 7,5%):
```
VF = 25.000 × (1,075)^3 × (1,032)(1,043)(1,056) = $35.301,51
```
Excel BR:
```
=25000*(1+7,5%)^3*(1+3,2%)*(1+4,3%)*(1+5,6%)
=25000*POTÊNCIA(1+7,5%;3)*(1+3,2%)*(1+4,3%)*(1+5,6%)
                                              → 35.301,51
```

**Para comparação**. Sem inflação, VF seria 25.000 × 1,075^3 = $31.058. A diferença de R$4.243 é o que a correção monetária protegeu. Esse R$4.243 nominalmente parece "ganho", mas em poder de compra é só reposição.

### Aplicação 4. CDB pós-fixado (List #57, slides 31 e 32)

**Enunciado**. Mr. Norival aplicou $25.000 em CDB de 120 dias com remuneração = correção monetária + 12% a.a. Inflação no período = 3,5%. Qual o valor bruto resgatado? Convenção: ano = 360 dias.

**Resolução**. O juro real é 12% a.a. fixo. O prazo de 120 dias é 1/3 do ano:
```
i_real_periodo = (1,12)^(120/360) - 1 = 3,85%
```
Excel BR: `=POTÊNCIA(1+12%;120/360)-1` → 0,0385 (3,85%)

Aplica Fisher pra achar o nominal do período:
```
1 + i = 1,0385 × 1,035 = 1,07485
```
Excel BR: `=(1+3,85%)*(1+3,5%)` → 1,07485

Resgate:
```
VF = 25.000 × 1,07485 = $26.871,16
```
Excel BR: `=25000*(1+3,85%)*(1+3,5%)` → 26.871,16

**Forma direta equivalente** (substituindo Fisher na fórmula):
```
VF = VP × (1 + i_real)^(t/360) × (1 + π)
```
Excel BR: `=25000*POTÊNCIA(1+12%;120/360)*(1+3,5%)` → 26.871,16

### Aplicação 5. Empréstimo IPCA + juros real (Problem Set, slides 33 e 34)

**Enunciado**. Indivíduo toma BRL 24.000 a juros reais de 1% a.m. mais correção pelo IPCA. Prazo 2 meses. Inflação mês 1: 1,5%; mês 2: 0,9%. Calcule:
- Valor atualizado pela correção monetária
- Valor com correção + juros real
- Taxa efetiva no período e ao ano

**Resolução em quatro passos**.

Passo 1, atualização pela inflação acumulada:
```
VF_IPCA = 24.000 × 1,015 × 1,009 = 24.579,24
```
Excel BR: `=24000*(1+1,5%)*(1+0,9%)` → 24.579,24

Passo 2, aplica juros real composto sobre o saldo corrigido:
```
VF_total = 24.579,24 × (1,01)^2 = 25.073,28
```
Excel BR: `=24579,24*(1+1%)^2` → 25.073,28
Ou direto: `=24000*(1+1,5%)*(1+0,9%)*(1+1%)^2` → 25.073,28

Passo 3, taxa efetiva no período (2 meses):
```
i_efetiva = 25.073,28 / 24.000 - 1 = 4,47%
```
Excel BR: `=25073,28/24000-1` → 0,0447 (4,47%)

Passo 4, taxa efetiva ao ano:
```
i_anual = (1,0447)^(12/2) - 1 = 30,02%
```
Excel BR: `=POTÊNCIA(1+4,47%;12/2)-1` → 0,3002 (30,02%)
Ou: `=(1+4,47%)^(12/2)-1`

**Por que separa correção e juro real**. Conceitualmente, a correção apenas repõe o poder de compra que o credor perderia esperando 2 meses (mantém o poder de compra do principal constante). O juro real é o ganho dele em cima do principal já corrigido. Aritmeticamente, dá no mesmo se você multiplicasse tudo de uma vez (multiplicação é comutativa), mas o desmembramento ajuda a explicar como contratos brasileiros realmente funcionam.

### Domínio do bloco 3
Você precisa conseguir:
- Explicar por que não pode cruzar nominal com real em VPL
- Calcular VPL pelas duas formas (real-real e nominal-nominal) e ver que dão o mesmo
- Resolver IPCA+x% por mais de um ano achando nominal e real, ambos
- Calcular valor de resgate de título com cupom real fixo e inflação anual variável
- Resolver CDB pós-fixado com juro real composto + correção monetária

---

## Bloco 4. Títulos públicos brasileiros (contexto rápido)

A aula encerrou conectando Fisher aos principais títulos do Tesouro Direto. Você precisa saber qual é qual e qual é o indexador.

| Sigla técnica | Tesouro Direto | Cupom semestral | Indexador |
|---|---|---|---|
| LFT | Tesouro Selic | Não | Selic (pós-fixado puro) |
| LTN | Tesouro Prefixado | Não | Prefixado |
| NTN-F | Tesouro Prefixado c/ Juros Sem. | Sim, R$48,81 | Prefixado |
| NTN-B Principal | Tesouro IPCA+ | Não | IPCA + cupom real |
| NTN-B | Tesouro IPCA+ c/ Juros Sem. | Sim, 2,956% do VNA | IPCA + cupom real |

Os dois NTN-B são a aplicação direta de Fisher. O VNA (Valor Nominal Atualizado) é corrigido pelo IPCA todo dia útil, e o cupom (real) incide sobre esse VNA. Rentabilidade nominal final é (1 + IPCA_acumulado)(1 + cupom_real) - 1, exatamente como Fisher manda.

LFT (Tesouro Selic) é diferente. Não usa Fisher pra montar a remuneração: ela só rende a Selic acumulada do período. É puro pós-fixado nominal.

LTN e NTN-F são prefixados. A taxa nominal é fixada na compra. A inflação realizada não muda o valor de resgate, mas muda o poder de compra final do investidor, ou seja, muda o juro real ex-post (que pode até ser negativo se a inflação subir muito após a compra).

---

## Bloco 5. Erros recorrentes que derrubam aluno

Lista das pegadinhas mais comuns em prova de PF nesse tema:

**Somar inflações mensais pra achar trimestral ou anual**. Errado, sempre. Tem que multiplicar (1+π_t). Soma só vale como aproximação grosseira pra valores muito pequenos, e mesmo aí introduz erro.

**Usar r ≈ i - π com inflação alta**. Em qualquer cenário com π acima de 4 ou 5%, a aproximação introduz erro perceptível. Use sempre a forma exata.

**Descontar fluxo real por taxa nominal em VPL**. Mistura proibida. Decide qual base usar antes de começar o cálculo. Forma mais segura: identifica primeiro se o fluxo está em termos reais ou nominais (o enunciado deixa claro), e escolhe a taxa correspondente.

**Usar VPL do Excel sem cuidar do t=0**. A função VPL desconta todos os valores começando em t=1. Se você jogar `=VPL(taxa;-100;35;50;30)`, ela desconta o -100 também (como se fosse t=1), e o VPL fica errado. Forma correta: `=-100 + VPL(taxa;35;50;30)`.

**Ler "IPCA+7%" como 7% nominal**. O 7% é o juro real, contratualmente. O nominal sai por Fisher.

**Confundir IPCA com INPC**. Cestas diferentes (1-40 SM vs 1-5 SM), pesos de grupo diferentes (INPC pesa mais alimentos), pesos regionais diferentes. São índices distintos.

**Anualizar taxa real multiplicando por 12/n em vez de elevar a (12/n)**. Anualização é capitalização composta. Taxa anual é (1 + r_periodo)^(12/n) - 1, não r_periodo × (12/n).

**Calcular juros reais sobre principal não corrigido em produto IPCA+x%**. A ordem conceitual é: primeiro corrige pelo IPCA, depois aplica o cupom real sobre o saldo corrigido.

**Esquecer que regime de metas começou em fevereiro de 1999**, não com o Plano Real (julho de 1994). Entre os dois, vigorou âncora cambial.

---

## Bloco 6. Roteiro de revisão pra hoje

Sugestão de ordem, pra fazer em 1 a 2 horas:

Primeiro, leia esse guia uma vez de ponta a ponta sem fazer conta. Foco é entender as intuições, não decorar números.

Segundo, refaça os três exemplos resolvidos do bloco 2 (José com 5,25% e 8%; Securato 2.27 com $500k → $530k; investimento R$10k → R$11.900 em 7 meses) numa folha em branco, sem olhar a solução. Esses três são os mais prováveis no quiz.

Terceiro, abre o Excel e refaz tudo lá usando as fórmulas em PT-BR do guia. Confirme que os números batem com os do guia.

Quarto, refaça o exemplo de VPL com inflação pelas duas formas (real-real e nominal-nominal) no Excel. Se der diferente, achou erro de conta, refaça.

Quinto, refaça o IPCA+7% por 2 anos achando nominal e real.

Sexto, faça o auto-teste do bloco 7 abaixo. Se errar alguma, volte na seção correspondente e refaz a leitura.

---

## Bloco 7. Auto-teste

Resolva sem olhar gabarito. Tempo recomendado: 30 minutos.

**Q1**. Defina inflação em uma frase e explique por que IPCA e INPC podem dar números diferentes no mesmo mês.

**Q2**. IPCA mensal: jan 0,4%, fev 0,3%, mar 0,5%. Qual a inflação trimestral acumulada?

**Q3**. Investimento rendeu 10% nominal num ano em que a inflação foi 6%. Qual o juro real exato? E pela aproximação? Compare.

**Q4**. CDB IPCA+5% por 2 anos. Inflação 4% no ano 1 e 6% no ano 2. Qual a taxa nominal anual e a taxa real anual esperada?

**Q5**. Projeto com fluxos reais -200, 80, 80, 80 nos anos 0 a 3. Taxa nominal 12%, inflação 5%. Calcule o VPL pelas duas formas (real-real e nominal-nominal).

**Q6**. Em que ano e mês começou o regime de metas no Brasil? Quem define a meta e quem executa?

**Q7**. Por que misturar taxa nominal com fluxo real em VPL gera erro?

### Gabarito

**Q1**. Inflação é a perda de poder de compra causada pelo aumento generalizado e sustentado de preços. IPCA e INPC divergem porque têm pesos de grupo diferentes (INPC pesa mais alimentos por refletir famílias de baixa renda; IPCA pesa mais transportes e educação) e pesos regionais diferentes (IPCA pesa mais SP e RJ).

**Q2**. (1,004)(1,003)(1,005) - 1 = 1,2024%.
Excel BR: `=(1+0,4%)*(1+0,3%)*(1+0,5%)-1` → 0,012024 (1,2024%).
Note que somar daria 1,2%, próximo mas tecnicamente errado.

**Q3**. 
Real exato por Fisher: r = 1,10 / 1,06 - 1 = 3,77%.
Excel BR: `=(1+10%)/(1+6%)-1` → 0,0377 (3,77%).
Aproximação: 10 - 6 = 4%. Excel BR: `=10%-6%` → 0,04 (4%).
Diferença de 23 bps. Em prova, use sempre o exato.

**Q4**.
Nominal: (1+i)^2 = (1,04)(1,05)(1,06)(1,05) = 1,2155, então i = 10,25% a.a.
Excel BR: `=POTÊNCIA((1+4%)*(1+5%)*(1+6%)*(1+5%);1/2)-1` → 0,1025 (10,25%).

Real: (1+r)^2 = 1,2155 / (1,04 × 1,06) = 1,1025, então r = 5,00% a.a.
Excel BR: `=POTÊNCIA((1+10,25%)^2/((1+4%)*(1+6%));1/2)-1` → 0,05 (5%).
O 5% real cai exato no cupom contratual, como esperado.

**Q5**.
Real: r = 1,12 / 1,05 - 1 = 6,67%.
Excel BR: `=(1+12%)/(1+5%)-1` → 0,0667 (6,67%).

VPL real expandido:
```
=-200 + 80/(1+6,67%) + 80/(1+6,67%)^2 + 80/(1+6,67%)^3
=-200 + 75,00 + 70,31 + 65,91 = 11,22
```
VPL real com função: `=-200 + VPL(6,67%;80;80;80)` → 11,22

Conversão fluxos pra nominal:
```
=80*(1+5%)         → 84,00
=80*(1+5%)^2       → 88,20
=80*(1+5%)^3       → 92,61
```

VPL nominal expandido:
```
=-200 + 84/(1+12%) + 88,2/(1+12%)^2 + 92,61/(1+12%)^3
=-200 + 75,00 + 70,31 + 65,91 = 11,22
```
VPL nominal com função: `=-200 + VPL(12%;84;88,2;92,61)` → 11,22

Mesmo VPL nas duas formas. Fisher confirmada.

**Q6**. Fevereiro de 1999. CMN define a meta. Bacen executa via taxa Selic através do Copom.

**Q7**. Porque o fluxo real está em poder de compra constante, sem inflação embutida, e a taxa nominal já inclui prêmio inflacionário. Descontar fluxo real por taxa nominal aplica desconto pela inflação duas vezes: uma na taxa, outra implicitamente porque o fluxo não cresce nominalmente. O VPL fica artificialmente baixo, e a decisão de investimento pode virar errada por causa do erro de mistura.

---

## Bloco 8. Cola de fórmulas (último recurso, na prova)

### Núcleo conceitual

```
INFLAÇÃO
  período:        π = P_f / P_0 - 1
  acumular:       π_total = ∏(1+π_t) - 1
  anualizar:      π_a = (1+π_total)^(1/anos) - 1

FISHER
  identidade:     (1+i) = (1+π)(1+r)
  juros real:     r = (1+i)/(1+π) - 1
  aproximação:    r ≈ i - π   [só p/ π pequeno]

NPV
  taxa real × fluxo real     ✓
  taxa nominal × fluxo nominal ✓
  cruzar                      ✗
  conversão fluxo: CF_nom_t = CF_real_t × (1+π)^t

ANUALIZAR TAXA DE PERÍODO
  i_anual = (1 + i_periodo)^(12/n_meses) - 1
  [ELEVA, não multiplica]

IPCA + x%
  o x é REAL, não nominal
  nominal sai por Fisher
```

### Cola Excel BR (todas as fórmulas que você pode precisar)

```
INFLAÇÃO
  período:           =P_f/P_0-1
  acumular 3 meses:  =(1+π1)*(1+π2)*(1+π3)-1
  acumular n meses:  =PRODUTO(1+intervalo)-1
  anualizar:         =POTÊNCIA(1+π_total;1/anos)-1
  ou:                =(1+π_total)^(1/anos)-1
  mensal p/ anual:   =POTÊNCIA(1+π_mensal;12)-1

FISHER
  juros real:        =(1+i)/(1+π)-1
  juros nominal:     =(1+r)*(1+π)-1
  aproximação:       =i-π

ANUALIZAR TAXA REAL
  ano a partir mês:  =POTÊNCIA(1+r_periodo;12/n_meses)-1
  ano a partir dia:  =POTÊNCIA(1+r_periodo;360/n_dias)-1

CONVERSÃO FLUXO REAL <-> NOMINAL
  real p/ nominal:   =CF_real*(1+π)^t
  nominal p/ real:   =CF_nominal/(1+π)^t

VPL
  expandido:         =-100 + 35/(1+r)^1 + 50/(1+r)^2 + 30/(1+r)^3
  função (CUIDADO):  =CF0 + VPL(taxa;CF1;CF2;CF3;...)
                     [VPL desconta a partir de t=1, soma CF0 fora]

PRODUTO IPCA + x%
  VF 1 ano:          =VP*(1+IPCA_ano)*(1+x)
  VF n anos diff π:  =VP*(1+x)^n*(1+π1)*(1+π2)*...*(1+πn)
  VF prazo fracion.: =VP*POTÊNCIA(1+x;dias/360)*(1+π_periodo)
```

### Atalhos de teclado úteis no Excel
- `F4`: trava referência ($A$1)
- `Ctrl+Shift+%`: formata célula como porcentagem
- `Ctrl+1`: abre formatação de célula
- `Ctrl+;`: insere data de hoje

Boa sorte amanhã.
