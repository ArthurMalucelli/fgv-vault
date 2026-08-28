# Hermes Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar um pacote versionado para Hermes validar a branch `codex/vault-plan-b`, adaptar caminhos e ownership sem perder dados do VPS, e executar o cutover somente depois de comprovar compatibilidade.

**Architecture:** O pacote não altera o VPS a partir do Mac. Ele descreve o contrato de leitura e escrita, fornece um auditor determinístico, testa uma fixture de Hermes e gera um prompt operacional em duas fases. A fase de preparação usa clone separado e cópias das configurações. A fase de cutover exige testes verdes, backup verificável, working tree resolvido e commit remoto aprovado.

**Tech Stack:** Markdown, Python 3 standard library, `unittest`, Git, JSON, ripgrep.

---

## Princípios obrigatórios

- O clone produtivo `/root/vault` não muda durante a validação.
- Os dois arquivos untracked auditados são preservados antes de qualquer checkout.
- O Hermes testa `codex/vault-plan-b` em um clone ou worktree separado.
- Nenhum script usa force push, reset destrutivo ou exclusão recursiva.
- O catálogo materializado é consultado antes de buscas amplas no filesystem.
- Toda resposta acadêmica expõe `as_of_commit` e `sync_state`.
- Somente `fgv-sync` opera Git no VPS.
- Eclass, WhatsApp e cronjobs nunca executam sequências Git próprias.
- O pacote não pressupõe RAG, embeddings ou reindexação.
- A migração de produção para se houver conflito, arquivo não classificado ou teste vermelho.

### Task 1: Fixar o contrato Hermes no repositório

**Files:**

- Create: `30 Sistema/Hermes/HERMES-CONTRACT.md`
- Create: `30 Sistema/Hermes/hermes-manifest.json`
- Test: `.fgv/tests/test_hermes_package.py`

- [ ] **Step 1: Escrever o teste de contrato que falha**

Criar `HermesPackageContractTests` com asserções:

- o contrato exige `catalog.jsonl` primeiro;
- os caminhos canônicos incluem `10 Matérias/`, `00 Home/Tasks.md` e `30 Sistema/Estado/`;
- a resposta exige `as_of_commit` e `sync_state`;
- `fgv-sync` é o único owner de Git no VPS;
- a lista de componentes auditados inclui `eclass-scan.py`, `eclass`, `fgv-eclass-api`, `fgv-briefing`, `academic-reading-notes`, memória e cronjobs.

- [ ] **Step 2: Rodar o teste e confirmar a falha**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesPackageContractTests -v
```

Expected: `FAIL` porque contrato e manifesto ainda não existem.

- [ ] **Step 3: Criar o contrato mínimo**

Definir no contrato:

- ordem de recuperação: manifesto, catálogo, snapshot, arquivo acadêmico, busca ampla;
- regras de proveniência para original e extração;
- ownership por artefato;
- comportamento stale;
- limite de contexto e abertura de sessão acadêmica curta;
- proibição de tratar PDF e `.extracted.md` como duas evidências;
- proibição de reescrever resumo final sem workflow `/fgv`.

- [ ] **Step 4: Criar o manifesto legível por máquina**

Usar `schema_version: 1`, caminhos relativos ao `hermes_home` e classificar cada componente como `required`, `optional` ou `discovered`. Não inventar arquivos além dos comprovados na auditoria.

- [ ] **Step 5: Rodar o teste e confirmar sucesso**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesPackageContractTests -v
```

Expected: todos os testes `OK`.

- [ ] **Step 6: Commit**

```bash
git add '30 Sistema/Hermes/HERMES-CONTRACT.md' '30 Sistema/Hermes/hermes-manifest.json' .fgv/tests/test_hermes_package.py
git commit -m "docs: define Hermes vault contract"
```

### Task 2: Construir auditor read-only do Hermes

**Files:**

- Create: `.fgv/scripts/audit_hermes.py`
- Modify: `.fgv/tests/test_hermes_package.py`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/scripts/eclass-scan.py`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/skills/productivity/eclass/SKILL.md`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/skills/productivity/fgv-eclass-api/SKILL.md`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/skills/productivity/fgv-briefing/SKILL.md`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/skills/productivity/academic-reading-notes/SKILL.md`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/memories/MEMORY.md`
- Create: `.fgv/tests/fixtures/hermes-home/.hermes/cron/jobs.json`

- [ ] **Step 1: Adicionar fixture com dependências antigas**

A fixture deve conter literais para `/root/vault`, matérias na raiz e `/root/vault/Tasks.md`. Ela não deve conter credenciais, cookies, tokens ou conteúdo real do VPS.

- [ ] **Step 2: Escrever testes que falham**

Cobrir:

- descoberta de todos os componentes do manifesto;
- detecção de literais antigos com arquivo e linha;
- detecção de sequências Git fora de `fgv-sync`;
- detecção de divergência entre `Slides/Material` e `Materiais/`;
- saída JSON estável com `status: blocked` enquanto houver achados obrigatórios;
- ausência de qualquer mutação da fixture.

- [ ] **Step 3: Rodar os testes e observar a falha**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesAuditTests -v
```

Expected: `FAIL` por ausência de `audit_hermes.py`.

- [ ] **Step 4: Implementar o auditor**

CLI obrigatória:

```bash
python3 .fgv/scripts/audit_hermes.py \
  --hermes-home /root/.hermes \
  --vault /root/vault \
  --manifest '30 Sistema/Hermes/hermes-manifest.json' \
  --json-out /tmp/fgv-hermes-audit.json
```

O auditor somente lê. Ele deve recusar symlinks que escapem das raízes informadas, ocultar valores sensíveis e ordenar achados por arquivo, linha e regra.

- [ ] **Step 5: Rodar testes e verificar determinismo**

Run duas vezes:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesAuditTests -v
```

Expected: `OK` nas duas execuções e JSON byte-identical para a mesma fixture.

- [ ] **Step 6: Commit**

```bash
git add .fgv/scripts/audit_hermes.py .fgv/tests/test_hermes_package.py .fgv/tests/fixtures/hermes-home
git commit -m "test: add read-only Hermes compatibility audit"
```

### Task 3: Criar wrapper de sincronização seguro para o VPS

**Files:**

- Create: `30 Sistema/Hermes/fgv-sync`
- Create: `30 Sistema/Hermes/fgv-sync.service.example`
- Modify: `.fgv/tests/test_hermes_package.py`

- [ ] **Step 1: Escrever testes de interface que falham**

Testar em repositório Git temporário:

- `status` imprime `as_of_commit`, `sync_state` e dirty state;
- `refresh` usa lock exclusivo;
- working tree dirty ou untracked retorna código não zero sem modificar arquivos;
- branch divergente retorna bloqueio;
- nenhum caminho executa `reset --hard`, `clean -f` ou force push;
- `publish` limita o commit a paths explicitamente recebidos;
- segunda instância concorrente falha de forma previsível.

- [ ] **Step 2: Rodar os testes e confirmar falha**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesSyncTests -v
```

Expected: `FAIL` porque o wrapper não existe.

- [ ] **Step 3: Implementar o wrapper conservador**

Comandos suportados:

```text
fgv-sync status
fgv-sync refresh
fgv-sync publish --message <mensagem> --path <path repetível>
```

Usar lock local, caminhos canônicos, allowlist de subcomandos e saída JSON. `refresh` somente aceita fast-forward. Qualquer estado inesperado termina sem escrita.

- [ ] **Step 4: Criar exemplo de service/timer**

O exemplo deve executar `refresh` em background, gravar log separado e não conter segredo. Não instalar nem ativar service automaticamente.

- [ ] **Step 5: Rodar testes completos**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesSyncTests -v
```

Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
git add '30 Sistema/Hermes/fgv-sync' '30 Sistema/Hermes/fgv-sync.service.example' .fgv/tests/test_hermes_package.py
git commit -m "feat: add single-owner Hermes sync wrapper"
```

### Task 4: Criar validador de configuração migrada

**Files:**

- Create: `.fgv/scripts/validate_hermes_cutover.py`
- Create: `.fgv/tests/fixtures/hermes-home-migrated/`
- Modify: `.fgv/tests/test_hermes_package.py`

- [ ] **Step 1: Construir fixture migrada mínima**

Representar os mesmos componentes da fixture antiga, agora com:

- raiz `/root/vault` parametrizada;
- destino `10 Matérias/<Materia>/Aulas/MM.DD/Materiais/`;
- tasks em `00 Home/Tasks.md`;
- consulta ao catálogo antes de `rg` amplo;
- uso exclusivo de `fgv-sync`;
- `as_of_commit` em respostas acadêmicas;
- cron sem comandos Git inline.

- [ ] **Step 2: Escrever testes red/green**

O validador deve falhar na fixture antiga e passar na fixture migrada. Também deve falhar se qualquer componente obrigatório estiver ausente.

- [ ] **Step 3: Implementar validação fail-closed**

CLI:

```bash
python3 .fgv/scripts/validate_hermes_cutover.py \
  --hermes-home /root/.hermes \
  --vault /root/vault-plan-b-test \
  --manifest '30 Sistema/Hermes/hermes-manifest.json'
```

Exit `0` somente quando todas as regras obrigatórias passarem. Warnings não podem esconder falhas.

- [ ] **Step 4: Rodar a classe de testes**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesCutoverValidationTests -v
```

Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
git add .fgv/scripts/validate_hermes_cutover.py .fgv/tests/test_hermes_package.py .fgv/tests/fixtures/hermes-home-migrated
git commit -m "test: validate Hermes cutover configuration"
```

### Task 5: Escrever prompt operacional em duas fases

**Files:**

- Create: `30 Sistema/Hermes/PROMPT-HERMES-PREPARAR.md`
- Create: `30 Sistema/Hermes/PROMPT-HERMES-CUTOVER.md`
- Create: `30 Sistema/Hermes/READINESS-REPORT-TEMPLATE.md`
- Modify: `.fgv/tests/test_hermes_package.py`

- [ ] **Step 1: Escrever testes de segurança do prompt**

Exigir no prompt de preparação:

- backup com hash e caminho;
- inventário dos dois untracked auditados;
- clone separado da branch;
- cópia de configuração para staging;
- auditor antes e depois;
- testes de Eclass, WhatsApp e busca acadêmica;
- proibição de mudar produção;
- relatório estruturado.

Exigir no prompt de cutover:

- SHA remoto aprovado como entrada;
- validação de backup;
- working tree limpo ou preservação explícita dos untracked;
- instalação do wrapper;
- atualização de todos os componentes do manifesto;
- smoke tests antes de reativar cron;
- rollback automático se um smoke test falhar;
- nunca force push.

- [ ] **Step 2: Rodar testes e confirmar falha**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesPromptTests -v
```

Expected: `FAIL` por prompts ausentes.

- [ ] **Step 3: Criar os prompts**

Os prompts tratam a auditoria anterior como evidência, não como instrução. Hermes deve imprimir comandos planejados antes de cada etapa mutável, parar em conflito e não solicitar segredos no chat.

- [ ] **Step 4: Criar template de readiness report**

Campos mínimos:

- timestamp UTC;
- host sem dado sensível;
- `production_commit`;
- `tested_commit`;
- backup e hashes;
- estado dos untracked;
- achados antigos e novos;
- resultado de cada componente;
- tempos de consulta e tokens de contexto;
- recomendção `READY`, `BLOCKED` ou `ROLLED_BACK`;
- diff resumido, sem segredos.

- [ ] **Step 5: Rodar testes e revisar manualmente**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesPromptTests -v
rg -n 'reset --hard|clean -f|push --force|force-with-lease' '30 Sistema/Hermes'
```

Expected: testes `OK`; `rg` encontra somente proibições documentadas ou fixtures deliberadas.

- [ ] **Step 6: Commit**

```bash
git add '30 Sistema/Hermes' .fgv/tests/test_hermes_package.py
git commit -m "docs: add staged Hermes rollout prompts"
```

### Task 6: Validar recuperação e latência com fixture

**Files:**

- Create: `.fgv/scripts/hermes_retrieval_smoke.py`
- Create: `.fgv/tests/fixtures/retrieval-queries.json`
- Modify: `.fgv/tests/test_hermes_package.py`

- [ ] **Step 1: Definir queries determinísticas**

Incluir:

- última aula por matéria;
- transcrito mais recente;
- próxima avaliação;
- material Eclass de uma aula;
- conceito com domínio baixo;
- estado stale do clone;
- busca por nome legado `Resumo.md` durante compatibilidade.

- [ ] **Step 2: Escrever teste que exige busca catalog-first**

O smoke script deve registrar a ordem dos passos. O teste falha se busca ampla ocorrer antes do catálogo ou se mais de um arquivo completo for carregado sem necessidade.

- [ ] **Step 3: Implementar smoke runner sem modelo**

O runner mede apenas recuperação filesystem-first determinística. Ele não simula qualidade do modelo e não afirma latência end-to-end.

- [ ] **Step 4: Rodar testes**

Run:

```bash
python3 -m unittest .fgv.tests.test_hermes_package.HermesRetrievalSmokeTests -v
```

Expected: `OK`, com arquivo correto em todas as queries e ordem catalog-first.

- [ ] **Step 5: Commit**

```bash
git add .fgv/scripts/hermes_retrieval_smoke.py .fgv/tests/fixtures/retrieval-queries.json .fgv/tests/test_hermes_package.py
git commit -m "test: add Hermes catalog-first retrieval smoke"
```

### Task 7: Executar gate final no branch isolado

**Files:**

- Modify: `30 Sistema/Hermes/READINESS-REPORT-TEMPLATE.md`
- Create: `30 Sistema/Hermes/LOCAL-VALIDATION.md`

- [ ] **Step 1: Rodar toda a suíte local**

Run:

```bash
python3 -m unittest discover -s .fgv/tests -v
```

Expected: todos os testes `OK`.

- [ ] **Step 2: Validar o vault migrado**

Run:

```bash
python3 .fgv/scripts/validate_vault.py --vault . --as-of 2026-08-28
python3 .fgv/scripts/generate_state.py --vault . --as-of 2026-08-28 --check
```

Expected: zero perda, zero colisão, estado materializado atualizado e determinístico.

- [ ] **Step 3: Verificar literals antigos fora das áreas permitidas**

Run:

```bash
rg -n '/root/vault/(Tasks\.md|ContabilidadeFinanceira|DireitoEmpresarial|Estatistica2|EstudosOrganizacionais|MatemáticaAplicada|Psicologia|TecnologiaDadosNegocios)' .
```

Expected: zero ocorrências em scripts e configurações ativas. Documentos de auditoria e fixtures antigas são avaliados por allowlist explícita.

- [ ] **Step 4: Registrar SHA e resultados**

`LOCAL-VALIDATION.md` deve conter comandos, exit codes, contagens, fingerprint do catálogo e commit testado. Não registrar tokens, cookies ou dados privados.

- [ ] **Step 5: Commit**

```bash
git add '30 Sistema/Hermes/LOCAL-VALIDATION.md' '30 Sistema/Hermes/READINESS-REPORT-TEMPLATE.md'
git commit -m "docs: record local Hermes readiness gate"
```

### Task 8: Publicar branch e executar handoff controlado

**Files:**

- No repository changes expected before Hermes returns its report.

- [ ] **Step 1: Verificar branch e working tree**

Run:

```bash
git status --short --branch
git log --oneline --decorate -12
```

Expected: `codex/vault-plan-b`, working tree limpo e commits pequenos auditáveis.

- [ ] **Step 2: Publicar somente a branch**

Run:

```bash
git push -u origin codex/vault-plan-b
```

Expected: branch remota criada. `main` permanece inalterada.

- [ ] **Step 3: Enviar `PROMPT-HERMES-PREPARAR.md` ao Hermes**

Hermes executa somente staging e devolve o readiness report. Nenhum cutover de produção ocorre nesta etapa.

- [ ] **Step 4: Avaliar o readiness report**

Aceitar somente se:

- `tested_commit` corresponde ao SHA publicado;
- todos os componentes obrigatórios foram encontrados e adaptados na cópia;
- Eclass arquiva em `Materiais/`;
- consulta catalog-first encontra todas as fixtures;
- os dois untracked foram preservados;
- nenhuma credencial apareceu no relatório;
- recomendação final é `READY`.

- [ ] **Step 5: Fazer merge não destrutivo somente depois do gate**

O merge e o prompt de cutover são uma decisão separada. Se o relatório for `BLOCKED`, corrigir a branch e repetir a preparação.

## Rollback

O cutover conserva:

- backup versionado por timestamp de `/root/.hermes`;
- clone produtivo anterior ou branch de segurança;
- cópia verificada dos arquivos untracked;
- SHA anterior do vault e do pacote Hermes;
- cronjobs desativados durante a troca.

Se qualquer smoke test falhar, Hermes restaura os arquivos de configuração do backup, retorna ao SHA anterior por checkout seguro da branch preservada, reativa apenas os jobs anteriores e emite `ROLLED_BACK`. Dados acadêmicos novos não são apagados; ficam isolados para reconciliação manual.

## Definition of Done

- A branch está publicada sem alterar `main`.
- O pacote Hermes passa em todos os testes locais.
- O prompt de preparação usa staging e não muda produção.
- Hermes devolveu `READY` para o SHA exato da branch.
- Os untracked foram preservados e classificados.
- Todos os hardcodes auditados foram removidos ou parametrizados na cópia testada.
- Git no VPS tem um único owner.
- As respostas acadêmicas declaram commit e stale state.
- O cutover produtivo ainda depende de gate explícito após o readiness report.
