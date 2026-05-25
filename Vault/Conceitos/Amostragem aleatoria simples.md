---
tipo: conceito
materias: [Estatistica]
tags: [conceito, amostragem]
---

# Amostragem aleatória simples

## Definição

Procedimento de amostragem em que **cada elemento da [[Populacao|população]] tem a mesma probabilidade de ser selecionado** para a amostra, e cada seleção é independente das outras.

É o caso "ideal" pra inferência estatística: garante representatividade no sentido probabilístico, e é a suposição que sustenta as fórmulas de [[Intervalo de Confiança|IC]] e testes de hipótese.

## Por que importa

Os ICs e testes assumem que a [[Media amostral|média amostral]] X̄ tem distribuição conhecida (normal, ou aproximadamente normal por [[Teorema do limite central|TLC]]). **Essa distribuição só faz sentido se a amostra for aleatória simples.** Se não for, X̄ pode estar enviesado, e o IC não estima o μ verdadeiro, estima o μ de um subgrupo qualquer.

## Exemplos do Nelson (o que NÃO é amostragem aleatória)

- **Pegar só os amigos que moram perto do trabalho** pra estimar tempo médio de deslocamento dos paulistanos. Resultado: X̄ vai ser bem menor que o μ real, porque os amigos não representam a população.
- **Pesquisa só com quem entra na loja às 14h numa terça-feira**. Não representa o cliente médio.
- **Sortear "quem aparecer primeiro" na lista**, que pode estar ordenada por algum critério escondido (por exemplo, alfabético favorecendo nomes do início).

## Como obter na prática

Idealmente: sortear uniformemente da população inteira. Na prática (cidade de SP, por exemplo), é caro e difícil. Aproximações usadas:

- **Amostragem sistemática**: sortear o primeiro, depois pegar de k em k.
- **Amostragem estratificada**: dividir a população em estratos (idade, bairro), sortear dentro de cada um.
- **Amostragem por conveniência**: pegar quem tá disponível. **NÃO é aleatória**, mas usada como aproximação por falta de verba.

Em trabalhos de FGV, vocês normalmente usam aproximações por conveniência, então o IC vale com ressalva.

## Suposição implícita em todo IC

| Para um IC ser válido, precisa: |
|---|
| 1. [[Media amostral|X̄]] ter distribuição normal (X normal OU n > 30 por TLC) |
| 2. Amostra ser **aleatória simples** (ou aproximação razoável) |

Se uma das duas quebra, o IC não significa o que diz que significa.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Amostragem aleatoria simples]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Amostragem]]
- [[Populacao]]
- [[Tamanho da amostra]]
- [[Intervalo de Confiança]]
- [[Teorema do limite central]]
- [[Inferencia estatistica]]
- [[Pesquisa de mercado]]
