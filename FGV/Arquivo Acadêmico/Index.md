---
tags: [index, home]
---

# FGV vault

Vault de estudos da FGV EAESP. Cada matéria ativa tem pasta própria na raiz, com sub-pasta `Aulas/MM.DD/` por aula contendo `Transcrito.md` e `Resumo.md`. Semestres encerrados são arquivados em pasta própria na raiz (`S1/`, futuramente `S2/`, etc.).

## Matérias ativas (2026.2)

| Matéria | Pasta | Tag |
|---|---|---|
| Tecnologia, Dados e Negócios | `TecnologiaDadosENegocios` | `#tdn` |
| Psicologia | `Psicologia` | `#psi` |
| Matemática Aplicada I | `MatematicaAplicada1` | `#ma1` |
| Estudos Organizacionais | `EstudosOrganizacionais` | `#eo` |
| Estatística II | `Estatistica2` | `#est2` |
| Direito Empresarial | `DireitoEmpresarial` | `#dir` |
| Contabilidade Financeira | `ContabilidadeFinanceira` | `#cont` |

## Arquivo

- `S1/` contém as matérias de 2026.1: ProdutosFinanceiros, Estatistica, ComportamentoDoConsumidor, OperacoesParaCompetitividade, IntroducaoAGestao, Programacao, Sociologia, PVU. As tasks do S1 estão na seção de arquivo de [[Tasks]].

## Estrutura

```
~/FGV/
├── <Matéria>/            (matérias do semestre corrente)
│   └── Aulas/
│       └── MM.DD/
│           ├── Transcrito.md
│           └── Resumo.md
├── S1/                   (arquivo do semestre 2026.1, mesma estrutura)
└── Vault/
    ├── Index.md          (este arquivo)
    ├── Tasks.md          (lista de prazos consolidada, único arquivo de tasks)
    ├── Conceitos/        (notas atômicas: SELIC, Greenwashing, etc.)
    ├── Templates/        (templates de aula, resumo, conceito)
    ├── Attachments/      (imagens e arquivos colados)
    └── Daily/            (daily notes, se ativar)
```

## Convenções

- Pasta de aula em formato `MM.DD` (ex: `08.12` = 12 de agosto), pro sort alfabético ficar cronológico
- `[[wikilinks]]` pra conceitos importantes
- Tag `#prova` em coisa pra revisar antes da prova
- Tag `#duvida` em ponto não entendido
- Tag `#aula` em transcript de aula
- Tasks com sintaxe Tasks plugin (📅 prazo, ⏫ prioridade)

## Atalhos úteis

| Atalho | Ação |
|---|---|
| Cmd+O | Quick switcher (abrir nota) |
| Cmd+P | Command palette |
| Cmd+Shift+F | Busca global no vault |
| Cmd+E | Toggle preview/edit |
| Cmd+Shift+G | Graph view |
| Cmd+Shift+T | Inserir template |
| Cmd+click em [[link]] | Abrir em painel ao lado |

## Tasks pendentes (próximas 2 semanas)

```tasks
not done
heading does not include Arquivo S1
due before in 14 days
sort by due
```

## Aulas com tag #prova

```dataview
TABLE WITHOUT ID
  file.link as "Aula",
  materia as "Matéria",
  data as "Data"
FROM #prova
SORT data DESC
LIMIT 10
```

## Conceitos mais conectados

```dataview
TABLE WITHOUT ID
  file.link as "Conceito",
  length(file.inlinks) as "Citações"
FROM "Vault/Conceitos"
SORT length(file.inlinks) DESC
LIMIT 15
```
