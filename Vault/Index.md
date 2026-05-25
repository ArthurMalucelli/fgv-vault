---
tags: [index, home]
---

# FGV vault

Vault de estudos da FGV EAESP. Cada matéria tem pasta própria, com sub-pasta `Aulas/DD.MM.AA/` por aula contendo `Transcrito.md` e `Resumo.md`.

## Matérias ativas

- [[ProdutosFinanceiros]]
- [[Estatistica]]
- [[ComportamentoDoConsumidor]]
- [[OperacoesParaCompetitividade]]
- [[IntroducaoAGestao]]
- [[Programacao]]
- [[Sociologia]]
- [[PVU]]

## Estrutura

```
~/FGV/
├── <Matéria>/
│   └── Aulas/
│       └── DD.MM.AA/
│           ├── Transcrito.md
│           └── Resumo.md
└── Vault/
    ├── Index.md          (este arquivo)
    ├── Tasks.md          (lista de prazos consolidada)
    ├── Conceitos/        (notas atômicas: SELIC, Greenwashing, etc.)
    ├── Templates/        (templates de aula, resumo, conceito)
    ├── Attachments/      (imagens e arquivos colados)
    └── Daily/            (daily notes, se ativar)
```

## Convenções

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
