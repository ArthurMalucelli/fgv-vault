# Design: Aula de testes de hipótese em Excel e R (Estatística II)

Data: 2026-08-17. Matéria: Estatistica2 (FGV EAESP, prof. Fernando Chertman, 2026.2). Alvo: Provinha 1 em 25/08 (aulas 2 a 6).

## 1. Objetivo

Material de estudo pra Arthur aprender a executar a receita completa de teste de hipótese (H0/H1, alfa, estatística, crítico e valor-p, decisão e interpretação) em duas ferramentas: Excel (fórmulas célula a célula, mais os atalhos `T.TEST`, `Z.TEST`, `CHISQ.TEST`) e R no terminal (base R, cálculo na mão com `qt/pt/qnorm/pnorm/qchisq/pchisq` e depois `t.test`, `prop.test`, `chisq.test`).

Critério de sucesso: dado um enunciado no estilo do professor, Arthur monta o teste nas duas ferramentas sem consultar nada além da aba `Mapa`, e escreve a frase de interpretação empresarial.

## 2. Escopo (decidido)

Entra:

- Z pra uma média com sigma conhecido
- t pra uma média (sumário e dados brutos)
- t pareado
- t pra duas médias independentes (Welch), marcado como extensão além dos slides do professor
- Z pra uma proporção
- Qui-quadrado de aderência e de independência (prévia das aulas 5 e 6, que caem na provinha)
- Exercícios pra fazer sozinho com gabarito

Não entra: poder do teste e beta numérico, teste pra duas proporções, ANOVA, teste de variância, testes não paramétricos, tidyverse, RStudio, R Markdown.

Dados: simulados uma vez com seed fixa (numpy, seed 2026), arredondados a 1 casa, hardcoded nos três artefatos. O gerador não é entregável. Onde o professor deu números (vendas 500/520/30/36, satisfação 7,0/6,8/0,5/20, golfe 100/400, pagamentos 100/60/40, canal x compra 3x2, sabores 18/22/20/20, atendimento 12 obs), usam-se os números dele.

Ambiente: R instalado via `brew install r` (único efeito fora do vault). Excel já instalado. LibreOffice disponível pra recálculo headless.

## 3. Arquivos

Pasta: `~/FGV/Estatistica2/Aulas/08.17/`

| Arquivo | Papel |
|---|---|
| `AulaTestesHipoteseExcelR.md` | Espinha da aula, vive no vault. YAML: `materia: Estatistica2`, `data: 2026-08-17`, `tema: Testes de hipótese em Excel e R (revisão aulas 2 a 6)`, `tags: [aula, estudo]`. Wikilinks nos conceitos centrais. Todo número vem do output real do R. |
| `TestesHipotese.xlsx` | Aba `Mapa` + uma aba por teste (`1_Z_Media`, `2_T_Media` com dois blocos, 2a sumário e 2b dados brutos, `3_Pareado`, `4_Welch`, `5_Proporcao`, `6_Qui_Aderencia`, `7_Qui_Independencia`) + aba `Exercicios` com os dados de E1 a E4 (sem solução). Fórmulas vivas. |
| `TestesHipotese.R` | Script base R, comentado em português, seções 0 a 7 espelhando o md, mais seção 8 com os dados dos exercícios (sem solução) e seção 9 gabarito comentada (`# GABARITO`, só descomentar depois de tentar). Roda inteiro com `Rscript`; feito pra colar bloco a bloco no console `R`. |
| `.superpowers/2026-08-17-aula-testes-hipotese-design.md` | Este documento. |
| `.superpowers/2026-08-17-aula-testes-hipotese-plan.md` | Plano de implementação (writing-plans). |

Notas de conceito novas em `~/FGV/Vault/Conceitos/` (só as que não existem, template `Vault/Templates/Conceito.md`, sem inventar conteúdo): `Teste bicaudal`, `Nivel de significancia`, `Teste pareado`, `Teste t para duas amostras`, `Teste qui-quadrado de aderencia`, `Teste qui-quadrado de independencia`, `Frequencia esperada`, `Distribuicao qui-quadrado`. Existentes que serão linkadas sem tocar: Teste de hipotese, Estatistica de teste, Valor-p, Valor critico, Regiao de rejeicao, Erro Tipo I, Erro Tipo II, Graus de liberdade, Distribuicao T de Student, Distribuicao normal, Z de alfa sobre 2, Teste unicaudal, Proporcao amostral, Erro padrao, Tamanho da amostra, Media amostral, Intervalo de Confiança, Nivel de Confianca, Teorema do limite central, Distribuicao binomial, Independencia.

## 4. Estrutura do md

0. Como usar (3 linhas: ler o bloco, fazer no Excel, fazer no R, exercício)
1. Setup: instalar R, abrir e sair (`R`, `q()`), 10 comandos de sobrevivência (`c`, `mean`, `sd`, `length`, `sqrt`, `?`, `t.test`, `prop.test`, `chisq.test`, `source`), Excel EN e PT (nomes lado a lado, Análise de Dados como opcional)
2. A receita (5 passos do professor) e a tabela de escolha: situação do enunciado, teste, estatística, distribuição, gl, função Excel, função R
3. Mapa de funções (mesmo conteúdo da aba `Mapa`)
4. Sete testes, cada um com: enunciado, passos 1 e 2 (hipóteses com a cauda justificada pelo verbo, alfa), passo 3 (fórmula e escolha Z ou T), Excel célula a célula, R na mão e função pronta com output real, passo 4 e 5 (crítico e valor-p, decisão, frase de interpretação), pegadinha do bloco
5. Exercícios E1 a E4 (enunciado e dados)
6. Pegadinhas consolidadas (ordem: mais martelado pelo professor primeiro) e templates de frase de interpretação
7. Gabarito de E1 a E4 (só números e decisão), depois de separador

Formatação obrigatória no vault (quirk do Dataview): fórmula Excel inline como =`FUNCAO()` com o sinal de igual fora do backtick; qualquer bloco multi-linha (Excel, R, output do R) em `<pre>` HTML com `<`, `>` e `&` escapados. Zero fenced code block. Zero travessão. Zero (i)(ii)(iii). Zero citação de fonte.

## 5. Os sete testes

Receita fixa em todos: 1 H0/H1 e cauda pelo verbo do enunciado ("aumentou/diminuiu" uni, "é diferente/mudou" bi). 2 alfa. 3 escolha e cálculo da estatística. 4 crítico e valor-p (o professor cobra os dois caminhos). 5 decisão e interpretação empresarial.

| # | Teste | Enunciado | H1 e cauda | Excel na mão | R | Intenção do resultado | Pegadinha |
|---|---|---|---|---|---|---|---|
| 1 | Z, uma média, sigma conhecido | Vendas: meta 500, n=36, x̄=520, sigma=30 (slide aula 3, só sumário) | μ>500, uni direita | `NORM.S.INV(1-α)`, `1-NORM.S.DIST(z,TRUE)` | `qnorm`, `pnorm` na mão (base R não tem z.test) | z=4, rejeita | Z só é legítimo com sigma dado |
| 2a | t, uma média, sumário | Satisfação: benchmark 7,0, n=20, x̄=6,8, s=0,5 (slide aula 3) | rodar duas vezes: μ≠7 e μ<7 | `T.INV.2T`, `T.INV`, `T.DIST.2T`, `T.DIST` | `qt`, `pt` | bicaudal não rejeita (p≈0,09), unicaudal rejeita (p≈0,045) | a cauda muda a decisão; `T.INV(α,gl)` sai negativo; `T.DIST.2T` exige valor absoluto |
| 2b | t, uma média, dados brutos | SLA 48h, n=25 entregas simuladas (exercício 1 aula 3) | μ>48, uni direita | `COUNT`, `AVERAGE`, `STDEV.S`, `SQRT`, `T.INV(1-α,gl)`, `T.DIST.RT` | `mean`, `sd`, `length`, depois `t.test(x, mu=48, alternative="greater")` | p entre 0,02 e 0,04: rejeita a 5%, não a 1% | alfa muda a decisão; `STDEV.S` e não `STDEV.P` |
| 3 | t pareado | Vendas antes/depois em 12 lojas simuladas (exercício 2 aula 3) | μ_D>0, uni direita, D=Depois−Antes | coluna D e repete o bloco 2b; atalho `T.TEST(dep,ant,1,1)` | `t.test(depois, antes, paired=TRUE, alternative="greater")` e `$conf.int` da versão bicaudal pro IC 95% de μ_D | rejeita claro; reportar D̄ (tamanho do efeito) e IC | pareado é uma amostra de diferenças; sinal de D |
| 4 | t duas médias independentes (Welch) | Ticket médio loja A (n=15) vs B (n=18), simulado. Extensão além dos slides | μ_A≠μ_B, bi | EP `SQRT(sA²/nA+sB²/nB)`, gl de Welch na célula, `T.DIST.2T`; atalho `T.TEST(A,B,2,3)` | `t.test(A, B)` (Welch é default; `var.equal=TRUE` só citado) | não rejeita a 5% por pouco (p entre 0,05 e 0,10) | gl de Welch não é n1+n2−2; `T.TEST` tipo 3 e não 2 |
| 5 | Z proporção | Golfe: baseline 20%, x=100 de n=400 (aula 4) | p>0,20, uni direita | `NORM.S.INV(0,95)`=1,645; `1-NORM.S.DIST(z,TRUE)` | z na mão com `pnorm`; `prop.test(100,400,p=0.2,alternative="greater",correct=FALSE)` e com `correct=TRUE` pra ver a diferença | z=2,5, p≈0,006, rejeita | p0 no denominador; `prop.test` default corrige continuidade |
| 6 | Qui-quadrado aderência | Pagamentos 100/60/40 vs 45/35/20, n=200 (exercício 1 aula 5, mesmo do script do professor) | pelo menos uma proporção difere, cauda direita | coluna (O−E)²/E, `SUM`, `CHISQ.INV.RT`, `CHISQ.DIST.RT`; atalho `CHISQ.TEST(obs,esp)` | soma na mão e `pchisq`; `chisq.test(x=obs, p=p_exp)` | χ²≈2,54, gl 2, não rejeita | gl=k−1; `CHISQ.TEST` devolve valor-p, não a estatística |
| 7 | Qui-quadrado independência | Canal x Compra 3x2, n=320 (exercício 2 aula 5) | canal e compra associados, cauda direita | matriz E com referências absolutas, (O−E)²/E, `SUM`, `CHISQ.DIST.RT`; atalho `CHISQ.TEST` | `matrix` e `dimnames` (código do professor), `chisq.test(tab)`, `$expected`, `$residuals` | χ²≈13,7, gl 2, rejeita; Search é o canal forte | gl=(r−1)(c−1); esperadas ≥5 (aviso do R no exercício 3 do professor) |

Parâmetros de simulação (ajustáveis no gerador até a intenção do resultado valer; valores finais ficam registrados no plano):

- 2b SLA: n=25, normal com média 49,5 e desvio 4, horas com 1 casa
- 3 Pareado: 12 lojas, Antes normal(200, 30), Depois = Antes + normal(12, 15), R$ mil com 1 casa
- 4 Welch: A n=15 normal(85, 12), B n=18 normal(95, 18), R$ com 1 casa
- E3 pareado: 10 pessoas, tempo de tarefa em minutos antes/depois de treinamento, Depois = Antes − normal(3, 4)
- E3 Welch: turma A n=12 normal(6,5, 1,2), turma B n=14 normal(7,2, 1,0), notas 0 a 10 com 1 casa

## 6. Exercícios

| # | Enunciado | Treina | Gabarito |
|---|---|---|---|
| E1 | Tempo de atendimento do professor: 12 obs (9,7 10,2 10,4 9,9 10,1 10,5 9,8 10,3 10,0 10,2 10,4 10,1), "mudou de 10 min?", α=5% | reproduzir resultado conhecido | t≈1,85, crítico 2,201, p≈0,09, não rejeita (bate com Resumo 08.07) |
| E2 | Conversão do site era 30%; landing nova deu 90 em 250 visitas; "mudou?" | proporção bicaudal e sensibilidade ao alfa | z≈2,07, p≈0,038: rejeita a 5%, não a 1% |
| E3 | Dois enunciados com dados: "mesmas 10 pessoas antes/depois do treinamento" e "duas turmas diferentes"; decidir pareado vs Welch e rodar | escolher o teste antes de calcular | um pareado, um Welch, números do gabarito vêm do R |
| E4 | 4 sabores 18/22/20/20, "preferência uniforme?" (slide aula 5) | qui-quadrado aderência com E iguais | χ²=0,4, gl 3, crítico 7,815, p≈0,94, não rejeita |

## 7. Layout do xlsx

Aba `Mapa`: colunas Objetivo | Excel EN | Excel PT | R | Devolve | Quando usar / observação. Linhas: n, média, desvio amostral, raiz, valor absoluto, Z crítico uni e bi, valor-p Z uni e bi, t crítico uni e bi, valor-p t direita, esquerda e bi, qui crítico, valor-p qui, atalhos `T.TEST` (tipos 1, 2, 3 e caudas 1, 2), `Z.TEST` (semântica: cauda superior), `CHISQ.TEST`, `t.test`, `prop.test`, `chisq.test`.

Aba de teste (padrão): título na linha 1; dados brutos na coluna A a partir da linha 3 (quando houver); bloco de passos em C:D com rótulo e valor: 1 H0, H1, cauda (texto); 2 α (input azul); 3 n, média, s (ou p̂), EP, estatística, gl; 4 crítico, valor-p; 5 decisão via =`IF(p<α,"Rejeita H0","Não rejeita H0")` e interpretação (texto). Inputs (μ0, σ, α, p0) em fonte azul, fórmulas em preto. Bloco "Atalho Excel" ao lado (`T.TEST`, `Z.TEST`, `CHISQ.TEST`) mostrando o mesmo valor-p. Formato numérico: estatística 3 casas, valor-p 4 casas. Testes 6 e 7: tabelas O e E lado a lado, coluna ou matriz (O−E)²/E, soma.

Aba `Exercicios`: dados de E1 a E4 em blocos separados, só rótulos e dados.

## 8. Script R

Cabeçalho: como rodar (`Rscript TestesHipotese.R` ou `source("TestesHipotese.R")` dentro do R, ou colar bloco a bloco). Seção 0: um helper mínimo `decide(p, alpha)` que imprime "Rejeita H0" ou "Não rejeita H0" (único helper; o resto é função nativa visível). Seções 1 a 7 espelham o md: dados hardcoded, cálculo na mão, função pronta, `cat` comparando os dois. Cada argumento comentado na primeira vez que aparece. Seção 8: dados dos exercícios. Seção 9: gabarito comentado.

## 9. Validação

- R: `Rscript TestesHipotese.R` roda inteiro sem erro. Output salvo e todo número do md copiado dele.
- Excel: workbook gerado com openpyxl, recalculado no LibreOffice headless, valores lidos de volta. Tabela cruzada R x Excel (estatística, crítico, valor-p de cada teste e dos gabaritos), tolerância 0,001. Qualquer par fora da tolerância bloqueia a entrega até explicar (diferença legítima documentada, como continuidade em `prop.test`, ou bug corrigido).
- md: todo wikilink resolve em nota existente ou criada; zero travessão, zero (i)(ii), zero fonte; nenhum fenced code block; abrir e conferir render dos `<pre>`.
- Escopo: nada além da seção 2.

## 10. Pronto

Três arquivos na pasta, notas de conceito novas criadas, mensagem final com a tabela cruzada R x Excel e a linha de "como usar".

## 11. Decisões registradas (perguntas do brainstorming)

- Escopo: núcleo + Welch + prévia de qui-quadrado (Arthur, 2026-08-17)
- Dados: simulados com seed, sem esperar download do eClass
- Ambiente: R via Homebrew, sem RStudio
- Formato: md + xlsx + R (opção A)
- Local do spec e do plano: pasta oculta `.superpowers/` dentro da pasta da aula (vault não é git, Obsidian não indexa dotfolder)
