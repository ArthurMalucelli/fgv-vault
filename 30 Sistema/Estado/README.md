# Estado gerado

`catalog.jsonl` e `dashboard-snapshot.md` são read models. O gerador compartilhado é o único escritor destes dois arquivos.

As notas, tarefas e estados de aprendizagem do filesystem são a fonte canônica. Arthur, `/fgv` e Hermes alteram apenas as fontes que possuem e depois executam:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/scripts/generate_state.py --vault . --as-of YYYY-MM-DD
```

Não edite os arquivos gerados manualmente. Em conflito Git, preserve as fontes e regenere o estado.

`.generation.lock` é um arquivo vazio e versionado usado para serializar geradores concorrentes. Não o remova. O modo `--check` apenas abre esse arquivo existente e não cria nem altera arquivos.

Hermes deve validar `schema_version` e o `catalog_sha256` incorporado ao snapshot. Se o catálogo estiver ausente, incompatível ou inconsistente, o fallback é a leitura direta do filesystem.

## Proveniência

- `source_fingerprint` autentica os bytes e caminhos das fontes acadêmicas que entraram no build.
- `build_fingerprint` combina contrato, versão do gerador, data `as_of` e `source_fingerprint`.
- `catalog_sha256` vincula o snapshot aos bytes exatos de `catalog.jsonl`.
- A proveniência por commit Git pertence ao `fgv-sync`. O gerador local não grava commit, hostname ou horário de máquina no estado.
