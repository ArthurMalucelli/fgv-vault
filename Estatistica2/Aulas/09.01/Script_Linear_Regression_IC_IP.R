
# 1o. Import the file (save the excel, and use the "Import Dataset" in the Environment window)

# 2o. Running the regression (the names are for this example - you should change it for your exercise)
# be careful with the way the object and variables names are written - capital letters, etc

regressao <- lm(Vendas ~ Publicidade, data = data_Q2_review)
summary(regressao)

# 3o. Getting the Confidence and Prediction Intervals
# this is for a specific value of X. You will need to change it according to the exercise

observacao <- data.frame(Publicidade = 127.8)
IC <- predict(regressao, newdata = observacao, interval = "confidence")
print(IC)
IP <- predict(regressao, newdata = observacao, interval = "prediction")
print(IP)