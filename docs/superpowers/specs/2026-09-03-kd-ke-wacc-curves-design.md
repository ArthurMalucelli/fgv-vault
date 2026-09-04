# Design: curvas de Kd, Ke e WACC

## Objetivo

Criar um visual didático que mostre como o custo da dívida, o custo do equity e o WACC variam conforme aumenta o endividamento. O material deve combinar leitura conceitual com uma simulação numérica ilustrativa, sem sugerir que os valores representam uma empresa real.

## Entregáveis

- `CurvasKdKeWacc.png`, com 2.400 por 960 pixels, para leitura e compartilhamento.
- `CurvasKdKeWacc.svg`, em formato vetorial para ampliação sem perda de qualidade.

Os dois arquivos serão salvos em `Vault/Attachments/`.

## Composição aprovada

O visual terá três gráficos separados, dispostos lado a lado em um canvas horizontal fixo:

- Curva do Kd.
- Curva do Ke.
- Curva do WACC.

Os três painéis usarão o mesmo eixo horizontal, com dívida sobre valor total, `D/V`, variando de 0% a 80%. Os eixos verticais poderão ter intervalos diferentes para tornar cada formato legível. Uma nota explícita informará que as escalas verticais são independentes.

## Premissas numéricas

Seja `x = D/V`, com `x` entre `0` e `0,80`.

```text
T = 25%
Rf = 5,0%
Prêmio de mercado = 7,78%
Beta desalavancado = 0,90

D/E = x / (1 - x)

Kd bruto(x) = 6,0% + 2,0% × x
              + 20,0% × [máx(0, x - 0,40) / 0,40]²

Kd líquido(x) = Kd bruto(x) × (1 - T)

Beta alavancado(x) = 0,90 × [1 + (1 - T) × D/E]

Ke(x) = Rf + Beta alavancado(x) × Prêmio de mercado

WACC(x) = (1 - x) × Ke(x) + x × Kd bruto(x) × (1 - T)
```

Com essas premissas, o WACC começa próximo de 12,0%, atinge um mínimo de aproximadamente 11,33% em `D/V` próximo de 41,3% e sobe de forma acentuada em níveis elevados de dívida. O mínimo será calculado por otimização contínua no intervalo de 0% a 80%, não pela escolha do menor ponto de uma grade discreta.

## Conteúdo de cada painel

### Kd

- Linha azul contínua para o Kd bruto.
- Linha azul tracejada para `Kd(1 - T)`, que entra no WACC.
- Anotação da região quase plana, onde o risco de crédito é contido.
- Anotação da região convexa, onde o spread de crédito aumenta.

### Ke

- Linha laranja contínua.
- Ponto inicial próximo de 12,0% quando `D/V = 0%`.
- Anotação explicando que o risco residual se concentra nos acionistas.
- Aceleração visível em níveis elevados de alavancagem.

### WACC

- Linha verde contínua.
- Curva em U no modelo ilustrativo.
- Marcador e linha vertical no mínimo calculado numericamente.
- Região anterior ao mínimo identificada como predominância do benefício fiscal.
- Região posterior ao mínimo identificada como predominância do risco financeiro.

## Linguagem visual

- Fundo claro adequado para leitura e impressão.
- Azul para dívida, laranja para equity e verde para WACC.
- Grade discreta e eixos em percentuais.
- Título geral: `Curvas de Kd, Ke e WACC versus endividamento`.
- Subtítulo: `Simulação didática com premissas ilustrativas`.
- Rodapé: `Curvas ilustrativas. Neste modelo, o formato em U resulta do benefício fiscal da dívida e do aumento assumido nos custos de dívida e equity em alta alavancagem.`
- Nenhuma fonte externa ou referência bibliográfica.

## Precisão conceitual

- O gráfico não apresentará a curva em U como uma lei universal.
- O Kd líquido será diferenciado do Kd bruto.
- O ponto ótimo será definido como o mínimo do WACC, não como igualdade entre Kd e Ke.
- O visual indicará que a relação depende das premissas escolhidas.

## Verificação

- Recalcular o WACC diretamente a partir de Kd, Ke, pesos e imposto em todos os pontos.
- Calcular o mínimo contínuo do WACC no intervalo de 0% a 80% e confirmar resultado próximo de `D/V = 41,2871%` e `WACC = 11,3349%`.
- Confirmar que o marcador do ponto ótimo coincide com esse mínimo contínuo.
- Verificar os valores inicial, mínimo e final da curva.
- Inspecionar o PNG renderizado para detectar rótulos cortados, sobreposição e baixa legibilidade.
- Validar que o SVG abre corretamente e contém os três painéis.

## Fora do escopo

- Estimar a estrutura ótima de uma empresa real.
- Usar dados de mercado ou ratings de crédito.
- Produzir uma planilha de valuation.
- Comparar diferentes regimes tributários.
