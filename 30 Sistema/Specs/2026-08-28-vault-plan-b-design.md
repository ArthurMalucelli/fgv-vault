# FGV Vault Plan B Design

## Objetivo

Transformar o vault FGV em um sistema acadêmico único para Arthur, Obsidian, Codex, Claude e Hermes. O sistema deve preservar todo o conteúdo atual, reduzir ambiguidade de busca, tornar o estado acadêmico visível em um dashboard, sustentar recuperação ativa e permitir que múltiplos agentes trabalhem sem sobrescrever os mesmos artefatos.

## Restrições confirmadas

- O vault vivo em `~/FGV` permanece intacto até Hermes validar a nova estrutura.
- A implementação ocorre na branch `codex/vault-plan-b` e em worktree isolada.
- Nenhuma informação atual será apagada durante a migração.
- O histórico Git não será reescrito nesta fase.
- Os arquivos binários permanecem no repositório durante a transição.
- As matérias ativas deixam a raiz e passam para `10 Matérias/`.
- `00 Home/` deve ser o primeiro folder visível no File Explorer do Obsidian.
- A data permanece na pasta da aula, não precisa ser repetida no nome visível dos arquivos.
- Arquivos de aula recebem nomes descritivos por tipo e tema.
- Codex e Claude devem produzir o mesmo contrato de saída ao executar `/fgv`.
- Hermes deve continuar acessando todo o conteúdo pelo GitHub, mas não pode depender de Dataview ou Tasks renderizados pelo Obsidian.

## Não objetivos desta fase

- Criar banco vetorial ou sistema de embeddings.
- Reescrever o histórico Git de 520 MB.
- Migrar automaticamente o VPS do Hermes a partir do Mac.
- Mesclar a branch em `main` antes dos testes do Hermes.
- Excluir duplicatas binárias sem revisão explícita.
- Trocar o provedor ou modelo usado pelo Hermes.

## Arquitetura final

```text
FGV/
├── 00 Home/
│   ├── Home.md
│   ├── Tasks.md
│   ├── Revisões.md
│   └── Inbox/
├── 10 Matérias/
│   ├── ContabilidadeFinanceira/
│   ├── DireitoEmpresarial/
│   ├── Estatistica2/
│   ├── EstudosOrganizacionais/
│   ├── MatemáticaAplicada/
│   ├── Psicologia/
│   └── TecnologiaDadosNegocios/
├── 20 Conhecimento/
│   └── Conceitos/
├── 30 Sistema/
│   ├── Anexos/
│   ├── Automacoes/
│   ├── Estado/
│   │   ├── catalog.jsonl
│   │   ├── dashboard-snapshot.md
│   │   └── sync-status.json
│   ├── Hermes/
│   ├── Plans/
│   ├── Skills/
│   ├── Specs/
│   ├── Templates/
│   └── Tutor/
└── 90 Arquivo/
    └── 2026.1/
```

As matérias em `10 Matérias/` representam somente o semestre ativo. No fechamento do semestre, elas migram para `90 Arquivo/<ano.semestre>/`. Isso preserva uma superfície diária curta sem perder histórico.

## Estrutura de matéria

```text
10 Matérias/ContabilidadeFinanceira/
├── Disciplina.md
├── Avaliações/
├── Treinos/
├── Erros.md
└── Aulas/
    └── 08.28/
        ├── Resumo - DRE, provisões e arrendamentos.md
        ├── Transcrito - DRE, provisões e arrendamentos.md
        ├── Fontes/
        │   └── Plaud - original.txt
        └── Materiais/
            ├── Slides - DRE.pdf
            └── Slides - DRE.extracted.md
```

`Disciplina.md` é o dashboard da matéria. Ele mostra próximas avaliações, últimas aulas, aulas incompletas, conceitos com domínio baixo, treinos e erros. O conteúdo é derivado das propriedades das notas e de `00 Home/Tasks.md`.

## Contrato de nomes

- Pasta de matéria: nome canônico atual, sem abreviação nova.
- Pasta de aula: `MM.DD`, com dois dígitos.
- Transcrito processado: `Transcrito - <tema curto>.md`.
- Resumo: `Resumo - <tema curto>.md`.
- Material original: `<tipo> - <tema>.<extensão>` quando for seguro renomear.
- Extração textual: mesmo nome do original com sufixo `.extracted.md`.
- Tema curto: dois a cinco conceitos discriminantes, sem repetir matéria ou data.
- Todo arquivo processado recebe `id` estável no YAML.

As buscas dos agentes usam padrões `Resumo*.md` e `Transcrito*.md`, nunca igualdade com um único nome fixo.

## Schema de metadata

### Campos comuns

```yaml
---
id: cont-2026-08-28-resumo
tipo: resumo
materias: [contabilidade-financeira]
semestre: 2026.2
data: 2026-08-28
tema: DRE, provisões e arrendamentos
topicos: [DRE, provisões, arrendamentos]
status: completo
origens: [plaud, eclass]
atualizado_por: fgv
atualizado_em: 2026-08-28T22:00:00-03:00
---
```

`materias` é sempre uma lista, inclusive em notas associadas a uma única matéria. Valores usam slugs canônicos definidos em `30 Sistema/Estado/materias.json`.

### Campos de aprendizagem

```yaml
dominio: 1
ultima_revisao:
proxima_revisao: 2026-08-29
```

`dominio` varia de zero a três:

- `0`: ainda não tentou recuperar.
- `1`: reconhece, mas não explica sem consulta.
- `2`: explica ou resolve com pequenos erros.
- `3`: explica ou resolve corretamente sem consulta.

### Campos de material extraído

```yaml
source_file: Slides - DRE.pdf
source_hash: sha256:...
extraction_type: pdf-text
canonical_for_search: true
```

Hermes pesquisa primeiro o arquivo extraído. O original permanece a referência para verificação e não conta como evidência independente.

## Dashboard e catálogo

`00 Home/Home.md` contém queries de Tasks, Bases e Dataview para uso dentro do Obsidian. Como Hermes lê Markdown bruto e não renderiza plugins, um gerador determinístico também produz:

- `30 Sistema/Estado/catalog.jsonl`: uma linha por artefato acadêmico.
- `30 Sistema/Estado/dashboard-snapshot.md`: estado acadêmico materializado.
- `30 Sistema/Estado/sync-status.json`: commit, horário e resultado da última geração.

O dashboard mostra:

- prazos próximos e atrasados;
- aulas com transcrição ausente;
- aulas com material, mas sem resumo final;
- revisões vencidas;
- estado de cada matéria;
- última aula processada;
- próxima avaliação;
- erros e conceitos de domínio baixo.

O gerador é o único escritor dos arquivos de estado. Codex, Claude e Hermes alteram artefatos canônicos e executam o mesmo gerador.

## Fluxo Plaud com `/fgv`

O fluxo diário do Arthur permanece:

1. Baixar a transcrição do Plaud.
2. Abrir Codex ou Claude.
3. Executar `/fgv` e anexar a transcrição.

O adaptador executa:

1. Detectar matéria, data, professor e tema.
2. Confirmar somente quando matéria ou data forem ambíguas.
3. Sincronizar o Git de forma segura antes de escrever.
4. Criar ou localizar a pasta da aula.
5. Mover o arquivo original para `Fontes/`.
6. Preservar o original, sem apagar.
7. Gerar transcrito limpo com mapa da aula no início.
8. Gerar resumo com recuperação ativa, aplicações e lacunas.
9. Criar somente conceitos centrais ou reutilizáveis.
10. Registrar prazos concretos em `00 Home/Tasks.md`.
11. Atualizar Google Calendar quando o adaptador tiver conector disponível.
12. Gerar catálogo e dashboard snapshot.
13. Validar caminhos, metadata e links.
14. Sincronizar o commit conforme a política Git aprovada.

## Recuperação ativa

Todo resumo contém:

- mapa da aula;
- conceitos essenciais;
- fórmulas e mecanismos;
- exemplos do professor;
- pegadinhas;
- cinco a dez perguntas para responder sem consulta;
- uma ou duas aplicações quando o conteúdo permitir;
- dúvidas abertas;
- próxima revisão;
- links para transcrito, materiais e conceitos.

Notas conceituais deixam de ser criadas em lote. Um conceito novo exige pelo menos um dos critérios:

- centralidade explícita na aula;
- uso em exercício ou avaliação;
- recorrência em mais de uma aula;
- relação entre matérias;
- necessidade de explicação própria.

## Ownership entre agentes

| Artefato | Escritor canônico |
|---|---|
| Plaud original | `/fgv` |
| Transcrito limpo | `/fgv` |
| Resumo final | `/fgv` |
| Material Eclass | Hermes |
| Markdown extraído | Hermes |
| Resumo preliminar sem Plaud | Hermes |
| Tasks vindas da aula | `/fgv` |
| Tasks vindas do Eclass | Hermes |
| Catálogo e dashboard snapshot | gerador compartilhado |

Hermes não reescreve silenciosamente um resumo final. Quando encontra lacuna, registra status parcial ou cria material complementar. O próximo `/fgv` pode incorporar a lacuna preservando proveniência.

## Skills compartilhadas

O contrato comum fica versionado em `30 Sistema/Skills/fgv-core/`. Ele contém workflow, schema, naming, templates e validações.

Os adaptadores permanecem pequenos:

- Codex: `~/.agents/skills/fgv/SKILL.md`.
- Claude: `~/.claude/skills/fgv/SKILL.md`.
- Hermes: skills e memória no VPS.

Codex e Claude carregam o mesmo core. Diferenças são limitadas a ferramentas de arquivos, Calendar, Git e confirmação. Um instalador local cria backups das skills atuais antes de ativar os adaptadores novos.

## Integração Hermes

A auditoria confirmou que Hermes é filesystem-first, usa clone persistente, ripgrep e leitura direta. Não existe banco vetorial. Portanto:

- renomes não exigem reindexação;
- caminhos hardcoded precisam ser atualizados;
- o script `eclass-scan.py` precisa gravar na nova estrutura;
- skills, memória e cronjobs precisam apontar para `10 Matérias/` e `00 Home/Tasks.md`;
- Hermes consulta `catalog.jsonl` antes de explorar o filesystem;
- Markdown extraído torna binários pesquisáveis por ripgrep;
- uma rotina de background mantém `/root/vault` atualizado;
- cada resposta acadêmica registra o commit utilizado;
- sessões acadêmicas evitam carregar histórico de WhatsApp com mais de 200 mil tokens.

A branch não entra em `main` até o Hermes executar o pacote de testes contra `codex/vault-plan-b`.

## Política Git

- `origin/main` continua como fonte compartilhada após o cutover.
- Toda escrita começa com verificação de working tree e sincronização.
- Escritas executam o gerador antes do commit.
- Commits incluem somente arquivos pertencentes ao workflow corrente e arquivos gerados.
- Em caso de concorrência, o escritor tenta uma atualização segura uma vez.
- Conflito interrompe a automação e gera relatório, nunca force push.
- Obsidian Git continua como backup de edições manuais.
- O histórico pesado permanece inalterado nesta fase.
- Limpeza do histórico exige projeto separado e aprovação explícita após o cutover.

## Migração

A migração ocorre por script determinístico e idempotente:

1. Gerar inventário e mapa antigo para novo.
2. Executar dry-run sem escrever.
3. Verificar colisões e links ambíguos.
4. Mover meta-organização para `00 Home`, `20 Conhecimento`, `30 Sistema` e `90 Arquivo`.
5. Mover matérias ativas para `10 Matérias`.
6. Renomear resumos e transcritos usando tema extraído de YAML ou conteúdo.
7. Padronizar metadata.
8. Reescrever wikilinks e caminhos explícitos.
9. Gerar dashboards de matéria e global.
10. Gerar catálogo e snapshot.
11. Validar contagens, hashes, links e Git diff.

Arquivos sem classificação segura vão para `00 Home/Inbox/Legado/`. Nenhum arquivo é excluído.

## Validação e critérios de aceite

### Integridade

- Mesma quantidade de arquivos de conteúdo antes e depois, exceto arquivos gerados novos.
- Mesmo hash para todo binário apenas movido.
- Zero arquivos perdidos.
- Zero colisões silenciosas.
- Zero links ambíguos novos.
- Links quebrados por acento corrigidos ou registrados.

### Obsidian

- `00 Home/Home.md` abre como página inicial.
- Tasks, Bases e Dataview renderizam sem erro.
- Templates usam o schema canônico.
- Attachments apontam para `30 Sistema/Anexos`.
- Daily Notes fica desativado até existir fluxo explícito.

### `/fgv`

- Codex e Claude geram os mesmos nomes, metadata e seções para uma fixture comum.
- Plaud original permanece em `Fontes/`.
- Tasks são deduplicadas.
- Conceitos não são criados em massa.
- Catálogo e snapshot refletem a nova aula.

### Hermes

- Pergunta por matéria e aula mais recente encontra o arquivo correto.
- Busca por transcrição funciona com nomes descritivos.
- Material Eclass chega à matéria e aula corretas.
- Original e extração não são tratados como evidências independentes.
- Clone local está no mesmo commit do remoto antes da resposta.
- Consulta acadêmica não carrega o histórico integral do WhatsApp.

## Rollout e rollback

1. Implementar e testar na worktree.
2. Publicar somente a branch `codex/vault-plan-b`.
3. Hermes cria backup de `/root/.hermes` e `/root/vault`.
4. Hermes testa a branch sem alterar `main`.
5. Codex e Claude testam adaptadores em diretórios temporários.
6. Arthur recebe relatório comparativo e prompt de cutover.
7. Após aprovação operacional, atualizar Hermes e adaptadores locais.
8. Mesclar a branch em `main`.

Rollback consiste em voltar os adaptadores antigos e retornar `main` ao commit anterior por operação não destrutiva. A branch de migração e os backups permanecem disponíveis para auditoria.
