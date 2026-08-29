# Readiness report Hermes

O arquivo entregue ao gate é JSON UTF-8, sem comentários, com exatamente estas chaves. Não inclua hostname, usuário real, token, cookie, senha, URL com credencial ou conteúdo dos arquivos auditados.

```json
{
  "schema_version": 1,
  "timestamp_utc": "2026-08-28T12:00:00Z",
  "host_role": "hermes-vps",
  "recommendation": "READY",
  "production_commit": "0000000000000000000000000000000000000000",
  "tested_commit": "1111111111111111111111111111111111111111",
  "package_manifest_sha256": "2222222222222222222222222222222222222222222222222222222222222222",
  "backup": {
    "path": "/root/backups/fgv-hermes-20260828T120000Z",
    "sha256": "3333333333333333333333333333333333333333333333333333333333333333"
  },
  "untracked": {
    "inventory_sha256": "4444444444444444444444444444444444444444444444444444444444444444",
    "backup_sha256": "5555555555555555555555555555555555555555555555555555555555555555",
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
    {
      "id": "latest_class",
      "duration_ms": 4
    }
  ],
  "context_tokens": 1200,
  "diff_summary": [
    "staged configuration only"
  ]
}
```

Valores permitidos para `recommendation`: `READY`, `BLOCKED` e `ROLLED_BACK`. O validador autoriza cutover somente para `READY`. `retrieval_fixture_mode` precisa ser `false` e `retrieval_sync_state` precisa ser `clean`. `query_timings` mede a recuperação local. `context_tokens` mede o contexto entregue ao modelo, não a resposta. `package_manifest_sha256` é o SHA-256 de `30 Sistema/Hermes/hermes-manifest.json`, não do bundle.
