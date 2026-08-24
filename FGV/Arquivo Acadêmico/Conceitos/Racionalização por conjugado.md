---
tipo: conceito
materias: [MatemáticaAplicada]
tags: [conceito]
---

# Racionalização por conjugado

## Definição

Técnica pra resolver limites com indeterminação 0/0 quando há raiz na expressão: multiplica numerador e denominador pelo conjugado do termo com raiz (mesmo termo, sinal trocado), o que elimina a raiz via diferença de quadrados e permite cancelar o fator que gera a indeterminação.

Exemplo completo (exercício da aula de 08.06, reconstruído do slide):

```
lim(x→0) (√(x²+16) − 4)/x²                      direto: 0/0
× (√(x²+16) + 4)/(√(x²+16) + 4)
= (x²+16−16) / (x²·(√(x²+16)+4))
= 1/(√(x²+16)+4) = 1/8
```

## Fórmula / aplicação

Multiplicar por 1 na forma (conjugado)/(conjugado). Ex.: pra √a - b, o conjugado é √a + b, e (√a - b)(√a + b) = a - b².

## Onde aparece nas aulas

```dataview
LIST
FROM [[Racionalização por conjugado]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Limite (cálculo)]]
