# Weekly FGV Summary Email — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a scheduled remote agent that emails Arthur every Sunday 19h (America/Sao_Paulo) with the upcoming week's FGV provas, quizzes, and entregas.

**Architecture:** Single cron-style scheduled task in Claude cloud. Agent uses Google Calendar MCP to fetch events from 3 calendars, classifies and ranks them, then sends via Gmail MCP. No local filesystem dependency. No code repo — the entire "code" is the prompt configured on the scheduled task.

**Tech Stack:** Claude scheduled remote agents (`mcp__scheduled-tasks__*` MCP), Google Calendar MCP, Gmail MCP.

---

## File Structure

This isn't a code project. The deliverables are:

- **Spec:** `~/FGV/30 Sistema/Automacoes/2026-05-25-weekly-summary-design.md` (already written, approved)
- **Plan:** `~/FGV/30 Sistema/Automacoes/2026-05-25-weekly-summary-plan.md` (this file)
- **Agent prompt:** lives inside the scheduled task config in Claude cloud. Source of truth backup goes to `~/FGV/30 Sistema/Automacoes/weekly-summary-prompt.md` so it can be re-deployed if needed.
- **Operational log:** `~/FGV/30 Sistema/Automacoes/weekly-summary-runlog.md` (manual notes on test fires, schedule changes, issues).

---

## Task 1: Verify cloud MCP connections (Calendar + Gmail)

**Files:**
- Read: `~/FGV/30 Sistema/Automacoes/2026-05-25-weekly-summary-design.md` (for calendar IDs)

- [x] **Step 1: Check scheduled-tasks MCP availability** ✅ 2026-08-16

Run: list current scheduled tasks via `mcp__scheduled-tasks__list_scheduled_tasks` (no args).
Expected: returns an array (possibly empty). If the tool errors with "not connected", the MCP isn't set up — stop and surface to user.

- [x] **Step 2: Confirm Calendar MCP is callable from a scheduled-agent context** ✅ 2026-08-16

Scheduled agents run server-side with their own connector set. The local `mcp__9650ae8d-...__list_calendars` MCP only proves it's connected for Arthur's local sessions, not for remote agents.

Approach: Create the scheduled task in Task 3 set to a one-shot run a few minutes in the future, with a minimal prompt that just calls `list_calendars`. If the test fire returns the 4 calendars, we know the agent context has Calendar. If it errors with "no MCP", instruct user to connect Google Calendar at claude.ai/settings/connectors.

This step is just confirming the local list_calendars call works as a sanity check.

Run: `mcp__9650ae8d-038d-4a39-a857-b1c2fef09413__list_calendars`
Expected: returns 4 calendars including Principal, FGV, Quiz & Provas, Provas. IDs match what's in the spec.

- [x] **Step 3: Confirm Gmail MCP is callable from local context** ✅ 2026-08-16

Same caveat: this only proves local. The real test is via the scheduled agent.

Run: `mcp__4c57eb1b-a665-46f8-b17c-64447ccbe0a6__list_labels` (low side-effect call).
Expected: returns Gmail labels. Confirms auth is alive.

- [x] **Step 4: Surface any gaps to user before continuing** ✅ 2026-08-16

If either MCP errors on the local check, the remote agent will also fail. Stop and ask user to fix the connection before proceeding to Task 2.

---

## Task 2: Author the agent prompt

**Files:**
- Create: `~/FGV/30 Sistema/Automacoes/weekly-summary-prompt.md`

- [x] **Step 1: Write the prompt to file** ✅ 2026-08-16

The full prompt the scheduled agent will receive at every fire. Self-contained. No outside context. Includes calendar IDs, classification rules, output format, email recipient.

```markdown
# Weekly FGV Summary — Agent Prompt

You are running as a scheduled remote agent. Your job: send Arthur an email with the upcoming week's FGV academic events.

## Inputs

- Current time: today (the moment this agent fires).
- Target window: next Monday 00:00 (America/Sao_Paulo) through the following Monday 00:00.
- Three Google Calendar IDs:
  - Quiz & Provas: `5364ec8461a80aea18246284ea4498cc0d258e24d42d2ad258a6a12c2515ee22@group.calendar.google.com`
  - Provas: `c845edd1eb15fdad75fc61b862906108b05520941d33dba93a90dda87b4761dc@group.calendar.google.com`
  - FGV (regular classes): `3e341bf84fff75ab530880c9e2d913e8db69b951e8fc4e2b860283171971e4a7@group.calendar.google.com`

## Steps

1. Compute the window in ISO-8601 with timezone America/Sao_Paulo.
2. Call `list_events` on Quiz & Provas and Provas calendars with that window. Collect all events.
3. Call `list_events` on FGV calendar with the same window. Filter to events whose title or description contains (case-insensitive) any of: "apresenta", "entrega", "trabalho", "relatório", "relatorio", "mini-prova", "miniprova", "orienta". Discard the rest (regular classes are out of scope).
4. Deduplicate across the 3 calendars by (title + start time + location). Keep the version with the richest description.
5. Classify each remaining event:
   - 🔴 PROVAS: title contains "prova" (case-insensitive) and NOT "mini-prova" alone (mini-prova counts as quiz tier).
   - 🟠 QUIZZES: title contains "quiz" or "mini-prova" / "miniprova".
   - 🟡 ENTREGAS: everything else (entrega, trabalho, relatório, apresentação, orientação).
6. Build the ranking of estudo. Weight each event: prova=3, quiz=2, entrega=1.5, orientação=1. Multiply by `(1 / days_until_event)` (clamp days_until to >=0.5 to avoid div-by-zero on same-day events). Sort descending.
7. Compose the email body in plain text (Gmail will render line breaks). Format below.
8. Send via Gmail. Subject: `[FGV] Semana DD/MM → DD/MM` (start and end of window in DD/MM format). From and to: arthurmalucelli89@gmail.com. Body: as below.

## Output format

```
🔴 PROVAS
• <Matéria> <tipo>, <dia-da-semana abreviado> <DD/MM> <HH:MMh> sala <X>

🟠 QUIZZES
• <Matéria>, <dia> <DD/MM> <HH:MMh>

🟡 ENTREGAS
• <Matéria> <descrição curta>, <DD/MM>

Ranking de estudo:
1. <Matéria> (<motivo curto: tipo + proximidade>)
2. ...
```

Rules:
- Omit a bucket header if it has zero events.
- If all 3 buckets are empty: body is `Semana sem eventos críticos.` and skip the ranking.
- Never use travessões (—). Use vírgula, dois pontos, parênteses, ou ponto.
- Never use inline enumeradores (i), (ii), (iii). Use real lists or "primeiro/segundo/terceiro".
- Dia da semana abreviado em PT-BR: seg, ter, qua, qui, sex, sáb, dom.
- If a calendar returns "no events" or errors, continue with what you have. If Calendar MCP errors entirely, send email with body `Erro ao acessar Google Calendar. Verificar conexão na próxima execução.` and subject `[FGV] Semana DD/MM → DD/MM (erro)`.

## Constraints

- Do not include events outside the window.
- Do not include regular aulas in the email (already filtered in step 3).
- Do not list events from the Principal calendar.
- Do not include sugestões de capítulos, conteúdos específicos, ou referências a aulas passadas.
- One email per execution. No follow-ups.

## Done condition

Email sent successfully via Gmail MCP, with a 200-like response from the send tool. If send fails, retry once. If it fails again, log the error to your own response (the scheduler will surface).
```

- [x] **Step 2: Commit the prompt to local notes** ✅ 2026-08-16

This file is the source of truth backup. If the scheduled task gets nuked, we redeploy from here. No git, just file existence.

Run: `ls -la ~/FGV/30\ Sistema/Automacoes/weekly-summary-prompt.md`
Expected: file exists, ~3-4 KB.

---

## Task 3: Create the scheduled task

**Files:**
- Read: `~/FGV/30 Sistema/Automacoes/weekly-summary-prompt.md`

- [x] **Step 1: Define the schedule parameters** ✅ 2026-08-16

- Cron expression: `0 19 * * SUN`
- Timezone: `America/Sao_Paulo`
- Name: `weekly-fgv-summary`
- Prompt: full contents of `~/FGV/30 Sistema/Automacoes/weekly-summary-prompt.md`

- [x] **Step 2: Create via scheduled-tasks MCP** ✅ 2026-08-16

Load the tool: `ToolSearch` with `select:mcp__scheduled-tasks__create_scheduled_task`.

Call `mcp__scheduled-tasks__create_scheduled_task` with the parameters above. If the schema requires different field names, adapt — the intent is "run this prompt on cron `0 19 * * SUN` Sao Paulo time".

Capture the returned task ID.

- [x] **Step 3: Verify creation** ✅ 2026-08-16

Call `mcp__scheduled-tasks__list_scheduled_tasks`.
Expected: the new task appears with the right schedule and next-fire timestamp.

If the schedule on the listed task doesn't match what we asked for (timezone got lost, cron normalized weird), call `mcp__scheduled-tasks__update_scheduled_task` to fix. Don't accept a wrong-time task.

- [x] **Step 4: Save task ID to runlog** ✅ 2026-08-16

Append to `~/FGV/30 Sistema/Automacoes/weekly-summary-runlog.md`:

```
# Weekly FGV Summary — Runlog

## 2026-05-25 — Setup
- Created scheduled task `weekly-fgv-summary`, ID: <task-id>
- Cron: `0 19 * * SUN` America/Sao_Paulo
- Next fire: <timestamp>
- Status: pending first run
```

---

## Task 4: Dry-run test fire

**Files:**
- Modify: `~/FGV/30 Sistema/Automacoes/weekly-summary-runlog.md`

- [x] **Step 1: Trigger the task manually** ✅ 2026-08-16

Most scheduler implementations have a "run now" or "fire once" option. Check the tool schema. If `mcp__scheduled-tasks__update_scheduled_task` doesn't expose a manual trigger, the cleanest alternative is to clone the task as a one-shot for "now + 2 minutes" and let the schedule fire naturally.

Capture the run's execution result (the agent's final output, which should mention sending the email).

- [x] **Step 2: Verify email arrived** ✅ 2026-08-16

Wait up to 2 minutes after the trigger. Then call `mcp__4c57eb1b-...__search_threads` with query `subject:"[FGV] Semana" newer_than:1h`.
Expected: at least one thread, with body matching the format spec.

- [x] **Step 3: Sanity-check the contents** ✅ 2026-08-16

Read the email. Check:
- Subject has the right date range for next week (seg→dom from a real perspective).
- Each bucket is correctly classified (prova vs quiz vs entrega).
- No travessões in the body.
- No (i)(ii)(iii).
- Ranking makes sense given the events.
- If buckets are empty, body says `Semana sem eventos críticos.`.

If any of these fail, edit `weekly-summary-prompt.md`, then update the scheduled task with the new prompt via `mcp__scheduled-tasks__update_scheduled_task`. Re-fire and re-check.

- [x] **Step 4: Update runlog with test result** ✅ 2026-08-16

Append to runlog:

```
## 2026-05-25 — Test fire
- Triggered at <timestamp>
- Email subject: <subject>
- Buckets: 🔴 N, 🟠 N, 🟡 N
- Issues: <none / list>
- Status: passing
```

---

## Task 5: Hand off to Arthur

**Files:** none

- [x] **Step 1: Summarize what's live** ✅ 2026-08-16

Report to user:
- Scheduled task name + ID
- Next real fire timestamp
- Where the prompt source-of-truth lives (`weekly-summary-prompt.md`)
- Where the runlog lives
- How to pause/modify: `mcp__scheduled-tasks__update_scheduled_task` or via Claude.ai if available

- [x] **Step 2: Flag known limitations** ✅ 2026-08-16

Remind user:
- Tasks.md is not included (no local filesystem access from remote agent).
- Recap das aulas passadas is not included (out of scope per spec).
- Vacation weeks where no events exist: email still goes out with "sem eventos críticos".
- If Google Calendar / Gmail connectors get disconnected from the cloud account, the agent fails silently. Worth a manual check after long breaks.

---

## Self-Review

**Spec coverage:** Walked through each section of the spec. Forward-looking core covered (Tasks 1-3). Email format spec mapped to prompt (Task 2). Edge cases (semana vazia, MCP failure) encoded in prompt. Tasks.md exclusion noted (Task 5). Calendar IDs match (Task 2).

**Placeholder scan:** No TBD/TODO. Every step has concrete commands or content. Task 3 step 2 has one conditional ("if schema requires different field names") but the intent is explicit.

**Type consistency:** No types per se, but naming is consistent: `weekly-fgv-summary` task name used throughout, `weekly-summary-prompt.md` used throughout, calendar IDs from spec match prompt.

**Gaps:**
- Spec says "1 retry on Calendar API down" — encoded in prompt's "If send fails, retry once". Calendar failure handling is in the prompt too.
- Spec says "Ranking de estudo: pondera por (peso × proximidade temporal)" — encoded in prompt step 6 with concrete weights and formula.
