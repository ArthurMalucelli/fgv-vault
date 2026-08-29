# Certificação da migração Plan B

## Resultado

Status: `PASS`.

- Data operacional: `2026-08-29`, fuso `America/Sao_Paulo`.
- Commit de conteúdo certificado: `10475654fad3ae35eee801c1a80cdf10ca316ebf`.
- Tree certificada: `6a2c982cd2103668dc57b0ef6dbe45525a2d06ec`.
- Commit da implementação de runtime: `10475654fad3ae35eee801c1a80cdf10ca316ebf`.
- Tree da implementação de runtime: `6a2c982cd2103668dc57b0ef6dbe45525a2d06ec`.
- Commit da suíte final: `10475654fad3ae35eee801c1a80cdf10ca316ebf`.
- Tree da suíte final: `6a2c982cd2103668dc57b0ef6dbe45525a2d06ec`.
- SHA-256 agregado do conteúdo certificado: `28e37f1ba2ee3e383ec160341e63591615b366bfdd79382df0a0b6699f2402cd`.
- Base preservada do vault vivo: `cf8fe8c440a4dd442490afee62c0119a7db5ef9c`.
- Branch de entrega: `codex/vault-plan-b`.

## Estrutura entregue

- `00 Home/`: dashboard, tarefas e entrada diária.
- `10 Matérias/`: sete matérias ativas, cada uma com aulas `MM.DD` e materiais em `Material/`.
- `20 Conhecimento/Conceitos/`: conceitos reutilizáveis e domínio de aprendizagem.
- `30 Sistema/`: estado gerado, especificações, planos, workflow `/FGV` e pacote Hermes.
- `90 Arquivo/2026.1/`: semestre anterior preservado.
- `.fgv/`: geradores, migradores, validadores e testes.

## Integridade

| Medida | Resultado |
|---|---:|
| Arquivos acadêmicos no catálogo | 1.036 |
| Entradas verificadas no filesystem | 1.549 |
| Arquivos byte a byte idênticos | 1.008 |
| Transformações de corpo autorizadas | 11 |
| Aulas com mudança apenas de metadados | 40 |
| Registros de delta do vault vivo | 13 |
| Links resolvidos | 5.035 |
| Links ambíguos | 0 |
| Links legados não resolvidos e preservados | 407 |
| Matérias ativas | 7 |
| Tarefas abertas | 9 |
| Estados de aprendizagem | 5 |
| Warnings do estado gerado | 0 |

Os 407 links legados não resolvidos não foram inventados nem redirecionados automaticamente. Eles permanecem preservados para correção explícita, sem ambiguidade criada pela migração.

## Gates

- Suíte integrada: 330 testes, `OK`.
- Estado determinístico: `state fresh`.
- Validador do vault: `pass` em todos os cinco grupos.
- Importador do delta vivo: `no_op`, 13 registros autenticados.
- Bundle Hermes PREPARAR: `pass`.
- Bundle Hermes CUTOVER: `pass`.
- Paridade dos adapters Codex e Claude: `true`.
- Duas revisões independentes do runner Hermes e dos testes de fronteira: `PASS`, sem P0, P1 ou P2.
- Vault vivo: limpo em `main`, igual a `origin/main`, sem modificação.

## Limite operacional

Esta certificação cobre a branch isolada e seus pacotes. Ela não instala skills globais, não altera `/root/.hermes`, não altera o VPS e não troca o vault vivo. O próximo passo autorizado é somente o PREPARAR do Hermes em staging. O CUTOVER depende de um readiness report `READY` autenticado.
