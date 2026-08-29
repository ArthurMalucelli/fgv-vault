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
- Codex e Claude compartilham um lock global por vault durante qualquer apply.
- O plano contém somente paths relativos internos. Source e analysis externos entram novamente no apply e seus hashes são reautenticados.
- Raw, manifest e nomes derivados são fixados no plano. Nenhum suffix é escolhido durante o apply.
- Cada transaction_id possui receipt durável em `30 Sistema/Estado/workflow-transactions/`.
- Falhas parciais avançam por roll-forward autenticado. Falha do dashboard deixa a transação em `state_pending`.
- O analysis usa schema fechado v1 em `.fgv/schemas/analysis.schema.json`.
- O gerador de estado é chamado como `generate_state.py --vault <root> --as-of YYYY-MM-DD`; `--as-of` é a data operacional em `America/Sao_Paulo`, separada da data da aula, e `--check` roda antes da primeira escrita no vault.
- `apply-plaud` persiste o `--as-of` no receipt; retries usam o mesmo valor. `build-state` e `apply-plaud` compartilham o lock global do vault.
- Rerun de receipt `complete` é somente leitura. Se o estado global estiver stale, use `build-state` com o `--as-of` operacional atual; uma transação histórica nunca regride o relógio do dashboard.

## Identidade e estados

O payload é a concatenação de bytes, nesta ordem:

- bytes UTF-8 do texto formado por `fgv:v` seguido, sem delimitador, pela versão decimal do contrato sem zeros à esquerda;
- source_sha256 tem exatamente 64 caracteres hexadecimais lowercase ASCII, sem prefixo;
- subject_id e class_date são codificados em UTF-8, em componentes separados e nessa ordem.

O separador é exatamente um byte NUL `0x00`, usado entre componentes adjacentes e sem separador no final. O digest_hex representa o digest SHA-256 do payload com 64 caracteres hexadecimais lowercase. O transaction_id usa os primeiros 20 caracteres de digest_hex.

`preflight -> planned -> raw -> manifest -> transcrito -> resumo -> concepts -> tasks -> state_pending -> complete`

Cada efeito local é persistido antes do checkpoint seguinte. Uma interrupção pode deixar um prefixo autenticável da transação; o retry verifica esse prefixo e continua sem duplicar. Calendar permanece somente como intent pendente e repetível, sem ação externa.

## Paths e nomes

- As pastas de aula seguem `10 Matérias/<folder>/Aulas/MM.DD/`.
- Os arquivos visíveis são `Transcrito - <tema>.md`, `Resumo - <tema>.md` e `Revisao - <tema>.md`.
- O raw é `Plaud - <transaction_id>.<ext>` e o manifest é `Manifest - <transaction_id>.json`.
- O ano permanece no YAML e nos IDs, nunca no nome visível dentro da pasta da aula.

## Limites desta branch

Nesta branch, são proibidos instalação live e merge em main.
