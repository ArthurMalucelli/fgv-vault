---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, valuation, renda-variavel]
---

# Modelo de Gordon

## Definição

Simplificação do [[DDM]] em que se assume que o [[Dividendos|dividendo]] cresce a uma taxa constante g pra sempre. Reduz a fórmula somatória do DDM a uma expressão fechada de três variáveis: dividendo, taxa de desconto e taxa de crescimento.

// preencher detalhes específicos na aula de 25.05.2026

## Fórmula / aplicação

<pre>
P₀ = Div₁ / (R_E − g)
</pre>

Onde:
- `Div₁` = próximo dividendo esperado (não o atual)
- `R_E` = retorno esperado / custo de capital próprio
- `g` = taxa de crescimento perpétua do dividendo

**Premissas**:
- g constante pra sempre (limitação forte)
- R_E > g (senão a fórmula explode pra infinito)
- Empresa não acaba

**Usos típicos**:
- Cálculo de [[Valor Terminal]] dentro de um DDM por múltiplos períodos
- Valuation rápido de empresas maduras com pagamento estável de dividendo

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[DDM]]
- [[Perpetuidade]]
- [[Valor Terminal]]
- [[Dividendos]]
