
modelo <- lm(Y ~ X, data = rodrigo)
summary(modelo)
residuos <- residuals(modelo)

shapiro.test(residuos)
install.packages("lmtest")
library(lmtest)
bptest(modelo)

novo <- data.frame(X = 6)
IC <- predict(modelo, newdata = novo, interval = "confidence", level = 0.95)
IP <- predict(modelo, newdata = novo, interval = "prediction", level = 0.95)