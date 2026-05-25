---
tipo: conceito
materias: [ComportamentoDoConsumidor]
tags: [conceito]
---

# Modelo de Fishbein

## Definição

Modelo compensatório de tomada de decisão do consumidor. Soma ponderada das avaliações que o consumidor faz de uma marca em cada atributo relevante da categoria. A marca com a maior soma é a escolhida.

É chamado de **compensatório** porque uma nota baixa em um atributo pode ser compensada por uma nota alta em outro.

## Fórmula / aplicação

```
Atitude(marca) = Σ (peso_i × nota_i)
```

`peso_i` = importância do atributo i (escala 0-10), o quanto aquele atributo pesa pra o consumidor da categoria
`nota_i` = avaliação que o consumidor dá pra marca naquele atributo (escala 0-10)

Para construir o modelo:
1. Definir o setor/categoria (ex: chocolate fino, ou melhor, presente)
2. Listar marcas no [[Conjunto de consideração]]
3. Levantar os atributos relevantes via pesquisa qualitativa
4. Calcular o peso de cada atributo (importância pro consumidor)
5. Coletar notas via [[Pesquisa de mercado]] com consumidores que efetivamente consumiram a marca
6. Calcular a soma ponderada por marca

Para que serve na prática (marketing): comunicar de forma direcionada. A marca enfatiza os atributos onde ganha, não onde perde. Nem sempre o consumidor escolhe pela soma maior, escolhe pela coincidência com o atributo que ele valoriza.

Atributos têm que ser **específicos**. "Qualidade" sozinho não é atributo válido (genérico demais). No caso de chocolate, vira doçura, intensidade, quanto é artesanal. Em cerveja, teor alcoólico, tipo, amargor. **Percepção de qualidade** (hierarquia mental entre marcas) é diferente de qualidade e pode entrar como atributo.

Visualização do modelo: [[Mapa perceptual]].

Contrasta com [[Regra não compensatória]] (atalhos: primeiro do Mercado Livre, fila menor, distribuição física).

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Atitudes]]
- [[Conjunto evocado]]
- [[Conjunto de consideração]]
- [[Modelo AIDA]]
- [[Mapa perceptual]]
- [[Regra compensatória]]
- [[Regra não compensatória]]
- [[Pesquisa top of mind]]
- [[Pesquisa de mercado]]
