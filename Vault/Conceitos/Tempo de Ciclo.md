---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, operações, produção]
---

# Tempo de Ciclo

## Definição

Tempo máximo permitido em cada estação de trabalho para que a linha consiga atender à demanda. É o "tic-tac" da linha: a cada TC unidades de tempo, uma peça pronta sai da linha.

Se uma estação tem soma de tempos maior que o TC, a linha não consegue produzir o volume demandado.

## Fórmula / aplicação

Caso 1, sem perda:
<pre>
TC = (horas × 60 × dias) / demanda
</pre>

Onde:
- horas = horas de operação por dia
- 60 = conversão de horas pra minutos
- dias = dias úteis no período
- demanda = unidades a produzir no período

Caso 2, com perda% (ineficiência):
<pre>
TC = [(horas × 60 × dias) / demanda] × (1 − perda%)
</pre>

A perda **reduz** o TC, deixando-o mais apertado. Lógica: se 15% do tempo é perdido (manutenção, retrabalho, paradas), o tempo útil é só 85% do bruto.

Exemplo:
- 8 horas × 60 × 25 dias = 12.000 minutos disponíveis
- Demanda = 4.000 unidades
- TC bruto = 12.000 / 4.000 = 3 minutos
- Com perda 15%: TC = 3 × 0,85 = 2,55 minutos

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Balanceamento de Linha]]
- [[Numero Teorico de Operadores]]
- [[Gargalo]]
- [[Eficiência do Balanceamento]]
