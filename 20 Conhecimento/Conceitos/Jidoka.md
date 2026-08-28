---
tipo: conceito
materias: [OperacoesParaCompetitividade]
tags: [conceito, lean]
---

# Jidoka

## Definicao

**"Qualidade construida a partir do processo"**. Um dos dois pilares da [[Casa do Lean]] (o outro e [[Just-in-Time]]). Significa que o processo tem a capacidade de **detectar anormalidade e parar sozinho**, em vez de seguir produzindo defeito.

## Tres componentes

1. **Separacao homem-maquina** — a maquina nao precisa do operador olhando o tempo todo; o operador so e chamado quando ha problema.
2. **Identificacao de anormalidades** — sensores ou logica detectam que algo saiu do padrao.
3. **[[Poka Yoke]]** — dispositivos a prova de erro que impedem fisicamente que o defeito ocorra ou passe adiante.

## Aplicacao em servicos

Em servico digital (TikTok, atendimento, software), Jidoka aparece como:
- Score de confianca da IA que segrega caso facil (decisao automatica) de caso ambiguo (revisao humana).
- Alertas automaticos quando metrica sai do baseline.
- Validacoes em formulario que impedem submissao com dado invalido.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Casa do Lean]]
- [[Just-in-Time]]
- [[Poka Yoke]]
- [[Pensamento Enxuto]]
