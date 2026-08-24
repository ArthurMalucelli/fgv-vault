---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, ia, tecnologia]
---

# Agente de IA

## Definicao

Sistema baseado em [[LLM]] que executa tarefas multi-step de forma **autonoma**, sem precisar de interacao prompt-resposta a cada passo. Decide, age, observa o resultado e itera.

## Diferenca pra IA generativa "conversacional"

- Conversacional: voce manda prompt, IA responde, voce manda outro prompt.
- Agente: voce define um objetivo, e o agente quebra em passos, executa cada um, usa ferramentas (search, code, APIs) e entrega o resultado final.

## Componentes tipicos

1. **Modelo base** ([[LLM]]).
2. **Ferramentas** (tool use): browser, terminal, APIs externas.
3. **Planejamento** (chain-of-thought, ReAct, etc).
4. **Memoria** (curto e longo prazo).
5. **Loop** de acao-observacao-decisao.

## Aplicacao em operacoes

- Automacao de workflow de SAC.
- Monitoramento autonomo de cadeia de suprimentos.
- Geracao automatica de relatorios.
- Execucao de tarefas administrativas (preencher formulario, agendar, comprar).
- Exemplo informal do trecho da aula: aluno menciona usar agente pra abrir Pix e comprar ingresso no momento exato do lancamento.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[LLM]]
- [[IA Generativa]]
