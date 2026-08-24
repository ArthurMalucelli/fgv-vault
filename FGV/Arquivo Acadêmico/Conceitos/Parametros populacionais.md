---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia]
---

# Parâmetros populacionais

## Definição

Valores fixos que descrevem características de uma [[Populacao|população]]. São constantes da população, não variáveis aleatórias. Geralmente desconhecidos, são exatamente o que a [[Inferencia estatistica|inferência]] tenta estimar.

## Notação padrão

| Parâmetro | Símbolo | Estatística amostral correspondente |
|---|---|---|
| Média populacional | μ (mu) | X̄ |
| Variância populacional | σ² (sigma ao quadrado) | s² |
| Desvio padrão populacional | σ | s |
| Proporção populacional | p | p̂ |

Letras gregas pra parâmetros, letras latinas (com chapéu/barra) pra estatísticas. Convenção universal.

## Diferença chave em relação à estatística amostral

- **Parâmetro:** valor único, fixo, desconhecido. Ex: a média de altura da FGV é um número específico, mesmo que ninguém o conheça.
- **[[Estatistica amostral]]:** variável aleatória. Pega uma amostra, calcula X̄, dá um valor. Pega outra amostra, dá outro valor.

Por isso a gente pode fazer afirmações probabilísticas sobre estatísticas (P(X̄ < 1,71) faz sentido), mas não sobre parâmetros (P(μ < 1,71) é 0 ou 1, não faz sentido como probabilidade na visão frequentista).

## Onde aparece nas aulas

```dataview
LIST
FROM [[Parametros populacionais]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Populacao]]
- [[Estatistica amostral]]
- [[Inferencia estatistica]]
- [[Media amostral]]
