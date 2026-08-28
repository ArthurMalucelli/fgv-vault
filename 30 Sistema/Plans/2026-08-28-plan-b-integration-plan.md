# FGV Plan B Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrar migração, dashboard, workflow `/fgv` e pacote Hermes em uma implementação coerente, portátil e testada na branch isolada.

**Architecture:** Quatro planos de componente definem requisitos detalhados. Este plano resolve sobreposições, fixa ownership de arquivos e determina a ordem de execução. O core `.fgv/` usa Python standard-library e `unittest`; estado materializado, migração, adapters e Hermes compartilham o mesmo registry e contrato, sem dependências duplicadas.

**Tech Stack:** Python 3.11+ standard library, `unittest`, Markdown, JSON, JSONL, Git, Obsidian.

---

## Planos de componente

- `2026-08-28-vault-structure-migration-plan.md`: classificação, moves, rewrites, renomes e validação estrutural.
- `2026-08-28-dashboard-catalog-plan.md`: read model, catálogo, snapshot e Home.
- `2026-08-28-fgv-workflow-unification-plan.md`: raw, transação, templates, tasks, Calendar e adapters.
- `2026-08-28-hermes-rollout-plan.md`: auditoria, sync owner, prompts, staging e gates do VPS.

Quando houver conflito, este plano tem precedência. Os planos de componente continuam sendo a especificação detalhada do comportamento.

## Resoluções de conflito

- `.fgv/VERSION`, `.fgv/CORE.md` e `.fgv/config/subjects.json` têm um único owner: foundation do workflow.
- O dashboard consome a configuração existente e pode adicionar campos compatíveis, nunca criar um registry paralelo.
- Catálogo e snapshot têm um único owner: `.fgv/scripts/fgv_state/` e `.fgv/scripts/generate_state.py`.
- O módulo `fgv_workflow.catalog` proposto no plano de workflow não é implementado. O CLI delega ao gerador de estado.
- Migração tem um único owner: `.fgv/scripts/fgv_migration/` e CLIs associados.
- O módulo `fgv_workflow.migration` proposto no plano de workflow não é implementado.
- `validate_vault.py` é compartilhado e composto pelo subsistema de migração. O gerador expõe seu próprio `--check`.
- `test_catalog.py` pertence ao dashboard. Conformance do workflow usa `test_workflow_conformance.py`.
- `test_hermes_package.py` pertence ao builder do workflow. Gates de rollout usam `test_hermes_rollout.py`.
- `30 Sistema/Hermes/fgv-sync` é a distribuição executável; `fgv_workflow.sync` fornece política e API testável.
- Python third-party, venv e instalação editável do plano de workflow ficam substituídos por standard-library e `PYTHONPATH=.fgv/src:.fgv/scripts`.
- JSON Schema é validado por funções locais para o subconjunto do contrato. Não há download de dependência.
- Frontmatter usa parser YAML-subset conservador. Documento fora do subconjunto gera warning ou falha definida, nunca interpretação inventada.
- O folder de aula permanece `MM.DD`. Ano fica em YAML e identidade transacional.
- A implementação pode migrar a branch isolada, mas não o vault vivo nem `main`.

## Ownership de paths

| Path | Owner |
|---|---|
| `.fgv/CORE.md`, `VERSION`, `config`, `schemas` | workflow foundation |
| `.fgv/src/fgv_workflow/` | workflow `/fgv` |
| `.fgv/scripts/fgv_migration/` | structural migration |
| `.fgv/scripts/fgv_state/` | dashboard and catalog |
| `.fgv/scripts/audit_hermes.py`, Hermes validators | Hermes rollout |
| `.fgv/tests/test_migration_*` | structural migration |
| `.fgv/tests/test_state_*` and catalog/frontmatter/task tests | dashboard |
| `.fgv/tests/test_workflow_*` and ingest/concepts/calendar tests | workflow |
| `.fgv/tests/test_hermes_rollout.py` | Hermes rollout |
| `00 Home/Home.md` | human shell, dashboard embeds generated snapshot |
| `30 Sistema/Estado/catalog.jsonl` | state generator only |
| `30 Sistema/Estado/dashboard-snapshot.md` | state generator only |
| `30 Sistema/Hermes/` | Hermes package and operator docs |

### Task 1: Bootstrap canônico

**Files:**

- Create: `.fgv/VERSION`
- Create: `.fgv/CORE.md`
- Create: `.fgv/config/subjects.json`
- Create: `.fgv/config/sync-ownership.json`
- Create: `.fgv/src/fgv_workflow/__init__.py`
- Create: `.fgv/tests/test_workflow_contract.py`

- [ ] **Step 1: Escrever testes RED para versão, invariantes, sete matérias e ownership Git.**
- [ ] **Step 2: Rodar `PYTHONPATH=.fgv/src:.fgv/scripts python3 -m unittest .fgv.tests.test_workflow_contract -v` e confirmar falha por arquivos ausentes.**
- [ ] **Step 3: Implementar somente o contrato mínimo, sem pacote paralelo.**
- [ ] **Step 4: Rodar GREEN e scan de paths duplicados.**
- [ ] **Step 5: Revisão de spec, revisão de qualidade e commit `feat: add canonical FGV contract`.**

### Task 2: Ferramentas e migração estrutural

**Files:**

- Follow: `2026-08-28-vault-structure-migration-plan.md`, Tasks 1 through 4.

- [ ] **Step 1: Implementar planner e applicator por TDD.**
- [ ] **Step 2: Provar 1.059 sources, 1.059 destinations, zero colisão e zero unclassified.**
- [ ] **Step 3: Commitar ferramentas e manifest antes de mover conteúdo.**
- [ ] **Step 4: Aplicar moves byte-identical e commitar somente estrutura.**
- [ ] **Step 5: Aplicar rewrites allowlist e configurações Obsidian em commit separado.**
- [ ] **Step 6: Revisão de spec e qualidade após cada commit.**

### Task 3: Naming ativo e contrato visual

**Files:**

- Follow: `2026-08-28-vault-structure-migration-plan.md`, Tasks 5 through 7.

- [ ] **Step 1: Planejar 42 renomes com `tema`, zero colisão e zero alteração no arquivo histórico.**
- [ ] **Step 2: Rodar RED, implementar renamer, aplicar e rodar GREEN.**
- [ ] **Step 3: Corrigir os três links curtos de Matemática Aplicada.**
- [ ] **Step 4: Criar Revisões, Inbox README e sete Disciplina.md.**
- [ ] **Step 5: Validar top-level visível e commitar naming separado dos shells.**

### Task 4: Catálogo e dashboard

**Files:**

- Follow: `2026-08-28-dashboard-catalog-plan.md`, adaptado ao ownership deste plano.

- [ ] **Step 1: Usar registry existente e escrever testes RED do parser, tasks, catálogo e snapshot.**
- [ ] **Step 2: Implementar `fgv_state` sem dependências externas.**
- [ ] **Step 3: Provar determinismo, NFC, exclusões, atomicidade, fail-closed e write-if-changed.**
- [ ] **Step 4: Transformar Home movido em shell humano e incorporar snapshot estático.**
- [ ] **Step 5: Gerar estado real com `--as-of 2026-08-28` e rodar `--check`.**
- [ ] **Step 6: Revisão de spec, qualidade e commit por unidade coesa.**

### Task 5: Core `/fgv` e Plaud

**Files:**

- Create: `.fgv/src/fgv_workflow/models.py`
- Create: `.fgv/src/fgv_workflow/subjects.py`
- Create: `.fgv/src/fgv_workflow/naming.py`
- Create: `.fgv/src/fgv_workflow/source_store.py`
- Create: `.fgv/src/fgv_workflow/date_resolution.py`
- Create: `.fgv/src/fgv_workflow/plaud.py`
- Create: `.fgv/src/fgv_workflow/concepts.py`
- Create: `.fgv/src/fgv_workflow/tasks.py`
- Create: `.fgv/src/fgv_workflow/calendar.py`
- Create: `.fgv/templates/`
- Test: dedicated `test_workflow_*.py` files

- [ ] **Step 1: Implementar cada módulo em ciclo RED, GREEN, REFACTOR.**
- [ ] **Step 2: Provar raw byte-identical, source externo preservado e manifest idempotente.**
- [ ] **Step 3: Provar `transaction_id`, naming sem data e data por evidência.**
- [ ] **Step 4: Provar transcrito, resumo e revisão com metadata e links coerentes.**
- [ ] **Step 5: Provar conceitos gated, tasks deduplicadas e Calendar intents confirmáveis.**
- [ ] **Step 6: Revisar e commitar por capacidade, nunca como megacommit.**

### Task 6: Adapters Codex e Claude

**Files:**

- Create: `.fgv/adapters/codex/SKILL.md.tmpl`
- Create: `.fgv/adapters/claude/SKILL.md.tmpl`
- Create: `.fgv/scripts/stage_adapters.py`
- Create: `.fgv/evals/evals.json`
- Create: `.fgv/tests/test_workflow_adapters.py`

- [ ] **Step 1: Snapshotar semanticamente as skills antigas dentro da fixture de teste, sem copiar segredos.**
- [ ] **Step 2: Escrever testes RED de conformance e recusa de instalação live.**
- [ ] **Step 3: Criar adapters finos com o mesmo contrato e diferenças apenas de ferramentas.**
- [ ] **Step 4: Gerar bundles somente em `30 Sistema/Estado/adapter-staging/`.**
- [ ] **Step 5: Executar evals com skill e baseline antigo, grade objetiva e benchmark.**
- [ ] **Step 6: Gerar viewer estático com o script oficial de `skill-creator`.**
- [ ] **Step 7: Não instalar em `~/.agents` nem `~/.claude`; entregar installer de cutover separado.**

### Task 7: Pacote Hermes

**Files:**

- Follow: `2026-08-28-hermes-rollout-plan.md`.

- [ ] **Step 1: Criar contrato, manifest e auditor read-only por TDD.**
- [ ] **Step 2: Criar wrapper `fgv-sync` e validar lock, dirty tree, fast-forward e scoped publish.**
- [ ] **Step 3: Criar validator de cutover e fixtures antiga/migrada.**
- [ ] **Step 4: Criar prompts PREPARAR e CUTOVER, mais readiness template.**
- [ ] **Step 5: Criar smoke catalog-first e provar `as_of_commit`/stale.**
- [ ] **Step 6: Construir bundle pinado sem tocar `/root/.hermes`.**

### Task 8: Gate integrado e publicação da branch

**Files:**

- Create: `30 Sistema/Estado/migration-validation.md`
- Create: `30 Sistema/Hermes/LOCAL-VALIDATION.md`
- Create: `30 Sistema/Estado/adapter-staging/fgv-skill-review.html`

- [ ] **Step 1: Rodar todos os `unittest` sem skip ou warning.**
- [ ] **Step 2: Rodar gerador duas vezes e comparar bytes.**
- [ ] **Step 3: Rodar validador estrutural e provar zero perda.**
- [ ] **Step 4: Rodar conformance Codex/Claude/Hermes em fixture comum.**
- [ ] **Step 5: Executar revisão final independente do diff completo.**
- [ ] **Step 6: Confirmar que `~/FGV`, skills live, VPS e `main` estão intactos.**
- [ ] **Step 7: Publicar somente `codex/vault-plan-b`.**
- [ ] **Step 8: Entregar prompt PREPARAR do Hermes e manter cutover bloqueado até readiness `READY`.**

## Definition of Done desta execução

- Branch isolada contém o vault reorganizado e todos os arquivos legados.
- `00 Home` aparece primeiro e matérias estão em `10 Matérias`.
- Dashboard humano e snapshot Hermes derivam da mesma fonte.
- `/fgv` de Codex e Claude possuem contrato idêntico e bundles em staging.
- Raw Plaud é preservado e ingestão é idempotente.
- Hermes possui pacote, auditor, sync wrapper e prompts, sem cutover produtivo.
- Todos os testes e validadores passam.
- A branch remota existe; `main` não mudou.
