# Pacote Hermes

O pacote tem duas fases independentes:

- `PREPARAR-BUNDLE.json` e `PROMPT-HERMES-PREPARAR.md`: auditoria e adaptação em staging. Não muda produção.
- `CUTOVER-BUNDLE.json` e `PROMPT-HERMES-CUTOVER.md`: mudança produtiva recuperável. Só roda com relatório `READY` autenticado.

Antes de usar qualquer fase, valide seus checksums:

```bash
python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/PREPARAR-BUNDLE.json'
python3 .fgv/scripts/verify_hermes_bundle.py --root "$PWD" --bundle '30 Sistema/Hermes/CUTOVER-BUNDLE.json'
```

O primeiro prompt é o handoff inicial para o Hermes. O segundo fica guardado até Arthur revisar o readiness report.

Consultas acadêmicas usam `hermes_catalog_query.py` com o SHA-256 pinado pelo snapshot. Evidências Eclass e WhatsApp só são válidas quando `hermes_channel_smoke.py` valida o schema AST fechado, executa novamente os entrypoints staging reais com Python isolado `-I` e autentica challenge, stdout consumido, path aberto, checkout e branch remota.
