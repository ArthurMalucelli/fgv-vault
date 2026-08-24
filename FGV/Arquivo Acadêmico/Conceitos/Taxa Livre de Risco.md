---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, risco, valuation]
---

# Taxa Livre de Risco

## Definição

Retorno teórico de um ativo sem risco de calote. Serve como piso/baseline pra todas as taxas de desconto: qualquer ativo arriscado precisa pagar essa taxa **mais** um [[Premio de Risco|prêmio de risco]].

## Fórmula / aplicação

Não tem fórmula. É a taxa observada em ativos considerados livres de risco.

**Proxies usadas na prática**:
- **Brasil**: [[Selic]] (taxa do BACEN), [[CDI]] (próximo da Selic), título público (LFT/LTN/NTN-B/NTN-F dependendo do prazo)
- **EUA**: Treasury Bills (curto prazo), Treasury Bonds (longo prazo)

**Uso central**:
- Em [[DDM]]/DCF: compõe a taxa de desconto junto com prêmio de risco
- Em [[CAPM]]: é o R_f da fórmula `R_E = R_f + β × (R_m − R_f)`
- Em [[WACC]]: insumo pra calcular custo de capital próprio
- Comparar com retorno de qualquer ativo arriscado pra decidir se vale a pena o risco extra

**Cuidado**: em períodos de juros altos no Brasil (como Selic em 13-15%), a taxa livre de risco vira "concorrente" das ações, porque o investidor pode ganhar bastante em renda fixa sem risco. Isso pressiona preços de ação pra baixo.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Premio de Risco]]
- [[SELIC]]
- [[CDI]]
- [[CAPM]]
