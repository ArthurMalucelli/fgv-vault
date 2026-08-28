---
materias: [matematica-aplicada]
semestre: 2026.2
data: 2026-08-18
tipo: resumo
tema: Limite fundamental, continuidade e assíntotas
status: completo
contract_version: 1
tags: [resumo]
---

# Resumo — 1^∞, continuidade e assíntotas

| Item | O que é |
|---|---|
| [[Forma indeterminada]] 1^∞ | Base que TENDE a 1 (1 + algo→0) elevada ao infinito é indeterminação; resolve pelo limite fundamental exponencial. Base exatamente 1 daria 1, mas não é o caso |
| [[Limite no Infinito]] | Comportamento no longo prazo; termos de menor grau somem, sobra o dominante (ex.: computadores → 50) |
| [[Continuidade]] em x = a | Precisa de: f(a) existe, limite em a existe, e limite = f(a). Intuição: gráfico sem tirar o lápis do papel |
| Descontinuidade removível | Limite existe (ex.: 3) mas f(2) não definida → basta definir f(2) = 3 pra tornar contínua |
| [[Assíntota Vertical]] | Só em RESTRIÇÃO de domínio; limite lateral no ponto dá ±∞ → tem; dá número → não tem; pode haver várias (uma por restrição) |
| [[Assíntota Horizontal]] | Reta y = L com L = limite no infinito; gráfico encosta sem tocar |

## Fórmulas

```
Contínua em a  ⟺  f(a) existe  ∧  lim(x→a) f(x) existe  ∧  lim(x→a) f(x) = f(a)
Assíntota vertical em x = a:  a fora do domínio  ∧  lim(x→a±) f(x) = ±∞
Assíntota horizontal:  y = L  onde  L = lim(x→±∞) f(x)
1^∞, 0/0, ∞/∞, ∞−∞  →  indeterminações (manipular antes de concluir)
```

## Pegadinhas / pontos de prova

- Ponto DENTRO do domínio nunca dá assíntota vertical: não perder tempo calculando.
- Limite existir no ponto NÃO garante continuidade: falta f(a) existir e ser igual.
- Candidata a assíntota vertical exige olhar os DOIS limites laterais.
- 1^∞ não é 1: cair nessa é erro clássico de prova.

## Próxima aula

- Derivadas (tem videoaula cobrindo a introdução).

## Pra fixar

- [[Continuidade]]
- [[Assíntota Vertical]]
- [[Assíntota Horizontal]]
- [[Forma indeterminada]]
- [[Limite no Infinito]]
- [[Limites Laterais]]
