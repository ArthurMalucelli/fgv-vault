---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste pareado

## Definição

Teste t aplicado às diferenças D = Depois − Antes medidas nas mesmas unidades (mesmas lojas, mesmas pessoas, antes e depois de uma intervenção). Vira um teste de uma média sobre D com μ_D = 0 em H0. Se as unidades são diferentes (dois grupos), não é pareado: é [[Teste t para duas amostras]].

## Fórmula / aplicação

<pre>
D_i = Depois_i − Antes_i
t = D̄ / (s_D / √n),   gl = n − 1
H1 típico: μ_D > 0 ("a campanha aumentou?"), cauda direita

Excel: coluna D = B − A, depois o bloco de uma média (AVERAGE, STDEV.S, T.INV, T.DIST.RT)
       atalho: T.TEST(depois, antes, caudas, 1)   (tipo 1 = pareado; caudas=1 devolve a cauda de |t|)
R:     t.test(depois, antes, paired = TRUE, alternative = "greater")
       IC 95% de mu_D: t.test(depois, antes, paired = TRUE)$conf.int

Reportar junto: tamanho do efeito (D̄) e IC de μ_D.
</pre>

Atenção ao sinal de D: se D = Antes − Depois, a cauda de H1 inverte.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste pareado]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Distribuicao T de Student]]
- [[Teste t para duas amostras]]
- [[Intervalo de Confiança]]
