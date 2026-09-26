
# Import database
# dados_mlr_apto from eclass


# Running the regression
regression <- lm(responses ~ circulation + adsize, data = dados_mlr_apto)
summary(regression)

