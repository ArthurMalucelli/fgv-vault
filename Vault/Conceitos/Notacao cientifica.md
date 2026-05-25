---
tipo: conceito
materias: [Programacao, Estatistica]
tags: [conceito]
---

# Notacao cientifica

## Definição

Forma compacta de escrever números muito grandes ou muito pequenos como produto de uma mantissa por uma potência de 10. Em Python e Pandas, usa a sintaxe `XeY` que significa `X × 10^Y`.

## Fórmula / aplicação

```python
1e3   # 1.000          (mil)
1e6   # 1.000.000      (milhão)
1e9   # 1.000.000.000  (bilhão)
1e12  # 1 trilhão
2.5e6 # 2.500.000
1e-3  # 0.001          (um milésimo)
```

Equivalentes em código:

```python
1e6 == 10**6 == 1_000_000   # tudo True
```

Uso típico: dividir valores grandes para exibir em escala mais legível.

```python
df["patrimonio"].mean() / 1e9    # média em bilhões
df["receita"].sum() / 1e6        # soma em milhões
```

**Underscore em literal**: `10_000_000` é apenas separador visual. Python ignora os `_`. Equivale a `10000000` e a `1e7`.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Pandas]]
