
# QuantStart
# Advanced Algorithmic Trading
# Michael L. Halls-Moore, PhD
# Part3 - Chapter 12
# CADF test on EWC & EWA ETF

library("quantmod")
library("tseries")

# EWA & EWC
getSymbols("EWA", from = "2006-04-26", to = "2012-04-09")
getSymbols("EWC", from = "2006-04-26", to = "2012-04-09")
ewa_adj <- unclass(EWA$EWA.Adjusted)
ewc_adj <- unclass(EWC$EWC.Adjusted)

# plot
plot(
    ewa_adj,
    type = "l",
    xlim = c(0, 1500),
    ylim = c(5.0, 35.0),
    xlab = "April 26th 2006 to April 9th 2012",
    ylab = "ETF Backward-Adjusted Price in USD", col = "blue"
)
par(new = T)
plot(
    ewc_adj,
    type = "l",
    xlim = c(0, 1500),
    ylim = c(5.0, 35.0),
    axes = F,
    xlab = "",
    ylab = "",
    col = "red"
)
par(new = F)

# Perform linear regression between the two series
# Since we don't which is independent & dependent, we need to perform both

comb1 <- lm(ewc_adj ~ ewa_adj)
comb2 <- lm(ewa_adj ~ ewc_adj)

# Then, perform CADF test based on both residuals.
# To find optimal hedge ratio, beta.

print(adf.test(comb1$residuals, k = 1)) # p-value: 0.02851
print(adf.test(comb2$residuals, k = 1)) # p-value: 0.02769

# Both linear regression,
# we have evidence to reject the null hypothesis of the presence of a unit root,
# leading to evidence for a stationary series (and cointegrated pair) at the 5% level.