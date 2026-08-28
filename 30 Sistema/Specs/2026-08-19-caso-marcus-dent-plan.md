---
tipo: plan
materia: ContabilidadeFinanceira
data: 2026-08-19
tags: [plan]
---

# Caso Marcus Dent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir a resolução do Caso Marcus Dent (Contabilidade Financeira, 19/08) como material de estudo no vault: `ResolucaoCasoMarcusDent.md` e `MarcusDentDFs.xlsx`, mais sete notas de conceito novas, tudo commitado em `~/FGV`.

**Architecture:** Um script Python (openpyxl) gera a planilha com quatro abas ligadas por fórmula a partir de uma aba de premissas; o LibreOffice recalcula e um script verificador confere os números do gabarito e os checks em zero. O markdown é escrito à mão com os mesmos números. Notas de conceito seguem o template do vault. Scripts ficam no scratchpad, só os entregáveis entram no vault.

**Tech Stack:** Python 3 + openpyxl; LibreOffice headless via `recalc.py` da skill xlsx; git no vault `~/FGV`.

Spec: `~/FGV/30 Sistema/Specs/2026-08-19-caso-marcus-dent-design.md`.

Caminhos usados em todas as tasks:

```bash
VAULT=/Users/arthurmalucelli/FGV
AULA="$VAULT/10 Matérias/ContabilidadeFinanceira/Aulas/08.19"
SCR=/private/tmp/claude-501/-Users-arthurmalucelli/f53a9de1-4730-4235-a5cd-a3c9b3c48003/scratchpad/marcusdent
XLSX_SCRIPTS="/Users/arthurmalucelli/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/f3275e4f-979d-4cd2-a4be-5b3b463fea2d/c1d131c7-b2a5-48e5-b6dc-dffeecfc54ac/skills/xlsx/scripts"
```

---

## File structure

| Arquivo | Responsabilidade |
|---|---|
| `$SCR/verify_marcus_dent.py` | Teste: abre o xlsx recalculado (valores cacheados) e compara 40 células com o gabarito; exit 1 se qualquer uma falhar. |
| `$SCR/build_marcus_dent_xlsx.py` | Gera `MarcusDentDFs.xlsx` com abas Premissas, Transacoes, Comparativo, Reconciliacao. |
| `$AULA/MarcusDentDFs.xlsx` | Entregável 1 (planilha). |
| `$AULA/ResolucaoCasoMarcusDent.md` | Entregável 2 (resolução, material de estudo com wikilinks). |
| `$VAULT/20 Conhecimento/Conceitos/{Caso Marcus Dent, Passivo Circulante, Passivo Não Circulante, Imobilizado, Juros a Pagar, Reconhecimento da Receita, Confrontação}.md` | Notas de conceito novas. |
| `$SCR/check_wikilinks.py` | Teste: todo `[[link]]` do md e das notas novas aponta pra arquivo existente em `20 Conhecimento/Conceitos/`. |

---

### Task 1: Verificador da planilha (teste primeiro)

**Files:**
- Create: `$SCR/verify_marcus_dent.py`

- [ ] **Step 1: Escrever o verificador**

```python
# /private/tmp/claude-501/-Users-arthurmalucelli/f53a9de1-4730-4235-a5cd-a3c9b3c48003/scratchpad/marcusdent/verify_marcus_dent.py
import sys
import openpyxl

F = "/Users/arthurmalucelli/FGV/10 Matérias/ContabilidadeFinanceira/Aulas/08.19/MarcusDentDFs.xlsx"

wb = openpyxl.load_workbook(F, data_only=True)
t, c, r = wb["Transacoes"], wb["Comparativo"], wb["Reconciliacao"]

checks = {
    "BP inicial total ativo":        (t["B13"].value, 64000),
    "BP inicial passivo+PL":         (t["B28"].value, 64000),
    "BP final total ativo":          (t["J13"].value, 69700),
    "BP final passivo+PL":           (t["J28"].value, 69700),
    "AC final":                      (t["J9"].value, 17200),
    "ANC final":                     (t["J12"].value, 52500),
    "PC final":                      (t["J18"].value, 2500),
    "PNC final":                     (t["J21"].value, 55080),
    "PL final":                      (t["J27"].value, 12120),
    "Caixa final no BP":             (t["J5"].value, 8400),
    "Clientes":                      (t["J6"].value, 6400),
    "Estoque":                       (t["J7"].value, 1300),
    "Despesa antecipada":            (t["J8"].value, 1100),
    "Depreciacao acumulada":         (t["J11"].value, -1500),
    "Salarios a pagar":              (t["J16"].value, 500),
    "Receita antecipada":            (t["J17"].value, 2000),
    "Juros a pagar":                 (t["J20"].value, 1080),
    "Lucros acumulados":             (t["J26"].value, 2120),
    "Receita":                       (t["J32"].value, 8000),
    "EBIT":                          (t["J37"].value, 3200),
    "Lucro liquido":                 (t["J39"].value, 2120),
    "Entradas de caixa":             (t["J43"].value, 3600),
    "Saidas de caixa":               (t["J44"].value, -5200),
    "Variacao de caixa":             (t["J45"].value, -1600),
    "Caixa final (fluxo)":           (t["J47"].value, 8400),
    "Check lucro vs lucros acum.":   (t["J40"].value, 0),
    "Check caixa final vs BP":       (t["J48"].value, 0),
    "Comparativo entradas":          (c["B7"].value, 3600),
    "Comparativo receitas":          (c["C7"].value, 8000),
    "Comparativo saidas":            (c["B14"].value, -5200),
    "Comparativo despesas":          (c["C14"].value, -5880),
    "Comparativo variacao caixa":    (c["B15"].value, -1600),
    "Comparativo lucro":             (c["C15"].value, 2120),
    "Comparativo check caixa":       (c["B17"].value, 0),
    "Comparativo check DRE":         (c["C17"].value, 0),
    "Reconciliacao FCO":             (r["B13"].value, -1600),
    "Reconciliacao check":           (r["B18"].value, 0),
}
for col in "BCDEFGHIJ":
    checks[f"Equacao patrimonial col {col}"] = (t[f"{col}29"].value, 0)
for col in "CDEFGHIJ":
    checks[f"Caixa vs conta caixa col {col}"] = (t[f"{col}49"].value, 0)

fails = []
for name, (got, exp) in checks.items():
    if got is None or abs(float(got) - exp) > 1e-6:
        fails.append((name, got, exp))
        print(f"FAIL  {name}: got {got!r}, expected {exp}")
print(f"{len(checks) - len(fails)}/{len(checks)} checks OK")
sys.exit(1 if fails else 0)
```

- [ ] **Step 2: Rodar e confirmar que falha (arquivo ainda não existe)**

Run:
```bash
mkdir -p "$SCR" && python3 "$SCR/verify_marcus_dent.py"
```
Expected: `FileNotFoundError` (o xlsx ainda não existe), exit code diferente de zero.

---

### Task 2: Gerador da planilha

**Files:**
- Create: `$SCR/build_marcus_dent_xlsx.py`
- Create (output): `$AULA/MarcusDentDFs.xlsx`

- [ ] **Step 1: Escrever o gerador**

```python
# /private/tmp/claude-501/-Users-arthurmalucelli/f53a9de1-4730-4235-a5cd-a3c9b3c48003/scratchpad/marcusdent/build_marcus_dent_xlsx.py
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

OUT = "/Users/arthurmalucelli/FGV/10 Matérias/ContabilidadeFinanceira/Aulas/08.19/MarcusDentDFs.xlsx"
NUM = r"#,##0;\(#,##0\);\-"
BLUE, GREEN = "FF0000FF", "FF008000"

wb = Workbook()


def lab(ws, coord, text, bold=False, wrap=False, center=False, italic=False):
    c = ws[coord]
    c.value = text
    c.font = Font(bold=bold, italic=italic)
    if wrap or center:
        c.alignment = Alignment(wrap_text=wrap, horizontal="center" if center else None, vertical="top")
    return c


def inp(ws, coord, value, fmt=NUM):
    c = ws[coord]
    c.value = value
    c.font = Font(color=BLUE)
    c.number_format = fmt
    return c


def fml(ws, coord, formula, bold=False, fmt=NUM):
    c = ws[coord]
    c.value = formula
    c.font = Font(bold=bold)
    c.number_format = fmt
    return c


def lnk(ws, coord, formula, bold=False, fmt=NUM):
    c = ws[coord]
    c.value = formula
    c.font = Font(color=GREEN, bold=bold)
    c.number_format = fmt
    return c


# ---------------------------------------------------------------- Premissas
ws = wb.active
ws.title = "Premissas"
lab(ws, "A1", "CASO MARCUS DENT: demonstracoes financeiras de janeiro/2024", bold=True)
lab(ws, "A2", "Valores em R$. Legenda:", bold=True)
ws["B2"].value = "azul = input do caso"; ws["B2"].font = Font(color=BLUE)
ws["C2"].value = "preto = formula"
ws["D2"].value = "verde = link entre abas"; ws["D2"].font = Font(color=GREEN)

lab(ws, "A4", "Abertura (31/12/2023)", bold=True)
lab(ws, "A5", "Emprestimo microcredito (principal)");            inp(ws, "B5", 54000)
lab(ws, "A6", "Taxa de juros mensal");                            inp(ws, "B6", 0.02, fmt="0.0%")
lab(ws, "A7", "Equipamentos (comprados com o emprestimo)");       fml(ws, "B7", "=B5")
lab(ws, "A8", "Vida util dos equipamentos (meses)");              inp(ws, "B8", 36, fmt="0")
lab(ws, "A9", "Capital inicial (economias depositadas)");         inp(ws, "B9", 10000)

lab(ws, "A11", "Janeiro/2024", bold=True)
lab(ws, "A12", "Servicos prestados no mes");                      inp(ws, "B12", 8000)
lab(ws, "A13", "% recebido a vista");                             inp(ws, "B13", 0.2, fmt="0%")
lab(ws, "A14", "Adiantamento recebido (servicos de marco)");      inp(ws, "B14", 2000)
lab(ws, "A15", "Aluguel pago no mes");                            inp(ws, "B15", 2200)
lab(ws, "A16", "Meses cobertos pelo aluguel pago");               inp(ws, "B16", 2, fmt="0")
lab(ws, "A17", "Compra de materiais (a vista)");                  inp(ws, "B17", 3000)
lab(ws, "A18", "Estoque de materiais em 31/01");                  inp(ws, "B18", 1300)
lab(ws, "A19", "Salarios e encargos do mes (pagos em fevereiro)"); inp(ws, "B19", 500)

lab(ws, "A21", "Derivados", bold=True)
lab(ws, "A22", "Depreciacao mensal");                             fml(ws, "B22", "=B7/B8")
lab(ws, "A23", "Juros do mes");                                   fml(ws, "B23", "=B5*B6")
lab(ws, "A24", "Aluguel de competencia do mes");                  fml(ws, "B24", "=B15/B16")
lab(ws, "A25", "Materiais consumidos");                           fml(ws, "B25", "=B17-B18")
lab(ws, "A26", "Recebido a vista de servicos");                   fml(ws, "B26", "=B12*B13")
lab(ws, "A27", "Servicos a receber (clientes)");                  fml(ws, "B27", "=B12-B26")
lab(ws, "A28", "Despesa antecipada de aluguel (fevereiro)");      fml(ws, "B28", "=B15-B24")
ws.column_dimensions["A"].width = 48
ws.column_dimensions["B"].width = 14

# ---------------------------------------------------------------- Transacoes
ws = wb.create_sheet("Transacoes")
lab(ws, "A1", "Efeito de cada transacao de janeiro/2024 no Balanco, na DRE e no Caixa", bold=True)
heads = ["BP inicial 31/12/23", "T1a Servicos", "T1b Adiantamento", "T2 Aluguel", "T3 Materiais",
         "T4 Salarios", "T5 Depreciacao", "T6 Juros", "BP final 31/01/24"]
descs = ["Emprestimo de 54.000 vira equipamentos; economias de 10.000 viram capital",
         "Presta 8.000, recebe 20% a vista, 80% fica a receber",
         "Recebe 2.000 por servicos que so presta em marco",
         "Paga 2.200 de aluguel de janeiro e fevereiro",
         "Compra 3.000 a vista, sobra 1.300 em estoque",
         "Salario de 500 do mes, pago em fevereiro",
         "54.000 / 36 meses",
         "2% x 54.000, pagos so no fim de 2 anos",
         "Soma das colunas"]
COLS = [get_column_letter(i) for i in range(2, 11)]  # B..J
for col, h, d in zip(COLS, heads, descs):
    lab(ws, f"{col}2", h, bold=True, wrap=True, center=True)
    lab(ws, f"{col}3", d, wrap=True, italic=True)
    ws.column_dimensions[col].width = 16
ws.column_dimensions["A"].width = 50
ws.row_dimensions[3].height = 64
ws.freeze_panes = "B4"
TX = COLS[1:-1]  # C..I


def sum_row(row):
    fml(ws, f"J{row}", f"=SUM(B{row}:I{row})")


def all_cols(row, expr, bold=False, cols=COLS):
    for col in cols:
        fml(ws, f"{col}{row}", expr.replace("X", col), bold=bold)


# ATIVO
lab(ws, "A4", "ATIVO", bold=True)
lab(ws, "A5", "Caixa e bancos")
lnk(ws, "B5", "=Premissas!B9"); lnk(ws, "C5", "=Premissas!B26"); lnk(ws, "D5", "=Premissas!B14")
lnk(ws, "E5", "=-Premissas!B15"); lnk(ws, "F5", "=-Premissas!B17"); sum_row(5)
lab(ws, "A6", "Clientes (duplicatas a receber)");           lnk(ws, "C6", "=Premissas!B27"); sum_row(6)
lab(ws, "A7", "Estoque de materiais");                      lnk(ws, "F7", "=Premissas!B18"); sum_row(7)
lab(ws, "A8", "Despesas antecipadas (aluguel de fevereiro)"); lnk(ws, "E8", "=Premissas!B28"); sum_row(8)
lab(ws, "A9", "Ativo circulante", bold=True);               all_cols(9, "=SUM(X5:X8)", bold=True)
lab(ws, "A10", "Equipamentos");                             lnk(ws, "B10", "=Premissas!B7"); sum_row(10)
lab(ws, "A11", "(-) Depreciacao acumulada");                lnk(ws, "H11", "=-Premissas!B22"); sum_row(11)
lab(ws, "A12", "Ativo nao circulante (imobilizado liquido)", bold=True); all_cols(12, "=X10+X11", bold=True)
lab(ws, "A13", "TOTAL DO ATIVO", bold=True);                all_cols(13, "=X9+X12", bold=True)

# PASSIVO
lab(ws, "A15", "PASSIVO", bold=True)
lab(ws, "A16", "Salarios a pagar");                         lnk(ws, "G16", "=Premissas!B19"); sum_row(16)
lab(ws, "A17", "Receita antecipada (adiantamento de clientes)"); lnk(ws, "D17", "=Premissas!B14"); sum_row(17)
lab(ws, "A18", "Passivo circulante", bold=True);            all_cols(18, "=SUM(X16:X17)", bold=True)
lab(ws, "A19", "Emprestimo a pagar (vence dez/2025)");      lnk(ws, "B19", "=Premissas!B5"); sum_row(19)
lab(ws, "A20", "Juros a pagar (vencem com o principal)");   lnk(ws, "I20", "=Premissas!B23"); sum_row(20)
lab(ws, "A21", "Passivo nao circulante", bold=True);        all_cols(21, "=X19+X20", bold=True)
lab(ws, "A22", "TOTAL DO PASSIVO", bold=True);              all_cols(22, "=X18+X21", bold=True)

# PL
lab(ws, "A24", "PATRIMONIO LIQUIDO", bold=True)
lab(ws, "A25", "Capital social");                           lnk(ws, "B25", "=Premissas!B9"); sum_row(25)
lab(ws, "A26", "Lucros acumulados (resultado do mes)");     inp(ws, "B26", 0)
for col in TX:
    fml(ws, f"{col}26", f"={col}39")
sum_row(26)
lab(ws, "A27", "TOTAL DO PL", bold=True);                   all_cols(27, "=X25+X26", bold=True)
lab(ws, "A28", "PASSIVO + PL", bold=True);                  all_cols(28, "=X22+X27", bold=True)
lab(ws, "A29", "Check: Ativo - (Passivo + PL)", italic=True); all_cols(29, "=X13-X28")

# DRE
lab(ws, "A31", "DRE (regime de competencia)", bold=True)
lab(ws, "A32", "Receita de servicos");                      lnk(ws, "C32", "=Premissas!B12"); sum_row(32)
lab(ws, "A33", "(-) Aluguel");                              lnk(ws, "E33", "=-Premissas!B24"); sum_row(33)
lab(ws, "A34", "(-) Salarios e encargos");                  lnk(ws, "G34", "=-Premissas!B19"); sum_row(34)
lab(ws, "A35", "(-) Materiais consumidos");                 lnk(ws, "F35", "=-Premissas!B25"); sum_row(35)
lab(ws, "A36", "(-) Depreciacao dos equipamentos");         lnk(ws, "H36", "=-Premissas!B22"); sum_row(36)
lab(ws, "A37", "Resultado operacional (EBIT)", bold=True);  all_cols(37, "=SUM(X32:X36)", bold=True, cols=COLS[1:])
lab(ws, "A38", "(-) Juros do emprestimo (despesa financeira)"); lnk(ws, "I38", "=-Premissas!B23"); sum_row(38)
lab(ws, "A39", "LUCRO LIQUIDO DO MES", bold=True);          all_cols(39, "=X37+X38", bold=True, cols=COLS[1:])
lab(ws, "A40", "Check: lucro da DRE - variacao de lucros acumulados", italic=True); fml(ws, "J40", "=J39-(J26-B26)")

# CAIXA
lab(ws, "A42", "CAIXA (regime de caixa)", bold=True)
lab(ws, "A43", "Entradas");                                 lnk(ws, "C43", "=Premissas!B26"); lnk(ws, "D43", "=Premissas!B14"); sum_row(43)
lab(ws, "A44", "Saidas");                                   lnk(ws, "E44", "=-Premissas!B15"); lnk(ws, "F44", "=-Premissas!B17"); sum_row(44)
lab(ws, "A45", "Variacao de caixa", bold=True);             all_cols(45, "=X43+X44", bold=True, cols=COLS[1:])
lab(ws, "A46", "Caixa inicial");                            fml(ws, "J46", "=B5")
lab(ws, "A47", "Caixa final", bold=True);                   fml(ws, "J47", "=J46+J45", bold=True)
lab(ws, "A48", "Check: caixa final - caixa do BP final", italic=True); fml(ws, "J48", "=J47-J5")
lab(ws, "A49", "Check: variacao de caixa - movimento na conta Caixa", italic=True)
for col in TX:
    fml(ws, f"{col}49", f"={col}45-{col}5")
fml(ws, "J49", "=J45-(J5-B5)")

# ---------------------------------------------------------------- Comparativo
ws = wb.create_sheet("Comparativo")
lab(ws, "A1", "Tabela comparativa: Fluxo de Caixa (regime de caixa) x DRE (regime de competencia)", bold=True)
lab(ws, "B3", "Fluxo de Caixa (Regime de Caixa)", bold=True, wrap=True, center=True)
lab(ws, "C3", "DRE (Regime de Competencia)", bold=True, wrap=True, center=True)
ws.row_dimensions[3].height = 32
lab(ws, "A4", "Receitas/Entradas", bold=True)
lab(ws, "A5", "Servicos");                 lnk(ws, "B5", "=Premissas!B26");  lnk(ws, "C5", "=Premissas!B12")
lab(ws, "A6", "Adiantam. Serv.");          lnk(ws, "B6", "=Premissas!B14");  fml(ws, "C6", 0)
lab(ws, "A7", "Subtotal", bold=True);      fml(ws, "B7", "=SUM(B5:B6)", bold=True); fml(ws, "C7", "=SUM(C5:C6)", bold=True)
lab(ws, "A8", "Despesas/Saidas", bold=True)
lab(ws, "A9", "Aluguel");                  lnk(ws, "B9", "=-Premissas!B15"); lnk(ws, "C9", "=-Premissas!B24")
lab(ws, "A10", "Salarios");                fml(ws, "B10", 0);                lnk(ws, "C10", "=-Premissas!B19")
lab(ws, "A11", "Material");                lnk(ws, "B11", "=-Premissas!B17"); lnk(ws, "C11", "=-Premissas!B25")
lab(ws, "A12", "Depreciacao do Equipamento"); fml(ws, "B12", 0);             lnk(ws, "C12", "=-Premissas!B22")
lab(ws, "A13", "Juros");                   fml(ws, "B13", 0);                lnk(ws, "C13", "=-Premissas!B23")
lab(ws, "A14", "Subtotal", bold=True);     fml(ws, "B14", "=SUM(B9:B13)", bold=True); fml(ws, "C14", "=SUM(C9:C13)", bold=True)
lab(ws, "A15", "Lucro / Variacao no Caixa", bold=True); fml(ws, "B15", "=B7+B14", bold=True); fml(ws, "C15", "=C7+C14", bold=True)
lab(ws, "A17", "Check contra a aba Transacoes (deve dar zero)", italic=True)
lnk(ws, "B17", "=B15-Transacoes!J45"); lnk(ws, "C17", "=C15-Transacoes!J39")
lab(ws, "A19", "Lucro menos variacao de caixa (explicado na aba Reconciliacao)", italic=True)
fml(ws, "C19", "=C15-B15")
ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 22

# ---------------------------------------------------------------- Reconciliacao
ws = wb.create_sheet("Reconciliacao")
lab(ws, "A1", "Reconciliacao: do lucro (competencia) a variacao de caixa (regime de caixa), metodo indireto", bold=True)
lab(ws, "A3", "Lucro liquido do mes", bold=True);                         lnk(ws, "B3", "=Transacoes!J39", bold=True)
lab(ws, "A4", "(+) Despesas que nao sairam do caixa", italic=True)
lab(ws, "A5", "Depreciacao");                                             lnk(ws, "B5", "=-Transacoes!J36")
lab(ws, "A6", "Juros provisionados e nao pagos (aumento de juros a pagar)"); lnk(ws, "B6", "=Transacoes!J20-Transacoes!B20")
lab(ws, "A7", "(-/+) Variacao do capital de giro", italic=True)
lab(ws, "A8", "(-) Aumento de clientes");                                lnk(ws, "B8", "=-(Transacoes!J6-Transacoes!B6)")
lab(ws, "A9", "(-) Aumento de estoque");                                 lnk(ws, "B9", "=-(Transacoes!J7-Transacoes!B7)")
lab(ws, "A10", "(-) Aumento de despesas antecipadas");                   lnk(ws, "B10", "=-(Transacoes!J8-Transacoes!B8)")
lab(ws, "A11", "(+) Aumento de salarios a pagar");                       lnk(ws, "B11", "=Transacoes!J16-Transacoes!B16")
lab(ws, "A12", "(+) Aumento de receita antecipada");                     lnk(ws, "B12", "=Transacoes!J17-Transacoes!B17")
lab(ws, "A13", "Caixa gerado (utilizado) nas operacoes, FCO", bold=True); fml(ws, "B13", "=SUM(B3:B12)", bold=True)
lab(ws, "A14", "Caixa de investimento em janeiro (equipamentos comprados em 31/12)"); inp(ws, "B14", 0)
lab(ws, "A15", "Caixa de financiamento em janeiro (emprestimo e capital em 31/12)"); inp(ws, "B15", 0)
lab(ws, "A16", "Variacao de caixa (indireto)", bold=True);               fml(ws, "B16", "=B13+B14+B15", bold=True)
lab(ws, "A17", "Variacao de caixa pelo metodo direto (aba Transacoes)"); lnk(ws, "B17", "=Transacoes!J45")
lab(ws, "A18", "Check: indireto - direto (deve dar zero)", italic=True); fml(ws, "B18", "=B16-B17")
ws.column_dimensions["A"].width = 66
ws.column_dimensions["B"].width = 14

wb.save(OUT)
print("saved", OUT)
```

- [ ] **Step 2: Gerar a planilha**

Run:
```bash
python3 "$SCR/build_marcus_dent_xlsx.py"
```
Expected: `saved /Users/arthurmalucelli/FGV/10 Matérias/ContabilidadeFinanceira/Aulas/08.19/MarcusDentDFs.xlsx`

- [ ] **Step 3: Recalcular com LibreOffice (grava os valores das fórmulas no arquivo)**

Run:
```bash
cd "$XLSX_SCRIPTS" && python3 recalc.py "$AULA/MarcusDentDFs.xlsx" 60
```
Expected: JSON com `"status": "success"` e `"total_errors": 0`. Se aparecer erro de fórmula (`#REF!`, `#NAME?`), corrigir o gerador e repetir os passos 2 e 3.

- [ ] **Step 4: Rodar o verificador**

Run:
```bash
python3 "$SCR/verify_marcus_dent.py"
```
Expected: `54/54 checks OK`, exit 0. Qualquer `FAIL` indica fórmula errada no gerador: corrigir, regenerar, recalcular, verificar de novo.

- [ ] **Step 5: Inspeção visual rápida das células de Transacoes**

Run:
```bash
python3 -c "
import openpyxl
ws = openpyxl.load_workbook('$AULA/MarcusDentDFs.xlsx', data_only=True)['Transacoes']
for r in [5,6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,25,26,27,28,29,32,37,39,43,44,45,47]:
    print(r, str(ws[f'A{r}'].value)[:38].ljust(38), [ws.cell(row=r, column=c).value for c in range(2,11)])
"
```
Expected: linha 13 termina em 69700, linha 28 idem, linha 29 toda zero, linha 39 termina em 2120, linha 45 termina em -1600.

---

### Task 3: Resolução em markdown

**Files:**
- Create: `$AULA/ResolucaoCasoMarcusDent.md`

- [ ] **Step 1: Escrever o arquivo com este conteúdo exato**

````markdown
---
materia: ContabilidadeFinanceira
data: 2026-08-19
tema: Caso Marcus Dent, regime de caixa vs competência num mês de consultório
tags: [caso, resolucao]
---

# Caso Marcus Dent: resolução

Enunciado em `Slides/Atividade Marcus Dent 2024-2.pdf`. Planilha com tudo em fórmulas: `MarcusDentDFs.xlsx` nesta pasta. É o exercício de fechamento do tema 4 ([[Regime de Caixa]] vs [[Regime de Competência]]), na mesma linha do [[Caso Zezinho Pipoqueiro]], mas com o descasamento no sentido oposto.

## Respostas diretas

| Pergunta | Resposta |
|---|---|
| Lucro ou prejuízo de janeiro | **Lucro de $2.120** |
| Caixa gerado ou utilizado em janeiro | **Utilizou $1.600** (caixa de 10.000 para 8.400) |
| Balanço inicial (31/12/2023) | Total **$64.000** |
| Balanço final (31/01/2024) | Total **$69.700** |

Caixa caiu e lucro subiu. Os dois estão certos ao mesmo tempo: respondem a gatilhos diferentes.

## Balanço inicial (31/12/2023)

Três fatos antes de janeiro: empréstimo de 54.000, compra imediata dos equipamentos com esse dinheiro, depósito de 10.000 das economias como capital.

```
ATIVO                            PASSIVO + PL
Caixa e bancos        10.000     Empréstimo a pagar       54.000
Equipamentos          54.000     Capital social           10.000
Total                 64.000     Total                    64.000  ✓
```

Nada de receita, despesa ou depreciação ainda: os equipamentos chegaram em 31/12 e só começam a ser usados em janeiro.

## Mapa das transações de janeiro

Pra cada evento, as três perguntas do roteiro dos Treinos: mexeu no caixa? gerou receita ou consumiu recurso no mês? o que mudou no balanço?

| # | Evento | Caixa | DRE | Balanço |
|---|---|---|---|---|
| T1a | Serviços de 8.000, recebe 20% à vista | +1.600 | Receita 8.000 | [[Contas a Receber\|Clientes]] +6.400 |
| T1b | Adiantamento de 2.000 por serviços de março | +2.000 | nada | [[Adiantamento de Cliente\|Receita antecipada]] (passivo) +2.000 |
| T2 | Aluguel de janeiro e fevereiro, 2.200 pagos | (2.200) | Despesa (1.100) | [[Despesa Antecipada]] (ativo) +1.100 |
| T3 | Materiais 3.000 à vista, sobra 1.300 | (3.000) | Despesa (1.700) | [[Estoque]] +1.300 |
| T4 | Salário de 500, pago em fevereiro | nada | Despesa (500) | [[Contas a Pagar\|Salários a pagar]] +500 |
| T5 | [[Depreciação]]: 54.000 / 36 meses | nada | Despesa (1.500) | Depreciação acumulada (1.500) |
| T6 | Juros: 2% x 54.000 | nada | Despesa (1.080) | [[Juros a Pagar]] +1.080 |

Três eventos tocam o caixa num valor e a DRE em outro (T1b, T2, T3), e três tocam a DRE sem tocar o caixa (T4, T5, T6). Só T1a mexe nos dois, e mesmo assim em valores diferentes.

## Tabela comparativa (layout da professora)

| | Fluxo de Caixa (regime de caixa) | DRE (regime de competência) |
|---|---|---|
| **Receitas/Entradas** | | |
| Serviços | 1.600 | 8.000 |
| Adiantam. Serv. | 2.000 | 0 |
| Subtotal | 3.600 | 8.000 |
| **Despesas/Saídas** | | |
| Aluguel | (2.200) | (1.100) |
| Salários | 0 | (500) |
| Material | (3.000) | (1.700) |
| Depreciação do Equipamento | 0 | (1.500) |
| Juros | 0 | (1.080) |
| Subtotal | (5.200) | (5.880) |
| **Lucro / Variação no Caixa** | **(1.600)** | **2.120** |

## DRE de janeiro

```
Receita de serviços                    8.000
(-) Aluguel                           (1.100)   [2.200 pagos, só janeiro é competência]
(-) Salários e encargos                 (500)   [trabalhado em janeiro, pago em fevereiro]
(-) Materiais consumidos              (1.700)   [3.000 comprados, 1.300 ficaram em estoque]
(-) Depreciação dos equipamentos      (1.500)   [54.000 / 36]
= Resultado operacional (EBIT)         3.200
(-) Juros do empréstimo               (1.080)   [2% x 54.000, pagos só em dez/2025]
= Lucro líquido do mês                 2.120
```

Sem imposto de renda no caso. O [[EBIT]] de 3.200 mostra que a operação em si se paga; o [[Resultado Financeiro]] de (1.080) é o custo de ter financiado o equipamento com dívida em vez de capital.

## Fluxo de caixa de janeiro ([[Método Direto]])

```
Entradas
  Recebimento de clientes (20% de 8.000)      1.600
  Adiantamento de clientes                    2.000
Saídas
  Aluguel (janeiro e fevereiro)              (2.200)
  Materiais                                  (3.000)
= Caixa utilizado nas operações (FCO)        (1.600)
FCI em janeiro                                    0   [equipamentos comprados em 31/12]
FCF em janeiro                                    0   [empréstimo e capital em 31/12]
= Variação de caixa                          (1.600)
Caixa inicial 10.000, caixa final 8.400  ✓
```

## Balanço final (31/01/2024)

```
ATIVO                                    PASSIVO + PL
Circulante                               Circulante
  Caixa e bancos               8.400       Salários a pagar               500
  Clientes                     6.400       Receita antecipada           2.000
  Estoque de materiais         1.300     = Passivo circulante           2.500
  Despesas antecipadas         1.100     Não circulante
= Ativo circulante            17.200       Empréstimo a pagar          54.000
Não circulante                             Juros a pagar                1.080
  Equipamentos                54.000     = Passivo não circulante      55.080
  (-) Depreciação acumulada   (1.500)    Total do passivo              57.580
= Imobilizado líquido         52.500     Patrimônio líquido
                                           Capital social              10.000
                                           Lucros acumulados            2.120
                                         = PL                          12.120
Total                         69.700     Total                         69.700  ✓
```

Amarras: a [[Equação Patrimonial]] fecha (69.700 = 57.580 + 12.120); o lucro de 2.120 é exatamente a variação do PL (10.000 para 12.120), que vai pra [[Lucros Acumulados]] porque nada foi distribuído; o caixa do [[Balanço Patrimonial]] (8.400) é o caixa final da [[DFC]].

Classificação: empréstimo e juros vencem em dezembro de 2025, mais de 12 meses depois da data do balanço, então ficam no [[Passivo Não Circulante]]. Salários e receita antecipada se resolvem em fevereiro e março, [[Passivo Circulante]]. Equipamentos menos depreciação acumulada é o [[Imobilizado]] líquido, o único item do [[Ativo Não Circulante]]; todo o resto do ativo é [[Ativo Circulante]].

## Reconciliação: do lucro ao caixa ([[Método Indireto]])

Lucro 2.120 e caixa (1.600) diferem em 3.720. A ponte, item por item:

```
Lucro líquido do mês                                          2.120
(+) Depreciação (despesa sem saída de caixa)                  1.500
(+) Juros provisionados e não pagos                           1.080
(-) Aumento de clientes (80% da receita ainda não entrou)    (6.400)
(-) Aumento de estoque (comprou mais do que consumiu)        (1.300)
(-) Aumento de despesa antecipada (aluguel de fev já pago)   (1.100)
(+) Aumento de salários a pagar (despesa sem pagamento)         500
(+) Aumento de receita antecipada (caixa sem receita)         2.000
= Caixa utilizado nas operações                              (1.600)  ✓
```

Leitura: 2.580 de despesas que não saíram do caixa empurram pra cima; 8.800 de ativos de giro que cresceram (dinheiro travado em clientes, estoque e aluguel antecipado) puxam pra baixo; 2.500 de passivos de giro que cresceram (terceiros financiando o consultório) empurram pra cima de novo. 2.120 + 2.580 - 8.800 + 2.500 = (1.600). O [[Capital de Giro]] cresceu 6.300 no mês e engoliu o lucro inteiro e mais um pouco.

## Pegadinhas / pontos de prova

- Adiantamento não é receita. Os 2.000 entram no caixa e viram passivo (obrigação de prestar o serviço em março). Só viram receita quando o serviço for prestado. É o caso "antecipado" do slide de vendas x recebimento: afeta o caixa de agora e o lucro do futuro.
- Compra não é despesa. Comprou 3.000 de material, consumiu 1.700. A despesa é o consumo; os 1.300 que sobraram são ativo, não custo do mês. Mesma lógica do [[CMV]] do Zezinho em M2.
- Pagamento não é despesa. Pagou 2.200 de aluguel, mas só 1.100 competem a janeiro. Os outros 1.100 são despesa antecipada: afetam o caixa agora e o lucro de fevereiro.
- Despesa sem caixa, três vezes. Salário (paga em fevereiro), depreciação (o caixa já saiu em 31/12, na compra) e juros (só em dez/2025). As três reduzem o lucro de janeiro sem mexer um centavo do caixa do mês.
- Depreciação é consumo de riqueza. 54.000 / 36 = 1.500 por mês. O equipamento se desgasta a cada mês de uso, com ou sem pagamento. Mesma lógica do motoboy com a moto de 12.000 e vida útil de 48 meses.
- Juros correm desde o dia 1. 2% x 54.000 = 1.080 em janeiro, despesa financeira e juros a pagar, mesmo com pagamento só em dois anos. Em janeiro dá 1.080 tanto em juros simples quanto compostos; a diferença aparece a partir de fevereiro (2% sobre 55.080 no composto).
- [[Reconhecimento da Receita]] no fato gerador. Prestou 8.000, a DRE reconhece 8.000, no momento da prestação do serviço, não do recebimento nem do contrato. O que não entrou (6.400) vira clientes a receber e não reduz a receita.
- [[Confrontação]]: as despesas de janeiro (material consumido, aluguel de janeiro, salário do mês, depreciação, juros) são reconhecidas no mesmo mês da receita que ajudaram a gerar. É isso que a competência faz: casar esforço com benefício no mesmo período.
- Caixa caiu e ele ficou mais rico. Caixa de 10.000 para 8.400, PL de 10.000 para 12.120. A riqueza aumentou 2.120 e está espalhada em clientes, estoque e aluguel antecipado, não em dinheiro. Resposta direta à pergunta do slide 2: caixa subindo ou caindo não diz se está ficando mais rico.
- Inverso do Zezinho M1. Lá, caixa maior que lucro (despesas incorridas sem pagamento). Aqui, lucro maior que caixa (receita reconhecida sem recebimento e capital de giro crescendo). Os dois sentidos do descasamento.
- Equipamento comprado em 31/12 não entra no fluxo de caixa de janeiro. O FCI de janeiro é zero. Se a pergunta fosse "desde a abertura", aí sim: FCF +64.000 (empréstimo e capital), FCI (54.000).

## Pra fixar

[[Regime de Caixa]], [[Regime de Competência]], [[Reconhecimento da Receita]], [[Confrontação]], [[DRE]], [[DFC]], [[Balanço Patrimonial]], [[Equação Patrimonial]], [[Depreciação]], [[Despesa Antecipada]], [[Adiantamento de Cliente]], [[Contas a Receber]], [[Contas a Pagar]], [[Estoque]], [[Juros a Pagar]], [[Imobilizado]], [[Ativo Circulante]], [[Ativo Não Circulante]], [[Passivo Circulante]], [[Passivo Não Circulante]], [[EBIT]], [[Resultado Financeiro]], [[Método Direto]], [[Método Indireto]], [[Lucros Acumulados]], [[Capital de Giro]], [[Caso Marcus Dent]]
````

- [ ] **Step 2: Conferir regras de escrita**

Run:
```bash
grep -n "—" "$AULA/ResolucaoCasoMarcusDent.md"; grep -nE "\((i|ii|iii|iv)\)" "$AULA/ResolucaoCasoMarcusDent.md"; echo "exit ok se nada acima"
```
Expected: nenhuma linha listada (sem travessão, sem enumerador inline).

- [ ] **Step 3: Conferir que os números do md batem com a planilha**

Run:
```bash
grep -cE "2\.120|1\.600|69\.700|64\.000|17\.200|52\.500|55\.080|12\.120|3\.200|5\.880|5\.200|3\.600" "$AULA/ResolucaoCasoMarcusDent.md"
```
Expected: número maior ou igual a 15 (só confirma que os valores do gabarito estão presentes; a fonte de verdade numérica é o verificador da Task 2).

---

### Task 4: Notas de conceito novas

**Files:**
- Create: `$VAULT/20 Conhecimento/Conceitos/Caso Marcus Dent.md`
- Create: `$VAULT/20 Conhecimento/Conceitos/Passivo Circulante.md`
- Create: `$VAULT/20 Conhecimento/Conceitos/Passivo Não Circulante.md`
- Create: `$VAULT/20 Conhecimento/Conceitos/Imobilizado.md`
- Create: `$VAULT/20 Conhecimento/Conceitos/Juros a Pagar.md`
- Create: `$VAULT/20 Conhecimento/Conceitos/Reconhecimento da Receita.md`
- Create: `$VAULT/20 Conhecimento/Conceitos/Confrontação.md`
- Create: `$SCR/check_wikilinks.py`

Formato: o template `30 Sistema/Templates/Conceito.md` (YAML `tipo: conceito`, `materias: [ContabilidadeFinanceira]`, `tags: [conceito]`; seções Definição, Fórmula / aplicação, Onde aparece nas aulas com o bloco dataview, Conceitos relacionados). O bloco dataview é sempre este, sem alterar:

````
```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```
````

- [ ] **Step 1: Escrever o verificador de wikilinks**

```python
# /private/tmp/claude-501/-Users-arthurmalucelli/f53a9de1-4730-4235-a5cd-a3c9b3c48003/scratchpad/marcusdent/check_wikilinks.py
import glob
import os
import re
import sys

VAULT = os.path.expanduser("~/FGV")
TARGETS = [
    f"{VAULT}/10 Matérias/ContabilidadeFinanceira/Aulas/08.19/ResolucaoCasoMarcusDent.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Caso Marcus Dent.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Passivo Circulante.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Passivo Não Circulante.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Imobilizado.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Juros a Pagar.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Reconhecimento da Receita.md",
    f"{VAULT}/20 Conhecimento/Conceitos/Confrontação.md",
]
notes = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(f"{VAULT}/20 Conhecimento/Conceitos/*.md")}
# a resolução também pode ser alvo de link (Caso Marcus Dent aponta pra ela)
notes.add("ResolucaoCasoMarcusDent")

bad = []
for path in TARGETS:
    if not os.path.exists(path):
        bad.append((path, "<arquivo não existe>"))
        continue
    text = open(path, encoding="utf-8").read()
    for link in set(re.findall(r"\[\[([^\]|#\\]+)", text)):
        link = link.strip()
        if link and link not in notes:
            bad.append((os.path.basename(path), link))
for f, l in bad:
    print(f"BROKEN  {f}: [[{l}]]")
print("ok" if not bad else f"{len(bad)} problemas")
sys.exit(1 if bad else 0)
```

- [ ] **Step 2: Rodar e confirmar que falha (notas ainda não existem)**

Run:
```bash
python3 "$SCR/check_wikilinks.py"
```
Expected: sete linhas `BROKEN ... <arquivo não existe>` mais links quebrados da resolução (Juros a Pagar, Imobilizado, Passivo Circulante, Passivo Não Circulante, Reconhecimento da Receita, Confrontação, Caso Marcus Dent), exit 1.

- [ ] **Step 3: Escrever `Caso Marcus Dent.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito, caso, competencia-vs-caixa]
---

# Caso Marcus Dent

## Definição

Caso de ContabilidadeFinanceira (aula de 19/08) que fecha o tema 4, formas de apuração do resultado. Dentista recém-formado abre consultório em 31/12/2023 com empréstimo de 54.000 (2% ao mês, principal e juros pagos só em dois anos, dinheiro todo convertido em equipamentos) e 10.000 de capital próprio. Em janeiro de 2024 presta 8.000 de serviços recebendo só 20%, recebe 2.000 de adiantamento, paga aluguel de dois meses, compra material além do consumo, deve o salário do mês, deprecia o equipamento e acumula juros.

## O resultado

- Lucro de janeiro: 2.120 ([[Regime de Competência]])
- Caixa utilizado em janeiro: 1.600, de 10.000 pra 8.400 ([[Regime de Caixa]])
- Balanço de 64.000 na abertura pra 69.700 no fim do mês; PL de 10.000 pra 12.120

## Por que é central

- É o espelho do [[Caso Zezinho Pipoqueiro]] M1: lá o caixa supera o lucro, aqui o lucro supera o caixa
- Reúne num mês só os quatro descasamentos do slide de vendas x recebimento e consumo x pagamento: a prazo ([[Contas a Receber]], [[Contas a Pagar]]), antecipado ([[Adiantamento de Cliente]], [[Despesa Antecipada]]), mais [[Depreciação]] e [[Juros a Pagar]] como despesas sem caixa
- A reconciliação pelo [[Método Indireto]] mostra o [[Capital de Giro]] engolindo o lucro

## Material

Pasta `10 Matérias/ContabilidadeFinanceira/Aulas/08.19/`: enunciado em `Slides/`, [[ResolucaoCasoMarcusDent]] e `MarcusDentDFs.xlsx`.

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Regime de Competência]] e [[Regime de Caixa]]
- [[Reconhecimento da Receita]] e [[Confrontação]]
- [[Adiantamento de Cliente]] e [[Despesa Antecipada]]
- [[Depreciação]] e [[Juros a Pagar]]
- [[Método Indireto]]
````

- [ ] **Step 4: Escrever `Passivo Circulante.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---

# Passivo Circulante

## Definição

Obrigações que vencem em até 12 meses depois da data do balanço (ou dentro do ciclo operacional, se for mais longo). Fornecedores, salários a pagar, impostos a recolher, adiantamentos de clientes, parcela de empréstimo que vence no ano. É a parte do [[Passivo]] que compete com o [[Ativo Circulante]] pela liquidez de curto prazo.

## Fórmula / aplicação

```
Caso Marcus Dent, 31/01/2024:
Salários a pagar (vence em fevereiro)         500
Receita antecipada (serviço em março)       2.000
= Passivo circulante                        2.500

O empréstimo de 54.000 NÃO entra aqui: vence em dez/2025, mais de 12 meses.
Liquidez corrente = AC / PC = 17.200 / 2.500 = 6,9
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Passivo]]
- [[Passivo Não Circulante]]
- [[Ativo Circulante]]
- [[Capital de Giro]]
- [[Liquidez Corrente]]
- [[Contas a Pagar]]
- [[Adiantamento de Cliente]]
````

- [ ] **Step 5: Escrever `Passivo Não Circulante.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---

# Passivo Não Circulante

## Definição

Obrigações com vencimento depois de 12 meses da data do balanço: empréstimos e financiamentos de longo prazo, debêntures, juros que só vencem junto com o principal. A classificação é pela data de vencimento em relação à data do balanço, não pela natureza da dívida: a mesma dívida migra pro [[Passivo Circulante]] quando faltar menos de um ano.

## Fórmula / aplicação

```
Caso Marcus Dent, 31/01/2024 (empréstimo vence em 31/12/2025):
Empréstimo a pagar              54.000
Juros a pagar (vencem juntos)    1.080
= Passivo não circulante        55.080

Em 31/01/2025 a dívida inteira vira circulante (falta menos de 12 meses).
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Passivo]]
- [[Passivo Circulante]]
- [[Juros a Pagar]]
- [[Endividamento]]
````

- [ ] **Step 6: Escrever `Imobilizado.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---

# Imobilizado

## Definição

Bens tangíveis que a empresa usa na operação por mais de um ano e não pretende vender: máquinas, equipamentos, veículos, prédios, móveis. Grupo do [[Ativo Não Circulante]]. Entra pelo custo de aquisição e vai sendo reduzido pela [[Depreciação]] acumulada conforme é consumido. A compra é [[Capex]], não despesa; a despesa aparece mês a mês via depreciação.

## Fórmula / aplicação

```
Imobilizado líquido = custo de aquisição - depreciação acumulada

Caso Marcus Dent, 31/01/2024:
Equipamentos                 54.000
(-) Depreciação acumulada    (1.500)   [54.000 / 36 meses x 1 mês]
= Imobilizado líquido        52.500

Motoboy do slide: moto 12.000, vida útil 48 meses, 250 por mês.
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Ativo Não Circulante]]
- [[Depreciação]]
- [[Capex]]
````

- [ ] **Step 7: Escrever `Juros a Pagar.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---

# Juros a Pagar

## Definição

Passivo que registra juros já incorridos (o tempo passou, a dívida rendeu) e ainda não pagos. Pelo [[Regime de Competência]] a despesa financeira entra na [[DRE]] no período em que o dinheiro ficou emprestado, independente da data de pagamento; a contrapartida é este passivo. Caixa só sai quando paga. Mesma lógica de salários a pagar, aplicada ao custo da dívida.

## Fórmula / aplicação

```
Juros do período = principal x taxa do período

Caso Marcus Dent, janeiro/2024: 54.000 x 2% = 1.080
DRE: despesa financeira (1.080)  |  BP: juros a pagar +1.080  |  Caixa: zero

Pagamento só em dez/2025, junto com o principal: até lá o saldo cresce todo mês.
Em capitalização composta o juro de fevereiro já incide sobre 55.080.
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Resultado Financeiro]]
- [[Contas a Pagar]]
- [[Passivo Não Circulante]]
- [[Regime de Competência]]
````

- [ ] **Step 8: Escrever `Reconhecimento da Receita.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---

# Reconhecimento da Receita

## Definição

Regra do [[Regime de Competência]] que define quando a receita entra na [[DRE]]: no momento em que a empresa transfere os riscos e benefícios do bem ou serviço, na prática a entrega do produto ou a prestação do serviço. Não é o contrato, não é o recebimento. Recebido antes da entrega é [[Adiantamento de Cliente]] (passivo); entregue antes do recebimento é [[Contas a Receber]] (ativo).

## Fórmula / aplicação

```
Correta Ltda (slide): recebe em janeiro, deveria prestar em fevereiro, presta em março.
Receita em março, ponto final.

Caso Marcus Dent, janeiro/2024:
Serviços prestados 8.000 -> receita 8.000 (mesmo recebendo só 1.600)
Adiantamento 2.000 por serviço de março -> receita zero em janeiro
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Regime de Competência]]
- [[Confrontação]]
- [[Adiantamento de Cliente]]
- [[Contas a Receber]]
````

- [ ] **Step 9: Escrever `Confrontação.md`**

````markdown
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---

# Confrontação

## Definição

Segunda metade do [[Regime de Competência]]: as despesas são reconhecidas no mesmo período das receitas que ajudaram a gerar. Esforço e benefício no mesmo exercício. Por isso material comprado só vira despesa quando consumido, aluguel pago adiantado só vira despesa no mês de uso, salário entra no mês trabalhado mesmo pago depois, e o equipamento entra aos poucos via [[Depreciação]] ao longo da vida útil.

## Fórmula / aplicação

```
Caso Marcus Dent, janeiro/2024, despesas confrontadas com a receita de 8.000:
Aluguel de janeiro       1.100   (pagou 2.200, só metade é do mês)
Salário do mês             500   (paga em fevereiro)
Material consumido       1.700   (comprou 3.000, sobrou 1.300)
Depreciação              1.500   (54.000 / 36)
Juros do mês             1.080   (paga em dez/2025)
```

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Regime de Competência]]
- [[Reconhecimento da Receita]]
- [[Custo vs Despesa]]
- [[Depreciação]]
- [[Despesa Antecipada]]
````

- [ ] **Step 10: Rodar o verificador de wikilinks**

Run:
```bash
python3 "$SCR/check_wikilinks.py"
```
Expected: `ok`, exit 0. Se aparecer `BROKEN`, o nome do link não bate com um arquivo em `20 Conhecimento/Conceitos/` (acento, maiúscula, plural): corrigir o link, não criar nota duplicada.

---

### Task 5: Commit e confirmação

**Files:**
- Modify: repo git `~/FGV` (novos arquivos das tasks 2, 3 e 4, mais este plano)

- [ ] **Step 1: Conferir o estado da pasta e do git**

Run:
```bash
ls -la "$AULA" && cd "$VAULT" && git status --short
```
Expected: `ResolucaoCasoMarcusDent.md`, `MarcusDentDFs.xlsx` e `Slides/` na pasta; git lista os dois arquivos, as sete notas novas e o plano como untracked.

- [ ] **Step 2: Commit**

```bash
cd "$VAULT" && git add "10 Matérias/ContabilidadeFinanceira/Aulas/08.19/ResolucaoCasoMarcusDent.md" "10 Matérias/ContabilidadeFinanceira/Aulas/08.19/MarcusDentDFs.xlsx" "20 Conhecimento/Conceitos/Caso Marcus Dent.md" "20 Conhecimento/Conceitos/Passivo Circulante.md" "20 Conhecimento/Conceitos/Passivo Não Circulante.md" "20 Conhecimento/Conceitos/Imobilizado.md" "20 Conhecimento/Conceitos/Juros a Pagar.md" "20 Conhecimento/Conceitos/Reconhecimento da Receita.md" "20 Conhecimento/Conceitos/Confrontação.md" "30 Sistema/Specs/2026-08-19-caso-marcus-dent-plan.md" && git commit -q -m "contabilidade: resolução do caso Marcus Dent (19/08)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>" && git log --oneline -1
```
Expected: uma linha com o hash e a mensagem do commit.

- [ ] **Step 3: Confirmar pro Arthur**

Listar: os dois arquivos da pasta 08.19, as sete notas de conceito criadas, o resultado do verificador (54/54) e do check de wikilinks (ok), o hash do commit. Registrar que não houve task nem update de calendar (sem prazo e sem transcript). Apontar o link quebrado pré-existente em `20 Conhecimento/Conceitos/Caso Zezinho Pipoqueiro.md` (`[[ResolucaoCasoZezinhoA]]`, o arquivo se chama `ResolucaoCasoZezinho.md`) sem corrigir, conforme a regra de não tocar nota existente.
