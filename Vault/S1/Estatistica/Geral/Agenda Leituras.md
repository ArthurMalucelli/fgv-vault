---
materia: Estatistica
professor: Nelson Lerner Barth
semestre: 2026.1
turma: T6
livro_texto: Anderson, Sweeney, Williams, Camm, Cochran. Estatística Aplicada à Administração e Economia. 5ª ed. Cengage, 2021
tags: [agenda, leituras, geral]
---

# Agenda de Leituras e Exercícios, Estatística I 2026.1

Fonte: `agenda.docx` (Geral). Livro-texto disponível no eClass via Biblioteca Virtual → MinhaBiblioteca, busca "Anderson". Soluções no Apêndice D.

## Bloco 1, Análise Univariada

### Variáveis (aulas 1)
Revisar a aula, saber classificar variáveis. Achar livro-texto no eClass.

### Tabelas, frequências, gráficos (aula 2)
- **Cap 2.1** Sintetizando dados pra variável categorizada (qualitativa)
- **Cap 2.2** Sintetizando dados pra variável quantitativa (não ler "ramos e folhas")
- **Exercícios cap 2:** 3, 4, 12, 22 (todos a lápis, sem Excel)

### Medidas de posição (aula 3)
- **Cap 3.1** Medidas de posição (não ler Média Geométrica nem Percentis)
- **Cap 3.4** Regra dos cinco itens, boxplot
- **Exercício cap 3:** 10 (calcule no Excel, ignore resposta do apêndice)
- **Exercício "Transporte"** (Conteúdo no eClass)

### Pesquisa em grupo (aula 4)
1º relatório, planejamento da pesquisa. Entrega via eClass até 04/03 23h58. Arquivo PDF nomeado A, B, C... pela letra da equipe. Um membro entrega.

### Dispersão (aula 5)
- **Cap 3.2** Medidas de variabilidade
- **Cap 3.3** ler **apenas Regra Empírica**
- **Exercícios cap 3:** 38, 44

### Padronização Z (aula 6)
- **Cap 3.3** ler **Forma de Distribuição** (sem fórmula) e **Scores-z**
- Exercício adaptado de Larson & Farber: idade Helen Mirren, z-escore esportivo Maria/Joana
- Exercício "padronizar variável e recalcular após alterar dados"
- Exercício Conceitual do penúltimo slide

### Coeficiente de variação (aula 7)
- Lista 1, 16 exercícios (questionário no eClass)

## Bloco 2, Análise Bivariada

### Quanti-quanti (aula 9)
- **Cap 3.5** (exceto Notas & Comentários)
- **Apêndice 3.2** (funções Excel)
- Exercícios: diagrama dispersão Renda × Educação, tabela Reclamações × Satisfação (covariância e correlação)
- **Pegadinha:** mudança de escala (multiplicar por 10) NÃO afeta correlação

### Quali-quali e quali-quanti (aula 10)
- Tabelas de contingência, proporções condicionais
- Exercícios: polícia única na cidade, inadimplência × emprego, cerveja × sexo, propaganda com efeitos especiais (boxplots)

## Bloco 3, Distribuições

### VA discreta + Binomial (aulas 14-15)
- **Cap 5** distribuição de probabilidade discreta
- **Cap 5.4** Binomial, condições de aplicabilidade
- Exercícios cap 5: ver lista no eClass
- **Pegadinha "ao menos k":** P(X≥k) = 1 - P(X≤k-1)

### VA contínua, Normal (aulas 17-18)
- **Cap 6.1** ler com atenção
- **Cap 6.2** ler até "Distribuição de Probabilidade Padrão" (parar antes)
- **Apêndice 6.2** apenas DIST.NORM.N e INV.NORM.N (não ler DISTR.EXPON)
- **Exercícios cap 6:** 18, 20, 24, 40, 46, 48
- Exercícios extras: demanda de pães (P(>450), quantidade pra 2% de falta), notas de exame (corte 20% melhores), altura noruegueses, TV tipo A vs tipo B (E(lucro))

## Bloco 4, Inferência

Conteúdo na agenda termina antes desse bloco, leituras serão indicadas em aula.

## Pegadinhas-chave da agenda

1. **Boxplot:** outlier exige > 1,5 × IIQ acima de Q3 (ou abaixo de Q1). Limite superior do exemplo: 570 + 1,5·430 = 1215, então 810 e 900 não são outliers.
2. **Z-score:** padronização preserva quem é melhor relativamente, independente de escala original. Maria > Joana se z_Maria > z_Joana, comparáveis entre testes diferentes.
3. **Correlação invariante a escala:** multiplicar variável por 10 não muda r. Mudança de escala mexe em covariância e desvio padrão na mesma proporção, efeitos cancelam.
4. **DIST.NORM.N retorna acumulada à esquerda.** Cauda direita = 1 - DIST.NORM.N(...).
5. **INV.NORM.N pede acumulada, não cauda.** Pra "5% maiores" passa 0,95.
6. **Variância vs DP no Excel da Normal:** Excel pede σ. Se enunciado dá σ², tira raiz.

## Conceitos cobertos

- [[Variancia e desvio padrao]]
- [[Variavel aleatoria discreta]]
- [[Variavel aleatoria continua]]
- [[Distribuicao binomial]]
- [[Distribuicao normal]]
- [[Distribuicao uniforme continua]]
- [[Distribuicao exponencial]]
- [[Funcao densidade de probabilidade]]
