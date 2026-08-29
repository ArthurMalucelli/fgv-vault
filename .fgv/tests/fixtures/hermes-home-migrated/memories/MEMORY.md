# Memória Plan B

Acesso direto a `catalog.jsonl` é proibido. Leia o hash em `dashboard-snapshot.md` e execute `python3 .fgv/scripts/hermes_catalog_query.py --vault "$FGV_VAULT_ROOT" --query-type <tipo> --expected-catalog-sha256 "$CATALOG_SHA256"`; depois releia o snapshot e abra apenas o caminho exato.
Use `hermes_catalog_query.py` com candidatos limitados. Nunca injete o catálogo completo no contexto.
O Git pertence a `fgv-sync`. Toda resposta declara `as_of_commit` e `sync_state`.
