---
title: Weekly FGV Summary Email
date: 2026-05-25
status: design-approved
---

# Weekly FGV Summary Email

Automação semanal: agente remoto manda email todo domingo 19h com look-ahead da semana de aula.

## Objetivo

Forward-looking puro. Provas, quizzes, entregas e atividades especiais da próxima semana (seg→dom), classificadas e ranqueadas por prioridade de estudo. Sem recap das aulas passadas. Sem dependência de filesystem local.

## Arquitetura

Agente remoto único na cloud Claude, cron `0 19 * * SUN` no timezone America/Sao_Paulo. Roda independente do Mac estar ligado.

```
Cron SUN 19h
    │
    ▼
[Agente remoto Claude]
    │
    ├──► Google Calendar MCP
    │      • Quiz & Provas (id 5364ec8461a80aea18246284ea4498cc0d258e24d42d2ad258a6a12c2515ee22@group.calendar.google.com)
    │      • Provas (id c845edd1eb15fdad75fc61b862906108b05520941d33dba93a90dda87b4761dc@group.calendar.google.com)
    │      • FGV (id 3e341bf84fff75ab530880c9e2d913e8db69b951e8fc4e2b860283171971e4a7@group.calendar.google.com)
    │
    ├──► Classificação + ranking
    │
    └──► Gmail MCP
           • from/to: arthurmalucelli89@gmail.com
```

## Pipeline

1. Time window: próxima segunda-feira 00:00 (timezone America/Sao_Paulo) até segunda seguinte 00:00. Como o cron roda domingo 19h, isso é "amanhã 05:00 UTC + 7 dias".
2. List events de **Quiz & Provas** e **Provas** sem filtro. Tudo dentro desse window vira candidato. Deduplicar por título+início+sala (Provas é redundante com Quiz & Provas conforme convenção atual).
3. List events de **FGV** com filtro de keywords na descrição ou título: `apresenta`, `entrega`, `trabalho`, `relatório`, `mini-prova`, `orienta`. Eventos sem keyword viram aulas regulares e são descartados.
4. Classifica por tipo:
   - 🔴 Prova: título contém `prova` (case-insensitive)
   - 🟠 Quiz: título contém `quiz`
   - 🟡 Entrega/Apresentação/Orientação: resto
5. Ranking de estudo: pondera por (peso do tipo × proximidade temporal inversa). Pesos: prova 3, quiz 2, entrega 1.5, orientação 1.
6. Compõe email (formato abaixo).
7. Envia via Gmail MCP.

## Formato do email

Subject: `[FGV] Semana DD/MM → DD/MM`

Body (markdown, sem travessão, sem (i)(ii)):

```
🔴 PROVAS
• <Matéria> <tipo>, <dia> <DD/MM> <HH:MMh> sala <X>

🟠 QUIZZES
• <Matéria>, <dia> <DD/MM> <HH:MMh>

🟡 ENTREGAS
• <Matéria> <descrição>, <DD/MM>

Ranking de estudo:
1. <Matéria> (<razão>)
2. ...
```

Edge cases:
- Semana vazia: body `"Semana sem eventos críticos. Foco em [matérias com prova/entrega na semana seguinte se houver]."`
- Bucket vazio: omitir cabeçalho.
- Calendar MCP falha: 1 retry. Se falhar de novo: body `"Erro ao acessar Calendar. Verificar conexão da skill schedule."`

## Dependências cloud

Pré-requisito: agente remoto Claude tem que ter **Google Calendar** e **Gmail** conectados (não só MCPs locais). Se não estiverem, primeiro setup roda fluxo de auth na Claude web.

## Tasks.md fica fora

Decisão tomada: sem GitHub bridge, agente remoto não acessa filesystem local. Tudo que pesa precisa estar no Google Calendar. Se houver prazo importante que só existe no Tasks.md, criar evento espelho no calendário Quiz & Provas manualmente.

## Não-objetivos

- Recap das aulas passadas (descartado: depende de filesystem local).
- Sugestão de capítulos/conteúdo específico pra estudar (depende de ler Resumo.md).
- Inclusão de Galapagos/MLS, treino, outros projetos (escopo travado em FGV).
- Múltiplos destinatários (só Arthur).

## Manutenção

- Mudança de calendário (IDs): editar prompt do agente.
- Mudança de horário: `schedule update <id>`.
- Pausar (férias longas): `schedule pause <id>` (se a skill suportar).
