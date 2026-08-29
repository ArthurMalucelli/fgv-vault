# Contrato Hermes para o vault FGV

## Escopo

Este contrato vale para toda resposta acadêmica, captura do Eclass, briefing, memória e job agendado do Hermes. O contrato do vault é a fonte normativa. Prompts e memórias locais são adaptadores e não podem redefinir caminhos, nomes ou ownership.

## Recuperação catalog-first

Em cada pergunta acadêmica, o Hermes segue esta ordem fechada:

1. Executa `.fgv/scripts/hermes_catalog_query.py` para ler `30 Sistema/Estado/catalog.jsonl` fora do contexto do modelo e devolver apenas o manifesto e no máximo cinco candidatos.
2. Lê `30 Sistema/Estado/dashboard-snapshot.md` e valida o hash do catálogo informado no cabeçalho.
3. Seleciona um caminho exato do catálogo e abre um único arquivo exato, quando o corpo for necessário.

O JSON do query local tem uma linha, no máximo 16 KiB e no máximo cinco candidatos. O catálogo completo nunca é injetado no prompt, na memória ou no contexto do modelo. Skills acadêmicas, Eclass e WhatsApp usam o mesmo comando determinístico e não acessam `catalog.jsonl` diretamente. O comando pode percorrer o JSONL internamente, mas não varre o vault. Evidências de canal preservam o stdout bruto desse comando e seu SHA-256; o readiness repete a query no staging e exige igualdade byte a byte.

Uma busca ampla só é permitida como fallback declarado quando o catálogo não contém candidato. O fallback é limitado a `00 Home/`, `10 Matérias/`, `20 Conhecimento/` e `90 Arquivo/`. Nunca varre `.fgv/`, `30 Sistema/Plans/`, `30 Sistema/Specs/`, `.git/` ou `.obsidian/` como conteúdo acadêmico.

As buscas por aulas usam `Resumo*.md` e `Transcrito*.md` somente quando o arquivo é filho direto de `Aulas/MM.DD/`. Um basename igual dentro de `Material/` não é aula nem transcrito. Nunca assumem que o arquivo se chama apenas `Resumo.md` ou `Transcrito.md`.

## Proveniência e freshness

Toda resposta acadêmica termina com estes campos:

```text
as_of_commit: <SHA Git de 40 caracteres>
sync_state: clean | dirty | stale | unknown
```

`as_of_commit` não vem do catálogo. Ele é o `git rev-parse HEAD` do mesmo checkout, obtido por `fgv-sync status`. A data operacional vem de `America/Sao_Paulo`, nunca de UTC, e é passada explicitamente como `operational_as_of` aos gates. O catálogo e o snapshot precisam declarar exatamente essa data. O catálogo prova seu conteúdo com `source_fingerprint` e `build_fingerprint`. Antes de responder, o owner executa `generate_state.py --check` nesse checkout. Só a combinação de data atual, check verde, working tree limpa, commit local sincronizado e binding Git canônico permite `sync_state: clean`.

Se houver mudança local, o Hermes usa `sync_state: dirty`, mesmo quando essa mudança também faria o check do estado falhar. Se o commit local estiver atrás ou o check do estado falhar numa árvore limpa, usa `sync_state: stale`. Se o fetch autenticado ou a relação entre commits não puder ser verificada, usa `sync_state: unknown`. Em qualquer caso diferente de `clean`, informa a limitação antes da resposta e não apresenta conteúdo como atual. `sync-status.json`, quando materializado por operação, é apenas um snapshot do status do owner e nunca substitui a verificação do checkout.

O checkout canônico usa a branch local `codex/vault-plan-b` e exatamente o upstream `origin/codex/vault-plan-b`. O remote `origin` tem uma única fetch URL e no máximo uma push URL, ambas normalizadas para `https://github.com/ArthurMalucelli/fgv-vault.git`, sem credenciais, query string ou fragmento embutido. Rewrites `insteadOf` e `pushInsteadOf`, `branch.pushRemote`, `remote.pushDefault` e listas múltiplas são proibidos. Cada gate revalida esse binding antes da próxima mutação. `status`, `refresh`, `publish`, smoke, readiness e cutover bloqueiam qualquer outro binding.

Um PDF e seu arquivo `.extracted.md` são a mesma fonte. O Markdown extraído é canônico para busca; o original serve para conferência. Eles nunca contam como duas evidências independentes.

## Caminhos canônicos

- Matérias ativas: `10 Matérias/<Materia>/`.
- Aulas: `10 Matérias/<Materia>/Aulas/MM.DD/`.
- Material Eclass: `10 Matérias/<Materia>/Aulas/MM.DD/Material/`.
- Tasks: `00 Home/Tasks.md`.
- Estado materializado: `30 Sistema/Estado/`.
- Conceitos: `20 Conhecimento/Conceitos/`.
- Arquivo: `90 Arquivo/<semestre>/`.

Nenhum componente ativo usa matérias na raiz, `Vault/`, `S1/`, `Slides/Material`, `Resumo.md` fixo ou `/root/vault/Tasks.md`.

## Ownership

`fgv-sync` é o único owner de Git no VPS. Eclass, WhatsApp, cronjobs, skills e memória não executam `git fetch`, `git pull`, `git merge`, `git commit` ou `git push`. Eles pedem `fgv-sync status`, `fgv-sync refresh` ou `fgv-sync publish`.

O gerador compartilhado é o único writer de `catalog.jsonl` e `dashboard-snapshot.md`. Hermes pode escrever material do Eclass, extração textual, resumo preliminar e tasks vindas do Eclass. Hermes não reescreve um resumo final produzido pelo workflow `/fgv`; registra a lacuna ou cria material complementar.

## Sessão e contexto

Cada pergunta começa sem despejar o vault ou o catálogo inteiro no contexto. O query local limitado decide os candidatos. O snapshot fornece estado agregado. Só então o Hermes abre o arquivo necessário. O limite normal é um arquivo acadêmico completo por pergunta; qualquer exceção precisa listar os caminhos e a razão.

## Falhas

Ausência de componente obrigatório, symlink que escape das raízes, data operacional vencida, catálogo inválido, orçamento de query excedido, upstream ou origin divergente, working tree sujo, divergência Git, checksum divergente ou smoke test vermelho bloqueia o cutover. O estado final permitido na preparação é `READY` ou `BLOCKED`. O cutover só começa após o validador aceitar `READY` para o SHA remoto exato e para o checksum exato deste manifesto.
