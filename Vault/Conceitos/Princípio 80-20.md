---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, qualidade]
---

# Princípio 80-20

## Definição

Regra empírica que diz que aproximadamente 80% dos efeitos vêm de 20% das causas. É a base teórica do diagrama de [[Pareto]].

Exemplos de aplicação:
- 80% das perdas vêm de 20% dos produtos.
- 80% do lucro vem de 20% dos clientes.
- 80% dos bugs vêm de 20% do código.
- 80% das reclamações vêm de 20% das categorias.

Não é regra exata. Na prática pode dar 70-25, 75-30, 85-15. O importante é o conceito de **concentração desproporcional**.

## Fórmula / aplicação

Não tem fórmula fechada. O método é:
1. Listar todos os itens com seu valor (perda, receita, frequência).
2. Ordenar do maior para o menor.
3. Calcular a frequência percentual acumulada.
4. Identificar o ponto em que se atinge ~80% do total.
5. Os itens até esse ponto são os "vital few"; o resto são os "trivial many".

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Pareto]]
- [[Ishikawa]]
