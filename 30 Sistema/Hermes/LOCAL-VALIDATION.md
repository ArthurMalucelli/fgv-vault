# Validação local do pacote Hermes

## Identidade

- Timestamp UTC: `2026-08-29T02:31:27Z`.
- Branch isolada: `codex/vault-hermes`.
- Base: `c840413926da944254edb57b14564cf68c001e3b`.
- Commit do pacote testado: `e6e2141fda0ec4bbb1d5061dcf71593c48fecdc3`.
- Tree do pacote testado: `330252349aa27b9bb9548652a9bd6d30a79f573d`.
- VPS, vault vivo e Git remoto: não acessados ou modificados.

## Checksums

- `hermes-manifest.json`: `bbdcf0a8be36eee71a4dc0afb6fb42df1e8e7dd192d4bf4294bf6f637a9bfcf3`.
- `PREPARAR-BUNDLE.json`: `2417b6bcf19ac96a721525bdd9b1ab30d5f6e885e1d6877f1fd6a4521d9bb421`.
- `CUTOVER-BUNDLE.json`: `897884285bcbaef94db38e1bfdbc2182529b7fdffb3efe9eaec00873742b31cc`.

## Gates executados

| Gate | Comando | Resultado |
|---|---|---|
| Suíte Hermes focal | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src' python3 -B .fgv/tests/test_hermes_package.py` | exit 0, 41 testes, `OK` |
| Suíte completa | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src' python3 -m unittest discover -s .fgv/tests -q` | exit 0, 195 testes, `OK` |
| Bundle PREPARAR | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'` | `pass` |
| Bundle CUTOVER | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'` | `pass` |
| Sintaxe do wrapper | `bash -n '30 Sistema/Hermes/fgv-sync'` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| Artefatos Python | `find .fgv -type d -name __pycache__ -print` | zero resultados |

Os testes cobrem auditoria AST e shell por formato fechado, imports em escopo aninhado, aliases por atribuição, Python `-c` em cron, operações destrutivas de `pathlib`, symlinks, paths antigos, Git fora do owner, comandos destrutivos, lock, working tree suja, fetch, status público fechado, validação do commit remoto em worktree temporária, fast-forward, preservação de HEAD em falha, publicação por allowlist, rebuild/check do estado, hashes adulterados, backup integral, zero untracked, evidência real, relatório recente, commit divergente, conjunto canônico exato de seis queries, paths selecionados e abertos, timings completos, smoke catalog-first, arquivo exato, `as_of_commit` e stale.

As seis queries live foram comparadas, sem escrita, ao catálogo imutável do commit integrado `7372c3c`: todas selecionaram os paths esperados. Isso valida a expectativa do smoke, não substitui sua repetição depois do merge do pacote Hermes.

## Limite deste receipt

Este receipt certifica o pacote isolado, não o cutover. Depois da integração, é obrigatório repetir a suíte, `generate_state.py --check`, `validate_vault.py`, o smoke sem `--fixture-mode` e o gate do readiness report no SHA remoto final. Até lá, o estado correto é `PACKAGE_READY_FOR_INTEGRATION`, não `READY` para produção.
