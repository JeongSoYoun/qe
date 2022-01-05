
# QuantStart
# Advanced Algorithmic Trading
# Michael L. Halls-Moore, PhD
# Part3 - Chapter 10

require(quantmod)

# Financial Data for "AAPL"

getSymbols("AAPL")
df <- AAPL
log_rt_diff <- diff(log(Cl(df)))

# find alpha & beta based on AIC
# Initialize

aic <- Inf
order <- c(0, 0, 0)

for (i in 0:4) {
    for (j in 0:4) {
        temp_aic <- AIC(arima(log_rt_diff, order = c(i, 0, j)))

        if (temp_aic < aic) {
            aic <- temp_aic
            order <- c(i, 0, j)
            arma <- arima(log_rt_diff, order = order)
        }
    }
}

# fit residual of time-series into our model
# check the autocorrelation function

acf(resid(arma), na.action = na.omit)