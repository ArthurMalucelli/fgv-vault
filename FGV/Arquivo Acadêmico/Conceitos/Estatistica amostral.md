---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia]
---

# Estatística amostral

## Definição

Função dos dados de uma amostra. Como a amostra é aleatória (vem de [[Amostragem]] aleatória), qualquer função dela também é aleatória. Estatística amostral é, então, uma variável aleatória.

Sinônimos comuns: estimador (quando a estatística é usada pra estimar um [[Parametros populacionais|parâmetro]]).

## Estatísticas mais usadas

| Estatística | Notação | Estima |
|---|---|---|
| [[Media amostral]] | X̄ ("X-barra" ou "X-chapéu") | μ |
| Variância amostral | s² | σ² |
| Desvio padrão amostral | s | σ |
| Proporção amostral | p̂ ("p-chapéu") | p |

## Notação chapéu/barra

Convenção: a barra (X̄) ou o chapéu (p̂) sinaliza que aquele valor é calculado a partir de uma amostra, não é o parâmetro real. Em inglês "hat", em português a gente fala "chapéu". Exemplo: X-chapéu, p-chapéu.

## Estatística é variável aleatória

Esse é o conceito central. Toda estatística tem distribuição (chamada [[Distribuicao amostral da media|distribuição amostral]] no caso de X̄), tem [[Valor esperado|esperança]] e tem variância. O desvio padrão de uma estatística amostral tem nome próprio: [[Erro padrao]].

## Estimador não-viesado

Uma estatística é não-viesada pra um parâmetro se, em média, ela acerta:

```
E(estatística) = parâmetro
```

X̄ é não-viesado pra μ porque E(X̄) = μ. Essa é uma boa propriedade desejável de um estimador.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Estatistica amostral]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Parametros populacionais]]
- [[Media amostral]]
- [[Distribuicao amostral da media]]
- [[Erro padrao]]
- [[Inferencia estatistica]]
