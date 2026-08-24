---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, qualidade, ferramenta]
---

# Pareto

## Definição

Diagrama (gráfico) que combina barras de frequência com linha de frequência acumulada, usado pra identificar quais poucos itens (causas, produtos, defeitos) concentram a maior parte do impacto. Nome vem do economista italiano Vilfredo Pareto, que observou que 80% da riqueza estava com 20% da população.

Aplicações típicas: análise de perdas (quais produtos geram mais perda), análise de receita (quais clientes geram mais lucro), análise de defeitos (quais causas geram mais reclamação).

## Fórmula / aplicação

Construção em 7 passos no Excel:

1. Tabela dinâmica com a categoria em Linhas e a contagem em Valores.
2. Copiar resultado para área limpa.
3. Ordenar do maior para o menor (Z para A).
4. Frequência % = freq / total × 100. Total como referência absoluta (F4).
5. Frequência % acumulada: primeira linha = primeira freq%. Depois = anterior + atual.
6. Selecionar categoria + frequência + (Ctrl) frequência acumulada.
7. Inserir → Gráficos Recomendados → Combinação (última opção). Adicionar rótulos de dados.

A linha sempre termina em 100%. Cada ponto indica o acumulado das categorias até ali.

Combina com [[Ishikawa]]: Ishikawa lista as causas qualitativamente, Pareto prioriza quantitativamente. Em seguida, [[5W2H]] planeja a ação corretiva.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Princípio 80-20]]
- [[Ishikawa]]
- [[5W2H]]
- [[PDCA]]
