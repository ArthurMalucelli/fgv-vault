# Contrato canônico do workflow FGV v1

Este arquivo é o único contrato de máquina editável do workflow FGV.

## Invariantes

- O raw Plaud é imutável, deve ser preservado byte a byte e sua origem externa nunca é apagada pelo workflow.
- O transaction_id é determinístico a partir da versão do contrato, do hash do raw, da matéria e da data resolvida.
- Matéria ou data ambígua interrompe qualquer escrita e exige confirmação.
- A reexecução da mesma transação é no-op verificável.
- Um arquivo pertencente a outra transaction_id nunca pode ser sobrescrito.
- Todo CalendarIntent entra primeiro em uma fila idempotente.
- Todo cancelamento ou reagendamento exige confirmação explícita antes do efeito externo.
- Um conceito novo exige critério explícito de promoção.
- Codex e Claude nunca executam Git de rede.
- Obsidian Git é o único owner de Git no Mac.
- fgv-sync é o único owner de Git no VPS.
- O catálogo e o snapshot do dashboard têm um único writer, `.fgv/scripts/generate_state.py`.
- Todos os paths são NFC.

## Identidade e estados

`transaction_id = sha256("fgv:v1\\0" + source_sha256 + "\\0" + subject_id + "\\0" + class_date)[:20]`

`preflight -> planned -> staged -> validated -> published -> side_effects_pending -> complete`

Qualquer falha antes de `published` preserva os arquivos canônicos anteriores. Uma falha de Calendar mantém o intent pendente e repetível.

## Paths e nomes

- As pastas de aula seguem `10 Matérias/<folder>/Aulas/MM.DD/`.
- Os arquivos visíveis são `Transcrito - <tema>.md`, `Resumo - <tema>.md` e `Revisao - <tema>.md`.
- O ano permanece no YAML e nos IDs, nunca no nome visível dentro da pasta da aula.

## Limites desta branch

Nesta branch, são proibidos instalação live e merge em main.
