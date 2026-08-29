# Validação local do pacote Hermes

## Identidade

- Timestamp UTC: `2026-08-29T17:40:25Z`.
- Branch isolada: `codex/vault-hermes`.
- Base: `c840413926da944254edb57b14564cf68c001e3b`.
- Commit do pacote testado: `9fc1199a6c18b447889bd693004e2c41350ef455`.
- Tree do pacote testado: `cc9c2d4a11f185516bdbbecda3bfda0044f2b7d8`.
- VPS, vault vivo e Git remoto: não acessados ou modificados.

## Checksums

- `hermes-manifest.json`: `123e040f3169676c6a56533a8179ef72bce485747b95afaf8999ca54a8e7509c`.
- `PREPARAR-BUNDLE.json`: `afabacca3ce5d08e104b925e4f7b40562fba2c42be835ba5245ac12a1086add8`.
- `CUTOVER-BUNDLE.json`: `f69ceb36a68cdd0917b0ca88138cedc1804d5cd3f195292b88d82dee437e7721`.

## Gates executados

| Gate | Comando | Resultado |
|---|---|---|
| Suíte Hermes focal | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src' python3 -B .fgv/tests/test_hermes_package.py` | exit 0, 71 testes, `OK` |
| Suíte completa | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src:.fgv/tests' python3 -B -m unittest discover -s .fgv/tests -p 'test_*.py'` | exit 0, 225 testes, `OK` |
| Bundle PREPARAR | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'` | `pass` |
| Bundle CUTOVER | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'` | `pass` |
| Sintaxe do wrapper | `bash -n '30 Sistema/Hermes/fgv-sync'` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| Artefatos Python | `find .fgv -type d -name __pycache__ -print` | zero resultados |

Os testes cobrem auditoria AST e shell por formato fechado, imports em escopo aninhado, aliases por atribuição, Python `-c` em cron, operações destrutivas de `pathlib`, symlinks, paths antigos, Git fora do owner, comandos destrutivos, lock, working tree suja, fetch, status público fechado, validação do commit remoto em worktree temporária, fast-forward, preservação de HEAD em falha, publicação por allowlist, rebuild/check do estado, hashes adulterados, backup integral, zero untracked, evidência real, relatório recente, commit divergente, conjunto canônico exato de seis queries, paths selecionados e abertos, timings completos, smoke catalog-first, arquivo exato, `as_of_commit` e stale.

Também estão cobertos a data operacional de São Paulo, o bloqueio de snapshot fora da data operacional, o vínculo exato com branch local, source branch, upstream, refspec de fetch e remote canônicos, a rejeição de rewrites e rotas alternativas de push, a reautenticação de `.git/config` depois de cada gate, o predicado de filho direto da aula, o filtro `subject_id`, a consulta limitada do catálogo e a recomputação byte a byte dos artefatos Eclass e WhatsApp.

Os gates adversariais incluem source branch maliciosa publicada no destino remoto canônico, troca do catálogo entre autenticação e consulta, probe morto de canal, reatribuição da API de processo, branch não executada, artefato de query fabricado fora do entrypoint e módulo local tentando substituir a biblioteca padrão. O channel smoke exige o schema AST fechado, executa os entrypoints staging reais com Python isolado `-I`, vincula challenge, bytes consumidos e hash do artefato, e o readiness repete essa execução antes de aceitar a evidência.

As consultas de teste usam fixtures explícitas e não substituem a repetição live depois do merge do pacote Hermes. Readiness só aceita as seis queries canônicas, no commit corrente, com artefatos reais, orçamento limitado e snapshot da mesma data operacional.

## Limite deste receipt

Este receipt certifica o pacote isolado, não o cutover. Depois da integração, é obrigatório repetir a suíte, `generate_state.py --check`, `validate_vault.py`, o smoke sem `--fixture-mode` e o gate do readiness report no SHA remoto final. Até lá, o estado correto é `PACKAGE_READY_FOR_INTEGRATION`, não `READY` para produção.
