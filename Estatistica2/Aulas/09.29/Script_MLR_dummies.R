
# -------------------------------
# MULTIPLE LINEAR REGRESSION
# -------------------------------

dados <- multiple_regression_dataset
rm(multiple_regression_dataset)
modelo_completo <- lm(sales ~ ad_spending + store_size + employees + price_index + region,
                      data = dados)

summary(modelo_completo)

# -------------------------------
# REORDERING THE LEVELS
# -------------------------------

dados$region <- relevel(as.factor(dados$region), ref = "North")
modelo_completo <- lm(sales ~ ad_spending + store_size + employees + price_index + region,
                      data = dados)
summary(modelo_completo)

# -------------------------------
# CORRELATION MATRIX
# -------------------------------

vars_quant <- dados[, c("sales", "ad_spending", "store_size", "employees", "price_index")]
cor(vars_quant)

#-------------------------------
# VIF
# -------------------------------

install.packages("car")   # run once if needed
library(car)

vif(modelo_completo)




# H0: residuals are normally distributed
# H1: residuals are not normally distributed
# ------------------------------
shapiro.test(modelo_completo$residuals)

# Optional: histogram of residuals
hist(modelo_completo$residuals, main = "Histogram of Residuals", xlab = "Residuals")

# Optional: QQ-plot
qqnorm(modelo_completo$residuals)
qqline(modelo_completo$residuals, col = 2)

# ------------------------------
# 3. Breusch-Pagan test
# H0: homoskedasticity
# H1: heteroskedasticity
# ------------------------------
install.packages("lmtest")   # run once if needed
library(lmtest)

bptest(modelo_completo)