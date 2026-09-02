
# 1o passo - importar os dados do excel

# 2o passo - Rodar a regressao
# no exemplo de revisao para o quiz2, o arquivo excel se chama data_Q2_review 
# Temos 20 observacoes de 2 variaveis - Vendas e Publicidade.

regressao <- lm(Vendas ~ Publicidade, data = data_Q2_review)
summary(regressao)


# 3o passo - Identificar o intervalo de confianca e predicao para um valor de x
observacao <- data.frame(Publicidade = 38.99)
IC <- predict(regressao, newdata = observacao, interval = "confidence")
IP <- predict(regressao, newdata = observacao, interval = "prediction")
