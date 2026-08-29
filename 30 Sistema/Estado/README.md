# Estado gerado

`catalog.jsonl` e `dashboard-snapshot.md` são read models. O gerador compartilhado é o único escritor destes dois arquivos.

As notas, tarefas e estados de aprendizagem do filesystem são a fonte canônica. Arthur, `/fgv` e Hermes alteram apenas as fontes que possuem e depois executam:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/scripts/generate_state.py --vault . --as-of YYYY-MM-DD
```

Não edite os arquivos gerados manualmente. Em conflito Git, preserve as fontes e regenere o estado.

Hermes deve validar `schema_version` e o `catalog_sha256` incorporado ao snapshot. Se o catálogo estiver ausente, incompatível ou inconsistente, o fallback é a leitura direta do filesystem.
