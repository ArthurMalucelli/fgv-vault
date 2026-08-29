# Validação local do pacote Hermes

## Identidade

- Timestamp UTC: `2026-08-29T04:41:32Z`.
- Branch isolada: `codex/vault-hermes`.
- Base: `c840413926da944254edb57b14564cf68c001e3b`.
- Commit do pacote testado: `bba13f42f6fcaee8ae0e00c657760d0e6dcf7ed9`.
- Tree do pacote testado: `a96a38b7fbafa607732825a5aa6e96a5fd6f3a84`.
- VPS, vault vivo e Git remoto: não acessados ou modificados.

## Checksums

- `hermes-manifest.json`: `5c34e7b59657188f88ee4d0bfd61ef2e70742184f606e39a906dd4dd2c9a2168`.
- `PREPARAR-BUNDLE.json`: `254548d8e4861462e49c632157d5c86b4b39e492266dca547c0b081d0ae15a75`.
- `CUTOVER-BUNDLE.json`: `86b7a02147572567a5ba3ac343d15c8589b16b8a3f67a57281ff26839d4a2604`.

## Gates executados

| Gate | Comando | Resultado |
|---|---|---|
| Suíte Hermes focal | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src' python3 -B .fgv/tests/test_hermes_package.py` | exit 0, 60 testes, `OK` |
| Suíte completa | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src' python3 -m unittest discover -s .fgv/tests -q` | exit 0, 214 testes, `OK` |
| Bundle PREPARAR | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'` | `pass` |
| Bundle CUTOVER | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'` | `pass` |
| Sintaxe do wrapper | `bash -n '30 Sistema/Hermes/fgv-sync'` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| Artefatos Python | `find .fgv -type d -name __pycache__ -print` | zero resultados |

Os testes cobrem auditoria AST e shell por formato fechado, imports em escopo aninhado, aliases por atribuição, Python `-c` em cron, operações destrutivas de `pathlib`, symlinks, paths antigos, Git fora do owner, comandos destrutivos, lock, working tree suja, fetch, status público fechado, validação do commit remoto em worktree temporária, fast-forward, preservação de HEAD em falha, publicação por allowlist, rebuild/check do estado, hashes adulterados, backup integral, zero untracked, evidência real, relatório recente, commit divergente, conjunto canônico exato de seis queries, paths selecionados e abertos, timings completos, smoke catalog-first, arquivo exato, `as_of_commit` e stale.

Também estão cobertos a data operacional de São Paulo, o bloqueio de snapshot fora da data operacional, o vínculo exato com branch local, upstream e remote canônicos, a rejeição de rewrites e rotas alternativas de push, a reautenticação de `.git/config` depois de cada gate, o predicado de filho direto da aula, o filtro `subject_id`, a consulta limitada do catálogo e a recomputação byte a byte dos artefatos Eclass e WhatsApp.

As consultas de teste usam fixtures explícitas e não substituem a repetição live depois do merge do pacote Hermes. Readiness só aceita as seis queries canônicas, no commit corrente, com artefatos reais, orçamento limitado e snapshot da mesma data operacional.

## Limite deste receipt

Este receipt certifica o pacote isolado, não o cutover. Depois da integração, é obrigatório repetir a suíte, `generate_state.py --check`, `validate_vault.py`, o smoke sem `--fixture-mode` e o gate do readiness report no SHA remoto final. Até lá, o estado correto é `PACKAGE_READY_FOR_INTEGRATION`, não `READY` para produção.
