---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, estimacao]
---

# Estimação por ponto

## Definição

Forma de [[Inferencia estatistica|inferência]] em que você usa uma única estatística amostral pra aproximar o [[Parametros populacionais|parâmetro populacional]] correspondente.

Exemplos:
- X̄ → estimativa de μ
- S → estimativa de σ
- p̂ → estimativa de p (proporção)

## Limitação

Diz "μ deve ser parecido com X̄", mas não quantifica o **grau de incerteza**. Quanto parecido? Quão errado pode estar? Pra responder isso, precisa de [[Estimacao por intervalo|estimação por intervalo]].

Estimar a idade média de uma população como 19,4 anos é uma estimativa por ponto. Não diz se o verdadeiro μ provavelmente está entre 19 e 20, ou entre 17 e 22.

## Contraponto com estimação por intervalo

| Característica | Por ponto | [[Estimacao por intervalo|Por intervalo]] |
|---|---|---|
| Output | Um número | Faixa [a, b] |
| Quantifica incerteza? | Não | Sim, via γ |
| Útil pra decisão? | Limitado | Sim |
| Exemplo | "X̄ = 34,20" | "μ ∈ [24,20; 44,20] com γ=95%" |

## Onde aparece nas aulas

```dataview
LIST
FROM [[Estimacao por ponto]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Estimacao por intervalo]]
- [[Intervalo de Confiança]]
- [[Media amostral]]
- [[Estatistica amostral]]
- [[Parametros populacionais]]
