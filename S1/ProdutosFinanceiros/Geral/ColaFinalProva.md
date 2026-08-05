---
materia: ProdutosFinanceiros
tipo: cola
tema: Revisão final prova (pós-parcial)
data: 2026-06-09
tags: [cola, prova, revisao]
---

# Cola Final — Produtos Financeiros

## 1. As 7 armadilhas que te pegaram hoje (decora essas, é onde você perde ponto)

1. **O "-1" é a liquidação D+1, não uma regra do título.**
   - Enunciado não fala de liquidação → assume D+1 → faz o -1 (ou conta a partir do dia seguinte).
   - "Liquidação = compra" / "mesmo dia" → **SEM -1**.
   - Dias úteis já dados no enunciado → usa o número cru, não mexe.
   - DIATRABALHOTOTAL sem a lista de feriados (3º argumento) conta feriado como dia útil. Sempre bota os feriados.

2. **Nominal divide, efetiva faz raiz.**
   - "Nominal X% a.a." → taxa do período = X/m (÷2 semestre, ÷12 mês).
   - "Efetiva X% a.a." → taxa do período = (1+X)^(1/m) − 1.
   - O cupom em R$ **sempre** divide por m (é pagamento, não taxa).

3. **Cupom da NTN-F = R$ 48,8088, não R$ 50.** É 10% efetivo: (1,10)^0,5 − 1 = 4,8809% × 1000. Não divide 10/2.

4. **Atingir Meta sempre faz o preço bater** (é o alvo que você fixou). Preço fechando não valida nada. Confere fluxos e prazos ANTES de confiar na taxa que sai.

5. **A taxa de desconto tem que estar na mesma unidade do período.** Fluxo semestral com taxa anual = desconta o dobro. Semestre → taxa de semestre.

6. **Fisher: acha o grandão (nominal) multiplicando, acha uma peça (real/inflação) dividindo.** Real e inflação no mesmo prazo.

7. **Confere o número que copia do enunciado.** Um dígito trocado (76.988 vs 76.998) contamina o resultado todo.

## 2. Fórmulas-núcleo por bloco

**Inflação / Fisher**
- Acumular: ∏(1+π) − 1 (multiplica, nunca soma)
- Anualizar: (1+taxa)^(252/n) − 1 ou (12/n) — eleva, não multiplica
- Fisher: (1+i) = (1+π)(1+r). Nominal = (1+r)(1+π)−1 ; Real = (1+i)/(1+π)−1
- IPCA+x%: o x é o juro real; nominal sai por Fisher

**LTN** (cupom zero)
- Preço: P = 1000/(1+i)^(du/252)
- YTM dado preço: (1000/P)^(252/du) − 1
- Sempre deságio (P < 1000). Nunca prêmio.

**NTN-F** (cupom semestral R$ 48,8088)
- P = Σ 48,81/(1+i)^(du_k/252) + 1000/(1+i)^(du_N/252)
- Cupons em 01/01 e 01/07, espaçados ~126 d.u. Conta pra trás a partir do vencimento.
- Último fluxo = cupom + principal. YTM dado preço → Atingir Meta.
- Cupom (10%) > YTM → ágio ; cupom < YTM → deságio.
- Sistema "americano" = bullet = mesma coisa (juros no caminho, principal no fim).

**SELIC / DI / CDB**
- Anual → diária: (1+i)^(1/252) − 1
- %CDI incide na taxa DIÁRIA: i_CDB_dia = %CDI × i_DI_dia, depois (1+i_CDB)^n
- CDI varia entre períodos → encadeia fatores (∏)
- Forward (Selic precificada): [fator_longo / fator_curto]^(252/du_trecho) − 1, onde fator = (1+i)^(du/252)
- Tributação RF (sobre o ganho): ≤180dc 22,5% | 181-360 20% | 361-720 17,5% | >720 15%

**Câmbio**
- Cotação direta sobe → moeda local DESVALORIZA
- IRP: F/S = (1+r_quote)/(1+r_base) na cotação quote/base
- PPP: S_new = S_old × (1+π_local)/(1+π_estrangeira)

**Ações (DDM / Gordon)**
- 1 período: P0 = (Div1 + P1)/(1+R_E)
- Retorno = Div1/P0 (dividend yield) + (P1−P0)/P0 (ganho de capital)
- Gordon: P0 = Div1/(R_E − g)
- Valor terminal = D/(R_perp − g): dá o valor NO ANO anterior ao 1º fluxo da perpetuidade
- Multiestágio com taxas diferentes: cada fluxo desconta pela taxa da fase que ele atravessa. O valor terminal nasce com a taxa da perpetuidade (D/r), mas volta pro presente pela taxa do estágio inicial.
- Dividendo da perpetuidade = payout × LPA. R_E não é taxa livre de risco.

## 3. Sanity checks (rodar antes de marcar qualquer resposta)

- LTN: P < 1000 sempre. Deu acima? Erro de sinal ou fórmula.
- NTN-F / bond: cupom vs YTM diz ágio/deságio. Confere o lado.
- Câmbio: inflação ou juro local maior → moeda local deprecia (S sobe).
- Retorno anualizado de período curto fica grande. Não é erro.
- Preço absurdamente baixo → taxa de desconto alta demais. Suspeita nº 1: taxa anual aplicada em período curto.
- Unidade na resposta (a.m., a.s., a.a., a.p.). Ele considera errado se vier na unidade errada.

## 4. O que NÃO precisa suar

- Conceito puro (IPCA vs INPC, regime de metas): ele quase não cobra. Lê uma vez e segue.
- Fundos (cap 5 Anbima): sem lista de exercício, provavelmente leve ou só conceitual. Não decora.
- Amortização (SAC/Price): caiu na parcial, **não cai agora**.
