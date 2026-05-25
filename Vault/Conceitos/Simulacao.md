---
tipo: conceito
materias: [Estatistica]
tags: [conceito, metodo]
---

# Simulação

## Definição

Técnica de "brincar de Deus": fixa a população (que normalmente é desconhecida), sorteia muitas amostras dela, e observa empiricamente o comportamento das estatísticas amostrais. Usada quando a resolução analítica é difícil ou impossível.

## Quando usar

- Não dá pra resolver o problema por matemática direta.
- Quer verificar empiricamente um resultado teórico (ex: confirmar que `E(X̄) = μ` e `σ(X̄) = σ/√n`).
- Distribuição da população é complexa ou desconhecida e precisa de aproximação.

## Mecânica básica (Excel)

```excel
= ALEATÓRIO.ENTRE(1; N)   ← sorteia índice da população
= PROCV(índice; pop; 2)   ← pega valor correspondente
```

Repete pra cada elemento da amostra. Calcula X̄ da amostra. Replica em múltiplas linhas (cada linha = um "universo paralelo" = uma réplica). No final, observa esperança, desvio padrão e variância da coluna de X̄s.

`F9` reordena todos os sorteios e gera um novo conjunto de réplicas.

## Universos paralelos / réplicas

Metáfora pedagógica: cada réplica é como um universo paralelo onde uma versão sua sorteou uma amostra diferente da mesma população. Quanto mais réplicas, mais a estatística empírica converge pra estatística teórica.

- 600 réplicas no Excel: já bate aproximadamente com teoria.
- Milhões: bate rigorosamente. Recomenda Python (NumPy) ao invés de Excel.

## Diferencial profissional

Se não sabe resolver por matemática, simulação resolve. O professor enfatizou que é um diferencial: começar a usar simulação pra tudo, inclusive como verificação de resultados analíticos.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Distribuicao amostral da media]]
- [[Teorema do limite central]]
- [[Amostragem]]
- [[Media amostral]]
