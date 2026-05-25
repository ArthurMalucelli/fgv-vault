---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, intervalo]
---

# Intervalo de Confiança

## Definição

Faixa de valores construída em torno de uma [[Estatistica amostral|estatística amostral]] (tipicamente X̄) que tem γ% de probabilidade de conter o parâmetro populacional desconhecido (tipicamente μ).

Forma geral pra a média, com σ populacional conhecido:

<pre>
IC_γ% = X̄ ± E
      = X̄ ± Z_(α/2) · σ / √n
</pre>

## Interpretação correta (vai cair)

**"95% dos intervalos construídos por esse procedimento contêm o μ verdadeiro."**

NÃO é: "tem 95% de chance do μ estar nesse intervalo específico". O μ é um parâmetro fixo, não tem distribuição. A aleatoriedade está na amostra, e portanto no intervalo.

## Lógica de construção (slide mais difícil da aula)

1. [[Distribuicao amostral da media|Distribuição amostral de X̄]] é normal (por suposição ou TLC)
2. 95% dos X̄ caem na faixa μ ± Z_(α/2)·σ_X̄
3. Logo, se você pôr um "bracinho" de tamanho E = Z_(α/2)·σ_X̄ em torno de qualquer X̄, ele alcança o μ em 95% dos casos
4. Quando X̄ cai dentro da faixa azul → o intervalo X̄ ± E inclui o μ
5. Quando X̄ cai fora (raro, 5%) → o intervalo perde o μ

## Os três pilares (γ, n, E)

Três alavancas, sempre em trade-off:

| Variável | Função | Trade-off |
|----------|--------|-----------|
| γ (confiança) | Probabilidade do procedimento acertar | Subir γ aumenta Z, logo E |
| n (tamanho amostra) | Custo da pesquisa | Subir n diminui E (∝ 1/√n) |
| E (precisão) | Largura do intervalo | Cortar E pela metade quadruplica n |

## Aplicação na pesquisa de mercado

Pesquisa eleitoral: "candidato A com 30%, margem de 2 pontos pra cima ou pra baixo, 95% de confiança". Aquela "margem" é justamente o E.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Intervalo de Confiança]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Margem de Erro]]
- [[Nivel de Confianca]]
- [[Z de alfa sobre 2]]
- [[Tamanho da amostra]]
- [[Estimacao por ponto]]
- [[Estimacao por intervalo]]
- [[Distribuicao amostral da media]]
- [[Erro padrao]]
- [[Media amostral]]
- [[Inferencia estatistica]]
