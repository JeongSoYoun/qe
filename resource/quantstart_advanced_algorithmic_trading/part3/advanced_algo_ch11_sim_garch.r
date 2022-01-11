
# QuantStart
# Advanced Algorithmic Trading
# Michael L. Halls-Moore, PhD
# Part3 - Chapter 11
# Simulate GARCH(1,1) model
# sigma^2(t) = alpha0 + alpha1*epsilon^2(t-1) + beta1*sigma^2(t-1) # nolint

require(tseries)

set.seed(2)
alpha_0 <- 0.2
alpha_1 <- 0.5
beta_1 <- 0.3

# w: Random White Noise Value
w <- rnorm(10000)

# eps,sigsq: 10000 '0' vectors
eps <- rep(0, 10000)
sigma_sq <- rep(0, 10000)

for (t in 2:10000) {
    sigma_sq[t] <- alpha_0 + (alpha_1 * eps[t - 1]^2) + (beta_1 * sigma_sq[t - 1]) # nolint
    eps[t] <- w[t] * sqrt(sigma_sq[t])
}

garch <- garch(eps, trace = FALSE)
print(confint(garch))