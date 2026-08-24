---
materia: TecnologiaDadosNegocios
data: 2026-08-14
tema: Sistemas integrados de gestão (ERP, CRM, SCM, BI, gestão do conhecimento) e desafios de implementação
tags: [resumo]
---

## Conceitos-chave

| Item | O que é |
|---|---|
| [[Sistemas Integrados de Gestão]] | Plataformas que conectam áreas e dados da empresa numa única plataforma, pra todo mundo ter a mesma versão da informação. Lógica multissistema: ERP é o guarda-chuva, os demais são especializados e se integram a ele. |
| [[ERP]] | Integra os principais processos numa só plataforma (compras, financeiro, RH, vendas, entregas, estoque, relatórios). Tem módulo básico de tudo; função especializada exige sistema dedicado integrado. Ex: SAP, Oracle, TOTVS, Microsoft Dynamics. |
| [[SCM]] | Gestão da cadeia de suprimentos, do fornecedor ao consumidor final, com rastreabilidade e visibilidade da cadeia inteira. Evita excesso de estoque e falta de produto na prateleira. |
| [[CRM]] | Gestão da relação com clientes e [[Prospect|prospects]] ao longo do ciclo comercial. Ex: Salesforce (o mais comum), HubSpot, RD Station. |
| [[Business Intelligence]] | Tecnologias e processos que transformam dado bruto em informação pra decisão: KPIs, dashboards. Ex: Power BI, Tableau, Qlik. |
| [[Gestão do Conhecimento]] | Capturar, organizar e compartilhar o conhecimento gerado na empresa: intranets, wikis internos, repositórios de práticas, e-learning. Menos comum nas empresas. |
| [[Conhecimento Explícito]] | Facilmente estruturado e documentado: missão, visão, códigos de conduta, manuais, tutoriais. |
| [[Conhecimento Tácito]] | Interpretação pessoal do explícito com base na vivência. Difícil de capturar; vai embora junto quando o funcionário sai. |
| [[Prospect]] | Candidato a cliente: pesquisou ou cotou mas não comprou. Também chamado de lead (vai aparecer em marketing). |
| [[Omnichannel]] | Múltiplos canais de comunicação com o cliente (telefone, e-mail, reunião, redes sociais), todos monitorados e gerenciados. |
| [[Cross-selling]] | Venda cruzada de complementares: computador + mouse. |
| [[Upselling]] | Vender versão melhor e mais cara: trocar iPhone 7 por iPhone 10. |
| [[Lock-in]] | Dependência do fornecedor: implementação de ERP leva de 2 a 5 anos, trocar de SAP pra Oracle depois não funciona. |
| [[Garbage In Garbage Out]] | Lixo entra, lixo sai: dado errado ou desatualizado gera análise sem valor. Vale pra BI e pra IA generativa (treinada na internet, cheia de garbage, filtrar é com você). |
| [[Blockchain]] | Tecnologia emergente da próxima aula: rastreabilidade de matéria-prima na cadeia (origem da carne, pedras preciosas). |

## Tipos de ERP

| Tipo | Onde roda | Trade-off |
|---|---|---|
| On-premises | Servidores da própria empresa | Opção mais cara: exige equipe de TI própria pra gestão e atualização |
| Nuvem | Servidores do fornecedor (SAP, Oracle) | Fornecedor cuida de atualização e gestão; empresa só acessa via internet |
| Híbrido | Parte na empresa, parte no fornecedor | Custo e desafio intermediários, depende do tipo de negócio |

A escolha depende do tamanho da empresa E do tipo de negócio.

## Os 4 tipos de CRM (questão de prova declarada)

| Tipo | Função |
|---|---|
| Operacional | Automação do dia a dia de vendas e marketing: a parte mecânica da área comercial |
| Analítico | Interpreta dados e gera insights sobre clientes pra aumentar receita |
| Estratégico | Analisa comportamento histórico pra direcionar campanhas, upselling e cross-selling |
| Colaborativo | Alinha todas as áreas da empresa em torno do cliente (ex: Amazon é top 10, empresa inteira prioriza) |

## Etapas do CRM

1. Identificar o cliente
2. Diferenciar e segmentar (o que compra, quanto gasta, prazo, preço vs qualidade)
3. Interagir e atender, guardando histórico ([[Omnichannel|omnichannel]])
4. Personalizar o atendimento

## Ajustes de implementação de ERP (glossário do Eclass)

| Termo | Significado |
|---|---|
| Parametrização | Ativar dentro do sistema os módulos que a empresa quer usar |
| Customização | Ajustar o sistema pra contemplar etapa do negócio não prevista |
| Tropicalização | Adaptação local, tipicamente tributação (EUA e Brasil são totalmente diferentes) |

## Como os sistemas se integram

- ERP registra a operação: venda, produção, estoque, financeiro
- CRM gerencia o relacionamento com quem compra
- SCM coordena abastecimento e logística com base nesses dados
- Gestão do conhecimento captura o aprendizado da operação pra reuso futuro
- BI entra no final: extrai dados de todos e gera informação pra decisão
- Conexão entre eles: APIs, middlewares (camadas intermediárias) e data warehouses (silos que concentram e estocam)

## Desafios por sistema

| Sistema | Desafios |
|---|---|
| ERP | Custo e tempo (mapear todos os processos), resistência dos funcionários, reengenharia de processos, [[Lock-in|lock-in]] de fornecedor, parametrização/customização/tropicalização |
| SCM | Complexidade da cadeia, visão holística difícil, custo de integração |
| CRM | Adoção pela área comercial (disciplina de inserir dados), qualidade e atualização dos dados, privacidade e segurança (não ser invasivo: o tênis que persegue no Facebook) |
| BI | Ter os KPIs certos: dashboard de 1 página, não relatório de 50 folhas |
| Gestão do Conhecimento | Segurança e propriedade intelectual (acesso total torna a empresa vulnerável), engajamento, captura do tácito |

Integração entre todos: resistência cultural, falta de planejamento estratégico (tempo/custo mal planejado, pressa) e dados inconsistentes (garbage in, garbage out).

## Pegadinhas / pontos de prova

- Os 4 tipos de CRM são questão de prova declarada pela professora.
- ERP é a FONTE dos dados; BI é a ANÁLISE. BI não centraliza nem integra informação. Se a prova disser que BI integra, está errado.
- Dado sozinho não é decisão (frase em vermelho): dado vira informação, que gera conhecimento, que sustenta a decisão ([[Dado, Informação e Conhecimento]]).
- Os sistemas nunca funcionam isolados (frase em vermelho): trocam dados via APIs, middlewares e data warehouses.
- ERP tem módulo básico de CRM e logística, mas relacionamento e cadeia bem feitos exigem CRM e SCM dedicados, integrados ao ERP.
- Dashboard: resumo ou infográfico em UMA página; board vê 1 a 2 slides no máximo.
- Drill down: funil do macro (1,5 bi de vendas/mês) pro micro (100 mi em automóveis).
- Desta aula, só o slide-síntese com a arvorezinha vermelha cai na prova, segundo a professora.

## Caso Target Canadá (atividade avaliada, entregue em sala)

- [[Caso Target Canada|Target Canadá]]: varejista americana fracassou violentamente na expansão pro Canadá. Base da Atividade Monitorada 1, feita e entregue em sala em 14.08 (na mão, no papel, 9 equipes de 5).
- Q1 (4 pts): marcar no texto problemas de tecnologia, pessoas, processos, dados e gestão (pelo menos 5 de cada no texto, podem se sobrepor, apresentar pelo menos 3 de cada).
- Q2 (5 pts): o fracasso foi mais tecnologia, pessoas ou processos? Um parágrafo com evidência do texto. Identificação vale 1 pt.
- Material do caso em `Material/` nesta pasta.

## Pra fixar

- [[Sistemas Integrados de Gestão]]
- [[ERP]]
- [[CRM]]
- [[SCM]]
- [[Business Intelligence]]
- [[Gestão do Conhecimento]]
- [[Conhecimento Tácito]]
- [[Conhecimento Explícito]]
- [[Lock-in]]
- [[Prospect]]
- [[Omnichannel]]
- [[Cross-selling]]
- [[Upselling]]
- [[Garbage In Garbage Out]]
- [[Blockchain]]
- [[Dado, Informação e Conhecimento]]
- [[Caso Target Canada]]

## Próxima aula

- Blockchain, dentro de tecnologias digitais emergentes, com aplicação em rastreabilidade da cadeia de suprimentos. Obs: pelo calendário FGV, o tema "Indústria 4.0 e Tecnologias Digitais Emergentes (IA, IoT, Digital Twin, Blockchain)" está no slot de 28.08; o slot de 21.08 estava reservado pra Atividade Monitorada, que a professora já aplicou em sala em 14.08.
- Trazer o caso impresso nas próximas aulas (recomendação dela).
- A última aula, de IA, vai ensinar a criar prompt.
