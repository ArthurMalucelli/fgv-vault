# Validação local do pacote Hermes

## Identidade

- Timestamp UTC: `2026-08-29T18:13:45Z`.
- Branch integrada: `codex/vault-plan-b`.
- Base original do pacote Hermes: `c840413926da944254edb57b14564cf68c001e3b`.
- Commit de runtime testado: `5b40839c46c842ecad5c1d6be21343ae431dc58c`.
- Tree de runtime testada: `3b0a00d0f2278133503eaee041c195150c75f2f0`.
- Commit da suíte final: `b47338e18bf3c68fdf55bc1fd8420e168ef625cf`.
- Tree da suíte final: `2bc26f4bf81eb3ecced06089bb6ee4f442ce4e56`.
- VPS e vault vivo: não modificados por esta validação.

## Checksums

- `hermes-manifest.json`: `123e040f3169676c6a56533a8179ef72bce485747b95afaf8999ca54a8e7509c`.
- `PREPARAR-BUNDLE.json`: `986560230a2c58d5d2e1e08e7e389fa7d9ce2260b7a03dd060e56bd0f34646b7`.
- `CUTOVER-BUNDLE.json`: `073bd8c599789b39dbf9d14bba1af139955d50e08d5df75d49a7807872168e79`.

## Gates executados

| Gate | Comando | Resultado |
|---|---|---|
| Correção focal final | quatro testes de UTF-8, bytes pinados, readiness e imports isolados | exit 0, 4 testes, `OK` |
| Suíte integrada completa | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src:.fgv/tests' python3 -B -m unittest discover -s .fgv/tests -p 'test_*.py' -q` | exit 0, 327 testes, `OK` |
| Bundle PREPARAR | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'` | `pass` |
| Bundle CUTOVER | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'` | `pass` |
| Sintaxe do wrapper | `bash -n '30 Sistema/Hermes/fgv-sync'` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| Artefatos Python | `find .fgv -type d -name __pycache__ -print` | zero resultados |

Os testes cobrem auditoria AST e shell por formato fechado, imports em escopo aninhado, aliases por atribuição, Python `-c` em cron, operações destrutivas de `pathlib`, symlinks, paths antigos, Git fora do owner, comandos destrutivos, lock, working tree suja, fetch, status público fechado, validação do commit remoto em worktree temporária, fast-forward, preservação de HEAD em falha, publicação por allowlist, rebuild/check do estado, hashes adulterados, backup integral, zero untracked, evidência real, relatório recente, commit divergente, conjunto canônico exato de seis queries, paths selecionados e abertos, timings completos, smoke catalog-first, arquivo exato, `as_of_commit` e stale.

Também estão cobertos a data operacional de São Paulo, o bloqueio de snapshot fora da data operacional, o vínculo exato com branch local, source branch, upstream, refspec de fetch e remote canônicos, a rejeição de rewrites e rotas alternativas de push, a reautenticação de `.git/config` depois de cada gate, o predicado de filho direto da aula, o filtro `subject_id`, a consulta limitada do catálogo e a recomputação byte a byte dos artefatos Eclass e WhatsApp.

Os gates adversariais incluem source branch maliciosa publicada no destino remoto canônico, troca do catálogo entre autenticação e consulta, probe morto de canal, reatribuição da API de processo, branch não executada, artefato de query fabricado fora do entrypoint, codificação de source divergente, troca do pathname depois da auditoria e módulo local tentando substituir a biblioteca padrão. O channel smoke exige o schema AST fechado e UTF-8 canônico, executa os bytes auditados pela entrada padrão com Python isolado `-I`, vincula challenge, bytes consumidos e hash do artefato, e o readiness repete essa execução antes de aceitar a evidência.

As consultas de teste usam fixtures explícitas e não substituem a repetição live depois do merge do pacote Hermes. Readiness só aceita as seis queries canônicas, no commit corrente, com artefatos reais, orçamento limitado e snapshot da mesma data operacional.

## Limite deste receipt

Este receipt certifica o pacote isolado, não o cutover. Depois da integração, é obrigatório repetir a suíte, `generate_state.py --check`, `validate_vault.py`, o smoke sem `--fixture-mode` e o gate do readiness report no SHA remoto final. Até lá, o estado correto é `PACKAGE_READY_FOR_INTEGRATION`, não `READY` para produção.
