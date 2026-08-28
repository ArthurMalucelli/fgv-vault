---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, amostragem]
---

# Tamanho da amostra

## Definição

n. Número de observações coletadas numa amostra. Variável central de design de pesquisa: controla custo, precisão e (via [[Teorema do limite central|TLC]]) validade das premissas de normalidade.

## Papel na fórmula do [[Intervalo de Confiança]]

n entra via √n no denominador da [[Margem de Erro|margem de erro]]:

<pre>
E = Z_(α/2) · σ / √n
</pre>

Quanto maior n, menor o E (intervalo mais estreito).

## Dimensionamento (fórmula inversa)

Dado um E alvo, qual n preciso?

<pre>
n = (Z_(α/2) · σ / E)²
</pre>

Sempre **arredonda pra cima** (convenção dos estatísticos pra garantir suficiência).

## A relação cruel: n ∝ 1/E²

Cortar a margem de erro pela metade exige **quadruplicar** o tamanho da amostra. Cortar em 10x exige 100x mais entrevistas. É o que faz pesquisa precisa ser cara.

Exemplo da aula: passar de E=10 pra E=5 (mesmas γ=95% e σ=100) levou n de 400 pra 1.537.

## Regra empírica n > 30

Pra invocar [[Teorema do limite central|TLC]] e tratar X̄ como normal (quando a população não é normal), precisa de **n > 30** (convenção, não teorema rigoroso). Abaixo disso, não pode usar essa abordagem se a distribuição original for desconhecida.

Por isso o Nelson exigiu n ≥ 40 nos trabalhos: garante que toda a maquinaria de IC vale.

## Trade-offs do design

Três alavancas, em trade-off duas a duas:

| Quero… | Custo |
|--------|-------|
| Diminuir E (mais precisão) | n sobe ao quadrado |
| Aumentar γ (mais confiança) | E aumenta, ou n sobe pra compensar |
| Diminuir n (menos custo) | Perde precisão (E sobe) ou confiança (γ cai) |

## Onde aparece nas aulas

```dataview
LIST
FROM [[Tamanho da amostra]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Intervalo de Confiança]]
- [[Margem de Erro]]
- [[Erro padrao]]
- [[Teorema do limite central]]
- [[Amostragem]]
