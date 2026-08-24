---
tipo: conceito
materias: [Estatistica2]
tags: [conceito, inferencia, teste]
---

# Estatística de Teste

## Definição

Medida de quantos erros-padrão o valor observado (média amostral, por exemplo) está distante do valor hipotético definido em [[Teste de hipotese|H0]]. Pode ser calculada como Z (quando σ populacional é conhecido, ou n grande) ou T (quando σ é desconhecido e n é pequeno, ver [[Distribuicao T de Student]]).

## Fórmula / aplicação

<pre>
Z = (valor observado − média) / desvio padrão

T = (X̄ − μ₀) / (S / √n)
</pre>

## Onde aparece nas aulas

```dataview
LIST
FROM [[Estatistica de teste]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Valor critico]]
- [[Valor-p]]
- [[Distribuicao T de Student]]
- [[Z de alfa sobre 2]]
- [[Erro padrao]]
