# Validação local do pacote Hermes

## Identidade

- Timestamp UTC: `2026-08-29T00:58:44Z`.
- Branch isolada: `codex/vault-hermes`.
- Base: `c840413926da944254edb57b14564cf68c001e3b`.
- Commit do pacote testado: `7ece80a2f384c304525293bc05d12719ed6af19d`.
- Tree do pacote testado: `00a6e778399a6ea2314d082b326518a096ee9bb3`.
- VPS, vault vivo e Git remoto: não acessados ou modificados.

## Checksums

- `hermes-manifest.json`: `7575b9e2be641badd46cdc57a35e1c392419390585e9d6692af1b75409937425`.
- `PREPARAR-BUNDLE.json`: `fd46a3649f58a5b2c797de235c9c37a2d845bf45dca19f908e9b6ffcc8b166eb`.
- `CUTOVER-BUNDLE.json`: `bc5d8a8d4f8823e3afda464219116614b9b05ab193059548411c8976e7f3051b`.

## Gates executados

| Gate | Comando | Resultado |
|---|---|---|
| Suíte completa | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='.fgv/scripts:.fgv/src' python3 -m unittest discover -s .fgv/tests -q` | exit 0, 182 testes, `OK` |
| Bundle PREPARAR | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'` | `pass` |
| Bundle CUTOVER | `python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'` | `pass` |
| Sintaxe do wrapper | `bash -n '30 Sistema/Hermes/fgv-sync'` | exit 0 |
| Whitespace | `git diff --check` | exit 0 |
| Artefatos Python | `find .fgv -type d -name __pycache__ -print` | zero resultados |

Os testes cobrem auditoria read-only, symlinks, paths antigos, Git fora do owner, determinismo, configuração migrada, lock, working tree sujo, fast-forward, divergência, publicação por allowlist, rebuild/check do estado, checksums adulterados, relatório não `READY`, commit divergente, smoke catalog-first, arquivo exato, `as_of_commit` e stale.

## Limite deste receipt

Este receipt certifica o pacote isolado, não o cutover. O gerador do dashboard pertence à branch de integração e ainda não existe nesta branch componente. Depois da integração, é obrigatório repetir a suíte, `generate_state.py --check`, o smoke sem `--fixture-mode` e o gate do readiness report no SHA remoto final. Até lá, o estado correto é `PACKAGE_READY_FOR_INTEGRATION`, não `READY` para produção.
