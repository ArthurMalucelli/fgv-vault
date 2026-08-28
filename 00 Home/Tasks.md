---
tags: [tasks, home]
---

# Tasks FGV

Lista consolidada de prazos. Tasks são adicionadas automaticamente pela skill `/fgv` quando ela detecta menção de prazo em transcript de aula. Você também pode adicionar manualmente. Este é o único arquivo de tasks do vault.

## Sintaxe

```
- [ ] Descrição da task #sigla 📅 YYYY-MM-DD ⏫
```

Tags de matéria 2026.2 (siglas curtas, agrupam no dashboard):
- `#tdn` Tecnologia, Dados e Negócios
- `#psi` Psicologia
- `#ma1` Matemática Aplicada I
- `#eo` Estudos Organizacionais
- `#est2` Estatística II
- `#dir` Direito Empresarial
- `#cont` Contabilidade Financeira

Tags do S1 (`#cdc`, `#est`, `#ig`, `#oc`, `#pvu`, `#pf`, `#prog`, `#soc`) só aparecem na seção de arquivo no fim deste arquivo.

Emojis de metadado:
- 📅 prazo final
- ⏫ alta prioridade
- 🔺 urgentíssima (prova, entrega final)
- 🔽 baixa
- 🔁 every week (recorrência)
- ✅ data de conclusão (auto)

Marcar como feita: clica no checkbox ou troca `[ ]` por `[x]`.

## Adicionadas pela skill /fgv

<!-- A skill adiciona tasks aqui automaticamente quando processa transcript -->

- [x] Imprimir o caso da aula de TDN (professora recomendou trazer impresso) #tdn 📅 2026-08-21 ✅ 2026-08-24
- [x] Fazer o exercício de Excel de teste de proporções no eClass #est2 📅 2026-08-18 ✅ 2026-08-24
- [ ] Prova parcial 1 de Contabilidade, 14h-15h30 no laboratório de informática (questionário Eclass + planilha em branco, sem internet) #cont 📅 2026-08-28 🔺
- [ ] Plantão de dúvidas online de Contabilidade à noite (véspera da prova) #cont 📅 2026-08-26
- [ ] Refazer a atividade pré-prova de Contabilidade como simulado de 2h (até 3 tentativas, sem nota) #cont 📅 2026-08-27 ⏫
- [ ] Quiz de Estatística II na aula (1ª Provinha, qui-quadrado, ~1h, 10 questões, R/Excel/mão) #est2 📅 2026-08-25 🔺

## Adicionadas manualmente

<!-- Espaço pra você adicionar prazos que não vieram de aula -->

### Apartamento novo

- [ ] Instalar chuveirinho no banheiro #casa
- [ ] Instalar cuba/prateleira para shampoo e produtos dentro do box #casa
- [ ] Instalar gancho para toalhas de rosto #casa

---

## Dashboard

### Todas as tasks pendentes ordenadas por prazo

```tasks
not done
heading does not include Arquivo S1
sort by due
hide backlink
hide edit button
hide postpone button
short mode
```

### Atrasadas

```tasks
not done
heading does not include Arquivo S1
due before today
sort by due
hide backlink
short mode
```

### Próximos 7 dias

```tasks
not done
heading does not include Arquivo S1
due before in 7 days
due after yesterday
sort by due
hide backlink
short mode
```

### Por matéria

```tasks
not done
heading does not include Arquivo S1
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

---
