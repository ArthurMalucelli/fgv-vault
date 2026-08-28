---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia]
---

# População

## Definição

Conjunto completo de elementos sobre os quais se quer tirar conclusões. Pode ser pessoas, cachorros, chamadas telefônicas, eventos, qualquer coisa.

A população é a entidade abstrata que tem [[Parametros populacionais|parâmetros]] (μ, σ², p) reais e fixos, geralmente desconhecidos.

## Por que não medir a população inteira

Em quase todo problema real, medir a população toda é inviável:
- Censo é caro e demorado
- A população pode ser teórica (ex: todas as chamadas que poderiam ser feitas no próximo mês)
- A medição pode ser destrutiva (ex: testar tempo de vida de lâmpadas até queimar)

Por isso a estatística existe: como inferir sobre algo que não dá pra medir todo, a partir de uma fração que dá.

## População vs amostra

| | População | Amostra |
|---|---|---|
| Tamanho | N (geralmente grande ou infinito) | n |
| Média | μ (parâmetro fixo desconhecido) | X̄ (estatística, varia) |
| Variância | σ² | s² |
| Acesso | quase nunca direto | direto |

## Onde aparece nas aulas

```dataview
LIST
FROM [[Populacao]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Amostragem]]
- [[Parametros populacionais]]
- [[Inferencia estatistica]]
