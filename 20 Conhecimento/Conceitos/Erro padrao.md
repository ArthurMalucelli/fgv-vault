---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia]
---

# Erro padrão

## Definição

Desvio padrão de uma [[Estatistica amostral]]. Mede a variabilidade da estatística entre amostras diferentes da mesma população.

Importante: erro padrão **não é** o desvio padrão da variável original, e **não é** o desvio padrão calculado dentro de uma amostra. É uma terceira coisa, que mede o quanto X̄ flutua se você pudesse repetir a amostragem várias vezes.

## Caso da [[Media amostral|média amostral]]

```
DP(X̄) = σ / √n
```

Onde σ é o desvio padrão populacional e n é o tamanho da amostra.

## Hierarquia dos "desvios padrão"

Esse é o ponto onde a maioria erra na prova. Distinguir três coisas:

<pre>
σ        ← DP populacional (dispersão dos indivíduos da população)
σ/√n     ← erro padrão (DP de X̄ entre amostras)
s        ← DP amostral (calculado em UMA amostra concreta)
</pre>

- σ é parâmetro fixo (não muda).
- σ/√n é parâmetro derivado, depende de n.
- s é estatística (varia de amostra pra amostra).

## Por que cai com √n, não com n

Porque Var(X̄) = σ²/n cai com n, mas DP é raiz da variância:

<pre>
DP(X̄) = √(σ²/n) = σ/√n
</pre>

Consequência prática: pra reduzir o erro padrão pela metade, precisa **quadruplicar** a amostra. Pra reduzir 10 vezes, precisa amostra 100 vezes maior. O retorno marginal de aumentar n é decrescente.

## Quando σ é desconhecido

Em quase todo problema real, você não conhece σ. Aí você troca por s (desvio padrão amostral) e o erro padrão estimado vira:

```
EP estimado = s / √n
```

Isso introduz uma camada extra de incerteza, e por isso entra a distribuição t de Student no lugar da normal (vem em aulas posteriores).

## Onde aparece nas aulas

```dataview
LIST
FROM [[Erro padrao]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Media amostral]]
- [[Distribuicao amostral da media]]
- [[Variancia e desvio padrao]]
- [[Estatistica amostral]]
