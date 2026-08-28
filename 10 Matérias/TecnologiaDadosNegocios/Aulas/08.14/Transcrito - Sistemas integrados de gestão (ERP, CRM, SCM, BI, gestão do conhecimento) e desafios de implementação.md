---
materias: [tecnologia-dados-negocios]
semestre: 2026.2
data: 2026-08-14
tipo: transcrito
tema: Sistemas integrados de gestão (ERP, CRM, SCM, BI, gestão do conhecimento) e desafios de implementação
status: completo
contract_version: 1
topicos: [Sistemas Integrados de Gestão, ERP, CRM, SCM, Business Intelligence, Gestão do Conhecimento, Conhecimento Tácito, Conhecimento Explícito, Lock-in, Prospect, Omnichannel, Garbage In Garbage Out, Caso Target Canada]
tags: [aula, transcrito]
---

## O problema da informação isolada

Se vocês tivessem que assumir a gestão de uma empresa hoje, onde cada setor tem planilhas para controlar a informação de forma isolada e separada, quais seriam os problemas que apareceriam? Olhem para a figura: o que vocês imaginam que aconteceria em cada setor utilizando a informação de forma separada e independente?

Se eu não passasse para vocês as informações da aula no Eclass, nem comunicasse dia de prova, o que aconteceria com vocês? Eu vou adicionar uma palavrinha ao que o Lucas falou: integração. As pessoas perderiam a visão do todo. Eu sou do departamento de vendas e não sei o que acontece na contabilidade ou na área de marketing, eu perco a visão do que acontece na empresa.

Mais um exemplo. Digamos que eu peço para a Giovana buscar uma maçã para mim, mas o Pedro não sabe que ela buscou, e eu peço: Pedro, dá para alguém ir buscar uma maçã? Os dois vão lá buscar a maçã. Duas pessoas fazendo a mesma coisa é retrabalho, e o retrabalho gera perda de eficiência.

Então, se cada área trabalha de forma isolada, nós vamos ter retrabalho e dados inconsistentes, porque eu não sei se o que o Rodrigo me passou é o que vale ou se o que a Catarina me passou é o que vale: cada um tem uma versão da informação. E, o mais importante, temos a dificuldade de integração entre a informação da empresa.

## Sistemas integrados de gestão

Os sistemas servem para interligar os setores e fazer com que a informação flua dentro da empresa de forma única, e que todos tenham, o mais importante, a mesma versão da informação.

O ápice disso são os [[Sistemas Integrados de Gestão|sistemas integrados de gestão]]: plataformas que conectam as áreas e os dados da empresa em uma única plataforma. Os exemplos são o [[ERP]], que é o Enterprise Resource Planning, o [[CRM]], que é o Customer Relationship Management, o [[SCM]], que é o Supply Chain Management, o [[Business Intelligence|BI]] e os sistemas de gestão de conhecimento, ou Knowledge Management Systems.

O ERP atua como um guarda-chuva que integra todas as demais áreas. Os demais sistemas são altamente especializados: servem para gerar a informação específica de cada área e complementar essa integração. Eles são integrados numa coisa que chamamos de lógica multissistema: uma solução específica integrada a outras, com um sistema-mãe, o guarda-chuva, integrando isso tudo.

## ERP (Enterprise Resource Planning)

O ERP é o guarda-chuva-mãe. Ele integra numa só plataforma os principais processos de uma empresa. Tem módulos básicos para operação e finanças: vai controlar a contabilidade e toda a cadeia da operação, desde que uma ordem de compra ou de serviço entra na empresa até que ela saia.

No exemplo vocês veem os módulos: compras, financeiro, recursos humanos, vendas, CRM, controle de entregas, clientes, relatórios e gráficos e controle de estoque. Embora o ERP seja uma solução mãe que tem tudo, ele tem o módulo mais básico das unidades específicas. Se eu quero ter um relacionamento melhor com os meus clientes, além do módulo dele eu vou ter que ter um CRM e integrá-lo a ele depois. A mesma coisa vale para a parte de logística.

O objetivo é integrar toda a informação dentro da empresa, evitar a divergência de informação, facilitar as decisões, evitar retrabalho e, o principal, reduzir os erros e os custos gerados por esse retrabalho. Exemplos: SAP, Oracle, TOTVS e Microsoft Dynamics. A escolha do tipo de ERP vai depender não só do tamanho da empresa, mas também do tipo de negócio dela. Nem todas as soluções são adequadas para todos os negócios.

## Tipos de ERP

Existem três categorias. A primeira é o on-premises: toda a solução hospedada nos servidores da companhia, no local. É a opção mais cara, porque demanda que a empresa tenha uma equipe de TI para gerenciar isso e cuidar da atualização.

A segunda é a solução em nuvem, onde a solução fica hospedada no servidor do fornecedor. Eu posso comprar o ERP da Oracle ou da SAP, mas ele fica hospedado nos servidores da SAP, e quem controla tudo em termos de atualização e gestão é o próprio fornecedor: eu simplesmente acesso o meu sistema pela internet.

A terceira é a híbrida: parte fica instalada na empresa e parte é disponibilizada pelo fornecedor. Cada solução vai ter um custo e vai trazer uma dificuldade e um desafio. Vai depender de cada tipo de negócio.

## Desafios de implementação do ERP

Primeiro, custo e tempo de implementação: não é uma coisa trivial, você precisa mapear todos os processos da empresa e entender se todos eles estão espelhados dentro daquele sistema.

Segundo, resistência dos funcionários: muitas vezes as empresas operam de uma forma mais orgânica, mais analógica, e as pessoas são resistentes a adotar esse tipo de processamento de informação.

Terceiro, reengenharia de processos: às vezes temos que adaptar processos que não funcionam corretamente para que eles se moldem ao sistema.

Quarto, dependência de fornecedor. Isso nós vamos ver mais para frente no módulo de economia da informação, que é o famoso [[Lock-in]]: eu fico dependendo de um fornecedor. Não posso gastar zilhões de moedas para implementar um sistema por dois a cinco anos e, de repente, mudar de ideia, "não gostei desse, vou sair da SAP e ir para a Oracle". Isso não funciona. Eu acabo ficando presa no fornecedor que escolhi.

E por fim, ajustes necessários: parametrização, customização e tropicalização. No Eclass, toda aula eu deixo um glossário de termos, e é importante que vocês saibam o que cada um significa. Parametrização é ativar dentro do módulo o que eu quero: o ERP mãe da Oracle ou da SAP vem com módulo de vendas, de finanças, de controladoria, de contabilidade, e eu ativo o que eu quero que esteja funcionando. Customização é quando eu tenho alguma etapa complementar que não está prevista nesse sistema, então tenho que fazer um ajuste para que o meu negócio esteja contemplado. E a tropicalização normalmente envolve a parte de tributação: o ERP nos Estados Unidos é carregado com um tipo de tributação que no Brasil é totalmente diferente.

## SCM (Supply Chain Management)

O Supply Chain Management, ou gestão da cadeia de suprimentos, como o nome já diz, vai gerir toda a cadeia de suprimentos, incluindo a parte de logística, que é um item dela, desde o fornecedor até o consumidor final.

Eu pus o desenho para vocês fazerem associação e lembrarem: eu faço a rastreabilidade da matéria-prima, do fabricante, do distribuidor, do atacadista e do varejista até chegar no usuário final, que é o consumidor. Eu tenho visibilidade de como tudo isso ocorre.

Nós vamos ver na próxima aula que o [[Blockchain|blockchain]], que é uma das tecnologias digitais emergentes, serve para fazer rastreabilidade de matéria-prima: entender se a carne que eu estou comprando vem de um fornecedor bom ou não, se as pedras preciosas que eu uso para fabricar joias vêm de meios corretos e oficiais ou de mecanismos expulsos do mercado, do mercado negro. O blockchain ajuda muito a complementar isso.

O objetivo é reduzir custo, promover agilidade e ter visibilidade da cadeia inteira. Prestem atenção, porque isso aparece no caso de hoje: o Supply Chain Management ajuda muito a evitar que tenha muito produto em estoque ou que falte produto na prateleira. Que eu tenha exatamente a conta certa que eu devo ter para que o meu negócio funcione. Os desafios são a complexidade da cadeia por si só (é muito difícil fazer a rastreabilidade de tudo isso e ter essa visão holística) e o custo de integração.

## CRM (Customer Relationship Management)

O próximo sistema, um dos mais comuns e utilizados, é o Customer Relationship Management, que serve para fazer todo o gerenciamento da relação com clientes e [[Prospect|prospects]] ao longo de todo o ciclo comercial.

Vocês sabem o que é um prospect? É um candidato a cliente. Sempre que um consumidor fez uma pesquisa, fez uma cotação, mas acabou não comprando, ele não é meu cliente: nós o chamamos de prospect, ou lead. É bom vocês começarem a se familiarizar, porque nas matérias de marketing vocês vão ver bastante. Prospect é todo cliente que não é cliente, um cliente em potencial.

O CRM vai fazer a gestão de todo o relacionamento: como eu me comunico, o que esse cliente compra, o que ele gosta, o que ele não gosta, o que ele reclamou nos canais. Eu tenho uma visão específica dessa parte do negócio. Exemplos: Salesforce, que é o mais comum, HubSpot e RD Station.

## Os quatro tipos de CRM

Nós temos quatro tipos de CRM e é importante que vocês saibam disso. *(Atenção: a professora avisou que isso é questão de prova.)*

O CRM operacional faz a automação do dia a dia de vendas e marketing: como o nome já diz, ele faz a parte mecânica da área comercial.

O CRM analítico serve para interpretar os dados e gerar insights sobre esses clientes: eu pego todas as reclamações que tem no meu sistema, quanto esse cliente compra, o que ele compra, o que ele gosta e o que ele não gosta, e gero informação para tentar aumentar a minha receita.

O CRM estratégico analisa o comportamento histórico dos clientes, justamente para direcionar campanhas de marketing e fazer upselling e cross-selling. [[Cross-selling]] é venda cruzada: vocês compram um computador, eu vendo um mouse junto, são coisas complementares. [[Upselling]] é quando eu estou vendendo uma versão melhor e mais cara: vocês têm um iPhone 7 e resolvem comprar um iPhone 10, uma versão mais sofisticada, mais moderna e mais cara. Isso é curiosidade, mas esses termos vão surgir.

E por fim, o CRM colaborativo ajuda todas as áreas da empresa a alinhar os esforços em torno desse cliente. Digamos que eu seja uma empresa de serviços de comunicações e tenho um cliente como a Amazon, que está com um problema no momento, e a Amazon é um dos meus dez maiores clientes. Se eu tenho um CRM colaborativo na empresa toda, a empresa inteira sabe que a Amazon é top 10, precisa se mobilizar para atendê-la e priorizar. Para isso serve.

## Etapas e desafios do CRM

O objetivo é óbvio: satisfação, fidelização, lealdade e aumentar a receita de vendas. As etapas de um CRM: primeiro, identificar quem é meu cliente. Depois, diferenciar e segmentar: saber o que ele compra, quanto gasta, com que prazo quer ser atendido, que tipo de qualidade exige ou não, se compra por preço ou por qualidade. Depois, atender, interagir e guardar o histórico.

Vocês sabem o que é um canal [[Omnichannel|omnichannel]]? Eu tenho múltiplos canais de comunicação com o cliente: telefone, e-mail, reunião, redes sociais que eu tenho que ficar monitorando, porque eles podem reclamar de mim lá, não necessariamente nas redes sociais da empresa. Eu tenho que gerenciar tudo isso.

E no final, personalizar, que é a etapa final: poder dar um atendimento específico para ele. Saber que a Luana gosta de comprar um perfume específico, com traços florais ou cítricos, e que custa até X dólares.

Os desafios aqui são um pouquinho diferentes dos outros dois sistemas. Primeiro, a adoção pela área comercial: a área comercial naturalmente tem um problema em inserir os dados no sistema, e essa disciplina é importantíssima. Segundo, qualidade e atualização dos dados: não adianta nada eu ter a informação do cliente se, na hora de mandar a nota fiscal, o endereço está errado e a nota não chega. Terceiro, privacidade e segurança desses dados: eu não posso ser invasiva nem manipuladora com os clientes, embora muitas empresas façam isso. Quantas vezes vocês entraram no Facebook, procuraram um tênis, e cada vez que abrem começam a aparecer as janelinhas com aquele tênis, como se vocês fossem eternamente comprar o mesmo tênis? Isso é um bom exemplo do que não se deve fazer.

## Business Intelligence

Depois nós temos o Business Intelligence, o famoso BI. O BI reúne várias tecnologias e processos para pegar todos esses recursos brutos que eu coletei dos clientes e da minha operação e gerar informação para tomada de decisão. Através disso eu consigo fazer monitoração do desempenho, através dos famosos KPIs, e consigo compartilhar na empresa todos os dados, obviamente por zonas de classificação de acesso à informação.

Frase em vermelho, importantíssima: o dado sozinho não é uma decisão. Lembram da primeira aula? "Produto A" é um dado. O que isso fala? Nada. O que importa é que ele é um insumo, uma matéria-prima para a tomada de decisão. O dado precisa ser transformado em informação que gera conhecimento para virar decisão. É a lógica de [[Dado, Informação e Conhecimento|dado, informação e conhecimento]].

E importante aqui é a comparação com o ERP. O ERP vai ser a fonte dos dados, e o BI envolve a análise desses dados. Então cuidado: o BI não centraliza e não integra a informação. Ele vai analisar essa informação. *(Pegadinha de prova: quem integra é o ERP; o BI analisa.)*

Exemplos: Power BI, Tableau e Qlik. O objetivo, como já discutimos, é apoiar a decisão e fazer monitoramento da performance.

A título de curiosidade, a análise drill down é um funil: eu saio de uma informação ampla e chego numa informação granulada. Digamos que eu sei que estou vendendo 1,5 bilhão em produtos por mês, e embaixo eu especifico que 100 milhões são relacionados a automóveis, 200 a outra categoria, e assim por diante. Saio de uma informação macro e chego numa informação micro: isso é drill down. Temos também o OLAP, que é o processamento analítico online, e o data mining, que é outra técnica que vocês vão ver mais para frente.

Os desafios: primeiro, ter indicadores de performance corretos em mãos, porque não adianta eu gerar um relatório de 50 folhas com informação que vai entupir o cérebro de vocês. Eu preciso ter o que nós chamamos de dashboard, que é o resumo ou infográfico em uma página. É isso que as empresas fazem: as reuniões do board têm no máximo um ou dois slides com o resumo de toda a informação que interessa para a companhia. Saber fazer isso, e vocês vão fazer isso hoje na segunda etapa da aula, também é uma arte.

## Gestão do conhecimento

Por último, nós temos os sistemas de [[Gestão do Conhecimento|gestão do conhecimento]]. Eles são menos comuns, nem todas as empresas têm, mas servem para capturar, organizar e compartilhar todo o conhecimento que é gerado dentro de uma empresa.

Eles envolvem dois tipos de conhecimento. O [[Conhecimento Explícito|explícito]] é o que pode ser facilmente estruturado e documentado dentro de uma empresa: missão, visão, objetivos, códigos de procedimento e de conduta, até manuais ou tutoriais, como mexer no Eclass, por exemplo. O [[Conhecimento Tácito|tácito]] é mais difícil e desafiador de capturar, porque ele é a interpretação pessoal que cada um faz daquele conhecimento explícito, com base na vivência. A minha vivência, experiência e bagagem de conhecimento são diferentes das da Giovana, da Sofia e do Caio. Cada um tem uma experiência diferente, e isso dificulta muito compartilhar.

Isso é um risco: quando um profissional sai da empresa e eu não tenho esse compartilhamento de conhecimento, a pessoa leva esse conhecimento junto com ela e a empresa perde. Hoje esse compartilhamento é feito através de softwares: intranets corporativas, wikis internos, repositórios de melhores práticas, sistemas de e-learning. Muitas empresas adotam procedimento padrão, por exemplo na área de vendas: o procedimento para vender para um cliente é esse, as pessoas precisam fazer aquele treinamento e estar em compliance com ele.

Outro exemplo: eu sou o vendedor da Amazon, mas a Laura vai fazer uma visita lá essa semana. Ela pode entrar na plataforma e ver tudo o que eu vendi para a Amazon, tudo o que a Amazon reclamou, o que ela comprou, o que ela gostaria de receber. Quando ela for, já vai ter todo esse conhecimento.

Mas, como eu tenho esse compartilhamento de tudo, qual é o grande risco? Segurança e propriedade intelectual. Numa empresa, eu não posso compartilhar para fora o conhecimento dela: isso é reino de espionagem, de vazamento de informações. Se eu tenho acesso a toda a informação da empresa, eu torno a empresa um tanto quanto vulnerável. Esse é um dos motivos pelos quais boa parte das empresas ainda não tem essa prática. Os outros desafios são o engajamento no compartilhamento e, justamente como falei, a captura do conhecimento tácito.

## Como os sistemas se integram na prática

Eu preparei um slide com a síntese de tudo: o objetivo de cada um dos sistemas, os benefícios que eles trazem e os desafios. *(Atenção: a professora disse que, para a prova, desta aula só precisa estudar esse slide-síntese, o que está marcado com a arvorezinha vermelha. Não precisa olhar os outros.)*

E por fim, o importantíssimo: como esses sistemas se integram na prática. O ERP registra a operação: a venda para o cliente, a produção, o estoque e o financeiro. O CRM gerencia o relacionamento com quem compra. O SCM coordena o abastecimento e a logística com base nesses dados. A gestão do conhecimento captura o aprendizado gerado nessa operação para reaproveitar na aprendizagem futura. E o BI entra no final do processo: ele extrai o dado de todos esses sistemas para gerar a informação que vocês vão precisar para tomar decisões.

Deixei em vermelho, importantíssimo: eles não funcionam de forma isolada. Eles estão integrados, trocam dados constantemente, e essa conexão é feita através de interfaces de aplicação, que são as famosas APIs, ou middlewares, que são camadas intermediárias que servem para fazer um sistema conversar com o outro, ou data warehouses, que são silos de informação, servidores que vão concentrar e estocar toda essa informação.

Quais são as principais dificuldades para integrar esses sistemas? Resistência cultural das pessoas. Falta de planejamento estratégico: a pessoa planejou errado o tempo ou o custo, ou quis apressar o processo. E dados inconsistentes. Vocês já ouviram a expressão [[Garbage In Garbage Out|garbage in, garbage out]]? Vocês vão ver nas próximas matérias de estatística e de dados: se eu jogo lixo dentro do sistema, e lixo quer dizer informação errada ou desatualizada, na hora que eu pedir para a minha IA fazer uma análise, o que vai sair é uma coisa sem sentido, sem valor.

Isso serve de alerta para vocês, que são usuários de Gemini, ChatGPT, Claude e outros. Lembrem-se de que essas plataformas são treinadas na internet, não só em bases confiáveis. Então elas têm muito garbage, e vocês precisam saber filtrar para tirar uma coisa de valor. Nós vamos ver na última aula, de IA, como criar um prompt.

## Atividade: o caso Target Canadá

Agora a atividade prática, sobre o [[Caso Target Canada|caso Target Canadá]]. A Target é uma cadeia famosa de varejo dos Estados Unidos que tentou implementar a operação no Canadá, a Target Canadá, e fracassou violentamente.

Organização: nove equipes de cinco pessoas, notebook fechado, celular guardado. O trabalho é na mão, no papel, e vocês me entregam antes de sair da sala. Eu trouxe nove casos impressos, um para cada equipe. Nas próximas aulas, eu aconselho vocês a trazerem o caso impresso.

Primeira parte: identifiquem no texto todos os problemas que aconteceram relacionados a tecnologia, pessoas, processos, dados e gestão, pintando cada categoria com uma canetinha de cor diferente. Tem no texto pelo menos cinco itens de cada, e eles podem se sobrepor: um erro de uma pessoa pode ser também um problema de gestão. Vocês têm que me apresentar pelo menos três de cada, e não precisa copiar a frase inteira: um bullet curto resume, tipo "a tecnologia não funcionou por causa disso".

Segunda parte: com base nisso, entendam o que funcionou e o que não funcionou e respondam: o fracasso foi mais culpa da tecnologia, das pessoas ou dos processos? Não quero um jornal, quero um parágrafo, com evidência do texto. Não precisa procurar fora do texto.

Pontuação: a primeira questão vale 4 pontos, a segunda vale 5 e a última vale 1. No final da aula, entreguem o caso pintado e a folhinha de respostas com identificação, pelo menos o nome de uma pessoa do grupo.
