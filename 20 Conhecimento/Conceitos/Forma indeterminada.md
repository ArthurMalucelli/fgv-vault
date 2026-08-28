---
tipo: conceito
materias: [MatemáticaAplicada]
tags: [conceito]
---

# Forma indeterminada

## Definição

Quando a substituição direta num limite dá 0/0: numerador e denominador tendem a zero juntos e a fração não pode ser calculada assim. Não é resposta (não é 0, nem 1, nem infinito): é sinal de que a expressão precisa ser simplificada antes de calcular o limite, por fatoração ou por [[Racionalização por conjugado]]. O limite pode perfeitamente existir: só o caminho da substituição que trava.

Atenção: 0/k com k ≠ 0 não é indeterminação, é simplesmente 0.

## Fórmula / aplicação

```
lim(x→1) (x−1)/(x²−1)     direto: 0/0
= lim(x→1) (x−1)/[(x+1)(x−1)] = lim(x→1) 1/(x+1) = 1/2
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[Forma indeterminada]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Limite (cálculo)]]
- [[Racionalização por conjugado]]
