---
tags: [tasks, home]
---

# Tasks FGV

Lista consolidada de prazos. Tasks são adicionadas automaticamente pela skill `/fgv` quando ela detecta menção de prazo em transcript de aula. Você também pode adicionar manualmente.

## Sintaxe

```
- [ ] Descrição da task #sigla 📅 YYYY-MM-DD ⏫
```

Tags de matéria (siglas curtas, agrupam no dashboard):
- `#cdc` — Comportamento do Consumidor
- `#est` — Estatística
- `#ig` — Introdução à Gestão
- `#oc` — Operações para Competitividade
- `#pvu` — PVU
- `#pf` — Produtos Financeiros
- `#prog` — Programação
- `#soc` — Sociologia

Emojis de metadado:
- 📅 prazo final
- ⏫ alta prioridade
- 🔺 urgentíssima (prova, entrega final)
- 🔽 baixa
- 🔁 every week (recorrência)
- ✅ data de conclusão (auto)

Marcar como feita: clica no checkbox ou troca `[ ]` por `[x]`.

## Adicionadas pela skill `/fgv`

<!-- A skill adiciona tasks aqui automaticamente quando processa transcript -->

- [ ] Prova final OC (unificada, 15h) #oc 📅 2026-06-11 🔺
- [ ] Entrega trabalho final OC: PDF dos slides + link do vídeo (até 14h59) #oc 📅 2026-06-01 🔺
- [x] Último exercício OC: análise EBIT/Reclame Aqui via GenAI (escolher loja, classificar elogios/reclamações por categoria, texto analítico ligando a prioridades competitivas, upload Word no E-Class até 16h40) #oc ⏫ 📅 2026-05-18 ✅ 2026-05-24
- [x] Exercício individual E-Class letra 15: Ishikawa + Pareto + PDCA (até 23h59) #oc ⏫ 📅 2026-05-10 ✅ 2026-05-24
- [ ] 4ª Provinha Estatística #est 📅 2026-05-27 ⏫
- [ ] Prova final Estatística (15h, NÃO deixar pra segunda chamada, é mais difícil por design) #est 📅 2026-06-08 🔺
- [ ] 3º relatório Estatística: Intervalos de Confiança a partir dos dados coletados #est 📅 2026-06-01 ⏫
- [x] Apresentação ensaio prototipagem CDC (8 min/grupo, feedback da prof. antes da final pro Bruno) #cdc ⏫ 📅 2026-05-13 ✅ 2026-05-24
- [x] Conferir todas as notas de Estatística no E-Class (planilha "Notas" + planilha de correção da ativ. de equipes); reclamações até sexta #est ⏫ 📅 2026-05-15 ✅ 2026-05-24
- [x] Entrega projeto trabalho final Soc (max 2 pgs: tema + objeto + questão + 2 textos do curso integrais) via eclass até 23h #soc 🔺 📅 2026-05-19 ✅ 2026-05-24
- [ ] Orientação trabalho final Soc Grupo A (presença obrigatória de todos) #soc 📅 2026-05-21 ⏫
- [ ] Orientação trabalho final Soc Grupo B (presença obrigatória de todos) #soc 📅 2026-05-26 ⏫
- [ ] Entrega relatório trabalho final Soc Grupo A (max 3 pgs) via eclass até 23h #soc 📅 2026-05-28 🔺
- [ ] Entrega relatório trabalho final Soc Grupo B (max 3 pgs) via eclass até 23h #soc 📅 2026-06-02 🔺
- [x] Definir grupo trabalho final Soc (5-6 pessoas, inalterável) + enviar lista pra silvia.rodrigues@fgv.br #soc ⏫ 📅 2026-05-19 ✅ 2026-05-24

## Adicionadas manualmente

<!-- Espaço pra você adicionar prazos que não vieram de aula -->

---

## Dashboard

### Todas as tasks pendentes ordenadas por prazo

```tasks
not done
sort by due
hide backlink
hide edit button
hide postpone button
short mode
```

### Atrasadas

```tasks
not done
due before today
sort by due
hide backlink
short mode
```

### Próximos 7 dias

```tasks
not done
due before in 7 days
due after yesterday
sort by due
hide backlink
short mode
```

### Por matéria

```tasks
not done
group by tags
sort by due
hide backlink
hide tags
short mode
```

### Concluídas recentemente (últimos 14 dias)

```tasks
done after 14 days ago
sort by done reverse
hide backlink
short mode
```
