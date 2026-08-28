---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste qui-quadrado de independencia

## Definição

Testa se DUAS variáveis categóricas cruzadas numa tabela de contingência r × c são independentes (a proporção de uma não muda conforme a outra). H0: independentes ([[Independencia]] no sentido probabilístico). H1: existe associação. Mesma conta serve pra homogeneidade (mesma distribuição em populações diferentes); muda só a pergunta.

## Fórmula / aplicação

<pre>
E_ij = (total da linha i × total da coluna j) / n
χ² = ΣΣ (O_ij − E_ij)² / E_ij
gl = (r − 1)(c − 1)
Resíduo de cada célula: (O − E)/√E   (sinal e tamanho dizem qual célula puxa o χ²)

Excel: matriz E com referências absolutas ($D4*B$7/$D$7), matriz (O−E)²/E, SUM,
       CHISQ.INV.RT(α, gl), CHISQ.DIST.RT(χ², gl); atalho CHISQ.TEST(obs, esp)
R:     tab <- matrix(c(...), nrow = r, byrow = TRUE); dimnames(tab) <- list(...)
       res <- chisq.test(tab); res$expected; res$residuals; prop.table(tab, 1)

Exemplo (aula 5): canal × compra 3×2, n = 320 → χ² = 13,694, gl 2, p = 0,0011: rejeita.
Search compra 50%, Email 40%, Social 25%.
</pre>

Condição: esperadas ≥ 5. Se falhar, o R avisa "Chi-squared approximation may be incorrect": juntar categorias ou teste exato de Fisher (2 × 2).

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste qui-quadrado de independencia]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Distribuicao qui-quadrado]]
- [[Frequencia esperada]]
- [[Teste qui-quadrado de aderencia]]
- [[Independencia]]
