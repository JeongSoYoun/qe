
# QuantStart
# Advanced Algorithmic Trading
# Michael L. Halls-Moore, PhD
# Part3 - Chapter 12
# Simulate Cointegrated Time Series

# Create Random Walk Model
# z[t]

library("tseries")
set.seed(123)
z <- rep(0, 1000)
for (t in 2:1000) {
    z[t] <- z[t - 1] + rnorm(1)
}

plot(z, type = "l")
plot(diff(z), type = "l")

# Linear Combination of two non-stationary time series
# ax[t]+by[t] = a(pz[t]+w[x,t]) + b(qz[t]+w[x,t]) # nolint
# ax[t]+by[t] = (ap+bq)z[t] + a * w[x,t]+b * w[x,t]
# if ap + bq = 0 -> we can make non-startionary time series to stationary time series # nolint

x <- y <- rep(0, 1000)
x <- 0.3 * z + rnorm(1000)
y <- 0.6 * z + rnorm(1000)

layout(1:2)
plot(x, type = "l")
plot(y, type = "l")

# make non-stationary to stationary time series

comb <- 2 * x - y
layout(1:2)
plot(comb, type = "l")
acf(comb)

# Augmented Dickey-Fuller test

result_adf <- adf.test(comb)
print(result_adf)

# Phillips-Perron test

result_pp <- pp.test(comb)
print(result_pp)

# Phillips-Ouliaris test

result_po <- po.test(cbind(2 * x, -1 * y))
print(result_po)