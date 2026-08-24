---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, intervalo]
---

# Margem de Erro

## Definição

Tamanho do "bracinho" para cada lado de X̄ num [[Intervalo de Confiança]]. Define a metade da largura do intervalo. Nelson chamou de "E" na aula (poderia ser "Ernesto" ou "Elefante").

<pre>
E = Z_(α/2) · σ / √n     ← σ populacional conhecido
</pre>

## Componentes

| Termo | O que controla |
|-------|----------------|
| [[Z de alfa sobre 2]] | Quão exigente é a confiança (γ alto → Z alto → E alto) |
| σ | Dispersão da [[Populacao|população]]. Você não controla |
| √n | [[Tamanho da amostra]]. Você controla pagando mais entrevistas |

## Sensibilidade

`E` é proporcional a `1/√n`. Pra cortar E pela metade, **n tem que quadruplicar**. Pra cortar em 10x, n tem que ser 100x maior.

É a relação que faz pesquisa precisa ser cara.

## Interpretação

E só faz sentido em relação à grandeza do que você está estimando:
- X̄ ≈ R$ 7, E = R$ 10 → margem maior que o próprio valor, ruim
- X̄ ≈ R$ 60, E = R$ 10 → ~17% do valor, razoável
- X̄ = 50.000 votos, E = 500 → 1%, ótimo

## Inverter pra dimensionar amostra

Quando o exercício pergunta "qual n eu preciso pra ter margem de erro tal?":

<pre>
n = (Z_(α/2) · σ / E)²
</pre>

Sempre arredonda pra cima (fetiche dos estatísticos pra garantir suficiência).

## Onde aparece nas aulas

```dataview
LIST
FROM [[Margem de Erro]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Intervalo de Confiança]]
- [[Z de alfa sobre 2]]
- [[Nivel de Confianca]]
- [[Tamanho da amostra]]
- [[Erro padrao]]
