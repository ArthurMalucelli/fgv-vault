# Briefing Plan B

Acesso direto a `catalog.jsonl` é proibido. Leia o hash em `dashboard-snapshot.md` e execute `python3 .fgv/scripts/hermes_catalog_query.py --vault "$FGV_VAULT_ROOT" --query-type latest_class --expected-catalog-sha256 "$CATALOG_SHA256"`; depois releia o snapshot e somente então o arquivo exato.
Use `hermes_catalog_query.py` com candidatos limitados. Nunca injete o catálogo completo no contexto.
Use `fgv-sync`. Responda com `as_of_commit` e `sync_state`.
