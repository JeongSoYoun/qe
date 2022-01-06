
# QuantStart
# Advanced Algorithmic Trading
# Michael L. Halls-Moore, PhD
# Part3 - Chapter 11

# TESLA DATA
library(forecast)
require("quantmod")
getSymbols("TSLA", from = "2013-01-01")
tsla_df <- TSLA

tsla_log_rt_diff <- diff(log(Cl(tsla_df)))

# Find order based on AIC

print("Finding order based on AIC...")
aic <- Inf
order <- c(0, 0, 0)
for (p in 1:4) {
    for (d in 0:1) {
        for (q in 1:4) {
            temp_aic <- AIC(arima(tsla_log_rt_diff, order = c(p, d, q)))

            if (temp_aic < aic) {
                aic <- temp_aic
                order <- c(p, d, q)
                arima <- arima(tsla_log_rt_diff, order = order)
            }
        }
    }
}

print("Done!")
print("Predicting Value of TSLA after 25 days")
plot(forecast(arima, h = 25))