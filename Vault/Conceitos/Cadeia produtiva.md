---
tipo: conceito
materias: [IntroducaoAGestao, OperacoesParaCompetitividade]
tags: [conceito, operacoes]
---

# Cadeia produtiva

## Definição

Sequência encadeada de atividades e atores que transforma matéria-prima em produto/serviço final entregue ao consumidor. Vai do extrativismo/cultivo até a entrega no ponto de venda (e, em visão estendida, até o descarte).

Diferente de [[Ciclo de Vida do Produto]]: cadeia produtiva foca em **atores e fluxos** (quem faz o quê, quem entrega pra quem), enquanto ciclo de vida foca em **etapas físicas e impacto ambiental**. Os dois se sobrepõem, mas a pergunta é diferente.

## Estrutura típica

```
Fornecedor de insumos → Produtor de matéria-prima → Indústria de transformação
                     → Distribuidor → Varejista → Consumidor
                     → Pós-venda / descarte / reciclagem
```

Cada elo é uma empresa (ou conjunto de empresas) com poder de barganha, margem e contribuição ao impacto total.

## Por que mapear

- **Identificar gargalos:** elo mais lento limita o throughput total (lógica de [[Gargalo]] em operações)
- **Identificar dependência:** elo único = [[Key-person risk]] da cadeia
- **Identificar oportunidade de inovação:** onde dá pra cortar etapa, substituir insumo, mudar processo
- **Avaliar impacto ambiental e social:** cadeia é onde mora o impacto real, não só na fábrica final
- **Diagnosticar [[Greenwashing]]:** empresa "sustentável" com cadeia opaca tipicamente tem impacto escondido a montante

## Cadeia curta vs cadeia longa

- **Cadeia curta** = poucos intermediários (produtor → consumidor direto, feira, CSA). Mais transparência, menos margem perdida, mais resiliência local. Mas escala limitada.
- **Cadeia longa** = muitos elos. Escala global, custo unitário baixo, mas opacidade ambiental e social. Padrão da indústria de commodity e fast fashion.

Inovação sustentável muitas vezes encurta a cadeia (reduz intermediários, aproxima produtor e consumidor).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Ciclo de Vida do Produto]]
- [[Sustentabilidade]]
- [[Sistema Aberto]]
- [[Gargalo]]
- [[Greenwashing]]
- [[Just-in-Time]]
