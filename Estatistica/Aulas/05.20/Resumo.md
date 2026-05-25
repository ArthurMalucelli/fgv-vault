---
tipo: resumo
materia: Estatistica
data: 2026-05-20
tema: IC para média (parte 2), Z vs T, distribuição T de Student
tags: [resumo]
---

# Resumo: IC para média (parte 2), Z vs T, TLC

## Ideia central

Na aula passada o σ populacional era conhecido (irrealista). **Na vida real você nunca conhece σ, conhece S.** A solução muda em duas dimensões:

1. **Troca σ por S** na fórmula.
2. **Troca Z por T** (distribuição [[Distribuicao T de Student|T de Student]]) pra compensar o erro de ter trocado σ por S.

A simplificação prática: se n > 50, S é uma boa aproximação de σ, e T ≈ Z, então pode usar `Z · S / √n`. Se n ≤ 50, é **obrigatório T**.

## Conceitos-chave

| Item | O que é |
|------|---------|
| S (desvio padrão amostral) | Calculado da amostra, com denominador n − 1. Estimativa de σ |
| [[Distribuicao T de Student]] | Distribuição parecida com a normal, mas mais larga. Depende de γ E do n |
| [[Graus de liberdade]] | Para IC de média = n − 1. Parâmetro do T |
| [[Amostragem aleatoria simples]] | Suposição: cada elemento da população tem mesma chance de entrar na amostra |
| [[Teorema do limite central]] | Para n > 30, X̄ é aproximadamente normal independente do formato de X |

## Fórmula geral (sempre vale)

<pre>
IC_γ% = X̄ ± T_(α/2, n-1) · S / √n
</pre>

**Excel:**

<pre>
T_(α/2, n-1) = INV.T(1 − α/2; n − 1)
</pre>

Cuidado com o ponto. `INV.T` ≠ `INVT`. O `INVT` sem ponto é outra coisa no Excel.

## Quando dá pra usar Z (simplificação)

| Situação | Use |
|---|---|
| σ conhecido (qualquer n) | **Z** |
| σ desconhecido, n > 50 | **Z** aproxima (T ≈ Z), ou **T** se quiser ser rigoroso |
| σ desconhecido, n ≤ 50 | **T obrigatório** |
| σ desconhecido, n < 30, mas X é normal | **T** (X̄ é normal pela suposição, não pelo TLC) |

**Regra do Nelson**: *"Se você puser S, ponha T."* T sempre é tecnicamente certo, qualquer n.

## Suposições pra IC valer (X̄ tem que ser normal)

| Como garantir X̄ normal | Condição |
|---|---|
| X já é normal | Qualquer n (mesmo n = 8) |
| X é qualquer coisa | n > 30 (por [[Teorema do limite central|TLC]]) |

Mais: amostragem precisa ser **aleatória simples**. Senão não representa.

## Comparação numérica T vs Z (γ = 95%)

| n | T_(2,5%, n−1) | Z_(2,5%) | Diferença |
|---|---|---|---|
| 8 | bem maior que 1,96 | 1,96 | grande |
| 25 | 2,064 | 1,96 | ~5% |
| 36 | 2,03 | 1,96 | ~4% |
| 120 | 1,98 | 1,96 | ~1% |
| 36.000 | 1,96 | 1,96 | zero |

**Conclusão prática**: pra n > 50, dá pra usar Z sem problema (diferença irrelevante). Pra n pequeno, T é bem maior.

## Roteiro de cálculo (qualquer exercício de IC pra média)

1. Identifica γ → calcula α = 1 − γ → α/2.
2. **σ ou S?** Se σ → fórmula com Z. Se S → fórmula com T (ou Z aproximado se n > 50).
3. **n grande ou pequeno?** Se n > 50 com S, dá pra usar Z (aprox). Caso contrário, T.
4. **X̄ é normal?** Check: X é normal? OU n > 30? Se nenhum dos dois, NÃO dá pra construir IC.
5. Calcula T_(α/2, n−1) = `INV.T(1 − α/2; n − 1)` ou Z_(α/2) = `INV.NORM.P.N(1 − α/2)`.
6. E = T · S / √n (ou Z · σ / √n).
7. IC = X̄ ± E.

## Exemplos da aula

### Exemplo 1: paulistanos (n grande, σ desconhecido)

n = 180, X̄ = 67 min, S = 17 min, γ = 95%.

Como n = 180 > 50, dá pra usar Z trocando σ por S:

```
E = 1,96 · 17 / √180
  = 1,96 · 17 / 13,42
  ≈ 2,48 min

IC_95% = 67 ± 2,48 = [64,52 ; 69,48] min
```

Suposições: TLC (n = 180) garante X̄ normal + amostragem aleatória simples.

### Exemplo 2: loja (n pequeno, X normal)

n = 25, X̄ = 18 min, S = 6 min, γ = 95%. Enunciado fala que X é normal.

n = 25 < 50, então T obrigatório:

```
T_(2,5%, 24) = INV.T(0,975; 24) ≈ 2,064

E = 2,064 · 6 / √25
  = 2,064 · 1,2
  ≈ 2,48 min

IC_95% = 18 ± 2,48 = [15,52 ; 20,48] min
```

Por que vale com n = 25 (menor que 30)? Porque X já é normal pelo enunciado → X̄ é normal pra qualquer n. Não preciso do TLC.

## Exercícios conceituais (verdadeiro/falso)

| Afirmação | Resposta |
|---|---|
| Quanto maior σ, **menor** a margem de erro | **F** (é o contrário, E ∝ σ) |
| Quanto maior γ, maior a margem de erro | **V** (Z sobe → E sobe) |
| Se n < 30, intervalo é inválido | **F** (vale se X é normal, mesmo n = 8) |
| Quadruplicar n divide E pela metade | **V** (E ∝ 1/√n) |

E mais o exercício 2:

> "Quando σ é desconhecido (caso real), qual usar?"

| Alternativa | Veredito |
|---|---|
| Usar T qualquer n | ✅ **certo** (T sempre é o tecnicamente correto) |
| T ou Z indiferente | ❌ (similares só pra n grande) |
| Z qualquer n | ❌ (só pra n > 50) |
| Z se n pequeno | ❌ (é o contrário) |
| T só se n grande | ❌ (T pra qualquer n; pra n grande Z também serve) |

## Pegadinhas / pontos de prova

- **Probabilidade de X̄ estar dentro do IC = 100%** (o IC é construído ao redor do X̄). Nelson já cobrou em prova.
- **"95% de confiança" não é "95% de chance do μ estar nesse IC específico".** O μ é fixo. A aleatoriedade está no procedimento: 95% dos ICs construídos assim contêm o μ.
- **σ ≠ S.** σ é o desvio padrão populacional (raramente conhecido). S é o amostral (sempre calculável a partir da amostra).
- **`INV.T` ≠ `INVT`.** Sem o ponto, é outra função no Excel. Conferir.
- **Graus de liberdade = n − 1** pra IC de média. Não confundir com n.
- **n = 50 é convenção do livro de vocês.** Outros livros usam 30 ou 100. Não é número mágico.
- **n pequeno + X normal = T obrigatório**, mas vale (X̄ é normal pela suposição). Não é violação.
- **n pequeno + X não-normal = não dá IC.** Nem T salva.
- **Suposição de amostragem aleatória simples.** Se a amostra é viciada (só amigos, só os que chegam rápido), o IC não representa nada.

## Pra fixar

- [[Distribuicao T de Student]]
- [[Graus de liberdade]]
- [[Amostragem aleatoria simples]]
- [[Intervalo de Confiança]]
- [[Margem de Erro]]
- [[Teorema do limite central]]
- [[Z de alfa sobre 2]]
- [[Distribuicao normal]]
- [[Tamanho da amostra]]
- [[Estimacao por intervalo]]

## Próxima aula (quarta 27/05)

**IC para proporção.** Caso clássico de pesquisa eleitoral ("candidato A com 30%, margem de 2 pontos"). Vai ser a quarta provinha no mesmo dia.

## Aviso administrativo

- **Quarta 27/05**: IC pra proporção + quarta provinha (estilo de sempre). Nelson disse que **não vai arredondar feito maluco** dessa vez, então pra cada cálculo vale a regra de arredondar pra cima (convenção dos estatísticos).
- **Última aula**: apresentações (data ambígua no transcript, Nelson explicou no final da aula).
