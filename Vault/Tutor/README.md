# Vault/Tutor/

Namespace do bot tutor (Hermes VPS). NAO edite arquivos aqui manualmente.

## Arquivos
- `log.md`: historico de sessoes, append-only
- `gaps.md`: gaps abertos por materia, sobrescrito a cada sessao
- `concepts-history.json`: tracking por conceito (bot-only)
- `conceitos-propostos/`: conceitos novos identificados em sessao, ainda nao no canon

## Promover conceito proposto
Move arquivo de `conceitos-propostos/X.md` para `Conceitos/X.md` e remove o frontmatter de proposta.
