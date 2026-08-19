---
tipo: spec
materia: ContabilidadeFinanceira
data: 2026-08-19
tags: [spec]
---

# Spec: resolução do Caso Marcus Dent (Contabilidade Financeira, aula 19/08)

## Objetivo

Resolver a atividade "Marcus Dent" (Profa. Edilene, fechamento do tema 4, regime de caixa vs competência) e deixar no vault um material de estudo com duas peças: uma resolução em markdown e uma planilha em fórmulas. Enunciado em `ContabilidadeFinanceira/Aulas/08.19/Slides/Atividade Marcus Dent 2024-2.pdf`.

Pedido da professora: lucro ou prejuízo do mês, caixa gerado ou utilizado no mês, balanço no início e no fim do mês, tabela comparativa Fluxo de Caixa vs DRE. Extra aprovado: reconciliação lucro até variação de caixa pelo método indireto.

## Resultado esperado (gabarito que os arquivos têm que reproduzir)

BP inicial 31/12/2023: Caixa 10.000, Equipamentos 54.000, total 64.000. Empréstimo 54.000, Capital 10.000, total 64.000.

Transações de janeiro (Caixa / DRE / BP):

| # | Evento | Caixa | DRE | BP |
|---|---|---|---|---|
| T1a | Serviços 8.000, 20% à vista | +1.600 | Receita 8.000 | Clientes +6.400 |
| T1b | Adiantamento por serviço de março | +2.000 | 0 | Receita antecipada (P) +2.000 |
| T2 | Aluguel jan e fev, 2.200 | (2.200) | (1.100) | Despesa antecipada (A) +1.100 |
| T3 | Material 3.000 à vista, sobra 1.300 | (3.000) | (1.700) | Estoque +1.300 |
| T4 | Salário 500, pago em fevereiro | 0 | (500) | Salários a pagar +500 |
| T5 | Depreciação 54.000 / 36 | 0 | (1.500) | Depreciação acumulada (1.500) |
| T6 | Juros 2% x 54.000 | 0 | (1.080) | Juros a pagar +1.080 |

Tabela comparativa: entradas 3.600 e saídas 5.200, variação de caixa (1.600). Receitas 8.000 e despesas 5.880, lucro 2.120. DRE com resultado operacional 3.200 antes dos juros.

BP final 31/01/2024, total 69.700:

- Ativo circulante 17.200: caixa 8.400, clientes 6.400, estoque 1.300, despesa antecipada 1.100.
- Ativo não circulante 52.500: equipamentos 54.000 menos depreciação acumulada 1.500.
- Passivo circulante 2.500: salários a pagar 500, receita antecipada 2.000.
- Passivo não circulante 55.080: empréstimo 54.000, juros a pagar 1.080.
- PL 12.120: capital 10.000, lucros acumulados 2.120.

Reconciliação indireta: 2.120 + 1.500 + 1.080 − 6.400 − 1.300 − 1.100 + 500 + 2.000 = (1.600).

Amarras obrigatórias: equação patrimonial fecha em cada coluna, lucro da DRE igual à variação de lucros acumulados, caixa final da DFC igual ao caixa do BP, reconciliação indireta igual à variação de caixa direta.

Decisões técnicas explicitadas no md: empréstimo e juros ficam no não circulante porque vencem em dezembro de 2025, mais de 12 meses da data do balanço. Juros de janeiro são 1.080 tanto em capitalização simples quanto composta, a diferença só aparece a partir de fevereiro.

## Entregáveis

Ambos em `~/FGV/ContabilidadeFinanceira/Aulas/08.19/`. O PDF do enunciado fica onde está, em `Slides/`.

### ResolucaoCasoMarcusDent.md

YAML: materia ContabilidadeFinanceira, data 2026-08-19, tema, tags `[caso, resolucao]`. Seções, nesta ordem:

1. Respostas diretas (tabela: lucro do mês, variação de caixa, totais dos dois balanços).
2. BP inicial.
3. Mapa das transações (tabela acima).
4. Tabela comparativa no layout exato da professora.
5. DRE de janeiro.
6. Fluxo de caixa de janeiro, método direto, com caixa inicial e final.
7. BP final, separado em circulante e não circulante.
8. Reconciliação lucro até caixa, método indireto.
9. Pegadinhas e pontos de prova.
10. Pra fixar: lista de wikilinks.

Regras de escrita: sem travessões, sem enumeradores inline, sem citar fontes, voz direta. Wikilinks na primeira ocorrência relevante de cada conceito.

### MarcusDentDFs.xlsx

Quatro abas, todos os números derivados de `Premissas` por fórmula. Convenção visual do Zezinho: azul é input, preto é fórmula, verde é link entre abas.

- `Premissas`: empréstimo, taxa mensal, vida útil em meses, capital inicial, serviços do mês, percentual recebido à vista, adiantamento, aluguel pago e número de meses cobertos, compra de material, estoque final, salário do mês.
- `Transacoes`: linhas são as contas do BP (ativo, passivo, PL), depois as linhas da DRE (receita, cada despesa, lucro), depois a linha de caixa. Colunas: BP inicial, T1a, T1b, T2, T3, T4, T5, T6, BP final. Linha de check `Ativo − (Passivo + PL)` em cada coluna. Linha de check `lucro da DRE − variação de lucros acumulados`.
- `Comparativo`: a tabela da professora (receitas e entradas, despesas e saídas, subtotais, resultado), duas colunas, puxando de `Transacoes`.
- `Reconciliacao`: método indireto, com check contra a variação de caixa da linha de caixa de `Transacoes`.

Gerar com openpyxl, recalcular com LibreOffice headless e verificar que todos os checks dão zero antes de considerar pronto.

## Conceitos no vault

Linkar nas notas já existentes: Regime de Caixa, Regime de Competência, DRE, DFC, Balanço Patrimonial, Equação Patrimonial, Depreciação, Despesa Antecipada, Adiantamento de Cliente (alias "receita antecipada", sem criar duplicata), Contas a Receber, Contas a Pagar, Estoque, Método Indireto, Lucros Acumulados, Resultado Financeiro, EBIT, Ativo Circulante, Ativo Não Circulante, Caso Zezinho Pipoqueiro (comparação).

Criar com o template `Vault/Templates/Conceito.md`: Caso Marcus Dent, Passivo Circulante, Passivo Não Circulante, Imobilizado, Juros a Pagar, Reconhecimento da Receita, Confrontação. Preencher só o que a aula e o enunciado sustentam, o resto fica `// preencher`.

## Fora de escopo

Sem tasks no Tasks.md (o enunciado não traz prazo). Sem update de Google Calendar (não há transcript nem menção de próxima aula). Sem entregável formal em PDF ou DOCX. Sem discussão de sustentabilidade do negócio além de uma linha nas pegadinhas.

## Verificação

Planilha recalculada com todos os checks em zero. Números do md iguais aos da planilha. Wikilinks apontando para notas existentes (sem link quebrado). Commit no vault: `contabilidade: resolução do caso Marcus Dent (19/08)`.
