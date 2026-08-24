---
tipo: conceito
materias: [MatemáticaAplicada]
tags: [conceito]
---

# Derivada

## Definição

Taxa de variação instantânea de uma função num ponto: o coeficiente angular da [[Reta Tangente]] ao gráfico nesse ponto. É o limite da [[Taxa de Variação Média]] quando o intervalo encolhe a zero. Analogia da aula: o radar tira fotos cada vez mais próximas e a variação média vira velocidade instantânea.

## Fórmula / aplicação

```
f'(a) = lim(x→a) [f(x) − f(a)] / (x − a)
f'(a) = lim(h→0) [f(a+h) − f(a)] / h
```

Trocando o ponto fixo a por x genérico, f'(x) vira função: a inclinação da tangente em cada ponto. Cálculo pela definição: expandir, cancelar constantes, fatorar o h, cortar, avaliar em h = 0.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Reta Tangente]]
- [[Taxa de Variação Média]]
- [[Limite (cálculo)]]
