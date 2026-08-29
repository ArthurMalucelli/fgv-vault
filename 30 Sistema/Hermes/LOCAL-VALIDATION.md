# Validação local do pacote Hermes

## Identidade

- Timestamp UTC: `2026-08-29T18:56:02Z`.
- Branch integrada: `codex/vault-plan-b`.
- Base original do pacote Hermes: `c840413926da944254edb57b14564cf68c001e3b`.
- Commit de runtime testado: `10475654fad3ae35eee801c1a80cdf10ca316ebf`.
- Tree de runtime testada: `6a2c982cd2103668dc57b0ef6dbe45525a2d06ec`.
- Commit da suíte final: `10475654fad3ae35eee801c1a80cdf10ca316ebf`.
- Tree da suíte final: `6a2c982cd2103668dc57b0ef6dbe45525a2d06ec`.
- VPS e vault vivo: não modificados por esta validação.

## Checksums

- `hermes-manifest.json`: `123e040f3169676c6a56533a8179ef72bce485747b95afaf8999ca54a8e7509c`.
- `PREPARAR-BUNDLE.json`: `6297c2c2e1efe747de1b86e3fe718d5f1ad7303eba5f3f90cb4a96ea64cfc5be`.
- `CUTOVER-BUNDLE.json`: `13e3141d25a94260327346a557dea64949e2c352842e73d7fb289d11310cda24`.

## Gates executados

| Gate | Comando | Resultado |
|---|---|---|
| Ranking Eclass final | quatro testes de documento, extração canônica, catálogo real e bundles | exit 0, 4 testes, `OK` |
| Suíte integrada completa | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src:.fgv/tests' python3 -B -m unittest discover -s .fgv/tests -p 'test_*.py' -q` | exit 0, 330 testes, `OK` |
| Bundle PREPARAR | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'` | `pass` |
| Bundle CUTOVER | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'` | `pass` |
| Sintaxe do wrapper | `bash -n '30 Sistema/Hermes/fgv-sync'` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| Artefatos Python | `find .fgv -type d -name __pycache__ -print` | zero resultados |

Os testes cobrem auditoria AST e shell por formato fechado, imports em escopo aninhado, aliases por atribuição, Python `-c` em cron, operações destrutivas de `pathlib`, symlinks, paths antigos, Git fora do owner, comandos destrutivos, lock, working tree suja, fetch, status público fechado, validação do commit remoto em worktree temporária, fast-forward, preservação de HEAD em falha, publicação por allowlist, rebuild/check do estado, hashes adulterados, backup integral, zero untracked, evidência real, relatório recente, commit divergente, conjunto canônico exato de seis queries, paths selecionados e abertos, timings completos, smoke catalog-first, arquivo exato, `as_of_commit` e stale.

Também estão cobertos a data operacional de São Paulo, o bloqueio de snapshot fora da data operacional, o vínculo exato com branch local, source branch, upstream, refspec de fetch e remote canônicos, a rejeição de rewrites e rotas alternativas de push, a reautenticação de `.git/config` depois de cada gate, o predicado de filho direto da aula, o filtro `subject_id`, a consulta limitada do catálogo e a recomputação byte a byte dos artefatos Eclass e WhatsApp.

Os gates adversariais incluem source branch maliciosa publicada no destino remoto canônico, troca do catálogo entre autenticação e consulta, probe morto de canal, reatribuição da API de processo, branch não executada, artefato de query fabricado fora do entrypoint, codificação de source divergente, troca do pathname depois da auditoria e módulo local tentando substituir a biblioteca padrão. O channel smoke exige o schema AST fechado e UTF-8 canônico, executa os bytes auditados pela entrada padrão com Python isolado `-I`, vincula challenge, bytes consumidos e hash do artefato, e o readiness repete essa execução antes de aceitar a evidência.

O ranking Eclass também é testado contra o catálogo real e contra permutações adversariais. `.extracted.md` é a versão canônica de um PDF, convenções equivalentes são agrupadas como uma fonte, documentos acadêmicos principais vencem código auxiliar na mesma data e a deduplicação independe da ordem e da data declarada.

As consultas de teste usam fixtures explícitas e não substituem a repetição live depois do merge do pacote Hermes. Readiness só aceita as seis queries canônicas, no commit corrente, com artefatos reais, orçamento limitado e snapshot da mesma data operacional.

## Limite deste receipt

Este receipt certifica o pacote integrado, não o cutover. O smoke sem `--fixture-mode` ainda precisa ser repetido no SHA remoto final, e o gate do readiness report continua obrigatório. Até lá, o estado correto é `BRANCH_CERTIFIED`, não `READY` para produção.
