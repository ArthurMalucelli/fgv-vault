# Aula 02 — SI e Sistemas Integrados

*Fonte: PPT 2_SIs Integrados.pdf — publicado no Eclass em 07/08/2026*
*Aula: 14/08/2026 | Prof. Suely Fischer Omura*

---

## Tópicos

**Sistema de Informação (SI)**
- Conjunto de pessoas, processos, dados e tecnologia para coletar, processar, armazenar e distribuir informação que apoia a tomada de decisão e controle organizacional
- Problema central: dados em silos → retrabalho, inconsistência, falta de visão única do negócio

**Sistemas Integrados de Gestão (SIG)**
Plataformas que conectam áreas e dados da empresa para otimizar a gestão. Dois modelos:
- Centralizador (ex: ERP) → uma única plataforma para tudo
- Multissistema → vários sistemas especializados integrados entre si

| Sistema | Foco | Exemplos |
|---------|------|----------|
| ERP | Integra todos os processos centrais (finanças, estoque, RH, vendas) | SAP, Oracle, TOTVS, Microsoft Dynamics |
| SCM | Coordenação estratégica da cadeia de suprimentos: fornecedor → cliente | — |
| CRM | Relacionamento com o cliente: marketing, vendas, atendimento | Salesforce, HubSpot, RD Station |
| BI | Transforma dados brutos em relatórios, dashboards e KPIs para decisão | Power BI, Tableau, Qlik |
| SGC/KMS | Captura e compartilha conhecimento tácito e explícito da organização | Wikis, intranets, e-learning |

**ERP — detalhe**
- Tipos: on premises (licença + servidores próprios), nuvem (hospedado pelo fornecedor), híbrido
- Desafios reais: custo/tempo de implementação, resistência cultural, reengenharia de processos, dependência de fornecedor, parametrização/customização/tropicalização

**CRM — detalhe**
- Etapas: identificar → diferenciar (segmentar) → atender/interagir/guardar histórico (omnichannel) → personalizar
- Não é só banco de dados de clientes: é estratégia de negócio centrada no cliente

**BI — ponto crítico**
- Dado não é decisão, é insumo para decisão. ERP = fonte; BI = análise
- Erro comum: confundir correlação com causalidade; ignorar validade externa de análises

**SGC — conhecimento tácito vs. explícito**
- Explícito: pode ser documentado (manuais, BDs, procedimentos)
- Tácito: reside em experiência e intuição — depende de interação social para ser compartilhado

**Integração: fluxo típico**
ERP (registra operação) → SCM (abastecimento/logística) → CRM (relacionamento com clientes) → BI (relatórios/decisão) → SGC (captura aprendizado)
ERP é o núcleo ("espinha dorsal"), os demais se conectam via APIs, middlewares ou data warehouses.

**Dificuldades na integração**
- Resistência cultural e treinamento insuficiente
- Falta de planejamento estratégico (escopo mal definido → estoura prazo/orçamento)
- Dados inconsistentes ("lixo entra, lixo sai")
- Custo de gestão, manutenção e compliance (ISO, segurança)

---

## ⚠️ Atividade em Sala — Estudo de Caso: Target Canada

**Formato:** trabalho em grupo de 5 pessoas | 30 min de análise | apresentação de 3 min por grupo (1 porta-voz)

**Roteiro de perguntas:**

**a) O fracasso da Target Canada ocorreu mais por culpa da tecnologia, das pessoas ou dos processos? (4,0 pts)**

Argumento principal: o fracasso foi sistêmico, mas o fator humano/processo foi dominante. A tecnologia (ERP SAP, sistema de dados) era capaz — o problema foi a implementação apressada, dados de produto corrompidos desde o início (erros em 70% dos itens), e decisões de gestão que ignoraram sinais de alerta.
- Tecnologia: SAP implementado sem dados limpos; sistema legado canadense incompatível; campos mal preenchidos geraram pedidos errados, excesso e falta simultâneos
- Pessoas: equipe inexperiente, sem tempo de treinamento; cultura de não questionar decisões da liderança; consultores externos sem accountability
- Processos: migração de dados feita manualmente e de forma descuidada; sem processo de validação de qualidade de dados; expansion plan agressivo demais (124 lojas em < 2 anos)
- Dados: inconsistência nos cadastros de produtos (preços, dimensões, fornecedores) → prateleiras vazias mesmo com estoque no depósito
- Gestão: deadline político (inaugurar lojas) sobrepôs prontidão operacional; sem piloto adequado antes do rollout em massa

Conclusão para defender: falha de gestão e processos. A tecnologia falhou como consequência, não como causa raiz.

**b) Problemas por categoria: (5,0 pts)**

- **Tecnologia:** SAP mal configurado; dados de entrada incorretos; integração entre sistemas legados canadenses e o ERP americano falhou; sistema não escalou para o volume de SKUs necessários
- **Pessoas:** time de TI sobrecarregado e inexperiente com SAP; sem treinamento adequado dos operadores; cultura hierárquica que silenciava alertas dos analistas
- **Processos:** migração de dados sem protocolo de validação; sem fase de piloto; processo de pedidos automáticos baseado em dados errados → pedidos fantasmas e rupturas simultâneas
- **Dados:** +70% dos produtos com dados incorretos (preço, tamanho, fornecedor); sistema de reposição automática gerou ordens erradas; sem processo de limpeza e governança de dados
- **Gestão:** deadline de inauguração das 124 lojas foi político, não operacional; sem go/no-go baseado em métricas de prontidão; ausência de responsabilização (accountability) clara por falhas de dados

**Entrega escrita:** até 3 páginas, uma entrega por equipe, via Eclass, até **20/08**

---

## Leitura Complementar

- Laudon & Laudon (2022). *Sistemas de informação gerenciais* (17ª ed.). Pearson.
- Luca & Edmondson (2024). Where data-driven decision-making can go wrong. *HBR*.

---

## Aviso Relacionado (07/08)

Prof. Suely lembrou: enviar composição dos grupos para **suely.omura@fgv.br** (até 07/08 poucos grupos tinham enviado). Também solicitou leitura do estudo de caso da Target Canada para a próxima aula.
