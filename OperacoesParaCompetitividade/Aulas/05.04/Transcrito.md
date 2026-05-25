---
materia: OperacoesParaCompetitividade
data: 2026-05-04
tema: Correção de balanceamento de linha, Pareto, 5W2H e PDCA
topicos: [Balanceamento de Linha, Tempo de Ciclo, Pareto, 5W2H, PDCA]
tags: [aula, transcrito]
---

# Aula 04.05 — Balanceamento, Pareto, 5W2H, PDCA

## Abertura e cronograma

Hoje, 4 de maio, segunda aula de fundamentos e argumentos de gestão. Vamos falar de Pareto, 5W2H, PDCA, e fazer a correção de um exercício da aula monitorada de [[Balanceamento de Linha]]. Esse exercício pretendo gastar no máximo 20 minutos.

Próxima semana tenho aula de [[Just-in-Time]] e [[Lean]]: o que é Lean, o que é Just-in-Time, qual a importância disso para a competitividade. Aula de 18 de maio: o papel das tecnologias na eficiência operacional. Essa aula está junto com a de hoje. Lá vou ensinar a fazer o gráfico de [[Pareto]] passo a passo, porque aparentemente será cobrado na prova final.

Já saiu a data da prova final: **11 de junho, 15 horas**. É unificada, então o horário não muda.

## Mudança no trabalho final (Projeto Final)

A estrutura do que vocês têm que pesquisar não muda. O que muda é o formato da entrega da apresentação.

Ao invés de apresentarem ao vivo, vocês vão gravar uma apresentação via Zoom, Teams ou qualquer ferramenta. É obrigatório todos os integrantes aparecerem no vídeo, mas não é obrigatório todos falarem. Sugiro que cada integrante fale pelo menos uma coisa, no mínimo se apresentar: "eu sou o João do grupo XPTO". Quanto mais participarem, melhor.

A apresentação deve ser preparada em slides (PowerPoint, Canva, Prezi, qualquer ferramenta).

Reduzi de 10 para **7 minutos** de duração. Por quê? No último dia de aula, vou abrir cada vídeo, deixar rodar os 7 minutos e fazer uma ou duas perguntas para os integrantes. Se nenhum integrante do grupo estiver presente, é WOP, ou seja, fica sem nota.

Entregáveis: PDF dos slides e link do vídeo. Hospedem o vídeo no modo privado em OneDrive ou Google Drive e mandem o link. Testem o link antes de enviar.

Prazo de entrega: até **1 de junho, 14h59**. Todos entregam na mesma data, para não gerar senso de injustiça.

Na penúltima aula é a chance de validar com o professor se o trabalho está no caminho certo, antes de finalizar. Na última aula faço o follow-up: todos os grupos vêm tirar dúvidas e mostrar a evolução do trabalho.

## Exercício 1 — Balanceamento de linha (8 horas, demanda 4000)

### Enunciado
A empresa opera 8 horas por dia, tem 25 dias disponíveis, considera uma perda de 15% e tem demanda de 4000 unidades.

Atividades e durações (em minutos):
- A: 1
- B: 2,5 (precedente A)
- C: 1 (precedente A)
- D: 1,5 (precedente B)
- E: 2,2 (precedente D)
- F: 1,5 (precedente E)

Soma dos tempos = 9,7 minutos.

### Letra A — Tempo de ciclo

Vou calcular o [[Tempo de Ciclo]]. O texto fala que a empresa trabalha 8 horas por dia, tem 25 dias disponíveis e demanda de 4000 unidades. Considere uma perda de 15%.

```
TC bruto = (8 × 60 × 25) / 4000 = 3 minutos
```

Mas ainda não está correto. O que tenho que considerar? A perda de 15%. Então multiplico pelo tempo líquido, que é 0,85:

```
TC = 3 × 0,85 = 2,55 minutos
```

### Letra B — Número teórico de operadores

```
N teórico = soma dos tempos / TC = 9,7 / 2,55 ≈ 3,8 → 4
```

Qualquer fração decimal é arredondada para o próximo inteiro. Aqui não é arredondamento financeiro.

### Letra C — Balanceamento (N real)

Tenho estação de trabalho que demora 1 minuto, outra que demora 2,5, outra 1,5. Está desbalanceado. O [[Balanceamento de Linha]] é um processo de organização, não é um método exato, é heurístico. Tento juntar atividades sem violar o tempo de ciclo, e respeitando a sequência lógica (precedência).

Não faz sentido juntar A com F porque preciso que as outras estejam prontas.

A regra é uma enumeração: para cada par possível, pergunto "tarefa1 + tarefa2 ≤ TC?". Se sim, junta; se não, fica sozinha.

- A + B = 1 + 2,5 = 3,5 → viola TC (2,55). Não junta.
- A + C = 1 + 1 = 2 ≤ 2,55. **Junta.**
- B + D = 2,5 + 1,5 = 4 → viola. B fica sozinha.
- D sozinha (1,5).
- E sozinha (2,2).
- F sozinha (1,5).

Estações resultantes: {A+C}, {B}, {D}, {E}, {F} → **N real = 5 operadores**.

### Letra D — Eficiência do balanceamento

A [[Eficiência do Balanceamento]] (PB) tem duas formas de cálculo. A forma rápida:

```
PB = N teórico / N real = 3,8 / 5 = 0,76 = 76%
```

Significa o quão eficiente essa linha está em termos de distribuição de trabalho, em termos de ocupação. Quanto mais próximo de 1, mais uniformes são as cargas, menos variação, menos dispersão.

## Exercício 2 — Fábrica de aspiradores

Esse exercício já foi questão de prova. **Atenção redobrada.**

### Enunciado e rede

Atividades, tempos (em minutos) e precedência:
- A: 0,2 (sem predecessor)
- B: 0,2 (predecessor A)
- C: 0,4 (sem predecessor)
- D: 0,4 (predecessor C)
- E: 0,3 (predecessor B)
- F: 0,7 (predecessor B)
- G: 0,4 (predecessor F)
- H: 0,5 (predecessor G)

Soma dos tempos = 3,1 minutos.

A pergunta é: **utilizando os 8 operadores da linha atual, qual seria a máxima produção diária teórica?**

### Caminho curto — máxima produção via gargalo

Aqui tem caminho longo e caminho curto. Tudo depende do que é perguntado. Como a pergunta é sobre máxima produção, eu pego a tarefa mais longa, que é o [[Gargalo]] da linha. Ela é quem restringe a máxima produção. Em logística vocês vão ver isso com o nome de gargalo, no terceiro semestre.

A tarefa mais longa é F (0,7 minutos).

```
Produção/hora = 60 / 0,7 ≈ 85,7 unidades
```

### Letra B — Tempo de ciclo (com demanda explícita)

Quando a demanda é dada (500 unidades, 8h/dia):

```
TC = (8 × 60) / 500 = 0,96 minutos
```

### Letra C — Número teórico de operadores

```
N teórico = 3,1 / 0,96 ≈ 3,2 → 4
```

### Letra D — Balanceamento

Verificando combinações respeitando precedência:

- A + B + E = 0,2 + 0,2 + 0,3 = 0,7 ≤ 0,96 → junta.
- C + D = 0,4 + 0,4 = 0,8 ≤ 0,96 → junta.
- F sozinho (0,7), porque F + G = 1,1 > 0,96 viola.
- G + H = 0,4 + 0,5 = 0,9 ≤ 0,96 → junta.

Estações: {A+B+E}, {C+D}, {F}, {G+H} → **N real = 4 operadores**.

Não existe somente uma solução combinada. Em outros exercícios você pode chegar no mesmo resultado combinando tarefas de forma diferente, é um problema combinatório.

## Pareto (Diagrama)

Já ouviram falar de Pareto? Bastante visto em Finanças e Contabilidade. Pareto foi um italiano que introduziu um conceito que as organizações usam hoje para focar e identificar problemas ou valores importantes, e priorizar clientes.

É um recurso gráfico usado tanto no contexto de **perdas** quanto de **ganhos**.

### Exemplo conceitual

Suponha uma empresa com R$ 1 milhão em perdas de produção numa semana, distribuído entre 10 produtos.

| Produto | Perda |
|---|---|
| 6 | R$ 600.000 |
| 9 | R$ 200.000 |
| 1, 2, 3, 4, 5, 7, 8, 10 | R$ 200.000 (somados) |

Produto 6 + Produto 9 = **R$ 800 mil = 80% das perdas**.
Produto 6 + Produto 9 = **2 produtos = 20% dos 10 produtos**.

Esse é o [[Princípio 80-20]], também conhecido como regra de Pareto.

### Para que serve

Mostrar quantitativamente quais produtos ou causas relevantes contribuem para as perdas (ou para o lucro, ou para a receita, dependendo do contexto). Se você identificar esse pequeno contingente de 20%, resolve 80% dos problemas.

Pode ser combinado com [[Ishikawa]]: enquanto Ishikawa olha qualitativamente as causas, Pareto olha quantitativamente. Você mapeia 10 causas no Ishikawa, identifica via Pareto que 2 estão gerando 80% das perdas, e age sobre essas duas.

### Como construir (passo a passo no Excel)

Base: 89 reclamações de um restaurante, em 5 categorias. Se quero contar a frequência de cada categoria, a forma mais rápida é tabela dinâmica.

**Passo 1.** Inserir tabela dinâmica (Inserir → Tabela Dinâmica → Nova Planilha).

**Passo 2.** Arrastar o campo "reclamação" para Linhas. Ele já agrupa as categorias.

**Passo 3.** Arrastar o mesmo campo "reclamação" para Valores. Ele soma a contagem em cada categoria.

Resultado:

| Reclamação | Frequência |
|---|---|
| Serviço lento | 42 |
| Mesas apertadas | 20 |
| Garçom | 12 |
| Ambiente amassado | 10 |
| Comida fria | 5 |
| **Total** | **89** |

**Passo 4.** Copiar para outra área e classificar do maior para o menor (Classificar e Filtrar → Z para A).

**Passo 5.** Calcular frequência percentual:

```
Freq% = freq / total × 100
```

O denominador (89) é referência absoluta. Selecionar a célula e apertar **F4** para travar.

**Passo 6.** Calcular frequência percentual acumulada:
- Primeira linha: igual à frequência percentual.
- Demais linhas: linha anterior acumulada + linha atual.

| Reclamação | Freq | Freq % | Freq % acum |
|---|---|---|---|
| Serviço lento | 42 | 47,2% | 47,2% |
| Mesas apertadas | 20 | 22,5% | 69,7% |
| Garçom | 12 | 13,5% | 83,1% |
| Ambiente | 10 | 11,2% | 94,4% |
| Comida fria | 5 | 5,6% | 100% |

**Passo 7.** Gráfico combinado:
- Selecionar reclamação + frequência. Segurar Ctrl e selecionar frequência acumulada também.
- Inserir → Gráficos Recomendados → Todos os Gráficos → última opção (Combinação).
- Aceitar o default (coluna para frequência, linha para acumulada).
- Clicar com o botão direito nas colunas → Adicionar Rótulos de Dados.

A linha sempre termina em 100%. Cada ponto da linha indica quanto as categorias até ali representam acumuladamente.

**Detalhe importante.** Dependendo da base, nem sempre o resultado é exatamente 80-20. Aqui o ponto mais próximo deu 69,7% (serviço lento + mesas apertadas) ou 83,1% (incluindo garçom).

## 5W2H

Depois que [[Ishikawa]] e Pareto identificaram as causas potenciais, é preciso fazer algo. Esse "fazer algo" é desenvolver um plano de ação, e o [[5W2H]] é a ferramenta para isso.

### Os 5 W

1. **What (o quê)** — descrição da ação a ser implementada.
2. **Why (por quê)** — razão da implementação. Qual o benefício?
3. **Who (quem)** — responsável pela ação.
4. **Where (onde)** — local da execução.
5. **When (quando)** — cronograma, prazo de execução.

### Os 2 H

6. **How (como)** — procedimento, atividades envolvidas.
7. **How much (quanto)** — custo de viabilização.

Algumas empresas omitem o How much, mas o ideal é colocar.

### Exemplo aplicado

A empresa identificou que o ambiente do restaurante é um dos maiores motivos de reclamação.

| Campo | Conteúdo |
|---|---|
| What | Melhorar ambiente para circulação dos clientes, menos enfumaçado |
| Why | Aumentar a receita do restaurante em 10% |
| Who | Gerente operacional + responsável de obras |
| Where | Unidade do Itaim Bibi |
| When | 2ª semana de maio de 2026 |
| How | Contratação de consultoria para treinamento, marcenaria X para ajuste físico |
| How much | Custo total estimado da intervenção |

Espero ver algo assim estruturado no diagnóstico do trabalho final: o que fazer, como fazer, quando fazer.

## PDCA

Direcionado à qualidade, é o ciclo do [[PDCA]]:

- **P (Plan)** — localizar problemas, estabelecer metas e planos de ação.
- **D (Do)** — conduzir a execução do plano.
- **C (Check)** — verificar atingimento da meta, comparar planejado com real.
- **A (Act)** — tomar ação corretiva no insucesso.

### A lógica do Check

Comparar planejado vs real:
- Se planejado = real, segue.
- Se planejado ≠ real (negativo), corrige.

Exemplo: planejou tirar 10 e tirou 1. Ação corretiva é cortar distrações (deixar de ir no jogo, deixar de ir no show). Daí o ciclo recomeça.

A comparação é sempre real vs planejado, toma ação, e o ciclo continua.

## Exercício individual (E-Class, letra 15)

Combina Ishikawa, Pareto e PDCA. Entrega: **domingo, 23h59**.

- Letra A: diagrama de Ishikawa.
- Letra B e C: aplicação dos demais conceitos (Pareto e PDCA, conforme o enunciado no E-Class).

## Próxima aula (11.05)

Just-in-Time e Lean. O que é Lean, o que é Just-in-Time, e qual a importância para a competitividade. Lean começa logo no início da próxima aula.
