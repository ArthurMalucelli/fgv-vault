---
materia: ProdutosFinanceiros
data: 2026-05-19
tema: Renda Fixa BR + Taxa de Câmbio + IRP + PPP (prova quarta 20.05)
topicos: [LTN, NTN-F, CDI, CDB, SELIC, Taxa de Câmbio, IRP, PPP, Dias Úteis, IR Renda Fixa]
tags: [resumo, prova, cheatsheet]
---

# Guia de Prova: Renda Fixa BR + Câmbio + IRP + PPP

Escopo da prova: renda fixa Brasil (títulos públicos LTN/NTN-F, CDI, CDB), taxa de câmbio, paridade do poder de compra (PPP), paridade da taxa de juros (IRP). Material consolidado de Aula 10, Aula 21, Listas 7, 8, 10 + análise do quiz da turma anterior. Planilha companheira: **GuiaProva_RendaFixaCambio.xlsx** com soluções vivas.

## TL;DR: armadilhas recorrentes do banco do professor

Pelo quiz aplicado em turma anterior, o professor cobra fórmula direta em metade das questões e armadilha conceitual na outra metade. Ranking das pegadinhas que reprovam mais gente:

1. **CDB %CDI com CDI variando entre sub-períodos**: aplicar o % no fator em vez da taxa diária. Fix: **i_CDB_dia = %CDI × i_DI_dia**, depois **(1+i_CDB)^n_du**, depois encadeia fatores entre períodos.
2. **LTN com venda intermediária + IR**: esquecer que o prazo restante diminui na venda, ou calcular IR sobre o total em vez do ganho. Fix: **du_venda = du_compra - Δdu**. IR = alíquota × (P_venda − P_compra).
3. **PPP com direção da inflação invertida**: inflação local > estrangeira → moeda local **deprecia** → mais moeda local por unidade da estrangeira.
4. **IRP com numerador/denominador invertidos**: na cotação **A/B**, A é quote (numerador) e B é base (denominador). A razão de juros segue a mesma ordem.
5. **LTN preço dado YTM**: confundir base ou direção. Fix: **P = 1000/(1+YTM)^(du/252)**. Sempre desconto, sempre 252.

Fórmula direta com 1 passo é fácil. **A prova te derruba em questões com 2+ etapas (algo varia no caminho) ou que exigem pensar a direção de uma relação**.

## Legenda de abreviações

Tudo o que aparece nas fórmulas a seguir.

**Taxas de juros (genéricas)**

| Símbolo | Lê-se | Significado |
|---|---|---|
| **i** | "i" | Taxa de juros genérica |
| **i_aa** | "i ao ano" | Taxa anual (ex: 10% a.a.) |
| **i_am** | "i ao mês" | Taxa mensal |
| **i_as** | "i ao semestre" | Taxa semestral |
| **i_du** ou **i_d** | "i ao dia útil" | Taxa por dia útil (a.d.u.) |
| **i_p** | "i do período" | Taxa de um período genérico de n du |
| **r** | "r" | Mesma coisa que **i**. Usado no contexto de câmbio (r_BRL, r_USD) |

**Unidades temporais**

| Símbolo | Significado |
|---|---|
| **du** | Dias úteis (base 252 no BR) |
| **dc** | Dias corridos (base 365, calendário civil) |
| **a.a.** | Ao ano (anual) |
| **a.m.** | Ao mês (mensal) |
| **a.s.** | Ao semestre (semestral) |
| **a.d.** ou **a.d.u.** | Ao dia útil (diária) |
| **a.p.** | Ao período |

**Taxas específicas de produtos**

| Símbolo | Significado |
|---|---|
| **i_DI_dia** ou **i_DI_d** | Taxa do CDI convertida pra diária. **= (1 + CDI_aa)^(1/252) − 1** |
| **i_CDB_dia** ou **i_CDB_d** | Taxa diária do CDB. **= %CDI × i_DI_dia** |
| **%CDI** | Percentual do CDI que o produto paga (ex: 90%, 127%, 238%) |
| **CDI_aa** | Taxa CDI anualizada (como divulgada) |
| **YTM** | Yield to Maturity. Taxa interna de retorno do título até o vencimento, anualizada |

**Preços e fluxos de títulos**

| Símbolo | Significado |
|---|---|
| **P** | Preço do título hoje |
| **P0** | Preço na compra |
| **P1** | Preço na venda (intermediária) |
| **VN** ou **VF** | Valor de face / valor nominal. LTN e NTN-F: sempre R$ 1.000 |
| **Cupom** | Cupom da NTN-F: R$ 48,8088 a cada semestre |
| **du_k** | Dias úteis até o k-ésimo cupom |
| **du_N** | Dias úteis até o último fluxo (vencimento) |
| **n** | Número de períodos |

**Símbolos matemáticos**

| Símbolo | Lê-se | Significado |
|---|---|---|
| **Σ** | Sigma | Somatório (somar todos os termos) |
| **Π** | Pi maiúsculo | Produtório (multiplicar todos os termos) |
| **Δ** | Delta | Variação (Δdu = dias úteis decorridos) |
| **π** | Pi minúsculo | Taxa de inflação |
| **^** | "elevado a" | Potenciação. **(1+i)^n** = (1+i) elevado a n |

**Câmbio**

| Símbolo | Significado |
|---|---|
| **S** | Spot. Taxa de câmbio à vista (hoje) |
| **F** | Forward. Taxa de câmbio futura (acordada hoje pra liquidar em data futura) |
| **S_BRL/USD** | Spot da cotação BRL por USD (quanto BRL custa 1 USD) |
| **r_quote** | Taxa de juros da moeda do numerador (ex: BRL em BRL/USD) |
| **r_base** | Taxa de juros da moeda do denominador (ex: USD em BRL/USD) |
| **π_local** | Inflação doméstica |
| **π_estrangeira** | Inflação do país estrangeiro |

**Notações curtas que aparecem**

- **f1, f2, F1, F2**: fatores de capitalização. **Fator = (1 + taxa)^prazo**.
- **(1+i)**: fator de capitalização (sempre 1 + taxa).
- **(1+i_BR) / (1+i_US)**: razão de fatores entre dois países (vai em IRP).

## Bloco 1: Conversão de taxas (base 252)

Premissa central: renda fixa BR usa **252 dias úteis** por ano. Todo o resto deriva disso.

<pre>
Anual → diária:    i_du = (1 + i_aa)^(1/252) − 1
Anual → mensal:    i_am = (1 + i_aa)^(21/252) − 1   (21 du/mês)
Anual → semestral: i_as = (1 + i_aa)^(1/2) − 1      (NTN-F cupom: 4,88% se i=10%)
Período n du → aa: i_aa = (1 + i_p)^(252/n) − 1
Encadear:          (1 + i_total) = Π(1 + i_k)
</pre>

Exemplo Q2 da turma anterior: CDI 10,24% a.a., mensal = (1,1024)^(1/12) − 1 = 0,82%.

## Bloco 2: CDI, CDB, %CDI

CDI segue de perto a SELIC, divulgado em % a.a. Pra usar em produtos, converte primeiro pra diária.

CDB indexado paga **X% do CDI**. O % se aplica na TAXA DIÁRIA, não no fator:

<pre>
i_DI_dia  = (1 + CDI_aa)^(1/252) − 1
i_CDB_dia = %CDI × i_DI_dia            ← pegadinha mais comum
Fator período = (1 + i_CDB_dia)^n_du
</pre>

**Quando o CDI varia entre sub-períodos**, calcula i_CDB_dia pra cada sub-período e encadeia:

<pre>
Fator_total = Π_k (1 + %CDI × i_DI_dia_k)^n_k − 1
</pre>

Reproduzindo a Q3 da turma anterior (238% do CDI, 27 du a 19,87%, 21 du a 17,45%):

<pre>
i_DI_d1   = (1,1987)^(1/252) − 1 = 0,0720% a.d.
i_CDB_d1  = 2,38 × 0,0720% = 0,1714% a.d.
F1        = (1,001714)^27 = 1,04736

i_DI_d2   = (1,1745)^(1/252) − 1 = 0,0638% a.d.
i_CDB_d2  = 2,38 × 0,0638% = 0,1518% a.d.
F2        = (1,001518)^21 = 1,03227

Total = 1,04736 × 1,03227 − 1 = 8,12%
</pre>

Quando o CDB paga taxa pós-fixada com CDI constante, basta calcular i_CDB_dia uma vez e aplicar **(1+i_CDB_dia)^n_du**.

## Bloco 3: [[LTN]] (Tesouro Prefixado)

Características:

- Valor de face (VN): **sempre R$ 1.000**.
- **Sem cupom**: paga só no vencimento (principal + juros embutidos no deságio).
- Sempre negociada com **deságio**: P < 1.000 (prêmio exigiria YTM negativa, sem sentido).
- Prazo em dias úteis, base 252.

Fórmulas:

<pre>
P   = 1000 / (1 + YTM_aa)^(du/252)
YTM = (1000/P)^(252/du) − 1
</pre>

No Excel:
<pre>
=1000/(1+YTM)^(du/252)
=-VP(YTM; du/252; ; 1000)        (alternativa)
=(1000/P)^(252/du)-1              (YTM dado preço)
</pre>

**Venda intermediária (marcação a mercado)**:

<pre>
P0 = 1000/(1+YTM_compra)^(du_compra/252)
P1 = 1000/(1+YTM_venda)^((du_compra − Δdu)/252)
Retorno período      = P1/P0 − 1
Retorno anualizado   = (P1/P0)^(252/Δdu) − 1
</pre>

Relação preço × YTM (cai em pegadinha):

- YTM **subiu** entre compra e venda: preço caiu → retorno **abaixo** da YTM contratada.
- YTM **caiu** entre compra e venda: preço subiu → retorno **acima** da YTM contratada.
- Vendeu no vencimento: recebeu YTM contratada (o que aconteceu no meio não importa).

## Bloco 4: [[NTN-F]] (Tesouro Prefixado com Juros Semestrais)

Características:

- VN: **R$ 1.000**.
- Cupom: **10% a.a. efetivo**, capitalizado semestralmente → **(1,10)^0,5 − 1 = 4,8809%** por semestre → **R$ 48,8088** por cupom.
- Cupons sempre em **01/01 e 01/07** (datas fixas). No último, paga cupom + principal: R$ 1.048,81.
- Espaçamento: ~126 du entre cupons (problemas simplificados usam 126 du exatos; problemas reais usam DIATRABALHOTOTAL com feriados).

Fórmula:

<pre>
P = Σ_k [48,8088 / (1+YTM)^(du_k/252)] + 1000/(1+YTM)^(du_N/252)
</pre>

O último termo geralmente fica: **(48,81 + 1000)/(1+YTM)^(du_N/252)**.

Para achar **YTM dado o preço**: não tem fórmula fechada. Usa **Atingir Meta** (Goal Seek) no Excel, ou TIR do fluxo (negativo na compra, positivo nos cupons + VF).

Exemplo Q1 da turma anterior (YTM 15,18%, du dos cupons: 104, 230, 356, 482, 608, 734):
<pre>
P = 48,81/1,1518^(104/252) + 48,81/1,1518^(230/252) + 48,81/1,1518^(356/252)
  + 48,81/1,1518^(482/252) + 48,81/1,1518^(608/252) + 1048,81/1,1518^(734/252)
  = 895,78
</pre>

**Relação preço × YTM**, similar à LTN:

- Cupom (10%) > YTM → preço com **prêmio** (P > 1.000). Ex: cupom 10%, YTM 9,48% → P = 1.031,92.
- Cupom = YTM → P = 1.000 (par).
- Cupom < YTM → preço com **deságio** (P < 1.000).

Quando vende intermediário: preço pode mudar por **dois motivos** simultâneos. Primeiro, YTM nova reprecifica os fluxos restantes. Segundo, alguns cupons já foram pagos (saem da soma).

## Bloco 5: Dias úteis (Tesouro Direto)

Convenção do TN:

- Janela: data de liquidação (**inclusive**) até data de vencimento (**exclusive**).
- Data de liquidação = D+1 da data de compra (1 dia útil depois).
- Excel: **=DIATRABALHOTOTAL(liq; venc−1; Feriados)**.
- Por que **−1**? DIATRABALHOTOTAL conta os dois extremos. Como vencimento é exclusive (rendimento já pago no dia anterior), subtrai 1.

Em exercícios analíticos, o du costuma vir dado direto.

Conversão aproximada quando o exercício te dá du mas a alíquota de IR usa d.c.:
<pre>
dias_corridos ≈ dias_úteis × 1,4
1 ano = 252 du ≈ 365 dc
1 semestre = 126 du ≈ 180 dc
</pre>

## Bloco 6: Tributação Renda Fixa BR

Alíquota regressiva, sobre o ganho:

| Prazo (dias corridos) | Alíquota |
|---|---|
| Até 180 | 22,5% |
| 181 a 360 | 20,0% |
| 361 a 720 | 17,5% |
| Acima de 720 | 15,0% |

<pre>
IR              = alíquota × (P_venda − P_compra)
Resgate líquido = P_venda − IR
</pre>

**Pegadinha**: aplicar a alíquota sobre o total resgatado em vez do ganho.

Caso Q14 da turma anterior: LTN, du 193 → vendeu após 65 du. Como d.c. ≈ d.u. × 1,4, ~91 dias corridos → 22,5%. Ganho = 938,79 − 912,15 = 26,64. IR = 22,5% × 26,64 ≈ R$ 6,00.

## Bloco 7: Taxa de câmbio (Aula 21)

Conceitos centrais:

- **Cotação direta** (padrão BR): preço da moeda estrangeira em moeda local. Ex: **1 USD = 5,39 BRL**.
- **Cotação indireta**: preço da moeda local em estrangeira. Ex: **1 BRL = 0,1855 USD**.
- Notação **A/B**: lê-se "A por 1 B". B é a base, A é o quote. **BRL/EUR = 4,43 significa "4,43 reais por 1 euro"**.

**Valorização vs Desvalorização** (em cotação direta):

- Cotação **sobe** (5,00 → 5,50 BRL/USD): moeda local **DESVALORIZOU**. Real perdeu valor; dólar ficou caro.
- Cotação **cai** (5,00 → 4,50): moeda local **VALORIZOU**. Real ganhou valor.

Variação % se mede na cotação direta:
<pre>
Δ% direta = +10% → moeda local desvalorizou 10%
Δ% direta = −10% → moeda local valorizou 10%
</pre>

Tipos de dólar no BR:

- **Comercial**: bancos e grandes empresas. Spread baixo.
- **Turismo**: bancos e pessoas físicas. Spread maior por volume pequeno.
- **Paralelo**: ilegal desde Collor.
- **Ptax**: taxa de referência do BACEN. Média de 4 janelas de consulta com 14 dealers credenciados (cada janela 2 min, dura 6 meses o credenciamento). Usada pra liquidar contratos futuros.

Spot vs Forward (relevante pra entender IRP):

| | Negociação | Liquidação |
|---|---|---|
| Spot | D+0 | D+0 ou D+2 |
| Forward | D+0 | D+N |

**Conversão de fluxos entre moedas** (cai em exercícios de VPL/TIR cross-currency):

Se você tem fluxos em USD e quer trazer pra R$:
<pre>
Fluxo_R$(t) = Fluxo_USD(t) × Cambio(t)
</pre>
onde Cambio(t) projeta a cotação no momento t. Se o real desvaloriza x% a.a., **Cambio(t) = Cambio(0) × (1+x)^t**.

Depois desconta os fluxos em R$ pela taxa de desconto em R$ (e fluxos em USD pela taxa em USD).

## Bloco 8: [[IRP]] (Interest Rate Parity / Paridade da Taxa de Juros)

Identidade central:

<pre>
(1 + r_country) / (1 + r_US) = Forward_country/USD / Spot_country/USD
</pre>

Lê assim: a razão dos fatores de juros entre dois países = razão forward/spot. Se um país tem juro mais alto, sua moeda tende a **se depreciar** no forward, para que o ganho de juros seja anulado (sem arbitragem).

**Generalizando** para qualquer cotação **quote/base**:

<pre>
F = S × (1 + r_quote) / (1 + r_base)
</pre>

**Regra mnemônica**: na cotação **A/B**, A é quote (numerador na razão de cotações). A taxa de A entra no numerador da razão de juros também. Combine **F_A/B / S_A/B = (1+r_A)/(1+r_B)**.

**Aplicação 1 (Q10 da turma anterior, JPY/USD)**:

- Spot JPY/USD = 128,77 (128,77 ienes por 1 USD; USD é base, JPY é quote).
- i_USD = 5,08%, i_JPY = 1,88%.

<pre>
F_JPY/USD = 128,77 × (1 + 0,0188) / (1 + 0,0508)
          = 128,77 × 0,96955
          = 124,85 JPY/USD
</pre>

USD se deprecia no forward (vale menos ienes amanhã) porque USD tem juro mais alto. Sem arbitragem: aplicar em USD deveria render igual a aplicar em JPY e trazer pelo forward.

**Aplicação 2: taxa equivalente em outra moeda** (slide aula 21):

Brasil 12% a.a., spot 5,50 BRL/USD, forward 5,82 BRL/USD. Qual o r_USD equivalente?

<pre>
F/S = (1+r_BRL)/(1+r_USD)
5,82/5,50 = 1,12/(1 + r_USD)
1 + r_USD = 1,12 × 5,50/5,82 = 1,0584
r_USD     = 5,84% a.a.
</pre>

**Verificação por R$ 100**: aplica R$ 100 no BR → vira R$ 112 em 1 ano → converte a 5,82 → US$ 19,24. Se tivesse convertido R$ 100 hoje a 5,50, teria US$ 18,18. Taxa em USD: 19,24/18,18 − 1 = 5,84%. Bate.

## Bloco 9: [[PPP]] (Purchasing Power Parity)

Identidade central (PPP relativa):

<pre>
E(1 + π_local) / E(1 + π_estrangeira) = E(spot_local/estrangeira) / spot_local/estrangeira
</pre>

Reorganizando:

<pre>
S_new = S_old × (1 + π_local) / (1 + π_estrangeira)
</pre>

**Lógica**: inflação local maior que estrangeira → moeda local perde poder de compra mais rápido → moeda local **deprecia** → precisa **MAIS** moeda local por unidade da estrangeira.

**Aplicação (Q9 da turma anterior, BRL/EUR)**:

- S_2022 = 4,43 BRL/EUR
- π_BR = 9,74%, π_EUR = 6,62%
- BR é local, EUR é estrangeira (no formato BRL/EUR).

<pre>
S_2023 = 4,43 × (1,0974) / (1,0662) = 4,43 × 1,02926 = 4,56 BRL/EUR
</pre>

Faz sentido: inflação BR > inflação EUR → BRL deprecia → precisa mais BRL por EUR.

**PPP absoluta** (estilo Big Mac): câmbio que igualaria o preço de uma cesta entre dois países.
<pre>
S_PPP = P_local / P_estrangeira
</pre>
Combo R$ 55 no BR e US$ 10 nos EUA → S_PPP = 5,50 BRL/USD.

**Por que PPP falha na prática**:

- Custos de transporte
- Barreiras comerciais (tarifas)
- Variações de qualidade
- Bens não-tradables (serviços domésticos)
- Fluxos financeiros, expectativas, política monetária

## Cheat Sheet final (1 linha cada)

<pre>
LTN          P = 1000/(1+YTM)^(du/252)
LTN inversa  YTM = (1000/P)^(252/du) - 1
NTN-F        P = Σ 48,81/(1+YTM)^(du_k/252) + 1000/(1+YTM)^(du_N/252) ; cupom = (1,1)^0,5 - 1 = 4,88% a.s.
CDB %CDI     i_CDB_d = %CDI × ((1+CDI_aa)^(1/252) - 1) ; F = (1+i_CDB_d)^n
CDB %CDI var Fator_tot = Π_k (1 + %CDI × i_DI_dia_k)^n_k - 1
Conversao    aa → mm: (1+i)^(21/252) - 1 ; periodo → aa: (1+i_p)^(252/n) - 1
IR RF BR     ≤180dc:22,5% | 181-360:20% | 361-720:17,5% | >720:15% (sobre o GANHO)
IRP          F/S = (1+r_quote)/(1+r_base) na cotacao quote/base
PPP          S_new = S_old × (1+π_local)/(1+π_estrangeira)
PPP absoluta S = P_local / P_estrangeira
Valoriz/desv direta sobe → moeda local DESVALORIZOU ; direta cai → local VALORIZOU
</pre>

## Estratégia de prova

Faz nessa ordem em cada questão:

1. **Leia o enunciado inteiro antes de calcular**. Identifique: é taxa BR (252) ou US (anual)? Tem cupom (NTN-F) ou não (LTN)? Tem mudança de YTM no meio (venda intermediária)? Tem IR? É câmbio (PPP/IRP) ou só conversão?
2. **Anote os dados em coluna** no canto. Use unidades (% a.a., du, R$, R$/US$).
3. **Para câmbio**, escreve qual moeda é local e qual é estrangeira ANTES de aplicar IRP/PPP. Marca quem é quote, quem é base.
4. **Verificação sanity** após calcular:
   - NTN-F com YTM > 10% (cupom) deve ter P < 1.000.
   - LTN sempre P < 1.000.
   - PPP: se inflação local > estrangeira, S_new > S_old.
   - IRP: se r_quote > r_base, F > S (quote deprecia em forward).
5. **Se errar a primeira tentativa, refaz a conta com a fórmula reescrita do zero** (não corrige a que está). Calculadora teimosa erra duas vezes a mesma coisa.

Boa prova.

## Pra fixar (Vault)

- [[LTN]]
- [[NTN-F]]
- [[CDB]]
- [[CDI]]
- [[SELIC]]
- [[Tesouro Direto]]
- [[Cupom Semestral]]
- [[IRP]]
- [[PPP]]
- [[Cotação Direta]]
- [[Ptax]]
- [[Dias Úteis]]
- [[IR Renda Fixa]]
