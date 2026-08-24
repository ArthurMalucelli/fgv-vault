---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, lean]
---

# Trabalho Padronizado

## Definicao

Sequencia de trabalho definida, documentada e seguida por todos que executam a mesma tarefa. SOP (Standard Operating Procedure). Faz parte da base da [[Casa do Lean]] junto com [[Heijunka]] e [[Kaizen]].

## Por que e base do Lean

Sem padrao, nao tem como:
- Detectar anormalidade (nao se sabe o que e "normal").
- Aplicar [[Jidoka]].
- Medir melhoria via [[PDCA]].
- Treinar pessoa nova sem perda de qualidade.

Padronizar nao engessa, **viabiliza melhoria**. Cada [[Kaizen]] bem-sucedido vira o novo padrao.

## Componentes tipicos

1. Sequencia de tarefas.
2. [[Takt time]] / tempo de ciclo alvo.
3. Estoque padrao em processo (WIP minimo).

## Aplicacao em servicos

Em servicos digitais, Trabalho Padronizado vira:
- SOP por categoria de problema (ex.: criterio de moderacao por tipo de violacao).
- Checklist binario para decisao operacional.
- Wiki interna referenciada pela ferramenta usada na operacao.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Casa do Lean]]
- [[Kaizen]]
- [[Jidoka]]
- [[PDCA]]
- [[5W2H]]
