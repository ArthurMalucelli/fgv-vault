---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, operações, produção]
---

# Eficiência do Balanceamento

## Definição

Métrica que mede quão uniformemente o trabalho está distribuído entre as estações de uma linha balanceada. Vai de 0 a 1 (ou 0% a 100%). Quanto mais perto de 1, mais uniforme a carga, menos ociosidade, menor variância entre estações.

## Fórmula / aplicação

Forma rápida:
<pre>
PB = N teórico / N real
</pre>

Forma equivalente (sai no mesmo número):
<pre>
PB = soma dos tempos / (N real × TC)
</pre>

Por que dão o mesmo resultado:
<pre>
N teórico = soma dos tempos / TC
PB = (soma dos tempos / TC) / N real
   = soma dos tempos / (N real × TC)
</pre>

Exemplos:
- N teórico 3,8, N real 5: PB = 3,8/5 = 0,76 = **76%**.
- N teórico 3,2, N real 4: PB = 3,2/4 = 0,80 = **80%**.

Interpretação:
- 100% = perfeito, sem ociosidade.
- 70-80% = típico de linhas reais.
- < 60% = problema sério de balanceamento, vale revisitar.

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
- [[Tempo de Ciclo]]
