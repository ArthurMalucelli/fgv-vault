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

## Adicionadas manualmente

<!-- Espaço pra você adicionar prazos que não vieram de aula -->

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

## Arquivo S1 (2026.1)

Tasks do primeiro semestre, preservadas como estavam no fim do semestre. Excluídas dos dashboards acima pelo filtro de heading.

- [ ] Prova final Programação (notebook Jupyter, 5 questões: conceito, ler pandas, if+validação, DataFrame, parse de strings) #prog 📅 2026-06-10 🔺
- [ ] Prova final OC (unificada, 15h) #oc 📅 2026-06-11 🔺
- [ ] Prova final Produtos Financeiros (cumulativa pós-parcial: listas 4/6/7/8/9/10, sem amortização) #pf 📅 2026-06-10 🔺
- [ ] Entrega trabalho final OC: PDF dos slides + link do vídeo (até 14h59) #oc 📅 2026-06-01 🔺
- [x] Último exercício OC: análise EBIT/Reclame Aqui via GenAI (escolher loja, classificar elogios/reclamações por categoria, texto analítico ligando a prioridades competitivas, upload Word no E-Class até 16h40) #oc ⏫ 📅 2026-05-18 ✅ 2026-05-24
- [x] Exercício individual E-Class letra 15: Ishikawa + Pareto + PDCA (até 23h59) #oc ⏫ 📅 2026-05-10 ✅ 2026-05-24
- [ ] Quarta provinha Estatística (IC para proporção + IC para média) #est 📅 2026-05-27 ⏫
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
- [x] Prova Produtos Financeiros (renda fixa BR + câmbio) #pf 🔺 📅 2026-05-20 ✅ 2026-05-24
- [ ] Atividade de valor Programação — trabalho em grupo no formato de prova (até 3 alunos, sem consulta) #prog 📅 2026-05-26 🔺
- [ ] Aula Programação de tirar dúvidas sobre o trabalho em grupo #prog 📅 2026-05-21 ⏫
- [ ] Baixar arquivo de dados do trabalho em grupo Programação #prog 📅 2026-05-20 ⏫
