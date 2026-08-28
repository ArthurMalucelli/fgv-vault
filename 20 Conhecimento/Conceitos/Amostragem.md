---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, amostragem]
---

# Amostragem

## Definição

Processo de selecionar um subconjunto (amostra) de uma [[Populacao|população]] pra extrair informação sobre ela. A qualidade da [[Inferencia estatistica|inferência]] depende diretamente de como a amostra foi obtida.

## Aleatória simples (com reposição)

Modelo padrão da disciplina. Cada elemento da população tem a mesma chance de ser sorteado, e o sorteio é feito com reposição (o mesmo elemento pode aparecer mais de uma vez).

Analogia da aula: notas no saco. Sorteia uma nota, anota, devolve, sorteia de novo. O saco "nunca acaba" porque tem reposição.

Com reposição garante:
- Independência entre observações
- Distribuição idêntica em cada extração (i.i.d.)

Esses dois requisitos são o que destrava as fórmulas E(X̄) = μ e Var(X̄) = σ²/n.

## Por que precisa ser aleatória

Sem aleatoriedade, a amostra pode estar viesada. Ex: se você pergunta altura só pra quem está no time de basquete, a média amostral vai estimar mal a média da FGV. Aleatoriedade é o que permite generalizar da amostra pra população.

## Tamanho da amostra (n)

Quanto maior n, menor o [[Erro padrao]]. Mas o ganho cai com √n: pra reduzir o erro pela metade, precisa quadruplicar a amostra. Esse é o limite prático que aparece em desenho de pesquisa.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Amostragem]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Inferencia estatistica]]
- [[Media amostral]]
- [[Distribuicao amostral da media]]
- [[Populacao]]
