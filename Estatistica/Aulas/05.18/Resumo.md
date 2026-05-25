---
materia: Estatistica
data: 2026-05-18
tema: Intervalo de Confiança para a média (parte 1)
tags: [resumo]
---

# Resumo: Intervalo de Confiança para a média (parte 1)

## Ideia central

Em vez de dizer "μ é parecido com X̄" ([[Estimacao por ponto|estimativa por ponto]]), você diz "μ está dentro de X̄ ± E com γ% de confiança" ([[Estimacao por intervalo|estimativa intervalar]]). Mesma lógica de pesquisa eleitoral ("candidato A com 20%, margem de 2 pontos").

**Interpretação correta**: se você tirasse muitas amostras e construísse o intervalo X̄ ± E em cada uma, **γ% dos intervalos** conteriam o μ verdadeiro. Como você só tira uma amostra na prática, fala que esse intervalo tem γ% de confiança de incluir o μ.

## Conceitos-chave

| Item | O que é |
|------|---------|
| [[Intervalo de Confiança]] | Faixa X̄ ± E construída em torno da média amostral, com γ% de confiança de conter o μ |
| [[Margem de Erro]] | E. Tamanho do "bracinho" para cada lado de X̄. E = Z_(α/2) · σ/√n |
| [[Nivel de Confianca]] | γ. Probabilidade do intervalo conter o μ. Tipicamente 90, 95 ou 99% |
| α | Complemento de γ. α = 1 − γ. É a chance do intervalo errar |
| [[Z de alfa sobre 2]] | Quantos desvios padrão da normal padrão deixam α/2 na cauda direita |
| [[Estimacao por ponto]] | Dar um número só: "μ ≈ X̄" |
| [[Estimacao por intervalo]] | Dar uma faixa: "μ ∈ [X̄ − E, X̄ + E]" com γ% de confiança |
| [[Tamanho da amostra]] | n. Quanto maior, menor a margem de erro (raiz quadrada) |
| σ populacional conhecido | Premissa irrealista, vale só nesta primeira aula. Próxima aula supera |

## Fórmulas

**Margem de erro (IC pra média, σ conhecido):**

<pre>
E = Z_(α/2) · σ / √n
</pre>

**Intervalo de confiança:**

<pre>
IC_γ% = X̄ ± E = [X̄ − E ; X̄ + E]
</pre>

**Tamanho de amostra (invertendo a fórmula):**

<pre>
n = (Z_(α/2) · σ / E)²
</pre>

Sempre **arredonda pra cima**, mesmo que dê vírgula 01.

**Excel:**

<pre>
Z_(α/2)  = INV.NORM.P.N(1 − α/2)
         = INV.NORM(1 − α/2; 0; 1)
</pre>

## Tabela de Z mágicos (decora 1,96 e 1,645)

| γ | α | α/2 | Z_(α/2) |
|---|---|-----|---------|
| 90% | 10% | 5% | **1,645** |
| 95% | 5% | 2,5% | **1,96** |
| 99% | 1% | 0,5% | 2,58 |

## Roteiro de cálculo (qualquer exercício)

1. Pega γ no enunciado
2. α = 1 − γ
3. α/2
4. Z_(α/2) = `INV.NORM.P.N(1 − α/2)`
5. Aplica a fórmula que o exercício pede:
   - Pediu IC? → E = Z · σ/√n, depois IC = X̄ ± E
   - Pediu n? → n = (Z · σ / E)², arredonda pra cima

## Trade-offs (essência da aula)

Você manipula 3 alavancas: γ (confiança), n (custo) e E (precisão). Não dá pra fixar duas e melhorar a terceira sem mexer em alguma:

| Quero… | Custo |
|--------|-------|
| **Aumentar γ** (mais confiança) | Z sobe → E aumenta. Pra manter E, n tem que subir |
| **Diminuir E** (mais precisão) | n tem que subir **ao quadrado**. Cortar E pela metade quadruplica n |
| **Diminuir n** (menos custo) | E aumenta (perde precisão) ou γ cai (perde confiança) |

A relação `n ∝ 1/E²` é a coisa cruel: pesquisa precisa fica muito cara muito rápido.

## Exemplos da aula

**Parque SP, planejamento (σ = 100, n = 400, γ = 95%):**

```
E = 1,96 · 100/√400 = 1,96 · 5 ≈ 10
```

Bracinho de R$ 10 antes mesmo de fazer a pesquisa.

**Mesma pesquisa, depois de feita (X̄ = 34,20):**

```
IC₉₅% = 34,20 ± 10 = [24,20 ; 44,20]
```

**Quero E = 5 (metade), mesma confiança:**

```
n = (1,96 · 100/5)² = 1.537 (quadruplica)
```

**Mesmo E = 5, mas baixo γ pra 90%:**

```
n = (1,645 · 100/5)² ≈ 1.083 (alívio modesto)
```

**Aviação (σ = 6, n = 64, X̄ = 15,2, γ = 95%):**

```
E = 1,96 · 6/√64 = 1,96 · 0,75 = 1,47
IC₉₅% = 15,2 ± 1,47 = [13,73 ; 16,67] assentos
```

**Aviação, quero E = 1:**

```
n = (1,96 · 6/1)² ≈ 138,29 → 139 voos
```

## Pegadinhas / pontos de prova

- **`INV.NORM.P.N(1 − α/2)` usa μ=0, σ=1, mas isso é só artifício pra obter Z_(α/2).** Não tem nada a ver com a média e o desvio padrão do problema. Z é uma constante adimensional.
- **Confundir nível de confiança γ com α.** γ é o tamanho da área azul (95%, 90%…). α = 1 − γ é a chance do intervalo errar. α/2 é a cauda de cada lado.
- **Esquecer de dividir por √n.** A fórmula é σ/√n (erro padrão), não σ direto. σ direto é dispersão de X individual; σ/√n é dispersão de X̄.
- **Não arredondar pra cima no n.** Se dá 138,29, é 139, não 138. Convenção dos estatísticos.
- **Achar que "95% de confiança" significa "95% de chance do μ estar nesse intervalo específico".** Errado tecnicamente. O μ é fixo (parâmetro populacional), não tem probabilidade. O que tem 95% é o procedimento: 95% dos intervalos construídos assim incluem o μ.
- **Aplicar a fórmula sem checar suposições.** Precisa de X̄ normal (X normal OU n > 30) e σ populacional conhecido (irrealista, próxima aula resolve).
- **Margem de erro só faz sentido relativa à grandeza.** E = 10 é gigante se X̄ ≈ 7, mas é razoável se X̄ ≈ 60.
- **Decorar errado o 1,645.** Pra γ = 90%, é 1,645 (não 1,65, não 1,64). Pra γ = 99%, é 2,58.

## Pra fixar

- [[Intervalo de Confiança]]
- [[Margem de Erro]]
- [[Z de alfa sobre 2]]
- [[Nivel de Confianca]]
- [[Tamanho da amostra]]
- [[Estimacao por ponto]]
- [[Estimacao por intervalo]]
- [[Distribuicao amostral da media]]
- [[Erro padrao]]
- [[Teorema do limite central]]

## Próxima aula

Parte 2 do IC pra média: **σ populacional desconhecido** (o caso real, 99% dos casos). Vai usar o S (desvio padrão amostral) no lugar de σ, e provavelmente vai aparecer a distribuição t de Student. Daqui a duas aulas, IC pra **proporção** (caso de pesquisa eleitoral).

## Aviso administrativo

**Prova final: 8 de junho, 15h.** Nelson recomenda fortemente não deixar pra segunda chamada (que é mais difícil por design).

## Bônus: comentário do Nelson sobre IA

Nelson reconhece o uso de IA como professor particular como **útil** (esclarece dúvida, contexto restringível). O que ele criticou foi:

1. **E-mail formal escrito 100% por IA**, que apaga a voz do aluno
2. **Pular o desafio da "página em branco"** nos exercícios

Mensagem: IA é ferramenta tipo calculadora ou Excel. Mas se você terceiriza a habilidade de pensar/escrever do zero, o empregador não tem motivo pra te contratar (ele usa IA direto). Não confundir uso instrumental com dependência.
