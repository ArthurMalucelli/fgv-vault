---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, estimacao]
---

# Estimação por intervalo

## Definição

Forma de [[Inferencia estatistica|inferência]] em que você usa uma faixa de valores (não um número só) pra aproximar o [[Parametros populacionais|parâmetro populacional]], junto com um [[Nivel de Confianca|nível de confiança]] γ associado.

Realização concreta: o [[Intervalo de Confiança]] X̄ ± E.

## Por que é melhor que [[Estimacao por ponto|estimação por ponto]]

Quantifica a incerteza. Em vez de "μ ≈ 34,20", você diz "μ ∈ [24,20; 44,20] com 95% de confiança". Quem vai tomar decisão (montar franquia, alocar capital, definir política) precisa do range, não do número solto.

## Analogia: pesquisa eleitoral

"Candidato A com 30% dos votos, margem de 2 pontos pra cima ou pra baixo." Isso é uma estimação por intervalo pra **proporção** (não pra média). Mesma lógica que a aula desenvolveu pra μ vai aparecer daqui a duas aulas pra p.

## Componentes obrigatórios

Qualquer estimação por intervalo precisa de três coisas:
- Estatística amostral (X̄, p̂…)
- [[Margem de Erro]] (E)
- [[Nivel de Confianca]] (γ)

Sem o γ, o intervalo perde significado: faixa de quê?

## Onde aparece nas aulas

```dataview
LIST
FROM [[Estimacao por intervalo]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Intervalo de Confiança]]
- [[Estimacao por ponto]]
- [[Margem de Erro]]
- [[Nivel de Confianca]]
