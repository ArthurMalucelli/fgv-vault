---
materia: OperacoesParaCompetitividade
data: 2026-06-11
tema: Prova Final Unificada (toda a disciplina)
tags: [resumo, prova]
---

# Prova Final OC — hoje, 11.06, 15h

Cobre **toda a disciplina, incluindo o que já caiu na parcial** (regra do syllabus). Vale 40%. Sem IA na prova.

Sinais explícitos do professor sobre o que cai:

- Pareto passo a passo no Excel: "aparentemente será cobrado na prova final".
- Exercício de balanceamento da fábrica de aspiradores: "já foi questão de prova, atenção redobrada".
- Veracidade (5 Vs): "não tô nos slides, anotem, é importante".
- A lista de 56 questões + o resumo oficial com 12 questões (arquivo da aula 23.03) são o mapa do conteúdo: Lean, prioridades competitivas, processos, qualidade, layouts, localização.

---

## 1. Conceitos e prioridades competitivas

| Conceito | Definição de prova |
|---|---|
| Gestão de operações | Planejamento, administração e controle sistemáticos de **processos que transformam insumos (inputs) em produtos e serviços (outputs)**, para clientes internos e externos. Objetivo: gerar valor com eficiência |
| Competitividade | Capacidade de **manter vantagem comparativa**: criar vantagem frente aos concorrentes, atrair e reter clientes |
| Operação competitiva | Entrega **valor superior ao cliente** (não "preço baixo sempre") |
| [[Prioridades Competitivas]] (os 5 critérios) | **Custo, Qualidade, Velocidade, Confiabilidade, Flexibilidade.** Layout NÃO é critério competitivo (pegadinha de questão) |
| Trade-off | Melhorar um objetivo **prejudica outro**. Recursos finitos forçam priorização |
| Critérios qualificadores | **Atributos mínimos pra competir.** Degrau: abaixo do nível de qualificação você nem é considerado; acima, não ganha mais por isso |
| Critérios ganhadores de pedido | **Convencem o cliente a escolher** a empresa. Relação linear: quanto melhor o desempenho, maior a probabilidade de ganhar o pedido |
| Critérios menos relevantes | Quase não afetam a decisão do cliente (linha achatada) |

Tradução fator competitivo (cliente) → objetivo de desempenho (operação):

| Se o cliente valoriza | A operação deve se superar em |
|---|---|
| Preço | Custo |
| Qualidade | Qualidade |
| Entrega rápida | Rapidez/Velocidade |
| Entrega confiável | Confiabilidade |
| Produtos inovadores | Flexibilidade (produto/serviço) |
| Ampla variedade | Flexibilidade (mix) |
| Alterar prazo e quantidade | Flexibilidade (volume/entrega) |

### Matriz Importância × Desempenho (Matriz ID)

Framework: clientes definem a **importância** dos critérios; concorrentes são a régua do **desempenho**. Análise simultânea → prioridades de ação em operações.

Escala de 9 pontos de IMPORTÂNCIA (o que o cliente acha):

- **1 a 3 = ganhadores de pedido** (1: vantagem crucial; 2: importante, sempre considerado; 3: vantagem útil)
- **4 a 6 = qualificadores** (precisa estar na média do setor ou perto)
- **7 a 9 = menos relevantes** (7: raramente considerado; 9: nunca)

Escala de 9 pontos de DESEMPENHO (vs concorrência):

- **1 a 3 = melhor** que o melhor concorrente
- **4 a 6 = igual** à concorrência
- **7 a 9 = pior** que a concorrência

Os eixos da matriz: importância no X **crescendo da esquerda pra direita em relevância** (9...7 pouco relevantes, 6...4 qualificadores, 3...1 ganhadores à direita); desempenho no Y (1 no topo, 9 embaixo). 4 zonas:

| Zona | Posição | Leitura | Ação |
|---|---|---|---|
| **EXCESSO** | Pouco importante + desempenho alto | Recurso sobrando onde o cliente não liga | Realocar recurso |
| **ADEQUADO** | Importância e desempenho alinhados (faixa superior) | Manter | Manter |
| **APRIMORAR** | Abaixo da faixa adequada | Melhorar quando der | Melhoria programada |
| **URGÊNCIA** | Muito importante (1-3) + desempenho pior (7-9) | Cliente valoriza e você apanha da concorrência | Ação imediata |

Regra de bolso de questão: **importância 1 + desempenho 8 ou 9 = URGÊNCIA. Importância 9 + desempenho 1 = EXCESSO.**

Caso XPTO (gabarito da aula monitorada, formato provável de questão aberta): o enunciado dá as notas EMBARALHADAS em texto ("péssima = 9, excelente = 1, ótima = 2, boa = 3, regular = 5"). Primeiro passo é montar a tabela Importância | Desempenho por critério. Resultado: Qualidade (imp 1, des 9) e Confiabilidade (imp 1, des 2), Flexibilidade (imp 2, des 3), Velocidade (imp 8, des 5), Preço (imp 9, des 1). Leitura: ganhadores de pedido = **Confiabilidade, Qualidade e Flexibilidade**; Qualidade está em **URGÊNCIA**; Preço está em **EXCESSO**.

Método Gap (formulação de estratégia em 4 passos): estabelecer objetivos de desempenho, avaliar atingimento e importância, **priorizar via Matriz ID**, desdobrar planos de ação.

Matriz da Estratégia de Operações (desdobramento): objetivo de desempenho crítico (linha) × áreas de decisão estratégica (colunas: tecnologia de processo / produção, recursos humanos / pessoas, rede de suprimentos / controle) → ações concretas em cada célula. No caso XPTO, "melhoria da qualidade" desdobra em padronizar processos + CEP (produção), inspeção e indicadores PPM (controle), treinamento e cultura de qualidade (pessoas).

## 2. Processos e indicadores

| Conceito | Definição de prova |
|---|---|
| Processo | **Conjunto organizado de atividades interagentes e interdependentes** com objetivos e funções determinadas. Transforma **insumos em outputs**, deve **agregar valor**, pode ser decomposto em subprocessos ("processo aninhado") |
| Mapa de processos / fluxograma | Esboça o fluxo de informações, clientes, equipamentos ou materiais pelas etapas. Sinônimos: diagrama de fluxo, blueprint. Serve pra **visualizar etapas e gargalos** |
| Símbolos | Retângulo = processo/ação; seta = fluxo; oval = início/fim; **losango = decisão**; círculo = conector/inspeção; triângulo invertido = estoque de matéria-prima; triângulo = estoque de produto acabado; hexágono = preparação |
| Swimlanes | Faixas por responsável (consumidor / vendas / operação) no mapa |
| Análise de processos | Etapas: identificar problema/oportunidade, mapear (documentar), medir desempenho, redesenhar, implementar melhorias |
| Diagrama de processo | Classifica cada passo em **Operação, Transporte, Inspeção, Demora, Armazenamento** com tempo e distância (caso do pronto-socorro). Melhorar = atacar transporte, demora e inspeção que não agregam |
| [[Gargalo]] | **A etapa mais lenta** do processo. Restringe a produção máxima. Reduz **equalizando carga entre etapas** |
| Lead time (LT) | Tempo total do início ao fim, soma dos tempos médios |
| Eficiência de fluxo | TVA / LT (TikTok: 1,5h/6h = **25%**; o resto é fila e loop) |

Tipologia de **processos produtivos** (volume × variedade), regra: quanto maior o volume, menor a customização:

1. **Jobbing**: baixo volume, alta customização (sob encomenda).
2. **Lotes**: volume médio, alguma padronização.
3. **Linha**: alto volume, baixa variedade.
4. **Fluxo contínuo**: altíssimo volume, totalmente padronizado (commodities).

Tipologia de **processos de serviços** (contato com cliente):

- **Front office**: alto contato, alta customização (flexibilidade).
- **Hybrid office**: intermediário.
- **Back office**: **baixo contato, alta padronização** (eficiência).

Regra: mais contato = mais flexibilidade; menos contato = mais eficiência.

## 3. Localização de operações

Decisão **estratégica**, de longo prazo, cara de reverter, baseada em **potencial de lucro**. Equilibra: custos que mudam com o local, capacidade de servir o cliente, potencial de receita. Níveis hierárquicos da decisão: região global (país) → sub-região → comunidade (cidade) → local específico (endereço).

Os **3 métodos** (sabe os três e quando usar cada um):

### 3a. Ponderação qualitativa (pontuação ponderada)

Pra cada fator: peso × nota. Soma. Maior escore vence. Junta fatores tangíveis e intangíveis.

<pre>
Escore da localidade = Σ (peso do fator × nota da localidade no fator)
</pre>

Exemplos resolvidos: aula (A = 76 vs B = 67 → A); lista Energix (X = 112 vs Y = 88 → X); Krajewski com escala 0-100 (C = 605 > A 585 > B 580 → C). Questão da lista 23.03: pesos MO 3, transporte 2, energia 1, locais A(4,3,5) e B(3,5,4) → A: 12+6+5 = 23, B: 9+10+4 = 23, **empate** (alternativa "ambos iguais").

### 3b. Ponto de equilíbrio (comparação de custos fixos e variáveis)

<pre>
PEQ = CF / (PV − CVu)          [unidades pra zerar; menor PEQ = melhor]
Lucro = RT − CVt − CF = Q×PV − Q×CVu − CF
</pre>

Dois critérios de escolha possíveis, e **eles podem divergir**:

| Exercício | Pelo LUCRO | Pelo menor PEQ |
|---|---|---|
| Mercúrio (Alpha CF 320k, CVu 40 vs Delta CF 280k, CVu 42; PV 80, Q 100k) | **Alpha** (3,68M vs 3,52M) | **Delta** (7.369 vs 8.000) |
| Enerbat (SP CF 450k, CVu 55 vs RJ CF 500k, CVu 50; PV 120, Q 80k) | **RJ** (5,10M vs 4,75M) | **SP** (6.923 vs 7.143) |

Pegadinha de prova: **ler qual critério a questão pede**. Lucro favorece quem tem custo variável menor em volume alto; PEQ favorece quem tem custo fixo menor. Questão da lista 23.03: A (CF 150k, CV 20) vs B (CF 90k, CV 30), PV 50 → PEQ A = 150.000/30 = **5.000**, PEQ B = 90.000/20 = **4.500** → melhor B.

Dominância: uma comunidade é descartada se **tanto CF quanto CV são maiores** que os de outra (suplantada).

### 3c. Centro de gravidade

Minimiza distância total ponderada (proxy de **custo de transporte**). Com custos de transporte iguais em todas as direções:

<pre>
Gx = Σ (xi × Ci) / Σ Ci          Gy = Σ (yi × Ci) / Σ Ci
xi, yi = coordenadas do mercado i;  Ci = volume/demanda do mercado i
(se o custo unitário pi difere por direção, multiplica também por pi)
</pre>

Exemplos resolvidos: Ômega aço → (6,67; 3,02), perto do mercado F; energia elétrica (Krajewski) → (12,4; 9,2) com Σci·xi = 7.504 e Σci = 607; questão da lista 23.03: A(1,2)d120, B(8,6)d180, C(5,1)d300 → Gx = (120+1.440+1.500)/600 = **5,10**, Gy = (240+1.080+300)/600 = **2,70**.

## 4. Layouts (arranjo físico)

Arranjo físico = onde posicionar pessoas, máquinas e equipamentos. Objetivo: segurança, atratividade, flexibilidade e eficiência. Impacta **produtividade e lead time**.

| Layout | Lógica | Ideal para | Vantagem | Desafio |
|---|---|---|---|---|
| **Posicional (posição fixa)** | Recurso transformado **não se move**; máquinas e pessoas vão até ele | Avião, navio, obra, cirurgia, mesa de restaurante | Viabiliza o imóvel | Coordenação complexa |
| **Funcional (por processo)** | **Processos semelhantes ficam juntos**; produto/cliente flui pelo roteiro que precisa | Alta variedade, baixo volume (supermercado, hospital geral, oficina) | Flexível | **Fluxo complexo e intermitente** |
| **Celular** | Pré-seleção pra uma **célula com todos os recursos da família** de produtos | Variedade média, volume médio (MasterChef, ala de maternidade) | Reduz **movimentação** | Definir famílias |
| **Linha (por produto)** | Sequência física = **roteiro obrigatório** do produto | **Alta repetição** (linha de montagem, bandejão) | **Fluxo previsível** | Rígido; mal balanceado = **ociosidade e gargalos** |

Matriz de layouts (decora a diagonal): volume baixo→alto no X, flexibilidade alta→baixa no Y: **Posicional → Funcional → Celular → Linha**. Posicional = fluxo intermitente; Linha = fluxo contínuo. Layouts **híbridos** combinam tipos (restaurante: salão posicional + buffet celular + comida a quilo em linha + cozinha funcional). Referência de aula: The Founder (layout do McDonald's desenhado na quadra).

## 5. Balanceamento de linha

Distribuir tarefas entre estações minimizando ociosidade, sem violar TC nem precedência. Método **heurístico** (mais de uma solução com a mesma eficiência).

<pre>
TC requerido = tempo disponível para produção / quantidade a produzir
TC com perda = TC × (1 − perda%)               [perda APERTA o TC]

N teórico (mínimo de estações) = Σ tempos das tarefas / TC
                                 SEMPRE arredonda PRA CIMA (3,5 → 4; 3,89 → 4)

Ocupação de cada posto = tempo do posto / TC
Tempo ocioso do ciclo  = Σ (TC − tempo de cada posto)
Proporção ociosa       = tempo ocioso / (N real × TC)

Eficiência (EB) = N teórico / N real
                = Σ tempos / (N real × TC)
                = média das ocupações dos postos
                = 1 − proporção ociosa            [todas dão o MESMO número]

Máxima produção = 60 / tempo da tarefa mais longa (gargalo)   [unid/h]
</pre>

Passo a passo: calcula TC (ajusta perda), N teórico (arredonda pra cima), agrupa tarefas respeitando (soma ≤ TC) e precedência direta, conta N real, calcula EB.

**Os 4 exercícios resolvidos do curso** (qualquer um pode voltar na prova):

1. **Bolos (aula de layout):** 9 tarefas, Σ = 1,68 min; 5.000 bolos/semana, 40h/semana. TC = 2.400/5.000 = **0,48 min**. N = 1,68/0,48 = 3,5 → **4**. Estações {a,b} 0,42, {c} 0,36, {d,e} 0,42, {f,g,h,i} 0,48. Ocioso = 0,24 min → proporção 0,24/(4×0,48) = 12,5% → **EB = 87,5%**.
2. **Monitorada ex. 1 (8h, 25 dias, perda 15%, demanda 4.000):** tarefas A1, B2,5, C1, D1,5, E2,2*, F1,5 (Σ 9,7). TC = (8×25×60)/4.000 = 3 × 0,85 = **2,55 min**. N teórico = 9,7/2,55 = 3,8 → **4**. Balanceamento do gabarito: {A+C} 2, {B} 2,5, {D} 1,5, {E} 1,5*, {F} 2,2 → **N real = 5**. EB = 3,8/5 = **76%** (ou média das ocupações, mesma coisa).
3. **Aspiradores (JÁ FOI PROVA):** A0,2 B0,2 C0,4 D0,4 E0,3 F0,7 G0,4 H0,5 (Σ 3,1). Máxima produção com 8 operadores = gargalo F: 60/0,7 = 85,7/h → **685/dia** (8h). Com demanda 500/dia: TC = 480/500 = **0,96**. N teórico = 3,1/0,96 = 3,23 → **4**. Balanceamento gabarito: {A+B+E} 0,7, {C+D} 0,8, {F} 0,7, {G+H} 0,9 → **N real = 4**. Dobrar produção? **Segundo turno** com os mesmos 8, sem contratar.
4. **Peças 45 min/h (aula de layout):** A3,0 B3,5 C1,0 D1,7 F2,8 G2,5 E3,0 (Σ 17,5). 10 peças/h, trabalhador só trabalha **45 min/h** → TC = **45/10 = 4,5 min** (pegadinha: usa o tempo ÚTIL, não 60). N teórico = 17,5/4,5 = 3,89 → **4**. Gabarito: postos {A} 3, {B+C} 4,5, {F+D} 4,5, {G} 2,5, {E} 3 → **N real = 5**, ocupações 66,7% / 100% / 100% / 55,6% / 66,7% → **EB = 77,8%**.

Pegadinha dupla: pergunta de **máxima produção** = 60/gargalo, sem balancear nada. Pergunta de **operadores/eficiência** = cálculo completo. E N real ≥ N teórico sempre.

## 6. Qualidade e ferramentas

[[Qualidade]] = **atender e superar expectativas** do cliente. Percepção subjetiva, multidimensional. **Não é redução de custos** (custo cai como consequência, não como objetivo).

12 dimensões (desempenho, conformidade, consistência, recursos, durabilidade, confiabilidade, limpeza, conforto, estética, comunicação, competência, simpatia, atenção): cliente não valoriza todas igualmente.

| Ferramenta | Função | Detalhe de prova |
|---|---|---|
| Folha de verificação | Coleta e conta ocorrências (tracinhos) | Alimenta o Pareto (questão MudaCerto) |
| [[Ishikawa]] (espinha de peixe) | **Causas e efeitos.** Qualitativo | 6M: mão de obra, máquina, método, material, medição, meio ambiente. **Causas, não sintomas.** Efeito à direita |
| [[Pareto]] | **Prioriza** causas. Quantitativo | Barras decrescentes + linha % acumulada (termina em 100%). [[Princípio 80-20]] é regra de bolso: restaurante deu 69,7%, Netflix deu 80,0% exato |
| Histograma | **Distribuição de frequências** | Não ordena nem acumula (≠ Pareto) |
| CEP | Monitora **desvios do processo** | Fora de controle = **causas especiais**; variabilidade comum é inerente |
| [[5W2H]] | **Plano de ação** | What, Why, Who, Where, When, How, How much |
| [[PDCA]] | Ciclo de melhoria | **Começa por Planejar.** Check = real vs planejado. Act = corrige no insucesso, padroniza no sucesso |

Encadeamento canônico (caso Netflix, formato de questão aberta):

1. [[Ishikawa]] mapeia causas (qualitativo).
2. [[Pareto]] prioriza (quantitativo): Preço 210 (42%) + Conteúdo 190 (38%) = **80% exatos**.
3. [[5W2H]] vira plano por causa priorizada.
4. [[PDCA]] executa, mede churn, corrige.

Pareto no Excel (professor avisou que cai): tabela dinâmica (campo em Linhas E em Valores) → classifica Z→A → Freq% = freq/total com **F4 no denominador** → acumulada (primeira = freq%; demais = anterior + atual) → Inserir → Gráficos Recomendados → Todos os Gráficos → **Combinação** (coluna + linha).

[[Sistema de Gestao da Qualidade|SGQ]]: coordena pessoas, processos e recursos pra qualidade consistente. Inputs: contexto, requisitos do cliente, partes interessadas. Outputs: satisfação, produtos conformes. Núcleo: PDCA organizacional.

## 7. Lean / Just-in-Time

[[Pensamento Enxuto]]: "fazer mais com menos, criando valor". Origem: **Toyota, década de 1950** (Taiichi Ohno e Shigeo Shingo). Não é Ford 1920.

3 pilares: **Valor** (pelo olhar do cliente), **Fluxo** (sem interrupção), **Kaizen** (melhoria contínua).

[[Valor]] (ótica Lean) = o que o cliente **percebe como útil e está disposto a pagar**. Buscar valor = **remover tudo que não agrega** (não é produzir mais rápido). Tradicional acelera a parte de Valor (ganho pequeno); Lean corta Waste (ganho grande).

[[MUDA]] = **desperdício**. Os 8: processamento desnecessário, movimentação, estoque, superprodução, espera, defeitos, transporte, **potencial humano não aproveitado** (o oitavo, moderno).

[[Casa do Lean]]: telhado = objetivos (qualidade, custo, prazo, redução de desperdícios); pilares = **JIT** ("peça certa, tempo certo, quantidade certa": fluxo contínuo, [[Takt time]], [[Sistema puxado|sistema puxado]], mão-de-obra flexível) e **[[Jidoka]]** ("qualidade construída a partir do processo": separação homem/máquina, identificação de anormalidades, [[Poka Yoke]]); centro = envolvimento; base = [[Heijunka]], [[Trabalho Padronizado]], [[Kaizen]], sobre **Estabilidade**.

| Termo | Resposta de prova |
|---|---|
| Fluxo contínuo | **Minimizar interrupções** |
| [[Poka Yoke]] | **Prevenção de erros** |
| [[Kaizen]] | **Melhoria contínua** (incrementos pequenos, permanente, operacionalizado pelo PDCA) |
| [[Jidoka]] | Separa **máquina e operador**; identifica **anomalias** |
| [[Takt time]] | Ritmo alinhado à demanda do cliente |
| [[Sistema puxado]] | Produz só o que o cliente pede (anti-superprodução) |
| One-piece flow | Batch=1 entrega em 0:29 vs batch=10 em 0:36. Menos WIP, menos lead time |
| [[Lean 4.0]] | **Combina digitalização com eliminação de desperdícios** (IoT, dados, IA). Amplia, não substitui |
| [[Cinco Porques]] | Cadeia de "por quê?" até a **causa raiz** (TikTok: ausência de Kaizen no design do processo) |

## 8. Tecnologias emergentes

| Conceito | Definição de prova |
|---|---|
| [[Big Data]] | Conjuntos de dados extremamente grandes e complexos (estruturados, semi e não estruturados) que **superam a capacidade das ferramentas tradicionais** de captura, gestão e análise |
| [[5 Vs do Big Data]] | **Variedade, Velocidade, Volume, Veracidade, Valor.** Valor é a SÍNTESE dos outros quatro. **Veracidade é o V esquecido** (professor mandou anotar) |
| [[Big Data Analytics]] | Transformar grandes volumes em **informação pra decisão**: estatística + [[Machine Learning]] + otimização. Sequência: Big Data → Analytics → Decisions |
| [[Dados nao estruturados]] | Sem padrão tabular (comentário, post, like). Desafio: cruzar pra gerar insight |
| IA | Máquinas realizando **tarefas que exigiriam inteligência humana**. Existe desde a Segunda Guerra; LLMs são a fase atual |
| [[IA Generativa]] | Algoritmos baseados em **LLMs** que criam conteúdo novo (texto, áudio, código, imagem) |
| [[Agente de IA]] | GenAI operando de forma **autônoma** |
| [[Ripple Effect]] | Efeito cascata: data centers → água/energia → combustível → preço final do serviço |

Aplicação cobrada (exercício EBIT): classificar elogios/reclamações em categorias por frequência e recomendar ancorado nas [[Prioridades Competitivas]] (Renner: confiabilidade, velocidade e custo sangrando; GenAI na retaguarda, não no marketing).

---

## Fórmulas consolidadas

<pre>
BALANCEAMENTO
TC          = tempo disponível / quantidade        (ajusta: × (1−perda%); usa tempo ÚTIL por hora)
N teórico   = Σ tempos / TC                        → arredonda SEMPRE pra cima
EB          = N teórico / N real = Σt/(N real×TC) = média das ocupações = 1 − proporção ociosa
Ocupação    = tempo do posto / TC
Máx produção = 60 / gargalo                        [unid/h]

LOCALIZAÇÃO
Escore ponderado = Σ (peso × nota)                 → maior vence
PEQ        = CF / (PV − CVu)                       → menor vence
Lucro      = Q×(PV − CVu) − CF                     → maior vence (critério ≠ PEQ!)
Gx         = Σ(xi × Ci) / ΣCi    Gy = Σ(yi × Ci) / ΣCi

QUALIDADE / PARETO
Freq%      = freq / total        Freq% acum = atual + acumulada anterior (fecha em 100%)

LEAN
Eficiência de fluxo = TVA / Lead Time              (TikTok: 1,5/6 = 25%)
</pre>

## Pegadinhas consolidadas (ler 10 min antes)

- **N teórico arredonda pra cima sempre.** 3,2 → 4. 3,5 → 4. 3,89 → 4.
- **Perda% diminui o TC** (×0,85 se perda 15%) e por isso **aumenta** operadores.
- **Tempo útil por hora**: "trabalha 45 min/h" → TC = 45/10, não 60/10.
- **Precedência direta** no agrupamento: só junta vizinhos na rede.
- **Máxima produção = 60/gargalo**, sem balancear. Lê a pergunta primeiro.
- **Lucro e PEQ podem escolher locais diferentes** (Mercúrio: Alpha pelo lucro, Delta pelo PEQ; Enerbat: RJ pelo lucro, SP pelo PEQ). Responde pelo critério pedido.
- **Dominância em localização**: descarta a comunidade que perde nos DOIS custos (fixo E variável).
- **Centro de gravidade pondera pela demanda**, não é média simples das coordenadas.
- **Matriz ID**: enunciado pode dar a escala embaralhada (XPTO: excelente = 1, péssima = 9). Monta a tabela antes de plotar. Importância 1 + desempenho 8/9 = **URGÊNCIA**; importância 9 + desempenho 1 = **EXCESSO**.
- **Layout NÃO é critério competitivo** (os 5: custo, qualidade, velocidade, confiabilidade, flexibilidade).
- **Qualificador habilita, ganhador converte.** Qualificador é degrau, ganhador é reta crescente.
- **Volume sobe → customização desce** (jobbing → lotes → linha → fluxo contínuo).
- **Back office = baixo contato + alta padronização**; front office é o oposto.
- **Diagonal de layouts**: posicional → funcional → celular → linha (volume sobe, flexibilidade desce).
- **PDCA começa por Planejar.** Check = real vs planejado.
- **Gargalo = etapa mais lenta** (não máquina parada).
- **Ishikawa = causas (quali); Pareto = prioriza (quanti); 5W2H = plano; PDCA = executa.** Nessa ordem (Netflix).
- **80-20 é regra de bolso**: 69,7% no restaurante, 80,0% exato no Netflix. Não força.
- **Histograma ≠ Pareto**: só distribui frequências, não ordena nem acumula.
- **CEP fora de controle = causas especiais.**
- **Qualidade ≠ corte de custos**; é atender/superar expectativa.
- **Valor (Lean) é definido pelo cliente.** JIT tem 4 elementos. Jidoka não é automação pura. Kaizen é permanente. Lean 4.0 amplia o Lean.
- **Valor é a síntese dos 5 Vs; Veracidade é o V que o professor mandou anotar.**
- Alternativa com **"apenas/somente" tende a estar errada**; a composta tende a estar certa.

## Arquivos desta pasta

- Lista de Questões - OC.pdf (56 questões) + Gabarito_Lista de Questões_OC.pdf: 1b 2c 3c 4b 5b 6b 7c 8c 9c 10b 11c 12b 13a 14c 15c 16c 17b 18a 19c 20b 21c 22c 23b 24b 25b 26c 27b 28c 29b 30b 31b 32b 33b 34b 35b 36b 37a 38b 39b 40c 41c 42c 43c 44b 45c 46b 47c 48b 49b 50b 51b 52c 53a 54c 55b 56c.
- Gabarito Atividade Monitorada - OC.pdf: caso XPTO (Matriz ID), pontuação ponderada Krajewski, centro de gravidade (12,4; 9,2), figuras volume×variedade e contato×padronização.
- Gabarito_Atividade_Balanceamento_de_Linha.pdf: exercícios 1 (TC 2,55) e aspiradores resolvidos.
- Gabarito_Localização.xlsx + Lista de Exercícios - Localização de Operações(1).docx: Energix (X 112 vs Y 88), Enerbat (lucro RJ vs PEQ SP), ponderada A/B/C (C 605), centro de gravidade (5,92; 4,88).
- O arquivo da aula 23.03 (Aulas/03.23/) é um resumo oficial + 12 questões extras com gabarito.
