---
tipo: conceito
materias: [ComportamentoDoConsumidor]
tags: [conceito, marketing, segmentacao]
---

# Persona

## Definição

Representação semi-fictícia do consumidor-alvo, construída a partir de dados reais de pesquisa. Sintetiza características demográficas, comportamentais, motivações e dores de um segmento em um perfil único e tangível, que serve de referência pra decisões de produto, marketing e comunicação.

## Diferença pra público-alvo

| Conceito | Granularidade | Exemplo |
|---|---|---|
| Público-alvo | Demográfico amplo | Jovens 17-24, alta renda, faculdade privada SP |
| Persona | Indivíduo representativo com nome, hábitos, dores | "Mariana, 19, estudante FGV, descobre marcas pelo Instagram, valoriza artesanal" |

Público-alvo segmenta. Persona dá rosto.

## Como construir

Input: [[Entrevista em profundidade]] com pessoas dentro do público-alvo, [[Mapa de Empatia]] consolidado.

Saída: ficha com nome fictício, idade, ocupação, canais de descoberta, dores principais, motivações, gatilhos de compra.

## Onde aparece nas aulas

```dataview
LIST
FROM "ComportamentoDoConsumidor"
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Design Thinking]]
- [[Mapa de Empatia]]
- [[Entrevista em profundidade]]
