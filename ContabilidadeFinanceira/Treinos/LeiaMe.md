---
materia: ContabilidadeFinanceira
tema: Treinos de elaboração das DFs
tags: [treino, indice]
---

# Treinos: elaboração das DFs

Cinco casos novos no formato da atividade HypeDrop e da planilha da videoaula do tema 3. Cada caso tem um enunciado em markdown e uma planilha com as abas de trabalho e o gabarito.

## Os exercícios

| # | Caso | Nível | Transações | Tempo alvo | O que entra de novo |
|---|---|---|---|---|---|
| 1 | [[Ex1_GraoDeOuro\|Cafeteria Grão de Ouro]] | Fácil | 6 | 15 min | Repertório exato da aula, tudo à vista ou a prazo simples |
| 2 | [[Ex2_PedalUrbano\|Bike Shop Pedal Urbano]] | Fácil | 6 | 15 min | Venda a prazo e contas a receber, primeiro caso com FCO negativo |
| 3 | [[Ex3_ValeVerde\|Distribuidora Vale Verde]] | Médio | 8 | 25 min | Balanço de abertura, recebimento que não é receita, capex a prazo, aporte e dividendos |
| 4 | [[Ex4_ClinicaVetor\|Clínica Vetor]] | Médio | 8 | 25 min | Empresa de serviços, custo do serviço prestado contra despesa, consumo de estoque sem caixa |
| 5 | [[Ex5_MarGrosso\|Cervejaria Mar Grosso S.A.]] | Difícil | 12 | 45 min | Depreciação, adiantamento de cliente, empréstimo com principal e juros separados, IR com parcela a pagar, capex financiado |

Ordem sugerida: na sequência. O 5 pressupõe que o 3 e o 4 já estão automáticos.

## Como usar a planilha

Quatro abas em cada arquivo:

- `Equação`: efeito de cada transação em Ativo, Passivo e PL, no formato do slide da professora. Duas linhas por transação, porque muita transação mexe em duas contas do mesmo lado. A coluna Check acusa na hora se aquela transação fechou.
- `Plan`: a planilha de trabalho, com Balanço Patrimonial, DRE e DFC. Uma coluna por transação.
- `Gabarito`: mesma estrutura, preenchida. Não abre antes de terminar, o check já te diz se acertou.
- `Gabarito Equação`: idem para a primeira aba.

Convenções:

- Célula amarela é sua. Total, saldo final, subtotal de DRE e DFC, variação de caixa e indicadores são fórmula, calculam sozinhos.
- Reduções entram negativas. CMV, despesas, pagamentos e amortizações são números negativos.
- A coluna Check compara o seu saldo final com o gabarito e mostra ✔ ou ✗ por linha.
- A linha "Diferença, se houver" tem que dar zero em todas as colunas, inclusive nas intermediárias. Se uma coluna isolada não fecha, o erro está naquela transação específica, o que poupa procurar no arquivo inteiro.
- A última amarra é "Caixa final da DFC menos Caixa do BP". Se der zero, as três demonstrações estão consistentes entre si.

## Roteiro para atacar qualquer um deles

1. Lê a transação e pergunta primeiro: mexeu no caixa? Se sim, tem linha na DFC e você já sabe o sinal.
2. Pergunta segundo: gerou receita ou consumiu recurso no período? Se sim, tem linha na DRE. [[Regime de Competência]] manda aqui, não o caixa.
3. Pergunta terceiro: o que mudou de saldo no balanço? Toda transação mexe em pelo menos duas contas, e os dois lados da [[Equação Patrimonial]] têm que continuar iguais.
4. Só depois de rodar as três perguntas você preenche a coluna.

Armadilhas que esses casos plantam de propósito: recebimento de cliente antigo não é receita, compra a prazo de imobilizado não é saída de caixa, adiantamento de cliente não é receita, dividendo não é despesa, e consumo de estoque não é evento de caixa.

## Conceitos cobrados

[[Balanço Patrimonial]], [[DRE]], [[DFC]], [[Equação Patrimonial]], [[Regime de Competência]], [[Custo vs Despesa]], [[Lucro Bruto]], [[Despesas Operacionais]], [[EBIT]], [[Margem Bruta]], [[Capital de Giro]], [[Método Indireto]], [[Capex]], [[Depreciação]], [[Resultado Financeiro]], [[Patrimônio Líquido]]

Material de origem na pasta da aula de 10.08: `T3 Efeito de Trans básicas nas DFs v2.pdf`, `T3 Ativ_ImpDFs_HypeDrop.pdf` e `Planilha DFs principais usada na videoaula.xlsx`. A base conceitual está em `EstudoDFs.md`.
