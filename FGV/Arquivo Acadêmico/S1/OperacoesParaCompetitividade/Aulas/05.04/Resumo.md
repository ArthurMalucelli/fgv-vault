---
materia: OperacoesParaCompetitividade
data: 2026-05-04
tema: Balanceamento de linha (correção), Pareto, 5W2H e PDCA
tags: [resumo]
---

# Resumo 04.05 — Balanceamento, Pareto, 5W2H, PDCA

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Balanceamento de Linha]] | Distribuir tarefas entre estações de trabalho minimizando ociosidade, sem violar TC nem precedência. Heurístico, não exato |
| [[Tempo de Ciclo]] | Tempo máximo permitido por estação para atender demanda. TC = (horas × 60 × dias) / demanda, ajustado por eficiência |
| [[Numero Teorico de Operadores]] | N teórico = soma dos tempos / TC. Sempre arredonda PARA CIMA, nunca arredondamento financeiro |
| [[Eficiência do Balanceamento]] | PB = N teórico / N real. Mede uniformidade da distribuição. Quanto mais perto de 1, melhor |
| [[Gargalo]] | Tarefa mais longa da linha, restringe a máxima produção. Em logística chama "guardado/cardápio" |
| [[Pareto]] | Gráfico que combina barras (frequência) e linha (% acumulada) para identificar poucos itens responsáveis por muito impacto |
| [[Princípio 80-20]] | 80% dos problemas vêm de 20% das causas. Inverso vale (80% lucro vem de 20% produtos) |
| [[5W2H]] | Plano de ação: What, Why, Who, Where, When, How, How much |
| [[PDCA]] | Ciclo de melhoria contínua: Plan, Do, Check, Act |
| [[Ishikawa]] | Diagrama qualitativo de causas. Combina com Pareto (qualitativo + quantitativo) |
| [[Just-in-Time]] | Próxima aula (11.05) |
| [[Lean]] | Próxima aula (11.05) |

## Fórmulas

<pre>
TC bruto = (horas × 60 × dias) / demanda
TC líquido = TC bruto × (1 − perda%)        [se exercício mencionar perda]

N teórico = soma dos tempos das tarefas / TC
            (SEMPRE arredondar para cima)

PB (eficiência) = N teórico / N real
                = soma dos tempos / (N real × TC)

Máxima produção (caminho do gargalo) = 60 / tempo da tarefa mais longa
                                       (em unidades por hora)

Frequência % acumulada = freq% atual + freq% acum anterior
</pre>

## Pegadinhas

- **Arredondamento de N teórico:** sempre PRA CIMA, mesmo que dê 3,1. Não é arredondamento financeiro. Se vier 3,8, vira 4. Se vier 3,2, vira 4 também.
- **Perda% reduz TC:** quando o exercício diz "considere perda de 15%", o TC fica MENOR (multiplica por 0,85), não maior. Logo o TC fica mais apertado e exige mais operadores.
- **Balanceamento respeita precedência:** A com F só dá pra juntar se F vier diretamente depois de A. Se C, D estão no meio, não pula.
- **N teórico ≠ N real:** N teórico vem da soma de tempos. N real vem do agrupamento heurístico, sempre é igual ou maior que o teórico.
- **Pergunta sobre máxima produção** = caminho curto do gargalo (60/maior tempo), não cálculo completo de balanceamento. Lê o enunciado antes de gastar tempo.
- **Pareto: 80-20 é regra de bolso, não exata.** Pode dar 70-25, 83-30 dependendo da base. Não force o número.
- **Excel — referência absoluta com F4:** o denominador (total) precisa estar travado pra arrastar a fórmula sem quebrar.
- **Excel — frequência acumulada:** primeira linha = primeira freq%. A partir da segunda, soma a anterior + atual. Termina em 100%.
- **Gráfico combinado de Pareto:** Inserir → Gráficos Recomendados → Todos os Gráficos → Combinação (última opção). Coluna pra frequência, linha pra acumulada.
- **5W2H pós-Ishikawa/Pareto:** Ishikawa identifica causas (qualitativo), Pareto prioriza (quantitativo), 5W2H planeja a ação corretiva. Sequência lógica.
- **PDCA — Check é comparar real vs planejado.** Se diferiu de forma negativa, vai pro Act (ação corretiva), e o ciclo recomeça.

## Pra fixar

- [[Balanceamento de Linha]]
- [[Tempo de Ciclo]]
- [[Numero Teorico de Operadores]]
- [[Eficiência do Balanceamento]]
- [[Gargalo]]
- [[Pareto]]
- [[Princípio 80-20]]
- [[5W2H]]
- [[PDCA]]
- [[Ishikawa]]

## Avisos da aula

- **Prova final:** 11 de junho, 15h, unificada.
- **Trabalho final:** virou vídeo gravado (Zoom/Teams), 7 minutos, todos no vídeo, link privado + PDF dos slides. Entrega até 1 de junho, 14h59.
- **Exercício individual (E-Class letra 15):** combina Ishikawa + Pareto + PDCA. Entrega domingo (10.05), 23h59.

## Próxima aula (11.05)

Just-in-Time e Lean. Ferramentas de competitividade.
