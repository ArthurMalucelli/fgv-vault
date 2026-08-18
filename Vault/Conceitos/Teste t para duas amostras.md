---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste t para duas amostras

## Definição

Compara as médias de dois grupos formados por unidades diferentes (clientes da loja A vs clientes da loja B, turma A vs turma B). H0: μ_A = μ_B. A versão padrão é a de Welch, que não supõe variâncias iguais; a versão pooled (variâncias iguais) existe, mas não é o default. Se as mesmas unidades foram medidas duas vezes, o teste certo é o [[Teste pareado]].

## Fórmula / aplicação

<pre>
EP = √( s²_A/n_A + s²_B/n_B )
t  = (x̄_A − x̄_B) / EP
gl de Welch = EP⁴ / [ (s²_A/n_A)²/(n_A − 1) + (s²_B/n_B)²/(n_B − 1) ]   (não é n_A + n_B − 2)

Excel: fórmula acima em células + T.INV.2T(α, gl) e T.DIST.2T(ABS(t), gl)
       atalho: T.TEST(A, B, 2, 3)   (2 caudas, tipo 3 = variâncias diferentes; tipo 2 = iguais)
       Excel trunca gl não inteiro em T.DIST/T.INV; T.TEST usa o gl fracionário
R:     t.test(A, B)                    (Welch é o default)
       t.test(A, B, var.equal = TRUE)  (pooled, só pra saber que existe)
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste t para duas amostras]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Teste pareado]]
- [[Distribuicao T de Student]]
- [[Graus de liberdade]]
- [[Erro padrao]]
