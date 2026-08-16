
# Exercise 1
obs <- c(Credit=100, Debit=60, Cash=40)
p_exp <- c(0.45, 0.35, 0.20)

chisq.test(x = obs, p = p_exp)

#####################################################################

# Exercise 2
tab2 <- matrix(c(48,72,
                30,90,
                40,40),
              nrow = 3, byrow = TRUE)

dimnames(tab2) <- list(Channel = c("Email","Social","Search"),
                      Outcome = c("Purchased","NotPurchased"))

tab2
chisq.test(tab2)

####################################################################

# Exercise 3

tab3 <- matrix(c(6,54,
                2,58,
                10,20),
              nrow=3, byrow=TRUE)

dimnames(tab3) <- list(Location=c("A","B","C"),
                      Status=c("Complaint","NoComplaint"))

test <- chisq.test(tab3)
test

# Check expected counts
test$expected

