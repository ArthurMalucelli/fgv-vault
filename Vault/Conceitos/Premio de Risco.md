---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, risco, valuation]
---

# Prêmio de Risco

## Definição

Retorno adicional que um investidor exige acima da [[Taxa Livre de Risco]] pra investir em um ativo com risco. Compensa a incerteza do fluxo de caixa esperado.

## Fórmula / aplicação

Em geral:

<pre>
Retorno exigido = Taxa Livre de Risco + Prêmio de Risco
</pre>

**Tipos de prêmio**:
- **Prêmio de risco de crédito**: cobrado em renda fixa privada (ex: CDB de banco médio paga mais que CDB de banco grande, que paga mais que título público).
- **Prêmio de risco de mercado** (`R_m − R_f`): cobrado em ações em geral. É um dos componentes do [[CAPM]].
- **Prêmio específico da empresa**: parte do prêmio que vem do risco daquela empresa especificamente (capturado via beta no CAPM).

**Em ações**: o prêmio de risco varia com:
- Volatilidade do dividendo (empresa cíclica → prêmio maior)
- Estrutura de capital (mais dívida → mais risco)
- Setor, geografia, governança

**Insight da aula**: no [[DDM]], a taxa de desconto NÃO pode ser a taxa livre de risco. Tem que incorporar prêmio de risco, porque o dividendo esperado é uma expectativa, não uma certeza.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Taxa Livre de Risco]]
- [[CAPM]]
- [[Retorno Esperado]]
- [[WACC]]
