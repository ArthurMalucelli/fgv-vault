---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste qui-quadrado de aderencia

## Definição

Testa se as contagens observadas de UMA variável categórica com k categorias seguem uma distribuição teórica (goodness-of-fit). H0: a distribuição observada segue a teórica (ex.: mix 45/35/20, ou uniforme 25% cada). H1: pelo menos uma proporção difere. Estatística compara observado com [[Frequencia esperada]] em cada categoria; distribuição [[Distribuicao qui-quadrado|qui-quadrado]] com gl = k − 1, sempre cauda direita.

## Fórmula / aplicação

<pre>
E_i = n × p_i          (esperada sob H0)
χ² = Σ (O_i − E_i)² / E_i
gl = k − 1             (k − c − 1 se c parâmetros foram estimados)
Rejeita se χ² > CHISQ.INV.RT(α, gl), ou valor-p = CHISQ.DIST.RT(χ², gl) < α

Excel: colunas O, p, E = p × n, (O−E)²/E; SUM; CHISQ.INV.RT; CHISQ.DIST.RT
       atalho: CHISQ.TEST(obs, esp) devolve só o valor-p
R:     chisq.test(x = obs, p = p_exp)     (sem p, assume proporções iguais)

Exemplo (aula 5): 100/60/40 vs 45/35/20, n = 200 → E = 90/70/40, χ² = 2,540, gl 2, crítico 5,991, p = 0,281: não rejeita.
</pre>

Condição: esperadas ≥ 5 na maioria das células.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste qui-quadrado de aderencia]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Teste de hipotese]]
- [[Distribuicao qui-quadrado]]
- [[Frequencia esperada]]
- [[Teste qui-quadrado de independencia]]
