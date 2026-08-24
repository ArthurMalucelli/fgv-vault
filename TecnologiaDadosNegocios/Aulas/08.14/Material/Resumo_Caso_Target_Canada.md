# Caso Target Canada — Resumo

**Fonte:** Laudon & Laudon, 2020  
**Matéria:** TDN — Aula 2 (14/08/2026)  
**Tema:** Falha de sistemas de informação e gestão de cadeia de suprimentos

---

## O que aconteceu

A Target tentou entrar no Canadá em 2013, adquirindo 189 locais da rede Zellers por US$ 1,8 bi e abrindo 133 lojas. Em janeiro de 2015, com US$ 7 bilhões gastos, entrou com pedido de falência e fechou tudo — 17.600 demitidos, lucro projetado apenas para 2021.

## Causa raiz: dados ruins no SAP

A Target escolheu implementar o SAP (novo, nunca usado internamente) em apenas 2 anos — tempo irreal para uma implantação desse porte. Fornecedores foram pressionados a cadastrar ~75.000 produtos às pressas. Resultado: **apenas 30% de precisão nos dados** (vs. 98–99% no padrão de mercado).

Erros concretos:
- Dimensões em polegadas no lugar de centímetros (ou na ordem errada)
- Moedas trocadas (CAD vs. USD)
- Largura cadastrada no campo de comprimento
- Campos obrigatórios em branco ou com typos

## Efeito cascata nos sistemas

| Sistema | Problema |
|---|---|
| **SAP (ERP)** | Dados sujos → pedidos errados, itens não alocados nas prateleiras |
| **Manhattan (WMS)** | Não se comunicava bem com SAP → embalagens "inexistentes" para o sistema |
| **JDA (previsão de demanda)** | Sem histórico de vendas, usou projeções otimistas baseadas em lojas dos EUA |
| **Reposição automática** | Desligado manualmente por analistas para maquiar KPIs |
| **POS (Retalix)** | Travava, cobrava errado, auto-checkout dava troco incorreto |

## Consequências operacionais

- CDs transbordando de estoque enquanto prateleiras das lojas ficavam vazias
- Target teve que alugar galpões extras → impossível rastrear itens
- Reposição manual nas 3 lojas-piloto (sistema desligado por meses)
- Analistas desligavam o reabastecimento automático para esconder ruptura de estoque

## Outros agravantes

- Prazo absurdo: cronograma de 124 lojas até fim de 2013 era irreal
- Sistema de checkout (Retalix) nunca foi substituído apesar dos bugs
- Preços mais altos e menos variedade do que nas lojas americanas
- Ferramenta de validação de dados no SAP instalada tarde demais (2014)

## Lição central

> Sistemas de informação não funcionam sem **dados de qualidade**. A velocidade de expansão sacrificou a integridade dos dados → os sistemas fizeram cálculos errados → a operação colapsou.  
> Internacionalizar sistemas (moeda, métricas, idioma) é complexo e subestimado.  
> Implementar ERP de grande porte em 2 anos é inviável.
