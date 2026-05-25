---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, operações, produção, logística]
---

# Gargalo

## Definição

Tarefa, estação ou recurso de uma linha de produção que tem o maior tempo de processamento e, portanto, restringe a máxima produção possível. Em logística e teoria das restrições, é tratado como o "constraint" do sistema.

A produção máxima da linha não pode passar do throughput do gargalo, independente da capacidade das outras estações.

Em alguns contextos é chamado de "cardápio" (terminologia que aparece na aula de logística do 3º semestre).

## Fórmula / aplicação

Cálculo de produção máxima usando o gargalo:

<pre>
Produção/hora = 60 / tempo da tarefa mais longa  (em minutos)
Produção/dia = (horas × 60) / tempo do gargalo
</pre>

Exemplo:
- Tarefa mais longa = F com 0,7 min.
- 60 / 0,7 ≈ 85,7 unidades por hora.
- Em 8 horas: ≈ 686 unidades por dia.

**Quando usar esse caminho curto:**
- Pergunta sobre **máxima produção** com número fixo de operadores.
- Não pede TC nem balanceamento detalhado.

Se a pergunta for sobre tempo de ciclo a partir de uma demanda, aí o caminho é completo: calcular [[Tempo de Ciclo]] → N teórico → balanceamento.

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
- [[Just-in-Time]]
- [[Lean]]
