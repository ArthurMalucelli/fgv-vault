---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia]
---

# Inferência estatística

## Definição

Conjunto de técnicas pra tirar conclusões sobre uma população a partir de uma [[Amostragem|amostra]]. É o terceiro grande bloco do curso, depois de probabilidade e variáveis aleatórias.

A premissa: você normalmente não tem acesso à [[Populacao|população]] inteira. Quer saber a altura média de todos os alunos da FGV, mas não consegue medir todos. Então mede uma amostra e infere o que pode sobre a população.

## Estrutura

A inferência se divide em três grandes problemas:

1. **Estimação pontual.** Dar um único número como melhor chute pro parâmetro. Ex: X̄ como estimador de μ.
2. **Estimação por intervalo.** Dar uma faixa com nível de confiança associado. Ex: intervalo de confiança de 95%.
3. **Teste de hipótese.** Decidir entre duas afirmações sobre a população (H₀ vs H₁) com base nos dados amostrais.

Os três usam o mesmo arcabouço de [[Distribuicao amostral da media|distribuição amostral]].

## Parâmetro vs estatística

| Conceito | População | Amostra |
|---|---|---|
| Média | μ (parâmetro) | X̄ (estatística) |
| Variância | σ² | s² |
| Proporção | p | p̂ |

[[Parametros populacionais]] são fixos e (geralmente) desconhecidos. [[Estatistica amostral|Estatísticas amostrais]] são variáveis aleatórias, mudam de amostra pra amostra.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Inferencia estatistica]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Amostragem]]
- [[Parametros populacionais]]
- [[Estatistica amostral]]
- [[Media amostral]]
- [[Distribuicao amostral da media]]
- [[Erro padrao]]
