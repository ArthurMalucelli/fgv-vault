# Readiness report Hermes

O gate recebe JSON UTF-8 sem comentários e com exatamente as chaves abaixo. `timestamp_utc` precisa ter no máximo 30 minutos. O SHA-256 exato deste arquivo JSON é uma entrada separada do validador.

```json
{
  "schema_version": 1,
  "timestamp_utc": "2026-08-28T12:00:00Z",
  "host_role": "hermes-vps",
  "recommendation": "READY",
  "production_commit": "0000000000000000000000000000000000000000",
  "tested_commit": "1111111111111111111111111111111111111111",
  "package_manifest_sha256": "2222222222222222222222222222222222222222222222222222222222222222",
  "prepare_bundle_sha256": "3333333333333333333333333333333333333333333333333333333333333333",
  "backup": {
    "path": "/root/backups/fgv-hermes-20260828T120000Z",
    "manifest_path": "backup-manifest.json",
    "manifest_sha256": "4444444444444444444444444444444444444444444444444444444444444444"
  },
  "untracked": {
    "inventory_sha256": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "files": [],
    "preserved": true,
    "classified": true
  },
  "findings": {
    "required_remaining": 0,
    "warnings": 0
  },
  "component_results": {
    "eclass-scan.py": "pass",
    "eclass": "pass",
    "fgv-eclass-api": "pass",
    "fgv-briefing": "pass",
    "academic-reading-notes": "pass",
    "memory": "pass",
    "cronjobs": "pass"
  },
  "smoke_tests": {
    "academic_retrieval": "pass",
    "eclass": "pass",
    "whatsapp": "pass"
  },
  "retrieval_fixture_mode": false,
  "retrieval_sync_state": "clean",
  "query_timings": [
    {"id": "ultima-aula-matematica", "duration_ms": 1},
    {"id": "transcrito-matematica", "duration_ms": 2},
    {"id": "proxima-avaliacao", "duration_ms": 3},
    {"id": "material-eclass", "duration_ms": 4},
    {"id": "conceito-gap", "duration_ms": 5},
    {"id": "compat-resumo", "duration_ms": 6}
  ],
  "context_tokens": 1200,
  "diff_summary": [
    "staged configuration only"
  ],
  "evidence": {
    "audit_after": {"path": "/abs/evidence/audit-after.json", "sha256": "5555555555555555555555555555555555555555555555555555555555555555"},
    "cutover_validation": {"path": "/abs/evidence/cutover-validation.json", "sha256": "6666666666666666666666666666666666666666666666666666666666666666"},
    "retrieval_smoke": {"path": "/abs/evidence/retrieval-smoke.json", "sha256": "7777777777777777777777777777777777777777777777777777777777777777"},
    "test_suite": {"path": "/abs/evidence/test-suite.json", "sha256": "8888888888888888888888888888888888888888888888888888888888888888"},
    "eclass_smoke": {"path": "/abs/evidence/eclass-smoke.json", "sha256": "9999999999999999999999999999999999999999999999999999999999999999"},
    "whatsapp_smoke": {"path": "/abs/evidence/whatsapp-smoke.json", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
  }
}
```

O inventário produtivo esperado é vazio. Qualquer arquivo untracked ou mudança tracked bloqueia `READY`.

O backup manifest é JSON fechado com `schema_version`, `production_commit`, `inventory_sha256` e `files`. Cada item de `files` tem `source_path`, `backup_path` e `sha256`. Ele precisa listar exatamente todos os arquivos regulares da configuração Hermes ativa, sem symlinks, em ordem de `source_path`. O validador compara origem, cópia e hashes byte a byte.

As seis evidências são arquivos JSON reais e pinados. O smoke acadêmico usa schema fechado e precisa declarar `fixture_mode: false`, `stale: false`, `sync_state: clean`, `state_check: pass` e `as_of_commit` igual a `tested_commit`.

O smoke contém exatamente estes seis resultados, nesta ordem: `ultima-aula-matematica`, `transcrito-matematica`, `proxima-avaliacao`, `material-eclass`, `conceito-gap` e `compat-resumo`. Cada resultado precisa ter `matched: true`, abrir apenas o path esperado em `retrieval-queries.json` e registrar os seis passos catalog-first. `query_timings` repete exatamente os seis IDs e as durações presentes nessa evidência, sem duplicatas. O resultado de cutover precisa declarar `vault_commit` igual a `tested_commit`. Um relatório preenchido sem esses arquivos não autoriza CUTOVER.
