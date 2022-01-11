
# QuantStart
# Advanced Algorithmic Trading
# Michael L. Halls-Moore, PhD
# Part3 - Chapter 11
# GARCH model on stock data

require(quantmod)
getSymbols("^FTSE")
log_rt_diff <- diff(log(Cl(FTSE)))
show(plot(log_rt_diff))

df <- as.numeric(log_rt_diff)
df <- df[!is.na(df)]

# fit on ARIMA model
print("Finding order based on AIC...")
final_aic <- Inf
final_order <- c(0, 0, 0)
for (p in 1:4) {
    for (d in 0:1) {
        for (q in 1:4) {
            temp_aic <- AIC(arima(df, order = c(p, d, q)))
            if (temp_aic < final_aic) {
                final_aic <- temp_aic
                final_order <- c(p, d, q)
                final_arima <- arima(df, order = final_order)
            }
        }
    }
}
print("Order of ARIMA model")
print(final_order)

# Clearly, we can see conditional heteroscedastic behavior
# Let's fit on GARCH model

garch <- garch(df, trace = F)
garch_res <- garch$res[-1]
acf(garch_res^2)