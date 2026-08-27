# Roteiro de estudo — PP1 de Contabilidade Financeira

**Prova:** sexta-feira, 28/08/2026, às 14h  
**Formato confirmado pela professora:** questões fechadas no Eclass + uma questão maior com planilha Excel; planilha formatada só com a estrutura geral, sem números, fórmulas ou garantia de nomes de contas específicos.  
**Escopo:** capítulos 1–3 e listas 1–5. Não incluir T6, débito/crédito, livro diário ou livro razão.

## Princípio do roteiro

A ordem é: estrutura → transações → caixa x competência → lógica → planilha completa → simulado. Não gastar a maior parte do tempo relendo slides; resolver e corrigir exercícios.

## Quarta à noite (26/08) — aquecimento e Excel

### Bloco 1 — 25 min: estrutura e contas
- Explicar, sem consulta: BP, DRE e DFC.
- Classificar: caixa, clientes, estoque, imobilizado, fornecedores, empréstimo, adiantamento de clientes, capital, lucros acumulados, receita, CMV e despesas.
- Rever apenas os erros.

### Bloco 2 — 55 min: HypeDrop na planilha em branco
Arquivos-base:
- `T3 Ativ_ImpDFs_HypeDrop.pdf`
- `T3 Ativ_ImpDFs Plan.xlsx`

Fazer sem abrir o arquivo respondido. Na planilha:
1. Inserir as contas necessárias.
2. Criar fórmulas de totais.
3. Criar a linha de conferência `Ativo − Passivo − PL`.
4. Montar BP, DRE e DFC.
5. Conferir caixa final da DFC contra caixa do BP.

Depois comparar com `T3 Ativ_ImpDFs HypeDrop RESP.xlsx` e anotar erros em três categorias: classificação, competência/caixa ou fórmula/sinal.

### Bloco 3 — 20 min: revisão ativa
Responder sem olhar:
- Compra de estoque é despesa quando?
- Venda a prazo afeta quais demonstrações?
- Adiantamento de cliente é receita quando?
- Depreciação afeta lucro e caixa como?
- Dividendo passa pela DRE?

Encerrar sem começar matéria nova tarde demais.

## Quinta (27/08) — domínio dos conceitos e simulado

Há Poupatempo às 9h30 e outro trabalho com prazo às 23h59; portanto, encaixar os blocos na tarde/noite e preservar tempo para concluir esse trabalho.

### Bloco 1 — 75 min: caixa x competência
Usar:
- `ZezinhoDFs.xlsx`
- `Atividade Marcus Dent 2024-2.pdf`
- `MarcusDentDFs.xlsx`

Ordem:
1. Zezinho: venda/compra à vista e depois a prazo; lucro x caixa; dividendos.
2. Marcus Dent: contas a receber, adiantamento de clientes, aluguel antecipado, materiais consumidos, salários a pagar, depreciação e juros.
3. Para cada evento, dizer separadamente: efeito no BP, DRE e caixa.

### Bloco 2 — 45 min: lógica contábil
Treinar equações de saldo:
- Estoque inicial + compras − CMV = estoque final.
- Clientes inicial + vendas a prazo − recebimentos = clientes final.
- Fornecedores inicial + compras a prazo − pagamentos = fornecedores final.
- Imobilizado inicial + compras − baixas = imobilizado final.
- Lucros acumulados inicial + lucro − dividendos = lucros acumulados final.

Fazer pelo menos oito questões numéricas variadas, sem ver solução antes.

### Bloco 3 — 1h50: Atividade pré-PP1 oficial
Fazer no Eclass em condição de prova:
- sem consulta;
- apenas Excel e calculadora;
- sem pausar para estudar;
- registrar dúvida e seguir;
- usar exatamente a convenção de sinal exigida no questionário.

### Bloco 4 — 45 min: correção cirúrgica
Não rever tudo. Para cada erro:
1. Identificar o conceito testado.
2. Refazer sem olhar o gabarito.
3. Escrever uma regra de uma linha.
4. Resolver uma variação gerada pelo Claude.

### Bloco 5 — 60 a 75 min: segunda planilha
Escolher Marcus Dent ou Loja Sedução. Priorizar Marcus Dent se ainda houver confusão em competência; usar Loja Sedução apenas se a base estiver sólida, pois é mais extensa.

## Sexta de manhã (28/08) — consolidar, não aprender do zero

### Bloco 1 — 75 a 90 min: simulado misto do Claude
- Questões numéricas, associação, V/F e múltipla escolha.
- Uma miniquestão de planilha.
- Sem T6/débito e crédito.

### Bloco 2 — 35 min: corrigir apenas erros
Repetir uma questão equivalente para cada erro.

### Bloco 3 — 20 min: checklist final
Memorizar:
- Ativo = Passivo + PL.
- Estoque vira CMV quando consumido/vendido.
- Receita é reconhecida quando ganha, não necessariamente recebida.
- Adiantamento de cliente começa como passivo.
- Despesa pode existir antes do pagamento.
- Depreciação reduz lucro sem saída de caixa naquele momento.
- Dividendos reduzem caixa e PL; não são despesa.
- Caixa final da DFC deve bater com o caixa do BP.
- Inserir linhas/colunas necessárias e fórmulas antes de preencher toda a planilha.

Parar a revisão com antecedência suficiente para comer, deslocar-se e chegar às 13h45.

---

# Prompts para usar no Claude

## Prompt 0 — preparar o Claude com os materiais oficiais

Envie o ZIP de referências junto com este prompt:

```text
Você será meu tutor de Contabilidade Financeira para a PP1 da FGV. Antes de criar exercícios, leia todos os arquivos anexados e faça um mapa curto dos tipos de exercício presentes. Use os materiais como referência de conteúdo, estrutura, vocabulário e dificuldade, mas não copie números nem enunciados literalmente.

Escopo permitido: capítulos 1–3 e listas 1–5; estrutura de BP, DRE e DFC; classificação de contas; efeito de transações; caixa x competência; contas a receber/pagar; estoque e CMV; adiantamento de clientes; despesas antecipadas; depreciação; juros; dividendos; equações de saldos; interpretação de DFs.

Fora do escopo: T6, débito/crédito, partidas dobradas, livro diário e livro razão.

Formato confirmado da prova: questões fechadas no Eclass (resposta numérica, associação, verdadeiro/falso e múltipla escolha) e uma questão maior de planilha. A planilha da prova vem formatada apenas com a estrutura geral, sem números e sem fórmulas; não presuma que nomes específicos como Caixa, Estoques ou Dividendos virão prontos. O aluno deve criar/encaixar as contas necessárias.

Regras durante os treinos:
1. Faça uma questão por vez e espere minha resposta.
2. Não revele a solução antecipadamente.
3. Depois da minha resposta, diga objetivamente se está certa, identifique o erro causal e dê uma regra curta para não repeti-lo.
4. Se eu errar, dê outra questão equivalente com números diferentes.
5. Use alternativas igualmente plausíveis; não deixe a correta óbvia pelo tamanho ou linguagem.
6. Em exercícios numéricos, garanta internamente que os dados são consistentes e que o BP fecha.
7. Diferencie claramente lucro, caixa e saldo patrimonial.
8. Não invente regras da professora que não estejam nos anexos.

Primeiro, mostre somente o mapa dos arquivos e confirme que entendeu o escopo. Não gere exercícios ainda.
```

## Prompt 1 — treino de classificação e estrutura

```text
Com base nos materiais anexados da PP1, conduza um treino de 20 questões fechadas, uma por vez, sobre estrutura e classificação de BP, DRE e DFC.

Misture:
- associação de contas a Ativo Circulante, Ativo Não Circulante, Passivo Circulante, Passivo Não Circulante, PL, Receita, Custo ou Despesa;
- identificação da demonstração correta;
- custo x despesa;
- saldo (“foto”) x fluxo do período;
- interpretação de estruturas para identificar o tipo de empresa;
- verdadeiro/falso e múltipla escolha com alternativas plausíveis.

Não inclua débito/crédito nem peça definição discursiva. Espere minha resposta a cada questão. Corrija de forma direta e mantenha um placar por tema. Ao final, apresente somente meus três pontos fracos e três questões extras focadas neles.
```

## Prompt 2 — treino de caixa x competência inspirado em Zezinho e Marcus Dent

```text
Use os casos Zezinho e Marcus Dent anexados como modelo de raciocínio, mas crie um caso empresarial novo e números diferentes. Faça 14 questões fechadas, uma por vez, cobrindo:
- venda à vista e a prazo;
- contas a receber;
- compra de estoque e reconhecimento do CMV;
- contas a pagar;
- salário incorrido e ainda não pago;
- aluguel pago antecipadamente;
- adiantamento recebido de cliente;
- depreciação;
- juros incorridos e não pagos;
- dividendos;
- diferença entre lucro e caixa operacional.

Para cada evento, posso ter de informar o efeito no BP, DRE e caixa ou calcular um valor. Não revele respostas antes da minha tentativa. Quando eu responder, corrija separando sempre:
1. o que foi ganho/consumido (competência);
2. o que foi recebido/pago (caixa);
3. o saldo que permanece no BP.

Os números devem ser inteiros e consistentes. Inclua pelo menos duas situações em que o lucro é positivo e o caixa operacional é negativo, ou vice-versa. Não inclua T6/débito e crédito.
```

## Prompt 3 — treino de lógica numérica

```text
Crie um treino de 12 questões numéricas fechadas no estilo “lógica das contas” dos materiais da PP1. Faça uma questão por vez, sem revelar o gabarito antes da minha resposta.

Use estas relações, variando qual termo é a incógnita:
- Estoque inicial + compras − CMV = estoque final.
- Clientes inicial + vendas a prazo − recebimentos = clientes final.
- Fornecedores inicial + compras a prazo − pagamentos = fornecedores final.
- Imobilizado inicial + compras − baixas = imobilizado final.
- Empréstimos inicial + captações − pagamentos do principal = empréstimos final.
- Lucros acumulados inicial + lucro líquido − dividendos = lucros acumulados final.

Misture enunciados diretos e casos em que os dados aparecem em BP, DRE ou DFC. Os números precisam fechar exatamente. Depois de cada resposta, mostre a equação preenchida, a conta e uma regra de uma linha. Se eu errar, dê imediatamente uma variação equivalente antes de avançar.
```

## Prompt 4 — gerar uma planilha de treino semelhante à HypeDrop

```text
Leia `T3 Ativ_ImpDFs_HypeDrop.pdf`, `T3 Ativ_ImpDFs Plan.xlsx` e `T3 Ativ_ImpDFs HypeDrop RESP.xlsx`. Crie um exercício NOVO, de dificuldade semelhante ou ligeiramente maior, com uma empresa e entre 8 e 10 transações coerentes. Inclua aporte de capital, compra de ativo, compra de estoque à vista ou a prazo, venda com CMV, despesa incorrida, empréstimo ou pagamento de fornecedor e dividendos. Pode incluir uma venda a prazo, mas mantenha o caso resolvível dentro do conteúdo da PP1.

Gere um arquivo `.xlsx` de treino que imite a condição da prova:
- uma única aba de trabalho;
- estrutura geral de Balanço Patrimonial, DRE e DFC;
- somente títulos gerais como Ativo Circulante, Ativo Não Circulante, Passivo Circulante, Passivo Não Circulante, Patrimônio Líquido, DRE, Operações, Investimentos e Financiamentos;
- NÃO preencher nomes específicos de contas como Caixa, Estoques, Clientes, Fornecedores, Capital, Lucros Acumulados ou Dividendos;
- NÃO inserir números, fórmulas, totais calculados ou gabarito na área de resposta;
- deixar linhas e colunas extras para eu criar contas e fórmulas;
- colocar o enunciado em uma aba separada ou em um PDF/arquivo de texto separado.

Antes de me entregar, resolva internamente e verifique:
1. Ativo = Passivo + PL em todas as etapas;
2. o lucro da DRE alimenta corretamente o PL;
3. o caixa final da DFC é igual ao caixa final do BP;
4. dividendos não passam pela DRE;
5. todas as incógnitas têm solução única.

Não entregue o gabarito agora. Entregue apenas o enunciado e a planilha vazia. Guarde a solução na conversa e espere eu enviar meu arquivo preenchido para correção.
```

## Prompt 5 — planilha avançada de caixa x competência

```text
Use `Atividade Marcus Dent 2024-2.pdf`, `MarcusDentDFs.xlsx`, `ZezinhoDFs.xlsx` e `T4_Loja Sedução_Planilha.xlsx` como referências. Crie um caso novo de dois meses, com dificuldade de PP1, envolvendo:
- serviços ou vendas à vista e a prazo;
- estoque e CMV;
- aluguel ou seguro antecipado;
- adiantamento de cliente;
- salário incorrido e pago no mês seguinte;
- imobilizado e depreciação;
- empréstimo e juros incorridos;
- dividendos.

Gere somente o enunciado e uma planilha `.xlsx` vazia, com a estrutura geral de BP, DRE e DFC, mas sem nomes específicos de contas, valores ou fórmulas. Deixe colunas para saldo inicial, transações e saldo final. Eu preciso decidir quais contas criar e onde encaixá-las.

Verifique internamente que o caso fecha e que o caixa da DFC bate com o BP. Não mostre gabarito. Quando eu devolver o arquivo preenchido, corrija célula por célula e classifique cada erro como: conta/classificação, competência, caixa, sinal, fórmula ou consequência de erro anterior.
```

## Prompt 6 — simulado final de 1h50

```text
Monte um simulado novo de PP1 com duração planejada de 1h50, baseado nos materiais anexados e na Atividade pré-PP1, sem copiar as perguntas.

O simulado deve combinar:
- respostas numéricas;
- associação;
- verdadeiro/falso;
- múltipla escolha com alternativas igualmente plausíveis;
- lógica de saldos;
- caixa x competência;
- uma questão maior de planilha com BP, DRE e DFC.

Todo o simulado deve ser fechado: nada de redação longa. Não inclua T6, débito/crédito, livro diário ou razão. Gere um PDF/arquivo de enunciado e um `.xlsx` vazio. Na planilha, forneça apenas a estrutura geral, sem nomes específicos de contas, números ou fórmulas.

Não mostre nenhuma resposta antes de eu terminar. Ao receber minhas respostas e a planilha preenchida:
1. dê a nota por seção;
2. indique o erro causal, sem descontar várias vezes por consequências do mesmo erro;
3. apresente um ranking dos temas fracos;
4. gere uma questão curta de reteste para cada tema em que errei.
```

## Prompt 7 — corrigir uma planilha preenchida

```text
Vou anexar minha planilha preenchida e os modelos oficiais. Não altere meu arquivo antes de analisá-lo. Faça uma auditoria célula por célula e verifique:
- classificação das contas;
- sinais;
- regime de competência;
- entradas e saídas de caixa;
- fórmulas e referências;
- Ativo = Passivo + PL;
- lucro líquido transferido ao PL;
- caixa final da DFC igual ao caixa do BP;
- dividendos fora da DRE.

Primeiro, identifique o PRIMEIRO erro causal em ordem cronológica. Explique em no máximo quatro linhas e peça que eu mesmo o corrija. Só depois que eu enviar a correção, avance para o próximo erro. Não me entregue a planilha pronta nem revele todos os erros de uma vez. Ao final, gere uma lista curta das regras que eu mais violei e uma questão de reteste para cada uma.
```

## Prompt 8 — revisão oral rápida antes da prova

```text
Faça uma revisão oral/rápida de PP1 com 15 perguntas, uma por vez. Eu responderei em uma frase ou com um número. Priorize armadilhas: lucro x caixa, compra x despesa, estoque x CMV, venda a prazo, adiantamento de cliente, despesa antecipada, salário a pagar, depreciação, juros, dividendos, classificação de contas e fechamento BP/DFC. Não inclua débito/crédito. Corrija diretamente e não dê pistas antes da resposta. No final, mostre apenas cinco regras que eu preciso lembrar na prova.
```
