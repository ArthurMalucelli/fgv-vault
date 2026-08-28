---
materias: [matematica-aplicada]
semestre: 2026.2
data: 2026-08-06
tipo: resumo
tema: Funções, Limites e Domínio
status: completo
contract_version: 1
tags: [resumo]
---

> [!info] Fontes
> Áudio da aula veio com falha de captação: este resumo cruza os fragmentos do transcript ([[Transcrito - Funções, Limites e Domínio]]), o slide 2 da professora e a tua anotação manual [[Limites - Introdução]].

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Função Potencial]] | Expoente fixo, base varia: f(x) = xⁿ. Cinco casos, cada um com domínio e gráfico próprios |
| [[Função Exponencial]] | Base fixa, expoente varia: f(x) = aˣ. Regras totalmente diferentes das potenciais, não misturar |
| [[Domínio de Função]] | Conjunto de x onde f está definida. Raiz de índice par exige radicando ≥ 0; expoente negativo exclui o zero |
| [[Função Composta]] | f(g(x)): aplica a regra da f com g(x) no lugar do x. Domínio se analisa na expressão já substituída |
| [[Limite (cálculo)]] | Comportamento de f(x) com x arbitrariamente perto de a, sem precisar de f(a) definida |
| [[Forma indeterminada]] | 0/0 na substituição direta. Não é resposta: é ordem de simplificar (fatoração ou conjugado) |
| [[Racionalização por conjugado]] | Multiplicar por 1 na forma conjugado/conjugado pra eliminar a raiz e cancelar o fator problemático |

## Domínio das funções potenciais (os 5 casos)

| Caso | Exemplo | Domínio |
|---|---|---|
| n par positivo | x², x⁴ | ℝ |
| n ímpar positivo | x, x³ | ℝ |
| n par negativo | x⁻² = 1/x² | ℝ menos {0} |
| n ímpar negativo | x⁻¹ = 1/x | ℝ menos {0} |
| n racional | x^(1/2) = √x | [0, +∞) |

## Fórmulas

Definição de limite (informal):

```
lim(x→a) f(x) = L
f(x) fica tão perto de L quanto se queira, tomando x suficientemente perto de a (x ≠ a)
```

Propriedades (valem se lim f e lim g existem; c constante):

```
1) lim [f + g] = lim f + lim g
2) lim [f − g] = lim f − lim g
3) lim c·f = c·lim f
4) lim [f·g] = lim f · lim g
5) lim [f/g] = lim f / lim g        SE lim g ≠ 0
6) lim [f]ⁿ = [lim f]ⁿ              n natural
7) lim ⁿ√f = ⁿ√(lim f)              SE lim f ≥ 0
8) lim ln(f) = ln(lim f)            SE lim f > 0
```

Existência: o limite existe quando os laterais coincidem, `lim(x→a⁻) f = lim(x→a⁺) f`.

Exemplo por fatoração:

```
lim(x→1) (x−1)/(x²−1) = lim(x→1) (x−1)/[(x+1)(x−1)] = lim(x→1) 1/(x+1) = 1/2
```

Exemplo por conjugado (exercício central da aula):

```
lim(x→0) (√(x²+16) − 4)/x²                      direto: 0/0
× (√(x²+16) + 4)/(√(x²+16) + 4)
= (x²+16−16) / (x²·(√(x²+16)+4))
= 1/(√(x²+16)+4) = 1/8
```

Aplicação (slide final): produção P(x) = (x²−9)/(x−3) com x → 3 kg de matéria prima:

```
lim(x→3) (x²−9)/(x−3) = lim(x→3) (x+3) = 6
```

Interpretação: perto de 3 kg de insumo, a produção se aproxima de 6 unidades, mesmo P(3) não sendo definida.

## Exemplos a) a h) do slide, resolvidos

Gabarito meu, pelas técnicas da aula (conferir se a professora divergir):

| Limite | Técnica | Resultado |
|---|---|---|
| a) lim(x→0) 9x⁶ − 6x² + 4 | substituição | 4 |
| b) lim(x→1) (x+5)¹⁰ | substituição | 6¹⁰ |
| c) lim(x→7) √(6x+7) | substituição (prop. 7) | 7 |
| d) lim(x→5) (x−5)/x | substituição, 0/5 | 0 |
| e) lim(x→6) (x²−12x+36)/(x−6) | fatora (x−6)² | 0 |
| f) lim(x→0) (x²+15x)/x | fatora x | 15 |
| g) lim(x→6) (x²−36)/(x−6) | fatora (x−6)(x+6) | 12 |
| h) lim(x→4) (√(x+5)−3)/(x−4) | conjugado | 1/6 |

## Pegadinhas / pontos de prova

- 0/0 não é zero, não é 1, não é infinito: é [[Forma indeterminada|forma indeterminada]], simplifica antes (fatoração ou conjugado).
- 0/k com k ≠ 0 dá simplesmente 0 (exemplo d). Só 0/0 indetermina. Não racionalizar à toa.
- O limite não exige a função definida no ponto: (x−1)/(x²−1) não existe em x = 1 e o limite lá é 1/2.
- Propriedade do quociente só separa os limites se o limite do denominador for diferente de zero.
- Raiz dentro do limite pede lim f ≥ 0; ln pede lim f > 0.
- Regra de [[Função Potencial|potencial]] (expoente fixo) não se aplica a [[Função Exponencial|exponencial]] (base fixa), e vice-versa.
- No conjugado, troca o sinal do termo com raiz e multiplica numerador E denominador.
- A ponte da aula: primeiro estimar por tabela de valores, depois "como calcular sem a tabela?". Saber os dois caminhos.

## Pra fixar

- [[Função Potencial]]
- [[Função Exponencial]]
- [[Domínio de Função]]
- [[Função Composta]]
- [[Limite (cálculo)]]
- [[Forma indeterminada]]
- [[Racionalização por conjugado]]

## Próxima aula

Slides 3 e 4 já estão baixados na pasta 08.18: limites infinitos e no infinito, continuidade, assíntotas horizontais e verticais. (Fonte: pasta da matéria, não fala da professora; o áudio não capturou anúncio de próxima aula.)
