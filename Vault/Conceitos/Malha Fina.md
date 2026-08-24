---
tipo: conceito
materias: [DireitoEmpresarial]
tags: [conceito, direito, tributos]
---

# Malha Fina

## Definição

Matriz de cruzamento de dados da Receita Federal. Recebe informações de movimentação bancária, cartões de crédito, compra e venda de imóveis, aplicações financeiras e planos de saúde, estima a renda implícita e compara com o imposto pago ("movimentou R$ 100 mil no mês, o imposto seria ~R$ 10 mil, cadê os pagamentos?"). É parametrizada pra priorizar rendas altas: acima do corte, o sistema dispara aviso pro fiscal olhar a declaração e intimar.

## Fórmula / aplicação

Números práticos da aula: movimentação mensal abaixo de ~R$ 10 mil não chama ninguém; na prática dos contadores, ação por sonegação começa em renda mensal na casa de R$ 50 mil. Autuação sem estrutura formal: multa ~75%. Retroação máxima de 5 anos, mas os 5 anos cheios (imposto + multa + juros) consomem o patrimônio inteiro. Daí o racional: abrir empresa e pagar ~10% ("perde um dedo, preserva as mãos").

## Onde aparece nas aulas

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, this.file.link)
SORT file.name DESC
```

## Conceitos relacionados

- [[CNPJ]]
- [[Lavagem de Dinheiro]]
- [[Instituição de Pagamento]]
