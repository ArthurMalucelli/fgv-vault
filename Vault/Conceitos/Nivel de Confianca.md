---
tipo: conceito
materias: [Estatistica]
tags: [conceito, inferencia, intervalo]
---

# Nível de Confiança

## Definição

Probabilidade γ (gama) de que o procedimento de construção do [[Intervalo de Confiança]] resulte num intervalo que contenha o parâmetro populacional verdadeiro.

Equivalentemente: proporção da área central da distribuição amostral que vamos "aceitar" como cobertura do intervalo. Tipicamente 90%, 95% ou 99%.

## α e α/2

α é o complemento de γ: a chance do intervalo errar.

<pre>
α   = 1 − γ
α/2 = chance de errar pra cada lado
</pre>

α/2 entra na fórmula porque o intervalo é simétrico em torno de X̄: metade da chance de erro fica em cada cauda da [[Distribuicao normal|normal]].

## Valores típicos

| γ | α | α/2 | [[Z de alfa sobre 2]] |
|---|---|-----|---------|
| 90% | 10% | 5% | 1,645 |
| 95% | 5% | 2,5% | 1,96 |
| 99% | 1% | 0,5% | 2,58 |

Decora 1,96 e 1,645. O 2,58 puxa no Excel.

## Trade-off com [[Margem de Erro]]

Confiança e precisão são antagônicas (com n fixo):
- Subir γ → Z sobe → E aumenta (intervalo mais largo, perde precisão)
- Aceitar γ menor → Z cai → E diminui (intervalo mais estreito)

Pra recuperar precisão sem perder confiança, só aumentando n.

## Interpretação correta

**γ% se refere ao procedimento, não ao intervalo específico.**

Quando você fala "tenho 95% de confiança que μ ∈ [a, b]", está dizendo que **o método** com que construiu esse intervalo, se repetido em muitas amostras, acertaria 95% das vezes. O intervalo concreto que você tem em mãos ou contém o μ ou não contém — μ é fixo, não tem probabilidade.

## Onde aparece nas aulas

```dataview
LIST
FROM [[Nivel de Confianca]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Intervalo de Confiança]]
- [[Z de alfa sobre 2]]
- [[Margem de Erro]]
- [[Distribuicao normal]]
