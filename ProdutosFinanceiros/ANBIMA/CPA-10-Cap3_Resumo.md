# CPA-10 Cap 3: Conceitos Básicos de Economia e Finanças

## 3.1 Conceitos básicos de economia

### 3.1.1 Indicadores econômicos

**[[PIB]] (Produto Interno Bruto)**: soma de bens e serviços **finais**, em termos monetários e a **valor de mercado**, produzidos numa região em determinado período. "Finais" exclui intermediários para evitar dupla contagem. Comparação internacional usa janela anual.

Duas óticas de cálculo:

| Ótica | Fórmula / Composição |
|---|---|
| Despesa | `Y = C + I + G + (X − M)` |
| Renda | Soma de salários, aluguéis, juros, lucros e dividendos |

Componentes da ótica da despesa: C consumo das famílias, I investimento, G despesa do governo, X exportações, M importações.

**Índices de inflação no Brasil**:

| Índice | Calculado por | Faixa / Composição | Uso principal |
|---|---|---|---|
| **[[IPCA]]** | IBGE (governo) | Famílias com renda 1 a 40 SM em áreas urbanas | **Meta de inflação oficial** do CMN/BACEN |
| **[[IGP-M]]** | IBRE/FGV | Média ponderada: IPA 60%, IPC 30%, INCC 10% | Indexador de contratos (aluguel), influência forte do atacado |

Pegadinha: IPCA é o índice oficial da meta, não o IGP-M nem o INPC.

**[[Taxa de câmbio]]**: preço relativo entre duas moedas. Notação XYZ/ABC: ABC moeda-base, XYZ moeda-contagem. BRL/USD = 3,00 significa 3 reais por 1 dólar (dólar é base).

| Tipo | Definição |
|---|---|
| Spot ("dólar pronto") | Taxa para compra/venda imediata, mercado em tempo real |
| **PTAX** | Média BACEN, 4 janelas de consulta no dia, código Sisbacen PTAX800, referência pra derivativos |

**Taxas de juros brasileiras**:

| Taxa | Origem | Base de cálculo | Uso |
|---|---|---|---|
| **[[Selic]] Over** | Média ponderada das compromissadas de 1 dia lastreadas em TPF, divulgada D+1 ~9h | Dias úteis, % a.a. | Custo do dinheiro de mercado |
| **Meta Selic** | Definida pelo Copom | Decisão administrativa, não média | Instrumento de política monetária |
| **[[Taxa DI]]** (Cetip Over Extragrupo) | Média B3 das DIs prefixadas de 1 DU **entre conglomerados diferentes** (Extragrupo) | 252 DU/ano | ~92% das debêntures, CDBs |
| **[[TR]]** | BACEN, a partir das LTNs no secundário, aplica fator redutor sobre TBF | Mensal | Poupança, FGTS, financiamento imobiliário |

Diferença Selic Over vs Meta Selic: Over é média realizada de mercado, Meta é alvo do Copom. Selic Over caminha colada na Meta. Selic e DI andam quase sobrepostas no gráfico histórico.

Pegadinha DI: apurada **diariamente** e aplicada em **dias úteis** (252 DU/ano), não corridos. Considera só Extragrupo (operações entre conglomerados distintos).

TBF é insumo da TR, não a própria TR.

### 3.1.2 Comitê de Política Monetária (Copom)

Criado em 1996 dentro do BACEN. **Três objetivos**:

- Implementar a política monetária.
- Definir a **meta da taxa Selic** e seu eventual viés.
- Analisar o Relatório de Inflação.

Composição: presidente + diretores do BACEN. **8 reuniões/ano** (~a cada 6 semanas), duração 2 dias.

| Dia | Atividade | Participantes |
|---|---|---|
| Dia 1 | Apresentações técnicas sobre conjuntura | Membros + chefes de departamentos (Deban, Demab, Depec, Depep, Depin, Derin, Gerin) |
| Dia 2 | Discussão e votação da meta Selic | Apenas membros do Copom + chefe Depep (sem voto) |

**Viés**: se Copom fixar viés (alta ou baixa), o presidente do BACEN pode alterar a meta entre reuniões **no mesmo sentido do viés**, sem reunião extraordinária. Sem viés, mudança só na próxima reunião (ordinária ou extraordinária). Decisão sempre divulgada ao final da reunião.

---

## 3.2 Conceitos básicos de finanças

### 3.2.1 Taxa de juros nominal e real

**Nominal**: taxa contratual aplicada sobre o montante, não desconta inflação.
**Real**: descontada da inflação, mostra ganho real de poder de compra.

Fórmula exata (Fisher):

```
RR = (1 + RN) / (1 + i) − 1
```

Aproximação:

```
RR ≈ RN − i
```

Exemplo: RN = 9%, i = 5%, exato 3,81%, aproximado 4%.

**Pontos críticos**:

- Inflação > nominal: taxa real **negativa**, perda de poder de compra.
- Deflação (i < 0): taxa real **maior que** a nominal.
- Em tese, política monetária estabiliza a real, na prática a real flutua bastante.

### 3.2.2 Capitalização simples vs composta

| Característica | Simples | Composta |
|---|---|---|
| Base de cálculo dos juros | Sempre o valor presente (montante inicial) | VP + juros acumulados (juros sobre juros) |
| Crescimento | Aritmético / linear | Geométrico / exponencial |
| Juros do período t | Idênticos a qualquer outro período | Crescentes (depende do saldo) |
| Uso típico no Brasil | Pouco frequente | Padrão em RF e mercados globais |

Fórmulas-chave:

```
Simples:    J = VP · r · n
            VF = VP · (1 + r·n)
            VP = VF / (1 + r·n)

Composta:   J = VP · [(1 + r)^n − 1]
            VF = VP · (1 + r)^n
```

Comparação numérica (R$ 10.000, 1% a.m., 6 meses):
- Simples: VF = 10.600,00, juros 600.
- Composta: VF = 10.615,20, juros 615,20.

### 3.2.3 Taxas equivalentes vs proporcionais

| Regime | Nome | Cálculo entre períodos |
|---|---|---|
| Simples | **Proporcional** | Multiplica/divide direto: 1% a.m. = 12% a.a. |
| Composto | **Equivalente** | Exponenciação: `r2 = (1 + r1)^(n2/n1) − 1` |

Exemplo composta: 1% a.m. equivale a (1 + 1%)^12 − 1 = **12,68% a.a.** (maior que o proporcional 12%).

**Fórmula DI (sempre 252 DU)**:

```
r_dia_util = (1 + Taxa_DI)^(1/252) − 1
r_periodo  = (1 + Taxa_DI)^(n/252) − 1
```

Exemplo: DI 10,14% a.a. equivale a 0,03833% por DU; 21 DU ≈ 0,81%; 126 DU (semestre) ≈ 4,95%.

### 3.2.4 Benchmark (índice de referência)

Conceito: parâmetro pra avaliar **desempenho relativo** de um produto. Retorno absoluto, sozinho, não diz nada ("12% comparado com o quê?").

**Qualidades exigidas de um benchmark válido**:

- Definido claramente.
- Mensurável com frequência.
- Investível (possível replicar componentes).
- Adequado ao produto avaliado.
- **Especificado antes** do início do período de avaliação (pra evitar cherry-picking).

Benchmarks comuns:

| Classe | Benchmarks |
|---|---|
| Renda fixa | Taxa DI, IMA-B (IPCA), IMA-C (IGP-M), IMA-S (Selic), rendimentos de TPF |
| Renda variável | Ibovespa, IBrX 100, IBrX 50, IGC, ISE |

Pegadinha: benchmark **não** restringe a atuação do gestor a uma classe de ativos nem aos componentes do índice. Vale tanto pra gestão passiva quanto ativa (no ativo, base pra taxa de performance).

### 3.2.5 Volatilidade

Definição: grau de variação dos preços de um ativo num período, medido pelo **desvio-padrão dos retornos logarítmicos**.

Pontos:

- Volatilidade é medida de **risco**, não de retorno, liquidez ou desempenho.
- Maior vol = preço oscila mais = mais incerteza.
- Comparação direta: para mesmo retorno esperado, escolher menor volatilidade.

Exemplo apostila (vol anualizada maio/2017): LCAM3 28,40%, BBDC4 53,02%, RSID3 115,32%.

### 3.2.6 Prazo médio ponderado (PMP)

Tempo médio pra recebimento dos fluxos do título, ponderado pelos valores presentes de cada fluxo. **Não** é o prazo até o vencimento (exceto em zero-coupon com bullet no vencimento).

Fórmula CMN (oficial):

```
PMP = [ Σ (Fj / (1+i)^(dj/252)) · dj ] / VP · (1/252)
```

Onde Fj é fluxo, dj dias úteis até o fluxo, i é TIR (252 DU), VP valor presente.

PMP de carteira: soma ponderada dos PMPs dos títulos, com pesos = VP de cada título / VP total da carteira.

**Propriedades (cai em prova)**:

| Variável | Relação com PMP |
|---|---|
| Prazo até o vencimento (com bullet) | **Direta** (maior prazo = maior PMP) |
| Taxa de juros do título (cupom) | **Inversa** (cupom maior = PMP menor, fluxos pesam mais cedo) |
| Frequência de pagamentos | **Inversa** (mais pagamentos = PMP menor) |

Caso PMP = prazo até vencimento: **cupom zero + amortização integral no vencimento (bullet)**. Único cenário em que coincidem.

### 3.2.7 Marcação a mercado (MtM)

**Conceito**: preço de um ativo = valor presente do fluxo de caixa esperado, descontado a taxa de mercado vigente.

```
Preço = Σ Fj / (1 + taxa_desconto)^(dj/252)
```

Duas razões pra preço oscilar:
- Mudança no fluxo esperado (ex.: dividendos futuros revistos em ações).
- Mudança na taxa de desconto exigida pelo mercado.

**Relação preço x taxa (RF com taxa fixa)**: **inversa**.

| Cenário (mesmo dia) | Efeito MtM |
|---|---|
| Taxa sobe | Preço cai (MtM **negativo**) |
| Taxa cai | Preço sobe (MtM positivo) |
| Taxa constante | Preço inalterado |

Se taxa de desconto = taxa contratual do cupom, **preço = valor nominal**.

**MtM vs marcação na curva**: MtM usa taxa de mercado atual; marcação na curva usa taxa do momento da aquisição (não capta volatilidade).

**Efeito do prazo**: para mesma taxa de desconto diferente da contratual, **prazo maior = maior afastamento entre preço e valor nominal** = maior sensibilidade do preço a variações da taxa. Aplica-se também a passivos.

### 3.2.8 Mercado primário vs secundário

| Mercado | Definição | Captação pelo emissor | Participantes típicos |
|---|---|---|---|
| **Primário** | Emissor lança títulos/ações pra primeiros investidores | **Sim** (recursos vão pra empresa) | Emissor, bancos de investimento, escritórios de advocacia, agentes fiduciários, institucionais, fundos |
| **Secundário** | Negociação após a emissão, sem envolvimento do emissor | **Não** | Corretoras, institucionais, PF, gestores, especuladores |

Relevância:
- Investidor: primário traz acesso a novos papéis (geralmente prêmio sobre o secundário pra atrair); secundário permite girar carteira e desfazer posições.
- Emissor: primário é onde capta; secundário serve pra ler custo de captação (próprio e de comparáveis), timing de emissão e gestão de tesouraria.

---

## Pontos críticos pra prova

1. **PIB**: bens e serviços **finais** (não intermediários), a **valor de mercado** (não a custo), `Y = C + I + G + (X − M)`.
2. **IPCA = meta oficial** (CMN/BACEN). IGP-M é contratos. Pegadinha: nunca INPC ou IPC.
3. **Selic Over** é média realizada das compromissadas; **Meta Selic** é decisão Copom. **Taxa DI** é apurada diária, base **252 DU**, **Extragrupo**.
4. **TR** remunera **poupança, FGTS, financiamento imobiliário**. Vem da TBF (LTNs no secundário) com fator redutor.
5. **Copom**: 8 reuniões/ano, 2 dias, define **meta Selic**. Viés permite alteração entre reuniões no mesmo sentido sem reunião extraordinária.
6. **Real ≈ Nominal − Inflação** (aproximação). Exata: `(1+RN)/(1+i) − 1`. Inflação > nominal = real negativa.
7. **Equivalente vs proporcional**: equivalente é composta (exponencial), proporcional é simples (linear). 1% a.m. = 12,68% a.a. equivalente, 12% a.a. proporcional.
8. **Benchmark**: ex-ante, mensurável, investível, adequado. Não restringe gestor à classe nem aos componentes.
9. **Volatilidade = desvio-padrão dos retornos**, mede **risco** (não retorno, não liquidez).
10. **PMP = prazo até venc.** somente se **cupom zero + bullet no vencimento**. Cupom maior reduz PMP, mais pagamentos reduzem PMP, prazo final maior aumenta PMP.
11. **MtM**: relação **preço x taxa é inversa**. Taxa sobe = preço cai = MtM negativo. Prazo maior amplifica o efeito.
12. **Mercado primário**: capta recurso pro emissor. **Secundário**: títulos trocam de mãos sem envolver o emissor.
