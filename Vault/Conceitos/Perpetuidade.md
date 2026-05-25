---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, matematica-financeira]
---

# Perpetuidade

## Definição

Fluxo de caixa que se repete pra sempre. Conceito de matemática financeira usado em [[Valuation]] pra calcular [[Valor Terminal]] de empresas que se assume terão vida infinita.

## Fórmula / aplicação

**Perpetuidade simples (fluxo constante)**:

<pre>
VP = C / r
</pre>

Onde:
- `C` = fluxo de caixa constante por período
- `r` = taxa de desconto por período

**Perpetuidade com crescimento (Gordon)**:

<pre>
VP = C₁ / (r − g)
</pre>

Onde:
- `C₁` = primeiro fluxo de caixa
- `g` = taxa de crescimento perpétua (constante)
- Restrição: `r > g`, senão a fórmula explode

**Uso em ações**: [[Modelo de Gordon]] é exatamente uma perpetuidade com crescimento aplicada a dividendos.

```
P₀ = Div₁ / (R_E − g)
```

**Uso em DDM com horizonte explícito**: depois de N anos de projeção explícita, calcula-se o [[Valor Terminal]] como perpetuidade do dividendo do ano N+1 em diante.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Modelo de Gordon]]
- [[Valor Terminal]]
- [[DDM]]
