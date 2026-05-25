---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, operações, produção]
---

# Balanceamento de Linha

## Definição

Distribuir as tarefas de uma linha de produção entre estações de trabalho buscando minimizar ociosidade e tempos mortos, sem violar dois critérios:
1. Nenhuma estação pode ter soma de tempos maior que o [[Tempo de Ciclo]].
2. A precedência das tarefas deve ser respeitada (uma tarefa só roda quando suas predecessoras terminaram).

É um método **heurístico**, não exato. Não há solução única: o mesmo problema admite combinações diferentes que respeitem ambos os critérios.

## Fórmula / aplicação

Sequência de cálculo:

<pre>
1. TC = (horas × 60 × dias) / demanda
   ajustar por (1 − perda%) se houver perda

2. N teórico = soma dos tempos / TC
   SEMPRE arredondar para cima (não financeiro)

3. Heurística de agrupamento, respeitando TC e precedência:
   para cada par (a, b) com b sucessora de a:
       se tempo(a) + tempo(b) ≤ TC: junta numa estação
       senão: cada uma fica em estação separada

4. N real = número de estações resultantes
   N real ≥ N teórico (sempre)

5. Eficiência = N teórico / N real
              = soma dos tempos / (N real × TC)
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Tempo de Ciclo]]
- [[Numero Teorico de Operadores]]
- [[Eficiência do Balanceamento]]
- [[Gargalo]]
- [[Just-in-Time]]
- [[Lean]]
