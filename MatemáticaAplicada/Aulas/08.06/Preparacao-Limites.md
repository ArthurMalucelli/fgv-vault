---
materia: MatemáticaAplicada
data: 2026-08-06
tema: Introdução a Limites
tags: [preparacao, limites, pre-calculo]
---

# Preparação — Aula 2: Introdução a Limites

## O que é limite (conceito central)

Limite é o valor que uma função **se aproxima** quando x se aproxima de um ponto, independente do que acontece *exatamente* naquele ponto.

Notação: lim(x→a) f(x) = L

Lê-se: "o limite de f(x) quando x tende a a é L"

**Exemplo intuitivo:**
- f(x) = (x² - 1)/(x - 1)
- Em x = 1 a função não existe (0/0)
- Mas quando x se aproxima de 1, f(x) se aproxima de 2
- Portanto: lim(x→1) (x²-1)/(x-1) = 2
- (Simplificando: (x-1)(x+1)/(x-1) = x+1 → em x=1 dá 2)

---

## Pré-cálculo necessário pra hoje

A Larissa vai usar funções o tempo todo pra construir limites. Revisão rápida:

### Funções polinomiais
- f(x) = 3x² - 2x + 1
- Para calcular limite: basta substituir x = a diretamente (quando não gera 0/0)
- lim(x→2) (3x² - 2x + 1) = 3(4) - 2(2) + 1 = **9**

### Funções racionais (fração de polinômios)
- f(x) = (x² - 4)/(x - 2)
- Problema quando denominador = 0
- Fatorar: (x-2)(x+2)/(x-2) = x + 2
- lim(x→2) = 4

### Fatoração que você precisa saber
- Diferença de quadrados: x² - a² = (x-a)(x+a)
- Trinômio: x² + bx + c = (x + r)(x + s) onde r·s = c e r+s = b

---

## Técnicas de limite (o que vai aparecer hoje)

### 1. Substituição direta
Se f(a) existe e não dá 0/0: substitui e calcula.

lim(x→3) (x² + 2) = 9 + 2 = **11**

### 2. Indeterminação 0/0 → fatorar
Quando substituir dá 0/0, fatorar o numerador e cancelar.

lim(x→2) (x² - 4)/(x - 2) = lim (x+2)(x-2)/(x-2) = lim (x+2) = **4**

### 3. Limites laterais
- Limite pela esquerda: lim(x→a⁻) f(x)
- Limite pela direita: lim(x→a⁺) f(x)
- O limite **existe** só se os dois lados dão o mesmo valor

### 4. Quando o limite não existe
- Os dois lados dão valores diferentes
- A função oscila infinitamente
- A função vai para ±∞

---

## Exercícios de aquecimento

Tenta resolver antes de olhar a resposta. É o tipo que vai aparecer na Atividade 1 (11/08).

**1.** lim(x→2) (3x - 1) = ?

**2.** lim(x→3) (x² - 9)/(x - 3) = ?

**3.** lim(x→1) (x² - 1)/(x - 1) = ?

**4.** lim(x→0) (x² + 3x)/x = ?

**5.** f(x) = { 2x+1 se x < 2 ; x² se x ≥ 2 }
   Calcule lim(x→2⁻) e lim(x→2⁺). O limite existe?

---

## Gabarito

1. lim(x→2) (3x-1) = 3(2)-1 = **5** (substituição direta)

2. lim(x→3) (x²-9)/(x-3) = lim (x+3)(x-3)/(x-3) = lim (x+3) = **6**

3. lim(x→1) (x²-1)/(x-1) = lim (x+1)(x-1)/(x-1) = lim (x+1) = **2**

4. lim(x→0) (x²+3x)/x = lim x(x+3)/x = lim (x+3) = **3**

5. lim(x→2⁻) = 2(2)+1 = **5** ; lim(x→2⁺) = 2² = **4** → lados diferentes → **limite não existe**

---

## O que esperar na aula de hoje

A Larissa vai construir a ideia de limite intuitivamente, provavelmente com exemplos gráficos e numéricos (tabela de valores de f(x) quando x se aproxima de um ponto). A formalização vem depois.

Foco: entender **o que limite significa**, não a definição épsilon-delta (isso não cai na graduação de Adm).

## Próxima cobrança

⚠️ **11/08 — Atividade 1 em sala (Pré-Cálculo, individual)**
Conteúdo: domínio/imagem, funções lineares, quadráticas, potência, exponenciais, logarítmicas.
Material: `Exercícios-NivelamentodeMatemática.pdf` no Eclass.
