---
tipo: conceito
materias: [ProdutosFinanceiros]
tags: [conceito, finanças, câmbio, derivativos]
---

# Forward (Contrato a Termo)

## Definição

Contrato bilateral que fixa hoje (D+0) o preço de uma transação que será liquidada em data futura (D+N). Derivativo de **primeira geração**. No câmbio, costuma ser chamado de **NDF** (Non-Deliverable Forward) por liquidar apenas a diferença, sem entrega física.

## Características

- **Mercado**: balcão (OTC), não bolsa.
- **Customização**: alto nível de detalhe (datas, valores, indexadores).
- **Liquidação**: só no vencimento, sem ajuste diário.
- **Liquidez**: baixa (não tem padronização).
- **Risco**: contraparte (credit risk).

## Fluxo financeiro no vencimento T

```
Fluxo = P_T (spot na liquidação) − P_t (preço acordado no contrato)
```
Se positivo, credita ao comprador; se negativo, debita.

## Spot vs Forward

| | Negociação | Liquidação |
|---|---|---|
| Spot | D+0 | D+0 ou D+2 |
| Forward | D+0 | D+N |

## Caso de uso típico

Importador que paga US$ 1M em 30 dias mas só recebe os reais na data do pagamento. Trava cotação hoje via forward (~5,43 BRL/USD com spot a 5,39) e elimina risco cambial.

## Vantagens vs Desvantagens

| Vantagens | Desvantagens |
|---|---|
| Customizado | Iliquidez |
| Sem chamadas de margem | Pouca transparência |
| Baixo custo operacional | Risco de crédito |

## Conceitos relacionados

- [[IRP]]
- [[Carry Trade]]
- [[Cotação Direta]]
- [[Ptax]]
