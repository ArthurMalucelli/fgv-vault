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
8. Conceitos novos só entram quando passam o gate. Tasks exigem data concreta e são deduplicadas.
9. Calendar produz apenas `CalendarIntent`. Cancelamento e reagendamento exigem confirmação explícita.
10. O core delega o refresh a `.fgv/scripts/generate_state.py`. Não mantenha um segundo gerador.
11. Retorne receipt com `transaction_id`, paths, hashes, intents e validações.

## Ferramentas do runtime

Use ferramentas locais do Claude. Um connector Calendar disponível só pode traduzir intents já confirmadas.
