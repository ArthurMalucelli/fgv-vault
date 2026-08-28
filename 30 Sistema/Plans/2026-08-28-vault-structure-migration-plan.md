# FGV Vault Structure Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar, somente na branch isolada, todos os 1.059 arquivos legados do vault FGV para a arquitetura `00 Home`, `10 Matérias`, `20 Conhecimento`, `30 Sistema` e `90 Arquivo`, sem perda, colisão ou aumento de links quebrados.

**Architecture:** Um planner Python standard-library classifica cada path legado em um manifesto determinístico. A aplicação ocorre em três commits auditáveis: moves byte-identical, rewrites de paths e configurações, depois renomes e metadata. Cada fase tem preflight, contagem, hashes e receipt. O vault vivo `~/FGV` permanece intacto.

**Tech Stack:** Python 3.11+ standard library, `unittest`, JSON, JSONL, Markdown, Obsidian configuration JSON, Git.

---

## Escopo travado

- Fonte de execução: worktree `codex/vault-plan-b`.
- Fonte de classificação: inventário auditado no commit-base da branch.
- Total legado esperado: 1.059 arquivos.
- Destinos únicos esperados: 1.059.
- Colisões esperadas: zero.
- Itens sem regra esperados: zero.
- Nenhum arquivo legado é apagado sem existir um destino verificado com o mesmo hash quando a fase exigir bytes idênticos.
- Arquivos novos de `.fgv/`, planos, relatórios e estado gerado não entram na contagem dos 1.059 legados.
- O histórico Git não é reescrito.
- Não há merge em `main` nesta execução.
- Não há instalação das skills live nem alteração do VPS.
- Paths são normalizados em Unicode NFC e emitidos com `/`.
- Nomes dentro de `90 Arquivo/2026.1` não são modernizados nesta fase.

## Mapa canônico auditado

| Origem | Destino | Arquivos esperados |
|---|---|---:|
| Home, Tasks e triagem legada | `00 Home/` | 7 |
| Sete matérias ativas | `10 Matérias/` | 221 |
| `Vault/Conceitos/**` | `20 Conhecimento/Conceitos/` | 505 |
| Specs, Templates, Tutor e automation | `30 Sistema/` | 13 |
| `Vault/S1/**` | `90 Arquivo/2026.1/` | 313 |
| Total | | 1.059 |

Mapeamentos especiais:

- `Vault/Index.md` para `00 Home/Home.md`.
- `Tasks.md` para `00 Home/Tasks.md`.
- `Vault/Controle de Faltas 2026.2.md` para `00 Home/Controle de Faltas 2026.2.md`.
- `Macro.md` para `00 Home/Inbox/Legado/Macro.md`.
- `Projeto 90 Dias.md` para `00 Home/Inbox/Legado/Projeto 90 Dias.md`.
- `Vault/FGV Finance/Prova - Tópicos cobrados.md` para `00 Home/Inbox/Legado/Prova - Tópicos cobrados.md`.
- `Vault/Conceitos/Sem título.md` para `00 Home/Inbox/Legado/Sem título.md`.
- `Vault/Specs/**` para `30 Sistema/Specs/**`.
- `Vault/Templates/**` para `30 Sistema/Templates/**`.
- `Vault/Tutor/**` para `30 Sistema/Tutor/**`.
- `Vault/automation/**` para `30 Sistema/Automacoes/**`.
- `Vault/S1/**` para `90 Arquivo/2026.1/**`.
- Cada matéria ativa na raiz para `10 Matérias/<pasta atual>/**`.

## Baseline de links

- Wikilinks totais: 5.402.
- Destinos não resolvidos: 408.
- Destinos ambíguos: 3.
- Aproximadamente 161 casos possuem match por normalização de acentos e devem ser reportados separadamente.
- A migração não pode aumentar unresolved ou ambiguous.
- Três links curtos em `MatemáticaAplicada/Aulas/08.06/` precisam acompanhar os renomes: dois `[[Resumo]]` e um `[[Transcrito]]`.

### Task 1: Criar inventário e planner determinístico

**Files:**

- Create: `.fgv/scripts/fgv_migration/__init__.py`
- Create: `.fgv/scripts/fgv_migration/inventory.py`
- Create: `.fgv/scripts/fgv_migration/rules.py`
- Create: `.fgv/scripts/plan_migration.py`
- Create: `.fgv/tests/test_migration_inventory.py`
- Create: `.fgv/tests/fixtures/migration-mini-vault/`

- [ ] **Step 1: Escrever testes que falham**

Cobrir com fixture realista:

- inventário ignora `.git`, `.obsidian`, `.fgv` e arquivos gerados;
- hash SHA-256 é calculado sobre bytes;
- paths são NFC e relativos;
- symlink é recusado;
- cada uma das categorias do mapa tem destino correto;
- item desconhecido vai para Inbox somente quando uma regra allowlist autoriza triagem;
- colisão exata e colisão após NFC bloqueiam o plano;
- ordenação do manifesto é estável.

- [ ] **Step 2: Rodar RED**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest .fgv.tests.test_migration_inventory -v
```

Expected: `FAIL` por módulos ausentes.

- [ ] **Step 3: Implementar o planner mínimo**

Cada registro do manifesto deve conter:

```json
{
  "schema_version": 1,
  "source": "Tasks.md",
  "destination": "00 Home/Tasks.md",
  "sha256": "<64 hex>",
  "size_bytes": 123,
  "category": "home",
  "phase": "structural",
  "reason": "canonical task file"
}
```

CLI:

```bash
python3 .fgv/scripts/plan_migration.py \
  --vault . \
  --base-ref origin/main \
  --output '30 Sistema/Estado/migration-manifest.json' \
  --check-only
```

O planner não escreve fora do arquivo `--output` e, em `--check-only`, não escreve nada.

- [ ] **Step 4: Rodar GREEN**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest .fgv.tests.test_migration_inventory -v
```

Expected: todos os testes `OK`.

- [ ] **Step 5: Commit**

```bash
git add .fgv/scripts/fgv_migration .fgv/scripts/plan_migration.py .fgv/tests/test_migration_inventory.py .fgv/tests/fixtures/migration-mini-vault
git commit -m "feat: add deterministic vault migration planner"
```

### Task 2: Provar o mapa completo do vault real

**Files:**

- Create: `30 Sistema/Estado/migration-manifest.json`
- Create: `30 Sistema/Estado/migration-baseline.json`
- Modify: `.fgv/tests/test_migration_inventory.py`

- [ ] **Step 1: Escrever teste de contrato do inventário real**

O teste recebe um manifest fixture e exige:

- 1.059 registros;
- 1.059 sources;
- 1.059 destinations;
- zero colisões;
- zero unclassified;
- contagens 7, 221, 505, 13 e 313;
- nenhum destination absoluto;
- nenhuma travessia `..`;
- todo source existe no commit-base;
- todo hash confere.

- [ ] **Step 2: Rodar RED com manifesto ausente**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest \
  .fgv.tests.test_migration_inventory.RealManifestContractTests -v
```

Expected: `FAIL` por manifesto ausente.

- [ ] **Step 3: Gerar o manifesto real sem mover arquivos**

Run:

```bash
python3 .fgv/scripts/plan_migration.py \
  --vault . \
  --base-ref origin/main \
  --output '30 Sistema/Estado/migration-manifest.json'
```

Expected:

```text
legacy_files=1059
unique_destinations=1059
collisions=0
unclassified=0
files_moved=0
```

- [ ] **Step 4: Registrar baseline de integridade**

`migration-baseline.json` inclui commit-base, contagens por categoria, hash do manifesto, baseline de links, contagem de binários e hash agregado ordenado. Não inclui paths absolutos, hostname ou mtime.

- [ ] **Step 5: Rodar GREEN e repetir para determinismo**

Gerar o manifesto duas vezes em diretórios temporários e comparar bytes.

Expected: testes `OK` e manifests idênticos.

- [ ] **Step 6: Commit**

```bash
git add '30 Sistema/Estado/migration-manifest.json' '30 Sistema/Estado/migration-baseline.json' .fgv/tests/test_migration_inventory.py
git commit -m "docs: record audited vault migration manifest"
```

### Task 3: Aplicar somente os moves byte-identical

**Files:**

- Create: `.fgv/scripts/apply_migration.py`
- Create: `.fgv/tests/test_migration_apply.py`
- Move: exactly the 1.059 legacy files listed in the manifest

- [ ] **Step 1: Escrever testes de aplicação e rollback**

Testar em cópia temporária:

- `--phase structural --dry-run` não muda bytes nem paths;
- HEAD diferente do baseline bloqueia;
- source faltando bloqueia antes do primeiro move;
- destination existente bloqueia antes do primeiro move;
- hash source divergente bloqueia antes do primeiro move;
- falha no meio restaura todos os paths anteriores;
- aplicação completa preserva cada hash e contagem;
- segunda aplicação retorna no-op verificável.

- [ ] **Step 2: Rodar RED**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest .fgv.tests.test_migration_apply -v
```

Expected: `FAIL` por applicator ausente.

- [ ] **Step 3: Implementar applicator transacional**

O script faz preflight integral, cria directories, aplica renames no mesmo filesystem, verifica destino e registra receipt. Em erro, executa o journal inverso. Ele não recebe globs e não infere paths fora do manifesto.

CLI:

```bash
python3 .fgv/scripts/apply_migration.py \
  --vault . \
  --manifest '30 Sistema/Estado/migration-manifest.json' \
  --phase structural \
  --expected-head <sha>
```

- [ ] **Step 4: Rodar GREEN em fixture**

Expected: todos os testes `OK`.

- [ ] **Step 5: Executar dry-run real**

Expected:

```text
planned_moves=1059
preflight=ok
files_written=0
```

- [ ] **Step 6: Aplicar no worktree isolado**

Antes de aplicar, confirmar branch e path. Depois, verificar:

```bash
git diff --summary
git diff --numstat
```

Expected: Git detecta moves; nenhum arquivo movido aparece com mudança de bytes.

- [ ] **Step 7: Rodar gate de integridade estrutural**

Expected:

- 1.059 destinos presentes;
- zero sources ainda presentes;
- hashes iguais aos do manifest;
- binários byte-identical;
- contagem legada preservada;
- nenhum arquivo fora do manifest movido.

- [ ] **Step 8: Commit estrutural isolado**

```bash
git add -A
git commit -m "refactor: move vault into Plan B structure"
```

Inspecionar o staging antes do commit. O commit não pode conter rewrites de conteúdo, renomes temáticos ou mudanças `.obsidian`.

### Task 4: Reescrever paths e configurações

**Files:**

- Create: `.fgv/scripts/rewrite_paths.py`
- Create: `.fgv/tests/test_path_rewrites.py`
- Modify: ten Markdown/config files with 64 audited old path literals
- Modify: `.obsidian/app.json`
- Modify: `.obsidian/templates.json`
- Modify: `.obsidian/graph.json`
- Modify: `.obsidian/core-plugins.json`
- Modify: `.obsidian/daily-notes.json`

- [ ] **Step 1: Escrever testes de rewrite**

Cobrir:

- somente literais mapeados mudam;
- wikilinks por basename permanecem quando ainda resolvem;
- links com path usam o novo path;
- links externos e URLs não mudam;
- bloco de código não recebe rewrite acidental;
- paths com espaços e acentos são tratados em NFC;
- segunda execução é no-op;
- configs continuam JSON válido.

- [ ] **Step 2: Rodar RED**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest .fgv.tests.test_path_rewrites -v
```

Expected: `FAIL` por rewriter ausente.

- [ ] **Step 3: Implementar allowlist de rewrites**

Config final:

- attachments: `30 Sistema/Anexos`;
- templates: `30 Sistema/Templates`;
- graph concept group: `path:20 Conhecimento/Conceitos`;
- daily notes core plugin: `false`;
- daily notes folder: `00 Home/Daily`;
- daily notes template: `30 Sistema/Templates/Daily.md` somente se o template existir, caso contrário campo vazio;
- `alwaysUpdateLinks`: `true` permanece.

- [ ] **Step 4: Rodar GREEN**

Expected: testes `OK`.

- [ ] **Step 5: Aplicar rewrites reais**

Run:

```bash
python3 .fgv/scripts/rewrite_paths.py \
  --vault . \
  --manifest '30 Sistema/Estado/migration-manifest.json'
```

Expected: exatamente os literals auditados ou um relatório de divergência que bloqueia o commit.

- [ ] **Step 6: Validar links**

Expected:

- unresolved menor ou igual a 408;
- ambiguous menor ou igual a 3;
- zero links absolutos antigos em arquivos ativos;
- matches por normalização de acento registrados.

- [ ] **Step 7: Commit de rewrites isolado**

```bash
git add .obsidian '00 Home' '10 Matérias' '20 Conhecimento' '30 Sistema' '90 Arquivo' .fgv/scripts/rewrite_paths.py .fgv/tests/test_path_rewrites.py
git commit -m "refactor: update vault paths and Obsidian config"
```

### Task 5: Renomear somente notas genéricas ativas

**Files:**

- Create: `.fgv/scripts/rename_lesson_notes.py`
- Create: `.fgv/tests/test_lesson_renames.py`
- Rename: 21 active `Resumo.md`
- Rename: 21 active `Transcrito.md`
- Modify: the three short links under `10 Matérias/MatemáticaAplicada/Aulas/08.06/`

- [ ] **Step 1: Escrever testes de naming**

Exigir:

- `tema` YAML preenchido é a única fonte do sufixo;
- `Resumo.md` vira `Resumo - <tema>.md`;
- `Transcrito.md` vira `Transcrito - <tema>.md`;
- data não aparece no filename;
- caracteres proibidos são normalizados sem perder o tema;
- path com mesmo destino bloqueia;
- notas no arquivo histórico não mudam;
- reexecução é no-op;
- links curtos da mesma aula são reescritos para o basename novo.

- [ ] **Step 2: Rodar RED**

Expected: `FAIL` por renamer ausente.

- [ ] **Step 3: Implementar o renamer por plano**

Primeiro emitir JSON com 42 operações e zero colisões. Depois aplicar somente quando `--apply` e `--expected-head` estiverem presentes.

- [ ] **Step 4: Dry-run real**

Expected:

```text
active_generic_notes=42
rename_operations=42
missing_tema=0
collisions=0
archive_operations=0
```

- [ ] **Step 5: Aplicar e validar**

Expected:

- zero `Resumo.md` ou `Transcrito.md` genéricos sob `10 Matérias`;
- 42 novos basenames temáticos;
- datas continuam apenas em pasta e YAML;
- três links de Matemática Aplicada resolvem;
- contagens e hashes dos corpos permanecem, exceto links/metadata explicitamente autorizados.

- [ ] **Step 6: Padronizar somente metadata ativa autorizada**

Adicionar ou normalizar de forma idempotente:

- `materias` como lista de slugs;
- `semestre: 2026.2`;
- `data` ISO consistente com pasta e contexto;
- `tipo`, `tema`, `status`;
- `contract_version: 1` quando a proveniência permitir;
- nunca inventar `source_sha256` para nota legada sem raw comprovado.

- [ ] **Step 7: Commit de naming e metadata isolado**

```bash
git add '10 Matérias' .fgv/scripts/rename_lesson_notes.py .fgv/tests/test_lesson_renames.py
git commit -m "refactor: give active class notes descriptive names"
```

### Task 6: Criar shells humanos da nova estrutura

**Files:**

- Create: `00 Home/Revisões.md`
- Create: `00 Home/Inbox/README.md`
- Create: seven `10 Matérias/<Materia>/Disciplina.md`
- Create: `30 Sistema/Estado/README.md`
- Create: `.fgv/tests/test_structure_contract.py`

- [ ] **Step 1: Escrever teste do contrato visual**

Exigir top-level visível exatamente ordenável como:

```text
00 Home
10 Matérias
20 Conhecimento
30 Sistema
90 Arquivo
```

Diretórios ocultos e `.obsidian` não entram na lista visual. Cada matéria ativa tem `Disciplina.md` e preserva `Aulas/`.

- [ ] **Step 2: Rodar RED**

Expected: falha pelos shells ausentes.

- [ ] **Step 3: Criar shells mínimos e humanos**

`Disciplina.md` contém frontmatter canônico, links para aulas, avaliações, treinos e erros, e um embed do estado gerado da matéria quando disponível. Não duplicar conteúdo acadêmico.

`00 Home/Revisões.md` explica a escala de domínio 0 a 3 e aponta para o snapshot. Inbox documenta triagem e proíbe abandono silencioso de arquivos.

- [ ] **Step 4: Rodar GREEN**

Expected: testes `OK`.

- [ ] **Step 5: Commit**

```bash
git add '00 Home/Revisões.md' '00 Home/Inbox/README.md' '10 Matérias' '30 Sistema/Estado/README.md' .fgv/tests/test_structure_contract.py
git commit -m "feat: add Plan B navigation shells"
```

### Task 7: Executar gate final e produzir receipt de rollback

**Files:**

- Create: `.fgv/scripts/validate_vault.py`
- Create: `30 Sistema/Estado/migration-receipt.json`
- Create: `30 Sistema/Estado/migration-validation.md`
- Create: `.fgv/tests/test_vault_validation.py`

- [ ] **Step 1: Escrever testes do validador fail-closed**

Cobrir arquivo faltante, hash divergente, colisão NFC, link novo quebrado, metadata inválida, config JSON inválido, top-level inesperado e binário alterado.

- [ ] **Step 2: Implementar validação read-only**

CLI:

```bash
python3 .fgv/scripts/validate_vault.py \
  --vault . \
  --manifest '30 Sistema/Estado/migration-manifest.json' \
  --baseline '30 Sistema/Estado/migration-baseline.json' \
  --as-of 2026-08-28
```

Exit `0` apenas quando todos os gates obrigatórios passarem.

- [ ] **Step 3: Rodar suite completa**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -v
git diff --check
```

Expected: todos os testes `OK` e diff limpo.

- [ ] **Step 4: Validar contagem e Git**

Expected:

- todos os 1.059 sources mapeados para destinos;
- zero perda;
- zero colisão;
- zero binário divergente;
- zero path antigo em automação ativa;
- links não pioraram;
- somente branch isolada mudou;
- `main` e `~/FGV` permanecem no commit anterior.

- [ ] **Step 5: Criar receipt de rollback**

O receipt lista SHA anterior, SHA atual, hash do manifest, commits das três fases, contagens, gates e a inversão source/destination. Ele não executa rollback.

- [ ] **Step 6: Commit final da migração**

```bash
git add .fgv/scripts/validate_vault.py .fgv/tests/test_vault_validation.py '30 Sistema/Estado/migration-receipt.json' '30 Sistema/Estado/migration-validation.md'
git commit -m "test: certify Plan B vault migration"
```

## Critérios de aceite

- `00 Home` é a primeira pasta visível.
- Matérias ativas estão somente em `10 Matérias`.
- Todo conteúdo legado está no Git, sem perda.
- 42 notas ativas possuem nomes temáticos.
- Arquivo histórico preserva naming antigo.
- Obsidian usa templates e attachments novos.
- Daily Notes está desativado.
- Home, catálogo e snapshot possuem um owner claro.
- A migração pode ser revertida pelo receipt sem reescrever histórico.
- O vault vivo, as skills live, o VPS e `main` permanecem intocados.
