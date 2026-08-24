---
tipo: conceito
materias: [ComportamentoDoConsumidor, IntroducaoAGestao]
tags: [conceito, ideacao, metodologia]
---

# How Might We

## Definição

Técnica de reenquadramento de problemas em perguntas abertas, formato "Como poderíamos...?". Usada na transição entre Define e Ideate do [[Design Thinking]] pra abrir espaço de soluções sem prescrever direção.

## Lógica

Cada palavra carrega sinal:
- **How**: assume que existe solução, foca em descobrir
- **Might**: indica que as ideias são possibilidades, reduz pressão de "estar certo"
- **We**: enquadra como esforço coletivo

## Como construir

1. Partir de uma dor identificada na fase Empathize ([[Mapa de Empatia]])
2. Reformular como pergunta "Como poderíamos..."
3. Calibrar amplitude: muito amplo gera ideias genéricas, muito estreito limita criatividade

Exemplo, dor: "consumidor desconfia de marcas sustentáveis sem evidência". HMW: "Como poderíamos transformar discurso de sustentabilidade em prova verificável durante a compra?"

## Onde aparece nas aulas

```dataview
LIST
FROM "ComportamentoDoConsumidor" OR "IntroducaoAGestao"
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[Design Thinking]]
- [[Brainstorming]]
- [[SCAMPER]]
- [[Mapa de Empatia]]
