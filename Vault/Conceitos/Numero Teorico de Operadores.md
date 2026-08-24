---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, operações, produção]
---

# Numero Teorico de Operadores

## Definição

Número mínimo teórico de estações (operadores) necessário pra atender à demanda. Representa o piso teórico: na prática (N real), o número quase sempre é maior por causa das restrições de precedência.

## Fórmula / aplicação

<pre>
N teórico = soma dos tempos das tarefas / TC

SEMPRE arredondar para o próximo INTEIRO superior.
NÃO é arredondamento financeiro (3,1 vira 4, não 3).
</pre>

Lógica: a soma de tempos é o trabalho total a ser feito. Dividir pelo TC dá quantos "buckets" do tamanho TC são necessários.

Exemplos:
- Soma = 9,7 min, TC = 2,55 min → 9,7/2,55 = 3,8 → **4 operadores teóricos**.
- Soma = 3,1 min, TC = 0,96 min → 3,1/0,96 = 3,2 → **4 operadores teóricos**.

Comparado ao N real:
- N real ≥ N teórico **sempre**.
- A diferença vem das restrições de precedência (não dá pra juntar A com F se C, D, E estão no caminho) e do formato das durações (tarefas grandes ocupam estação inteira sozinhas).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Balanceamento de Linha]]
- [[Tempo de Ciclo]]
- [[Eficiência do Balanceamento]]
