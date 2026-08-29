---
name: fgv
description: Processa transcrições Plaud e pedidos acadêmicos no vault FGV pelo contrato canônico versionado.
---

# FGV runtime adapter

CONTRACT: 1
CORE: `<vault>/.fgv/CORE.md`
CLI: `python3 <vault>/.fgv/scripts/fgv_workflow.py`
GIT_ROLE: `mac-agent`

1. Carregue `.fgv/VERSION`, `.fgv/CORE.md` e `.fgv/config/subjects.json`.
2. Para Plaud, leia a transcrição inteira. Resolva matéria pelo registry e data por evidência. Se uma delas estiver ambígua, pergunte antes de escrever.
3. Produza um `analysis.json` temporário com `subject_id`, `topic`, `cleaned_transcript`, `summary`, `topics`, cinco a dez `review_questions`, `concept_candidates`, `task_mentions` e `calendar_mentions`.
4. No transcrito, retire ruído sem apagar definições, mecanismos, exemplos, números, perguntas substantivas e alertas de prova. No resumo, condense todo conceito preservado.
5. Rode `plan-plaud`, confira paths e `transaction_id`, depois rode `apply-plaud` apenas com plano válido.
6. Nunca mova, altere ou apague a origem Plaud. O core preserva uma cópia byte-identical em `Fontes/`.
7. Nunca execute Git de rede, commit ou push. Obsidian Git é o owner no Mac.
8. Conceitos novos só entram quando passam o gate. Tasks exigem data concreta, recebem a tag do registry e são deduplicadas.
9. Calendar produz apenas `CalendarIntent`. Cancelamento e reagendamento exigem confirmação explícita.
10. O core delega o refresh a `.fgv/scripts/generate_state.py`. Passe em `--as-of` a data operacional em `America/Sao_Paulo`, nunca a data histórica da aula. Não mantenha um segundo gerador.
11. Se o receipt terminar em `state_pending`, rode o mesmo apply novamente com o mesmo `--as-of` persistido. O core autentica o que já existe e conclui somente o refresh pendente.
12. Retorne receipt com `transaction_id`, paths, hashes, intents e validações.
13. Rerun de receipt `complete` é somente leitura. Se o dashboard estiver stale, rode `build-state --vault <vault> --as-of YYYY-MM-DD` com a data operacional atual.

## Analysis v1 mínimo

```json
{
  "schema_version": 1,
  "subject_id": "contabilidade-financeira",
  "topic": "DRE e provisões",
  "cleaned_transcript": "## Competência\n\nTexto limpo.",
  "summary": "## Conceitos essenciais\n\nResumo denso.",
  "topics": ["DRE", "provisões"],
  "review_questions": ["1?", "2?", "3?", "4?", "5?"],
  "concept_candidates": [],
  "task_mentions": [{"description": "Revisar provisões", "due": "2026-09-04", "priority": ""}],
  "calendar_mentions": []
}
```

## Ferramentas do runtime

Use ferramentas locais do Codex e solicite aprovação no momento exato de qualquer efeito externo autorizado.

```sh
python3 <vault>/.fgv/scripts/fgv_workflow.py plan-plaud --vault <vault> --source <transcript> --analysis <analysis.json> --class-date YYYY-MM-DD --runtime codex --output <plan.json>
python3 <vault>/.fgv/scripts/fgv_workflow.py apply-plaud --plan <plan.json> --vault <vault> --source <transcript> --analysis <analysis.json> --processor codex --as-of YYYY-MM-DD
python3 <vault>/.fgv/scripts/fgv_workflow.py build-state --vault <vault> --as-of YYYY-MM-DD
```
