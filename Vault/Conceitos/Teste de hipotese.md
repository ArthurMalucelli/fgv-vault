---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Teste de Hipótese

## Definição

Procedimento pra avaliar se os dados de uma amostra dão evidência suficiente pra rejeitar, ou não, uma afirmação inicial sobre a população.

- **H0 (hipótese nula)**: a afirmação inicial, presumida verdadeira até prova em contrário (analogia: réu inocente até se provar culpado).
- **H1 (hipótese alternativa)**: o que se quer verificar se há evidência pra sustentar.

Nunca se afirma com certeza que H0 é falsa ou verdadeira: a decisão é probabilística, tomada com um grau de confiança (tipicamente 95%), porque sempre existe uma chance de a amostra não representar bem a população.

## Fórmula / aplicação

Roteiro fixo pra resolver qualquer exercício:

<pre>
1. Definir H0 e H1
2. Definir alfa (nível de significância)
3. Calcular a [[Estatistica de teste]] (Z ou T)
4. Achar o [[Valor critico]] ou o [[Valor-p]]
5. Comparar e decidir: rejeita ou não rejeita H0
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Teste de hipotese]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Estatistica de teste]]
- [[Valor-p]]
- [[Valor critico]]
- [[Erro Tipo I]]
- [[Erro Tipo II]]
- [[Regiao de rejeicao]]
- [[Nivel de Confianca]]
- [[Intervalo de Confiança]]
